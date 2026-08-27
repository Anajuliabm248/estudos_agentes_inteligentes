import agente_controle_acesso
import agente_loja
import agente_plataforma_cursos


def agente_ini():
    print("Bem vindo(a) à pasta de agentes inteligentes!")
    # agente_loja.iniciar_agente()
    # agente_controle_acesso.iniciar_agente()
    agente_plataforma_cursos.iniciar_agente()

if __name__ == '__main__':
    agente_ini()
