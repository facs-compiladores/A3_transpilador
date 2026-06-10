from parser import Parser
from semantic import SemanticAnalyzer

class Transpiler:

    def __init__(self, lexer=None):
        self.lexer = lexer
        self.symbols = {}

    def transpile(self, code):
        try:
            tokens = self.lexer.tokenize(code)
        except Exception as e:
            raise Exception(f"Erro durante a tokenização: {str(e)}")

        parser = Parser(tokens)
        program = parser.parse_program()

        semantic = SemanticAnalyzer()
        self.symbols = semantic.analyze(program)

        output_lines = []
        for statement in program.statements:
            output_lines.extend(self.transpile_statement(statement))

        return "\n".join(output_lines)

    def transpile_statement(self, statement):
        node_type = statement.__class__.__name__
        if node_type == 'DeclarationNode':
            return [self.transpile_declaration(statement)]
        if node_type == 'PrintNode':
            return [self.transpile_print(statement)]
        if node_type == 'InputNode':
            return [self.transpile_input(statement)]
        if node_type == 'AssignmentNode':
            return [self.transpile_assignment(statement)]
        if node_type == 'IfNode':
            return self.transpile_if(statement)
        if node_type == 'WhileNode':
            return self.transpile_while(statement)
        if node_type == 'ForNode':
            return self.transpile_for(statement)
        raise Exception(f"Tipo de nó desconhecido ao transpilar: {node_type}")

    def transpile_declaration(self, node):
        lines = []
        initial = {'int': '0', 'float': '0.0', 'string': '""', 'bool': 'False'}
        for identifier in node.identifiers:
            default_value = initial.get(node.type, 'None')
            if node.initializers:
                default_value = self.transpile_expression(node.initializers[0])
            lines.append(f"{identifier} = {default_value}")
        return "\n".join(lines)

    def transpile_print(self, node):
        return f"print({self.transpile_expression(node.expression)})"

    def transpile_input(self, node):
        var_type = self.symbols.get(node.identifier)
        if var_type == 'int':
            return f"{node.identifier} = int(input())"
        if var_type == 'float':
            return f"{node.identifier} = float(input())"
        return f"{node.identifier} = input()"

    def transpile_assignment(self, node):
        expression = self.transpile_expression(node.expression)
        return f"{node.identifier} = {expression}"

    def transpile_if(self, node):
        lines = []
        lines.append(f"if {self.transpile_expression(node.condition)}:")
        for statement in node.then_branch:
            for child_line in self.transpile_statement(statement):
                lines.append(f"    {child_line}")

        for elif_node in node.elif_branches:
            lines.append(f"elif {self.transpile_expression(elif_node.condition)}:")
            for statement in elif_node.body:
                for child_line in self.transpile_statement(statement):
                    lines.append(f"    {child_line}")

        if node.else_branch is not None:
            lines.append("else:")
            for statement in node.else_branch:
                for child_line in self.transpile_statement(statement):
                    lines.append(f"    {child_line}")

        return lines

    def transpile_while(self, node):
        lines = []
        lines.append(f"while {self.transpile_expression(node.condition)}:")
        for statement in node.body:
            for child_line in self.transpile_statement(statement):
                lines.append(f"    {child_line}")
        return lines
    
    def transpile_for(self, node):
        lines = []
        start = self.transpile_expression(node.start_expr)
        end = self.transpile_expression(node.end_expr)
        lines.append(f"for {node.identifier} in range({start}, {end}):")
        for statement in node.body:
            for child_line in self.transpile_statement(statement):
                lines.append(f"    {child_line}")          
        return lines
    

    def transpile_expression(self, expr):
        class_name = expr.__class__.__name__
        if class_name == 'LiteralNode':
            return expr.value
        if class_name == 'VariableReferenceNode':
            return expr.name
        if class_name == 'BinaryOpNode':
            left = self.transpile_expression(expr.left)
            right = self.transpile_expression(expr.right)
            return f"({left} {expr.operator} {right})"
        raise Exception(f"Expressão desconhecida ao transpilar: {class_name}")
