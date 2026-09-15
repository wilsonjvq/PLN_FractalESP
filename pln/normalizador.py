import re


def normalizar_texto(texto):

    if not isinstance(texto, str):
        raise TypeError(
            "El texto debe ser una cadena."
        )

    texto = texto.strip()

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto