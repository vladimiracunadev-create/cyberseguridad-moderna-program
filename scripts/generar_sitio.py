#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera un sitio estático (site/) a partir de los Markdown del repositorio,
para publicarlo en GitHub Pages. Renderiza el README raíz, el índice de
clases, los README de parte y los 310 README de clase a HTML, reescribiendo
los enlaces internos .md -> .html para que la navegación funcione en el sitio.

Uso:  python scripts/generar_sitio.py
Salida: carpeta site/ con index.html y el árbol de clases en HTML.
Requiere: pip install "markdown>=3.6"
"""
from __future__ import annotations
import os
import re
import shutil

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")

# Markdown de origen que se publican (rutas relativas al repo).
INCLUIR_TOP = ["README.md", "ROADMAP.md", "CONTRIBUTING.md", "SECURITY.md",
               "rutas/README.md", "autoevaluaciones/README.md", "labs/README.md",
               "ctf/README.md"]

LINK_MD = re.compile(r"\]\(([^)]+?)\.md((?:#[^)]*)?)\)")

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Ciberseguridad Moderna</title>
<style>
  :root {{ color-scheme: light dark; }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.65; max-width: 900px; margin: 0 auto; padding: 2rem 1.2rem 5rem;
    color: #1b1f24; background: #ffffff;
  }}
  @media (prefers-color-scheme: dark) {{
    body {{ color: #e6edf3; background: #0d1117; }}
    a {{ color: #6cb6ff; }}
    code, pre {{ background: #161b22 !important; }}
    table, th, td {{ border-color: #30363d !important; }}
    thead th {{ background: #161b22 !important; }}
  }}
  a {{ color: #0969da; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  h1, h2, h3 {{ line-height: 1.25; }}
  h1 {{ border-bottom: 1px solid #d0d7de; padding-bottom: .3em; }}
  h2 {{ border-bottom: 1px solid #d0d7de; padding-bottom: .2em; margin-top: 2rem; }}
  code {{ background: #f2f4f6; padding: .15em .35em; border-radius: 5px; font-size: .9em; }}
  pre {{ background: #f2f4f6; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
  pre code {{ background: transparent; padding: 0; }}
  table {{ border-collapse: collapse; width: 100%; overflow-x: auto; display: block; }}
  th, td {{ border: 1px solid #d0d7de; padding: .5em .75em; text-align: left; }}
  thead th {{ background: #f2f4f6; }}
  blockquote {{ border-left: 4px solid #d0d7de; margin: 1rem 0; padding: .2rem 1rem; color: inherit; opacity: .9; }}
  .nav {{ font-size: .9rem; margin-bottom: 1.5rem; opacity: .85; }}
</style>
</head>
<body>
<div class="nav"><a href="{home}">🛡️ Inicio</a> · <a href="{indice}">📚 Clases</a> · <a href="{rutas}">🧭 Rutas</a> · <a href="{quiz}">📝 Autoevaluación</a> · <a href="{progreso}">✅ Progreso</a></div>
{body}
</body>
</html>
"""


def reescribir_enlaces(texto: str) -> str:
    """Convierte enlaces internos ...algo.md(#anchor) en ...algo.html(#anchor)."""
    return LINK_MD.sub(lambda m: f"]({m.group(1)}.html{m.group(2)})", texto)


def render(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
    )


def profundidad(rel: str) -> int:
    return rel.replace("\\", "/").count("/")


def escribir(rel_md: str, md_text: str) -> None:
    rel_html = rel_md[:-3] + ".html"
    destino = os.path.join(OUT, rel_html)
    os.makedirs(os.path.dirname(destino) or OUT, exist_ok=True)
    prof = profundidad(rel_html)
    subir = "../" * prof
    title = "Programa de Ciberseguridad Moderna"
    m = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    if m:
        title = re.sub(r"[#*`]", "", m.group(1)).strip()
    html = PLANTILLA.format(
        title=title,
        home=f"{subir}index.html" if prof else "index.html",
        indice=f"{subir}classes/README.html" if prof else "classes/README.html",
        rutas=f"{subir}rutas/README.html" if prof else "rutas/README.html",
        quiz=f"{subir}autoevaluaciones/quiz.html" if prof else "autoevaluaciones/quiz.html",
        progreso=f"{subir}autoevaluaciones/progreso.html" if prof else "autoevaluaciones/progreso.html",
        body=render(reescribir_enlaces(md_text)),
    )
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)


def main() -> int:
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    generados = 0

    # Documentos del nivel superior.
    for rel in INCLUIR_TOP:
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            escribir(rel, open(p, encoding="utf-8").read())
            generados += 1

    # Todo el árbol de classes/.
    for cur, _, files in os.walk(os.path.join(ROOT, "classes")):
        for fn in files:
            if fn.endswith(".md"):
                p = os.path.join(cur, fn)
                rel = os.path.relpath(p, ROOT).replace("\\", "/")
                escribir(rel, open(p, encoding="utf-8").read())
                generados += 1

    # index.html del sitio = README raíz renderizado.
    shutil.copyfile(os.path.join(OUT, "README.html"), os.path.join(OUT, "index.html"))

    # Páginas interactivas del portal (quiz + progreso), ya autocontenidas.
    destino_auto = os.path.join(OUT, "autoevaluaciones")
    os.makedirs(destino_auto, exist_ok=True)
    for nombre in ("quiz.html", "progreso.html"):
        origen = os.path.join(ROOT, "autoevaluaciones", nombre)
        if os.path.isfile(origen):
            shutil.copyfile(origen, os.path.join(destino_auto, nombre))
            generados += 1

    # .nojekyll para que Pages no ignore archivos con nombres especiales.
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    print(f"Sitio generado en site/  ({generados} páginas HTML + index.html)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
