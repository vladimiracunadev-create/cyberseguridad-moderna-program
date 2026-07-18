# 🔵 Analista SOC / Blue Team

> Detección, monitoreo, threat hunting y respuesta temprana: eres los ojos que ven
> al atacante cuando todavía se puede parar.
>
> **Nivel de entrada:** accesible; es de las mejores puertas de entrada a la ciberseguridad · **Foco:** telemetría, SIEM, detección, threat hunting y respuesta a incidentes · **Certificación faro:** BTL1

## 🧭 Qué es y por qué importa

El **blue team** es el equipo defensor. Mientras el red team ataca, el blue team **detecta,
contiene y responde**. El corazón operativo de esa defensa es el **SOC** (Security Operations
Center): el centro donde se centraliza la telemetría de toda la organización — logs de red,
endpoints, servidores, nube, identidad — y desde donde se vigila 24/7 buscando señales de
compromiso.

Un SOC se organiza por **niveles**, y entender esto es clave antes de postularte:

- **L1 — Analista de triaje.** La primera línea. Recibe las alertas que dispara el SIEM, las
  clasifica (¿es real o falso positivo?), enriquece con contexto básico y escala lo que importa.
  Es la puerta de entrada más común al oficio. También es el nivel con más ruido y más fatiga:
  gran parte de tu jornada es descartar falsos positivos.
- **L2 — Analista de investigación.** Toma lo que L1 escala y lo investiga a fondo: correlaciona
  eventos, reconstruye la línea de tiempo de un incidente, decide si hay que contener. Requiere
  más criterio y más conocimiento técnico.
- **L3 — Threat hunter / ingeniero de detección.** No espera a la alerta: **caza** amenazas de
  forma proactiva formulando hipótesis, y **construye** las reglas de detección que L1 y L2 usarán
  mañana. Es el nivel más creativo y mejor pagado del SOC operativo.

Sobre esto se apoyan roles vecinos: **respuesta a incidentes (IR)**, **forense (DFIR)**,
**threat intelligence** e **ingeniería de detección**. Muchas carreras defensivas empiezan como
L1 y de ahí divergen.

Un matiz honesto sobre los **turnos**: un SOC que vigila 24/7 necesita cobertura nocturna y de
fin de semana. En L1 es habitual rotar turnos, incluidos nocturnos. No es para siempre — es el
peaje de entrada — pero conviene saberlo antes, no después. Lo compensa que **el blue team es de
los caminos con la barrera de entrada más baja y la demanda más alta** del sector.

## 🗓️ Un día en el puesto

Un turno típico de un analista L1/L2 se parece a esto:

- **Relevo y contexto:** recibes el traspaso del turno anterior — incidentes abiertos, alertas
  en curso, campañas que vigilar.
- **Cola de alertas:** el grueso del día. Tomas alertas del SIEM una por una, decides si son
  falsos positivos (la mayoría lo serán) o si merecen escalar, y las documentas. La disciplina
  de **no cerrar en automático** lo que parece rutinario es lo que separa a un buen analista.
- **Investigación:** ante una alerta seria, pivotas entre fuentes — logs de endpoint, tráfico de
  red, eventos de Windows — para reconstruir qué pasó y si hay más máquinas afectadas.
