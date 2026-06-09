# Transpilador Swhthon → Python

Este projeto consiste em um transpilador da linguagem **Swhthon** para **Python**. A linguagem Swhthon baseia seus termos e sintaxe na língua Swahili.

---

## Sumário
1. [Como Executar](#como-executar)
2. [Estrutura Básica do Programa](#estrutura-básica-do-programa)
3. [Tipos de Variáveis](#tipos-de-variáveis)
4. [Booleans](#booleans)
5. [Entrada e Saída de Dados](#entrada-e-saída-de-dados)
6. [Atribuição de Valores](#atribuição-de-valores)
7. [Operações Matemáticas e Comparação](#operações-matemáticas-e-comparação)
8. [Estrutura Condicional (Ternário)](#estrutura-condicional-ternário)
9. [Regras Importantes](#regras-importantes)
10. [Mapa Comparativo com Python](#mapa-comparativo-com-python)

---

## Como Executar

Para rodar o transpilador e executar o código gerado, siga as instruções abaixo:

1. **Transpilar o arquivo `.swhthon`:**
   Execute o script principal passando o arquivo fonte como argumento:
   ```bash
   python main.py input.swhthon
   ```
   *(Substitua `input.swhthon` pelo caminho do seu arquivo).*

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
> Isso irá solicitar a entrada do usuário e convertê-la automaticamente ao tipo declarado da variável `a`.

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

## Estrutura Condicional (Ternário)

Swhthon suporta o uso de ternários inline para tomada de decisão e concatenação em expressões:

```swhthon
chapa("Aprovado" if aprovado else "Reprovado").
```

---

## Regras Importantes

> - **Fim de comando:** Cada instrução/linha de comando deve obrigatoriamente terminar com `.` (ponto final), equivalente ao uso de `;` (ponto e vírgula) em linguagens como Java ou C.
> - **Declaração obrigatória:** Toda variável precisa ser declarada com seu respectivo tipo antes de ser utilizada.
> - **Aspas de Texto:** Valores do tipo String/texto devem ser delimitados estritamente por aspas duplas (`" "`).

---

## Mapa Comparativo com Python

A tabela abaixo resume a correspondência direta de palavras-chave e conceitos entre a linguagem **Swhthon** e o **Python**:

| Conceito | Swhthon | Python |
| :--- | :--- | :--- |
| **Início do programa** | `programu` | *(não existe)* |
| **Fim do programa** | `mwisho` | *(não existe)* |
| **Tipo inteiro** | `nambari` | `int` |
| **Tipo decimal** | `kuelea` | `float` |
| **Tipo string** | `kamba` | `str` |
| **Boolean verdadeiro** | `kweli` | `True` |
| **Boolean falso** | `uongo` | `False` |
| **If** | `ikiwa` | `if` |
| **Else** | `mwingine` | `else` |
| **While** | `wakati` | `while` |
| **For** | `kwa` | `for` |
| **Entrada de dados** | `pembejeo()` | `input()` |
| **Saída de dados** | `chapa()` | `print(x)` |
| **Atribuição** | `:=` | `=` |
| **Número** | número (regex) | `int` / `float` |
| **Texto** | `"..."` | `"..."` ou `'...'` |
| **Fim de comando** | `. (ponto)` | `;` (opcional) |