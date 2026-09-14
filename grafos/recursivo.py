from collections import deque

def iniciar_agente():
    print("Você está acessando: Agente de navegação de sites com grafos")
    print("Versão RECURSIVA!!!!\n\n")
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
            'objetivo': None,
            'caminho': []
        }

        self.objetivos = [
            'notebook_gamer',
            'iOS',
            'faq',
            'mouse'
        ]

    # função que realiza a busca do menor caminho, baseada em busca de profundidade e feita de forma recursiva
    def procurar_caminho(
            self,
            site,
            inicio,
            objetivo,
            visitados=None,
            caminho=None
    ):
        # executado somente na primeira chamada
        if visitados is None:
            visitados = set()

            if inicio not in site or objetivo not in site:
                return None

        if caminho is None:
            caminho = []

        # vê o estado atual
        visitados.add(inicio)
        caminho_atual = caminho + [inicio]

        # realiza o teste de objetivo
        if inicio == objetivo:
            return caminho_atual

        # explora recursivamente os estados adjacentes
        for proxima_pagina in site[inicio]:
            if proxima_pagina not in visitados:
                resultado = self.procurar_caminho(
                    site,
                    proxima_pagina,
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
        pagina_inicial = self.estado['pagina']
        print(f'Estado inicial: {pagina_inicial}')

        for objetivo in self.objetivos:
            print(f'Objetivo: {objetivo}')

            self.estado['objetivo'] = objetivo

            caminho_trilhado = self.procurar_caminho(
                self.site,
                pagina_inicial,
                objetivo
            )

            if caminho_trilhado is None:
                self.estado['caminho'] = []
                print('Nenhuma solução encontrada para o objetivo')

            else:
                self.estado['caminho'] = caminho_trilhado
                self.estado['pagina'] = caminho_trilhado[-1]

                # o custo é calculado pela quantidade de navegações menos a primeira página
                custo = len(caminho_trilhado) - 1

                print(f'Caminho encontrado: {' -> '.join(caminho_trilhado)}')
                print(f'Custo da solução: {custo}')
                print('\n================================================================\n')

            # reinicia a página inicial para realizar o próximo teste de objetivo
            self.estado['pagina'] = pagina_inicial


if __name__ == '__main__':
    iniciar_agente()