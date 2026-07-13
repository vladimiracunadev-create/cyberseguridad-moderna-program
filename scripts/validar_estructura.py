#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Valida la integridad del currículo del Programa de Ciberseguridad Moderna.

Comprueba:
  1. Cada parte (classes/parte-*/) tiene su README.md.
  2. Cada carpeta de clase (classes/parte-*/NNN-slug/) tiene su README.md no trivial.
  3. La numeración de clases es secuencial y sin huecos (001..N).
  4. Todos los enlaces internos a archivos .md resuelven (no hay enlaces rotos).

Uso:  python scripts/validar_estructura.py
Salida: código 0 si todo está bien; 1 si hay errores (para CI).
"""
from __future__ import annotations
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = os.path.join(ROOT, "classes")
MIN_BYTES = 400  # un README real es mucho mayor; esto detecta stubs vacíos
LINK_RE = re.compile(r"\]\((\.\.?/[^)]+\.md)\)")

# Secciones que TODA clase debe incluir (robustez pedagógica).
SECCIONES_REQUERIDAS = [
    "## 🎯 Objetivo",
    "## 📚 Resultados de aprendizaje",
    "## ⚠️ Errores comunes",
    "## ❓ Preguntas frecuentes",
    "## 🔗 Referencias",
    "## ➡️ Siguiente clase",
]


def main() -> int:
    errores: list[str] = []
    nums: list[int] = []
    n_partes = 0
    n_clases = 0

    if not os.path.isdir(CLASSES):
        print("ERROR: no existe el directorio classes/")
        return 1

    for parte in sorted(os.listdir(CLASSES)):
        pdir = os.path.join(CLASSES, parte)
        if not (os.path.isdir(pdir) and parte.startswith("parte-")):
            continue
        n_partes += 1
        if not os.path.isfile(os.path.join(pdir, "README.md")):
            errores.append(f"Falta README de parte: {parte}/README.md")

        for clase in sorted(os.listdir(pdir)):
            cdir = os.path.join(pdir, clase)
            if not os.path.isdir(cdir):
                continue
            n_clases += 1
            m = re.match(r"^(\d{3})-", clase)
            if m:
                nums.append(int(m.group(1)))
            readme = os.path.join(cdir, "README.md")
            if not os.path.isfile(readme):
                errores.append(f"Falta README de clase: {parte}/{clase}/README.md")
            elif os.path.getsize(readme) < MIN_BYTES:
                errores.append(f"README demasiado corto (<{MIN_BYTES} B): {parte}/{clase}/README.md")
            else:
                contenido = open(readme, encoding="utf-8").read()
                faltan = [s for s in SECCIONES_REQUERIDAS if s not in contenido]
                if faltan:
                    errores.append(
                        f"Secciones faltantes en {parte}/{clase}/README.md: "
                        + ", ".join(f'"{s}"' for s in faltan)
                    )

    # numeración secuencial
    nums.sort()
    if nums:
        esperado = list(range(1, len(nums) + 1))
        if nums != esperado:
            faltan = sorted(set(esperado) - set(nums))
            dup = sorted({x for x in nums if nums.count(x) > 1})
            if faltan:
                errores.append(f"Huecos en la numeracion de clases: {faltan}")
            if dup:
                errores.append(f"Numeros de clase duplicados: {dup}")

    # enlaces internos .md
    enlaces = 0
    rotos = 0
    for cur, _, files in os.walk(CLASSES):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(cur, fn)
            with open(p, encoding="utf-8") as fh:
                txt = fh.read()
            for mm in LINK_RE.finditer(txt):
                enlaces += 1
                tgt = os.path.normpath(os.path.join(cur, mm.group(1)))
                if not os.path.exists(tgt):
                    rotos += 1
                    errores.append(f"Enlace roto en {os.path.relpath(p, ROOT)} -> {mm.group(1)}")

    print("== Validacion del Programa de Ciberseguridad Moderna ==")
    print(f"Partes encontradas : {n_partes}")
    print(f"Clases encontradas : {n_clases}")
    print(f"Enlaces .md revisados: {enlaces} (rotos: {rotos})")

    if errores:
        print(f"\nFALLO: {len(errores)} problema(s):")
        for e in errores[:50]:
            print(f"  - {e}")
        if len(errores) > 50:
            print(f"  ... y {len(errores) - 50} mas")
        return 1

    print("\nOK: estructura y enlaces integros.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
