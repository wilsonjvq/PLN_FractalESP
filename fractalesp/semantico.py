from .lexer import ErrorFractalEsp


FORMAS_VALIDAS = {
    "triangulo",
    "copo",
    "cantor",
    "helecho"
}


COLORES_VALIDOS = {
    "azul": "blue",
    "rojo": "red",
    "verde": "green",
    "negro": "black",
    "morado": "purple",
    "naranja": "orange",
    "cian": "cyan",
    "magenta": "magenta",
}


def analizar_semantico(ast):

    p = ast["propiedades"]

    # ======================================================
    # FORMA
    # ======================================================

    forma_info = p["forma"]

    forma = forma_info["valor"].lower()

    if forma not in FORMAS_VALIDAS:

        raise ErrorFractalEsp(
            "semántico",
            f"forma no soportada: {forma!r}. "
            f"Valores válidos: "
            f"{', '.join(sorted(FORMAS_VALIDAS))}",
            forma_info["linea"],
            forma_info["columna"],
        )

    # ======================================================
    # REPETICIONES
    # ======================================================

    rep_info = p["repeticiones"]

    texto_rep = rep_info["valor"]

    try:
        numero_rep = float(texto_rep)

    except ValueError:

        raise ErrorFractalEsp(
            "semántico",
            f"repeticiones debe ser un número entero; "
            f"se recibió {texto_rep!r}",
            rep_info["linea"],
            rep_info["columna"],
        )

    if not numero_rep.is_integer():

        raise ErrorFractalEsp(
            "semántico",
            f"repeticiones debe ser entero; "
            f"se recibió {texto_rep!r}",
            rep_info["linea"],
            rep_info["columna"],
        )

    repeticiones = int(numero_rep)

    if not 0 <= repeticiones <= 8:

        raise ErrorFractalEsp(
            "semántico",
            f"repeticiones fuera de rango: {repeticiones}. "
            f"El rango permitido es 0..8",
            rep_info["linea"],
            rep_info["columna"],
        )

    # ======================================================
    # ANGULO
    # ======================================================

    ang_info = p["angulo"]

    try:
        angulo = float(ang_info["valor"])

    except ValueError:

        raise ErrorFractalEsp(
            "semántico",
            f"angulo debe ser numérico; "
            f"se recibió {ang_info['valor']!r}",
            ang_info["linea"],
            ang_info["columna"],
        )

    if not 0 <= angulo <= 360:

        raise ErrorFractalEsp(
            "semántico",
            f"angulo fuera de rango: {angulo}. "
            f"El rango permitido es 0..360 grados",
            ang_info["linea"],
            ang_info["columna"],
        )

    # ======================================================
    # COLOR
    # ======================================================

    color_info = p["color"]

    color = color_info["valor"][1:-1].lower()

    if color not in COLORES_VALIDOS:

        raise ErrorFractalEsp(
            "semántico",
            f"color no soportado: {color!r}. "
            f"Colores válidos: "
            f"{', '.join(sorted(COLORES_VALIDOS))}",
            color_info["linea"],
            color_info["columna"],
        )

    return {
        "nombre": ast["nombre"],
        "forma": forma,
        "repeticiones": repeticiones,
        "angulo": angulo,
        "color": COLORES_VALIDOS[color],
    }