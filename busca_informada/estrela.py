import heapq

def a_estrela(grafo, heuristica, inicio, objetivo):
    fronteira = []
    heapq.heappush(fronteira, (heuristica[inicio], 0, inicio,[inicio]))

    melhores_custos = { inicio: 0 }
    print('mc', melhores_custos)

    while fronteira:
        f, g, atual, caminho = heapq.heappop(fronteira)

        if g > melhores_custos[atual]:
            continue

        print(f"Expandindo {atual}: " f"g={g}, " f"h={heuristica[atual]}, " f"f={f}")

        if atual == objetivo:
            return caminho, g

        for vizinho, custo in grafo[atual]:
            novo_g = g + custo
            print('novo_g',novo_g)

            if (vizinho not in melhores_custos or novo_g < melhores_custos[vizinho] ):
                melhores_custos[vizinho] = novo_g

                novo_f = (novo_g + heuristica[vizinho])
                print('novo_f',novo_f)

                novo_caminho = (caminho + [vizinho])
                print('novo_caminho',novo_caminho)

                heapq.heappush(fronteira, (novo_f,novo_g,vizinho, novo_caminho))

    return None, None

grafo = {
    "A": [("B", 2), ("C", 5)],
    "B": [("D", 3), ("E", 4)],
    "C": [("F", 2)],
    "D": [("G", 8)],
    "E": [("G", 2)],
    "F": []
}

heuristica = {
    "A": 7,
    "B": 6,
    "C": 5,
    "D": 5,
    "E": 2,
    "F": 3,
    "G": 0
}

caminho, custo = a_estrela(grafo,heuristica,"A","G")

print("Caminho:", caminho)
print("Custo:", custo)