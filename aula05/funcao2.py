# Exemplo 2 - Função

# Usando função para calcular média.

def calcular_media(lista_de_numeros):
    """"
    Esta função recebe uma lista de números, calcula a média
    e retorna o resultado.
    """

    #  A função 'sum()' é uma função embutida do Python que soma
    #  os itens de uma lista
    total = sum(lista_de_numeros)

    # A função 'len() é outra função embutida que retorna o número
    # de itens em uma lista.
    quantidade = len(lista_de_numeros)

    # Evita divisão por zero se a lista estiver vazia
    if quantidade == 0:
        return 0

    media = total / quantidade
    return media

# --- Como usar a função ---

# Criamos uma lista de notas.
notas_aluno1 = [8.5, 7.0, 9.0, 10.0]

# Passamos a lista para a nossa função:
media_aluno1 = calcular_media(notas_aluno1)

print(f"A média do aluno 1 é: {media_aluno1}")
