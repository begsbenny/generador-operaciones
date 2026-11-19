"""Configuración del Generador de Operaciones: constantes, colores, tema y valores por defecto.

Los metadatos (versión, autor, fecha) están en operaciones/__init__.py
y el historial de cambios en CHANGELOG.md.
"""

# --- Tema de CustomTkinter ---
APARIENCIA = "dark"      # "dark" o "light"
TEMA_COLOR = "blue"      # "blue", "green", "dark-blue"


def aplicar_tema():
    """Aplica el tema de CustomTkinter. Llamar antes de crear la ventana.

    customtkinter se importa aquí (y no arriba) para que este módulo, y por
    tanto logic.py y los tests, no dependan de ninguna librería visual.
    """
    import customtkinter as ctk

    ctk.set_appearance_mode(APARIENCIA)
    ctk.set_default_color_theme(TEMA_COLOR)


# --- Ventana ---
ARCHIVO_ICONO = "icon.ico"   # En assets/; se usa en la ventana y en el ejecutable
VENTANA_ALTO = 520

# --- Texto / zoom ---
FONT_FAMILY = "Courier"
FONT_FAMILY_OPERADOR = "Arial Black"   # Solo el operador al inicio; el zoom lo pasa a FONT_FAMILY
FONT_SIZE_INICIAL = 72
FONT_SIZE_MIN = 24
FONT_SIZE_MAX = 220
FONT_SIZE_PASO = 8

# --- Generación ---
OPERADORES = ("+", "-", "×", "÷")
CIFRAS_POR_DEFECTO = 2
LIMITE_POR_DEFECTO = 99

# --- Colores posicionales (unidades, decenas, centenas...) ---
colores_posicionales = ["#0074D9", "#FF4136", "#2ECC40"]  # Azul, Rojo, Verde

# --- Canvas y línea de la operación ---
CANVAS_BG = "#2b2b2b"
COLOR_LINEA = "#DCE4EE"        # Gris muy claro: visible en modo oscuro
LINEA_GROSOR = 3

# --- Cuadrículas decorativas (tic-tac-toe con letras a-i) ---
TICTACTOE_LETRAS = tuple("abcdefghi")
TICTACTOE_TAM = 60
TICTACTOE_COLOR_LINEA = "#555555"
TICTACTOE_COLOR_LETRA = "#606060"
COLOR_LETRAS_RESULTADO = "#555555"   # Letras junto al botón Generar
