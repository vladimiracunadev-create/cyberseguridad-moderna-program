# 🧭 Rutas guiadas por rol

El programa tiene 340 clases; **no todas son para todos a la vez**. Estas rutas ordenan el
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
- 📖 **[Guía de carrera completa →](pentester.md)** — qué es, día a día, skills, certis, salario y progresión.

## 🔴 Red Teamer

Emulación de adversarios, evasión y dominio de Active Directory.

1. Ruta de Pentester (arriba) como base
2. 📚 **Parte 7** — Red Team y operaciones ofensivas (161–180)
3. 📚 **Parte 6** — Análisis de malware (141–160) · para entender payloads y evasión
4. 📚 **Parte 5** — Explotación (116–140) · desarrollo de exploits y evasión

- 🧪 [`red-team-ad`](../labs/red-team-ad/README.md) (+ GOAD)
- 🎓 **CRTO** · OSEP (PEN-300)
- 📖 **[Guía de carrera completa →](red-team.md)** — qué es, día a día, skills, certis, salario y progresión.

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
- 📖 **[Guía de carrera completa →](soc-blue-team.md)** — qué es, día a día, skills, certis, salario y progresión.

## 🛡️ Analista de Gestión de Vulnerabilidades

Ciclo de vulnerabilidades, hardening/parchado, controles (AV/EDR) y reporte — el rol de *vulnerability management / security operations*.

1. 📚 **Parte 0** — Fundamentos (001–025) · Windows, Linux y redes
2. 📚 **Parte 1** — Redes y escaneo (026–045) · Nmap y enumeración
3. 📚 **Parte 3** — Análisis de vulnerabilidades (**071**, Nessus/OpenVAS) y reporte (**085**)
4. 📚 **Parte 17** — **318** Gestión del programa de vulnerabilidades · **322** Threat Intelligence · **324** Hardening y gestión de configuración · **321** Comunicación y reporte
5. 📚 **Parte 8** — **189** EDR · 188 Threat hunting · 195 Threat Intelligence · 197 Métricas del SOC
6. 📚 **Parte 11** — 240 SCA/dependencias · **245** Gestión de vulnerabilidades a escala
7. 📚 **Parte 9** — **219** Ejercicios de mesa (simulacros) · + Partes 3–7 para las pruebas de penetración de validación

- 🧪 [`appsec-code`](../labs/appsec-code/README.md) (SAST/vulns en código) · [`appsec-web`](../labs/appsec-web/README.md) · [`rootcause-windows`](../labs/rootcause-windows/README.md) (controles/EDR en Windows)
- 🎓 **CompTIA CySA+** · Security+ · (certs de producto: Tenable/Qualys/Rapid7)
- 📖 **[Guía de carrera completa →](gestion-vulnerabilidades.md)** — qué es, día a día, skills, certis, salario y progresión.

## 🕵️ DFIR / Analista forense

Adquisición, memoria, timelines y respuesta a incidentes.

1. 📚 **Parte 0** — Fundamentos (001–025)
2. 📚 **Parte 1** — Redes (026–045)
3. 📚 **Parte 6** — Análisis de malware (141–160)
4. 📚 **Parte 9** — Forense digital y respuesta a incidentes (201–220)
5. 📚 **Parte 8** — Detección (181–200) · para cerrar el ciclo detección→respuesta

- 🧪 [`blue-team-soc`](../labs/blue-team-soc/README.md) · [`dfir-memoria`](../labs/dfir-memoria/README.md) · 🚩 [CTF forense](../ctf/README.md)
- 🎓 **GCFA / GCFE** (SANS) · CHFI
- 📖 **[Guía de carrera completa →](dfir.md)** — qué es, día a día, skills, certis, salario y progresión.

## 🕸️ AppSec / Bug Bounty

Seguridad de aplicaciones y caza de vulnerabilidades web.

1. 📚 **Parte 0** — Fundamentos (001–025)
2. 📚 **Parte 2** — Criptografía (046–065)
3. 📚 **Parte 4** — Seguridad web (086–115) · núcleo
4. 📚 **Parte 11** — DevSecOps y SDLC (236–248) · para el lado defensivo
5. 📚 **Parte 15** — Seguridad de IA/LLM (291–300) · superficie moderna

