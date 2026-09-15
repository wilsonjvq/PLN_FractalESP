import re


PALABRAS_CLAVE = {
    "forma": "FORMA",
    "repeticiones": "REPETICIONES",
    "angulo": "ANGULO",
    "color": "COLOR",
}


TOKEN_REGEX = re.compile(
    r'(?P<ESPACIO>[ \t\r\n]+)'
    r'|(?P<LLAVE_IZQ>\{)'
    r'|(?P<LLAVE_DER>\})'
    r'|(?P<DOSPUNTOS>:)'
    r'|(?P<CADENA>"[^"\n]*")'
    r'|(?P<NUMERO>[+-]?(?:\d+(?:\.\d*)?|\.\d+))'
    r'|(?P<IDENT>[A-Za-zÁÉÍÓÚÑáéíóúñ_][A-Za-zÁÉÍÓÚÑáéíóúñ_0-9]*)'
)


class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return (
            f"{self.tipo}({self.valor!r}, "
            f"L{self.linea}:C{self.columna})"
        )


class ErrorFractalEsp(Exception):
    def __init__(self, fase, mensaje, linea, columna):
        self.fase = fase
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

        super().__init__(
            f"ERROR {fase.upper()} | "
            f"línea {linea}, columna {columna}: {mensaje}"
        )


def _posicion(codigo, indice):
    antes = codigo[:indice]

    linea = antes.count("\n") + 1

    ultima_nueva_linea = antes.rfind("\n")

    if ultima_nueva_linea == -1:
        columna = indice + 1
    else:
        columna = indice - ultima_nueva_linea

    return linea, columna


def analizar_lexico(codigo):
    tokens = []
    indice = 0

    while indice < len(codigo):

        coincidencia = TOKEN_REGEX.match(codigo, indice)

        if coincidencia is None:
            linea, columna = _posicion(codigo, indice)
            caracter = codigo[indice]

            raise ErrorFractalEsp(
                "léxico",
                f"carácter no reconocido: {caracter!r}",
                linea,
                columna,
            )

        tipo = coincidencia.lastgroup
        valor = coincidencia.group()

        linea, columna = _posicion(codigo, indice)

        indice = coincidencia.end()

        if tipo == "ESPACIO":
            continue

        if tipo == "IDENT":

            palabra = valor.lower()

            if palabra == "fractal":
                tipo = "FRACTAL"

            elif palabra in PALABRAS_CLAVE:
                tipo = PALABRAS_CLAVE[palabra]

            else:
                tipo = "IDENT"

        tokens.append(
            Token(
                tipo,
                valor,
                linea,
                columna
            )
        )

    tokens.append(
        Token(
            "EOF",
            "",
            *_posicion(codigo, len(codigo))
        )
    )

    return tokens