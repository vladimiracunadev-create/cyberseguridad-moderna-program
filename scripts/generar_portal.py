# -*- coding: utf-8 -*-
"""
Genera el "portal" de evaluación (Fase 4) a partir de:
  - autoevaluaciones/preguntas.json  (banco de preguntas por parte)
  - el árbol classes/                 (para el checklist de progreso)

Produce (archivos estáticos, autocontenidos, aptos para GitHub Pages):
  - autoevaluaciones/quiz.html        (autoevaluación interactiva)
  - autoevaluaciones/progreso.html    (checklist de 310 clases con localStorage)
  - autoevaluaciones/README.md        (versión imprimible con respuestas)

Uso: python scripts/generar_portal.py
"""
from __future__ import annotations
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTO = os.path.join(ROOT, "autoevaluaciones")
CLASSES = os.path.join(ROOT, "classes")

CSS = """
:root{color-scheme:light dark}
*{box-sizing:border-box}
body{font-family:system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;line-height:1.6;
 max-width:900px;margin:0 auto;padding:1.5rem 1.1rem 4rem;color:#14181d;background:#fff}
@media(prefers-color-scheme:dark){body{color:#e6edf3;background:#0d1117}
 .card{background:#161b22!important;border-color:#30363d!important}
 .opt:hover{background:#1c2330!important} a{color:#6cb6ff}}
h1{color:#0b3d2e}h2{color:#0b3d2e;margin-top:2rem}
@media(prefers-color-scheme:dark){h1,h2{color:#3fb950}}
.nav{font-size:.9rem;margin-bottom:1.5rem;opacity:.9}
.card{border:1px solid #d0d7de;border-radius:10px;padding:1rem 1.1rem;margin:1rem 0;background:#fbfdfe}
.q{font-weight:600;margin-bottom:.5rem}
.opt{display:block;padding:.45rem .6rem;border-radius:7px;cursor:pointer;border:1px solid transparent}
.opt:hover{background:#eef3f0}
.opt input{margin-right:.5rem}
.ok{background:#d5f5e3!important;border-color:#2ecc71!important}
.bad{background:#fadbd8!important;border-color:#e74c3c!important}
.exp{margin-top:.5rem;font-size:.9rem;opacity:.85;display:none}
button{background:#2e8b57;color:#fff;border:0;border-radius:8px;padding:.5rem .9rem;cursor:pointer;font-size:1rem}
button:hover{background:#256e46}
.score{font-weight:700;margin-top:.6rem}
.bar{height:12px;border-radius:6px;background:#e5e9ec;overflow:hidden;margin:.3rem 0}
.bar>i{display:block;height:100%;background:#2e8b57}
.prog-part{margin:.8rem 0}
progress{width:100%;height:16px}
label.cls{display:block;padding:.2rem .3rem;border-radius:6px}
label.cls:hover{background:#eef3f0}
@media(prefers-color-scheme:dark){label.cls:hover{background:#1c2330}}
.small{font-size:.85rem;opacity:.8}
"""


def nav(rel_home="../index.html"):
    return (f'<div class="nav"><a href="{rel_home}">🛡️ Inicio</a> · '
            f'<a href="../classes/README.html">📚 Clases</a> · '
            f'<a href="../rutas/README.html">🧭 Rutas</a> · '
            f'<a href="quiz.html">📝 Autoevaluación</a> · '
            f'<a href="progreso.html">✅ Progreso</a></div>')


def pagina(titulo, cuerpo):
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(titulo)}</title><style>{CSS}</style></head>"
            f"<body>{cuerpo}</body></html>")


def cargar_preguntas():
    with open(os.path.join(AUTO, "preguntas.json"), encoding="utf-8") as f:
        return json.load(f)


