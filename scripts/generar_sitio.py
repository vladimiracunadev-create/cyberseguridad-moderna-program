#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera un sitio estático (site/) a partir de los Markdown del repositorio,
para publicarlo en GitHub Pages. Renderiza el README raíz, el índice de
clases, los README de parte y los README de clase a HTML, reescribiendo
los enlaces internos .md -> .html para que la navegación funcione en el sitio.

Uso:  python scripts/generar_sitio.py
Salida: carpeta site/ con index.html y el árbol de clases en HTML.
Requiere: pip install "markdown>=3.6"
"""
from __future__ import annotations
import glob
import html as htmllib
import json
import os
import re
import shutil

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")

# Markdown de origen que se publican (rutas relativas al repo).
INCLUIR_TOP = ["README.md", "ROADMAP.md", "CONTRIBUTING.md", "SECURITY.md",
               "rutas/README.md", "autoevaluaciones/README.md", "labs/README.md",
               "ctf/README.md", "docs/syllabus.md", "docs/rubrica-evaluacion.md",
               "docs/examen-final-por-rol.md", "soluciones/README.md",
               "soluciones/parte-01-redes.md", "soluciones/parte-02-criptografia.md",
               "soluciones/parte-03-pentesting.md", "soluciones/parte-04-web.md",
               "soluciones/parte-05-binarios.md", "soluciones/parte-07-red-team.md",
               "soluciones/parte-08-blue-team.md", "soluciones/parte-09-dfir.md",
               "soluciones/parte-17-profundizacion.md"]

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
<div class="nav"><a href="{home}">🛡️ Inicio</a> · <a href="{indice}">📚 Clases</a> · <a href="{rutas}">🧭 Rutas</a> · <a href="{quiz}">📝 Autoevaluación</a> · <a href="{progreso}">✅ Progreso</a> · <a href="{certis}">🎓 Certis</a></div>
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
        certis=f"{subir}certificaciones/README.html" if prof else "certificaciones/README.html",
        body=render(reescribir_enlaces(md_text)),
    )
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)


LANDING_CSS = """
:root{
  --verde:#2e8b57; --verde2:#0b3d2e; --acento:#3fb950;
  --bg:#ffffff; --bg2:#f4f7f6; --txt:#12181d; --muted:#5b6670; --card:#ffffff; --borde:#e2e8ec;
}
@media (prefers-color-scheme:dark){
  :root{ --bg:#0d1117; --bg2:#111820; --txt:#e6edf3; --muted:#9aa7b2; --card:#161b22; --borde:#273039; --verde:#3fb950; }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--txt);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1040px;margin:0 auto;padding:0 1.1rem}
/* Hero */
.hero{position:relative;overflow:hidden;color:#fff;text-align:center;padding:4.5rem 1.1rem 3.2rem;
  background:radial-gradient(1200px 500px at 50% -10%,#1f7a4d 0%,#0b3d2e 55%,#062018 100%)}
.hero::after{content:"";position:absolute;inset:0;opacity:.10;
  background-image:linear-gradient(#fff 1px,transparent 1px),linear-gradient(90deg,#fff 1px,transparent 1px);
  background-size:34px 34px;mask-image:radial-gradient(circle at 50% 0,#000,transparent 75%)}
.hero>*{position:relative;z-index:1}
.hero .escudo{font-size:3.2rem;line-height:1}
.hero h1{font-size:clamp(1.8rem,4.5vw,3rem);margin:.4rem 0 .3rem;font-weight:800;letter-spacing:-.5px}
.hero .sub{font-size:clamp(1rem,2.2vw,1.25rem);opacity:.92;max-width:640px;margin:0 auto 1.4rem}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin-bottom:1.6rem}
.chip{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);border-radius:999px;
  padding:.28rem .8rem;font-size:.85rem;font-weight:600;backdrop-filter:blur(4px)}
.cta{display:flex;flex-wrap:wrap;gap:.7rem;justify-content:center}
.btn{display:inline-block;padding:.7rem 1.3rem;border-radius:10px;font-weight:700;font-size:1rem;transition:transform .08s ease,box-shadow .2s}
.btn:hover{transform:translateY(-2px)}
.btn-1{background:#fff;color:#0b3d2e;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.btn-2{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.5)}
/* Aviso */
.aviso{background:var(--bg2);border-bottom:1px solid var(--borde);font-size:.9rem;color:var(--muted)}
.aviso .wrap{padding:.7rem 1.1rem;text-align:center}
/* Stats */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:1rem;margin:2.6rem 0}
.stat{background:var(--card);border:1px solid var(--borde);border-radius:14px;padding:1.1rem;text-align:center}
.stat b{display:block;font-size:1.9rem;color:var(--verde);font-weight:800;line-height:1}
.stat span{font-size:.85rem;color:var(--muted)}
/* Secciones */
h2.sec{font-size:1.5rem;margin:2.6rem 0 1.1rem;font-weight:800}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1rem}
.feat{background:var(--card);border:1px solid var(--borde);border-radius:14px;padding:1.2rem;transition:border-color .2s,transform .08s}
.feat:hover{border-color:var(--verde);transform:translateY(-2px)}
.feat .ic{font-size:1.7rem}
.feat h3{margin:.5rem 0 .3rem;font-size:1.08rem}
.feat p{margin:0;color:var(--muted);font-size:.92rem}
/* Partes */
.parts{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.8rem}
.part{display:flex;gap:.75rem;align-items:center;background:var(--card);border:1px solid var(--borde);
  border-radius:12px;padding:.8rem .9rem;transition:border-color .2s,transform .08s}
.part:hover{border-color:var(--verde);transform:translateY(-2px)}
.part .num{flex:0 0 auto;width:38px;height:38px;border-radius:10px;display:grid;place-items:center;
  font-weight:800;color:#fff;background:linear-gradient(135deg,var(--verde),var(--verde2))}
.part .t{font-size:.92rem;font-weight:600;line-height:1.25}
.part .c{font-size:.78rem;color:var(--muted)}
/* Footer */
footer{margin-top:3rem;border-top:1px solid var(--borde);background:var(--bg2)}
footer .wrap{padding:2rem 1.1rem;text-align:center;color:var(--muted);font-size:.9rem}
footer a{color:var(--verde);font-weight:600}
"""


def datos_partes():
    partes = []
    for pdir in sorted(glob.glob(os.path.join(ROOT, "classes", "parte-*")),
                       key=lambda p: int(re.search(r"parte-(\d+)", p).group(1))):
        idx = int(re.search(r"parte-(\d+)", pdir).group(1))
        slug = os.path.basename(pdir)
        nums, titulo = [], slug
        rp = os.path.join(pdir, "README.md")
        if os.path.isfile(rp):
            mm = re.search(r"^#\s+Parte\s+\d+\s*[—-]\s*(.+)$",
                           open(rp, encoding="utf-8").read(), re.MULTILINE)
            if mm:
                titulo = mm.group(1).split(":")[0].strip()
        for c in glob.glob(os.path.join(pdir, "*")):
            m = re.match(r"^(\d{3})", os.path.basename(c))
            if m and os.path.isdir(c):
                nums.append(int(m.group(1)))
        partes.append({"idx": idx, "slug": slug, "titulo": titulo,
                       "n": len(nums), "ini": min(nums), "fin": max(nums)})
    return partes


def escribir_landing(partes) -> None:
    total = sum(p["n"] for p in partes)
    # Contadores dinámicos (se ajustan solos al crecer el programa).
    try:
        with open(os.path.join(ROOT, "autoevaluaciones", "preguntas.json"), encoding="utf-8") as f:
            n_preg = sum(len(p["preguntas"]) for p in json.load(f)["partes"])
    except Exception:
        n_preg = 0
    try:
        with open(os.path.join(ROOT, "certificaciones", "_mapeo.json"), encoding="utf-8") as f:
            n_cert = len(json.load(f)["certs"])
    except Exception:
        n_cert = 0
    n_labs = len([d for d in glob.glob(os.path.join(ROOT, "labs", "*")) if os.path.isdir(d)])
    stats = [(str(total), "clases"), (str(len(partes)), "partes"), (str(n_labs), "laboratorios"),
             (str(n_preg), "preguntas"), (str(n_cert), "certis mapeadas")]
    stats_html = "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for v, k in stats)
    feats = [
        ("📚", "Currículo completo", f"{total} clases de fundamentos a nivel experto, cada una con objetivo, laboratorio, ejercicios y referencias.", "classes/README.html"),
        ("🧭", "Rutas por rol", "Recorridos ordenados para pentester, red team, SOC, DFIR, AppSec, cloud y GRC.", "rutas/README.html"),
        ("🧪", "Laboratorios", "Entornos Docker que se levantan con un comando: web, SOC, Active Directory y criptografía.", "labs/README.html"),
        ("🚩", "Retos CTF", "Colección de retos con solución por categoría: web, cripto, redes, forense, OSINT y pwn.", "ctf/README.html"),
        ("📝", "Autoevaluación", f"{n_preg} preguntas interactivas con puntuación, una batería por parte.", "autoevaluaciones/quiz.html"),
        ("✅", "Tu progreso", f"Marca las {total} clases y sigue tu avance (se guarda en tu navegador).", "autoevaluaciones/progreso.html"),
        ("🎓", "Certificaciones", "Mapeo a Security+, PenTest+, CySA+, OSCP, CISSP, BTL1 y SANS con % de cobertura por dominio.", "certificaciones/README.html"),
    ]
    feats_html = "".join(
        f'<a class="feat" href="{u}"><div class="ic">{i}</div><h3>{t}</h3><p>{d}</p></a>'
        for i, t, d, u in feats)
    parts_html = "".join(
        f'<a class="part" href="classes/{p["slug"]}/README.html">'
        f'<div class="num">{p["idx"]}</div>'
        f'<div><div class="t">{htmllib.escape(p["titulo"])}</div>'
        f'<div class="c">{p["n"]} clases · {p["ini"]:03d}–{p["fin"]:03d}</div></div></a>'
        for p in partes)
    cuerpo = f"""
<header class="hero">
  <div class="escudo">🛡️</div>
  <h1>Programa de Ciberseguridad Moderna</h1>
  <p class="sub">El curso más completo en español — de redes, criptografía y Linux hasta Red Team, DFIR, cloud y seguridad de IA.</p>
  <div class="chips">
    <span class="chip">{total} clases</span><span class="chip">{len(partes)} partes</span>
    <span class="chip">Fundamentos → Experto</span><span class="chip">Español</span><span class="chip">MIT</span>
  </div>
  <div class="cta">
    <a class="btn btn-1" href="classes/README.html">📚 Empezar el curso</a>
    <a class="btn btn-2" href="rutas/README.html">🧭 Elegir mi ruta</a>
  </div>
</header>
<div class="aviso"><div class="wrap">⚠️ Contenido para aprendizaje y pruebas <b>autorizadas</b>. Practica solo en entornos propios o con permiso explícito.</div></div>
<main class="wrap">
  <div class="stats">{stats_html}</div>
  <h2 class="sec">Qué incluye</h2>
  <div class="grid">{feats_html}</div>
  <h2 class="sec">Las {len(partes)} partes</h2>
  <div class="parts">{parts_html}</div>
</main>
<footer><div class="wrap">
  Programa de Ciberseguridad Moderna · {total} clases · licencia
  <a href="https://github.com/vladimiracunadev-create/modern-cybersecurity-program">MIT en GitHub</a><br>
  <a href="classes/README.html">Índice de clases</a> · <a href="rutas/README.html">Rutas</a> ·
  <a href="autoevaluaciones/quiz.html">Autoevaluación</a> · <a href="autoevaluaciones/progreso.html">Progreso</a>
</div></footer>
"""
    doc = (f"<!doctype html><html lang='es'><head><meta charset='utf-8'>"
           f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>Programa de Ciberseguridad Moderna</title>"
           f"<style>{LANDING_CSS}</style></head><body>{cuerpo}</body></html>")
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)


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
    # Documentos de certificaciones (uno por cert + índice).
    for p in glob.glob(os.path.join(ROOT, "certificaciones", "*.md")):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        escribir(rel, open(p, encoding="utf-8").read())
        generados += 1

    # Portada diseñada (NO se usa el README como landing: el markdown dentro de
    # <div align="center"> no se renderiza y se veía roto).
    escribir_landing(datos_partes())

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
