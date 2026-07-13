# -*- coding: utf-8 -*-
"""
Genera, POR PARTE, el material descargable de cada clase:
  - una guía en PDF (render del README vía Microsoft Edge headless)
  - una presentación PPTX (python-pptx) resumida por secciones
y añade a cada README una sección "📥 Material descargable" con los enlaces.

Uso:  python scripts/generar_material.py <indice_de_parte>     # p. ej. 0, 1, 2 ...
      python scripts/generar_material.py <idx> --solo-una      # solo la 1ª clase (prueba)

Requisitos: python-pptx, markdown, y Microsoft Edge (o Chrome) instalado.
"""
from __future__ import annotations
import glob
import html as htmllib
import os
import re
import subprocess
import sys
import tempfile

import markdown
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = os.path.join(ROOT, "classes")

NAVEGADORES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def navegador() -> str:
    for p in NAVEGADORES:
        if os.path.isfile(p):
            return p
    raise SystemExit("No se encontró Edge ni Chrome para generar PDFs.")


CSS = """
@page { size: A4; margin: 16mm 15mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.5; color: #14181d; }
h1 { font-size: 20pt; color: #0b3d2e; border-bottom: 2px solid #2e8b57; padding-bottom: 4px; }
h2 { font-size: 13.5pt; color: #0b3d2e; margin-top: 16px; border-bottom: 1px solid #cfd8dc;
     padding-bottom: 2px; page-break-after: avoid; }
h3 { font-size: 11.5pt; }
code { background: #eef1f3; padding: 1px 4px; border-radius: 4px; font-size: 9pt;
       font-family: 'Cascadia Code', Consolas, monospace; }
pre { background: #f4f6f8; border: 1px solid #dde3e8; border-radius: 6px; padding: 8px 10px;
      overflow-x: auto; page-break-inside: avoid; font-size: 8.6pt; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 6px 0; page-break-inside: avoid; }
th, td { border: 1px solid #c4ccd2; padding: 4px 7px; text-align: left; vertical-align: top; }
th { background: #eaf3ee; }
blockquote { border-left: 3px solid #2e8b57; margin: 8px 0; padding: 2px 12px; background: #f5f9f7;
             color: #333; }
a { color: #0b6; text-decoration: none; }
"""


def md_a_html(md_text: str) -> str:
    cuerpo = markdown.markdown(
        md_text, extensions=["tables", "fenced_code", "sane_lists", "attr_list"]
    )
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{cuerpo}</body></html>"


