"""Punto de entrada: `python -m operaciones` o el comando `operaciones`."""

from operaciones import config
from operaciones.gui import OperacionesApp


def main():
    config.aplicar_tema()   # Debe ejecutarse antes de crear la ventana
    app = OperacionesApp()
    app.mainloop()


if __name__ == "__main__":
    main()
