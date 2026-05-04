a = 0
b = 0
total = 0
print("===# PROGRAMA DE SOMA #===")
print("Digite A")
a = int(input())
print("Digite B")
b = int(input())
total = a + b
aprovado = True
maior = a > b
print("Resultado:")
print(total)
print("Status:")
print("Aprovado" if aprovado else "Reprovado")
print("Maior número:")
print("A é maior" if maior else "B é maior")