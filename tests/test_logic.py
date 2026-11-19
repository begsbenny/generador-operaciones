"""Pruebas de operaciones.logic (Python puro, no abren ninguna ventana)."""

import pytest

from operaciones import logic
from operaciones.logic import Operacion

REPETICIONES = 500


# --- Utilidades ---------------------------------------------------------

@pytest.mark.parametrize("numero, esperado", [
    (123, "abc"), (987, "ihg"), (105, "a?e"), (0, "?"),
])
def test_numero_a_letras(numero, esperado):
    assert logic.numero_a_letras(numero) == esperado


@pytest.mark.parametrize("texto, defecto, esperado", [
    ("5", 2, 5), ("0", 2, 2), ("-3", 2, 2), ("abc", 2, 2), ("", 2, 2),
])
def test_safe_int(texto, defecto, esperado):
    assert logic.safe_int(texto, defecto) == esperado


@pytest.mark.parametrize("cifras, minimo, maximo", [
    (1, 0, 9), (2, 10, 99), (3, 100, 999),
])
def test_generar_numero_respeta_las_cifras(cifras, minimo, maximo):
    for _ in range(REPETICIONES):
        assert minimo <= logic.generar_numero(cifras) <= maximo


def test_generar_numero_respeta_el_limite():
    for _ in range(REPETICIONES):
        assert 10 <= logic.generar_numero(2, limite=40) <= 40


# --- normalizar_parametros ---------------------------------------------

@pytest.mark.parametrize("c1, c2, lim, op, esperado", [
    ("", "", "", "+", (2, 2, 99)),            # todo vacío: valores por defecto
    ("", "", "999", "+", (3, 3, 999)),        # solo límite: deduce las cifras
    ("", "", "abc", "+", (2, 2, 99)),         # límite inválido
    ("3", "2", "", "+", (3, 2, 999)),         # sin límite: sube al máximo de las cifras
    ("3", "3", "50", "+", (3, 3, 999)),       # límite menor al mínimo posible
    ("2", "2", "50", "+", (2, 2, 50)),        # límite válido: se respeta
    ("abc", "x", "99", "+", (2, 2, 99)),      # cifras inválidas
    ("2", "4", "9999", "÷", (2, 2, 99)),      # división: el divisor no excede al dividendo; el máximo baja a 99
    ("2", "4", "9999", "+", (2, 4, 9999)),    # en otras operaciones sí puede
])
def test_normalizar_parametros(c1, c2, lim, op, esperado):
    assert logic.normalizar_parametros(c1, c2, lim, op) == esperado


@pytest.mark.parametrize("c1, c2, lim, op, esperado", [
    ("2", "2", "999", "+", (2, 2, 99)),       # demasiado grande para 2 cifras: baja a 99
    ("2", "2", "100", "×", (2, 2, 99)),
    ("2", "2", "99", "+", (2, 2, 99)),        # justo el máximo: se mantiene
    ("2", "2", "80", "+", (2, 2, 80)),        # menor pero válido: se mantiene
    ("2", "2", "10", "-", (2, 2, 10)),        # el mínimo de 2 cifras: se mantiene
    ("2", "2", "9", "+", (2, 2, 99)),         # no cabe ningún número de 2 cifras: sube a 99
    ("3", "3", "80", "+", (3, 3, 999)),       # menor que el mínimo de 3 cifras: sube a 999
    ("2", "3", "5000", "+", (2, 3, 999)),     # manda el número con más cifras
    ("3", "2", "500", "+", (3, 2, 500)),
    ("1", "1", "50", "+", (1, 1, 9)),         # una cifra: máximo 9
    ("1", "1", "5", "+", (1, 1, 5)),
    ("1", "1", "", "+", (1, 1, 9)),           # vacío con una cifra: 9 (antes quedaba en 0)
    ("1", "1", "0", "+", (1, 1, 9)),
    ("2", "2", "-5", "+", (2, 2, 99)),        # negativo: inválido
    ("4", "2", "99999", "×", (4, 2, 9999)),
])
def test_normalizar_ajusta_el_valor_maximo_a_las_cifras(c1, c2, lim, op, esperado):
    assert logic.normalizar_parametros(c1, c2, lim, op) == esperado


def test_normalizar_el_maximo_siempre_cabe_en_las_cifras():
    for c1 in range(1, 5):
        for c2 in range(1, 5):
            for lim in ("", "0", "1", "9", "10", "50", "99", "100", "999", "5000", "99999", "abc", "-3"):
                for op in logic.config.OPERADORES:
                    n1, n2, limite = logic.normalizar_parametros(str(c1), str(c2), lim, op)
                    m = max(n1, n2)
                    minimo = 10 ** (m - 1) if m > 1 else 1
                    assert minimo <= limite <= 10 ** m - 1, (c1, c2, lim, op, n1, n2, limite)


def test_normalizar_ignora_espacios():
    assert logic.normalizar_parametros(" 3 ", " 2 ", " 500 ", "+") == (3, 2, 500)


# --- generar_operacion --------------------------------------------------

def test_suma():
    for _ in range(REPETICIONES):
        op = logic.generar_operacion(2, 2, 99, "+")
        assert op.operador == "+" and op.resultado == op.a + op.b
        assert 10 <= op.a <= 99 and 10 <= op.b <= 99


def test_resta_nunca_da_negativo():
    for _ in range(REPETICIONES):
        op = logic.generar_operacion(2, 2, 99, "-")
        assert op.operador == "-" and op.a >= op.b
        assert op.resultado == op.a - op.b >= 0


