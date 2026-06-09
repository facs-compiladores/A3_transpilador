import sys
from lexer import Lexer
from parser import Parser, print_ast
from transpiler import Transpiler

lexer = Lexer()
transpiler = Transpiler(lexer)

if len(sys.argv) < 2:
    print("Um programa fonte de entrada deve ser inserido. Encerrando transpilador")
    sys.exit(1)

file_path = sys.argv[1]
show_ast = '--print-ast' in sys.argv[2:]

try:
  with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()
except:
  print("Erro ao abrir arquivo de entrada. Encerrando transpilador")
  sys.exit(1)

try:
  if show_ast:
      tokens = lexer.tokenize(code)
      program = Parser(tokens).parse_program()
      print_ast(program)
  output = transpiler.transpile(code)
except Exception as e:
  print(f"Erro ao transpilar arquivo fonte swhthon: {e}. Encerrando transpilador")
  sys.exit(1)

try:
  with open("output.py", "w", encoding="utf-8") as f:
      f.write(output)
except:
  print("Erro ao gerar arquivo de saída em python. Encerrando transpilador")
  sys.exit(1)

print("[!] O código foi transpilado com sucesso! ")
print("[>] O arquivo 'output.py' foi gerado nesta pasta. ")