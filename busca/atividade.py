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
    def procurar_caminho(self, site, inicio, objetivo):
        # primeiro verifica se é possível realizar a busca
        if inicio not in site or objetivo not in site:
            return None

        # fila de filas
        fila = [[inicio]]
        print('fila: ', fila)
        visitados = {inicio}
        print(f'visitados: {visitados}')

        while fila:
            caminho = fila.pop(0)
            print(f'caminho atual: {caminho}')
            atual = caminho[-1]
            print('atual: ', atual)

            if atual == objetivo:
                return caminho

            # lógica para verificar as páginas ligadas coma a página atual
            for vizinho in site[atual]:
                # se a página ainda não foi visitada adiciona ela na fila de visitados e caminho
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(
                        (caminho + [vizinho])
                    )
                    print('vizinho: ', vizinho)

        # no caso da fila terminar e o objetivo não for encontrado
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

            print(f'Caminho encontrado: {' -> '.join(caminho_trilhado)}')
            print(f'Custo da solução: {custo}')
            print('\n================================================================\n')


if __name__ == '__main__':
    iniciar_agente()