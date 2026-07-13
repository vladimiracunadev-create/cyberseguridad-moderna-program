# Parte 15 — Seguridad de IA y machine learning

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-16-capstones-y-preparacion-de-certificaciones/README.md)

**10 clases** · rango 291–300 · Ataques adversariales, OWASP LLM, prompt injection y defensa con IA

**Fuentes de referencia de esta parte:**

- **OWASP Top 10 for Large Language Model Applications** (OWASP Foundation, 2023–2025) — taxonomía de riesgos de aplicaciones con LLM.
- **MITRE ATLAS™** (Adversarial Threat Landscape for Artificial-Intelligence Systems) — matriz de tácticas y técnicas contra sistemas de ML.
- **NIST AI Risk Management Framework (AI RMF 1.0, NIST AI 100-1)** y su perfil de IA generativa (NIST AI 600-1).
- Biggio & Roli, *"Wild Patterns: Ten Years After the Rise of Adversarial Machine Learning"* (Pattern Recognition, 2018).
- Goodfellow, Shlens & Szegedy, *"Explaining and Harnessing Adversarial Examples"* (ICLR, 2015).
- **ISO/IEC 42001:2023** — sistema de gestión de la IA (AI management system) y **ISO/IEC 23894:2023** — gestión del riesgo de IA.

---

## 🎯 ¿De qué trata esta parte?

Los modelos de machine learning y, sobre todo, los grandes modelos de lenguaje (LLM) ya no son curiosidades de laboratorio: son componentes de producción que toman decisiones de crédito, filtran spam, detectan fraude, moderan contenido y conversan con clientes. Esa superficie nueva trae vulnerabilidades nuevas. Un clasificador puede engañarse con ruido imperceptible; un conjunto de entrenamiento puede envenenarse con puertas traseras; un modelo caro puede robarse a través de su propia API; y un asistente con LLM puede secuestrarse con una simple frase escondida en un documento. Esta parte enseña a pensar en la seguridad del ciclo de vida completo de la IA: datos, entrenamiento, modelo, despliegue e inferencia.

La disciplina se apoya en marcos serios y reproducibles: la taxonomía **OWASP Top 10 para LLM**, la matriz de amenazas **MITRE ATLAS**, y el **NIST AI RMF** para gobernar el riesgo. No se trata de alarmismo, sino de ingeniería: entender qué puede fallar, cómo medirlo con herramientas reales (garak, PyRIT, Adversarial Robustness Toolbox) y cómo mitigarlo con controles concretos.

Sirve a ingenieros de ML que quieren endurecer sus modelos, a equipos de AppSec que ahora heredan aplicaciones con LLM, a red teamers que evalúan sistemas de IA y a responsables de GRC que deben gobernar su adopción con criterios de seguridad y ética.

## 🧩 Problemas que resuelve

- Modelos de visión o NLP que se equivocan ante entradas manipuladas de forma imperceptible (ejemplos adversariales).
- Conjuntos de datos y modelos preentrenados contaminados con puertas traseras o sesgos inyectados.
- Fuga y robo de propiedad intelectual: extracción de modelos y de datos de entrenamiento vía la API.
- Aplicaciones con LLM vulnerables a *prompt injection*, *jailbreaks*, fuga de secretos y ejecución de acciones no autorizadas por agentes.
- Pipelines RAG que exponen datos sensibles o son manipulables desde documentos hostiles.
- Uso ofensivo de la IA (phishing automatizado, deepfakes, malware asistido) y falta de gobernanza y controles éticos.

## 🎓 Resultados de aprendizaje

Al terminar la parte, el alumno podrá:

1. Mapear la superficie de ataque de un sistema de ML/LLM sobre MITRE ATLAS y OWASP LLM.
2. Generar y evaluar ejemplos adversariales con Adversarial Robustness Toolbox (ART).
3. Diseñar y detectar ataques de envenenamiento y puertas traseras en datos y modelos.
4. Ejecutar y mitigar ataques de extracción/robo de modelos e inversión/inferencia de membresía.
5. Auditar una aplicación con LLM contra el OWASP Top 10 y probarla con garak y PyRIT.
6. Construir defensas para prompt injection en arquitecturas RAG y de agentes (aislamiento, allowlists, human-in-the-loop).
7. Aplicar IA a la defensa (detección, triage de SOC) evaluando falsos positivos y evadibilidad.
8. Gobernar el riesgo de IA con NIST AI RMF e ISO/IEC 42001, incluyendo consideraciones éticas y legales.

## 🧱 Prerrequisitos

- **Parte 14 — GRC, riesgo y cumplimiento** (marcos de riesgo, políticas, controles).
- Fundamentos de programación en Python y familiaridad con conceptos básicos de ML (entrenamiento, inferencia, features, etiquetas).
- Nociones de seguridad de aplicaciones web y APIs (partes previas del programa).
- Un entorno de laboratorio aislado con Python 3.10+, capacidad de crear entornos virtuales y, deseablemente, GPU opcional.

## 🗺️ Estructura temática

| Bloque | Clases | Foco |
|--------|--------|------|
| Fundamentos y superficie de ataque | 291 | Panorama, ciclo de vida, MITRE ATLAS, NIST AI RMF |
| Ataques al modelo | 292, 293, 294 | Adversariales, envenenamiento/backdoors, robo/extracción |
| Seguridad de LLM y aplicaciones | 295, 296, 297 | OWASP Top 10 LLM, prompt injection/jailbreaks, RAG y agentes |
| IA como herramienta | 298, 299 | Defensa (SOC/detección), ofensiva y deepfakes |
| Gobernanza | 300 | Ética, regulación, gestión del riesgo de IA |

## 🔗 Referencias de la parte

- OWASP Top 10 for LLM Applications — <https://genai.owasp.org/>
- MITRE ATLAS — <https://atlas.mitre.org/>
- NIST AI Risk Management Framework — <https://www.nist.gov/itl/ai-risk-management-framework>
- Adversarial Robustness Toolbox (IBM/LF AI) — <https://github.com/Trusted-AI/adversarial-robustness-toolbox>
- garak (NVIDIA) — <https://github.com/NVIDIA/garak> · PyRIT (Microsoft) — <https://github.com/Azure/PyRIT>
- ISO/IEC 42001:2023 — <https://www.iso.org/standard/81230.html>

## ▶️ Empezar

[Clase 291 — Introducción a la seguridad de IA y ML](291-introduccion-a-la-seguridad-de-ia-y-ml/README.md)
