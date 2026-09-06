def iniciar_agente():
    print("Você está acessando: Agente de recomendação de conteúdo")
    agente = Agente()
    agente.iniciar()


class Agente:
    def __init__(self):
        self.estado = {
        }

    def atualizar_estado(self, percepcao):


    def decidir(self, percepcao):


    def executar(self, acao):


    def iniciar(self):
        percepcoes = [

        ]

        for percepcao in percepcoes:
            print(f"\n--- Nova Percepção do Agente: {percepcao} ---")
            self.atualizar_estado(percepcao)
            acao = self.decidir(percepcao)
            self.executar(acao)
            print(f"Estado atual: {self.estado}")
