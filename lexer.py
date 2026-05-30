import re
from lexer_tokens import TOKENS

class Lexer:

  def __init__(self, tokens_list=None):
    self.tokens_list = tokens_list or TOKENS

  def tokenize(self, code):
      generated_tokens = []

      while code:
          match = None
          for token_type, pattern in self.tokens_list:
              regex = re.compile(pattern)
              match = regex.match(code)

              if match:
                  text = match.group(0)

                  if token_type != 'SKIP':
                      generated_tokens.append((token_type, text))

                  code = code[len(text):]
                  break

          if not match:
              raise SyntaxError("Token é incorreto")

      if not generated_tokens:
          raise Exception("Nenhum token foi gerado pelo lexer")
      
      return generated_tokens

