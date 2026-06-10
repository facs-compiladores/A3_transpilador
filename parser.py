from dataclasses import dataclass

@dataclass
class Node:
    pass

@dataclass
class ProgramNode(Node):
    statements: list

@dataclass
class DeclarationNode(Node):
    type: str
    identifiers: list
    initializers: list | None = None

@dataclass
class PrintNode(Node):
    expression: Node

@dataclass
class InputNode(Node):
    identifier: str

@dataclass
class AssignmentNode(Node):
    identifier: str
    expression: Node

@dataclass
class LiteralNode(Node):
    value: any
    type: str

@dataclass
class VariableReferenceNode(Node):
    name: str

@dataclass
class BinaryOpNode(Node):
    left: Node
    operator: str
    right: Node

@dataclass
class ElifNode(Node):
    condition: Node
    body: list

@dataclass
class IfNode(Node):
    condition: Node
    then_branch: list
    elif_branches: list
    else_branch: list | None

@dataclass
class WhileNode(Node):
    condition: Node
    body: list

@dataclass
class ForNode(Node):
    identifier: str
    start_expr: Node
    end_expr: Node
    body: list

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current()
        if token and token[0] == token_type:
            self.pos += 1
            return token
        raise SyntaxError(f"Esperado {token_type}, encontrado {token}")

    def parse_program(self):
        self.eat('PROGRAM')
        statements = []

        while self.current() and self.current()[0] != 'END':
            statements.append(self.parse_statement())

        self.eat('END')
        return ProgramNode(statements=statements)

    def parse_statement(self):
        token = self.current()
        if token is None:
            raise SyntaxError("Declaração ou comando inesperado no final do programa")

        if token[0] in ['INT', 'FLOAT', 'STRING', 'BOOLEAN_TRUE', 'BOOLEAN_FALSE']:
            return self.parse_declaration()

        return self.parse_command()

    def parse_declaration(self):
        type_token = self.eat(self.current()[0])
        declaration_type = 'bool' if type_token[0] in ['BOOLEAN_TRUE', 'BOOLEAN_FALSE'] else type_token[0].lower()
        identifiers = []

        first_var = self.eat('ID')
        identifiers.append(first_var[1])

        while self.current() and self.current()[0] == 'COMMA':
            self.eat('COMMA')
            next_var = self.eat('ID')
            identifiers.append(next_var[1])

        initializers = None
        if self.current() and self.current()[0] == 'ASSIGN':
            self.eat('ASSIGN')
            initializers = [self.parse_expression()]

        self.eat('DOT')
        return DeclarationNode(type=declaration_type, identifiers=identifiers, initializers=initializers)

    def parse_command(self):
        token = self.current()
        if token is None:
            raise SyntaxError("Comando inesperado no final do programa")

        if token[0] == 'PRINT':
            return self.parse_print()

        if token[0] == 'INPUT':
            return self.parse_input()

        if token[0] == 'IF':
            return self.parse_if()

        if token[0] == 'WHILE':
            return self.parse_while()

        if token[0] == 'ID':
            return self.parse_assign()
        
        if token[0] == 'FOR':
            return self.parse_for()

        raise SyntaxError(f"Comando inválido: {token}")

    def parse_print(self):
        self.eat('PRINT')
        self.eat('LPAREN')
        expression = self.parse_expression()
        self.eat('RPAREN')
        self.eat('DOT')
        return PrintNode(expression=expression)

    def parse_input(self):
        self.eat('INPUT')
        self.eat('LPAREN')
        var = self.eat('ID')
        self.eat('RPAREN')
        self.eat('DOT')
        return InputNode(identifier=var[1])

    def parse_assign(self):
        var = self.eat('ID')
        self.eat('ASSIGN')
        expression = self.parse_expression()
        self.eat('DOT')
        return AssignmentNode(identifier=var[1], expression=expression)

    def parse_if(self):
        self.eat('IF')
        condition = self.parse_expression()
        self.eat('DOT')
        then_branch = self.parse_block(stop_tokens=['ELIF', 'ELSE', 'END_IF'])

        elif_branches = []
        while self.current() and self.current()[0] == 'ELIF':
            self.eat('ELIF')
            elif_condition = self.parse_expression()
            self.eat('DOT')
            elif_body = self.parse_block(stop_tokens=['ELIF', 'ELSE', 'END_IF'])
            elif_branches.append(ElifNode(condition=elif_condition, body=elif_body))

        else_branch = None
        if self.current() and self.current()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('DOT')
            else_branch = self.parse_block(stop_tokens=['END_IF'])

        self.eat('END_IF')
        self.eat('DOT')

        return IfNode(
            condition=condition,
            then_branch=then_branch,
            elif_branches=elif_branches,
            else_branch=else_branch,
        )

    def parse_while(self):
        self.eat('WHILE')
        condition = self.parse_expression()
        self.eat('DOT')
        body = self.parse_block(stop_tokens=['END_WHILE'])
        self.eat('END_WHILE')
        self.eat('DOT')
        return WhileNode(condition=condition, body=body)
    
    def parse_for(self):
        self.eat('FOR')
        var = self.eat('ID')
        self.eat('ASSIGN')
        start_expr = self.parse_expression()
        self.eat('COMMA')                   
        end_expr = self.parse_expression()
        self.eat('DOT')
        
        body = self.parse_block(stop_tokens=['END_FOR'])
        
        self.eat('END_FOR')
        self.eat('DOT')
        
        return ForNode(
            identifier=var[1], 
            start_expr=start_expr, 
            end_expr=end_expr, 
            body=body
        )

    def parse_block(self, stop_tokens):
        statements = []
        while self.current() and self.current()[0] not in stop_tokens:
            statements.append(self.parse_command())
        return statements

    def parse_expression(self):
        return self.parse_relational()

    def parse_relational(self):
        node = self.parse_additive()
        while self.current() and self.current()[0] in ['LT', 'GT', 'EQ']:
            operator = self.eat(self.current()[0])[1]
            right = self.parse_additive()
            node = BinaryOpNode(left=node, operator=operator, right=right)
        return node

    def parse_additive(self):
        node = self.parse_term()
        while self.current() and self.current()[0] in ['PLUS', 'MINUS']:
            operator = self.eat(self.current()[0])[1]
            right = self.parse_term()
            node = BinaryOpNode(left=node, operator=operator, right=right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current() and self.current()[0] in ['MULT', 'DIV']:
            operator = self.eat(self.current()[0])[1]
            right = self.parse_factor()
            node = BinaryOpNode(left=node, operator=operator, right=right)
        return node

    def parse_factor(self):
        token = self.current()
        if token is None:
            raise SyntaxError("Expressão inesperada no final")

        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            literal_type = 'float' if '.' in token[1] else 'int'
            return LiteralNode(value=token[1], type=literal_type)

        if token[0] == 'TEXT':
            self.eat('TEXT')
            return LiteralNode(value=token[1], type='string')

        if token[0] == 'BOOLEAN_TRUE':
            self.eat('BOOLEAN_TRUE')
            return LiteralNode(value='True', type='bool')

        if token[0] == 'BOOLEAN_FALSE':
            self.eat('BOOLEAN_FALSE')
            return LiteralNode(value='False', type='bool')

        if token[0] == 'ID':
            self.eat('ID')
            return VariableReferenceNode(name=token[1])

        if token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()
            self.eat('RPAREN')
            return node

        raise SyntaxError(f"Fator inválido na expressão: {token}")


def print_ast(node, indent=0):
    prefix = '  ' * indent
    node_type = node.__class__.__name__

    if node_type == 'ProgramNode':
        print(prefix + 'Program')
        for statement in node.statements:
            print_ast(statement, indent + 1)
        return

    if node_type == 'DeclarationNode':
        print(prefix + f"Declaration(type={node.type}, ids={node.identifiers})")
        return

    if node_type == 'PrintNode':
        print(prefix + 'Print')
        print_ast(node.expression, indent + 1)
        return

    if node_type == 'InputNode':
        print(prefix + f"Input(identifier={node.identifier})")
        return

    if node_type == 'AssignmentNode':
        print(prefix + f"Assignment(identifier={node.identifier})")
        print_ast(node.expression, indent + 1)
        return

    if node_type == 'LiteralNode':
        print(prefix + f"Literal(type={node.type}, value={node.value})")
        return

    if node_type == 'VariableReferenceNode':
        print(prefix + f"VariableReference(name={node.name})")
        return

    if node_type == 'BinaryOpNode':
        print(prefix + f"BinaryOp(operator={node.operator})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
        return

    if node_type == 'ElifNode':
        print(prefix + 'Elif')
        print_ast(node.condition, indent + 1)
        for stmt in node.body:
            print_ast(stmt, indent + 1)
        return

    if node_type == 'IfNode':
        print(prefix + 'If')
        print_ast(node.condition, indent + 1)
        for stmt in node.then_branch:
            print_ast(stmt, indent + 1)
        for elif_node in node.elif_branches:
            print_ast(elif_node, indent + 1)
        if node.else_branch is not None:
            print(prefix + 'Else')
            for stmt in node.else_branch:
                print_ast(stmt, indent + 1)
        return

    if node_type == 'WhileNode':
        print(prefix + 'While')
        print_ast(node.condition, indent + 1)
        for stmt in node.body:
            print_ast(stmt, indent + 1)
        return

    if node_type == 'ForNode':
        print(prefix + f"For(var={node.identifier})")
        print_ast(node.start_expr, indent + 1)
        print_ast(node.end_expr, indent + 1)
        for stmt in node.body:
            print_ast(stmt, indent + 1)
        return

    print(prefix + f"UnknownNode(type={node_type})")
