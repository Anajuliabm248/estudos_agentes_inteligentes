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

    # Responsável por interpretar os eventos e atualizar o estado interna do agente
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

    # Analisa o estado atual para determinar a melhor ação
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

    # Coordena o ciclo de vida do agente (Percepção -> Decisão -> Ação)
    def executar(self, eventos, decidir_por_propriedade):
        for evento in eventos:
            print(f"\n--- Novo evento do Agente: {evento} ---")
            print(f"Estado anterior: {self.estado}")

            self.perceber(evento)
            decisao = self.decidir(self.estado)
            self.agir(decisao)

            print(f"Novo estado: {self.estado}")

    def iniciar(self):
        print('INICIANDO AGENTE DE MONITORAMENTO DE PEDIDOS')
        self.executar(self.eventos)


if __name__ == "__main__":
    agente = Agente()
    agente.iniciar()
