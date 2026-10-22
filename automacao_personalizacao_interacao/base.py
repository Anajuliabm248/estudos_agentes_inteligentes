def perceber(relato):
    return {
        "servico": relato.get("servico"),
        "erro": relato.get("erro"),
        "falha_tecnica": relato.get("falha_tecnica"),
        "tentativas": relato.get("tentativas", 0)
    }


def decidir(contexto):
    if not contexto["servico"]:
        return "solicitar_dados"
    if contexto["tentativas"] >= 3:
        return "encaminhar"
    if contexto["falha_tecnica"] is True:
        return "encaminhar"
    if contexto["erro"] == "senha":
        return "orientar_senha"
    if contexto["falha_tecnica"] is None:
        return "solicitar_detalhes"
    return "orientar"


def executar(acao):
    # Simulação; uma aplicação real chamaria um serviço.
    if acao == "solicitar_dados":
        return {"sucesso": True, "estado": "aguardando_dados"}
    if acao == "solicitar_detalhes":
        return {"sucesso": True, "estado": "aguardando_detalhes"}
    if acao == "orientar_senha":
        return {"sucesso": True, "estado": "orientacao_apresentada"}
    if acao == "orientar":
        return {"sucesso": True, "estado": "orientacao_apresentada"}
    if acao == "encaminhar":
        return {"sucesso": True, "estado": "encaminhada"}
    return {"sucesso": False, "estado": "acao_desconhecida"}


def verificar(resultado):
    if resultado["sucesso"]:
        return f"Operação confirmada: {resultado['estado']}"
    return "Não foi possível confirmar a execução."


def atender(relato):
    contexto = perceber(relato)
    acao = decidir(contexto)
    resultado = executar(acao)
    return {
        "acao_selecionada": acao,
        "resultado": verificar(resultado)
    }


casos = [
    {"relato": {"servico": None, "erro": None},
     "esperada": "solicitar_dados"},
    {"relato": {"servico": "disciplinas", "erro": "senha",
                "falha_tecnica": False, "tentativas": 1},
     "esperada": "orientar_senha"},
    {"relato": {"servico": "disciplinas", "erro": "pagina indisponivel",
                "falha_tecnica": True, "tentativas": 1},
     "esperada": "encaminhar"}
]

for caso in casos:
    contexto = perceber(caso["relato"])
    acao = decidir(contexto)
    print(acao, acao == caso["esperada"])