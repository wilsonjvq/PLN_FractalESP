from fractalesp.lexer import analizar_lexico, ErrorFractalEsp
from fractalesp.parser import analizar_sintactico
from fractalesp.semantico import analizar_semantico
from fractalesp.generador import GENERADORES


# ==========================================================
# CÓDIGO DE EJEMPLO
# ==========================================================

CODIGO_EJEMPLO = '''fractal "MiPrimerFractal" {
    forma: triangulo
    repeticiones: 3
    angulo: 0
    color: "azul"
}'''


# ==========================================================
# COMPILADOR
# ==========================================================

def compilar(codigo, generar=True):

    salida = []

    salida.append("=" * 70)
    salida.append("COMPILACIÓN FRACTALESP")
    salida.append("=" * 70)
    salida.append("")

    figura = None

    try:

        # ==================================================
        # 1. ANÁLISIS LÉXICO
        # ==================================================

        salida.append("[1/4] ANÁLISIS LÉXICO")

        tokens = analizar_lexico(codigo)

        salida.append("OK — tokens reconocidos:")

        for token in tokens:

            salida.append(
                f"  {token.tipo}('{token.valor}', "
                f"L{token.linea}:C{token.columna})"
            )

        salida.append("")

        # ==================================================
        # 2. ANÁLISIS SINTÁCTICO
        # ==================================================

        salida.append("[2/4] ANÁLISIS SINTÁCTICO")

        ast = analizar_sintactico(tokens)

        salida.append("OK — estructura válida:")
        salida.append(str(ast))
        salida.append("")

        # ==================================================
        # 3. ANÁLISIS SEMÁNTICO
        # ==================================================

        salida.append("[3/4] ANÁLISIS SEMÁNTICO")

        parametros = analizar_semantico(ast)

        salida.append("OK — significado válido:")
        salida.append(str(parametros))
        salida.append("")

        # ==================================================
        # 4. GENERACIÓN
        # ==================================================

        salida.append("[4/4] GENERACIÓN")

        if generar:

            forma = parametros["forma"]

            if forma not in GENERADORES:
                raise ErrorFractalEsp(
                    f"Forma de fractal no soportada: {forma}"
                )

            figura = GENERADORES[forma](parametros)

            salida.append("OK — fractal generado.")

        else:

            salida.append(
                "OMITIDA — modo de prueba sin gráfico."
            )

        salida.append("")
        salida.append("=" * 70)
        salida.append("RESULTADO: COMPILACIÓN EXITOSA")
        salida.append("=" * 70)

        return {
            "exito": True,
            "salida": "\n".join(salida),
            "tokens": tokens,
            "ast": ast,
            "parametros": parametros,
            "figura": figura
        }

    except ErrorFractalEsp as error:

        salida.append("")
        salida.append("=" * 70)
        salida.append("ERROR DE COMPILACIÓN")
        salida.append("=" * 70)
        salida.append(str(error))

        return {
            "exito": False,
            "salida": "\n".join(salida),
            "error": str(error),
            "figura": None
        }

    except Exception as error:

        salida.append("")
        salida.append("=" * 70)
        salida.append("ERROR INTERNO")
        salida.append("=" * 70)
        salida.append(
            f"{type(error).__name__}: {error}"
        )

        return {
            "exito": False,
            "salida": "\n".join(salida),
            "error": str(error),
            "figura": None
        }


# ==========================================================
# PRUEBA DESDE CONSOLA
# ==========================================================

if __name__ == "__main__":

    resultado = compilar(
        CODIGO_EJEMPLO,
        generar=True
    )

    print(resultado["salida"])