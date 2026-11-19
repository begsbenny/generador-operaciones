"""Pruebas de los recursos incluidos: icono y empaquetado."""

import struct
from pathlib import Path

from operaciones import config

RAIZ = Path(__file__).resolve().parents[1]          # No depende de la carpeta desde la que se ejecute pytest
ASSETS = RAIZ / "src" / "operaciones" / "assets"
PATRONES_PAQUETE = ("assets/*",)


def test_los_avisos_de_terceros_incluyen_customtkinter():
    avisos = (RAIZ / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    assert "CustomTkinter" in avisos and "MIT" in avisos


def test_el_icono_es_un_ico_valido_con_los_tamanos_necesarios():
    datos = (ASSETS / config.ARCHIVO_ICONO).read_bytes()
    reservado, tipo, cantidad = struct.unpack("<HHH", datos[:6])
    assert (reservado, tipo) == (0, 1)                       # firma de un archivo .ico
    tamanos = {datos[6 + 16 * i] or 256 for i in range(cantidad)}
    assert {16, 32, 48, 256} <= tamanos


def test_los_datos_del_paquete_incluyen_los_recursos():
    pyproject = (RAIZ / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.setuptools.package-data]" in pyproject
    for patron in PATRONES_PAQUETE:
        assert f'"{patron}"' in pyproject


def test_el_script_del_ejecutable_incluye_icono_y_recursos():
    script = (RAIZ / "scripts" / "build_exe.py").read_text(encoding="utf-8")
    assert "--icon" in script and "--add-data" in script
    assert "LICENSE" in script and "THIRD_PARTY_NOTICES.md" in script
