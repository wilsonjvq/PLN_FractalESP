import tkinter as tk
from tkinter import scrolledtext

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from main import compilar, CODIGO_EJEMPLO


# ==========================================================
# VENTANA PRINCIPAL
# ==========================================================

class VentanaFractalEsp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "FractalESP - Lenguaje para generación de fractales"
        )

        self.root.geometry("1400x850")
        self.root.minsize(1100, 700)

        self.figura_actual = None
        self.canvas = None

        self.crear_interfaz()

        # Cargar ejemplo inicialmente
        self.editor_codigo.insert(
            "1.0",
            CODIGO_EJEMPLO
        )

        # Compilar automáticamente al iniciar
        self.compilar_codigo()

    # ======================================================
    # CREAR INTERFAZ
    # ======================================================

    def crear_interfaz(self):

        # --------------------------------------------------
        # TÍTULO
        # --------------------------------------------------

        titulo = tk.Label(
            self.root,
            text="FractalESP",
            font=("Arial", 22, "bold")
        )

        titulo.pack(
            pady=(10, 0)
        )

        subtitulo = tk.Label(
            self.root,
            text="Lenguaje para generación de fractales",
            font=("Arial", 11)
        )

        subtitulo.pack(
            pady=(0, 10)
        )

        # --------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # --------------------------------------------------

        contenedor = tk.Frame(
            self.root
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        contenedor.grid_columnconfigure(
            0,
            weight=1
        )

        contenedor.grid_columnconfigure(
            1,
            weight=1
        )

        contenedor.grid_rowconfigure(
            0,
            weight=1
        )

        # --------------------------------------------------
        # PANEL IZQUIERDO
        # --------------------------------------------------

        panel_izquierdo = tk.Frame(
            contenedor,
            bd=1,
            relief="solid"
        )

        panel_izquierdo.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5)
        )

        panel_izquierdo.grid_rowconfigure(
            1,
            weight=1
        )

        panel_izquierdo.grid_columnconfigure(
            0,
            weight=1
        )

        etiqueta_codigo = tk.Label(
            panel_izquierdo,
            text="Código FractalESP",
            font=("Arial", 12, "bold"),
            anchor="w"
        )

        etiqueta_codigo.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        self.editor_codigo = scrolledtext.ScrolledText(
            panel_izquierdo,
            wrap=tk.NONE,
            font=("Consolas", 11),
            undo=True
        )

        self.editor_codigo.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        # --------------------------------------------------
        # PANEL DERECHO
        # --------------------------------------------------

        panel_derecho = tk.Frame(
            contenedor,
            bd=1,
            relief="solid"
        )

        panel_derecho.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0)
        )

        panel_derecho.grid_rowconfigure(
            1,
            weight=1
        )

        panel_derecho.grid_columnconfigure(
            0,
            weight=1
        )

        etiqueta_grafico = tk.Label(
            panel_derecho,
            text="Visualización del fractal",
            font=("Arial", 12, "bold"),
            anchor="w"
        )

        etiqueta_grafico.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=8
        )

        self.panel_grafico = tk.Frame(
            panel_derecho,
            bg="white"
        )

        self.panel_grafico.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        # --------------------------------------------------
        # BOTONES
        # --------------------------------------------------

        panel_botones = tk.Frame(
            self.root
        )

        panel_botones.pack(
            fill="x",
            padx=10,
            pady=5
        )

        boton_compilar = tk.Button(
            panel_botones,
            text="▶ Compilar",
            font=("Arial", 10, "bold"),
            command=self.compilar_codigo,
            padx=15,
            pady=5
        )

        boton_compilar.pack(
            side="left",
            padx=5
        )

        boton_limpiar = tk.Button(
            panel_botones,
            text="Limpiar salida",
            command=self.limpiar_salida,
            padx=15,
            pady=5
        )

        boton_limpiar.pack(
            side="left",
            padx=5
        )

        boton_ejemplo = tk.Button(
            panel_botones,
            text="Cargar ejemplo",
            command=self.cargar_ejemplo,
            padx=15,
            pady=5
        )

        boton_ejemplo.pack(
            side="left",
            padx=5
        )

        # --------------------------------------------------
        # SALIDA DEL COMPILADOR
        # --------------------------------------------------

        etiqueta_salida = tk.Label(
            self.root,
            text="Salida del compilador",
            font=("Arial", 12, "bold"),
            anchor="w"
        )

        etiqueta_salida.pack(
            fill="x",
            padx=10,
            pady=(5, 3)
        )

        self.salida_compilador = scrolledtext.ScrolledText(
            self.root,
            height=13,
            wrap=tk.NONE,
            font=("Consolas", 9),
            state="disabled"
        )

        self.salida_compilador.pack(
            fill="both",
            padx=10,
            pady=(0, 10)
        )

    # ======================================================
    # COMPILAR
    # ======================================================

    def compilar_codigo(self):

        codigo = self.editor_codigo.get(
            "1.0",
            tk.END
        ).strip()

        if not codigo:

            self.mostrar_salida(
                "No se ingresó código FractalESP."
            )

            self.limpiar_figura()

            return

        # Compilar
        resultado = compilar(
            codigo,
            generar=True
        )

        # Mostrar salida real del compilador
        self.mostrar_salida(
            resultado["salida"]
        )

        # Mostrar o limpiar fractal
        if resultado["exito"]:

            figura = resultado.get(
                "figura"
            )

            if figura is not None:

                self.mostrar_figura(
                    figura
                )

        else:

            self.limpiar_figura()

    # ======================================================
    # MOSTRAR SALIDA
    # ======================================================

    def mostrar_salida(self, texto):

        self.salida_compilador.config(
            state="normal"
        )

        self.salida_compilador.delete(
            "1.0",
            tk.END
        )

        self.salida_compilador.insert(
            tk.END,
            texto
        )

        self.salida_compilador.config(
            state="disabled"
        )

        self.salida_compilador.see(
            "1.0"
        )

    # ======================================================
    # MOSTRAR FIGURA
    # ======================================================

    def mostrar_figura(self, figura):

        # Eliminar figura anterior
        self.limpiar_figura()

        self.figura_actual = figura

        self.canvas = FigureCanvasTkAgg(
            figura,
            master=self.panel_grafico
        )

        self.canvas.draw()

        widget_canvas = self.canvas.get_tk_widget()

        widget_canvas.pack(
            fill="both",
            expand=True
        )

    # ======================================================
    # LIMPIAR FIGURA
    # ======================================================

    def limpiar_figura(self):

        if self.canvas is not None:

            self.canvas.get_tk_widget().destroy()

            self.canvas = None

        if self.figura_actual is not None:

            plt.close(
                self.figura_actual
            )

            self.figura_actual = None

    # ======================================================
    # LIMPIAR SALIDA
    # ======================================================

    def limpiar_salida(self):

        self.salida_compilador.config(
            state="normal"
        )

        self.salida_compilador.delete(
            "1.0",
            tk.END
        )

        self.salida_compilador.config(
            state="disabled"
        )

    # ======================================================
    # CARGAR EJEMPLO
    # ======================================================

    def cargar_ejemplo(self):

        self.editor_codigo.delete(
            "1.0",
            tk.END
        )

        self.editor_codigo.insert(
            "1.0",
            CODIGO_EJEMPLO
        )

        self.compilar_codigo()


# ==========================================================
# INICIAR APLICACIÓN
# ==========================================================

def iniciar():

    root = tk.Tk()

    app = VentanaFractalEsp(
        root
    )

    root.mainloop()


# ==========================================================
# EJECUCIÓN DIRECTA
# ==========================================================

if __name__ == "__main__":

    iniciar()