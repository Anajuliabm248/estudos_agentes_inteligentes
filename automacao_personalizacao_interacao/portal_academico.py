from automacao_personalizacao_interacao.base import contexto


class Agente:
    def __init__(self):
        self.solicitacao = {
            "id": 101,
            "estudante": 25,
            "objetivo": "acessar_material",
            "recurso": "disciplina",
            "falha_tecnica": None,
            "tentativas": 1,
            "orientacao_anterior": False,
            "status": "aberta"
        }

    def perceber(self, solicitacao):
        if solicitacao[]

    def decidir(self, contexto):

        if not contexto["objetivo"] or contexto["falha_tecnica"] is None :
            return "solicitar_informacoes"
        elif contexto["objetivo"] is "acessar_disciplina" and contexto["orientacao_anterior"] is False:
            return "orientar_acesso"
        elif contexto["objetivo"] is "acessar_material":
            if not contexto["recurso"]:
                return "solicitar_informacoes"
            else:
                return "disponibilizar_recurso"
        elif contexto["falha_tecnica"] is True or contexto["tentativas"] >=3 or contexto["orientacao_anterior"] is True:
            return "encaminhar_suporte"
        elif contexto["status"] is "encerrada" :
            return "nao_processar"
        else:
            return "encaminhar_suporte"


    def executar(self, acao, solicitacao):


    def verificar_resultado(self, resultado):


    def processar_solicitacao(self, solicitacoes):
        for solicitacao in solicitacoes:
            print(f"\n--- Nova solicitação do Agente: {solicitacao} ---")

            contexto = self.perceber(self.solicitacao)
            acao = self.decidir(contexto)
            resultado = self.executar(acao, solicitacao)
            self.verificar_resultado(resultado)

            print(f"Novo estado: {self.solicitacao}")

if __name__ == '__main__':
    agente = Agente()
    agente.processar_solicitacao(agente.solicitacao)