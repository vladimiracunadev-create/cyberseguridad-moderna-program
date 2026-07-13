# 🧭 Rutas guiadas por rol

El programa tiene 330 clases; **no todas son para todos a la vez**. Estas rutas ordenan el
recorrido según el rol al que apuntas: qué partes hacer, en qué orden, con qué laboratorios
practicar y a qué certificación apuntar. Todas asumen que **empiezas por la Parte 0**
(fundamentos): es el cimiento común.

> Leyenda: 📚 partes/clases · 🧪 laboratorio · 🚩 reto CTF · 🎓 certificación sugerida.

---

## 🎯 Pentester / Ethical Hacker

Ofensiva generalista: reconocimiento, explotación, web, post-explotación y reporte.

1. 📚 **Parte 0** — Fundamentos (001–025)
2. 📚 **Parte 1** — Redes (026–045)
3. 📚 **Parte 2** — Criptografía (046–065) · foco en hashing, TLS, contraseñas
4. 📚 **Parte 3** — Pentesting: metodología (066–085)
5. 📚 **Parte 4** — Seguridad web (086–115)
6. 📚 **Parte 5** — Explotación de binarios (116–140) · al menos 116–125
7. 📚 **Parte 12** — OSINT e ingeniería social (249–260)

- 🧪 [`appsec-web`](../labs/appsec-web/README.md) · [`red-team-ad`](../labs/red-team-ad/README.md)
- 🚩 [CTF web / pwn / redes](../ctf/README.md)
- 🎓 **OSCP** (PEN-200) · CompTIA PenTest+

## 🔴 Red Teamer

Emulación de adversarios, evasión y dominio de Active Directory.

1. Ruta de Pentester (arriba) como base
2. 📚 **Parte 7** — Red Team y operaciones ofensivas (161–180)
3. 📚 **Parte 6** — Análisis de malware (141–160) · para entender payloads y evasión
4. 📚 **Parte 5** — Explotación (116–140) · desarrollo de exploits y evasión

- 🧪 [`red-team-ad`](../labs/red-team-ad/README.md) (+ GOAD)
- 🎓 **CRTO** · OSEP (PEN-300)

## 🔵 Analista SOC / Blue Team

Detección, monitoreo, threat hunting y respuesta temprana.

1. 📚 **Parte 0** — Fundamentos (001–025)
2. 📚 **Parte 1** — Redes y NSM (026–045)
3. 📚 **Parte 6** — Análisis de malware (141–160) · triaje y comportamiento
4. 📚 **Parte 8** — Blue Team, detección y SOC (181–200)
5. 📚 **Parte 9** — DFIR (201–220) · al menos respuesta a incidentes

- 🧪 [`blue-team-soc`](../labs/blue-team-soc/README.md)
- 🚩 [CTF forense / redes](../ctf/README.md)
- 🎓 **BTL1** (Blue Team Level 1) · CompTIA CySA+

## 🕵️ DFIR / Analista forense

Adquisición, memoria, timelines y respuesta a incidentes.

1. 📚 **Parte 0** — Fundamentos (001–025)
2. 📚 **Parte 1** — Redes (026–045)
3. 📚 **Parte 6** — Análisis de malware (141–160)
4. 📚 **Parte 9** — Forense digital y respuesta a incidentes (201–220)
5. 📚 **Parte 8** — Detección (181–200) · para cerrar el ciclo detección→respuesta

- 🧪 [`blue-team-soc`](../labs/blue-team-soc/README.md) · [`dfir-memoria`](../labs/dfir-memoria/README.md) · 🚩 [CTF forense](../ctf/README.md)
- 🎓 **GCFA / GCFE** (SANS) · CHFI

## 🕸️ AppSec / Bug Bounty

Seguridad de aplicaciones y caza de vulnerabilidades web.

1. 📚 **Parte 0** — Fundamentos (001–025)
2. 📚 **Parte 2** — Criptografía (046–065)
3. 📚 **Parte 4** — Seguridad web (086–115) · núcleo
4. 📚 **Parte 11** — DevSecOps y SDLC (236–248) · para el lado defensivo
5. 📚 **Parte 15** — Seguridad de IA/LLM (291–300) · superficie moderna

- 🧪 [`appsec-web`](../labs/appsec-web/README.md) · [`appsec-code`](../labs/appsec-code/README.md) · 🚩 [CTF web](../ctf/README.md)
- 🎓 **eWPTX** · Burp Suite Certified Practitioner

## ☁️ Cloud Security Engineer

Seguridad de nube, contenedores y pipelines.

1. 📚 **Parte 0** — Fundamentos (001–025)
2. 📚 **Parte 2** — Criptografía (046–065) · claves, KMS, TLS
3. 📚 **Parte 4** — Seguridad web (086–115) · APIs
4. 📚 **Parte 10** — Nube y contenedores (221–235)
5. 📚 **Parte 11** — DevSecOps (236–248)

- 🎓 AWS Security Specialty · **CKS** (Kubernetes Security)

## 🏛️ GRC / Gestión de seguridad

Gobernanza, riesgo, cumplimiento y auditoría.

1. 📚 **Parte 0** — Fundamentos (001–025) · contexto técnico mínimo
2. 📚 **Parte 14** — GRC, riesgo y cumplimiento (276–290) · núcleo
3. 📚 **Parte 8** — SOC (181–200) y **Parte 9** — DFIR (201–220) · para dialogar con lo técnico
4. 📚 **Parte 11** — DevSecOps (236–248) · gestión de riesgo en el SDLC

- 🎓 **CISSP** · ISO 27001 Lead Implementer/Auditor · CISM

---

## Después de tu ruta

- Consulta el [mapeo a certificaciones](../certificaciones/README.md) para ver cuánto cubre el programa de tu examen objetivo.
- Refuerza con las [autoevaluaciones](../autoevaluaciones/README.md) por parte.
- Marca tu avance en el [seguimiento de progreso](../autoevaluaciones/README.md#progreso).
- Cierra con los **capstones** de la [Parte 16](../classes/parte-16-capstones-y-preparacion-de-certificaciones/README.md).

> ¿No encajas en un solo rol? Es normal. Combina rutas: casi todos los perfiles se benefician
> de entender **el otro lado** (un pentester que sabe cómo lo detectan es mejor pentester).
