from collections import deque

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
            'objetivo': None,
            'caminho': []
        }

        self.objetivos = [
            'notebook_gamer',
            'iOS',
            'faq',
            'mouse'
        ]

    # função que realiza a busca do menor caminho, baseada em busca em largura
    def procurar_caminho(self, site, inicio, objetivo):
        # primeiro verifica se é possível realizar a busca
        if inicio not in site or objetivo not in site:
            return None

        # a fila é como uma tupla com dois objetos, que guarda o estado inicial e o caminho percorrido
        # semelhante às filas em C, feitas com struct, mas bem mais simples já que é python
        fila = deque([(inicio, [inicio])])

        # lógica para não visitara a mesma página mais de uma vez
        visitados = {inicio}

        while fila:
            # remove e retorna o primeiro elemento à esquerda da fila
            pagina_atual, caminho_atual = fila.popleft()

            # faz o teste de objetivo
            if pagina_atual == objetivo:
                return caminho_atual

            # lógica para verificar as páginas ligadas coma a página atual
            for proxima_pagina in site[pagina_atual]:
                # se a página ainda não foi visitada adiciona ela na fila de visitados e caminho
                if proxima_pagina not in visitados:
                    visitados.add(proxima_pagina)

                    novo_caminho = caminho_atual + [proxima_pagina]

                    fila.append(
                        (proxima_pagina, novo_caminho)
                    )

        # no caso da fila terminar e o objetivo não for encontrado
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