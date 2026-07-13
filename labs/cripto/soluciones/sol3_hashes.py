# -*- coding: utf-8 -*-
"""Solución Reto 3 — cracking de hashes MD5 sin sal con diccionario."""
import hashlib
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "retos")


def main() -> None:
    hashes = [h.strip() for h in open(os.path.join(BASE, "reto3_hashes.txt"), encoding="utf-8") if h.strip()]
    palabras = [p.strip() for p in open(os.path.join(BASE, "diccionario.txt"), encoding="utf-8") if p.strip()]
    tabla = {hashlib.md5(p.encode()).hexdigest(): p for p in palabras}
    for h in hashes:
        print(f"{h} -> {tabla.get(h, '[NO ENCONTRADO]')}")
    print("\n[i] Moraleja: MD5 sin sal + contraseñas débiles = crackeo instantáneo. Usa Argon2/bcrypt.")


if __name__ == "__main__":
    main()
