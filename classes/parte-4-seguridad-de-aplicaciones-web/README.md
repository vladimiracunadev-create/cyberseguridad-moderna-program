# Parte 4 — Seguridad de aplicaciones web

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-5-explotacion-de-sistemas-y-binarios/README.md)

**30 clases** · rango 086–115 · OWASP Top 10, Burp Suite, inyecciones, XSS, SSRF, APIs y bug bounty

**Fuentes de referencia de esta parte:**

- Dafydd Stuttard y Marcus Pinto — *The Web Application Hacker's Handbook* (2ª ed., Wiley)
- Peter Yaworski — *Real-World Bug Hunting* (No Starch Press)
- Vickie Li — *Bug Bounty Bootcamp* (No Starch Press)
- OWASP — *Top 10 (2021)*, *Web Security Testing Guide (WSTG)* y *Application Security Verification Standard (ASVS)*
- PortSwigger — *Web Security Academy* (material de laboratorio y taxonomía de ataques)

---

## 🎯 ¿De qué trata esta parte?

La web es la superficie de ataque más expuesta de casi cualquier organización: un navegador, una URL y un endpoint HTTP bastan para alcanzar datos, lógica de negocio e infraestructura interna. Esta parte enseña a **encontrar, explotar y corregir** las vulnerabilidades que dominan el panorama real de las aplicaciones web modernas, desde el clásico SQL injection hasta ataques de protocolo como el HTTP request smuggling.

Trabajaremos con el **OWASP Top 10** como mapa mental, el **Web Security Testing Guide** como metodología y **Burp Suite** como herramienta central de proxy e interceptación. Cada clase combina teoría (cómo y por qué falla el código) con laboratorio práctico sobre entornos deliberadamente vulnerables y autorizados: **DVWA**, **OWASP Juice Shop** y los **PortSwigger Web Security Academy labs**.

Sirve a pentesters web, cazadores de bugs (bug bounty), desarrolladores que quieren escribir código seguro y equipos de AppSec/DevSecOps. Al final no solo sabrás romper aplicaciones: sabrás explicar el impacto, priorizar el riesgo y proponer la corrección correcta.

## 🧩 Problemas que resuelve

- Identificar la **superficie de ataque** real de una aplicación web moderna (SPA, API, microservicios).
- Detectar y explotar las **10 categorías de OWASP** con evidencia reproducible.
- Usar **Burp Suite y ZAP** con fluidez para interceptar, modificar y automatizar peticiones.
- Encadenar vulnerabilidades (p. ej. SSRF → metadata cloud → RCE) para demostrar impacto real.
- Auditar **APIs REST y GraphQL**, JWT, OAuth y mecanismos de autenticación/sesión.
- Distinguir un hallazgo trivial de uno crítico y **redactar reportes** aceptables en programas de bug bounty.
- Cerrar el círculo: proponer **secure coding** y defensas efectivas, no solo señalar el fallo.

## 🎓 Resultados de aprendizaje

Al terminar la parte, el alumno podrá:

- Mapear una aplicación y priorizar su superficie de ataque siguiendo la WSTG.
- Explotar inyecciones (SQL, NoSQL, comandos, plantillas) y automatizarlas con sqlmap.
- Detectar y explotar XSS reflejado, almacenado y basado en DOM, y evaluar su impacto.
- Analizar y atacar SSRF, XXE, CSRF, deserialización insegura y carga de archivos.
- Auditar tokens JWT, flujos OAuth 2.0/OIDC y controles de acceso (IDOR, path traversal).
- Evaluar la seguridad de APIs REST/GraphQL y ataques de protocolo (request smuggling, cache poisoning).
- Ejecutar una metodología de bug bounty y redactar reportes con impacto y remediación.
- Recomendar controles de secure coding alineados con OWASP ASVS.

## 🧱 Prerrequisitos

- **Parte 1** (fundamentos de redes y HTTP) y **Parte 2** (Linux, herramientas).
- **Parte 3** (metodología de pentesting): reconocimiento, enumeración y gestión de un compromiso.
- Nociones de HTTP, HTML, JavaScript y SQL básicos. No hace falta ser desarrollador experto, pero saber leer código ayuda mucho.

## 🗺️ Estructura temática

| Bloque | Clases | Contenido |
|--------|--------|-----------|
| Fundamentos y herramientas | 086–090 | Superficie de ataque, OWASP Top 10, Burp, ZAP, mapeo |
| Inyecciones | 091–095 | SQLi, blind SQLi, sqlmap, NoSQL, command injection |
| Cross-site y falsificación | 096–099 | XSS reflejado, XSS stored/DOM, CSRF, SSRF |
| Datos, auth y sesiones | 100–105 | XXE, auth bypass, sesiones, JWT, OAuth, IDOR/path traversal |
| Server-side avanzado | 106–109 | Deserialización, SSTI, upload, lógica de negocio |
| APIs y protocolo | 110–113 | REST, GraphQL, request smuggling/cache, client-side |
| Cierre profesional | 114–115 | Bug bounty y secure coding |

## 🔗 Referencias de la parte

- Stuttard & Pinto, *The Web Application Hacker's Handbook*, 2ª ed., Wiley.
- Yaworski, *Real-World Bug Hunting*, No Starch Press.
- Li, *Bug Bounty Bootcamp*, No Starch Press.
- OWASP Top 10 — <https://owasp.org/Top10/>
- OWASP Web Security Testing Guide — <https://owasp.org/www-project-web-security-testing-guide/>
- OWASP ASVS — <https://owasp.org/www-project-application-security-verification-standard/>
- PortSwigger Web Security Academy — <https://portswigger.net/web-security>

## ▶️ Empezar

[Clase 086 — Arquitectura web moderna y superficie de ataque](086-arquitectura-web-moderna-y-superficie-de-ataque/README.md)
