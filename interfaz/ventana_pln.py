import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from main import compilar, CODIGO_EJEMPLO

from pln.normalizador import normalizar_texto
from pln.extractor import extraer_representacion
from pln.traductor import traducir_fractalesp


# ==========================================================
# VENTANA PRINCIPAL
# ==========================================================

class VentanaFractalEspPLN:

    def __init__(self, root):

        self.root = root

        # --------------------------------------------------
        # CONFIGURACIÓN DE VENTANA
        # --------------------------------------------------

        self.root.title(
            "FractalESP - PLN + Compilador"
        )

        # Tamaño fijo adecuado para pantalla Full HD
        self.root.geometry(
            "1100x1000"
        )

        self.root.resizable(
            False,
            False
        )

        self.figura_actual = None
        self.canvas = None

        # --------------------------------------------------
        # CREAR INTERFAZ
        # --------------------------------------------------

        self.crear_interfaz()

        # Cargar código inicial
        self.editor_codigo.insert(
            "1.0",
            CODIGO_EJEMPLO
        )

        # Compilar automáticamente
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
            pady=(8, 0)
        )

        subtitulo = tk.Label(
            self.root,
            text="Procesamiento de Lenguaje Natural + Lenguaje para generación de fractales",
            font=("Arial", 10)
        )

        subtitulo.pack(
            pady=(0, 6)
        )

        # ==================================================
        # SECCIÓN PLN
        # ==================================================

        panel_pln = tk.Frame(
            self.root,
            bd=1,
            relief="solid"
        )

        panel_pln.pack(
            fill="x",
            padx=10,
            pady=(0, 5)
        )

        # --------------------------------------------------
        # TÍTULO PLN
        # --------------------------------------------------

        etiqueta_pln = tk.Label(
            panel_pln,
            text="1. Lenguaje natural",
            font=("Arial", 11, "bold"),
            anchor="w"
        )

        etiqueta_pln.pack(
            fill="x",
            padx=8,
            pady=(5, 2)
        )

        # --------------------------------------------------
        # ENTRADA LENGUAJE NATURAL
        # --------------------------------------------------

        self.entrada_natural = scrolledtext.ScrolledText(
            panel_pln,
            height=2,
            wrap=tk.WORD,
            font=("Arial", 11),
            undo=True
        )

        self.entrada_natural.pack(
            fill="x",
            padx=8,
            pady=(0, 5)
        )

        # Texto inicial
        self.entrada_natural.insert(
            "1.0",
            "Dibuja un copo azul con 5 repeticiones"
        )

        # --------------------------------------------------
        # BOTÓN CONVERTIR
        # --------------------------------------------------

        panel_boton_pln = tk.Frame(
            panel_pln
        )

        panel_boton_pln.pack(
            fill="x",
            padx=8,
            pady=(0, 5)
        )

        boton_convertir = tk.Button(
            panel_boton_pln,
            text="🧠 Convertir a FractalESP",
            font=("Arial", 10, "bold"),
            command=self.convertir_lenguaje_natural,
            padx=15,
            pady=5
        )

        boton_convertir.pack(
            side="left"
        )

        # --------------------------------------------------
        # SALIDA PLN
        # --------------------------------------------------

        etiqueta_salida_pln = tk.Label(
            panel_pln,
            text="Salida del PLN",
            font=("Arial", 10, "bold"),
            anchor="w"
        )

        etiqueta_salida_pln.pack(
            fill="x",
            padx=8,
            pady=(0, 2)
        )

        self.salida_pln = scrolledtext.ScrolledText(
            panel_pln,
            height=4,
            wrap=tk.NONE,
            font=("Consolas", 9),
            state="disabled"
        )

        self.salida_pln.pack(
            fill="x",
            padx=8,
            pady=(0, 7)
        )

        # ==================================================
        # CONTENEDOR CENTRAL
        # ==================================================

        contenedor = tk.Frame(
            self.root
        )

        contenedor.pack(
            fill="x",
            expand=False,
            padx=10,
            pady=5
        )

        contenedor.configure(
            height=400
        )

        contenedor.pack_propagate(False)

        contenedor.grid_columnconfigure(
            0,
            weight=4
        )

        contenedor.grid_columnconfigure(
            1,
            weight=6
        )

        contenedor.grid_rowconfigure(
            0,
            weight=1
        )

        # ==================================================
        # PANEL IZQUIERDO
        # ==================================================

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
            text="2. Código FractalESP",
            font=("Arial", 11, "bold"),
            anchor="w"
        )

        etiqueta_codigo.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=6
        )

        self.editor_codigo = scrolledtext.ScrolledText(
            panel_izquierdo,
            wrap=tk.NONE,
            font=("Consolas", 10),
            undo=True
        )

        self.editor_codigo.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(0, 8)
        )

        # ==================================================
        # PANEL DERECHO
        # ==================================================

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
            text="3. Visualización del fractal",
            font=("Arial", 11, "bold"),
            anchor="w"
        )

        etiqueta_grafico.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=6
        )

        self.panel_grafico = tk.Frame(
            panel_derecho,
            bg="white"
        )

        self.panel_grafico.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(0, 8)
        )

        # ==================================================
        # BOTONES DEL COMPILADOR
        # ==================================================

        panel_botones = tk.Frame(
            self.root
        )

        panel_botones.pack(
            fill="x",
            padx=10,
            pady=4
        )

        # --------------------------------------------------
        # COMPILAR
        # --------------------------------------------------

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

        # --------------------------------------------------
        # LIMPIAR
        # --------------------------------------------------

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

        # --------------------------------------------------
        # CARGAR EJEMPLO
        # --------------------------------------------------

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

        # ==================================================
        # SALIDA DEL COMPILADOR
        # ==================================================

        etiqueta_salida = tk.Label(
            self.root,
            text="4. Salida del compilador",
            font=("Arial", 11, "bold"),
            anchor="w"
        )

        etiqueta_salida.pack(
            fill="x",
            padx=10,
            pady=(3, 2)
        )

        self.salida_compilador = scrolledtext.ScrolledText(
            self.root,
            height=7,
            wrap=tk.NONE,
            font=("Consolas", 9),
            state="disabled"
        )

        self.salida_compilador.pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )

    # ======================================================
    # CONVERTIR LENGUAJE NATURAL
    # ======================================================

    def convertir_lenguaje_natural(self):

        texto = self.entrada_natural.get(
            "1.0",
            tk.END
        ).strip()

        if not texto:

            self.mostrar_salida_pln(
                "ERROR: No se ingresó una instrucción."
            )

            return

        try:

            # ----------------------------------------------
            # NORMALIZACIÓN
            # ----------------------------------------------

            texto_normalizado = (
                normalizar_texto(
                    texto
                )
            )

            # ----------------------------------------------
            # PLN
            # ----------------------------------------------

            representacion = (
                extraer_representacion(
                    texto_normalizado
                )
            )

            # ----------------------------------------------
            # TRADUCCIÓN
            # ----------------------------------------------

            codigo = (
                traducir_fractalesp(
                    representacion
                )
            )

            # ----------------------------------------------
            # ACTUALIZAR EDITOR
            # ----------------------------------------------

            self.editor_codigo.delete(
                "1.0",
                tk.END
            )

            self.editor_codigo.insert(
                "1.0",
                codigo
            )

            # ----------------------------------------------
            # MOSTRAR RESULTADO DEL PLN
            # ----------------------------------------------

            datos = representacion.model_dump()

            salida = (
                "ENTRADA:\n"
                f"{texto}\n\n"

                "NORMALIZADO:\n"
                f"{texto_normalizado}\n\n"

                "REPRESENTACIÓN INTERMEDIA:\n"
                f"forma: {datos['forma']}\n"
                f"repeticiones: {datos['repeticiones']}\n"
                f"angulo: {datos['angulo']}\n"
                f"color: {datos['color']}\n\n"

                "ESTADO:\n"
                "Conversión realizada correctamente."
            )

            self.mostrar_salida_pln(
                salida
            )

        except Exception as error:

            mensaje = (
                "ERROR EN EL PLN\n\n"
                f"{type(error).__name__}: "
                f"{error}"
            )

            self.mostrar_salida_pln(
                mensaje
            )

            messagebox.showerror(
                "Error de PLN",
                str(error)
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

        try:

            resultado = compilar(
                codigo,
                generar=True
            )

            # ----------------------------------------------
            # SALIDA REAL DEL COMPILADOR
            # ----------------------------------------------

            self.mostrar_salida(
                resultado["salida"]
            )

            # ----------------------------------------------
            # MOSTRAR FRACTAL
            # ----------------------------------------------

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

        except Exception as error:

            self.mostrar_salida(
                "ERROR AL COMPILAR\n\n"
                f"{type(error).__name__}: "
                f"{error}"
            )

            self.limpiar_figura()

    # ======================================================
    # MOSTRAR SALIDA PLN
    # ======================================================

    def mostrar_salida_pln(self, texto):

        self.salida_pln.config(
            state="normal"
        )

        self.salida_pln.delete(
            "1.0",
            tk.END
        )

        self.salida_pln.insert(
            tk.END,
            texto
        )

        self.salida_pln.config(
            state="disabled"
        )

        self.salida_pln.see(
            "1.0"
        )

    # ======================================================
    # MOSTRAR SALIDA COMPILADOR
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

        self.limpiar_figura()

        self.figura_actual = figura

        self.canvas = FigureCanvasTkAgg(
            figura,
            master=self.panel_grafico
        )

        self.canvas.draw()

        widget_canvas = (
            self.canvas.get_tk_widget()
        )

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

        self.mostrar_salida(
            ""
        )

    # ======================================================
    # CARGAR EJEMPLO
    # ======================================================

    def cargar_ejemplo(self):

        self.entrada_natural.delete(
            "1.0",
            tk.END
        )

        self.entrada_natural.insert(
            "1.0",
            "Dibuja un copo azul con 5 repeticiones"
        )

        self.mostrar_salida_pln(
            ""
        )

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

    VentanaFractalEspPLN(
        root
    )

    root.mainloop()


# ==========================================================
# EJECUCIÓN DIRECTA
# ==========================================================

if __name__ == "__main__":

    iniciar()