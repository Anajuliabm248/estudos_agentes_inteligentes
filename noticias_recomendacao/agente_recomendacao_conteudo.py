import random  # faz o sorteio quando as melhores notícias ficam empatadas
import re  # encontra as palavras dos títulos usando um padrão de busca
import unicodedata  # ajuda a retirar os acentos antes de comparar as palavras

import pandas as pd  # lê os arquivos CSV e organiza os dados em tabelas


class Agente:
    # prepara um agente novo, assim cada user recebe sua própria memória
    def __init__(self, conteudos_df, historico_df):
        # conteúdos e histórico são as fontes de dados usadas pelo agente
        self.conteudos_df = conteudos_df
        self.historico_df = historico_df

        # usuário e momento identificam a situação mostrada na execução
        # visualizou e recomendações antigas ajudam a bloquear repetições chatas
        # conteúdos interessantes fornecem os títulos usados na comparação
        # listas de cliques e ignoradas registram eventos para acompanhar o estado
        self.estado = {
            "usuario": 0,
            "momento": 0,
            "visualizou": [],
            "leituras_rapidas": [],
            "conteudos_interessantes": [],
            "clique_recomendacao": [],
            "ignorou_recomendacao": [],
            "recomendacoes_antigas": [],
            "interesses": {
                "Tecnologia": 0,
                "Esportes": 0,
                "Entretenimento": 0,
                "Economia": 0,
                "Educação": 0,
            },
        }

    # separa as notícias que ainda podem participar da escolha
    def selecionar_candidatos(self):
        # o + junta as listas, vloqueando notícias já recomendadas ou visualizadas de serem repetidas
        ids_bloqueados = (
                self.estado["visualizou"]
                + self.estado["recomendacoes_antigas"]
        )

        # isin verifica quais IDs estão bloqueados e ~ inverte essa seleção
        candidatos = self.conteudos_df[
            ~self.conteudos_df["id"].isin(ids_bloqueados)
        ]

        return candidatos

    # interesses recentes são mais relevantes que interesses antigos,
    # assim a cada nova percepção do usuário é preservada apenas 80% da pontuação anterior
    def reduzir_interesses_antigos(self):
        for categoria_estado in self.estado["interesses"]:
            self.estado["interesses"][categoria_estado] *= 0.8

    # funçãozinha complementar para guardar um conteúdo interessante sem repetir o id
    def registrar_conteudo_interessante(self, conteudo_id):
        if conteudo_id not in self.estado["conteudos_interessantes"]:
            self.estado["conteudos_interessantes"].append(conteudo_id)

    # transforma cada evento recebido em mudanças na memória do agente
    def atualizar_estado(self, percepcao):
        self.estado["momento"] = percepcao["momento"]

        # iloc[0] pega a primeira linha encontrada
        conteudo = self.conteudos_df.loc[
            self.conteudos_df["id"] == percepcao["conteudo_id"]
            ].iloc[0]

        categoria_conteudo = conteudo["categoria"]
        evento = percepcao["evento"]

        # recomendacao é uma ação antiga, logo registrar esse evento não soma interesse
        if evento != "recomendacao":
            self.reduzir_interesses_antigos()

        if evento == "visualizacao":
            self.estado["visualizou"].append(percepcao["conteudo_id"])
            tempo = percepcao["tempo_segundos"]

            # sinal fraco para explorar depois; não aumenta a pontuação de interesse
            if 0 <= tempo < 100:
                if percepcao["conteudo_id"] not in self.estado["leituras_rapidas"]:
                    self.estado["leituras_rapidas"].append(percepcao["conteudo_id"])

            # os limites e pontos foram escolhidos com base nos resultados do historico
            # menos de 100 segundos não soma pontos de interesse
            if tempo >= 250:
                self.estado["interesses"][categoria_conteudo] += 3
                self.registrar_conteudo_interessante(percepcao["conteudo_id"])
            elif tempo >= 200:
                self.estado["interesses"][categoria_conteudo] += 2
                self.registrar_conteudo_interessante(percepcao["conteudo_id"])
            elif tempo >= 100:
                self.estado["interesses"][categoria_conteudo] += 1
                self.registrar_conteudo_interessante(percepcao["conteudo_id"])

        elif evento == "recomendacao":
            self.estado["recomendacoes_antigas"].append(
                percepcao["conteudo_id"]
            )

        elif evento == "ignorou_recomendacao":
            self.estado["ignorou_recomendacao"].append(
                percepcao["conteudo_id"]
            )
            # retira um ponto das recomendações ignoradas, consideradas desinteressantes
            # o max impede que o resultado fique negativo
            self.estado["interesses"][categoria_conteudo] = max(
                0,
                self.estado["interesses"][categoria_conteudo] - 1,
            )

        elif evento == "clique_recomendacao":
            # aqui o clique vale quatro pontos, já que foi interessante o bastante para fazer o user clicar
            self.estado["clique_recomendacao"].append(
                percepcao["conteudo_id"]
            )
            self.estado["interesses"][categoria_conteudo] += 4
            self.registrar_conteudo_interessante(percepcao["conteudo_id"])

    # função para preparar o título para comparar palavras
    def extrair_palavras(self, titulo):
        # lower deixa tudo minúsculo e NFD separa as letras dos acentos
        titulo_normalizado = unicodedata.normalize("NFD", titulo.lower())
        # Mn identifica marcas como os acentos; join junta o que sobrou
        titulo_sem_acentos = "".join(
            caractere
            for caractere in titulo_normalizado
            if unicodedata.category(caractere) != "Mn"
        )

        # são palavras pouco úteis para esta comparação
        palavras_sem_significado = {
            "a", "as", "o", "os", "de", "da", "das", "do", "dos",
            "e", "em", "para", "como", "um", "uma",
            "ano", "atualidade", "maiores", "nova", "novas", "novo",
            "novos", "principais",
        }

        # o regex pega letras e o set elimina palavras repetidas no mesmo título
        palavras = set(re.findall(r"[a-z]+", titulo_sem_acentos))
        # a diferença de conjuntos remove as palavras que escolhemos ignorar
        return palavras - palavras_sem_significado

    # compara as alternativas por pontuação e devolve os dados da notícia escolhida
    def decidir(self):
        candidatos = self.selecionar_candidatos()

        if candidatos.empty:
            # None indica que não foi possível escolher uma notícia
            return None

        # primeiro tenta as categorias com interesse positivo
        disponiveis = candidatos
        candidatos = disponiveis[
            disponiveis["categoria"].map(self.estado["interesses"]) > 0
        ]
        exploratoria = False
        ids_interessantes = self.estado["conteudos_interessantes"]

        # se essas opções acabaram, usa categorias acessadas por menos de 100s
        if candidatos.empty:
            exploratoria = True
            ids_interessantes = self.estado["leituras_rapidas"]
            categorias_rapidas = self.conteudos_df.loc[
                self.conteudos_df["id"].isin(ids_interessantes), "categoria"
            ]
            candidatos = disponiveis[
                disponiveis["categoria"].isin(categorias_rapidas)
            ]
            if candidatos.empty:
                return None

        # na exploração, os títulos de referência são os das leituras rápidas
        titulos_interessantes = self.conteudos_df.loc[
            self.conteudos_df["id"].isin(ids_interessantes), "titulo"
        ]

        palavras_dos_interessantes = set()
        # reúne as palavras em um conjunto, sem contar repetições
        for titulo in titulos_interessantes:
            palavras_dos_interessantes.update(self.extrair_palavras(titulo))

        pontuacoes = {}

        # iterrows devolve índice e linha
        # _ indica que não precisamos do índice
        for _, candidato in candidatos.iterrows():
            conteudo_id = candidato["id"]
            categoria = candidato["categoria"]

            utilidade_categoria = (
                0 if exploratoria else self.estado["interesses"][categoria]
            )
            palavras_candidato = self.extrair_palavras(candidato["titulo"])
            # & mantém somente as palavras presentes nos dois conjuntos
            palavras_em_comum = palavras_candidato & palavras_dos_interessantes
            utilidade_semelhanca = len(palavras_em_comum) * 0.5

            # a utilidade soma interesse da categoria e 0,5 por palavra em comum
            pontuacoes[conteudo_id] = (
                    utilidade_categoria + utilidade_semelhanca
            )

        # values fornece as notas e max encontra a maior delas
        maior_pontuacao = max(pontuacoes.values())
        # items fornece os pares ID/nota, guardamos todos os empatados no topo
        melhores_ids = [
            conteudo_id
            for conteudo_id, pontuacao in pontuacoes.items()
            if pontuacao == maior_pontuacao
        ]

        # o sorteio ocorre apenas entre as maiores notas e pode variar por execução
        id_escolhido = random.choice(melhores_ids)
        conteudo_escolhido = candidatos.loc[
            candidatos["id"] == id_escolhido
            ].iloc[0]

        # devolve a notícia e as notas para explicar a decisão na saída
        return {
            "conteudo": conteudo_escolhido,
            "pontuacao": maior_pontuacao,
            "pontuacoes": pontuacoes,
            "exploratoria": exploratoria,
        }

    # avalia somente as recomendações antigas e as respostas registradas no histórico
    # sem informar usuário, calcula os resultados gerais
    def calcular_desempenho(self, usuario=None):
        historico = self.historico_df
        if usuario is not None:
            historico = historico.loc[historico["usuario"] == usuario]

        total_recomendacoes = 0
        total_cliques = 0
        total_ignoradas = 0
        tempo_total = 0

        # conta cada tipo de evento e soma apenas o tempo dos cliques em recomendações
        # pressupõe o formato fornecido: tempos válidos e uma resposta por recomendação
        for _, evento in historico.iterrows():
            if evento["evento"] == "recomendacao":
                total_recomendacoes += 1
            elif evento["evento"] == "clique_recomendacao":
                total_cliques += 1
                tempo_total += evento["tempo_segundos"]
            elif evento["evento"] == "ignorou_recomendacao":
                total_ignoradas += 1

        # None significa que faltam dados para calcular; evita divisão por zero
        taxa_cliques = None
        taxa_ignoradas = None
        tempo_medio = None

        if total_recomendacoes > 0:
            # taxa = quantidade de respostas / total de recomendações x 100
            taxa_cliques = (total_cliques / total_recomendacoes) * 100
            taxa_ignoradas = (total_ignoradas / total_recomendacoes) * 100

        if total_cliques > 0:
            # média aritmética = soma dos tempos / quantidade de cliques
            tempo_medio = tempo_total / total_cliques

        return {
            "total_recomendacoes": total_recomendacoes,
            "total_cliques": total_cliques,
            "total_ignoradas": total_ignoradas,
            "tempo_total": tempo_total,
            "taxa_cliques": taxa_cliques,
            "taxa_ignoradas": taxa_ignoradas,
            "tempo_medio": tempo_medio,
        }

    # mostra as três medidas sem confundir o histórico com a nova recomendação
    def mostrar_desempenho(self, usuario=None):
        desempenho = self.calcular_desempenho(usuario)
        escopo = "geral" if usuario is None else f"usuário {usuario}"
        print(f"\n--- Desempenho do histórico: {escopo} ---")
        print("Estas medidas avaliam as recomendações antigas do CSV.")
        print(f"Total de recomendações: {desempenho['total_recomendacoes']}")
        print(f"Cliques: {desempenho['total_cliques']}")
        print(f"Ignoradas: {desempenho['total_ignoradas']}")

        if desempenho["taxa_cliques"] is not None:
            print(f"Taxa de cliques: {desempenho['taxa_cliques']:.2f}%")
            print(f"Taxa de ignoradas: {desempenho['taxa_ignoradas']:.2f}%")
        else:
            print("Taxas: não calculáveis, pois não há recomendações.")

        if desempenho["tempo_medio"] is not None:
            print(f"Tempo médio após clique: {desempenho['tempo_medio']:.2f} segundos")
        else:
            print("Tempo médio: não calculável, pois não há cliques.")

        # são indícios de interesse: clicar ou permanecer muito tempo não garante satisfação
        print("CTR maior e taxa de ignoradas menor tendem a ser melhores.")
        print("Tempo médio maior pode indicar interesse; valores extremos exigem análise.")


    # o print é nosso atuador, apresentando a recomendação no terminal
    def executar(self, decisao):
        if decisao is None:
            print(
                "Ação: não há conteúdo disponível nas categorias de interesse "
                "nem nas de leituras rápidas. Itens vistos ou já recomendados foram excluídos."
            )
            return

        if decisao["exploratoria"]:
            print(
                "Sugestão exploratória: categorias de interesse sem opções novas; "
                "usando categorias de leituras rápidas (menos de 100 segundos)."
            )
            if decisao["pontuacao"] == 0:
                print(
                    "Sem palavras em comum nos títulos: sorteio entre notícias "
                    "das categorias acessadas rapidamente."
                )
            else:
                print("Prioridade para palavras em comum com títulos dessas leituras rápidas.")

        conteudo = decisao["conteudo"]
        print(f"Pontuações dos candidatos: {decisao['pontuacoes']}")
        print(
            f"Ação: recomendar o conteúdo {conteudo['id']} — "
            f'"{conteudo["titulo"]}".'
        )
        print(f"Categoria: {conteudo['categoria']}")
        # .2f mostra duas casas decimais sem mudar a nota usada na decisão
        print(f"Utilidade: {decisao['pontuacao']:.2f}")

    # primeiro processamos o histórico e depois decidimos uma vez
    # as respostas do histórico pertencem às ações antigas, não à nova recomendação
    def iniciar(self, usuario):
        self.estado["usuario"] = usuario

        # filtra um usuário e respeita a ordem temporal exigida pelo trabalho
        historico_usuario = self.historico_df.loc[
            self.historico_df["usuario"] == usuario
            ].sort_values("momento")

        for _, percepcao in historico_usuario.iterrows():
            # identifica ações antigas corretamente na apresentação do histórico
            tipo_registro = (
                "Ação antiga registrada"
                if percepcao["evento"] == "recomendacao"
                else "Nova percepção"
            )
            print(
                f"\n--- {tipo_registro}: "
                f"{percepcao['evento']} ---"
            )
            self.atualizar_estado(percepcao)
            print(f"Estado atual: {self.estado}")

        print("\n--- Decisão do agente ---")
        decisao = self.decidir()
        self.executar(decisao)
        self.mostrar_desempenho(usuario)


if __name__ == "__main__":
    # leitura dos eventos funciona como sensor da simulação
    conteudos_df = pd.read_csv("conteudos.csv")
    historico_df = pd.read_csv("historico.csv")

    # os cinco usuários fornecidos pelo professor; um agente novo evita misturar perfis
    for usuario in range(1, 6):
        print(f"\n========== USUÁRIO {usuario} ==========")
        agente = Agente(conteudos_df, historico_df)
        agente.iniciar(usuario)

    # usa os totais gerais, sem fazer uma média das médias individuais
    agente.mostrar_desempenho()

