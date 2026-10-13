def busca_largura(grafo, inicio, objetivo):
    fila = [[inicio]]
    visitados = {inicio}

    while fila:
        caminho = fila.pop(0)
        atual = caminho[-1]

        if atual == objetivo:
            return caminho

        for vizinho in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(caminho + [vizinho])

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
    caminho = busca_largura(grafo, "A", "H")
    print('\n\ncaminho final: ', caminho)
