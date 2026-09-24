def iniciar_agente():
    print("Você está acessando: Agente de loja")
    agente = Agente()
    agente.iniciar()


class Agente:
    def __init__(self):
        self.estado = {
            "logado": False,
            "prod_atual": None,
            "carrinho": []
        }
        self.add = 0
        self.rem = 0

    def atualizar_estado(self, percepcao):
        if percepcao == 'login':
            self.estado["logado"] = True

        elif percepcao == 'logout':
            self.estado["logado"] = False

        elif percepcao.startswith('visualizou:'):
            self.estado["prod_atual"] = percepcao.split(':')[1]

        elif percepcao.startswith('adicionou:'):
            produto = percepcao.split(':')[1]
            if produto not in self.estado["carrinho"]:
                self.estado["carrinho"].append(produto)
                self.add += 1

        elif percepcao.startswith('remover:'):
            produto = percepcao.split(':')[1]
            if produto not in self.estado["carrinho"]:
                print(f'Aviso: O produto "{produto}" não consta no carrinho.')
            else:
                self.estado["carrinho"].remove(produto)
                self.rem += 1

    def decidir(self, percepcao):
        if percepcao == 'login':
            return 'permitir_acesso'

        if percepcao == 'logout':
            if len(self.estado["carrinho"]) > 0:
                return 'oferecer_recuperacao'
            return 'encerrar_sessao'

        if percepcao.startswith('visualizou:'):
            return 'visualizou_prod'

        if percepcao.startswith('adicionou:'):
            return 'adicionou_prod'

        if percepcao.startswith('remover:'):
            return 'remover_prod'

    def executar(self, acao):
        if acao == 'permitir_acesso':
            print("Ação executada: Logado com sucesso!")
        elif acao == 'encerrar_sessao':
            print("Ação executada: Logout feito com sucesso.")
        elif acao == 'oferecer_recuperacao':
            print("Ação executada: Atenção! Você tem itens no carrinho. Deseja realmente sair?")
        elif acao == 'visualizou_prod':
            print("Ação executada: Visualizou produto.")
        elif acao == 'adicionou_prod':
            print("Ação executada: Adicionou produto no carrinho.")
        elif acao == 'remover_prod':
            print("Ação executada: Removeu ou tentou remover produto do carrinho.")

    # como a regra própria do sistema é baseada na remoção de produtos, logo o seu
    # desempenho é baseado na relação entre adicionado e retirado do carrinho,
    # quanto maior a taxa de retenção, melhor o desempenho do agente

    def exibir_desempenho(self):
        print('\n==========================================================')
        print('Desempenho do agente')
        print(f"Adicionados no carrinho: {self.add}")
        print(f"Removidos do carrinho: {self.rem}")

        if self.add > 0:
            taxa_retencao = ((self.add - self.rem) / self.add) * 100
            print(f"Taxa de retenção no carrinho: {taxa_retencao:.1f}%")
        print('==========================================================\n')

    def iniciar(self):
        percepcoes = [
            'login', 'visualizou:notebook', 'adicionou:notebook',
            'visualizou:mouse', 'adicionou:mouse', 'remover:mouse', 'logout'
        ]

        for percepcao in percepcoes:
            print(f"\n--- Nova Percepção do Agente: {percepcao} ---")
            self.atualizar_estado(percepcao)
            acao = self.decidir(percepcao)
            self.executar(acao)
            print(f"Estado atual: {self.estado}")

        self.exibir_desempenho()
        return self.add, self.rem