# Analisador Semântico (Semantic Analyzer)

O analisador semântico é a terceira etapa do compilador. Ele percorre a Árvore de Sintaxe Abstrata (AST) gerada pelo parser e valida se o programa faz sentido lógico e respeita as regras de contexto da linguagem Swhthon, tais como tipos de dados, escopo e declarações de variáveis.

O analisador semântico deste projeto é implementado no arquivo [semantic.py](semantic.py).

---

## 1. Tabela de Símbolos (`self.symbols`)

A tabela de símbolos é a estrutura de dados central do analisador semântico. Ela é implementada como um dicionário Python em que:
*   As **chaves** representam os nomes das variáveis (identificadores) declarados no programa.
*   Os **valores** guardam o tipo da variável (`'int'`, `'float'`, `'string'` ou `'bool'`).

---

## 2. O Padrão de Projeto Visitor (Visitor Pattern)

O analisador semântico caminha pela árvore sintática utilizando o padrão de projeto **Visitor**. 

O método genérico `visit(node)` obtém a classe do nó atual e resolve dinamicamente o método correspondente utilizando reflexão em tempo de execução:

```python
method_name = f"visit_{node.__class__.__name__}"
visitor = getattr(self, method_name, self.generic_visit)
return visitor(node)
```
Isso separa as regras de checagem semântica das definições físicas dos nós da AST em classes distintas, mantendo o código modular e extensível.

---

## 3. Regras Semânticas Validadas

O `SemanticAnalyzer` impõe as seguintes restrições lógicas e validações estáticas:

### Validação de Declarações
*   **Declarações Duplicadas (`visit_DeclarationNode`):** Impede a declaração de variáveis com nomes idênticos no mesmo escopo. Se o identificador já constar na tabela de símbolos, levanta um erro:
    ```python
    raise SemanticError(f"Variável '{identifier}' já declarada")
    ```
*   **Variáveis não Declaradas:** Garante que qualquer uso de variável (atribuições, leitura do teclado `pembejeo`, referências em expressões) seja validado contra a tabela de símbolos. Se não encontrada, levanta uma exceção (ex: `Variável não declarada: x`).

### Validação e Coerção em Atribuições (`visit_AssignmentNode`)
O método `can_assign(target_type, expression_type)` avalia a compatibilidade de tipo:
1.  **Mesmo Tipo:** Permitido (ex: `int := int`).
2.  **Promoção Implícita (Coerção):** É permitido atribuir um valor `int` a uma variável `float` (coerção implícita para decimal).
3.  **Incompatibilidade:** Qualquer outra atribuição (como `string` para `int`, ou `float` para `int` diretamente) levanta um erro semântico de tipo incompatível.

### Verificação de Tipos de Controle
*   **Estruturas de Decisão e Loops (`IfNode`/`ElifNode`/`WhileNode`):** O validador avalia o tipo da expressão de condição. Ela deve obrigatoriamente ser avaliada como um booleano (`'bool'`). Qualquer outro tipo (ex: `int`) levanta um erro.
*   **Limites de Iteração (`ForNode`):** Valida se as expressões que definem o ponto de partida (`start_expr`) e de parada (`end_expr`) do loop são resolvidas estritamente como números inteiros (`'int'`).

### Escopo Temporário de Iteração (`visit_ForNode`)
Para o laço `kwa i := 0, 5.`:
*   O analisador insere temporariamente o identificador da variável iteradora (`i`) na tabela de símbolos como `'int'` durante a análise interna do bloco de comandos do laço.
*   Caso a variável não estivesse previamente declarada no escopo global antes do laço, ela é descartada (`pop`) da tabela de símbolos ao fim da execução da verificação do bloco `kwa`, prevenindo o vazamento de escopo.

### Verificação de Expressões Matemáticas e Lógicas (`visit_BinaryOpNode`)
*   **Operações Matemáticas (`+`, `-`, `*`, `/`):** Permite se ambos os lados forem numéricos (`int` ou `float`). Se ao menos um operando for `float`, o tipo resultante da expressão é promovido para `float`.
*   **Concatenação de Strings:** Permite o operador de soma (`+`) se e somente se ambos os operandos forem `'string'`. O tipo retornado é `'string'`.
*   **Operações Lógicas e Relacionais (`<`, `>`, `==`):** Valida se os dois lados da expressão relacional possuem tipos correspondentes. O tipo resultante de retorno da validação é `'bool'`.
