class Agente:
    def __init__(self):
        self.fluxo = {
            "inicio": ["financeiro", "tecnico", "triagem"],
            "triagem": ["tecnico", "financeiro"],
            "tecnico": ["diagnostico", "especialista"],
            "financeiro": ["aprovacao", "especialista"],
            "diagnostico": ["especialista"],
            "aprovacao": ["especialista"],
            "especialista": ["resolucao"],
            "resolucao": ["fim"],
            "fim": []
        }

        self.estado = {
            "inicio": "inicio",
            "objetivo": "fim"
        }

    def busca_largura(self, fluxo, inicio, objetivo):
        fila = [[inicio]]
        print('fila=', fila)
        visitados = {inicio}
        print('visitados=', visitados)

        while fila:
            caminho = fila.pop(0)
            print('caminho=', caminho)
            atual = caminho[-1]
            print('explorando=', atual)

            if atual == objetivo:
                return caminho

            for vizinho in fluxo[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    print('descoberto=', vizinho)
                    print('visitados=', visitados)
                    fila.append(caminho + [vizinho])

        return None

    def busca_profundidade(
            self,
            grafo,
            inicio,
            objetivo,
            visitados=None,
            caminho=None
    ):
        if visitados is None:
            visitados = set()

        if caminho is None:
            caminho = [inicio]

        print("caminho:", caminho)
        print("explorando:", inicio)

        if inicio == objetivo:
            return caminho

        visitados.add(inicio)
        print("visitados:", visitados)

        for vizinho in grafo.get(inicio, []):
            if vizinho not in visitados:
                print('descoberto:', vizinho)
                resultado = self.busca_profundidade(
                    grafo,
                    vizinho,
                    objetivo,
                    visitados,
                    caminho + [vizinho]
                )

                if resultado is not None:
                    return resultado

        return None


    def iniciar(self):
        fluxo = self.fluxo
        inicio = self.estado["inicio"]
        objetivo = self.estado["objetivo"]

        print('=========================BFS==========================')
        largura = self.busca_largura(fluxo, inicio, objetivo)
        print('\nCAMINHO ENCONTRADO:', largura)

        print('\n\n=========================DFS==========================')
        largura = self.busca_profundidade(fluxo, inicio, objetivo)
        print('\nCAMINHO ENCONTRADO:', largura)

if __name__ == '__main__':
        agente = Agente()
        agente.iniciar()