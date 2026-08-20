def iniciar_agente():
    print("Você está acessando: Agente de controle de acesso")
    agente = Agente()
    agente.iniciar()


class Agente:
    def __init__(self):
        self.estado = {
            "logado": False,
            "pagina_atual": "/",
            "tentativas_admin": 0,
            "bloqueado": False
        }

    def atualizar_estado(self, percepcao):
        if percepcao == 'login_sucesso':
            self.estado["logado"] = True

        elif percepcao == 'logout':
            self.estado["logado"] = False
            self.estado['pagina_atual'] = '/'

        elif percepcao.startswith('acesso_pagina:'):
            pagina = percepcao.split(':')[1]
            self.estado["pagina_atual"] = pagina

        elif percepcao == 'acesso_admin':
            if self.estado['bloqueado']:
                pass
            elif not self.estado['logado']:
                self.estado['tentativas_admin'] += 1
                if self.estado['tentativas_admin'] >= 3:
                    self.estado['bloqueado'] = True
            else:
                self.estado['pagina_atual'] = '/admin'

    def decidir(self, percepcao):
        if percepcao == 'login_sucesso':
            return 'registrar_acesso'

        if percepcao == 'logout':
            return 'encerrar_sessao'

        if percepcao.startswith('acesso_pagina:'):
            return 'acesso_pagina'

        if percepcao == 'acesso_admin':
            if self.estado['bloqueado']:
                return 'bloquear_acesso'
            elif not self.estado['logado']:
                return 'negar_acesso_admin'
            else:
                return 'permitir_acesso_admin'

    def executar(self, acao):
        if acao == 'registrar_acesso':
            print("Ação executada: Logado com sucesso!")
        elif acao == 'encerrar_sessao':
            print("Ação executada: Logout feito com sucesso.")
        elif acao == 'acesso_pagina':
            print("Ação executada: Acessando página:", self.estado['pagina_atual'])
        elif acao == 'permitir_acesso_admin':
            print('Ação executada: Acesso à página de admin permitido.')
        elif acao == 'negar_acesso_admin':
            print('Ação executada: Acesso à página de admin negado, necessário autenticação prévia!')
        elif acao == 'bloquear_acesso':
            print('Ação executada: SISTEMA BLOQUEADO - Múltiplas tentativas falhas.')

    def exibir_desempenho(self):
        print('\n==========================================================')
        print('Desempenho do agente')
        print(f"Tentativas de acesso admin não autorizado: {self.estado['tentativas_admin']}")
        print(f"Status da conta: {'Bloqueada' if self.estado['bloqueado'] else 'Ativa'}")
        print('==========================================================\n')

    def iniciar(self):
        percepcoes = [
            'login_sucesso', 'acesso_pagina:/produtos', 'acesso_admin', 'logout',
            'acesso_admin', 'acesso_admin', 'acesso_admin', 'acesso_admin'
        ]

        for percepcao in percepcoes:
            print(f"\n--- Nova Percepção do Agente: {percepcao} ---")
            self.atualizar_estado(percepcao)
            acao = self.decidir(percepcao)
            self.executar(acao)
            print(f"Estado atual: {self.estado}")

        self.exibir_desempenho()