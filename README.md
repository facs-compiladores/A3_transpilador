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
9. [Estrutura de Repetição (Loop Wakati)](#estrutura-de-repetição-loop-wakati)
10. [Estrutura de Repetição (Loop Kwa)](#estrutura-de-repetição-loop-kwa)
11. [Análise Semântica e Verificação de Tipos](#análise-semântica-e-verificação-de-tipos)
12. [Regras Importantes](#regras-importantes)
13. [Mapa Comparativo com Python](#mapa-comparativo-com-python)

---

## Como Executar

Para rodar o transpilador e executar o código gerado, siga as instruções abaixo:

1. **Transpilar o arquivo `.swhthon`:**
   Execute o script principal passando o arquivo fonte como argumento:
   ```bash
   python main.py test_cases/teste.swhthon
   ```
   *(Substitua `test_cases/input.swhthon` pelo caminho do seu arquivo).*

   Para visualizar a **Árvore de Sintaxe Abstrata (AST)** gerada pelo parser durante a transpilação, adicione a flag `--print-ast`:
   > ```bash
   > python main.py test_cases/teste.swhthon --print-ast
   > ```

2. **Executar o arquivo Python gerado:**
   O transpilador gerará o arquivo correspondente com extensão `.py` dentro do diretório `output/`. Para executá-lo, utilize:
   ```bash
   python output/teste.py
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

A linguagem suporta 3 tipos principais de dados. Elas podem ser declaradas de forma simples ou inicializadas diretamente na declaração (inicialização inline):

1. **Inteiro (Int)**
   ```swhthon
   nambari x.
   nambari x := 10.
   ```
2. **Decimal (Float)**
   ```swhthon
   kuelea y.
   kuelea y := 3.14.
   ```
3. **String (Texto)**
   ```swhthon
   kamba nome.
   kamba nome := "Maria".
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
*   `+` : Soma (e concatenação de Strings)
*   `-` : Subtração
*   `*` : Multiplicação
*   `/` : Divisão
*   `>` : Maior que
*   `<` : Menor que

### Concatenação de Strings
O operador `+` também é suportado para concatenar duas Strings. O analisador semântico valida se ambos os operandos são do tipo string:
```swhthon
kamba message.
kamba name.
kamba output.

message := "Olá, ".
pembejeo(name).
output := message + name.
chapa(output).
```

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

## Estrutura de Repetição (Loop Wakati)

A linguagem suporta laços de repetição do tipo `while` utilizando a palavra-chave `wakati`. Assim como nas condicionais, a condição do loop deve terminar com um ponto `.`, e o bloco de comandos deve ser encerrado com `mwisho.`:

```swhthon
wakati x < 5.
  x := x + 1.
  chapa(x).
mwisho.
```

---

## Estrutura de Repetição (Loop Kwa)

A linguagem suporta laços de repetição do tipo `for` utilizando a palavra-chave `kwa`. A variável iteradora é inicializada com um valor inicial e incrementada até o limite final (exclusivo). A linha de definição deve terminar com um ponto `.`, e o bloco de comandos deve ser encerrado com `mwisho.`:

```swhthon
kwa i := 0, 5.
  chapa(i).
mwisho.
```

> O analisador semântico valida se os limites inicial e final são do tipo inteiro (`int`). A variável iteradora (`i`) é temporariamente tipada como `int` dentro do escopo do laço.

---

## Análise Semântica e Verificação de Tipos

O compilador inclui um **Analisador Semântico** (`SemanticAnalyzer`) que realiza validações estáticas da AST para impedir a geração de código com falhas lógicas:
*   **Redeclaração de variáveis:** Erro caso uma variável seja declarada múltiplas vezes.
*   **Uso de variáveis não declaradas:** Erro caso uma variável não definida por `nambari`, `kuelea` ou `kamba` seja referenciada em atribuições, leituras (`pembejeo`) ou prints.
*   **Compatibilidade de atribuição:** Impede atribuições de tipos incompatíveis (ex: atribuir `string` a uma variável do tipo `int`). Conversões implícitas de `int` para `float` são permitidas.
*   **Condições booleanas obrigatórias:** Garante que as expressões nos cabeçalhos de `ikiwa` (if), `sivyo` (elif) e `wakati` (while) resultem sempre em um valor do tipo `bool`.
*   **Operações válidas:** Valida operadores de expressões matemáticas e lógicas binárias conforme os tipos compatíveis envolvidos.

---

## Regras Importantes

> - **Fim de comando:** Cada instrução/linha de comando deve obrigatoriamente terminar com `.` (ponto final), equivalente ao uso de `;` (ponto e vírgula) em linguagens como Java ou C.
> - **Declaração obrigatória:** Toda variável precisa ser declarada com seu respectivo tipo antes de ser utilizada.
> - **Declarações Livres:** As variáveis não precisam ser declaradas exclusivamente no início do programa; você pode misturar declarações e comandos livremente ao longo do código.
> - **Inicialização Inline:** Variáveis podem opcionalmente ser declaradas e inicializadas em uma única instrução (ex: `nambari x := 10.`).
> - **Aspas de Texto:** Valores do tipo String/texto devem ser delimitados estritamente por aspas duplas (`" "`).

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
| **While** | `wakati` | `while` | **Suportado** (estruturado em blocos) |
| **For** | `kwa` | `for` | **Suportado** (estruturado em blocos) |
| **Entrada de dados** | `pembejeo()` | `input()` | **Suportado** (com cast automático de tipo) |
| **Saída de dados** | `chapa()` | `print(x)` | **Suportado** |
| **Atribuição** | `:=` | `=` | **Suportado** |
| **Número** | número (regex) | `int` / `float` | **Suportado** |
| **Texto** | `"..."` | `"..."` ou `'...'` | **Suportado** |
| **Fim de comando** | `. (ponto)` | `;` (opcional) | **Suportado** |