def gen_quiz(data):
    js = json.dumps(data["partes"], ensure_ascii=False)
    cuerpo = f"""{nav()}
<h1>📝 Autoevaluación</h1>
<p class="small">Una batería por parte. Marca una opción por pregunta y pulsa <b>Corregir</b>.
Se resalta el acierto/error y aparece la explicación. Tu nota no se envía a ningún sitio.</p>
<div id="app"></div>
<script>
const PARTES = {js};
const app = document.getElementById('app');
PARTES.forEach((parte, pi) => {{
  const sec = document.createElement('section');
  sec.innerHTML = `<h2>Parte ${{parte.idx}} — ${{parte.titulo}}</h2>`;
  parte.preguntas.forEach((pr, qi) => {{
    const card = document.createElement('div'); card.className='card';
    let opts = pr.opciones.map((o,oi)=>
      `<label class="opt" data-p="${{pi}}" data-q="${{qi}}" data-o="${{oi}}">
         <input type="radio" name="q_${{pi}}_${{qi}}" value="${{oi}}">${{o}}</label>`).join('');
    card.innerHTML = `<div class="q">${{qi+1}}. ${{pr.q}}</div>${{opts}}
      <div class="exp" id="e_${{pi}}_${{qi}}">✔️ ${{pr.exp}}</div>`;
    sec.appendChild(card);
  }});
  const btn = document.createElement('button');
  btn.textContent = 'Corregir parte ' + parte.idx;
  const score = document.createElement('div'); score.className='score';
  btn.onclick = () => {{
    let ok=0;
    parte.preguntas.forEach((pr,qi)=>{{
      const sel = sec.querySelector(`input[name="q_${{pi}}_${{qi}}"]:checked`);
      sec.querySelectorAll(`.opt[data-q="${{qi}}"]`).forEach(l=>l.classList.remove('ok','bad'));
      const correcta = sec.querySelector(`.opt[data-q="${{qi}}"][data-o="${{pr.correcta}}"]`);
      if(correcta) correcta.classList.add('ok');
      if(sel){{
        if(parseInt(sel.value)===pr.correcta) ok++;
        else sec.querySelector(`.opt[data-q="${{qi}}"][data-o="${{sel.value}}"]`).classList.add('bad');
      }}
      document.getElementById(`e_${{pi}}_${{qi}}`).style.display='block';
    }});
    score.textContent = `Puntuación: ${{ok}} / ${{parte.preguntas.length}}`;
  }};
  sec.appendChild(btn); sec.appendChild(score);
  app.appendChild(sec);
}});
</script>"""
    with open(os.path.join(AUTO, "quiz.html"), "w", encoding="utf-8") as f:
        f.write(pagina("Autoevaluación — Ciberseguridad Moderna", cuerpo))


def listar_clases():
    partes = []
    for pdir in sorted(glob.glob(os.path.join(CLASSES, "parte-*")),
                       key=lambda p: int(re.search(r"parte-(\d+)", p).group(1))):
        idx = int(re.search(r"parte-(\d+)", pdir).group(1))
        titulo = os.path.basename(pdir).split("-", 2)[-1].replace("-", " ").capitalize()
        clases = []
        for cdir in sorted(glob.glob(os.path.join(pdir, "*"))):
            if not os.path.isdir(cdir):
                continue
            slug = os.path.basename(cdir)
            m = re.match(r"^(\d{3})", slug)
            if not m:
                continue
            readme = os.path.join(cdir, "README.md")
            t = slug
            if os.path.isfile(readme):
                mm = re.search(r"^#\s+(.+)$", open(readme, encoding="utf-8").read(), re.MULTILINE)
                if mm:
                    t = re.sub(r"[#*`]", "", mm.group(1)).strip()
            clases.append({"n": m.group(1), "t": t})
        partes.append({"idx": idx, "titulo": titulo, "clases": clases})
    return partes


