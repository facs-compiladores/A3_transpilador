from transpiler import transpile
import sys

try:
  file_path = sys.argv[1]
except:
  print("Um programa fonte de entrada deve ser inserido. Encerrando transpilador")
  sys.exit(1)

try:
  with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()
except:
  print("Erro ao abrir arquivo de entrada. Encerrando transpilador")
  sys.exit(1)

try:
  output = transpile(code)
except:
  print("Erro ao transpilar arquivo fonte swhthon. Encerrando transpilador")
  sys.exit(1)

try:
  with open("output.py", "w", encoding="utf-8") as f:
      f.write(output)
except:
  print("Erro ao gerar arquivo de saída em python. Encerrando transpilador")
  sys.exit(1)

print("[!] O código foi transpilado com sucesso! ")
print("[>] O arquivo 'output.py' foi gerado nesta pasta. ")