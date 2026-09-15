import json

import ollama


MODELO_OLLAMA = "llama3.2:3b"


SYSTEM_PROMPT = """
Eres el componente de PLN del lenguaje FractalESP.

Tu tarea es interpretar instrucciones escritas en español
y convertirlas en una representación estructurada JSON.

FractalESP permite las siguientes formas:

- triangulo
- copo
- cantor
- helecho

Las propiedades disponibles son:

- forma
- repeticiones
- angulo
- color

Debes identificar estas propiedades a partir del lenguaje
natural.

Reglas:

1. forma debe ser una de:
   triangulo
   copo
   cantor
   helecho

2. repeticiones debe ser un número entero.

3. angulo debe ser un número.

4. color debe ser un texto.

5. Si el usuario no proporciona una propiedad,
   utiliza null.

6. No inventes valores proporcionados por el usuario.

7. No escribas código FractalESP.

8. No escribas explicaciones.

9. Devuelve exclusivamente un objeto JSON válido.

Ejemplo:

Entrada:
"Dibuja un copo azul con 5 repeticiones"

Salida:

{
    "forma": "copo",
    "repeticiones": 5,
    "angulo": null,
    "color": "azul"
}
"""


def extraer_json(texto):

    inicio = texto.find("{")
    fin = texto.rfind("}")

    if inicio == -1 or fin == -1:
        raise ValueError(
            "Ollama no devolvió un objeto JSON."
        )

    contenido = texto[
        inicio:fin + 1
    ]

    return json.loads(contenido)


def interpretar(texto):

    respuesta = ollama.chat(

        model=MODELO_OLLAMA,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": texto
            }
        ],

        options={
            "temperature": 0
        }
    )

    contenido = respuesta[
        "message"
    ][
        "content"
    ]

    return extraer_json(
        contenido
    )