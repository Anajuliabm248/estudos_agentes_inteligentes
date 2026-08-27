def iniciar_agente():
    print("Você está acessando: Agente de plataforma de cursos")
    agente = Agente()
    agente.iniciar()


class Agente:
    def __init__(self):
        self.estado = {
            "autenticado": True,
            "pagina": "atividade",
            "acessos_atividades": 0,
            "tentativas_total": 0,
            "recebeu_ajuda": False
        }

    def atualizar_estado(self, percepcao):
        if percepcao == 'login':
            self.estado["autenticado"] = True

        if percepcao == 'logout':
            self.estado["autenticado"] = False
            self.estado["pagina"] = 'login'
            self.estado["acessos_atividades"] = 0

        if percepcao.startswith('pagina:') and self.estado['autenticado']:
            self.estado["pagina"] = percepcao.split(':')[1]

            if self.estado['pagina'] == 'atividade':
                self.estado["acessos_atividades"] += 1
                self.estado["tentativas_total"] += 1

                if self.estado["acessos_atividades"] >=4:
                    self.estado["recebeu_ajuda"] = True


    # só faz o return para o executar (define a ação)
    def decidir(self, percepcao):
        if percepcao == 'login':
            return 'mostrar_conteudo'

        if percepcao == 'logout':
            return 'finalizar'

        if percepcao == 'suporte':
            return 'encaminhar_suporte' if self.estado['autenticado'] else 'solicitar_login'

        if percepcao.startswith('pagina:'):
            if not self.estado['autenticado']:
                return 'solicitar_login'

            if self.estado['pagina'] == 'conteudo':
                return 'mostrar_conteudo'

            if self.estado['pagina'] == 'atividade':
                if self.estado['acessos_atividades'] == 1:
                    return 'mostrar_atividade'
                elif self.estado['acessos_atividades'] == 3:
                    return 'recomendar_revisao'
                elif self.estado['acessos_atividades'] >= 4:
                    return 'oferecer_ajuda'

    def executar(self, acao):
        if acao == 'solicitar_login':
            print("Ação executada: faça o login para continuar")

        elif acao == 'mostrar_conteudo':
            print("Ação executada: conteudo mostrado com sucesso")

        elif acao == 'mostrar_atividade':
            print("Ação executada: atividade mostrado com sucesso")

        elif acao == 'oferecer_ajuda':
            print("Ação executada: ajuda oferecida com sucesso")

        elif acao == 'recomendar_revisao':
            print("Ação executada: revisão recomendada com sucesso")

        elif acao == 'encaminhar_suporte':
            print("Ação executada: suporte encaminhado com sucesso")

        elif acao == 'finalizar':
            print("Ação executada: logout finalizado com sucesso")


    def iniciar(self):
        percepcoes = [
            'pagina:atividade', 'pagina:conteudo', 'pagina:atividade', 'logout', 'pagina:atividade', 'login', 'pagina:atividade', 'pagina:atividade', 'suporte', 'logout'
        ]

        for percepcao in percepcoes:
            print(f"\n--- Nova Percepção do Agente: {percepcao} ---")
            self.atualizar_estado(percepcao)
            acao = self.decidir(percepcao)
            self.executar(acao)
            print(f"Estado atual: {self.estado}")



    # PARTE 1
    # Quais informações são utilizadas para tomar a decisão?
    #    autenticado, página e tentativas

    # O agente utiliza informações de acontecimentos anteriores?
    #    sim, ele guarda tentativas na memória

    # O agente consegue diferenciar duas situações que possuem a mesma percepção atual?
    #    sim, baseado nas tentativas ou se está logado ou não

    # O que acontece quando nenhuma regra é satisfeita?
    #    Não foi implementado nada que não tivesse regra definida


    # PARTE 2
    # Para o agente reflexivo simples, as duas situações são indistinguíveis.
    # Explique por que o agente não consegue utilizar o fato de que o usuário já havia acessado a atividade anteriormente.
    #    No caso demonstrado ele não conseguiu utilizar o fato de que o usuário já havia acessado a atividade
    #    já que não havia sido implementada memória no agente, assim toda tentativa é a primeira

    # PARTE 3
    # O que mudou na arquitetura do agente?
    #    agora ele possui memória, logo consegue saber quantas tentativas de acessar a atividade já foram feitas

    # Por que esse agente consegue distinguir situações que o agente anterior não conseguia?
    #    porque ele não tinha estado interno (memória)

    # Que tipo de informação pode ser mantida no estado interno?
    #    estado de autenticação, acessos, tentativas totais e se recebeu ajuda