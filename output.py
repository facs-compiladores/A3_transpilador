a = 0
b = 0
total = 0
aprovado = False
maior = False
print("===# PROGRAMA DE SOMA #===")
print("Digite A")
a = int(input())
print("Digite B")
b = int(input())
total = (a + b)
aprovado = True
maior = (a > b)
print("Resultado:")
print(total)
print("Status:")
if aprovado:
    print("Aprovado")
else:
    print("Reprovado")
    print("Maior número:")
    if maior:
        print("A é maior")
    else:
        print("B é maior")