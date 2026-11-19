# Historial de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).
Las versiones siguen [SemVer](https://semver.org/lang/es/).

## [1.1.1] - 2026-11-19

### Cambiado
- Valores por defecto ajustados.
- Código reorganizado como paquete (`src/operaciones/`) con `config`, `logic`, `gui` (clase `OperacionesApp`) y arranque, sin variables globales.
- Versión, autor y fecha pasan a `operaciones/__init__.py`; el historial, a este archivo.
- Se quitó el correo de contacto de la ventana «Acerca de», que ahora indica la licencia.
- El autor figura con su nombre completo (Benny Ronaldo Rojas Villadeza).
- El programa pasa a llamarse «Generador de Operaciones».
- La generación de divisiones tiene un tope de intentos: si los parámetros no permiten ninguna división exacta, falla con un error en lugar de bloquear el programa.
- El valor máximo se ajusta al rango que permiten las cifras elegidas: con 2 y 2 cifras es como máximo 99 y un valor menor y válido (por ejemplo 80) se respeta. Con una cifra y el campo vacío queda en 9, no en 0.

### Corregido
- Parpadeos visuales al generar una operación (ceros temporales, signo y línea).
- El conjunto ya no se desplaza lateralmente cuando cambia la cantidad de cifras del resultado.
- La raya bajo los operandos ya no se ve más larga que la fila más ancha: su contenedor pintaba un fondo propio.

### Añadido
- Icono de la aplicación, en la ventana y en el ejecutable.
- Pruebas automáticas con pytest.
- Licencia MIT (`LICENSE`) y avisos de licencias de terceros (`THIRD_PARTY_NOTICES.md`).
- Script para generar el ejecutable en Windows (`scripts/build_exe.py`), README y AGENTS.md.

## [1.1.0] - 2026-11-06

### Cambiado
- Migración a CustomTkinter: interfaz moderna con bordes redondeados y tema visual agradable.

## [1.0.0] - 2025-10-24

### Añadido
- Versión inicial estable: generador de operaciones.
- Colores posicionales (unidades, decenas, centenas).
- Zoom dinámico con la rueda del ratón.
