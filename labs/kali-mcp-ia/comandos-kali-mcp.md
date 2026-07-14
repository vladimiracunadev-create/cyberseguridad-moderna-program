# Playbooks de kali-mcp mapeados al curso

Los `.md` de `.claude/commands/` de **[kali-mcp](https://github.com/pabpereza/kali-mcp)**
(de *pabpereza*, licencia **MIT**) son **playbooks de pentest orquestado por IA**: cada uno
le dice al agente cómo coordinar herramientas de Kali para una fase concreta.

Aquí los integramos como **puente entre la metodología del curso y la automatización con IA**:
qué automatiza cada comando, en qué fase encaja y **qué clase(s) del programa** te enseñan la
técnica *por debajo* — porque para supervisar al agente (Parte 18) primero tienes que saber
hacerlo a mano.

> 🙏 **Atribución.** Los comandos y su contenido son de **pabpereza/kali-mcp (MIT)**. Aquí
> **no se reproducen**: se catalogan y se enlazan a su archivo original. Descárgalos desde el
> repositorio oficial.
>
> ⚠️ **Uso ético.** Todos son para pentest **autorizado** (laboratorio propio o permiso escrito).
> La IA acelera; la autorización, la supervisión y la responsabilidad son **humanas** (clases 335, 339).

## 🗺️ Catálogo (21 playbooks)

| Playbook (repo) | Qué automatiza | Fase | Clases del curso |
|---|---|---|---|
| [`kali-start`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-start.md) | Inicia la sesión y define el **alcance** | Planificación | 067 (RoE/alcance), 340 |
| [`kali-recon`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-recon.md) | Reconocimiento general | Recon | 068, 069, **334** |
| [`kali-network-discovery`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-network-discovery.md) | Descubrimiento de hosts en la red | Recon | 029, **334** |
| [`kali-mass-scan`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-mass-scan.md) | Escaneo masivo de puertos | Recon | 030, 031, **334** |
| [`kali-subdomain-enum`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-subdomain-enum.md) | Enumeración de subdominios | Recon | 069, 251 |
| [`kali-vuln-scan`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-vuln-scan.md) | Escaneo de vulnerabilidades | Análisis | **071**, **318** |
| [`kali-waf-detect`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-waf-detect.md) | Detección de WAF | Web | 086, 090 |
| [`kali-web-audit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-web-audit.md) | Auditoría web (OWASP) | Web | Parte 4 (086–115), **336** |
| [`kali-web-fuzz`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-web-fuzz.md) | Fuzzing de rutas/parámetros web | Web | 090, 108, 136 |
| [`kali-wp-audit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-wp-audit.md) | Auditoría de WordPress | Web | Parte 4, **336** |
| [`kali-osint`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-osint.md) | OSINT de fuentes abiertas | Recon/OSINT | Parte 12 (249–260), **336** |
| [`kali-sniff`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-sniff.md) | Captura/análisis de tráfico | Redes | 026, 040 |
| [`kali-brute`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-brute.md) | Ataques de fuerza bruta a credenciales | Acceso | 081 |
| [`kali-hash-crack`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-hash-crack.md) | Cracking de hashes | Credenciales | **080** |
| [`kali-exploit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-exploit.md) | Explotación (supervisada) | Explotación | 072–073, Parte 5, **335** |
| [`kali-ad-audit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-ad-audit.md) | Auditoría de Active Directory | AD | Parte 7 (170–175) |
| [`kali-forensics`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-forensics.md) | Triaje/forense asistido | Defensa/DFIR | Parte 9 (201–220), **337** |
| [`kali-audit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-audit.md) | Auditoría general de seguridad | Auditoría | 285, 318 |
| [`kali-pentest`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-pentest.md) | Orquesta el pentest (sub-agentes en paralelo) | Todo | 066 (PTES), **340** |
| [`kali-finish`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-finish.md) | Consolida hallazgos y genera el **informe** | Reporte | **085**, **338** |
| [`kali-resume`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-resume.md) | Reanuda una sesión previa | Operación | 338 |

## 🔎 Qué hace cada playbook (guía de exploración)

Descripciones **redactadas para el curso** (resumen propio) de qué encontrarás en cada `.md`.
Para ver los **pasos exactos**, abre el archivo enlazado en la tabla de arriba o clónalo:
`git clone https://github.com/pabpereza/kali-mcp`.

**Sesión y orquestación**

- **`kali-start`** — Inicializa la sesión: define objetivo y **alcance**, crea la estructura de carpetas/metadatos y prepara el registro. Es el "contrato" de la sesión.
- **`kali-pentest`** — El **director**: lanza sub-agentes en paralelo por fase, coordina el trabajo y consolida resultados.
- **`kali-resume`** — Reanuda una sesión previa leyendo su estado y continúa donde se quedó.
- **`kali-finish`** — Cierra la sesión: revisa las salidas de los sub-agentes, hace **doble verificación** (completitud, evidencia), detecta huecos (y pregunta si re-ejecutar), y compila un **informe por severidad** con matriz de riesgo, rutas de ataque, remediación y resumen ejecutivo.

**Reconocimiento**

- **`kali-recon`** — Recon (mayormente pasivo): orquesta `nmap -sV -sC`, `whatweb`, `wafw00f`, `gobuster`/`ffuf`, `nikto`, `nuclei`, `enum4linux` y `searchsploit`; entrega tabla de puertos/servicios + vectores priorizados.
- **`kali-network-discovery`** — Descubre hosts vivos en un rango (barrido de red) e inventaría.
- **`kali-mass-scan`** — Escaneo masivo de puertos sobre muchos objetivos para mapear la superficie rápido.
- **`kali-subdomain-enum`** — Enumera subdominios (fuentes pasivas + diccionario DNS) y los resuelve.

**Vulnerabilidades y web**

- **`kali-vuln-scan`** — Escaneo de vulnerabilidades (plantillas `nuclei`, scripts nmap) y correlación con exploits conocidos.
- **`kali-waf-detect`** — Detecta si hay **WAF/IPS** y de qué producto, para ajustar el enfoque.
- **`kali-web-audit`** — Auditoría web: fingerprinting, descubrimiento de contenido, checks OWASP, cabeceras y `nikto`/`nuclei`.
- **`kali-web-fuzz`** — Fuzzing de rutas/parámetros web con diccionarios para hallar contenido oculto.
- **`kali-wp-audit`** — Auditoría específica de **WordPress** (`wpscan`): versión, plugins/temas vulnerables, usuarios.
- **`kali-osint`** — Inteligencia de fuentes abiertas del objetivo (dominios, correos, metadatos) **sin tocarlo**.

**Credenciales y explotación (supervisadas)**

- **`kali-sniff`** — Captura/analiza tráfico de red para observar protocolos y credenciales en claro.
- **`kali-brute`** — Fuerza bruta a servicios de autenticación **dentro del alcance**, con diccionarios.
- **`kali-hash-crack`** — Cracking de hashes capturados con diccionarios/reglas.
- **`kali-exploit`** — Explotación **supervisada**: a partir de los hallazgos, propone y ejecuta PoC con **validación humana** (nunca autónoma).
- **`kali-ad-audit`** — Auditoría de **Active Directory** (enumeración, Kerberos, rutas de ataque) contra un dominio autorizado.

**Auditoría y defensa**

- **`kali-audit`** — Auditoría integral, más profunda que `kali-recon` (recon + vuln + explotación ligera).
- **`kali-forensics`** — Triaje/forense asistido: recolecta artefactos y evidencia para análisis defensivo/IR.

> 🧠 **Lo pedagógico:** fíjate en el patrón común — cada playbook **encadena herramientas → resume con evidencia → guarda en la sesión**, y `kali-finish` **verifica y detecta huecos** antes de reportar. Ese rigor (evidencia, deduplicación, doble chequeo) es exactamente lo que enseñan las clases 085, 318, 321 y 338. La IA acelera el flujo; el método sigue siendo el del pentester profesional.

## 🧭 Cómo usar este catálogo

1. **Aprende la técnica a mano** en la clase indicada (columna derecha).
2. **Entiende el playbook** abriendo su `.md` en el repo oficial: verás cómo un agente encadena las herramientas.
3. **Ejecútalo supervisado** en el [lab kali-mcp-ia](README.md) contra un objetivo propio, **validando** cada resultado (recuerda: la IA alucina — clases 331, 335, 338).
4. **Cierra con `kali-finish`** y verifica el informe contra la evidencia real.

## 🔗 Referencias

- **kali-mcp (MIT)** — <https://github.com/pabpereza/kali-mcp> · carpeta `.claude/commands/`.
- [Lab kali-mcp-ia](README.md) y [Parte 18 — IA aplicada a la ciberseguridad](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/README.md).
