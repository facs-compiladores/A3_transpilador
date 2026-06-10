import sys
import os
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
  tokens = lexer.tokenize(code)
  program = Parser(tokens).parse_program()
  if show_ast:
      print_ast(program)
  output = transpiler.transpile(code)
except Exception as e:
  print(f"Erro ao transpilar arquivo fonte swhthon: {e}. Encerrando transpilador")
  sys.exit(1)

try:
  output_dir = "output"
  os.makedirs(output_dir, exist_ok=True)
  output_file_name = os.path.splitext(os.path.basename(file_path))[0] + ".py"
  output_path = os.path.join(output_dir, output_file_name)
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(output)
except Exception as e:
  print(f"Erro ao gerar arquivo de saída em python: {e}. Encerrando transpilador")
  sys.exit(1)

print("[!] O código foi transpilado com sucesso! ")
print(f"[>] O arquivo '{output_path}' foi gerado. ")