- **Threat hunting (si el SOC madura):** ratos dedicados a buscar proactivamente lo que ninguna
  regla detectó todavía, partiendo de una hipótesis concreta ("¿hay beaconing hacia dominios
  recién registrados?").
- **Escalado y handoff:** documentas y pasas a L2/IR lo que lo requiere, y dejas el traspaso
  limpio para el siguiente turno.

Dicho sin adornos: hay **fatiga de alertas** y mucho **ruido**. La habilidad no es ver una
película de hacking, es mantener la atención y el criterio cuando la alerta número 200 del día
parece igual a las 199 anteriores — y la 201 es la buena.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **Redes de verdad.** TCP/IP, DNS, HTTP, proxies. No puedes detectar tráfico malicioso si no
  sabes cómo se ve el legítimo. Es la base número uno del rol.
- **Sistemas operativos y sus logs.** Windows sobre todo (Event Logs, Sysmon, procesos, servicios,
  registro) y Linux. La telemetría de endpoint es donde vive la mayoría de las detecciones.
- **El SIEM como herramienta central:** cómo se ingiere la telemetría, cómo se normaliza y cómo se
  consulta. Saber escribir búsquedas (SPL, KQL o similar) es pan de cada día.
- **MITRE ATT&CK.** El lenguaje común de la detección. Mapear alertas a técnicas concretas
  estructura todo tu trabajo.
- **Comportamiento del malware y del atacante:** cómo se ve el movimiento lateral, el C2, el
  beaconing, la persistencia — para reconocerlos en los logs.

### Herramientas del oficio

```text
SIEM:            Splunk, Elastic Stack, Microsoft Sentinel, Wazuh
Detección:       reglas Sigma, MITRE ATT&CK, YARA
EDR/Endpoint:    Sysmon, Velociraptor, EDR comerciales (CrowdStrike, Defender)
Red/NSM:         Zeek, Suricata, Wireshark, NetFlow
Threat Intel:    MISP, OpenCTI, feeds de IoC
Automatización:  SOAR, Python para enriquecer y automatizar triaje
```

Ninguna herramienta te vuelve analista por sí sola. El SIEM sin criterio solo te entrega más
alertas que ignorar. Lo que se paga es tu capacidad de **interpretar** lo que la herramienta
muestra.

### Habilidades no técnicas

- **Atención sostenida y criterio bajo ruido:** la habilidad central del L1.
- **Comunicación clara:** un escalado mal escrito hace perder tiempo crítico. Documentar bien es
  parte del trabajo, no un extra.
- **Curiosidad metódica:** el threat hunter que hay en ti nace de preguntar "¿y si...?" y saber
  perseguir la respuesta sin desviarte.
- **Aguante para el turno:** gestionar la rotación y la carga sin que el criterio se resienta.

## 📚 Tu ruta en el programa

Orden recomendado (según el [índice de rutas](./README.md)):

1. 📚 [**Parte 0** — Fundamentos y prerrequisitos](../classes/parte-0-fundamentos-y-prerrequisitos/README.md) (001–025) · Linux, Windows, redes y Python: la base sin la que nada de lo demás se sostiene.
2. 📚 [**Parte 1** — Redes y seguridad de redes](../classes/parte-1-redes-y-seguridad-de-redes/README.md) (026–045) · captura de tráfico, IDS/IPS y NSM: aprendes a ver la red.
3. 📚 [**Parte 6** — Análisis de malware](../classes/parte-6-analisis-de-malware/README.md) (141–160) · triaje y comportamiento: reconocer qué hace un binario sospechoso.
4. 📚 [**Parte 8** — Blue Team, detección y SOC](../classes/parte-8-blue-team-deteccion-y-soc/README.md) (181–200) · el núcleo del rol.
5. 📚 [**Parte 9** — Forense digital y respuesta a incidentes](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/README.md) (201–220) · qué hacer cuando la detección se confirma.

Clases concretas por las que empezar (el corazón está en la Parte 8):

- 🏢 [181 · El SOC moderno: roles, niveles y procesos](../classes/parte-8-blue-team-deteccion-y-soc/181-el-soc-moderno-roles-niveles-y-procesos/README.md) — el mapa del oficio antes que cualquier herramienta.
- 🗃️ [183 · SIEM: arquitectura y componentes](../classes/parte-8-blue-team-deteccion-y-soc/183-siem-arquitectura-y-componentes/README.md) — cómo se ingiere y consulta la telemetría.
- 🔎 [184 · Splunk para detección](../classes/parte-8-blue-team-deteccion-y-soc/184-splunk-para-deteccion/README.md) — el SIEM más pedido en ofertas, con las manos en el teclado.
- ✍️ [186 · Escritura de reglas de detección con Sigma](../classes/parte-8-blue-team-deteccion-y-soc/186-escritura-de-reglas-de-deteccion-con-sigma/README.md) — de consumidor de alertas a autor de detecciones.
- 🧬 [187 · Detección basada en MITRE ATT&CK](../classes/parte-8-blue-team-deteccion-y-soc/187-deteccion-basada-en-mitre-att-ck/README.md) — el lenguaje común que estructura todo.
- 🏹 [188 · Threat hunting: metodología](../classes/parte-8-blue-team-deteccion-y-soc/188-threat-hunting-metodologia/README.md) — cazar antes de que salte la alerta.
- 💻 [189 · Análisis de endpoints con EDR](../classes/parte-8-blue-team-deteccion-y-soc/189-analisis-de-endpoints-con-edr/README.md) — donde vive la mayoría de las detecciones modernas.

Refuerzo desde las Partes 1, 6 y 9:

- 🌐 [043 · Network Security Monitoring (NSM): fundamentos](../classes/parte-1-redes-y-seguridad-de-redes/043-network-security-monitoring-nsm-fundamentos/README.md) — la disciplina de vigilar la red.
- 🦠 [148 · Análisis de comportamiento](../classes/parte-6-analisis-de-malware/148-analisis-de-comportamiento/README.md) — qué hace el malware, para reconocerlo en los logs.
- 🚨 [215 · Playbooks de respuesta a incidentes](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/215-playbooks-de-respuesta-a-incidentes/README.md) — el guion cuando la detección se confirma.

### Laboratorio y CTF

- 🧪 [`blue-team-soc`](../labs/blue-team-soc/README.md) — tu SOC de práctica: monta un SIEM,
  ingiere telemetría, escribe reglas y triaja alertas reales generadas contra tu propio entorno.
- 🚩 [CTF de forense y redes](../ctf/README.md) — los retos de **forense** y **redes** entrenan
  justo los músculos del blue team: leer una captura, seguir un flujo, reconstruir qué pasó.

## 🎓 Certificaciones

Con archivo en el programa (mapean a partes concretas):

- 🥇 [**BTL1** (Blue Team Level 1)](../certificaciones/btl1.md) — la **certificación faro** del rol:
  cien por cien práctica, cubre SIEM, análisis de logs, threat intel, forense y respuesta a
  incidentes. Es la que mejor demuestra que sabes hacer el trabajo, no solo hablar de él.
- 📋 [**CompTIA CySA+** (CS0-003)](../certificaciones/comptia-cysa-plus-cs0-003.md) — analista de
  seguridad con foco en detección y análisis de comportamiento. Buen complemento teórico y muy
  reconocida en ofertas de empleo.
- 🎓 [**CompTIA Security+** (SY0-701)](../certificaciones/comptia-security-plus-sy0-701.md) — la
  certificación **de entrada** al sector. No es específica de blue team, pero abre muchas puertas
  de RRHH y asienta el vocabulario común.

Para especializarte más adelante en respuesta e incidentes:

- 🏛️ [**SANS GCIH / GCFA**](../certificaciones/sans-gcih-gcfa.md) — manejo de incidentes y forense
  avanzado. Caras, pero de las más respetadas para dar el salto a DFIR senior.

Consulta el [mapeo completo a certificaciones](../certificaciones/README.md) para ver cuánto cubre
el programa de cada examen.

## 📈 Progresión de carrera y salario

Ruta habitual: **SOC L1 → SOC L2 → L3 / Threat Hunter → Detection Engineer o IR/DFIR → SOC Lead /
Manager**. Desde L2/L3 se abren también los caminos de **threat intelligence**, **ingeniería de
detección** y **respuesta a incidentes**, que suelen pagar por encima del SOC operativo.

Rangos **orientativos y aproximados** (varían mucho por empresa, sector y experiencia; el blue
team es de los roles con **entrada más accesible**, y eso presiona los salarios junior a la baja
frente a la ofensiva):

```text
Región            L1/entrada           L2/L3 · hunter/IR senior
----------------  -------------------  ------------------------
LATAM             USD 12k – 28k / año  USD 30k – 55k+ / año
España            EUR 22k – 35k / año  EUR 40k – 65k+ / año
Remoto (USD)      USD 55k – 85k / año  USD 100k – 150k+ / año
```

Los números remotos en USD asumen contratación por empresas de EE. UU./Europa, muy competida y
con listón alto de inglés. La buena noticia del rol: la **abundancia de plazas L1** hace que sea
uno de los primeros empleos reales más alcanzables del sector — y desde dentro, subir de nivel
depende sobre todo de lo que aprendas en el turno.

## ⚠️ Mitos y errores comunes

- **"El SOC es aburrido / es solo mirar pantallas."** Hay ruido, sí, pero el trabajo de fondo —
  reconstruir un incidente, cazar lo que nadie detectó — es de los más intelectualmente exigentes
  de la ciberseguridad.
- **"L1 es un callejón sin salida."** Al contrario: es la mejor rampa de lanzamiento. Casi todos
  los DFIR, threat hunters e ingenieros de detección empezaron triando alertas.
- **"El SIEM detecta solo; yo apruebo."** El SIEM entrega alertas, no veredictos. El criterio para
  separar señal de ruido lo pones tú, y es justo lo que se paga.
- **"Necesito ser un experto ofensivo antes de defender."** No. Ayuda entender el ataque, pero se
  entra a blue team con fundamentos sólidos de redes y sistemas, sin pasar por OSCP.
- **"Los turnos nocturnos son para siempre."** Son el peaje de L1 en muchos SOC, no una condena.
  Al subir de nivel, la rotación se suaviza o desaparece.

## 🚀 Siguientes pasos

1. **Asienta la base** con las **Partes 0 y 1**: sin redes y sistemas sólidos, las alertas no te
   dirán nada.
2. Haz la **Parte 8** completa y monta el laboratorio [`blue-team-soc`](../labs/blue-team-soc/README.md):
   ingiere telemetría real y escribe tus primeras reglas.
3. Practica lectura forense con los [CTF de forense y redes](../ctf/README.md) y refuerza con la
   **Parte 9**.
4. Apunta a **BTL1** como certificación de rol; si buscas primero abrir puertas de RRHH, empieza
   por **Security+**.
5. Construye **evidencia pública**: writeups de tus investigaciones de laboratorio, reglas Sigma
   propias, análisis de capturas. En defensa, demostrar que sabes triar y cazar vale más que
   cualquier título.

---

- ⬅️ [Volver al índice de rutas](./README.md)
- 🏠 [Inicio del programa](../README.md)
