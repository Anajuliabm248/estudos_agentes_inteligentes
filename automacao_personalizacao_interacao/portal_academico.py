class Agente:
    solicitacoes = [
        {
            "id": 101,
            "estudante": 25,
            "objetivo": "acessar_material",
            "recurso": "disciplina",
            "falha_tecnica": False,
            "tentativas": 0,
            "orientacao_anterior": False,
            "status": "aberta",
        },
        {
            "id": 102,
            "estudante": 26,
            "objetivo": "acessar_disciplina",
            "recurso": "disciplina",
            "falha_tecnica": None,
            "tentativas": 1,
            "orientacao_anterior": False,
            "status": "aberta",
        },
        {
            "id": 103,
            "estudante": 27,
            "objetivo": "acessar_disciplina",
            "recurso": "disciplina",
            "falha_tecnica": True,
            "tentativas": 1,
            "orientacao_anterior": False,
            "status": "aberta",
        },
        {
            "id": 104,
            "estudante": 28,
            "objetivo": "acessar_disciplina",
            "recurso": "disciplina",
            "falha_tecnica": False,
            "tentativas": 3,
            "orientacao_anterior": False,
            "status": "aberta",
        },
        {
            "id": 105,
            "estudante": 29,
            "objetivo": "acessar_disciplina",
            "recurso": "disciplina",
            "falha_tecnica": False,
            "tentativas": 1,
            "orientacao_anterior": True,
            "status": "aberta",
        },
        {
            "id": 106,
            "estudante": 30,
            "objetivo": "acessar_material",
            "recurso": "disciplina",
            "falha_tecnica": False,
            "tentativas": 0,
            "orientacao_anterior": False,
            "status": "encerrada",
        },
    ]

    mensagens = {
        "solicitar_informacoes": (
            "Solicitar informações complementares ao estudante."
        ),
        "orientar_acesso": (
            "Fornecer orientação para acesso à disciplina."
        ),
        "disponibilizar_recurso": (
            "Indicar o recurso acadêmico solicitado."
        ),
        "encaminhar_suporte": (
            "Encaminhar a solicitação ao suporte acadêmico."
        ),
        "nao_processar": (
            "Solicitação encerrada."
        ),
    }

    def perceber(self, solicitacao):
        return {
            "id": solicitacao["id"],
            "estudante": solicitacao["estudante"],
            "objetivo": solicitacao["objetivo"],
            "recurso": solicitacao["recurso"],
            "falha_tecnica": solicitacao["falha_tecnica"],
            "tentativas": solicitacao["tentativas"],
            "orientacao_anterior": solicitacao["orientacao_anterior"],
            "status": solicitacao["status"],
        }

    def decidir(self, contexto):
        if contexto["status"] == "encerrada":
            return "nao_processar"

        if not contexto["objetivo"]:
            return "solicitar_informacoes"

        if contexto["falha_tecnica"] is True:
            return "encaminhar_suporte"

        if contexto["tentativas"] >= 3:
            return "encaminhar_suporte"

        if contexto["objetivo"] == "acessar_material":
            if not contexto["recurso"]:
                return "solicitar_informacoes"

            return "disponibilizar_recurso"

        if contexto["objetivo"] == "acessar_disciplina":
            if contexto["falha_tecnica"] is None:
                return "solicitar_informacoes"

            if contexto["orientacao_anterior"] is True:
                return "encaminhar_suporte"

            return "orientar_acesso"

        return "solicitar_informacoes"

    def executar(self, acao, solicitacao, sucesso=True):
        if acao not in self.mensagens:
            return {
                "sucesso": False,
                "mensagem": "A ação selecionada não é válida.",
            }

        if acao == "nao_processar":
            return {
                "sucesso": True,
                "mensagem": self.mensagens[acao],
            }

        if not sucesso:
            return {
                "sucesso": False,
                "mensagem": (
                    "Não foi possível executar a ação da solicitação "
                    f"{solicitacao['id']}."
                ),
            }

        return {
            "sucesso": True,
            "mensagem": self.mensagens[acao],
        }

    def verificar_resultado(self, resultado):
        return resultado["sucesso"] is True

    def processar_solicitacao(self, solicitacao, sucesso_execucao=True):
        contexto = self.perceber(solicitacao)
        acao = self.decidir(contexto)
        resultado = self.executar(
            acao,
            solicitacao,
            sucesso=sucesso_execucao,
        )
        sucesso_confirmado = self.verificar_resultado(resultado)

        resposta = {
            "solicitacao": solicitacao["id"],
            "acao": acao,
            "sucesso": sucesso_confirmado,
            "mensagem": resultado["mensagem"],
        }

        print("Solicitação:", resposta["solicitacao"])
        print("Ação selecionada:", resposta["acao"])
        print("Execução confirmada:", resposta["sucesso"])
        print("Resultado:", resposta["mensagem"])
        print("=" * 60)


if __name__ == "__main__":
    agente = Agente()
    for solicitacao in agente.solicitacoes:
        print("\n--- Nova solicitação do agente ---")
        agente.processar_solicitacao(solicitacao)

    # teste do sétimo cenário, com a ação correta, mas a execução com falha
    print("\n--- Teste de falha na execução ---")
    agente.processar_solicitacao(
        agente.solicitacoes[0],
        sucesso_execucao=False,
    )
