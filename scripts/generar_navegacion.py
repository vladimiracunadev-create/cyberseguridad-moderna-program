# -*- coding: utf-8 -*-
"""
Genera la navegacion hacia atras ("## ⬅️ Clase anterior") en cada clase, de forma
que el programa se pueda recorrer en los DOS sentidos.

La numeracion de clases es GLOBAL (001→340) y cruza las partes: la anterior a la
026 (Parte 1) es la 025 (Parte 0). Por eso el orden se calcula sobre el numero de
clase, no por carpeta.

Convenciones que respeta (ya existentes en el repo):
  - La seccion "## ➡️ Siguiente clase" se mantiene tal cual; esta solo se inserta
    justo ANTES.
  - El texto del enlace se toma del H1 real del README destino (fuente de verdad,
    con sus tildes), no del slug de la carpeta.
  - Los extremos enlazan al indice del programa, igual que ya hace la clase 340.

Es idempotente: si la seccion ya existe, se reescribe con el valor correcto. Se
puede re-ejecutar cada vez que se anadan o reordenen clases.

Uso:
    python scripts/generar_navegacion.py           # aplica
    python scripts/generar_navegacion.py --check   # no escribe; falla si hay drift (CI)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = os.path.join(ROOT, "classes")

SEC_ANTERIOR = "## ⬅️ Clase anterior"
SEC_SIGUIENTE = "## ➡️ Siguiente clase"
VOLVER_INDICE = "[Volver al índice del programa](../../README.md)"


def clases_ordenadas():
    """Devuelve [(num, parte_dir, clase_dir)] ordenado por numero global de clase."""
    out = []
    for parte in sorted(os.listdir(CLASSES)):
        pdir = os.path.join(CLASSES, parte)
        if not (os.path.isdir(pdir) and parte.startswith("parte-")):
            continue
        for clase in sorted(os.listdir(pdir)):
            cdir = os.path.join(pdir, clase)
            if not os.path.isdir(cdir):
                continue
            m = re.match(r"^(\d{3})-", clase)
            if m and os.path.isfile(os.path.join(cdir, "README.md")):
                out.append((int(m.group(1)), parte, clase))
    out.sort(key=lambda t: t[0])
    return out


def titulo_de(parte, clase):
    """Texto del enlace = H1 del README destino, sin el '# '."""
    ruta = os.path.join(CLASSES, parte, clase, "README.md")
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            if linea.startswith("# "):
                return linea[2:].strip()
    return clase


def ruta_relativa(parte_origen, parte_destino, clase_destino):
    if parte_origen == parte_destino:
        return f"../{clase_destino}/README.md"
    return f"../../{parte_destino}/{clase_destino}/README.md"


def enlace_a(parte_origen, vecino):
    """Enlace al README de la clase vecina, o al indice si no hay vecina (extremos)."""
    if vecino is None:
        return VOLVER_INDICE
    _, p_vec, c_vec = vecino
    rel = ruta_relativa(parte_origen, p_vec, c_vec)
    return f"[{titulo_de(p_vec, c_vec)}]({rel})"


def bloque(seccion, parte_origen, vecino):
    return f"{seccion}\n\n{enlace_a(parte_origen, vecino)}\n\n"


def main():
    check = "--check" in sys.argv
    clases = clases_ordenadas()
    if not clases:
        print("ERROR: no se encontraron clases")
        return 1

    cambiados, drift = 0, []
    for i, (num, parte, clase) in enumerate(clases):
        ruta = os.path.join(CLASSES, parte, clase, "README.md")
        with open(ruta, encoding="utf-8") as f:
            txt = f.read()

        if SEC_SIGUIENTE not in txt:
            print(f"ERROR: {parte}/{clase} no tiene '{SEC_SIGUIENTE}'")
            return 1

        anterior = clases[i - 1] if i > 0 else None
        siguiente = clases[i + 1] if i < len(clases) - 1 else None

        # Quita la seccion "anterior" previa (idempotencia) antes de reinsertarla.
        nuevo = re.sub(
            re.escape(SEC_ANTERIOR) + r"\n\n.*?\n\n(?=" + re.escape(SEC_SIGUIENTE) + ")",
            "",
            txt,
            flags=re.DOTALL,
        )
        # Reescribe "Siguiente" completa: su enlace tambien se deriva del H1 destino,
        # asi ambos sentidos usan la misma fuente de verdad y no divergen.
        nuevo = re.sub(
            re.escape(SEC_SIGUIENTE) + r"\n\n.*?(?=\n\n|\Z)",
            (bloque(SEC_ANTERIOR, parte, anterior)
             + bloque(SEC_SIGUIENTE, parte, siguiente)).rstrip("\n"),
            nuevo,
            count=1,
            flags=re.DOTALL,
        )
        nuevo = nuevo.rstrip("\n") + "\n"

        if nuevo != txt:
            cambiados += 1
            drift.append(f"{parte}/{clase}")
            if not check:
                with open(ruta, "w", encoding="utf-8", newline="\n") as f:
                    f.write(nuevo)

    if check:
        if drift:
            print(f"DRIFT: {len(drift)} clases con navegación desactualizada:")
            for d in drift[:10]:
                print(f"  - {d}")
            if len(drift) > 10:
                print(f"  ... y {len(drift) - 10} más")
            print("Ejecuta: python scripts/generar_navegacion.py")
            return 1
        print(f"OK: navegación bidireccional coherente en {len(clases)} clases.")
        return 0

    print(f"Navegación generada: {cambiados} clases actualizadas de {len(clases)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
