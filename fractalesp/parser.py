from .lexer import ErrorFractalEsp


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        return self.tokens[self.pos]

    def avanzar(self):
        token = self.actual()
        self.pos += 1
        return token

    def esperar(self, tipo, descripcion=None):

        token = self.actual()

        if token.tipo != tipo:

            esperado = descripcion or tipo

            raise ErrorFractalEsp(
                "sintáctico",
                f"se esperaba {esperado}, "
                f"pero se encontró {token.tipo} ({token.valor!r})",
                token.linea,
                token.columna,
            )

        return self.avanzar()

    def parsear(self):

        self.esperar(
            "FRACTAL",
            "'fractal'"
        )

        nombre = self.esperar(
            "CADENA",
            "una cadena con el nombre del fractal"
        )

        self.esperar(
            "LLAVE_IZQ",
            "'{'"
        )

        propiedades = {}

        for _ in range(4):

            token = self.actual()

            if token.tipo == "LLAVE_DER":

                raise ErrorFractalEsp(
                    "sintáctico",
                    "faltan propiedades: se requieren "
                    "forma, repeticiones, angulo y color",
                    token.linea,
                    token.columna,
                )

            if token.tipo not in {
                "FORMA",
                "REPETICIONES",
                "ANGULO",
                "COLOR"
            }:

                raise ErrorFractalEsp(
                    "sintáctico",
                    f"se esperaba una propiedad válida, "
                    f"pero se encontró {token.valor!r}",
                    token.linea,
                    token.columna,
                )

            clave_token = self.avanzar()

            clave = clave_token.valor.lower()

            if clave in propiedades:

                raise ErrorFractalEsp(
                    "sintáctico",
                    f"la propiedad {clave!r} está repetida",
                    clave_token.linea,
                    clave_token.columna,
                )

            self.esperar(
                "DOSPUNTOS",
                "':'"
            )

            if clave == "forma":

                valor = self.esperar(
                    "IDENT",
                    "un identificador de forma: "
                    "triangulo, copo, cantor o helecho"
                )

            elif clave == "repeticiones":

                valor = self.esperar(
                    "NUMERO",
                    "un número entero"
                )

            elif clave == "angulo":

                valor = self.esperar(
                    "NUMERO",
                    "un número"
                )

            else:

                valor = self.esperar(
                    "CADENA",
                    "una cadena de color"
                )

            propiedades[clave] = {
                "valor": valor.valor,
                "linea": valor.linea,
                "columna": valor.columna,
                "token": valor.tipo,
            }

        self.esperar(
            "LLAVE_DER",
            "'}'"
        )

        self.esperar(
            "EOF",
            "fin del programa"
        )

        requeridas = {
            "forma",
            "repeticiones",
            "angulo",
            "color"
        }

        faltantes = requeridas - set(propiedades)

        if faltantes:

            token = self.actual()

            raise ErrorFractalEsp(
                "sintáctico",
                "faltan propiedades obligatorias: "
                + ", ".join(sorted(faltantes)),
                token.linea,
                token.columna,
            )

        return {
            "nombre": nombre.valor[1:-1],
            "propiedades": propiedades,
        }


def analizar_sintactico(tokens):
    return Parser(tokens).parsear()