def perceber(solicitacao):
    # Organiza as informações relevantes para a decisão.
    return {
        "id": solicitacao["id"],
        "estudante": solicitacao["estudante"],
        "objetivo": solicitacao["objetivo"],
        "recurso": solicitacao["recurso"],
        "falha_tecnica": solicitacao["falha_tecnica"],
        "tentativas": solicitacao["tentativas"],
        "orientacao_anterior": solicitacao["orientacao_anterior"],
        "status": solicitacao["status"]
    }


def decidir(contexto):
    # Seleciona uma ação de acordo com o contexto observado.

    if contexto["status"] == "encerrada":
        return "nao_processar"

    if not contexto["objetivo"]:
        return "solicitar_informacoes"

    if contexto["tentativas"] >= 3:
        return "encaminhar_suporte"

    if contexto["falha_tecnica"] is True:
        return "encaminhar_suporte"

    if contexto["objetivo"] == "acessar_material":
        if not contexto["recurso"]:
            return "solicitar_informacoes"

        return "disponibilizar_recurso"

    if contexto["objetivo"] == "acessar_disciplina":
        if contexto["falha_tecnica"] is None:
            return "solicitar_informacoes"

        if contexto["orientacao_anterior"]:
            return "encaminhar_suporte"

        return "orientar_acesso"

    return "solicitar_informacoes"


def executar(acao, contexto, sucesso=True):
    # Simula a execução da ação selecionada.

    if acao == "nao_processar":
        return {
            "sucesso": True,
            "confirmado": True,
            "mensagem": "Solicitação encerrada; nenhuma ação realizada."
        }

    if not sucesso:
        return {
            "sucesso": False,
            "confirmado": False,
            "mensagem": "Não foi possível confirmar a execução da ação."
        }

    mensagens = {
        "solicitar_informacoes":
            "Solicitar informações complementares ao estudante.",
        "orientar_acesso":
            "Fornecer orientação para acesso à disciplina.",
        "disponibilizar_recurso":
            "Indicar o recurso acadêmico solicitado.",
        "encaminhar_suporte":
            "Encaminhar a solicitação ao suporte acadêmico."
    }

    return {
        "sucesso": True,
        "confirmado": True,
        "mensagem": mensagens[acao]
    }


def verificar_resultado(resultado):
    # Verifica se a execução foi confirmada.
    return (
        resultado["sucesso"]
        and resultado["confirmado"]
    )


def processar_solicitacao(solicitacao, sucesso_execucao=True):
    #Coordena as etapas de funcionamento do agente.

    contexto = perceber(solicitacao)
    acao = decidir(contexto)

    resultado = executar(acao, contexto, sucesso_execucao)

    confirmado = verificar_resultado(resultado)

    resposta = {
        "solicitacao": solicitacao["id"],
        "acao": acao,
        "mensagem": resultado["mensagem"],
        "confirmado": confirmado
    }

    print("Solicitação:", resposta["solicitacao"])
    print("Ação selecionada:", resposta["acao"])
    print("Resultado:", resposta["mensagem"])
    print("Execução confirmada:", resposta["confirmado"])
    print("-" * 40)

    return resposta


solicitacoes = [
    {
        "id": 101,
        "estudante": 25,
        "objetivo": "acessar_material",
        "recurso": "disciplina",
        "falha_tecnica": False,
        "tentativas": 0,
        "orientacao_anterior": False,
        "status": "aberta"
    },
    {
        "id": 102,
        "estudante": 26,
        "objetivo": "acessar_disciplina",
        "recurso": "disciplina",
        "falha_tecnica": None,
        "tentativas": 1,
        "orientacao_anterior": False,
        "status": "aberta"
    },
    {
        "id": 103,
        "estudante": 27,
        "objetivo": "acessar_disciplina",
        "recurso": "disciplina",
        "falha_tecnica": True,
        "tentativas": 1,
        "orientacao_anterior": False,
        "status": "aberta"
    },
    {
        "id": 104,
        "estudante": 28,
        "objetivo": "acessar_disciplina",
        "recurso": "disciplina",
        "falha_tecnica": False,
        "tentativas": 3,
        "orientacao_anterior": False,
        "status": "aberta"
    },
    {
        "id": 105,
        "estudante": 29,
        "objetivo": "acessar_disciplina",
        "recurso": "disciplina",
        "falha_tecnica": False,
        "tentativas": 1,
        "orientacao_anterior": True,
        "status": "aberta"
    },
    {
        "id": 106,
        "estudante": 30,
        "objetivo": "acessar_material",
        "recurso": "disciplina",
        "falha_tecnica": False,
        "tentativas": 0,
        "orientacao_anterior": False,
        "status": "encerrada"
    }
]

for solicitacao in solicitacoes:
    processar_solicitacao(solicitacao)


processar_solicitacao(solicitacoes[2], sucesso_execucao=False)