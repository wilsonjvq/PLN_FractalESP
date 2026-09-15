def traducir_fractalesp(
    representacion,
    nombre="MiFractal"
):

    forma = representacion.forma

    repeticiones = (
        representacion.repeticiones
    )

    angulo = (
        representacion.angulo
    )

    color = (
        representacion.color
    )

    if repeticiones is None:
        repeticiones = 1

    if angulo is None:
        angulo = 0

    if color is None:
        color = "azul"

    codigo = f'''fractal "{nombre}" {{
    forma: {forma}
    repeticiones: {repeticiones}
    angulo: {angulo}
    color: "{color}"
}}'''

    return codigo