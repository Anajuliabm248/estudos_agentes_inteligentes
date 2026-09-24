def iniciar_agente():
    print("Você está acessando: Agente de navegação de sites com grafos")
    agente = Agente()
    agente.iniciar()

class Agente:
    def __init__(self):
        self.site = {
            "home": ["produtos", "ofertas", "suporte"],
            "produtos": ["notebooks", "celulares"],
            "ofertas": ["notebooks"],
            "suporte": ["faq"],
            "notebooks": ["notebook_gamer", "notebook_basico"],
            "celulares": ["iOS", "android"],
            "faq": [],
            "notebook_gamer": [],
            "notebook_basico": [],
            "iOS": [],
            "android": []
        }

        self.estado = {
            'pagina': 'home',
            'objetivo': 'notebook_gamer',
            'caminho': []
        }

    # função que realiza a busca do menor caminho, baseada em busca em largura
    def procurar_caminho(self, site, inicio, objetivo, visitados=None, caminho=None):
        # primeiro verifica se é possível realizar a busca
        if inicio not in site or objetivo not in site:
            return None

        # executado somente na primeira chamada
        if visitados is None:
            visitados = set()

        if caminho is None:
            caminho = []

        # vê o estado atual
        visitados.add(inicio)
        print('visitados: ', visitados)
        caminho_atual = caminho + [inicio]
        print('caminho_atual: ', caminho_atual)

        # realiza o teste de objetivo
        if inicio == objetivo:
            return caminho_atual

        # explora recursivamente os estados adjacentes
        for vizinho in site[inicio]:
            if vizinho not in visitados:
                print('vizinho: ', vizinho)
                resultado = self.procurar_caminho(
                    site,
                    vizinho,
                    objetivo,
                    visitados,
                    caminho_atual
                )

                # interrompe a busca quando encontra uma solução
                if resultado is not None:
                    return resultado

        # caso nenhum caminho foi encontrado a partir deste estado
        return None

    def iniciar(self):
        caminho_trilhado = self.procurar_caminho(
            self.site,
            inicio=self.estado['pagina'],
            objetivo=self.estado['objetivo']
        )

        if caminho_trilhado is None:
            self.estado['caminho'] = []
            print('Nenhuma solução encontrada para o objetivo')

        else:
            self.estado['caminho'] = caminho_trilhado
            self.estado['pagina'] = caminho_trilhado[-1]

            # o custo é calculado pela quantidade de navegações menos a primeira página
            custo = len(caminho_trilhado) - 1

            print(f'\n\nCaminho encontrado: {' -> '.join(caminho_trilhado)}')
            print(f'Custo da solução: {custo}')
            print('\n================================================================\n')


if __name__ == '__main__':
    iniciar_agente()