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
            "recebeu_ajuda": False,
            "percentual_conclusao": 40,
            "tempo_disponivel": 30,
            "conteudo_nao_estudado": 20
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

    def calcular_utilidade(self):
        utilidade_ajuda = 0
        utilidade_revisao = 0

        if self.estado["acessos_atividades"] <= 2:
            utilidade_ajuda += 3


        if self.estado["acessos_atividades"] >= 3:
            utilidade_revisao += 3

        if self.estado["conteudo_nao_estudado"] >= 50:
            utilidade_revisao += 2

        if self.estado["percentual_conclusao"] >= 70:
            utilidade_ajuda += 2

        if self.estado["tempo_disponivel"] <= 20:
            utilidade_ajuda += 1

        print(f"Utilidade oferecer ajuda: {utilidade_ajuda}")
        print(f"Utilidade recomendar revisão: {utilidade_revisao}")

        if utilidade_revisao > utilidade_ajuda:
            return 'recomendar_revisao'

        return 'oferecer_ajuda'

    def decidir(self, percepcao):
        if percepcao == 'login':
            return 'mostrar_conteudo'

        if percepcao == 'logout':
            return 'finalizar'

        if percepcao == 'suporte':
            return (
                'encaminhar_suporte'
                if self.estado['autenticado']
                else 'solicitar_login'
            )

        if percepcao.startswith('pagina:'):
            if not self.estado['autenticado']:
                return 'solicitar_login'

            if self.estado['pagina'] == 'conteudo':
                return 'mostrar_conteudo'

            if self.estado['pagina'] == 'atividade':

                if self.estado['acessos_atividades'] == 1:
                    return 'mostrar_atividade'

                return self.calcular_utilidade()

    def executar(self, acao):
        if acao == 'solicitar_login':
            print("Ação executada: faça o login para continuar")

        elif acao == 'mostrar_conteudo':
            print("Ação executada: conteúdo mostrado com sucesso")

        elif acao == 'mostrar_atividade':
            print("Ação executada: atividade mostrada com sucesso")

        elif acao == 'oferecer_ajuda':
            print("Ação executada: ajuda oferecida com sucesso")
            self.estado["recebeu_ajuda"] = True

        elif acao == 'recomendar_revisao':
            print("Ação executada: revisão recomendada com sucesso")

        elif acao == 'encaminhar_suporte':
            print("Ação executada: suporte encaminhado com sucesso")

        elif acao == 'finalizar':
            print("Ação executada: logout finalizado com sucesso")

    def iniciar(self):
        percepcoes = [
            'pagina:atividade',
            'pagina:atividade',
            'pagina:atividade',
            'pagina:conteudo',
            'suporte',
            'logout'
        ]

        for percepcao in percepcoes:
            print(f"\n--- Nova Percepção do Agente: {percepcao} ---")
            self.atualizar_estado(percepcao)
            acao = self.decidir(percepcao)
            self.executar(acao)
            print(f"Estado atual: {self.estado}")