def test_multiplicacion():
    for _ in range(REPETICIONES):
        op = logic.generar_operacion(2, 1, 99, "×")
        assert op.operador == "×" and op.resultado == op.a * op.b


@pytest.mark.parametrize("c1, c2, limite", [(2, 1, 99), (2, 2, 99), (3, 2, 999), (1, 1, 9), (2, 2, 50)])
def test_division_exacta_y_dentro_de_rango(c1, c2, limite):
    for _ in range(REPETICIONES):
        op = logic.generar_operacion(c1, c2, limite, "÷")
        assert op.operador == "÷"
        assert op.b != 0 and op.a == op.b * op.resultado       # exacta
        assert op.a <= limite                                   # dentro del límite
        assert op.a >= (10 ** (c1 - 1) if c1 > 1 else 0)        # con las cifras pedidas
        assert op.b >= (10 ** (c2 - 1) if c2 > 1 else 1)


def test_operador_desconocido_se_trata_como_suma():
    op = logic.generar_operacion(2, 2, 99, "?")
    assert op.operador == "+" and op.resultado == op.a + op.b


def test_valores_no_positivos_usan_los_por_defecto():
    op = logic.generar_operacion(0, -1, 0, "+")
    assert 10 <= op.a <= 99 and 10 <= op.b <= 99


def test_division_imposible_falla_en_vez_de_colgarse(monkeypatch):
    monkeypatch.setattr(logic, "MAX_INTENTOS_DIVISION", 50)
    # dividendo de 3 cifras con límite 99: no existe ninguno
    with pytest.raises(ValueError):
        logic.generar_operacion(3, 1, 99, "÷")


# --- alinear_operandos --------------------------------------------------

def test_alinear_operandos_usa_el_ancho_del_mayor():
    assert logic.alinear_operandos(Operacion(5, 12, 60, "×")) == (" 5", "12", 2)
    assert logic.alinear_operandos(Operacion(99, 99, 198, "+")) == (" 99", " 99", 3)


# --- max_digitos --------------------------------------------------------

@pytest.mark.parametrize("c1, c2, limite, op, esperado", [
    # Suma: max_a + max_b
    (2, 2, 99, "+", 3),      # 99 + 99 = 198 (3 dígitos)
    (1, 1, 9, "+", 2),       # 9 + 9 = 18 (2 dígitos)
    (3, 2, 999, "+", 4),     # 999 + 99 = 1098 (4 dígitos)
    (2, 2, 50, "+", 3),      # 50 + 50 = 100 (3 dígitos)
    # Resta: max(max_a, max_b)
    (2, 2, 99, "-", 2),      # max(99, 99) = 99 (2 dígitos)
    (3, 2, 999, "-", 3),     # max(999, 99) = 999 (3 dígitos)
    (1, 1, 9, "-", 1),       # max(9, 9) = 9 (1 dígito)
    # Multiplicación: max_a * max_b
    (2, 2, 99, "×", 4),      # 99 * 99 = 9801 (4 dígitos)
    (1, 1, 9, "×", 2),       # 9 * 9 = 81 (2 dígitos)
    (3, 2, 999, "×", 5),     # 999 * 99 = 98901 (5 dígitos)
    (2, 1, 99, "×", 3),      # 99 * 9 = 891 (3 dígitos)
    # División: max_a (dividendo)
    (2, 1, 99, "÷", 2),      # max_a = 99 (2 dígitos)
    (3, 2, 999, "÷", 3),     # max_a = 999 (3 dígitos)
    (1, 1, 9, "÷", 1),       # max_a = 9 (1 dígito)
    # Operador desconocido = suma
    (2, 2, 99, "?", 3),      # 99 + 99 = 198 (3 dígitos)
    # Límite menor que el máximo de cifras
    (2, 2, 50, "+", 3),      # max_a=50, max_b=50 -> 100 (3 dígitos)
    (2, 2, 50, "×", 4),      # 50 * 50 = 2500 (4 dígitos)
])
def test_max_digitos(c1, c2, limite, op, esperado):
    assert logic.max_digitos(c1, c2, limite, op) == esperado


def test_max_digitos_respeta_limite_por_defecto():
    # límite <= 0 usa LIMITE_POR_DEFECTO (99)
    assert logic.max_digitos(2, 2, 0, "+") == 3
    assert logic.max_digitos(2, 2, -5, "+") == 3


# --- Propiedad: max_digitos cubre todas las operaciones generadas ---------

@pytest.mark.parametrize("c1, c2, limite, op", [
    (2, 2, 99, "+"),
    (2, 2, 99, "-"),
    (2, 1, 99, "×"),
    (3, 2, 999, "÷"),
    (1, 1, 9, "+"),
    (2, 2, 50, "+"),
    (2, 2, 50, "×"),
])
def test_max_digitos_cubre_todas_las_operaciones(c1, c2, limite, op):
    N = logic.max_digitos(c1, c2, limite, op)
    for _ in range(500):
        op_obj = logic.generar_operacion(c1, c2, limite, op)
        assert len(str(op_obj.a)) <= N
        assert len(str(op_obj.b)) <= N
        assert len(str(op_obj.resultado)) <= N


# --- Pureza -------------------------------------------------------------

def test_logic_no_depende_de_librerias_visuales():
    import sys
    assert "tkinter" not in sys.modules
    assert "customtkinter" not in sys.modules
