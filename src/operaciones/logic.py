"""Lógica pura del Generador de Operaciones.

Este módulo no depende de tkinter ni de CustomTkinter: solo calcula números
y textos. La interfaz se encarga de dibujarlos.
"""

import math
import random
from dataclasses import dataclass

from operaciones import config

MAX_INTENTOS_DIVISION = 10_000   # Tope de seguridad para no quedar en un bucle infinito


@dataclass(frozen=True)
class Operacion:
    """Una operación ya resuelta. En '÷', `a` es el dividendo y `resultado` el cociente."""
    a: int
    b: int
    resultado: int
    operador: str


# ----------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------
def numero_a_letras(num):
    """Convierte cada dígito 1-9 en a-i ('?' para el 0 u otro carácter)."""
    mapa = {str(i): chr(96 + i) for i in range(1, 10)}
    return "".join(mapa.get(ch, "?") for ch in str(num))


def safe_int(s, default):
    """Convierte a entero positivo; devuelve `default` si no es válido o es <= 0."""
    try:
        v = int(s)
        return v if v > 0 else default
    except ValueError:
        return default


def _positivo(valor, defecto):
    return valor if valor > 0 else defecto


def generar_numero(cifras, limite=None):
    """Número aleatorio con exactamente `cifras` cifras (1 cifra incluye el 0), hasta `limite`."""
    low = 10 ** (cifras - 1) if cifras > 1 else 0
    high = min(10 ** cifras - 1, limite or 10 ** cifras - 1)
    return random.randint(low, high)


# ----------------------------------------------------------------------
# Parámetros de entrada
# ----------------------------------------------------------------------
def normalizar_parametros(raw_cifras1, raw_cifras2, raw_limite, operador):
    """Convierte lo escrito en los campos en valores coherentes.

    Devuelve (cifras1, cifras2, limite) ya corregidos para mostrar en la interfaz:
    - Campos vacíos o inválidos toman valores por defecto.
    - Solo con límite: las cifras se deducen de él.
    - En división, el divisor no puede tener más cifras que el dividendo.
    - El límite se mantiene dentro del rango que permiten las cifras (con 2 y 2 cifras, de 10 a 99);
      fuera de ese rango pasa al máximo de esas cifras.
    """
    c1, c2, lim = raw_cifras1.strip(), raw_cifras2.strip(), raw_limite.strip()

    if not c1 and not c2 and not lim:
        cifras1 = cifras2 = config.CIFRAS_POR_DEFECTO
        limite = config.LIMITE_POR_DEFECTO
    elif not c1 and not c2 and lim:
        try:
            limite = int(lim)
        except ValueError:
            limite = config.LIMITE_POR_DEFECTO
        cifras1 = cifras2 = len(str(limite))
    else:
        cifras1 = safe_int(c1, config.CIFRAS_POR_DEFECTO)
        cifras2 = safe_int(c2, config.CIFRAS_POR_DEFECTO)
        limite = safe_int(lim, 0)

    if operador == "÷" and cifras2 > cifras1:
        cifras2 = cifras1

    # El valor máximo debe caber en las cifras elegidas: con 2 y 2 cifras, entre 10 y 99.
    # Si está fuera de ese rango (vacío, inválido, demasiado pequeño o demasiado grande) pasa
    # al máximo posible; un valor dentro del rango (por ejemplo 80) se respeta.
    max_cifras = max(cifras1, cifras2)
    maximo_posible = 10 ** max_cifras - 1
    minimo = 10 ** (max_cifras - 1) if max_cifras > 1 else 1
    if limite < minimo or limite > maximo_posible:
        limite = maximo_posible

    return cifras1, cifras2, limite


# ----------------------------------------------------------------------
# Generación de operaciones
# ----------------------------------------------------------------------
def _generar_division(cifras1, cifras2, limite):
    """División exacta: elige el divisor y luego un cociente que mantenga el dividendo en rango."""
    low_a = 10 ** (cifras1 - 1) if cifras1 > 1 else 0
    high_a = min(10 ** cifras1 - 1, limite)
    low_b = 10 ** (cifras2 - 1) if cifras2 > 1 else 1
    high_b = min(10 ** cifras2 - 1, limite)

    for _ in range(MAX_INTENTOS_DIVISION):
        b = random.randint(low_b, high_b)
        if b == 0:
            continue
        min_q = math.ceil(low_a / b)
        max_q = high_a // b
        if min_q <= max_q:
            q = random.randint(min_q, max_q)
            return Operacion(a=b * q, b=b, resultado=q, operador="÷")
    raise ValueError("No se pudo generar una división exacta con esos parámetros.")


def generar_operacion(cifras1, cifras2, limite, operador):
    """Genera una operación aleatoria y devuelve su resultado.

    Un operador desconocido se trata como suma. En la resta, el mayor va arriba.
    """
    cifras1 = _positivo(cifras1, config.CIFRAS_POR_DEFECTO)
    cifras2 = _positivo(cifras2, config.CIFRAS_POR_DEFECTO)
    limite = _positivo(limite, config.LIMITE_POR_DEFECTO)

    if operador == "÷":
        return _generar_division(cifras1, cifras2, limite)

    a = generar_numero(cifras1, limite)
    b = generar_numero(cifras2, limite)

    if operador == "-":
        if b > a:
            a, b = b, a
        return Operacion(a, b, a - b, "-")
    if operador == "×":
        return Operacion(a, b, a * b, "×")
    return Operacion(a, b, a + b, "+")


# ----------------------------------------------------------------------
# Presentación (texto plano)
# ----------------------------------------------------------------------
def max_digitos(cifras1, cifras2, limite, operador):
    """Máxima cantidad de cifras que puede tener cualquier fila (operando o resultado)
    con los parámetros ya normalizados. Mismos topes que generar_operacion.
    """
    # Aplicar los mismos topes que generar_operacion
    limite = _positivo(limite, config.LIMITE_POR_DEFECTO)

    # Máximo valor para cada operando según sus cifras y el límite
    max_a = min(10 ** cifras1 - 1, limite)
    max_b = min(10 ** cifras2 - 1, limite)

    if operador == "+":
        max_res = max_a + max_b
    elif operador == "-":
        max_res = max(max_a, max_b)
    elif operador == "×":
        max_res = max_a * max_b
    elif operador == "÷":
        max_res = max_a  # El dividendo máximo
    else:
        max_res = max_a + max_b  # Operador desconocido = suma

    # El máximo de dígitos entre a, b y resultado
    return max(len(str(max_a)), len(str(max_b)), len(str(max_res)))


def alinear_operandos(op):
    """Alinea a la derecha los dos operandos. Devuelve (texto_a, texto_b, ancho).

    `ancho` es el largo máximo entre a, b y el resultado (sirve para dimensionar la línea).
    """
    ancho = max(len(str(op.a)), len(str(op.b)), len(str(op.resultado)))
    return str(op.a).rjust(ancho), str(op.b).rjust(ancho), ancho
