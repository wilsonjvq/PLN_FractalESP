from pln.normalizador import normalizar_texto


pruebas = [
    "  QUIERO HACER UN TRIÁNGULO AZUL  ",
    "Genera un CÓPO de Koch",
    "   quiero   un   helecho   verde   ",
    "Conjunto de CANTOR"
]


for texto in pruebas:

    resultado = normalizar_texto(
        texto
    )

    print("Original:")
    print(texto)

    print("Normalizado:")
    print(resultado)

    print("-" * 60)