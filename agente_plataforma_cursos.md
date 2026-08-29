# Atividades da aula 4 - Agentes de plataforma de cursos
> Estudo sobre a arquitetura de agentes

### PARTE 1
#### Quais informações são utilizadas para tomar a decisão?
    autenticado, página e tentativas

#### O agente utiliza informações de acontecimentos anteriores? 
    sim, ele guarda tentativas na memória

#### O agente consegue diferenciar duas situações que possuem a mesma percepção atual?
    sim, baseado nas tentativas ou se está logado ou não

#### O que acontece quando nenhuma regra é satisfeita?
    Não foi implementado nada que não tivesse regra definida


### PARTE 2
#### Para o agente reflexivo simples, as duas situações são indistinguíveis. Explique por que o agente não consegue utilizar o fato de que o  usuário já havia acessado a atividade anteriormente.
    No caso demonstrado ele não conseguiu utilizar o fato de que o usuário já havia acessado a atividade
    já que não havia sido implementada memória no agente, assim toda tentativa é a primeira

### PARTE 3
#### O que mudou na arquitetura do agente?
    agora ele possui memória, logo consegue saber quantas tentativas de acessar a atividade já foram feitas

#### Por que esse agente consegue distinguir situações que o agente anterior não conseguia?
    porque ele não tinha estado interno (memória)

#### Que tipo de informação pode ser mantida no estado interno?
    estado de autenticação, acessos, tentativas totais e se recebeu ajuda

### PARTE 4
#### Qual é o estado atual?
    O estado atual contém informações sobre:
    - se o usuário está autenticado
    - página atual
    - quantidade de acessos à atividade
    - tentativas totais
    - se o usuário já recebeu ajuda

#### Qual é o objetivo?
    Ajudar o usuário a concluir a atividade

#### Quais ações poderiam aproximar o agente do objetivo?
    mostrar_atividade, recomendar_revisao, oferecer_ajuda e encaminhar_suporte

#### Como o objetivo pode ser modelado a nível de código?
    O agente pode analisar seu estado atual e escolher uma ação
    que ajude o usuário a avançar na atividade, como foi implementado no código
    Por exemplo:
        - primeiro acesso -> mostrar atividade
        - segundo acesso -> recomendar revisão
        - vários acessos -> oferecer ajuda

#### Por que uma arquitetura orientada a objetivos é mais adequada para esse problema do que simplesmente adicionar novas regras?
    Porque o agente passa a escolher ações pensando no objetivo que
    deseja alcançar, que é ajudar o usuário a concluir a atividade.
    Apenas adicionar regras pode deixar o agente cada vez mais complexo
    e preso a situações específicas. Com um objetivo, diferentes ações
    podem ser avaliadas de acordo com o quanto ajudam o usuário a avançar,
    assim sendo ideal já que não se prende a uma regra específica, como é o caso do número de acessos

### PARTE 5

#### Qual é a diferença entre possuir um objetivo e possuir critérios de preferência?
    O objetivo indica o que o agente deseja alcançar, logo os critérios de preferência ajudam o agente a escolher qual ação
    é mais adequada quando existem várias ações que podem atingir esse mesmo objetivo


#### Por que a existência de duas ações capazes de contribuir para o mesmo objetivo pode exigir uma avaliação de utilidade?
    Porque as duas ações podem ajudar, mas uma delas pode ser mais
    adequada dependendo da situação do usuário. A utilidade permite
    comparar as opções e escolher a que provavelmente terá melhor resultado.


#### Em uma aplicação real, que outros critérios poderiam ser utilizados?
    - desempenho do usuário nas atividades anteriores   
    - tempo que ele está parado na atividade
    - quantidade de erros
    - dificuldade da atividade
    - conteúdos que já foram estudados
    - preferência do usuário por ajuda ou revisão


#### A nível de código, como a utilidade poderia ser implementada?
    Poderia ser atribuindo uma pontuação para cada ação de acordo
    com o estado atual do usuário e escolhendo a ação com maior pontuação.

### PARTE 6
| Arquitetura | Informações utilizadas | Como decide? | Principal vantagem | Principal limitação |
|---|---|---|---|---|
| Reflexivo simples | Apenas a percepção atual | Utiliza regras de condição e ação | É simples e rápido | Não considera acontecimentos anteriores |
| Baseado em modelo | Percepção atual e estado interno | Utiliza regras considerando também informações armazenadas na memória | Consegue utilizar histórico e diferenciar situações parecidas | Ainda depende bastante de regras definidas |
| Orientado a objetivos | Percepção, estado interno e objetivo | Escolhe ações que ajudam a alcançar o objetivo definido | Permite considerar diferentes caminhos para alcançar um resultado | Pode exigir uma análise maior das ações possíveis |
| Baseado em utilidade | Percepção, estado interno, objetivo e critérios de preferência | Compara a utilidade das ações e escolhe a mais adequada | Consegue escolher entre várias ações possíveis de acordo com a situação | É mais complexo e exige definir critérios de avaliação |

#### Qual das quatro arquiteturas você utilizaria para o agente da plataforma de cursos? Justifique.
    Eu utilizaria a arquitetura baseada em utilidade, porque o agente pode possuir várias maneiras de ajudar o usuário a concluir uma atividade.
    Além de considerar o histórico e o objetivo de conclusão, o agente poderia avaliar informações como número de tentativas, percentual de conclusão do curso, tempo disponível e quantidade de conteúdo ainda não estudado.
    Dessa forma, ele poderia comparar ações como oferecer ajuda e recomendar revisão e escolher aquela que for mais adequada para a situação atual do usuário.

### Desafio final