def generar_pdf(nav: str, html_path: str, pdf_path: str) -> None:
    uri = "file:///" + html_path.replace("\\", "/")
    subprocess.run(
        [nav, "--headless=new", "--disable-gpu", "--no-first-run",
         "--no-default-browser-check", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf_path}", uri],
        check=True, timeout=90,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


# ---------- PPTX ----------
VERDE = RGBColor(0x0B, 0x3D, 0x2E)
VERDE2 = RGBColor(0x2E, 0x8B, 0x57)
GRIS = RGBColor(0x22, 0x28, 0x2E)


def limpiar_inline(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)  # enlaces -> texto
    s = re.sub(r"[*`_]+", "", s)                     # énfasis / code
    return s.strip()


def partir_secciones(md_text: str) -> list[tuple[str, str]]:
    # separa por encabezados de nivel 2
    partes = re.split(r"\n##\s+", "\n" + md_text)
    out = []
    for p in partes[1:]:
        linea, _, resto = p.partition("\n")
        out.append((linea.strip(), resto.strip()))
    return out


def bullets_de(cuerpo: str, maximo: int = 7) -> list[str]:
    items: list[str] = []
    for linea in cuerpo.splitlines():
        l = linea.strip()
        if not l:
            continue
        if l.startswith("|"):  # fila de tabla -> 1ª y 2ª celda
            celdas = [c.strip() for c in l.strip("|").split("|")]
            if set("".join(celdas)) <= set("-: "):
                continue
            if celdas and celdas[0] in ("#", "Tema", "Síntoma / mensaje", "Síntoma"):
                continue
            texto = " — ".join([c for c in celdas[:2] if c])
            items.append(limpiar_inline(texto))
        elif re.match(r"^(\d+\.|[-*])\s+", l):
            items.append(limpiar_inline(re.sub(r"^(\d+\.|[-*])\s+", "", l)))
        elif l.startswith(">") or l.startswith("#") or l.startswith("```"):
            continue
        elif l.startswith(":"):  # definición
            items.append(limpiar_inline(l[1:].strip()))
        else:
            if len(l) > 3:
                items.append(limpiar_inline(l))
        if len(items) >= maximo:
            break
    return [i for i in items if i][:maximo]


def add_slide_contenido(prs, titulo: str, bullets: list[str]) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # en blanco
    # barra de título
    izq, arr, ancho = Inches(0.5), Inches(0.35), Inches(9)
    tb = slide.shapes.add_textbox(izq, arr, ancho, Inches(0.9)).text_frame
    tb.word_wrap = True
    p = tb.paragraphs[0]
    r = p.add_run(); r.text = titulo
    r.font.size = Pt(26); r.font.bold = True; r.font.color.rgb = VERDE
    # cuerpo
    cuerpo = slide.shapes.add_textbox(izq, Inches(1.4), ancho, Inches(5.4)).text_frame
    cuerpo.word_wrap = True
    for i, b in enumerate(bullets):
        par = cuerpo.paragraphs[0] if i == 0 else cuerpo.add_paragraph()
        run = par.add_run(); run.text = "•  " + b
        run.font.size = Pt(15); run.font.color.rgb = GRIS
        par.space_after = Pt(6)


def construir_pptx(md_text: str, titulo: str, subtitulo: str, out_path: str) -> None:
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    # portada
    s = prs.slides.add_slide(prs.slide_layouts[6])
    caja = s.shapes.add_textbox(Inches(0.6), Inches(2.4), Inches(8.8), Inches(2.5)).text_frame
    caja.word_wrap = True
    p = caja.paragraphs[0]; r = p.add_run(); r.text = titulo
    r.font.size = Pt(32); r.font.bold = True; r.font.color.rgb = VERDE
    p2 = caja.add_paragraph(); r2 = p2.add_run(); r2.text = subtitulo
    r2.font.size = Pt(16); r2.font.color.rgb = VERDE2
    p3 = caja.add_paragraph(); r3 = p3.add_run()
    r3.text = "Programa de Ciberseguridad Moderna"
    r3.font.size = Pt(12); r3.font.color.rgb = GRIS

    saltar = {"➡️ Siguiente clase", "📥 Material descargable"}
    for titulo_sec, cuerpo in partir_secciones(md_text):
        if any(k in titulo_sec for k in saltar):
            continue
        bullets = bullets_de(cuerpo)
        if not bullets:
            continue
        add_slide_contenido(prs, titulo_sec, bullets)
    prs.save(out_path)


# ---------- README: sección de material ----------
def anadir_seccion_descargas(readme: str, pdf_name: str, pptx_name: str) -> None:
    txt = open(readme, encoding="utf-8").read()
    if "## 📥 Material descargable" in txt:
        return
    bloque = (
        "## 📥 Material descargable\n\n"
        f"- 📄 [Guía en PDF](./{pdf_name}) — versión imprimible de esta clase.\n"
        f"- 🎞️ [Presentación (PPTX)](./{pptx_name}) — deck para proyectar en clase.\n\n"
    )
    marcador = "## ➡️ Siguiente clase"
    if marcador in txt:
        txt = txt.replace(marcador, bloque + marcador, 1)
    else:
        txt = txt.rstrip() + "\n\n" + bloque
    open(readme, "w", encoding="utf-8", newline="\n").write(txt)


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("Uso: python scripts/generar_material.py <indice_parte> [--solo-una]")
    idx = int(sys.argv[1])
    solo_una = "--solo-una" in sys.argv

    partes = sorted(glob.glob(os.path.join(CLASSES, f"parte-{idx}-*")))
    if not partes:
        raise SystemExit(f"No existe la parte {idx}")
    pdir = partes[0]
    clases = sorted(d for d in glob.glob(os.path.join(pdir, "*")) if os.path.isdir(d))
    if solo_una:
        clases = clases[:1]

    nav = navegador()
    tmp = tempfile.mkdtemp(prefix="matcurso_")
    hechos = 0
    for cdir in clases:
        readme = os.path.join(cdir, "README.md")
        if not os.path.isfile(readme):
            continue
        md_text = open(readme, encoding="utf-8").read()
        slug = os.path.basename(cdir)
        m = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
        titulo = re.sub(r"[#*`]", "", m.group(1)).strip() if m else slug
        num = slug[:3]
        pdf_name = f"clase-{num}-guia.pdf"
        pptx_name = f"clase-{num}-presentacion.pptx"

        # PDF
        html_path = os.path.join(tmp, f"{slug}.html")
        open(html_path, "w", encoding="utf-8").write(md_a_html(md_text))
        generar_pdf(nav, html_path, os.path.join(cdir, pdf_name))
        # PPTX
        construir_pptx(md_text, titulo, os.path.basename(pdir).replace("-", " "),
                       os.path.join(cdir, pptx_name))
        # README
        anadir_seccion_descargas(readme, pdf_name, pptx_name)
        hechos += 1
        print(f"  [OK] {slug}  -> {pdf_name} + {pptx_name}")

    print(f"Parte {idx}: material generado para {hechos} clase(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
