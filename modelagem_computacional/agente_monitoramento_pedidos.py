class Agente:
    def __init__(self):
        self.eventos = [
            {"tipo": "pedido_realizado", "pedido": 101},
            {"tipo": "pedido_enviado", "pedido": 101},
            {"tipo": "pedido_realizado", "pedido": 102},
            {"tipo": "pedido_cancelado", "pedido": 102},
            {"tipo": "pedido_entregue", "pedido": 101}
        ]
        self.estado = {
            "pedidos_ativos": [],
            "pedidos_entregues": [],
            "pedidos_cancelados": [],
            "ultimo_evento": None
        }

    # Responsável por interpretar os eventos e atualizar o estado interno do agente
    def perceber(self, evento):
        self.estado["ultimo_evento"] = evento["tipo"]

        if evento["tipo"] == "pedido_realizado":
            self.estado["pedidos_ativos"].append(evento["pedido"])

        elif evento["tipo"] == "pedido_enviado":
            print(f"Pedido {evento['pedido']} foi enviado.")

        elif evento["tipo"] == "pedido_entregue":
            pedido = evento["pedido"]
            if pedido in self.estado["pedidos_ativos"]:
                self.estado["pedidos_ativos"].remove(pedido)
            self.estado["pedidos_entregues"].append(pedido)

        elif evento["tipo"] == "pedido_cancelado":
            pedido = evento["pedido"]
            if pedido in self.estado["pedidos_ativos"]:
                self.estado["pedidos_ativos"].remove(pedido)
            self.estado["pedidos_cancelados"].append(pedido)

    # Estratégia original (prioriza cancelamentos, depois entregas, depois ativos)
    def decidir(self, estado):
        if estado["pedidos_cancelados"]:
            decisao = "informar_cancelamento"
        elif estado["pedidos_entregues"]:
            decisao = "informar_entrega"
        elif estado["pedidos_ativos"]:
            decisao = "informar_pedido_ativo"
        else:
            decisao = "nenhuma_acao"
        return decisao

    # Nova estratégia de decisão (prioriza pedidos ativos, depois entregas, depois cancelamentos)
    def decidir_por_prioridade(self, estado):
        if estado["pedidos_ativos"]:
            decisao = "informar_pedido_ativo"
        elif estado["pedidos_entregues"]:
            decisao = "informar_entrega"
        elif estado["pedidos_cancelados"]:
            decisao = "informar_cancelamento"
        else:
            decisao = "nenhuma_acao"
        return decisao

    # Executa a decisão tomada no ambiente
    def agir(self, decisao):
        if decisao == "informar_cancelamento":
            print("Existem pedidos cancelados.")
        elif decisao == "informar_entrega":
            print("Existe pedido entregue.")
        elif decisao == "informar_pedido_ativo":
            print("Existe pedido em andamento.")
        else:
            print("Nenhuma ação necessária.")

    # Coordena o ciclo de vida do agente recebendo a estratégia de decisão por parâmetro
    def executar(self, eventos, estrategia_decisao=None):
        # Se nenhuma estratégia for passada por parâmetro, usa a padrão (decidir)
        if estrategia_decisao is None:
            estrategia_decisao = self.decidir

        for evento in eventos:
            print(f"\n--- Novo evento do Agente: {evento} ---")
            print(f"Estado anterior: {self.estado}")

            self.perceber(evento)
            # Utiliza a função/estratégia de decisão passada dinamicamente
            decisao = estrategia_decisao(self.estado)
            self.agir(decisao)

            print(f"Novo estado: {self.estado}")

    def iniciar(self):
        print('INICIANDO AGENTE DE MONITORAMENTO DE PEDIDOS')
        self.executar(self.eventos)


if __name__ == "__main__":
    agente = Agente()

    # Exemplo 1: Executando com a estratégia padrão (decidir)
    # agente.iniciar()

    # Exemplo 2: Executando explicitamente com a nova estratégia (decidir_por_prioridade)
    print("=== EXECUTANDO COM A NOVA ESTRATÉGIA (Pedidos Ativos em Prioridade) ===")
    agente.executar(agente.eventos, agente.decidir_por_prioridade)