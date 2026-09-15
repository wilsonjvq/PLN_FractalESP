from pln.normalizador import (
    normalizar_texto
)

from pln.extractor import (
    extraer_representacion
)

from pln.traductor import (
    traducir_fractalesp
)


pruebas = [

    "Dibuja un copo azul con 5 repeticiones",

    "Quiero generar un triángulo de Sierpinski rojo con 4 repeticiones",

    "Haz un conjunto de Cantor verde con 6 repeticiones",

    "Genera un helecho de Barnsley morado con 5 repeticiones",

    "Crea un copo naranja con 3 repeticiones y ángulo 20"
]


for texto in pruebas:

    print()
    print("=" * 70)

    print("ENTRADA:")
    print(texto)

    texto_normalizado = (
        normalizar_texto(
            texto
        )
    )

    print()
    print("NORMALIZADO:")
    print(texto_normalizado)

    representacion = (
        extraer_representacion(
            texto_normalizado
        )
    )

    print()
    print("REPRESENTACIÓN INTERMEDIA:")
    print(
        representacion.model_dump()
    )

    codigo = (
        traducir_fractalesp(
            representacion
        )
    )

    print()
    print("CÓDIGO FRACTALESP:")
    print(codigo)

    print()