# Playbooks de kali-mcp: análisis en profundidad y mapeo al curso

Los `.md` de `.claude/commands/` de **[kali-mcp](https://github.com/pabpereza/kali-mcp)**
(de *pabpereza*, licencia **MIT**) son **playbooks de pentest orquestado por IA**: cada uno
le indica al agente qué herramientas de Kali ejecutar, en qué orden, con qué controles de
autorización y cómo dejar evidencia. Este documento los **explica en profundidad con palabras
propias** (adaptación educativa), los **mapea a las clases del programa** y propone **mejoras**.

> 🙏 **Atribución.** Diseño y contenido original: **pabpereza/kali-mcp (MIT)**. Aquí se
> **analiza y resume** (no se reproduce el código de los playbooks) para fines didácticos.
> Para el contenido literal: `git clone https://github.com/pabpereza/kali-mcp`.
>
> ⚠️ **Uso ético.** Todo es para pentest **autorizado** (laboratorio propio o permiso escrito).
> La IA acelera; la autorización, la supervisión y la responsabilidad son **humanas** (clases 335, 339).

## 🧠 Los 4 patrones de diseño (lo más valioso)

Antes de los comandos, fíjate en estos patrones — son la lección de ingeniería que puedes
llevarte a cualquier flujo con IA:

1. **Autorización por niveles (scoping).** Casi todos preguntan primero el alcance con opciones
   escalonadas: *pasivo → prueba de credenciales → completo*. Las acciones intrusivas (brute,
   sqlmap, exploit) quedan **detrás de una confirmación explícita**. Es la [Clase 067](../../classes/parte-3-hacking-etico-y-pentesting-metodologia/067-reglas-de-engagement-alcance-y-contratos/README.md) (RoE) hecha código.
2. **Loot-before-exploit + *credential broker*** (en `pentest`/`audit`). El orquestador lanza
   una **Ola A** de solo-reconocimiento donde cada sub-agente termina con `HARVESTED CREDENTIALS:`;
   consolida ese botín; y solo entonces lanza la **Ola B** intrusiva **sembrando** esas
   credenciales — así prueba **reutilización de contraseñas** antes de fuerza bruta ciega. Es
   eficiente y realista (la reutilización es el hallazgo más común). Conecta con 081 y 172.
3. **Persistencia de sesión (evidencia).** Todo se guarda en `sessions/<target>_<fecha>/`
   (`session.md`, `targets.md`, `findings.md`, `assets/`). Reproducibilidad y trazabilidad —
   [Clase 085](../../classes/parte-3-hacking-etico-y-pentesting-metodologia/085-reporte-profesional-de-pentest/README.md) y 321.
4. **Control de calidad en el cierre** (`finish`). No confía a ciegas: **verifica** que cada
   sub-agente produjo salida real, **detecta huecos**, **deduplica** y clasifica por severidad
   con matriz de riesgo y remediación. Antídoto contra las alucinaciones (clases 331, 338).

## 🗺️ Índice rápido (playbook ↔ fase ↔ clases)

| Playbook | Fase | Clases del curso |
|---|---|---|
| [`kali-start`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-start.md) | Planificación | 067, 340 |
| [`kali-network-discovery`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-network-discovery.md) | Descubrimiento | 029, 334 |
| [`kali-mass-scan`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-mass-scan.md) | Descubrimiento | 030, 031, 334 |
| [`kali-recon`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-recon.md) | Recon | 068, 069, 334 |
| [`kali-osint`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-osint.md) | OSINT | Parte 12, 336 |
| [`kali-subdomain-enum`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-subdomain-enum.md) | Recon | 069, 251 |
| [`kali-vuln-scan`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-vuln-scan.md) | Análisis | 071, 318 |
| [`kali-waf-detect`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-waf-detect.md) | Web | 086, 113 |
| [`kali-web-audit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-web-audit.md) | Web | Parte 4, 336 |
| [`kali-web-fuzz`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-web-fuzz.md) | Web | 090, 108, 136 |
| [`kali-wp-audit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-wp-audit.md) | Web | Parte 4, 336 |
| [`kali-sniff`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-sniff.md) | Redes | 026, 040 |
| [`kali-brute`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-brute.md) | Credenciales | 081 |
| [`kali-hash-crack`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-hash-crack.md) | Credenciales | 080, 057 |
| [`kali-exploit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-exploit.md) | Explotación | 072, 073, Parte 5, 335 |
| [`kali-ad-audit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-ad-audit.md) | AD | 170–175 |
| [`kali-forensics`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-forensics.md) | Forense | 064, Parte 9, 337 |
| [`kali-audit`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-audit.md) | Orquestación | 066, 285, 340 |
| [`kali-pentest`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-pentest.md) | Orquestación | 066, 340 |
| [`kali-finish`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-finish.md) | Reporte | 085, 338 |
| [`kali-resume`](https://github.com/pabpereza/kali-mcp/blob/main/.claude/commands/kali-resume.md) | Operación | 338 |

## 🔎 Análisis en profundidad

### Sesión y orquestación

**`kali-start`** — Prepara la sesión antes de tocar nada: pide objetivo(s), **tipo de engagement**
y **nivel de autorización**, y crea `sessions/<target>_<fecha>/` con `session.md` (estado `IN
PROGRESS`), `targets.md` y `assets/`. Es el "contrato" y el cuaderno de bitácora. → *Clase 067.*
**💡 Mejora:** guardar en `session.md` la **evidencia de autorización** (quién autorizó, ventana,
IPs en alcance) y una lista de exclusiones para que los demás playbooks la respeten.

**`kali-pentest`** — El **orquestador**: hace un `nmap` inicial, pregunta el alcance y lanza
**sub-agentes en paralelo, uno por servicio**, con el patrón de **dos olas** (recon/loot →
explotación sembrada con el botín). Consolida el informe final. → *Clases 066, 340.*
**💡 Mejora:** un **guard de alcance** central que rechace cualquier IP fuera de `targets.md`
antes de ejecutar, y límites de tasa por defecto para no saturar.

**`kali-audit`** — Variante por servicio: descubre puertos y lanza **un sub-agente por puerto**
con un *prompt* especializado por protocolo (HTTP, SSH, FTP, SMB, MySQL, RDP, SNMP, LDAP, DNS…),
también con el broker de credenciales entre olas. → *Clases 066, 285.*
**💡 Mejora:** externalizar los *prompts* por servicio a plantillas versionadas y añadir un
servicio "IoT/OT" con precauciones (no sondear agresivamente equipos industriales).

**`kali-resume`** — Reanuda una sesión: lista las existentes, carga `session.md`/`assets/`,
resume estado y **huecos**, y sugiere siguientes pasos. → *Clase 338.*
**💡 Mejora:** un `diff` de qué cambió desde la última vez y detección de resultados **caducados**
(re-escanear si pasaron N días).

**`kali-finish`** — El **finalizador de calidad**: inventaría los `assets/`, **verifica** que
cada sub-agente entregó resultados reales (no errores), **detecta huecos** (y ofrece re-ejecutar),
**deduplica** hallazgos y compila `findings.md` por severidad con matriz de riesgo, rutas de
ataque y remediación. → *Clases 085, 338.*
**💡 Mejora:** exigir **evidencia reproducible por hallazgo** (comando + salida) y marcar como
"sin verificar" todo lo que no la tenga — cierra la puerta a hallazgos alucinados.

### Reconocimiento

**`kali-network-discovery`** — Descubre hosts vivos en un rango (`nmap -sn`), luego escaneo
rápido de top-100, fingerprint de OS y versión, y **paraleliza un sub-agente por host**. Entrega
un mapa de red. → *Clases 029, 334.* **💡 Mejora:** preferir descubrimiento por ARP en LAN
(menos ruidoso) y respetar una lista de exclusión.

**`kali-mass-scan`** — Velocidad: `masscan` (top-ports o 1-65535) con tasa configurable, parseo
a tabla IP→puertos, y **verificación dirigida con `nmap -sV`** solo sobre lo que salió abierto.
→ *Clases 030, 031.* **💡 Mejora:** tasa por defecto conservadora y aviso de que masscan puede
tumbar servicios frágiles; guardar la tasa usada en la evidencia.

**`kali-recon`** — Recon **pasivo** encadenado: `nmap -sV -sC` → `whatweb` → `wafw00f` →
`gobuster`/`ffuf` → `nikto` → `nuclei` (critical/high) → `enum4linux`/`crackmapexec --shares` →
`ssl-enum-ciphers` → `searchsploit`. Entrega puertos/servicios + **vectores priorizados**.
→ *Clases 068, 069, 334.* **💡 Mejora:** cachear resultados para no repetir escaneos y añadir
un modo "solo pasivo real" que no lance `nikto`/`gobuster` (que sí tocan el objetivo).

**`kali-osint`** — Sin tocar el objetivo: `whois`, `dig ANY/MX/NS/TXT` (SPF/DKIM/DMARC),
`whatweb`, `theHarvester`, `fierce`, `dnsrecon`, `sublist3r`, `amass -passive`. → *Parte 12, 336.*
**💡 Mejora:** deduplicar subdominios/correos entre herramientas y **respetar privacidad**
(no perfilar personas; solo superficie técnica).

**`kali-subdomain-enum`** — Especialista en subdominios: pasivo (`sublist3r`, `amass`,
`theHarvester`) + DNS (`fierce`, `dnsrecon`, `axfr`) + **vhosts** (`ffuf -H "Host: FUZZ"`) +
validación (resolución e `whatweb`). → *Clases 069, 251.* **💡 Mejora:** correlacionar por IP
para detectar *dev/staging* y marcar subdominios con certificados expirados.

### Vulnerabilidades y web

**`kali-vuln-scan`** — Identificación **sin explotar**: `nmap --script vuln`, `nuclei`, `nikto`,
scripts SMB (`smb-vuln-*`), SSL (`ssl-poodle`/`heartbleed`), `searchsploit`, `wafw00f`. Entrega
tabla de CVEs con severidad. → *Clases 071, 318.* **💡 Mejora:** enriquecer cada CVE con **EPSS y
CISA KEV** para priorizar por explotación real (justo lo de la clase 318), no solo por CVSS.

**`kali-waf-detect`** — Perfila el WAF/IPS: `wafw00f -a`, fingerprint manual por cabeceras
(`cf-ray`, `X-Sucuri`…), payloads de prueba (SQLi/XSS/traversal) midiendo el código de respuesta,
análisis de **cabeceras de seguridad** y detección de **rate limiting**. → *Clases 086, 113.*
**💡 Mejora:** no lanzar payloads de prueba en modo pasivo; y correlacionar con la clase 113
(CORS/headers) para un scorecard de cabeceras.

**`kali-web-audit`** — Auditoría web con **dos niveles** (pasivo: `nikto`/`gobuster`/`dirb`/`wpscan`;
completo: añade `sqlmap`). → *Parte 4, 336.* **💡 Mejora:** sustituir `dirb` (lento) por `feroxbuster`
y validar SQLi con una PoC de bajo impacto antes de volcar datos.

**`kali-web-fuzz`** — Fuzzing avanzado: `ffuf` (directorios/archivos/backups/extensiones), `wfuzz`,
**descubrimiento de parámetros con `arjun`**, y `nuclei`; opción de inyección de comandos con
`commix`. → *Clases 090, 108, 136.* **💡 Mejora:** calibrar el filtro de tamaño (`-fs`) por baseline
para reducir ruido y limitar la recursión para no explotar en peticiones.

**`kali-wp-audit`** — WordPress: `wpscan` (versión/CVEs, plugins, temas, usuarios) + `gobuster`;
opción de fuerza bruta a `wp-login.php`. → *Parte 4, 336.* **💡 Mejora:** usar un **API token de
WPScan** para datos de vulnerabilidades al día y avisar del riesgo de lockout antes de la fuerza bruta.

### Redes, credenciales y explotación (supervisadas)

**`kali-sniff`** — Captura/analiza tráfico: descubre interfaces, captura acotada con `tcpdump`
(por tiempo/paquetes/puerto) y analiza con `tshark` (jerarquía de protocolos, conversaciones,
**extracción de credenciales en claro** HTTP-Basic/FTP, DNS, anomalías). → *Clases 026, 040.*
**💡 Mejora:** hashear/**redactar** las credenciales capturadas en el informe y recordar el marco
legal de la interceptación (solo tu red).

**`kali-brute`** — Fuerza bruta con `hydra` (SSH/FTP/HTTP-form…), autorización **obligatoria** con
opción de diccionario reducido (top-50) para minimizar impacto. → *Clase 081.* **💡 Mejora:** por
defecto **no** usar `rockyou`; respetar la política de lockout descubierta y parar al primer acierto.

**`kali-hash-crack`** — Identifica el tipo de hash (`hash-identifier`/`hashid`) y crackea con
`john`/`hashcat` (diccionario → reglas `best64` → fuerza bruta corta), con generación de
diccionarios a medida (`cewl`, `crunch`). → *Clases 080, 057.* **💡 Mejora:** detectar el modo
hashcat automáticamente y **nunca** exfiltrar los hashes originales a un servicio externo.

**`kali-exploit`** — Explotación con autorización **obligatoria** y una opción clave **"verify
only"** (confirmar la vuln con scripts nmap sin lanzar payloads). Si se autoriza: verifica →
elige módulo (`msfconsole`) → configura → ejecuta → post-explotación mínima (`whoami`, `id`).
→ *Clases 072, 073, Parte 5, 335.* **💡 Mejora:** **snapshot** del objetivo antes de explotar y
registro inmutable de cada payload enviado (trazabilidad legal).

**`kali-ad-audit`** — Active Directory por niveles: enumeración (`enum4linux`, `crackmapexec`,
`smbclient`, scripts SMB/LDAP) → prueba de credenciales (spraying, null session) → avanzado
(`impacket-secretsdump`/`psexec`, AS-REP Roasting, Kerberoasting, Responder, Pass-the-Hash).
→ *Clases 170–175.* **💡 Mejora:** por defecto quedarse en enumeración; el `Responder` en modo
activo es muy intrusivo — exigir confirmación separada y ventana pactada.

### Forense (defensivo)

**`kali-forensics`** — Análisis de un archivo/imagen: identifica el tipo (`file`, cabecera hex),
extrae **metadatos** (`exiftool`, GPS/autor), **strings** (ASCII/UTF-16 buscando URLs/claves),
**archivos embebidos** (`binwalk`, `foremost`, entropía), **esteganografía** (`steghide`, `zsteg`),
disco/archivo (`fdisk`, montaje ro, ZIP) y hashes de integridad. → *Clases 064, Parte 9, 337.*
**💡 Mejora:** calcular el hash **antes** de tocar nada (cadena de custodia) y trabajar siempre
sobre una **copia**, nunca el original.

## 🧭 Cómo estudiarlos (recorrido sugerido)

1. **Aprende la técnica a mano** en la clase de la columna derecha (no supervisas lo que no entiendes).
2. **Lee el playbook** en el repo (enlace del índice) y compara con el análisis de arriba.
3. **Fíjate en los 4 patrones** — son transferibles a cualquier automatización con IA.
4. **Ejecútalo supervisado** en el [lab kali-mcp-ia](README.md) contra un objetivo **propio**,
   validando cada resultado (la IA alucina — clases 331, 335, 338), y cierra con `kali-finish`.

## 🔗 Referencias

- **kali-mcp (MIT)** — <https://github.com/pabpereza/kali-mcp> · carpeta `.claude/commands/`.
- [Lab kali-mcp-ia](README.md) y [Parte 18 — IA aplicada a la ciberseguridad](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/README.md).
