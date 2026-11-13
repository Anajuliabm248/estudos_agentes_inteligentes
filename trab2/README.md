# Trabalho 2 - Agente Inteligente para Economia de Energia
> Ana Júlia Bock Medina - SPI UFSM
> Agentes Iteligentes para Sistemas Web - Leandro Freitas

## Resumo
- Este projeto implementa um agente inteligente que analisa o consumo de energia de uma residência, identifica oportunidades de economia e recomenda ações conforme as prioridades dos moradores;
- O usuário pode aceitar ou rejeitar recomendações;
- O agente atualiza seu estado a cada resposta, assim recomendações tratadas deixam de ficar pendentes e o consumo estimado é reduzido quando uma ação é aceita.

## Instruções de execução

1. Abra a pasta trab2 em uma IDE (de preferência Pycharm)

2. Execute o programa no terminal com:

```bash
python agente_energia.py
```

ou então em `Run` agente_energia (shift + F10)

3. O programa apresentará os dados da residência, as recomendações ordenadas e o estado inicial da simulação.

4. Depois, escolha uma recomendação pendente pelo número exibido.

5. Para a recomendação escolhida, informe:

```text
1 - Aceitar
2 - Rejeitar
```

6. Digite `0` na escolha de recomendações quando quiser encerrar a simulação.


## Dependências

O projeto foi desenvolvido em Python e utiliza a biblioteca Pandas para ler e organizar o arquivo CSV.
Assim, caso o Pandas não esteja instalado, execute:

```bash
python -m pip install pandas
```

Sys e Time são utilizados apenas para perfumaria do terminal.

## Residência demonstrada

A residência utilizada na demonstração é a `R01`.

Ela é configurada no método `carregar_dados_residencia()` pela variável:

```python
residencia_id = 'R01'
```

Para testar outra residência, basta trocar esse valor por outra residência entre `R01` e `R10`.
Ao trocar o identificador, o programa carrega os novos dados, utiliza os respectivos pesos e gera recomendações personalizadas para a residência selecionada.

## Explicação dos métodos

### `carregando()`

Exibe uma pequena animação de carregamento antes de mostrar as recomendações (enfeite).

### `perceber(df)`

Recebe os dados filtrados da residência e organiza as informações que o agente precisa observar:

- Dados gerais da residência.
- Pesos de economia, conforto, flexibilidade e baixo esforço.
- Equipamentos e seus atributos.
- Consumo diário inicial da residência.

### `oportunidades_elegiveis(equipamentos)`

Analisa cada equipamento e seleciona somente as oportunidades que atendem aos quatro critérios definidos no trabalho:

- Possui redução de uso.
- Tem economia potencial maior que zero.
- Não é essencial.
- Tem impacto no conforto menor ou igual a três.

### `calcular_utilidade(oportunidades, pesos)`

Calcula as notas de economia, conforto, flexibilidade e baixo esforço para cada oportunidade elegível.

Depois, utiliza os pesos da residência para calcular a utilidade final de cada recomendação.

### `ordenar_recomendacoes(oportunidades)`

Ordena as oportunidades pela utilidade calculada, da maior para a menor.

### `estado_inicial(contexto, recomendacoes)`

Cria o estado inicial da simulação, guardando:

- Residência selecionada.
- Consumo diário estimado.
- Oportunidades pendentes.

### `dados_residencia(contexto)`

Apresenta os dados da residência selecionada, incluindo número de moradores, meta de consumo, tarifa, perfil e prioridades.

### `apresentacao(recomendacoes)`

Exibe as recomendações ordenadas, mostrando equipamento, categoria, economia potencial, impacto no conforto, flexibilidade, esforço, utilidade e descrição da oportunidade.

Também registra as recomendações que já foram apresentadas ao usuário.

### `feedback()`

Permite que o usuário escolha uma recomendação pendente para tratar ou encerrar a simulação.

### `resposta(recomendacao)`

Recebe a decisão de aceitar ou rejeitar a recomendação escolhida.

Quando a recomendação é aceita, ela é registrada, removida das pendentes e sua economia potencial é subtraída do consumo diário estimado.

Quando a recomendação é rejeitada, ela é registrada e removida das pendentes, mas o consumo permanece igual.

### `mostrar_estado()`

Exibe o estado atual do agente, incluindo recomendações apresentadas, aceitas, rejeitadas e pendentes, além do consumo diário estimado atualizado.

### `inicio()`

Coordena o funcionamento completo do agente:

1. Carrega os dados da residência.
2. Percebe e organiza as informações.
3. Identifica oportunidades elegíveis.
4. Calcula a utilidade.
5. Ordena e apresenta as recomendações.
6. Inicia a interação com o usuário.