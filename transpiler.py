class Transpiler:

  def __init__(self, lexer=None):
      self.lexer = lexer

  def transpile(self, code):
      try:
        tokens = self.lexer.tokenize(code)
      except Exception as e:
        raise Exception(f"Erro durante a tokenização: {str(e)}")
      
      output = []
      variables = {}
      i = 0

      def format_expr(expr_tokens):
          out = ""
          for t, v in expr_tokens:

              # booleans
              if t == 'BOOLEAN_TRUE':
                  v = "True"
              elif t == 'BOOLEAN_FALSE':
                  v = "False"

              # operadores com espaço obrig
              if v in ["+", "-", "*", "/", ">", "<", "==", "if", "else"]:
                  out += f" {v} "
              else:
                  if out and not out.endswith(" "):
                      out += " "
                  out += v

          return " ".join(out.split())

      while i < len(tokens):
          token, value = tokens[i]

          # =====================
          # INT
          # =====================
          if token == 'INT':
              i += 1

              while i < len(tokens) and tokens[i][0] != 'DOT':
                  if tokens[i][0] == 'ID':
                      var = tokens[i][1]
                      variables[var] = 'int'
                      output.append(f"{var} = 0")
                  i += 1
              i += 1

              continue

          # =====================
          # FLOAT
          # =====================
          elif token == 'FLOAT':
              i += 1
              while i < len(tokens) and tokens[i][0] != 'DOT':
                  if tokens[i][0] == 'ID':
                      var = tokens[i][1]
                      variables[var] = 'float'
                      output.append(f"{var} = 0.0")
                  i += 1
              i += 1
              continue

          # ====================
          # PRINT
          # =====================
          elif token == 'PRINT':
              j = i + 2
              expr = []
              while j < len(tokens) and tokens[j][0] != 'RPAREN':
                  expr.append(tokens[j])
                  j += 1
              output.append(f"print({format_expr(expr)})")
              i = j + 2

              continue

          # =====================
          # INPUT
          # =====================
          elif token == 'INPUT':
              j = i + 2
              var = tokens[j][1]
              if var not in variables:
                  raise Exception(f"Variável não declarada: {var}")

              if variables[var] == 'int':
                  output.append(f"{var} = int(input())")
              elif variables[var] == 'float':
                  output.append(f"{var} = float(input())")
              else:
                  output.append(f"{var} = input()")

              i = j + 2

              continue

          # =====================
          # ASSIGN
          # =====================
          elif token == 'ASSIGN':
              var = tokens[i - 1][1]
              j = i + 1
              expr = []
              while j < len(tokens) and tokens[j][0] != 'DOT':
                  t, v = tokens[j]
                  expr.append((t, v))
                  j += 1

              output.append(f"{var} = {format_expr(expr)}")
              i = j + 1

              continue

          # =====================
          # BOOL
          # ====================
          elif token in ['BOOLEAN_TRUE', 'BOOLEAN_FALSE']:
              i += 1
              continue

          i += 1

      return "\n".join(output)