def busca_profundidade(grafo, inicio, objetivo):
    pilha = [[inicio]]
    print('pilha: ', pilha)
    visitados = {inicio}
    print('visitados: ', visitados)

    while pilha:
        caminho = pilha.pop()
        print('caminho: ', caminho)
        atual = caminho[-1]
        print('atual: ', atual)

        if atual == objetivo:
            return caminho

        for vizinho in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                pilha.append(caminho + [vizinho])
                print('vizinho: ', vizinho)

    return None

grafo = {
    "A": ["B", "C"],
    "B": ["A", "D", "E", "H"],
    "C": ["A"],
    "D": ["B", "F", "H"],
    "E": ["B"],
    "F": ["D", "H"],
    "H": ["B", "F"]
}

if __name__ == "__main__":
    caminho = busca_profundidade(grafo, "A", "H")
    print('caminho final: ', caminho)