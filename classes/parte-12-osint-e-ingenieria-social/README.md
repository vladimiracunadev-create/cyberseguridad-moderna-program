# Parte 12 — OSINT e ingeniería social

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-13-seguridad-movil-iot-e-inalambrica/README.md)

**12 clases** · rango 249–260 · Inteligencia de fuentes abiertas, phishing y OPSEC personal

**Fuentes de referencia de esta parte:**

- Michael Bazzell — *Open Source Intelligence Techniques* (11.ª ed.).
- Michael Bazzell — *Extreme Privacy: What It Takes to Disappear*.
- Christopher Hadnagy — *Social Engineering: The Science of Human Hacking* (2.ª ed.).
- Robert Cialdini — *Influence: The Psychology of Persuasion*.
- MITRE ATT&CK — Táctica *Reconnaissance* (TA0043) y *Resource Development* (TA0042).
- OSINT Framework (osintframework.com) y Trace Labs OSINT VM.

---

## 🎯 ¿De qué trata esta parte?

La inteligencia de fuentes abiertas (OSINT) es el arte de recolectar, correlacionar y analizar
información **públicamente disponible** para construir un panorama sobre una persona, una empresa,
un dominio o una infraestructura. Es la primera fase de casi cualquier operación ofensiva
(red team, pentest, threat intel) y, al mismo tiempo, la materia prima del atacante real. Quien
entiende OSINT entiende cuánto se expone una organización sin darse cuenta, y aprende a reducir esa
superficie. Esta parte cubre desde los fundamentos metodológicos hasta la automatización con
SpiderFoot y Maltego, pasando por Shodan, Censys y la geolocalización de imágenes.

La segunda mitad aborda la **ingeniería social**: la explotación del factor humano. El firewall más
caro no detiene a un empleado que entrega su contraseña por teléfono a alguien que "suena oficial".
Estudiaremos los principios psicológicos de la influencia, el pretexting, el vishing y las campañas
de phishing controladas con GoPhish, siempre desde la óptica de la simulación autorizada y la
concienciación defensiva.

Esta parte sirve a analistas de threat intelligence, red teamers, investigadores, periodistas,
equipos de concienciación (security awareness) y a cualquier profesional que quiera entender —y
reducir— su propia huella digital. La OPSEC personal cierra el círculo: proteger tu identidad es la
mejor forma de comprender cómo se vulnera la de otros.

## 🧩 Problemas que resuelve

- Mapear la superficie de exposición pública de una organización antes de un pentest.
- Verificar identidades, detectar suplantaciones y validar fuentes en investigaciones.
- Descubrir subdominios, correos y tecnologías filtradas que amplían el vector de ataque.
- Localizar dispositivos expuestos en Internet (Shodan/Censys) y priorizar su remediación.
- Medir la resiliencia humana de una empresa mediante simulacros de phishing éticos y medibles.
- Formar a los empleados para reconocer pretextos, vishing y correos maliciosos.
- Reducir la huella digital personal y operar con anonimato defendible cuando el trabajo lo exige.

## 🎓 Resultados de aprendizaje

Al terminar la parte, el alumno podrá:

- Aplicar un ciclo de inteligencia (dirección, recolección, procesamiento, análisis, difusión) sobre un objetivo autorizado.
- Realizar OSINT de personas, empresas, dominios y redes sociales documentando la cadena de custodia.
- Geolocalizar imágenes y verificar contenido combinando metadatos y análisis visual.
- Consultar Shodan y Censys con dorks precisos para inventariar exposición técnica.
- Automatizar la recolección y correlación con SpiderFoot y Maltego.
- Diseñar y ejecutar una campaña de phishing controlada con GoPhish, con métricas y reporte.
- Explicar los principios de influencia de Cialdini y construir pretextos verosímiles y éticos.
- Implementar controles de defensa contra ingeniería social y un plan de OPSEC personal.

## 🧱 Prerrequisitos

- Parte 1 (fundamentos y ética/legalidad de la ciberseguridad).
- Parte 3–4 (redes, DNS y protocolos) para entender OSINT de dominios e infraestructura.
- Manejo básico de Linux, la terminal y máquinas virtuales aisladas.
- Nociones de la Parte 11 (DevSecOps) ayudan a contextualizar filtraciones en repositorios.

## 🗺️ Estructura temática

| Bloque | Clases | Enfoque |
|--------|--------|---------|
| Metodología OSINT | 249 | Ciclo de inteligencia, ética y legalidad |
| OSINT por objetivo | 250–252 | Personas, empresas/dominios, redes sociales |
| OSINT visual y técnico | 253–254 | Geolocalización de imágenes, Shodan/Censys |
| Automatización | 255 | SpiderFoot y Maltego |
| Ingeniería social | 256–258 | Fundamentos, pretexting/vishing, phishing con GoPhish |
| Defensa y anonimato | 259–260 | Controles anti-SE y OPSEC personal |

## ⚖️ Nota ética y legal (léela antes de empezar)

Todo el contenido de esta parte se enseña con fines **defensivos, de concienciación y de pruebas
autorizadas**. OSINT se practica **únicamente sobre información genuinamente pública** y sobre
objetivos para los que tienes autorización o que son de acceso legítimo (tú mismo, tu organización,
un cliente con contrato). La ingeniería social —pretexting, vishing, phishing— solo es lícita con
**permiso explícito y por escrito** (alcance, ventana temporal, "reglas de enfrentamiento" y
contacto de escalado firmados). Recolectar datos personales sin base legal, suplantar identidades
fuera de un engagement autorizado o acosar puede constituir delito (GDPR/leyes de protección de
datos, fraude, usurpación de identidad). Ante la duda, no lo hagas: pide autorización.

## 🔗 Referencias de la parte

- Bazzell, M. *Open Source Intelligence Techniques*. https://inteltechniques.com/book1.html
- Bazzell, M. *Extreme Privacy*. https://inteltechniques.com/book7.html
- Hadnagy, C. *Social Engineering: The Science of Human Hacking*. Wiley.
- Cialdini, R. *Influence: The Psychology of Persuasion*.
- MITRE ATT&CK — Reconnaissance (TA0043). https://attack.mitre.org/tactics/TA0043/
- OSINT Framework. https://osintframework.com/

## ▶️ Empezar

[Clase 249 — Fundamentos de OSINT](249-fundamentos-de-osint/README.md)
