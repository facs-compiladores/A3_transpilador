import re

TOKENS = [
    # Palavras reservadas
    ('PROGRAM', r'programu'),
    ('END', r'mwisho'),
    ('INT', r'nambari'),
    ('FLOAT', r'kuelea'),
    ('STRING', r'kamba'),
    # ('BOOLEAN', r'kweliuongo'), 
    ('BOOLEAN_TRUE', r'kweli'),
    ('BOOLEAN_FALSE', r'uongo'),
    ('IF', r'ikiwa'),
    ('ELSE', r'mwingine'),
    ('WHILE', r'wakati'),
    ('FOR', r'kwa'),
    ('INPUT', r'pembejeo'),
    ('PRINT', r'chapa'),

    ('ASSIGN', r':='),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('ID', r'[a-zA-Z][a-zA-Z0-9]*'),
    ('TEXT', r'"[^"]*"'),

    # Operações básicas
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULT', r'\*'),
    ('DIV', r'/'),

    # Maior que, menor que, igual a...
    ('LT', r'<'), 
    ('GT', r'>'),
    ('EQ', r'=='),

    # Simbolos matemáticos
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LBRACK', r'\['),
    ('RBRACK', r'\]'),

    # . | , e ;
    ('DOT', r'\.'),
    ('COMMA', r','),
    ('SEMIC', r';'),

    # Para ignorar os caracteres não-importantes
    ('SKIP', r'[ \t\n]+'),
]

def tokenize(code):
    tokens = []

    while code:
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code)

            if match:
                text = match.group(0)

                if token_type != 'SKIP':
                    tokens.append((token_type, text))

                code = code[len(text):]
                break

        if not match:
            raise SyntaxError("Token é incorreto")

    return tokens

# https://www.dabeaz.com/ply/
