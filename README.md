# Traductor PLN a Lenguaje Formal FractalESP

Proyecto de Procesamiento de Lenguaje Natural (PLN) que permite convertir instrucciones expresadas en español a código formal del lenguaje FractalESP para la generación de fractales.

El sistema utiliza Ollama con `llama3.2:3b` para interpretar las instrucciones del usuario y generar una representación estructurada que posteriormente es validada y traducida a código FractalESP.

## Características

* Traducción de lenguaje natural en español a FractalESP.
* Interpretación mediante un modelo de lenguaje local.
* Validación de la información extraída.
* Generación automática de código FractalESP.
* Compilación y generación de fractales.
* Interfaz gráfica desarrollada con Tkinter.

## Fractales disponibles

* `triangulo` — Triángulo de Sierpinski
* `copo` — Copo de nieve de Koch
* `cantor` — Conjunto de Cantor
* `helecho` — Helecho de Barnsley

## Propiedades disponibles

* `forma`
* `repeticiones`
* `angulo`
* `color`

## Requisitos

* Python 3.9 o superior
* Ollama
* Modelo `llama3.2:3b`

## Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
cd FractalESP_PNL
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows:

```powershell
.venv\Scripts\activate
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

Instalar el modelo de Ollama:

```powershell
ollama pull llama3.2:3b
```

## Ejecución

Ejecutar:

```powershell
python main.py
```

Para utilizar el traductor PLN, Ollama debe estar instalado y disponible en el sistema.

## Ejemplo

Entrada en lenguaje natural:

```text
Dibuja un copo azul con 5 repeticiones.
```

Salida en FractalESP:

```text
fractal "MiFractal" {
    forma: copo
    repeticiones: 5
    angulo: 0
    color: "azul"
}
```

El código generado puede ser procesado posteriormente por el compilador de FractalESP para generar el fractal.

## Estructura del proyecto

```text
FractalESP_PNL/
├── fractalesp/    # Lenguaje formal y compilador
├── pln/           # Procesamiento de lenguaje natural
├── datos/         # Datos y conceptos
├── pruebas/       # Pruebas del sistema
├── interfaz/      # Interfaz gráfica
├── main.py        # Punto de entrada
└── requirements.txt
```

## Proyecto académico

Desarrollado para el curso de Procesamiento de Lenguaje Natural.

Universidad Nacional del Altiplano — Puno
Escuela Profesional de Ingeniería de Sistemas
