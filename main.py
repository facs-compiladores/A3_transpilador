from lexer import Lexer
from transpiler import Transpiler
lexer = Lexer()
transpiler = Transpiler(lexer)

with open("input.swhthon", "r", encoding="utf-8") as f:
    code = f.read()

output = transpiler.transpile(code)

with open("output.py", "w", encoding="utf-8") as f:
    f.write(output)

print("[!] O código foi transpilado com sucesso! ")
print("[>] O arquivo 'output.py' foi gerado nesta pasta. ")