def gen_progreso(partes):
    js = json.dumps(partes, ensure_ascii=False)
    cuerpo = f"""{nav()}
<h1>✅ Mi progreso</h1>
<p class="small">Marca las clases que completes. Tu avance se guarda <b>solo en este navegador</b>
(localStorage), no se envía a ningún servidor.</p>
<div class="prog-part"><b>Total</b><progress id="tot" max="0" value="0"></progress>
<span id="tottxt"></span> · <button id="reset">Reiniciar</button></div>
<div id="app"></div>
<script>
const PARTES = {js};
const KEY='ccm-progreso';
let hecho = JSON.parse(localStorage.getItem(KEY)||'{{}}');
const app=document.getElementById('app');
let total=0, done=0;
PARTES.forEach(p=>{{
  total += p.clases.length;
  const sec=document.createElement('section');
  const pb=`pb_${{p.idx}}`;
  sec.innerHTML=`<h2>Parte ${{p.idx}} — ${{p.titulo}}</h2>
    <progress id="${{pb}}" max="${{p.clases.length}}" value="0"></progress> <span id="${{pb}}t"></span>`;
  p.clases.forEach(c=>{{
    const id='c'+c.n;
    const lab=document.createElement('label'); lab.className='cls';
    lab.innerHTML=`<input type="checkbox" data-p="${{p.idx}}" id="${{id}}"> ${{c.n}} — ${{c.t}}`;
    sec.appendChild(lab);
    const cb=lab.querySelector('input');
    cb.checked=!!hecho[id];
    cb.onchange=()=>{{ if(cb.checked)hecho[id]=1; else delete hecho[id];
      localStorage.setItem(KEY,JSON.stringify(hecho)); pintar(); }};
  }});
  app.appendChild(sec);
}});
function pintar(){{
  done=0;
  PARTES.forEach(p=>{{
    let d=0; p.clases.forEach(c=>{{ if(hecho['c'+c.n]) d++; }});
    done+=d;
    const bar=document.getElementById('pb_'+p.idx); bar.value=d;
    document.getElementById('pb_'+p.idx+'t').textContent=`${{d}}/${{p.clases.length}}`;
  }});
  const tot=document.getElementById('tot'); tot.max=total; tot.value=done;
  document.getElementById('tottxt').textContent=`${{done}}/${{total}} clases (${{Math.round(done/total*100)}}%)`;
}}
document.getElementById('reset').onclick=()=>{{ if(confirm('¿Reiniciar tu progreso?')){{hecho={{}};
  localStorage.removeItem(KEY); document.querySelectorAll('input[type=checkbox]').forEach(c=>c.checked=false); pintar();}} }};
pintar();
</script>"""
    with open(os.path.join(AUTO, "progreso.html"), "w", encoding="utf-8") as f:
        f.write(pagina("Mi progreso — Ciberseguridad Moderna", cuerpo))


def gen_readme(data):
    L = ["# 📝 Autoevaluaciones\n",
         "Batería de preguntas por parte para comprobar lo aprendido. Esta es la versión de lectura "
         "(con respuestas plegadas). Para la versión **interactiva** con puntuación, abre "
         "[`quiz.html`](quiz.html) desde el [sitio del curso](https://vladimiracunadev-create.github.io/cyberseguridad-moderna-program/autoevaluaciones/quiz.html).\n",
         "> 🧭 ¿No sabes por dónde empezar? Mira las [rutas por rol](../rutas/README.md).\n",
         "<a id=\"progreso\"></a>\n",
         "## Seguimiento de progreso\n",
         "Lleva la cuenta de las 310 clases en [`progreso.html`](progreso.html) "
         "(se guarda en tu navegador).\n",
         "---\n"]
    for p in data["partes"]:
        L.append(f"## Parte {p['idx']} — {p['titulo']}\n")
        for i, pr in enumerate(p["preguntas"], 1):
            L.append(f"**{i}. {pr['q']}**\n")
            for j, o in enumerate(pr["opciones"]):
                L.append(f"- {chr(97+j)}) {o}")
            correcta = f"{chr(97+pr['correcta'])}) {pr['opciones'][pr['correcta']]}"
            L.append(f"\n<details><summary>Ver respuesta</summary>\n\n**Correcta: {correcta}.** {pr['exp']}\n\n</details>\n")
    with open(os.path.join(AUTO, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))


def main():
    os.makedirs(AUTO, exist_ok=True)
    data = cargar_preguntas()
    gen_quiz(data)
    gen_progreso(listar_clases())
    gen_readme(data)
    n = sum(len(p["preguntas"]) for p in data["partes"])
    print(f"Portal generado: quiz.html, progreso.html, README.md ({n} preguntas, {len(data['partes'])} partes).")


if __name__ == "__main__":
    main()
