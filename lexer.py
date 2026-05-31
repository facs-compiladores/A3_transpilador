import re
from lexer_tokens import TOKEN_SPECS, KEYWORDS

class Lexer:

  def __init__(self, token_specs=None, keywords=None):
      self.token_specs = token_specs or TOKEN_SPECS
      self.keywords = keywords or KEYWORDS
      self.rules = [
          (name, re.compile(pattern))
          for name, pattern in self.token_specs
      ]

  def tokenize(self, code):
      generated_tokens = []

      while code:
          match = None
          for token_type, regex in self.rules:
              match = regex.match(code)
              
              if not match:
                continue
              
              text = match.group(0)

              if token_type == 'ID' and text in self.keywords:
                    token_type = self.keywords[text]
              
              if token_type != 'SKIP':
                    generated_tokens.append((token_type, text))
              code = code[len(text):]
              break

          if not match:
              raise Exception("Token inválido: " + code[0])

      if not generated_tokens:
          raise Exception("Nenhum token foi gerado pelo lexer")
      
      return generated_tokens

