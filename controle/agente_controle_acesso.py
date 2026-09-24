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
            "bloqueado": False,

            # estdos adicionados da regra extra
            "sessao_suspeita": False,
            "admin_confirmado": False,
            "codigo_validado": False
        }

    def atualizar_estado(self, percepcao):
        if percepcao == 'login_sucesso':
            self.estado["logado"] = True

        elif percepcao == 'logout':
            self.estado["logado"] = False
            self.estado["pagina_atual"] = "/"
            self.estado["admin_confirmado"] = False
            self.estado["codigo_validado"] = False

        elif percepcao.startswith('acesso_pagina:'):
            pagina = percepcao.split(':')[1]
            self.estado["pagina_atual"] = pagina

        elif percepcao == 'acesso_admin':
            if self.estado["bloqueado"]:
                pass

            elif not self.estado["logado"]:
                self.estado["tentativas_admin"] += 1

                if self.estado["tentativas_admin"] >= 2:
                    self.estado["sessao_suspeita"] = True

                if self.estado["tentativas_admin"] >= 3:
                    self.estado["bloqueado"] = True

            elif self.estado["sessao_suspeita"]:
                # caso a sessão for suspeita, o acesso só é liberado depois da confirmação completa
                if self.estado["admin_confirmado"] and self.estado["codigo_validado"]:
                    self.estado["pagina_atual"] = "/admin"
                    self.estado["sessao_suspeita"] = False
                else:
                    pass

            else:
                self.estado["pagina_atual"] = "/admin"

        elif percepcao == 'credenciais_admin_validas':
            if self.estado["logado"] and self.estado["sessao_suspeita"]:
                self.estado["admin_confirmado"] = True

        elif percepcao == 'credenciais_admin_invalidas':
            self.estado["admin_confirmado"] = False
            self.estado["codigo_validado"] = False
            self.estado["tentativas_admin"] += 1

            if self.estado["tentativas_admin"] >= 3:
                self.estado["bloqueado"] = True

        elif percepcao == 'codigo_seguranca_valido':
            if self.estado["admin_confirmado"]:
                self.estado["codigo_validado"] = True

        elif percepcao == 'codigo_seguranca_invalido':
            self.estado["codigo_validado"] = False
            self.estado["tentativas_admin"] += 1

            if self.estado["tentativas_admin"] >= 3:
                self.estado["bloqueado"] = True

    def decidir(self, percepcao):
        if percepcao == 'login_sucesso':
            return 'registrar_acesso'

        if percepcao == 'logout':
            return 'encerrar_sessao'

        if percepcao.startswith('acesso_pagina:'):
            return 'acesso_pagina'

        if percepcao == 'acesso_admin':
            if self.estado["bloqueado"]:
                return 'bloquear_acesso'

            elif not self.estado["logado"]:
                return 'negar_acesso_admin'

            elif self.estado["sessao_suspeita"]:
                if self.estado["admin_confirmado"] and self.estado["codigo_validado"]:
                    return 'permitir_acesso_admin'
                else:
                    return 'exigir_verificacao_admin'

            else:
                return 'permitir_acesso_admin'

        if percepcao == 'credenciais_admin_validas':
            return 'solicitar_codigo_seguranca'

        if percepcao == 'credenciais_admin_invalidas':
            if self.estado["bloqueado"]:
                return 'bloquear_acesso'
            return 'negar_credenciais_admin'

        if percepcao == 'codigo_seguranca_valido':
            return 'verificacao_concluida'

        if percepcao == 'codigo_seguranca_invalido':
            if self.estado["bloqueado"]:
                return 'bloquear_acesso'
            return 'negar_codigo_seguranca'

        return 'acao_desconhecida'

    def executar(self, acao):
        if acao == 'registrar_acesso':
            print("Ação executada: Logado com sucesso!")

        elif acao == 'encerrar_sessao':
            print("Ação executada: Logout feito com sucesso.")

        elif acao == 'acesso_pagina':
            print("Ação executada: Acessando página:", self.estado["pagina_atual"])

        elif acao == 'permitir_acesso_admin':
            print("Ação executada: Acesso à página de admin permitido.")

        elif acao == 'negar_acesso_admin':
            print("Ação executada: Acesso à página de admin negado, necessário autenticação prévia!")

        elif acao == 'bloquear_acesso':
            print("Ação executada: SISTEMA BLOQUEADO - Múltiplas tentativas falhas.")

        elif acao == 'exigir_verificacao_admin':
            print("Ação executada: Verificação administrativa reforçada exigida.")
            print("Informe e-mail, senha de administrador e código de segurança.")

        elif acao == 'solicitar_codigo_seguranca':
            print("Ação executada: Credenciais de administrador válidas.")
            print("Agora informe o código de segurança.")

        elif acao == 'negar_credenciais_admin':
            print("Ação executada: Credenciais administrativas inválidas.")

        elif acao == 'verificacao_concluida':
            print("Ação executada: Código de segurança válido. Verificação concluída.")

        elif acao == 'negar_codigo_seguranca':
            print("Ação executada: Código de segurança inválido.")

        elif acao == 'acao_desconhecida':
            print("Ação executada: Nenhuma ação definida para essa percepção.")

    def exibir_desempenho(self):
        print('\n==========================================================')
        print('Desempenho do agente')
        print(f"Tentativas de acesso admin não autorizado: {self.estado['tentativas_admin']}")
        print(f"Status da conta: {'Bloqueada' if self.estado['bloqueado'] else 'Ativa'}")
        print(f"Sessão suspeita: {'Sim' if self.estado['sessao_suspeita'] else 'Não'}")
        print(f"Admin confirmado: {'Sim' if self.estado['admin_confirmado'] else 'Não'}")
        print(f"Código validado: {'Sim' if self.estado['codigo_validado'] else 'Não'}")
        print('==========================================================\n')

    def iniciar(self):
        percepcoes = [
            'acesso_admin',
            'acesso_pagina:/produtos',
            'acesso_admin',
            'login_sucesso',
            'acesso_admin',
            'credenciais_admin_validas',
            'codigo_seguranca_valido',
            'acesso_admin',
            'logout',
            'acesso_admin',
            'acesso_admin',
        ]

        for percepcao in percepcoes:
            print(f"\n--- Nova Percepção do Agente: {percepcao} ---")
            print(f"Estado anterior: {self.estado}")

            self.atualizar_estado(percepcao)
            acao = self.decidir(percepcao)
            self.executar(acao)

            print(f"Novo estado: {self.estado}")

        self.exibir_desempenho()
