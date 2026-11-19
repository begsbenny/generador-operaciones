"""Recursos incluidos con el programa: icono de la ventana.

Las librerías gráficas no se importan aquí, así este módulo se puede importar sin ellas.
"""

from pathlib import Path

from operaciones import config

# Funciona igual en desarrollo y dentro del .exe de PyInstaller
RUTA_ASSETS = Path(__file__).resolve().parent / "assets"


def aplicar_icono(ventana):
    """Pone el icono del programa en la ventana (barra de título y barra de tareas)."""
    ruta = RUTA_ASSETS / config.ARCHIVO_ICONO

    def poner():
        try:
            ventana.iconbitmap(str(ruta))
        except Exception:
            pass   # sistemas sin soporte de .ico: se deja el icono por defecto

    # CustomTkinter pone su propio icono unos 200 ms después de abrir la ventana: se reemplaza justo después
    ventana.after(300, poner)
