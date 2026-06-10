from dataclasses import dataclass

class SemanticError(Exception):
    pass

@dataclass
class Symbol:
    name: str
    type: str

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}

    def analyze(self, program):
        self.symbols = {}

        for statement in program.statements:
            self.visit(statement)

        return self.symbols

    def visit(self, node):
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise SemanticError(f"No semantic visitor for node type {node.__class__.__name__}")

    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_DeclarationNode(self, node):
        for identifier in node.identifiers:
            if identifier in self.symbols:
                raise SemanticError(f"Variável '{identifier}' já declarada")
            self.symbols[identifier] = node.type

        if node.initializers:
            initializer_type = self.visit(node.initializers[0])
            if not self.can_assign(node.type, initializer_type):
                raise SemanticError(
                    f"Tipo incompatível na declaração: '{node.identifiers[0]}' é {node.type} e inicialização é {initializer_type}"
                )

    def visit_PrintNode(self, node):
        self.visit(node.expression)

    def visit_InputNode(self, node):
        if node.identifier not in self.symbols:
            raise SemanticError(f"Variável não declarada para input: {node.identifier}")

    def visit_AssignmentNode(self, node):
        if node.identifier not in self.symbols:
            raise SemanticError(f"Variável não declarada em atribuição : {node.identifier}")

        expression_type = self.visit(node.expression)
        target_type = self.symbols[node.identifier]

        if not self.can_assign(target_type, expression_type):
            raise SemanticError(
                f"Tipo incompatível na atribuição: '{node.identifier}' é {target_type} e expressão é {expression_type}"
            )

    def visit_IfNode(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != 'bool':
            raise SemanticError(f"Condição if deve ser bool, não {condition_type}")

        for statement in node.then_branch:
            self.visit(statement)

        for elif_node in node.elif_branches:
            self.visit(elif_node)

        if node.else_branch is not None:
            for statement in node.else_branch:
                self.visit(statement)

    def visit_ElifNode(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != 'bool':
            raise SemanticError(f"Condição elif deve ser bool, não {condition_type}")
        for statement in node.body:
            self.visit(statement)

    def visit_WhileNode(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != 'bool':
            raise SemanticError(f"Condição while deve ser bool, não {condition_type}")
        for statement in node.body:
            self.visit(statement)

    def visit_ForNode(self, node):
        start_type = self.visit(node.start_expr)
        end_type = self.visit(node.end_expr)

        if start_type != 'int':
            raise SemanticError(f"Limite inicial do for deve ser int, não {start_type}" )
        if end_type != 'int':
            raise SemanticError(f"Limite final do for deve ser int, não {end_type}" )

        original_type = self.symbols.get(node.identifier)
        self.symbols[node.identifier] = 'int'

        for statement in node.body:
            self.visit(statement)

        if original_type:
            self.symbols[node.identifier] = original_type
        else:
            self.symbols.pop(node.identifier, None)
            
    def visit_VariableReferenceNode(self, node):
        if node.name not in self.symbols:
            raise SemanticError(f"Variável não declarada: {node.name}")
        return self.symbols[node.name]

    def visit_LiteralNode(self, node):
        return node.type

    def visit_BinaryOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.operator

        if op in ['+', '-', '*', '/']:
            if left_type in ['int', 'float'] and right_type in ['int', 'float']:
                return 'float' if left_type == 'float' or right_type == 'float' else 'int'
            if op == '+' and left_type == 'string' and right_type == 'string':
                return 'string'
            raise SemanticError(
                f"Operador aritmético '{op}' não suportado para tipos {left_type} e {right_type}"
            )

        if op in ['<', '>', '==']:
            if left_type != right_type:
                raise SemanticError(
                    f"Operador relacional '{op}' não suporta tipos diferentes: {left_type} e {right_type}"
                )
            return 'bool'

        raise SemanticError(f"Operador desconhecido na expressão: {op}")

    @staticmethod
    def can_assign(target_type, expression_type):
        if target_type == expression_type:
            return True
        if target_type == 'float' and expression_type == 'int':
            return True
        return False
