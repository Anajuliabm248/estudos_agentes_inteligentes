"""
ampliação para recomendar materiais de estudo:
● preservar o funcionamento do agente desenvolvido na Aula 11;
● identificar quando uma solicitação deve resultar na disponibilização de materiais de estudo;
● avaliar quais materiais são adequados para um estudante;
● calcular a utilidade dos materiais candidatos;
● ordenar as recomendações de acordo com a utilidade calculada;
● executar a recomendação e verificar se a ação foi realizada com sucesso.
"""


class Agente:
    solicitacoes = [
        {
            "id": 101,
            "estudante": 25,
            "objetivo": "acessar_material",
            "recurso": "árvores", "falha_tecnica": False,
            "tentativas": 0,
            "orientacao_anterior": False,
            "status": "aberta",
            "assuntos_interesse": ["árvores", "recursão"],
            "nivel_maximo": 2,
            "formato_preferido": "exercicio",
            "tempo_disponivel": 20
        },
        {
            "id": 102,
            "estudante": 26,
            "objetivo": "acessar_disciplina",
            "recurso": "disciplina",
            "falha_tecnica": None,
            "tentativas": 1, "orientacao_anterior":
            False, "status": "aberta"
        },
        {
            "id": 103,
            "estudante": 27,
            "objetivo": "acessar_disciplina",
            "recurso": "disciplina",
            "falha_tecnica": True,
            "tentativas": 1,
            "orientacao_anterior": False,
            "status": "aberta"
        },
        {
            "id": 104,
            "estudante": 28,
            "objetivo": "acessar_disciplina",
            "recurso": "disciplina",
            "falha_tecnica": False,
            "tentativas": 3,
            "orientacao_anterior": False,
            "status": "aberta"
        },
        {
            "id": 105,
            "estudante": 29,
            "objetivo": "acessar_disciplina",
            "recurso": "disciplina",
            "falha_tecnica": False,
            "tentativas": 1,
            "orientacao_anterior": True,
            "status": "aberta"
        },
        {
            "id": 106,
            "estudante": 30,
            "objetivo": "acessar_material",
            "recurso": "disciplina",
            "falha_tecnica": False,
            "tentativas": 0,
            "orientacao_anterior": False,
            "status": "encerrada"
        },
    ]

    materiais = [
        {
            "id": "M1",
            "titulo": "Exercícios de árvores",
            "assuntos": ["árvores", "recursão"],
            "nivel": 2,
            "formato": "exercicio",
            "duracao": 15,
            "disponivel": True,
            "atualidade": 6,
            "relevancia": 9
        },
        {
            "id": "M2",
            "titulo": "Vídeo: árvores binárias",
            "assuntos": ["árvores"],
            "nivel": 1,
            "formato": "video",
            "duracao": 12,
            "disponivel": True,
            "atualidade": 8,
            "relevancia": 8
        },
        {
            "id": "M3",
            "titulo": "Texto sobre recursão",
            "assuntos": ["recursão"],
            "nivel": 2,
            "formato": "texto",
            "duracao": 25,
            "disponivel": True,
            "atualidade": 9,
            "relevancia": 7
        },
        {
            "id": "M4",
            "titulo": "Exercícios avançados",
            "assuntos": ["árvores"],
            "nivel": 3,
            "formato": "exercicio",
            "duracao": 20,
            "disponivel": True,
            "atualidade": 7,
            "relevancia": 8
        },
        {
            "id": "M5",
            "titulo": "Introdução a listas",
            "assuntos": ["listas"],
            "nivel": 1,
            "formato": "video",
            "duracao": 10,
            "disponivel": False,
            "atualidade": 8,
            "relevancia": 6
        }
    ]

    mensagens = {
        "solicitar_informacoes": (
            "Solicitar informações complementares ao estudante."
        ),
        "orientar_acesso": (
            "Fornecer orientação para acesso à disciplina."
        ),
        "disponibilizar_recurso": (
            "Indicar o recurso acadêmico solicitado."
        ),
        "encaminhar_suporte": (
            "Encaminhar a solicitação ao suporte acadêmico."
        ),
        "nao_processar": (
            "Solicitação encerrada."
        ),
    }

    # perceber a solicitação e organizar as informações relevantes;
    def perceber(self, solicitacao):
        return {
            "id": solicitacao["id"],
            "estudante": solicitacao["estudante"],
            "objetivo": solicitacao["objetivo"],
            "recurso": solicitacao["recurso"],
            "falha_tecnica": solicitacao["falha_tecnica"],
            "tentativas": solicitacao["tentativas"],
            "orientacao_anterior": solicitacao["orientacao_anterior"],
            "status": solicitacao["status"],
            "assuntos_interesse": solicitacao["assuntos_interesse"],
            "nivel_maximo": solicitacao["nivel_maximo"],
            "formato_preferido": solicitacao["formato_preferido"],
            "tempo_disponivel": solicitacao["tempo_disponivel"]
        }

    # decidir qual ação deve ser realizada; manter regras
    def decidir(self, contexto):
        if contexto["status"] == "encerrada":
            return "nao_processar"

        if not contexto["objetivo"]:
            return "solicitar_informacoes"

        if contexto["falha_tecnica"] is True:
            return "encaminhar_suporte"

        if contexto["tentativas"] >= 3:
            return "encaminhar_suporte"

        if contexto["objetivo"] == "acessar_material":
            if not contexto["recurso"]:
                return "solicitar_informacoes"

            # a partir dessa decisão a recomendação deve ser incorporada:
            return "disponibilizar_recurso"

        if contexto["objetivo"] == "acessar_disciplina":
            if contexto["falha_tecnica"] is None:
                return "solicitar_informacoes"

            if contexto["orientacao_anterior"] is True:
                return "encaminhar_suporte"

            return "orientar_acesso"

        return "solicitar_informacoes"

    # verificar o resultado da execução;
    def verificar_resultado(self, resultado):
        return resultado["sucesso"] is True


    # seleciona os materiais candidatos a recomendação (filtro)
    def material_candidato(self, contexto):
        candidatos = []

        for material in self.materiais:
            if not material["disponivel"]: #1
                continue
            if contexto["recurso"] not in material["assuntos"]: #2
                continue
            if material["nivel"] > contexto["nivel_maximo"]: #3
                continue
            if material["duracao"] > contexto["tempo_disponivel"]: #4
                continue

            # se atender a todos os critérios:
            candidatos.append(material)

        return candidatos


    def calcular_compatibilidade(self, material, contexto):
        ass_pont = 0
        for_pont = 0

        for assunto in self.materiais:
            if assunto["assunto"] in contexto["assuntos_interesse"]:
                ass_pont += 1
            if assunto["formato"] == contexto["formato_preferido"]:
                for_pont += 1

        # 𝐶(𝑚) = 𝑚𝑖𝑛 (10, 3*𝐼(𝑚) + 4 𝐹(𝑚))
        c_m = (3 * ass_pont) + (4 * for_pont)
        return min(10, c_m)

    def calcular_nivel_dificuldade(self, material, contexto):
        n_m = 10 if material["nivel"] == contexto["nivel_maximo"] else 8
        return n_m

    def calcular_utilidade(self, material, contexto, c_m):
        # (N(m)): adequação do nível de dificuldade;
        n_m = self.calcular_nivel_dificuldade(material, contexto)
        # (A(m)): atualidade do material;
        a_m = material["atualidade"]
        # (R(m)): relevância geral do material.
        r_m = material["relevancia"]

        # 𝑈(𝑚)=0,5 𝐶(𝑚)+0,2 𝑁(𝑚)+0,2 𝐴(𝑚)+0,1 𝑅(𝑚) (utilidade)
        u_m = (0.5 * c_m) + (0.2 * n_m) + (0.2 * a_m) + (0.1 * r_m)

        return u_m

    def gerar_recomendacao(self, contexto):
        candidatos = self.material_candidato(contexto)

        if not candidatos:
            return "Nenhum material adequado encontrado"

        recomendacoes = []

        for material in candidatos:
            # (C(m)): compatibilidade com as preferências do estudante
            c_m = self.calcular_compatibilidade(material,contexto)
            # (U(m): utilidade do material
            u_m = self.calcular_utilidade(material,contexto, c_m)

            justificativa = (f"Recomendado por abordar sobre: '{contexto['recurso']}', "
                             f"durar {material['duracao']}"
                             f", estando dentro do limite de {contexto['tempo_disponivel']}.")
            if material["formato"] == contexto["formato_preferido"]:
                justificativa += " Além disso, corresponde ao formato preferido."

            recomendacoes.append({
                "id": material["id"],
                "titulo": material["titulo"],
                "utilidade": u_m,
                "justificativa": justificativa
            })

        recomendacoes.sort(key=lambda x: x["utilidade"], reverse=True)

        texto_rec = "Materiais recomendados:\n"
        for r in recomendacoes:
            texto_rec += f" - [{r['id']}] {r['titulo']} | Utilidade: {r['utilidade']:.2f}\n   Justificativa: {r['justificativa']}\n"
        return texto_rec.strip()

    # executar a ação escolhida;
    def executar(self, acao, solicitacao, contexto, sucesso=True):
        if acao not in self.mensagens:
            return {
                "sucesso": False,
                "mensagem": "A ação selecionada não é válida.",
            }

        if acao == "nao_processar":
            return {
                "sucesso": True,
                "mensagem": self.mensagens[acao],
            }

        if not sucesso:
            return {
                "sucesso": False,
                "mensagem": (
                    "Não foi possível executar a ação da solicitação "
                    f"{solicitacao['id']}."
                ),
            }

        if acao == "disponibilizar_recurso":
            return {
                "mensagem": self.mensagens[acao],
                "recomendacao": self.gerar_recomendacao(contexto)

            }

        return {
            "sucesso": True,
            "mensagem": self.mensagens[acao],
        }

    # coordenar essas etapas para processar uma solicitação completa.
    def processar_solicitacao(self, solicitacao, sucesso_execucao=True):
        contexto = self.perceber(solicitacao)
        acao = self.decidir(contexto)
        resultado = self.executar(
            acao,
            solicitacao,
            contexto,
            sucesso=sucesso_execucao,
        )

        sucesso_confirmado = self.verificar_resultado(resultado)

        resposta = {
            "solicitacao": solicitacao["id"],
            "acao": acao,
            "sucesso": sucesso_confirmado,
            "mensagem": resultado["mensagem"],
        }

        print("Solicitação:", resposta["solicitacao"])
        print("Ação selecionada:", resposta["acao"])
        print("Execução confirmada:", resposta["sucesso"])
        print("Resultado:", resposta["mensagem"])
        print("=" * 60)


if __name__ == "__main__":
    agente = Agente()
    for solicitacao in agente.solicitacoes:
        print("\n--- Nova solicitação do agente ---")
        agente.processar_solicitacao(solicitacao)

    # teste do sétimo cenário, com a ação correta, mas a execução com falha
    print("\n--- Teste de falha na execução ---")
    agente.processar_solicitacao(
        agente.solicitacoes[0],
        sucesso_execucao=False,
    )
