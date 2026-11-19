# Guía para agentes — Generador de Operaciones

App de escritorio en Python (CustomTkinter). Layout `src/`, paquete `operaciones`.

## Mapa: qué archivo tocar
| Quiero cambiar… | Archivo |
|---|---|
| Versión, autor, fecha, licencia | `src/operaciones/__init__.py` |
| Historial de cambios | `CHANGELOG.md` |
| Colores, fuentes, tamaños y zoom, operadores, valores por defecto, tema | `src/operaciones/config.py` |
| Cómo se carga el icono | `src/operaciones/recursos.py` |
| Archivo del icono | `src/operaciones/assets/` |
| Generación de operaciones e interpretación de los campos (sin interfaz) | `src/operaciones/logic.py` |
| Widgets, layout, dibujo de la operación, zoom, eventos | `src/operaciones/gui.py` |
| Arranque de la app | `src/operaciones/__main__.py` |
| Generar el .exe (solo en Windows) | `scripts/build_exe.py` |

## Flujo (operaciones)
Enter / botón → `OperacionesApp.accion_principal`:
1. `logic.normalizar_parametros` corrige lo escrito en los campos (y la GUI lo refleja).
2. `logic.generar_operacion` devuelve un `logic.Operacion(a, b, resultado, operador)`.
3. `dibujar_operacion` lo pinta; el siguiente Enter llama a `mostrar_resultado`.

## Reglas
- `logic.py` es Python puro: **nunca** importar tkinter ni customtkinter (ni en `config.py` ni en `__init__.py` a nivel de módulo).
- `__init__.py` solo contiene el docstring y los metadatos; no importa nada del paquete.
- Sin variables globales: el estado vive en atributos de `OperacionesApp` (`esperando_resultado`, `operacion_actual`, `font_size`).
- Todo valor configurable (colores, límites, textos fijos) va en `config.py`, no en línea.
- No usar widgets temporales ni `update_idletasks()` al dibujar; la línea es un `Frame` con `fill="x"`.
- Las filas usan N = `max_digitos` ranuras fijas; la línea usa `relwidth=ancho/N` anclada a la derecha.
- El contenedor de la línea debe ser transparente (`CTkFrame`). Un `tk.Frame` normal pinta su propio fondo y parece una línea más larga que las cifras.
- `normalizar_parametros` mantiene el valor máximo dentro del rango de las cifras (con 2 y 2 cifras, de 10 a 99); fuera de ese rango pasa al máximo posible.
- No incluir datos personales de contacto (correos, teléfonos) en el código ni en la interfaz.
- Los recursos viven en `src/operaciones/assets/`, dentro del paquete (así viajan en el `.exe`).
- El `.exe` solo se genera en Windows (`python scripts/build_exe.py`).
- Licencia MIT: no añadir textos de «derechos reservados»; si se añade una dependencia, anotar su licencia en `THIRD_PARTY_NOTICES.md`.
- Todo cambio en `logic.py` debe llevar su test en `tests/test_logic.py`.
- Al publicar una versión: actualizar `__version__` y `__date__` en `__init__.py` y añadir su entrada `## [X.Y.Z]` en `CHANGELOG.md` (un test lo comprueba).

## Comandos
- Instalar: `pip install -e ".[dev]"`
- Probar: `pytest`
- Ejecutar: `python run.py`
- Compilar .exe (solo Windows): `python scripts/build_exe.py` (o `--carpeta`)

## Nota
La GUI no tiene tests automáticos; verificarla abriendo la app (generar, revelar resultado, zoom con rueda, cada operador).
