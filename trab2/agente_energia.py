import pandas as pd
import sys
import time

class AgenteEnergia:
    # inicialização do agente
    def __init__(self):
        self.estado = {
            'residencia': None,
            'consumo_diario_estimado': None,
            'recomendacoes_apresentadas': [],
            'recomendacoes_aceitas': [],
            'recomendacoes_rejeitadas': [],
            'oportunidades_pendentes': [],
        }

    def carregando(self):
        for _ in range(3):  # Repete o ciclo 3 vezes
            for pontos in range(4):  # Vai de 0 a 3 pontinhos
                # O espaço no final apaga os pontos anteriores quando o ciclo reinicia
                texto = f"\rCarregando recomendações {'.' * pontos}   "
                sys.stdout.write(texto)
                sys.stdout.flush()
                time.sleep(0.2)


    def perceber(self, df):
        return {
            # dados gerais
            # iloc[0] pega só o primeiro, já que todas as linhas do df são iguais
            'residencia': {
                'id': df['residencia_id'].iloc[0],
                'num_moradores': df['numero_moradores'].iloc[0].item(),
                'meta_consumo': df['meta_consumo_diario_kwh'].iloc[0].item(),
                'tarifa': df['tarifa_base_rs_kwh'].iloc[0].item(),
                'perfil_morador': df['perfil_morador'].iloc[0],
                # prioridades em conjunto, tbm pega só o primeiro (todos iguais)
                'pesos': {
                    'economia': df['peso_economia'].iloc[0].item(),
                    'conforto': df['peso_conforto'].iloc[0].item(),
                    'flexibilidade': df['peso_flexibilidade'].iloc[0].item(),
                    'baixo_esforco': df['peso_baixo_esforco'].iloc[0].item()
                },
            },

            # equipamentos em conjunto também, mas formam series
            # (elemento + indice)
            'equipamentos': {
                'id': df['equipamento_id'],
                'nome': df['equipamento'],
                'categoria': df['categoria'],
                'potencia': df['potencia_kw'],
                'horas_uso': df['horas_uso_diario'],
                'consumo_estimado': df['consumo_diario_estimado_kwh'],
                'reducao_uso': df['reducao_uso'],
                'essencialidade': df['essencialidade'],
                'impacto_conforto': df['impacto_conforto_1a5'],
                'flexibilidade': df['flexibilidade_reducao_uso_1a5'],
                'esforco': df['esforco_1a5'],
                'economia_potencial': df['economia_potencial_reducao_kwh']
            },

            # consumo inicial é a soma do consumo de todos os equipamentos
            'consumo_inicial': df['consumo_diario_estimado_kwh'].sum().item(),
        }


    def oportunidades_elegiveis(self, equipamentos):
        elegiveis = []

        # junta os valores que estavam separados em várias series e
        # forma um unico dicionário completo para cada equipamento
        for indice in equipamentos['id'].index:
            equipamento = {
                campo: valores.loc[indice]
                for campo, valores in equipamentos.items()
            }

            if not equipamento['reducao_uso']:
                continue
            if equipamento['economia_potencial'] <= 0:
                continue
            if equipamento['essencialidade'] == 'essencial':
                continue
            if equipamento['impacto_conforto'] > 3:
                continue

            elegiveis.append(equipamento)

        return elegiveis


    def calcular_utilidade(self, oportunidades, pesos):
        if not oportunidades:
            return []

        maior_economia = max(
            equipamento['economia_potencial']
            for equipamento in oportunidades
        )

        for equipamento in oportunidades:
            nota_economia = 1 + 4 * (
                    equipamento['economia_potencial'] / maior_economia
            )
            nota_conforto = 6 - equipamento['impacto_conforto']
            nota_flexibilidade = equipamento['flexibilidade']
            nota_baixo_esforco = 6 - equipamento['esforco']

            utilidade = (
                    pesos['economia'] * nota_economia
                    + pesos['conforto'] * nota_conforto
                    + pesos['flexibilidade'] * nota_flexibilidade
                    + pesos['baixo_esforco'] * nota_baixo_esforco
            )

            equipamento['nota_economia'] = nota_economia
            equipamento['nota_conforto'] = nota_conforto
            equipamento['nota_flexibilidade'] = nota_flexibilidade
            equipamento['nota_baixo_esforco'] = nota_baixo_esforco
            equipamento['utilidade'] = utilidade

        return oportunidades


    # ordena as oportunidades da melhor para a menos vantajosa
    def ordenar_recomendacoes(self, oportunidades):
        recomendacoes_ordenadas = sorted(
            oportunidades,
            key=lambda equipamento: equipamento['utilidade'],
            reverse=True
        )
        return recomendacoes_ordenadas


    def processar_feedback(self, recomendacao):
        print('\n============ OPÇÕES ============')
        print('[1] Aceitar')
        print('[2] Rejeitar')
        resposta = input('R: ')

        if resposta == '1':
            self.estado['recomendacoes_aceitas'].append(recomendacao)
            self.estado['oportunidades_pendentes'].remove(recomendacao)

            consumo_atual = self.estado['consumo_diario_estimado']
            economia = recomendacao['economia_potencial']
            self.estado['consumo_diario_estimado'] = (max(0, consumo_atual - economia))
            print('Recomendação aceita.')

        elif resposta == '2':
            self.estado['recomendacoes_rejeitadas'].append(recomendacao)
            self.estado['oportunidades_pendentes'].remove(recomendacao)
            print('Recomendação rejeitada.')

        else:
            print('Resposta inválida.')
            return 'continue'

        self.mostrar_estado()


    def feedback(self):
        while self.estado['oportunidades_pendentes']:
            print('\n============ ESCOLHA UMA RECOMENDAÇÃO ============')

            for posicao, recomendacao in enumerate(
                    self.estado['oportunidades_pendentes'], start=1):
                print(f"[{posicao}] {recomendacao['nome']}")

            escolha = input('Digite o número da recomendação ou 0 para sair: ')

            if escolha == '0':
                self.mostrar_estado()
                break

            if not escolha.isdigit():
                print('Digite um número válido.')
                continue

            posicao = int(escolha)
            pendentes = self.estado['oportunidades_pendentes']

            if posicao < 1 or posicao > len(pendentes):
                print('Recomendação não encontrada.')
                continue

            recomendacao = pendentes[posicao - 1]
            resp = self.processar_feedback(recomendacao)

            if resp == 'continue':
                continue


    def apresentacao(self, recomendacoes):

        print('\n\n============ RECOMENDAÇÕES ============')

        for posicao, recomendacao in enumerate(recomendacoes, start=1):
            print(f'\n-------- Recomendação {posicao} --------')
            print('Equipamento:', recomendacao['nome'])
            print('Categoria:', recomendacao['categoria'])
            print(
                'Economia potencial diária:',
                f"{recomendacao['economia_potencial']:.2f} kWh"
            )
            print('Impacto no conforto:', recomendacao['impacto_conforto'])
            print('Flexibilidade:', recomendacao['flexibilidade'])
            print('Esforço:', recomendacao['esforco'])
            print('Utilidade:', f"{recomendacao['utilidade']:.2f}")
            print(
                'Descrição:',
                f"Otimizar ou reduzir o uso do equipamento {recomendacao['nome']}."
            )

            if recomendacao['id'] not in self.estado['recomendacoes_apresentadas']:
                self.estado['recomendacoes_apresentadas'].append(
                    recomendacao['id']
                )


    def mostrar_estado(self):
        print('\n============ ESTADO ============')
        print('Residência:', self.estado['residencia']['id'])
        print(
            'Consumo diário estimado:',
            f"{self.estado['consumo_diario_estimado']:.3f} kWh"
        )
        print(
            'Recomendações apresentadas:',
            self.estado['recomendacoes_apresentadas']
        )
        print(
            'Recomendações aceitas:',
            [rec['id'] for rec in self.estado['recomendacoes_aceitas']]
        )
        print(
            'Recomendações rejeitadas:',
            [rec['id'] for rec in self.estado['recomendacoes_rejeitadas']]
        )
        print(
            'Oportunidades pendentes:',
            [rec['id'] for rec in self.estado['oportunidades_pendentes']]
        )


    def estado_inicial(self, contexto, recomendacoes):
        self.estado['residencia'] = contexto['residencia']
        self.estado['consumo_diario_estimado'] = contexto['consumo_inicial']
        self.estado['oportunidades_pendentes'] = recomendacoes.copy()


    def dados_residencia(self, contexto):
        residencia = contexto['residencia']

        print('\n============ DADOS DA RESIDÊNCIA ============')
        print('ID:', residencia['id'])
        print('Número de moradores:', residencia['num_moradores'])
        print('Meta de consumo diário:', residencia['meta_consumo'], 'kWh')
        print('Tarifa:', residencia['tarifa'], 'R$/kWh')
        print('Perfil do morador:', residencia['perfil_morador'])

        print('\n------------ PRIORIDADES ------------')
        for peso, valor in residencia['pesos'].items():
            print(f'{peso}: {valor}')

        print()


    def carregar_dados_residencia(self):
        # carregamento dos dados
        df = pd.read_csv('dataset_consumo_energia.csv')

        residencia_id = 'R02'
        df_residencia = df[df['residencia_id'] == residencia_id]

        return df_residencia


    def inicio(self):

        df_residencia = self.carregar_dados_residencia()
        contexto = self.perceber(df_residencia)

        oportunidades = self.oportunidades_elegiveis(contexto['equipamentos'])
        oportunidades = self.calcular_utilidade(oportunidades, contexto['residencia']['pesos'])
        recomendacoes = self.ordenar_recomendacoes(oportunidades)

        # executa a simulação
        self.estado_inicial(contexto, recomendacoes)
        self.dados_residencia(contexto)
        self.carregando()
        self.apresentacao(recomendacoes)
        self.mostrar_estado()
        self.feedback()


if __name__ == '__main__':
    agente = AgenteEnergia()
    agente.inicio()
