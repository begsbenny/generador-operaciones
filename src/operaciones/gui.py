"""Interfaz gráfica del Generador de Operaciones (CustomTkinter, POO)."""

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from operaciones import __copyright__, __date__, __license__, __version__, config, logic, recursos


class OperacionesApp(ctk.CTk):
    """Ventana principal. Todo el estado vive en atributos de instancia."""

    def __init__(self):
        super().__init__()

        # --- Estado de la aplicación (antes variables globales) ---
        self.esperando_resultado = False   # False: el próximo Enter genera; True: revela el resultado
        self.operacion_actual = None       # logic.Operacion en pantalla
        self.font_size = config.FONT_SIZE_INICIAL

        # --- Ventana ---
        self.title(f"Generador de Operaciones v{__version__}")
        self.geometry(f"{self.winfo_screenwidth()}x{config.VENTANA_ALTO}")

        # Grid principal: fila 0 = controles (auto), fila 1 = área central (expandible)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # --- Variables de control ---
        self.operacion_var = ctk.StringVar(master=self, value=config.OPERADORES[0])

        # --- Frame superior (inputs) ---
        self.frame_inputs = ctk.CTkFrame(self, corner_radius=10)
        self.frame_inputs.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        self.frame_inputs.grid_columnconfigure(0, weight=1, minsize=140)  # Izquierda (cuadrícula)
        self.frame_inputs.grid_columnconfigure(1, weight=2)               # Centro (controles)
        self.frame_inputs.grid_columnconfigure(2, weight=1, minsize=140)  # Derecha (cuadrícula)
        self.frame_inputs.grid_rowconfigure(0, weight=1)

        # Área izquierda: cuadrícula tic-tac-toe (letras a-i)
        self.frame_izq_wrapper = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_izq_wrapper.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_izq_wrapper.grid_columnconfigure(0, weight=1)
        self.frame_izq_wrapper.grid_rowconfigure(0, weight=1)

        self.canvas_izq = tk.Canvas(
            self.frame_izq_wrapper, width=config.TICTACTOE_TAM, height=config.TICTACTOE_TAM,
            highlightthickness=0, bg=config.CANVAS_BG,
        )
        self.canvas_izq.grid(row=0, column=0, sticky="")
        self.dibujar_tictactoe(self.canvas_izq)

        # Área central: controles
        self.frame_centro = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_centro.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        for col in range(4):
            self.frame_centro.grid_columnconfigure(col, weight=1)
        self.frame_centro.grid_rowconfigure(0, weight=0)
        self.frame_centro.grid_rowconfigure(1, weight=0)

        self.entry_cifras1 = self._crear_campo(self.frame_centro, 0, "Cifras (Arriba):", 60, str(config.CIFRAS_POR_DEFECTO))
        self.entry_cifras2 = self._crear_campo(self.frame_centro, 1, "Cifras (Abajo):", 60, str(config.CIFRAS_POR_DEFECTO))

        # Bloque operación (radios)
        self.frame_operacion = ctk.CTkFrame(self.frame_centro, fg_color="transparent")
        self.frame_operacion.grid(row=0, column=2, padx=10, pady=10, sticky="n")

        self.label_operacion = ctk.CTkLabel(
            self.frame_operacion, text="Operación:", font=ctk.CTkFont("Arial", 12)
        )
        self.label_operacion.pack(pady=(5, 2))

        self.frame_radios = ctk.CTkFrame(self.frame_operacion, fg_color="transparent")
        self.frame_radios.pack()
        self.radios_operacion = []
        for sym in config.OPERADORES:
            radio = ctk.CTkRadioButton(
                self.frame_radios, text=sym, variable=self.operacion_var, value=sym,
                font=ctk.CTkFont("Arial", 14, "bold"), width=30,
            )
            radio.pack(side="left", padx=8)
            self.radios_operacion.append(radio)

        self.entry_limite = self._crear_campo(self.frame_centro, 3, "Valor Máximo:", 100, str(config.LIMITE_POR_DEFECTO))

        # Fila del botón Generar (con las letras del resultado a los lados)
        self.frame_botones = ctk.CTkFrame(self.frame_centro, fg_color="transparent")
        self.frame_botones.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky="ew", padx=10)
        self.frame_botones.grid_columnconfigure(0, weight=1)
        self.frame_botones.grid_columnconfigure(1, weight=0)
        self.frame_botones.grid_columnconfigure(2, weight=1)

        self.label_letras_izq = ctk.CTkLabel(
            self.frame_botones, text="", font=ctk.CTkFont("Arial", 12, "bold"),
            text_color=config.COLOR_LETRAS_RESULTADO,
        )
        self.label_letras_izq.grid(row=0, column=0, sticky="w", padx=(10, 0))

        self.btn_generar = ctk.CTkButton(
            self.frame_botones, text="Generar / Enter", command=self.accion_principal,
            font=ctk.CTkFont("Arial", 13, "bold"), height=40, width=220, corner_radius=8,
        )
        self.btn_generar.grid(row=0, column=1)

        self.label_letras_der = ctk.CTkLabel(
            self.frame_botones, text="", font=ctk.CTkFont("Arial", 12, "bold"),
            text_color=config.COLOR_LETRAS_RESULTADO,
        )
        self.label_letras_der.grid(row=0, column=2, sticky="e", padx=(0, 10))

        # Área derecha: cuadrícula tic-tac-toe (letras a-i)
        self.frame_der_wrapper = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_der_wrapper.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.frame_der_wrapper.grid_columnconfigure(0, weight=1)
        self.frame_der_wrapper.grid_rowconfigure(0, weight=1)

        self.canvas_der = tk.Canvas(
            self.frame_der_wrapper, width=config.TICTACTOE_TAM, height=config.TICTACTOE_TAM,
            highlightthickness=0, bg=config.CANVAS_BG,
        )
        self.canvas_der.grid(row=0, column=0, sticky="")
        self.dibujar_tictactoe(self.canvas_der)

        # --- Área central: la operación ---
        self.area_central = ctk.CTkFrame(self, fg_color="transparent")
        self.area_central.grid(row=1, column=0, sticky="nsew", padx=15, pady=(5, 10))
        self.area_central.grid_columnconfigure(0, weight=1)
        self.area_central.grid_rowconfigure(0, weight=1)

        self.col_principal = ctk.CTkFrame(self.area_central, fg_color="transparent")
        self.col_principal.grid(row=0, column=0)

        # Columna izquierda: números
        self.col_numeros = ctk.CTkFrame(self.col_principal, fg_color="transparent")
        self.col_numeros.pack(side="left", anchor="e")

        self.frame_a = ctk.CTkFrame(self.col_numeros, fg_color="transparent")
        self.frame_a.pack(anchor="e")

        self.frame_b = ctk.CTkFrame(self.col_numeros, fg_color="transparent")
        self.frame_b.pack(anchor="e")

        # Contenedor de la línea: altura fija y ancho lleno. Es TRANSPARENTE (CTkFrame) a propósito:
        # un tk.Frame normal pintaría su propio fondo gris y parecería una línea más larga que las cifras.
        # La línea interna se ancla a la derecha con relwidth.
        self.frame_linea_contenedor = ctk.CTkFrame(
            self.col_numeros, fg_color="transparent", width=1, height=config.LINEA_GROSOR, corner_radius=0
        )
        self.frame_linea_contenedor.pack(anchor="e", fill="x")

        self.frame_linea = tk.Frame(self.frame_linea_contenedor, bg=config.COLOR_LINEA)
        # Se posiciona con place en dibujar_operacion (relwidth = ancho / N)

        self.frame_result = ctk.CTkFrame(self.col_numeros, fg_color="transparent")
        self.frame_result.pack(anchor="e")

        self.frames_operacion = [self.frame_a, self.frame_b, self.frame_result]

        # Estado para ancho fijo de filas (N ranuras)
        self._n_ranuras = 0
        self._labels_resultado = []  # Etiquetas pre-creadas para el resultado

        # Columna derecha: operador
        self.col_operador = ctk.CTkFrame(self.col_principal, fg_color="transparent", width=80)
        self.col_operador.pack(side="left", padx=(10, 0), anchor="n")

        self.label_op = ctk.CTkLabel(
            self.col_operador, text="",
            font=ctk.CTkFont(config.FONT_FAMILY_OPERADOR, self.font_size, "bold"),
        )
        self.label_op.pack(anchor="n", pady=(0, 0))

        # --- Pie de ventana ---
        self.footer = ctk.CTkLabel(
            self, text=f"{__copyright__} — v{__version__}",
            font=ctk.CTkFont("Arial", 9), text_color="gray",
        )
        self.footer.grid(row=2, column=0, pady=(0, 5))

        self.boton_info = ctk.CTkButton(
            self, text="Acerca de", command=self.mostrar_acerca_de,
            font=ctk.CTkFont("Arial", 10), height=30, corner_radius=6,
            fg_color="transparent", border_width=1, text_color=("gray10", "gray90"),
        )
        self.boton_info.grid(row=3, column=0, pady=(0, 15))

        # --- Eventos ---
        self.bind("<Return>", self.accion_principal)
        self.bind("<MouseWheel>", self.zoom_text)
        self.entry_cifras1.focus()
        recursos.aplicar_icono(self)

    # ------------------------------------------------------------------
    # Construcción auxiliar
    # ------------------------------------------------------------------
    def _crear_campo(self, parent, columna, texto, ancho, valor_inicial):
        """Crea un bloque «etiqueta + campo numérico» y devuelve el campo."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=columna, padx=10, pady=10, sticky="n")

        label = ctk.CTkLabel(frame, text=texto, font=ctk.CTkFont("Arial", 12))
        label.pack(pady=(5, 2))

        entry = ctk.CTkEntry(frame, width=ancho, justify="center", font=ctk.CTkFont("Arial", 14))
        entry.pack(pady=(0, 5))
        entry.insert(0, valor_inicial)
        # Al enfocar, selecciona todo el contenido para reescribir rápido
        entry.bind("<FocusIn>", lambda e, campo=entry: campo.select_range(0, "end"))
        return entry

    def dibujar_tictactoe(self, canvas):
        """Dibuja la cuadrícula decorativa 3x3 con las letras a-i."""
        canvas.delete("all")
        tam = config.TICTACTOE_TAM
        celda = tam // 3
        for k in (1, 2):
            canvas.create_line(celda * k, 0, celda * k, tam, fill=config.TICTACTOE_COLOR_LINEA, width=1)
            canvas.create_line(0, celda * k, tam, celda * k, fill=config.TICTACTOE_COLOR_LINEA, width=1)

        for idx, letra in enumerate(config.TICTACTOE_LETRAS):
            fila, col = divmod(idx, 3)
            canvas.create_text(
                col * celda + celda // 2, fila * celda + celda // 2,
                text=letra, fill=config.TICTACTOE_COLOR_LETRA, font=("Arial", 11, "bold"),
            )

    def _fuente_numeros(self):
        return ctk.CTkFont(config.FONT_FAMILY, self.font_size, "bold")

    @staticmethod
    def _escribir_en(entry, valor):
        entry.delete(0, "end")
        entry.insert(0, str(valor))

    # ------------------------------------------------------------------
    # Control principal
    # ------------------------------------------------------------------
    def accion_principal(self, event=None):
        """Primer Enter: genera una operación. Segundo Enter: muestra el resultado."""
        if not self.esperando_resultado:
            operador = self.operacion_var.get()

            # 1. Normalizar lo escrito y reflejar los valores finales en los campos
            cifras1, cifras2, limite = logic.normalizar_parametros(
                self.entry_cifras1.get(), self.entry_cifras2.get(), self.entry_limite.get(), operador
            )
            self._escribir_en(self.entry_cifras1, cifras1)
            self._escribir_en(self.entry_cifras2, cifras2)
            self._escribir_en(self.entry_limite, limite)

            # 2. Calcular N = max_digitos para ancho fijo de filas
            self._n_ranuras = logic.max_digitos(cifras1, cifras2, limite, operador)

            # 3. Generar y dibujar
            self.operacion_actual = logic.generar_operacion(cifras1, cifras2, limite, operador)
            letras = logic.numero_a_letras(self.operacion_actual.resultado)
            self.label_letras_izq.configure(text=letras)
            self.label_letras_der.configure(text=letras)
            self.dibujar_operacion(self.operacion_actual)

            self.esperando_resultado = True
        else:
            self.mostrar_resultado()
            self.esperando_resultado = False

        self.focus_set()

    # ------------------------------------------------------------------
    # Dibujo
    # ------------------------------------------------------------------
    def _crear_etiquetas_numero(self, frame, n_ranuras, numero_str, colores=None):
        """Crea o actualiza N etiquetas para un número alineado a la derecha.
        Si `colores` es None, usa colores posicionales; si es una lista, usa esos colores.
        Devuelve la lista de etiquetas creadas.
        """
        for widget in frame.winfo_children():
            widget.destroy()

        labels = []
        # Rellenar con espacios a la izquierda hasta n_ranuras
        texto = numero_str.rjust(n_ranuras)
        for i, ch in enumerate(texto[::-1]):
            if colores is None:
                color = config.colores_posicionales[i % len(config.colores_posicionales)]
            else:
                color = colores[i]
            lbl = ctk.CTkLabel(
                frame, text=ch,
                text_color=color,
                font=self._fuente_numeros(),
            )
            lbl.pack(side="right")
            labels.append(lbl)
        return labels

    def colorear_numero(self, frame, numero_str):
        """Dibuja un número dígito a dígito, con color según su posición (de derecha a izquierda)."""
        self._crear_etiquetas_numero(frame, self._n_ranuras, numero_str)

    def dibujar_operacion(self, operacion):
        """Dibuja los operandos, el operador y la línea; deja vacío el resultado."""
        texto_a, texto_b, ancho_chars = logic.alinear_operandos(operacion)

        # Alinear a la derecha con N ranuras fijas
        self._crear_etiquetas_numero(self.frame_a, self._n_ranuras, texto_a)
        self._crear_etiquetas_numero(self.frame_b, self._n_ranuras, texto_b)
        self.label_op.configure(text=operacion.operador)

        # Preparar etiquetas del resultado: N ranuras con espacios, colores posicionales
        self._labels_resultado = self._crear_etiquetas_numero(
            self.frame_result, self._n_ranuras, " " * self._n_ranuras
        )

        # Posicionar la línea: anclada a la derecha, relwidth = ancho_chars / N
        if self._n_ranuras > 0:
            relwidth = ancho_chars / self._n_ranuras
            self.frame_linea.place(relx=1.0, rely=0, anchor="ne", relwidth=relwidth, relheight=1)

    def mostrar_resultado(self):
        """Revela el resultado actualizando las etiquetas pre-creadas (sin cambiar tamaño)."""
        resultado_str = str(self.operacion_actual.resultado)
        # Alinear a la derecha con N ranuras
        texto = resultado_str.rjust(self._n_ranuras)
        for i, (lbl, ch) in enumerate(zip(self._labels_resultado, texto[::-1])):
            lbl.configure(text=ch)
            # Mantener el color posicional
            lbl.configure(text_color=config.colores_posicionales[i % len(config.colores_posicionales)])

    # ------------------------------------------------------------------
    # Zoom
    # ------------------------------------------------------------------
    def zoom_text(self, event):
        """Aumenta o reduce el tamaño del texto con la rueda del ratón."""
        paso = config.FONT_SIZE_PASO if event.delta > 0 else -config.FONT_SIZE_PASO
        self.font_size = max(config.FONT_SIZE_MIN, min(config.FONT_SIZE_MAX, self.font_size + paso))

        for frame in self.frames_operacion:
            for lbl in frame.winfo_children():
                lbl.configure(font=self._fuente_numeros())

        # También actualizar etiquetas del resultado pre-creadas
        for lbl in self._labels_resultado:
            lbl.configure(font=self._fuente_numeros())

        self.label_op.configure(font=self._fuente_numeros())

    # ------------------------------------------------------------------
    # Auxiliares
    # ------------------------------------------------------------------
    def mostrar_acerca_de(self):
        about_text = (
            f"{__copyright__}\n\n"
            f"Versión: {__version__}\n"
            f"Fecha: {__date__}\n\n"
            "Descripción:\n"
            "Generador de Operaciones con colores posicionales.\n"
            "Permite ajustar el tamaño de fuente con la rueda del ratón.\n\n"
            f"Software libre, publicado bajo licencia {__license__}."
        )
        messagebox.showinfo("Acerca de", about_text)