- 🧪 [`appsec-web`](../labs/appsec-web/README.md) · [`appsec-code`](../labs/appsec-code/README.md) · 🚩 [CTF web](../ctf/README.md)
- 🎓 **eWPTX** · Burp Suite Certified Practitioner
- 📖 **[Guía de carrera completa →](appsec.md)** — qué es, día a día, skills, certis, salario y progresión.

## ☁️ Cloud Security Engineer

Seguridad de nube, contenedores y pipelines.

1. 📚 **Parte 0** — Fundamentos (001–025)
2. 📚 **Parte 2** — Criptografía (046–065) · claves, KMS, TLS
3. 📚 **Parte 4** — Seguridad web (086–115) · APIs
4. 📚 **Parte 10** — Nube y contenedores (221–235)
5. 📚 **Parte 11** — DevSecOps (236–248)

- 🎓 AWS Security Specialty · **CKS** (Kubernetes Security)
- 📖 **[Guía de carrera completa →](cloud-security.md)** — qué es, día a día, skills, certis, salario y progresión.

## 🏛️ GRC / Gestión de seguridad

Gobernanza, riesgo, cumplimiento y auditoría.

1. 📚 **Parte 0** — Fundamentos (001–025) · contexto técnico mínimo
2. 📚 **Parte 14** — GRC, riesgo y cumplimiento (276–290) · núcleo
3. 📚 **Parte 8** — SOC (181–200) y **Parte 9** — DFIR (201–220) · para dialogar con lo técnico
4. 📚 **Parte 11** — DevSecOps (236–248) · gestión de riesgo en el SDLC

- 🎓 **CISSP** · ISO 27001 Lead Implementer/Auditor · CISM
- 📖 **[Guía de carrera completa →](grc.md)** — qué es, día a día, skills, certis, salario y progresión.

---

## 🤝 Analista de Cooperación y Alianzas Técnicas

Cooperación institucional, alianzas estratégicas e intercambio de información en ciberseguridad. Un puente entre lo técnico y lo estratégico: no auditas sistemas, articulas actores.

1. 📚 **Parte 0** — Fundamentos (001–025) · el lenguaje común: tríada CIA, panorama de amenazas (002), **frameworks NIST/ISO/MITRE (003)** y ética, legalidad y divulgación responsable (025)
2. 📚 **Parte 14** — GRC, riesgo y cumplimiento (276–290) · **núcleo**: gobernanza (276), ISO 27001 (278), NIST CSF (279), **protección de datos y cumplimiento GDPR/HIPAA/PCI (281, 289)**, políticas y procedimientos (282) y **riesgo de terceros y proveedores (284)** — la base de las alianzas
3. 📚 **Parte 1** — Redes (026–045) · solo lo introductorio, para dialogar con perfiles técnicos y foros del sector
4. 📚 **Parte 8** — Blue Team / SOC (181–200) · detección e **intercambio de información de amenazas** (buenas prácticas, foros, comunidades)

- 🎓 Alineado con **CISSP** (gobernanza y gestión de riesgo) e **ISO 27001**
- 💡 El programa te da la **base técnica y de GRC** que pide el puesto (fundamentos, protección de datos, reportes técnicos, coordinación). Las competencias de **cooperación, diplomacia técnica, inglés y gestión documental** las aportas tú: el curso te hace creíble ante los actores técnicos con los que articularás.
- 📖 **[Guía de carrera completa →](cooperacion-alianzas.md)** — qué es, día a día, skills, certis, salario y progresión.

---

## Después de tu ruta

- Consulta el [mapeo a certificaciones](../certificaciones/README.md) para ver cuánto cubre el programa de tu examen objetivo.
- Refuerza con las [autoevaluaciones](../autoevaluaciones/README.md) por parte.
- Marca tu avance en el [seguimiento de progreso](../autoevaluaciones/README.md#progreso).
- Cierra con los **capstones** de la [Parte 16](../classes/parte-16-capstones-y-preparacion-de-certificaciones/README.md).

> ¿No encajas en un solo rol? Es normal. Combina rutas: casi todos los perfiles se benefician
> de entender **el otro lado** (un pentester que sabe cómo lo detectan es mejor pentester).
