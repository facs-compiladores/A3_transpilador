# Transpilador Swhthon → Python

Este projeto consiste em um transpilador da linguagem de programação fictícia **Swhthon** para **Python**. A linguagem Swhthon baseia seus termos e sintaxe na língua africana **Swahili**.

## Equipe

- nome
- nome
- nome
- nome
- nome

---

## Sumário
1. [Como Executar](#como-executar)
2. [Estrutura Básica do Programa](#estrutura-básica-do-programa)
3. [Tipos de Variáveis](#tipos-de-variáveis)
4. [Booleans](#booleans)
5. [Entrada e Saída de Dados](#entrada-e-saída-de-dados)
6. [Atribuição de Valores](#atribuição-de-valores)
7. [Operações Matemáticas e Comparação](#operações-matemáticas-e-comparação)
8. [Estruturas Condicionais (Blocos)](#estruturas-condicionais-blocos)
9. [Estrutura Condicional (Ternário Inline)](#estrutura-condicional-ternário-inline)
10. [Análise Semântica e Verificação de Tipos](#análise-semântica-e-verificação-de-tipos)
11. [Regras Importantes](#regras-importantes)
12. [Mapa Comparativo com Python](#mapa-comparativo-com-python)

---

## Como Executar

Para rodar o transpilador e executar o código gerado, siga as instruções abaixo:

1. **Transpilar o arquivo `.swhthon`:**
   Execute o script principal passando o arquivo fonte como argumento:
   ```bash
   python main.py input.swhthon
   ```
   *(Substitua `input.swhthon` pelo caminho do seu arquivo).*

   Para visualizar a **Árvore de Sintaxe Abstrata (AST)** gerada pelo parser durante a transpilação, adicione a flag `--print-ast`:
   > ```bash
   > python main.py input.swhthon --print-ast
   > ```

2. **Executar o arquivo Python gerado:**
   O transpilador gerará um arquivo chamado `output.py` na raiz do projeto. Execute-o com:
   ```bash
   python output.py
   ```

---

## Estrutura Básica do Programa

Todo programa escrito em Swhthon deve iniciar com a palavra-chave de início e encerrar com a palavra-chave de término seguida de ponto final:

```swhthon
programu

# O código do seu programa vai aqui...

mwisho.
```

---

## Tipos de Variáveis

A linguagem suporta 3 tipos principais de dados, declarados conforme os exemplos a seguir:

1. **Inteiro (Int)**
   ```swhthon
   nambari x.
   ```
2. **Decimal (Float)**
   ```swhthon
   kuelea y.
   ```
3. **String (Texto)**
   ```swhthon
   kamba nome.
   ```

---

## Booleans

Os booleanos são representados por:
*   `kweli` → Equivalente a `True` em Python
*   `uongo` → Equivalente a `False` em Python

### Exemplo de uso:
```swhthon
kweli aprovado.
uongo ativo.
```

---

## Entrada e Saída de Dados

### Saída de dados (PRINT)
Para imprimir dados na tela, utiliza-se a palavra-chave `chapa`:
```swhthon
chapa("Olá mundo").
```
> O código acima é o equivalente direto a `print('Olá mundo')` em Python.

### Entrada de dados (INPUT)
Para capturar a entrada do usuário e armazenar em uma variável já declarada, utiliza-se `pembejeo`:
```swhthon
pembejeo(a).
```
> Isso irá solicitar a entrada do usuário e convertê-la automaticamente ao tipo de dados da variável correspondente (com cast de tipo automático para `int` ou `float`).

---

## Atribuição de Valores

A atribuição em Swhthon é feita utilizando o operador composto `:=` (dois pontos e igual).

```swhthon
a := 10.         # (Equivalente a: a = 10 em Python)
b := a + 5.      # (Equivalente a: b = a + 5 em Python)
```

---

## Operações Matemáticas e Comparação

A linguagem suporta os seguintes operadores padrão:
*   `+` : Soma
*   `-` : Subtração
*   `*` : Multiplicação
*   `/` : Divisão
*   `>` : Maior que
*   `<` : Menor que

### Exemplos:
```swhthon
total := a + b.
maior := a > b.
```

---

## Estruturas Condicionais (Blocos)

A linguagem suporta estruturas condicionais estruturadas completas com blocos de desvios utilizando as seguintes palavras-chave:
*   `ikiwa <condição>.` $\rightarrow$ Início do bloco `if`
*   `sivyo <condição>.` $\rightarrow$ Bloco `elif` (Else If)
*   `mwingine.` $\rightarrow$ Bloco `else`

Cada cabeçalho de bloco condicional deve terminar obrigatoriamente com um ponto `.`:

```swhthon
ikiwa a > b.
chapa("A maior que B"). 
sivyo a < b.
chapa("B maior que A").
mwingine.
chapa("A igual a B").
```

> O transpiler aninha e indenta automaticamente os comandos que fazem parte de cada bloco condicional no arquivo final de saída Python.

---

## Estrutura Condicional (Ternário Inline)

A linguagem também permite o uso de ternários inline para tomada de decisão em expressões de atribuição ou concatenação, mas utilizando a sintaxe nativa do Python (`if` / `else`):

```swhthon
chapa("Aprovado" if aprovado else "Reprovado").
```

> O ternário inline não traduz as palavras-chave em Swahili (`ikiwa` / `mwingine`). Use-as apenas para condicionais em blocos estruturados.

---

## Análise Semântica e Verificação de Tipos

O compilador inclui um **Analisador Semântico** (`SemanticAnalyzer`) que realiza validações estáticas da AST para impedir a geração de código com falhas lógicas:
*   **Redeclaração de variáveis:** Erro caso uma variável seja declarada múltiplas vezes.
*   **Uso de variáveis não declaradas:** Erro caso uma variável não definida por `nambari`, `kuelea` ou `kamba` seja referenciada em atribuições, leituras (`pembejeo`) ou prints.
*   **Compatibilidade de atribuição:** Impede atribuições de tipos incompatíveis (ex: atribuir `string` a uma variável do tipo `int`). Conversões implícitas de `int` para `float` são permitidas.
*   **Condições booleanas obrigatórias:** Garante que as expressões nos cabeçalhos de `ikiwa` e `sivyo` resultem sempre em um valor do tipo `bool`.
*   **Operações válidas:** Valida operadores de expressões matemáticas e lógicas binárias conforme os tipos compatíveis envolvidos.

---

## Regras Importantes

> - **Fim de comando:** Cada instrução/linha de comando deve obrigatoriamente terminar com `.` (ponto final), equivalente ao uso de `;` (ponto e vírgula) em linguagens como Java ou C.
> - **Declaração obrigatória:** Toda variável precisa ser declarada com seu respectivo tipo antes de ser utilizada.
> - **Aspas de Texto:** Valores do tipo String/texto devem ser delimitados estritamente por aspas duplas (`" "`).

> **Palavras-chave sem suporte no Transpiler:**
> As palavras-chave `wakati` (while) e `kwa` (for) continuam apenas mapeadas no Lexer e **não são suportadas** nem implementadas na AST ou transpiler no momento.

---

## Mapa Comparativo com Python

A tabela abaixo resume a correspondência direta de palavras-chave e conceitos entre a linguagem **Swhthon** e o **Python**, indicando o estado atual de suporte:

| Conceito | Swhthon | Python | Estado de Suporte |
| :--- | :--- | :--- | :--- |
| **Início do programa** | `programu` | *(não existe)* | Ignorado pelo transpiler (não gera código) |
| **Fim do programa** | `mwisho` | *(não existe)* | Ignorado pelo transpiler (não gera código) |
| **Tipo inteiro** | `nambari` | `int` | **Suportado** (inicializa como `= 0`) |
| **Tipo decimal** | `kuelea` | `float` | **Suportado** (inicializa como `= 0.0`) |
| **Tipo string** | `kamba` | `str` | **Suportado** (inicializa como `= ""`) |
| **Boolean verdadeiro** | `kweli` | `True` | **Suportado** |
| **Boolean falso** | `uongo` | `False` | **Suportado** |
| **If** | `ikiwa` | `if` | **Suportado** (estruturado em blocos) |
| **Elif (Else If)** | `sivyo` | `elif` | **Suportado** (estruturado em blocos) |
| **Else** | `mwingine` | `else` | **Suportado** (estruturado em blocos) |
| **While** | `wakati` | `while` | *Não implementado no Transpiler* |
| **For** | `kwa` | `for` | *Não implementado no Transpiler* |
| **Entrada de dados** | `pembejeo()` | `input()` | **Suportado** (com cast automático de tipo) |
| **Saída de dados** | `chapa()` | `print(x)` | **Suportado** |
| **Atribuição** | `:=` | `=` | **Suportado** |
| **Número** | número (regex) | `int` / `float` | **Suportado** |
| **Texto** | `"..."` | `"..."` ou `'...'` | **Suportado** |
| **Fim de comando** | `. (ponto)` | `;` (opcional) | **Suportado** |