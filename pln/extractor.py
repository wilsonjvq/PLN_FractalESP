from pln.ollama import interpretar
from pln.validador import (
    validar_representacion
)


def extraer_representacion(texto):

    datos = interpretar(
        texto
    )

    representacion = (
        validar_representacion(
            datos
        )
    )

    return representacion