from lexer import tokenize

# Aqui ainda falta adicionar algumas coisas que estão no transpiler mas não aqui

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.variables = {}

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current()

        if token and token[0] == token_type:
            self.pos += 1
            return token

        raise SyntaxError(f"Esperado {token_type}")

    def parse_program(self):

        self.eat('PROGRAM')

        while self.current()[0] in ['INT','FLOAT','STRING','BOOLEAN']:
            self.parse_declaration()

        while self.current()[0] != 'END':
            self.parse_command()

        self.eat('END')

    def parse_declaration(self):

        type_token = self.eat(self.current()[0])

        var = self.eat('ID')
        self.variables[var[1]] = type_token[0]

        while self.current()[0] == 'COMMA':
            self.eat('COMMA')
            var = self.eat('ID')
            self.variables[var[1]] = type_token[0]

        self.eat('DOT')

    def parse_command(self):

        token = self.current()[0]

        if token == 'PRINT':
            self.parse_print()

        elif token == 'INPUT':
            self.parse_input()

        elif token == 'ID':
            self.parse_assign()

    def parse_print(self):

        self.eat('PRINT')
        self.eat('LPAREN')

        if self.current()[0] == 'TEXT':
            self.eat('TEXT')
        else:
            var = self.eat('ID')

            if var[1] not in self.variables:
                raise Exception("Variável não declarada")

        self.eat('RPAREN')
        self.eat('DOT')

    def parse_input(self):

        self.eat('INPUT')
        self.eat('LPAREN')

        var = self.eat('ID')

        if var[1] not in self.variables:
            raise Exception("Variável não declarada")

        self.eat('RPAREN')
        self.eat('DOT')

    def parse_assign(self):

        var = self.eat('ID')

        if var[1] not in self.variables:
            raise Exception("Variável não declarada")

        self.eat('ASSIGN')
        self.eat('NUMBER')
        self.eat('DOT')