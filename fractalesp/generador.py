import numpy as np
import matplotlib.pyplot as plt


# ==========================================================
# 1. TRIÁNGULO DE SIERPINSKI
# ==========================================================

def generar_sierpinski(parametros):
    repeticiones = parametros["repeticiones"]
    color = parametros["color"]
    nombre = parametros["nombre"]

    puntos = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.5, np.sqrt(3) / 2]
    ])

    puntos_actuales = puntos.copy()

    for _ in range(repeticiones):
        nuevos_puntos = []

        for i in range(len(puntos_actuales)):
            p1 = puntos_actuales[i]
            p2 = puntos_actuales[(i + 1) % len(puntos_actuales)]

            nuevos_puntos.append(p1)
            nuevos_puntos.append((p1 + p2) / 2)

        puntos_actuales = np.array(nuevos_puntos)

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.fill(
        puntos[:, 0],
        puntos[:, 1],
        color="white",
        edgecolor=color,
        linewidth=1.5
    )

    # Generación recursiva del Sierpinski
    def triangulo(p1, p2, p3, nivel):
        if nivel == 0:
            ax.fill(
                [p1[0], p2[0], p3[0]],
                [p1[1], p2[1], p3[1]],
                color=color
            )
            return

        m12 = (p1 + p2) / 2
        m23 = (p2 + p3) / 2
        m31 = (p3 + p1) / 2

        triangulo(p1, m12, m31, nivel - 1)
        triangulo(m12, p2, m23, nivel - 1)
        triangulo(m31, m23, p3, nivel - 1)

    triangulo(puntos[0], puntos[1], puntos[2], repeticiones)

    ax.set_title(nombre)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()

    return fig


# ==========================================================
# 2. COPITO DE KOCH
# ==========================================================

def generar_koch(parametros):
    repeticiones = parametros["repeticiones"]
    color = parametros["color"]
    angulo = parametros["angulo"]
    nombre = parametros["nombre"]

    def koch(p1, p2, nivel):
        if nivel == 0:
            return [p1, p2]

        p1 = np.array(p1)
        p2 = np.array(p2)

        vector = (p2 - p1) / 3

        a = p1 + vector
        b = p1 + 2 * vector

        angulo_rad = np.radians(60 + angulo)

        rotacion = np.array([
            [np.cos(angulo_rad), -np.sin(angulo_rad)],
            [np.sin(angulo_rad), np.cos(angulo_rad)]
        ])

        c = a + rotacion @ vector

        puntos = []

        puntos.extend(koch(p1, a, nivel - 1)[:-1])
        puntos.extend(koch(a, c, nivel - 1)[:-1])
        puntos.extend(koch(c, b, nivel - 1)[:-1])
        puntos.extend(koch(b, p2, nivel - 1))

        return puntos

    triangulo = [
        np.array([0.0, 0.0]),
        np.array([1.0, 0.0]),
        np.array([0.5, np.sqrt(3) / 2]),
        np.array([0.0, 0.0])
    ]

    todos = []

    for i in range(3):
        segmento = koch(
            triangulo[i],
            triangulo[i + 1],
            repeticiones
        )

        todos.extend(segmento[:-1])

    todos.append(triangulo[-1])

    todos = np.array(todos)

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.plot(
        todos[:, 0],
        todos[:, 1],
        color=color,
        linewidth=1.5
    )

    ax.set_title(nombre)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()

    return fig


# ==========================================================
# 3. CONJUNTO DE CANTOR
# ==========================================================

def generar_cantor(parametros):
    repeticiones = parametros["repeticiones"]
    color = parametros["color"]
    nombre = parametros["nombre"]

    fig, ax = plt.subplots(figsize=(7, 5))

    def cantor(x1, x2, y, nivel):
        if nivel == 0:
            return

        ax.plot(
            [x1, x2],
            [y, y],
            color=color,
            linewidth=6,
            solid_capstyle="butt"
        )

        tercio = (x2 - x1) / 3

        cantor(
            x1,
            x1 + tercio,
            y - 1,
            nivel - 1
        )

        cantor(
            x2 - tercio,
            x2,
            y - 1,
            nivel - 1
        )

    cantor(0, 1, 0, repeticiones + 1)

    ax.set_title(nombre)
    ax.axis("off")

    fig.tight_layout()

    return fig


# ==========================================================
# 4. HELECHO DE BARNSLEY
# ==========================================================

def generar_helecho(parametros):
    repeticiones = parametros["repeticiones"]
    color = parametros["color"]
    angulo = parametros["angulo"]
    nombre = parametros["nombre"]

    iteraciones = max(1000, repeticiones * 5000)

    x = 0.0
    y = 0.0

    puntos_x = []
    puntos_y = []

    rng = np.random.default_rng(42)

    for _ in range(iteraciones):

        numero = rng.random()

        if numero < 0.01:

            x_nuevo = 0
            y_nuevo = 0.16 * y

        elif numero < 0.86:

            x_nuevo = (
                0.85 * x
                + 0.04 * y
            )

            y_nuevo = (
                -0.04 * x
                + 0.85 * y
                + 1.6
            )

        elif numero < 0.93:

            x_nuevo = (
                0.20 * x
                - 0.26 * y
            )

            y_nuevo = (
                0.23 * x
                + 0.22 * y
                + 1.6
            )

        else:

            x_nuevo = (
                -0.15 * x
                + 0.28 * y
            )

            y_nuevo = (
                0.26 * x
                + 0.24 * y
                + 0.44
            )

        x = x_nuevo
        y = y_nuevo

        # Aplicar ángulo adicional
        if angulo != 0:
            rad = np.radians(angulo)

            x_rotado = (
                x * np.cos(rad)
                - y * np.sin(rad)
            )

            y_rotado = (
                x * np.sin(rad)
                + y * np.cos(rad)
            )

            x = x_rotado
            y = y_rotado

        puntos_x.append(x)
        puntos_y.append(y)

    fig, ax = plt.subplots(figsize=(6, 7))

    ax.scatter(
        puntos_x,
        puntos_y,
        s=0.2,
        color=color
    )

    ax.set_title(nombre)
    ax.axis("off")

    fig.tight_layout()

    return fig


# ==========================================================
# DICCIONARIO DE GENERADORES
# ==========================================================

GENERADORES = {
    "triangulo": generar_sierpinski,
    "copo": generar_koch,
    "cantor": generar_cantor,
    "helecho": generar_helecho
}