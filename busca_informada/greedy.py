import heapq

def greedy(grafo, heuristica, inicio, objetivo):
    fronteira = []

    heapq.heappush(fronteira, (heuristica[inicio], inicio, [inicio]) )

    visitados = set()

    while fronteira:
        h, atual, caminho = heapq.heappop(fronteira)

        if atual in visitados:
            continue

        visitados.add(atual)

        print(f"Expandindo {atual}: h={heuristica[atual]}")

        if atual == objetivo:
            return caminho

        for vizinho, _ in grafo[atual]: #para grafo["A"], o primeiro item é a tupla ("B", 2). Nesse caso vizinho = "B" e o 2 é ignorado através do uso de _
            if vizinho not in visitados:
                novo_caminho = caminho + [vizinho]

                heapq.heappush(
                    fronteira,(heuristica[vizinho], vizinho, novo_caminho)
                )

    return None


grafo = {
    "A": [("B", 2), ("C", 5)],
    "B": [("D", 3), ("E", 4)],
    "C": [("F", 2)],
    "D": [("G", 8)],
    "E": [("G", 2)],
    "F": [],
    "G": []
}

heuristica = {
    "A": 7,
    "B": 6,
    "C": 5,
    "D": 5,
    "E": 2,
    "F": float("inf"),
    "G": 0
}

# passa por parâmetro o grafo, heurística, início e objetivo
caminho = greedy(grafo, heuristica,"A","G")

print(caminho)