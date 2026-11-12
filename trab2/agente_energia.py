import pandas as pd

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

    # percepção
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

            # equipamentos em conjunto também, mas formam series (elemento + indice)
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

    # identificação das oportunidades elegíveis
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

    # calculo da utilidade
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

            print(f"--- equipamento {equipamento['id']} ---")
            print('Nota de economia:', round(nota_economia, 2))
            print('Nota de conforto:', round(nota_conforto, 2))
            print('Nota de flexibilidade:', round(nota_flexibilidade, 2))
            print('Nota de baixo esforço:', round(nota_baixo_esforco, 2))
            print('Utilidade:', round(utilidade, 2))

        return oportunidades

    # ordena as oportunidades da melhor para a menos vantajosa
    def ordenar_recomendacoes(self, oportunidades):
        recomendacoes_ordenadas = sorted(
            oportunidades,
            key=lambda equipamento: equipamento['utilidade'],
            reverse=True
        )

        print("\n----Ordem------")
        for recomendacao in recomendacoes_ordenadas:
            print(recomendacao['id'])

        return recomendacoes_ordenadas

    # atualização do estado
    def atualizar_estado(self, contexto):
        self.estado['residencia'] = contexto['residencia']
        self.estado['consumo_diario_estimado'] = contexto['consumo_inicial']

    # execução da simulação
    def inicio(self):
        # carregamento dos dados
        df = pd.read_csv('dataset_consumo_energia.csv')

        # configuração da residência
        residencia_id = 'R01'
        df_residencia = df[df['residencia_id'] == residencia_id]

        contexto = self.perceber(df_residencia)
        oportunidades = self.oportunidades_elegiveis(contexto['equipamentos'])
        self.calcular_utilidade(oportunidades, contexto['residencia']['pesos'])
        self.ordenar_recomendacoes(oportunidades)

        self.atualizar_estado(contexto)


if __name__ == '__main__':
    agente = AgenteEnergia()
    agente.inicio()
