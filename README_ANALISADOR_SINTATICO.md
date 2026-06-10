# Analisador Sintático (Parser)

O analisador sintático é a segunda etapa do compilador. Ele recebe a lista linear de tokens gerada pelo analisador léxico e reconstrói a estrutura lógica do programa na forma de uma **Árvore de Sintaxe Abstrata (AST)**, validando se o código cumpre as regras gramaticais da linguagem Swhthon.

O módulo sintático deste projeto é implementado no arquivo [parser.py](parser.py).

---

## 1. Nós da AST (`Node` e `dataclasses`)

A estrutura do programa analisado é mapeada em uma árvore cujos nós são definidos usando classes decoradas com `@dataclass`. Os principais nós de dados e controle são:

*   `ProgramNode`: Raiz da árvore que contém uma lista com todos os comandos/declarações do programa (`statements`).
*   `DeclarationNode`: Declaração de variáveis. Armazena o tipo da variável (`type`), os nomes dos identificadores declarados (`identifiers`) e os valores de inicialização opcionais (`initializers`).
*   `PrintNode`: Comando de saída `chapa(...)`, contendo a expressão de impressão.
*   `InputNode`: Comando de entrada de dados `pembejeo(...)`, contendo a variável receptora.
*   `AssignmentNode`: Comando de atribuição, com a variável de destino (`identifier`) e a árvore da expressão avaliada (`expression`).
*   `IfNode` / `ElifNode`: Condicionais contendo a expressão de condição (`condition`), o bloco a ser executado (`then_branch`/`body`) e caminhos alternativos.
*   `WhileNode` / `ForNode`: Laços de repetição que armazenam suas condições de controle e listas de comandos internos.
*   `BinaryOpNode`: Operações matemáticas e relacionais contendo operandos esquerdo e direito e o operador.
*   `LiteralNode` / `VariableReferenceNode`: Folhas da árvore representando valores fixos ou referências a variáveis.

---

## 2. Algoritmo de Análise Sintática Preditiva LL(1)

O parser é construído como um **Analisador Preditivo de Descida Recursiva**, que realiza o mapeamento da gramática de cima para baixo (top-down) consumindo os tokens sequencialmente.

### Métodos Auxiliares de Controle de Fluxo
*   `current()`: Retorna o token atual sob o cursor sem consumi-lo da lista.
*   `eat(token_type)`: Verifica se o tipo do token atual coincide com o tipo esperado (`token_type`). Se for igual, avança o cursor e retorna o token consumido. Se houver divergência, interrompe o processo lançando um erro de sintaxe:
    ```python
    raise SyntaxError(f"Esperado {token_type}, encontrado {token}")
    ```

### Parsing de Estrutura Principal (`parse_program` / `parse_statement`)
*   O parser consome obrigatoriamente a abertura do programa (`programu`).
*   Em seguida, executa um laço consumindo instruções genéricas via `parse_statement()` até encontrar a marca de fim do programa (`mwisho.`). 
*   `parse_statement()` permite misturar livremente declarações de variáveis (`parse_declaration`) e comandos gerais (`parse_command`).

### Mapeamento de Comandos de Bloco
*   `parse_if()`: Consome cabeçalho `ikiwa <condição>.`, lê blocos recursivamente até parar nos stop-tokens `ELIF`, `ELSE` ou `END_IF` (palavra-chave `mwishoikiwa.`). Repete se encontrar `sivyo` ou `mwingine`, e consome a marca de encerramento `mwishoikiwa.` ao final.
*   `parse_while()`: Consome cabeçalho `wakati <condição>.`, e chama recursivamente `parse_block` até parar no stop-token `END_WHILE` (palavra-chave `mwishowakati.`), consumindo a marca de encerramento `mwishowakati.` ao final.
*   `parse_for()`: Consome cabeçalho `kwa <id> := <inicio>, <fim>.`, lê o bloco interno de comandos até parar no stop-token `END_FOR` (palavra-chave `mwishokwa.`), e consome a marca de encerramento `mwishokwa.` ao final.

---

## 3. Resolução da Precedência Matemática sem Recursividade à Esquerda

Gramáticas de descida recursiva entram em loop infinito se houver recursividade à esquerda (por exemplo, `E -> E + T`). Para contornar esse problema e respeitar as regras matemáticas de precedência, o parser quebra a gramática de expressões em níveis hierárquicos e substitui a recursão por laços (`while`):

```
expressao   -> relacional
relacional  -> aditivo { ('<' | '>' | '==') aditivo }
aditivo     -> termo { ('+' | '-') termo }
termo       -> fator { ('*' | '/') fator }
fator       -> NUMBER | TEXT | BOOLEAN | ID | '(' expressao ')'
```

Essa estrutura hierárquica garante que a árvore sintática seja construída de forma que:
1.  Os parênteses e valores literais fiquem no nível mais interno da árvore (`parse_factor`).
2.  A multiplicação e a divisão sejam priorizadas (`parse_term`), ficando aninhadas abaixo de operações de soma e subtração (`parse_additive`).
3.  Operadores de comparação sejam avaliados por último no topo da hierarquia de expressões aritméticas (`parse_relational`).
4.  O laço `while` nas funções lê os operandos da esquerda para a direita de forma iterativa, eliminando a recursividade à esquerda.
