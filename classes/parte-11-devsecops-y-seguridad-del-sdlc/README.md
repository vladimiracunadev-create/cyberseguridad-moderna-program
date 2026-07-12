# Parte 11 — DevSecOps y seguridad del SDLC

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-12-osint-e-ingenieria-social/README.md)

**13 clases** · rango 236–248 · Shift-left, threat modeling, SAST/DAST/SCA y supply chain

**Fuentes de referencia de esta parte:**

- Julien Vehent — *Securing DevOps: Security in the Cloud* (Manning, 2018).
- Laura Bell, Michael Brunton-Spall, Rich Smith, Jim Bird — *Agile Application Security* (O'Reilly, 2017).
- Jim Bird — *DevOpsSec* (O'Reilly, 2016).
- OWASP SAMM v2 (Software Assurance Maturity Model).
- OWASP Application Security Verification Standard (ASVS) v4.
- NIST SP 800-218 — *Secure Software Development Framework (SSDF)*.

---

## 🎯 ¿De qué trata esta parte?

DevSecOps no es una herramienta ni un producto: es la práctica de integrar la seguridad
en cada fase del ciclo de vida del software (SDLC), de forma automatizada y con el mismo
ritmo con el que los equipos hoy construyen, prueban y despliegan. En lugar de dejar la
seguridad como una auditoría al final (cuando corregir cuesta 10 o 100 veces más), la
movemos hacia la izquierda del ciclo —**shift-left**— para detectar y prevenir defectos
mientras el código todavía está barato de cambiar.

Esta parte recorre el arsenal completo del ingeniero DevSecOps: modelar amenazas antes de
escribir código (STRIDE, DREAD), analizar el código propio (SAST), la aplicación en
ejecución (DAST), las dependencias de terceros (SCA), y la cadena de suministro entera
(SBOM, SLSA, firmas). Veremos cómo blindar el pipeline de CI/CD —que se ha vuelto un
objetivo de primer nivel tras incidentes como SolarWinds y Codecov—, cómo construir
imágenes de contenedor mínimas y firmadas, y cómo expresar políticas de seguridad como
código auditable con OPA.

Está pensada para desarrolladores que quieren dueño de la seguridad de lo que construyen,
para ingenieros de plataforma/SRE que operan pipelines, y para AppSec que necesitan
escalar sin ser cuello de botella. El hilo conductor es la **automatización**: la seguridad
que no está en el pipeline no existe a la velocidad del negocio.

## 🧩 Problemas que resuelve

- Vulnerabilidades detectadas en producción cuando arreglarlas es carísimo y arriesgado.
- Equipos de AppSec convertidos en cuello de botella que frena las entregas.
- Dependencias de terceros con CVEs conocidos que entran sin control al producto.
- Secretos (API keys, tokens, contraseñas) filtrados en repositorios de código.
- Pipelines de CI/CD con permisos excesivos y sin control de integridad, usados como vector de ataque.
- Imágenes de contenedor infladas, con paquetes vulnerables y ejecutando como root.
- Ausencia de trazabilidad: nadie sabe qué componentes contiene realmente un artefacto (falta de SBOM).
- Backlog de vulnerabilidades sin priorización basada en riesgo real (explotabilidad, exposición).

## 🎓 Resultados de aprendizaje

Al terminar la parte, el alumno podrá:

- Diseñar un SDLC seguro con controles automatizados por fase y justificar la filosofía shift-left con datos de coste.
- Construir un modelo de amenazas de un sistema real usando STRIDE y priorizar con DREAD/ábacos de riesgo.
- Integrar SAST (Semgrep), DAST (OWASP ZAP) y SCA (Dependency-Check, Trivy) en un pipeline y gestionar sus falsos positivos.
- Detectar y prevenir secretos en código con gitleaks y hooks de pre-commit.
- Endurecer un pipeline de CI/CD (GitHub Actions) aplicando mínimo privilegio, pinning y aislamiento.
- Producir imágenes de contenedor mínimas, escaneadas y firmadas (cosign).
- Escribir políticas como código con OPA/Rego y validarlas con Conftest en el pipeline.
- Generar un SBOM (CycloneDX/SPDX) y explicar los niveles de SLSA para la cadena de suministro.
- Operar un programa de gestión de vulnerabilidades a escala con métricas de SLA y priorización por riesgo.

## 🧱 Prerrequisitos

- **Parte 3–4** (fundamentos de redes y criptografía) para entender firmas y TLS en el pipeline.
- **Parte 9** (seguridad de aplicaciones web / OWASP) para SAST, DAST y seguridad de APIs.
- **Parte 10** (seguridad en la nube y contenedores) para imágenes, registries y OPA.
- Manejo práctico de Git, línea de comandos, Docker y al menos un lenguaje (Python/JS/Go).
- Nociones de CI/CD (GitHub Actions, GitLab CI o similar).

## 🗺️ Estructura temática

| Bloque | Clases | Foco |
|--------|--------|------|
| **Fundamentos y diseño** | 236, 237 | Secure SDLC, shift-left y modelado de amenazas |
| **Análisis del código y la app** | 238, 239 | SAST y DAST |
| **Terceros y secretos** | 240, 241 | SCA/dependencias y secretos en el código |
| **Pipeline y artefactos** | 242, 243 | CI/CD seguro e imágenes de contenedor |
| **Gobierno y cadena de suministro** | 244, 245, 246 | Políticas como código, gestión de vulnerabilidades, SBOM/SLSA |
| **APIs y cultura** | 247, 248 | Seguridad de APIs y cultura DevSecOps / champions |

## 🔗 Referencias de la parte

- OWASP SAMM v2 — <https://owaspsamm.org/>
- OWASP ASVS — <https://owasp.org/www-project-application-security-verification-standard/>
- OWASP DevSecOps Guideline — <https://owasp.org/www-project-devsecops-guideline/>
- NIST SP 800-218 SSDF — <https://csrc.nist.gov/pubs/sp/800/218/final>
- SLSA Framework — <https://slsa.dev/>
- Julien Vehent, *Securing DevOps*, Manning 2018.
- Bell, Brunton-Spall, Smith, Bird, *Agile Application Security*, O'Reilly 2017.

## ▶️ Empezar

[Clase 236 — Secure SDLC y filosofía shift-left](236-secure-sdlc-y-filosofia-shift-left/README.md)
