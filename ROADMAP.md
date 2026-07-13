# 🗺️ Roadmap

El programa se construye por fases. El **currículo escrito** (README completo por cada una
de las 310 clases) es la base y el primer entregable.

## Fase 1 — Currículo escrito completo ✅ (en curso)

- [x] Diseño del currículo: 17 partes, 310 clases, numeración 001–310.
- [x] Estructura de carpetas + índice maestro (`classes/README.md`).
- [x] README de cada parte (narrativa, prerrequisitos, fuentes).
- [x] README rico por clase (objetivo, temas, definiciones, laboratorio, ejercicios, reto, errores comunes, FAQ, referencias).

## Fase 2 — Laboratorios ejecutables ✅ (completa)

- [x] Estructura de laboratorios ([`labs/`](labs/README.md)) con convención común y guía de uso.
- [x] Lab **AppSec Web** ([`labs/appsec-web`](labs/appsec-web/README.md)) — OWASP Juice Shop + DVWA en Docker, recorrido guiado ligado a la Parte 4.
- [x] Lab **Blue Team / SOC** ([`labs/blue-team-soc`](labs/blue-team-soc/README.md)) — Elasticsearch + Kibana con telemetría de un ataque para detección/threat hunting (Parte 8).
- [x] Lab **Red Team / Active Directory** ([`labs/red-team-ad`](labs/red-team-ad/README.md)) — caja de atacante + guía GOAD (Parte 7).
- [x] Lab de **criptografía** ([`labs/cripto`](labs/cripto/README.md)) — 4 retos con solución en Python puro (Parte 2).
- [x] Colección de **retos tipo CTF** ([`ctf/`](ctf/README.md)) con solución, por categoría.

## Fase 3 — Material complementario ✅ (completa)

Generado con `scripts/generar_material.py <parte>` (PDF vía navegador headless, PPTX vía
python-pptx). Notebooks **descartados** por decisión.

- [x] Guías **PDF** imprimibles por clase — **las 310 clases** (partes 0–16).
- [x] Presentaciones **PPTX** por clase — **las 310 clases** (partes 0–16).
- [x] Sección "📥 Material descargable" enlazada en cada README de clase.
- [x] ~~Notebooks~~ — descartado.

## Fase 4 — Portal y evaluación ✅ (completa)

- [x] Sitio web navegable del currículo (GitHub Pages, con nav a rutas/quiz/progreso).
- [x] Autoevaluaciones interactivas por parte ([`autoevaluaciones/`](autoevaluaciones/README.md), 85 preguntas).
- [x] Seguimiento de progreso de las 310 clases (localStorage).
- [x] Rutas guiadas por rol ([`rutas/`](rutas/README.md)): pentester, red team, SOC, DFIR, AppSec, cloud, GRC.

---

**Las 4 fases del roadmap están completas.** ¿Ideas o mejoras? Abre un *issue* o revisa
[CONTRIBUTING.md](CONTRIBUTING.md).
