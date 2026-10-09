while True:
  try:
        numero = int(input("Digite um número para ver a tabuada do mesmo: "))
        break
  except ValueError:
    print("Por favor, digite apenas números inteiros.\n")


print("")
  
contador = 1
while contador <= 10:
    print(f"{numero} x {contador} = {numero * contador}")
    print("")
    contador += 1
