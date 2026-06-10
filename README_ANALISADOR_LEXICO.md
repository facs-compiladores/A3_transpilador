# Analisador Léxico (Lexer)

O analisador léxico é a primeira etapa do compilador. Ele é responsável por ler o fluxo de caracteres do código fonte em **Swhthon** e agrupá-los em uma sequência de unidades significativas chamadas **Tokens**, eliminando elementos irrelevantes (como espaços em branco e quebras de linha).

O módulo léxico deste projeto é composto por dois arquivos principais:
1. [lexer_tokens.py](lexer_tokens.py)
2. [lexer.py](lexer.py)

---

## 1. Definições de Tokens e Palavras-chave (`lexer_tokens.py`)

Este arquivo centraliza a especificação léxica da linguagem por meio de expressões regulares (Regex) e um dicionário de mapeamento de palavras-chave.

### Expressões Regulares (`TOKEN_SPECS`)
As regras de tokens são definidas como uma lista de tuplas contendo o nome do token e seu padrão em regex:

*   `NUMBER`: `\d+(\.\d+)?` (Casa números inteiros como `10` ou decimais com ponto flutuante como `3.14`).
*   `TEXT`: `"[^"]*"` (Casa cadeias de caracteres delimitadas por aspas duplas, ex: `"Olá"`).
*   `ASSIGN`: `:=` (Operador de atribuição de valores).
*   `PLUS` / `MINUS` / `MULT` / `DIV`: Operadores aritméticos aritméticos (`+`, `-`, `*`, `/`).
*   `LT` / `GT` / `EQ`: Operadores relacionais (`<`, `>`, `==`).
*   `LPAREN` / `RPAREN`: Delimitadores de parâmetros de funções/expressões `(` e `)`.
*   `DOT`: O caractere `.` que serve para encerrar os comandos.
*   `COMMA`: O caractere `,` usado para separar variáveis em declarações e limites no laço `kwa`.
*   `SKIP`: Padrões de espaços em branco, tabulações e novas linhas `[ \t\n]+` que são descartados pelo lexer.
*   `ID`: Identificador genérico `[A-Za-z][A-Za-z0-9]*` para variáveis e palavras-chave.

### Dicionário de Palavras-chave (`KEYWORDS`)
Se um token casado pelo padrão `ID` constar no dicionário `KEYWORDS`, o tipo do token é promovido para a palavra-chave Swahili correspondente. Esse dicionário contém:
*   `programu` $\rightarrow$ `PROGRAM`
*   `mwisho` $\rightarrow$ `END`
*   `nambari` $\rightarrow$ `INT`
*   `kuelea` $\rightarrow$ `FLOAT`
*   `kamba` $\rightarrow$ `STRING`
*   `kweli` $\rightarrow$ `BOOLEAN_TRUE`
*   `uongo` $\rightarrow$ `BOOLEAN_FALSE`
*   `ikiwa` $\rightarrow$ `IF`
*   `sivyo` $\rightarrow$ `ELIF`
*   `mwingine` $\rightarrow$ `ELSE`
*   `wakati` $\rightarrow$ `WHILE`
*   `kwa` $\rightarrow$ `FOR`
*   `pembejeo` $\rightarrow$ `INPUT`
*   `chapa` $\rightarrow$ `PRINT`

---

## 2. A Classe Lexer (`lexer.py`)

A classe `Lexer` implementa a máquina de estados que consome o código-fonte de entrada.

### Inicialização
O construtor da classe compila previamente os padrões de expressões regulares de todos os tokens em objetos regex do Python, visando ganho de performance em tempo de execução:
```python
self.rules = [
    (name, re.compile(pattern))
    for name, pattern in self.token_specs
]
```

### O Algoritmo de Tokenização (`tokenize`)
O método recebe o código fonte em string e itera enquanto houver caracteres a serem processados:

1.  **Correspondência de Padrão:** O lexer varre a lista de regras ordenadas e tenta casar o padrão regex contra a extremidade atual do código usando `regex.match()`.
2.  **Identificadores vs. Palavras-Chave:** Se o lexer encontra um identificador (`ID`), ele verifica se o texto faz parte do dicionário de palavras-chave da linguagem (`KEYWORDS`). Se sim, o tipo do token é redefinido.
3.  **Descarte de Espaços:** Se o padrão casado for da categoria `SKIP` (espaços, quebras de linha), o trecho de código é recortado, mas nenhum token é inserido na lista resultante.
4.  **Consumo de Caracteres:** Caso um token válido seja identificado, ele é adicionado à lista de saída como uma tupla `(tipo_do_token, texto_casado)`. O trecho correspondente é removido do código de entrada e a busca reinicia do novo ponto de partida.
5.  **Erro Léxico:** Se nenhum padrão regex de token for casado com os caracteres na posição atual do fluxo de código, o analisador léxico interrompe a execução e lança um erro detalhado indicando o caractere inesperado:
    ```python
    raise Exception("Token inválido: " + code[0])
    ```
