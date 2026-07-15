# -*- coding: utf-8 -*-
"""
Falla si algun archivo de texto del repo tiene mojibake (texto doblemente
codificado) o no es UTF-8 valido.

Contexto: el README y los generadores del sitio llegaron a tener texto
decodificado como cp1252 y re-guardado como UTF-8 ("mAs" por "mas", los emoji
rotos). Este check evita que vuelva a colarse en main.

Por que NO se detecta con grep: un patron no-ASCII ('A') puede corromperse al
pasar por el shell y acabar buscando los BYTES del texto SANO (el byte C3 esta
en toda vocal acentuada), dando falsos positivos en archivos correctos. La
deteccion aqui es programatica, por round-trip, sin patrones.

Por que 'sloppy' cp1252: cp1252 deja sin definir los bytes 81/8D/8F/90/9D, y los
emoji los llevan (el selector VS16 U+FE0F -> EF B8 8F). Con cp1252 puro esas
lineas lanzan UnicodeEncodeError y quedarian sin detectar EN SILENCIO.

Uso:
    python scripts/validar_encoding.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXTS = {".md", ".json", ".html", ".py", ".yml", ".yaml", ".jsonc", ".toml",
        ".txt", ".css", ".js"}
SKIP = {".git", "node_modules", ".venv", "venv", "__pycache__", "site", "dist"}

# Tabla sloppy-cp1252: byte -> char (huecos de cp1252 resueltos como latin-1)
_DEC = {}
for _b in range(256):
    try:
        _DEC[_b] = bytes([_b]).decode("cp1252")
    except UnicodeDecodeError:
        _DEC[_b] = chr(_b)
_ENC = {c: b for b, c in _DEC.items()}


def linea_con_mojibake(linea: str) -> bool:
    """True si la linea se puede 'des-corromper', o sea: esta corrupta.

    Una linea sana no sobrevive el round-trip (sus bytes no son UTF-8 valido).
    """
    try:
        arreglada = bytes(_ENC[c] for c in linea).decode("utf-8")
    except (KeyError, UnicodeDecodeError):
        return False
    return arreglada != linea


def main() -> int:
    malos: list[str] = []
    no_utf8: list[str] = []
    revisados = 0

    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for nombre in files:
            if os.path.splitext(nombre)[1].lower() not in EXTS:
                continue
            ruta = os.path.join(base, nombre)
            rel = os.path.relpath(ruta, ROOT).replace("\\", "/")
            try:
                with open(ruta, "rb") as f:
                    texto = f.read().decode("utf-8")
            except UnicodeDecodeError:
                no_utf8.append(rel)
                continue
            revisados += 1
            n = sum(1 for linea in texto.split("\n") if linea_con_mojibake(linea))
            if n:
                malos.append(f"{rel} ({n} líneas)")

    print(f"Archivos revisados: {revisados}")
    if not malos and not no_utf8:
        print("OK: sin mojibake; todo UTF-8 válido.")
        return 0

    for m in malos:
        print(f"ERROR mojibake: {m}")
    for m in no_utf8:
        print(f"ERROR no es UTF-8: {m}")
    print("\nRepara con: python scripts/reparar_encoding.py --fix")
    return 1


if __name__ == "__main__":
    sys.exit(main())
