# 🕵️ DFIR / Analista forense

> Adquisición, memoria, timelines y respuesta a incidentes: cuando la alerta ya se
> confirmó, eres quien reconstruye qué pasó, contiene el daño y sostiene la evidencia
> con rigor suficiente para que aguante en un tribunal.
>
> **Nivel de entrada:** intermedio; conviene llegar con base de blue team o sysadmin, no es una primera puerta típica · **Foco:** adquisición forense, memoria, timelines, respuesta a incidentes y cadena de custodia · **Certificación faro:** GCFA (SANS)

## 🧭 Qué es y por qué importa

**DFIR** son dos disciplinas hermanas que casi siempre viajan juntas: **forense digital**
(*Digital Forensics*) — extraer y analizar evidencia de sistemas comprometidos — y
**respuesta a incidentes** (*Incident Response*) — el proceso operativo de gestionar un
compromiso de principio a fin. El forense te dice **qué pasó**; la respuesta decide **qué
hacer al respecto**, y a menudo bajo el reloj.

El marco de referencia del oficio es el **ciclo de respuesta a incidentes** (NIST 800-61 /
SANS PICERL). Sus fases:

- **Preparación.** Todo lo que haces *antes* del incidente: playbooks, herramientas listas,
  telemetría activada, contactos claros. El incidente se gana o se pierde aquí.
- **Identificación.** Confirmar que hay un incidente real, delimitar su alcance y clasificar
  su severidad. Es donde el DFIR recoge el testigo de la detección del SOC.
- **Contención.** Frenar la hemorragia sin destruir evidencia: aislar máquinas, cortar
  cuentas, bloquear C2 — pero preservando lo que necesitarás analizar.
- **Erradicación.** Sacar al atacante del entorno: eliminar persistencia, malware y accesos.
- **Recuperación.** Restaurar operaciones de forma segura y vigilada, verificando que el
  atacante no vuelve.
- **Lecciones aprendidas.** El *post-mortem* honesto: qué falló, qué detectó, qué se mejora.
  La fase que más se salta y la que más valor deja.

Dentro del forense hay tres frentes, cada uno con su ventana de oportunidad:

- **Forense de disco.** El almacenamiento persistente: sistema de archivos, artefactos de
  Windows/Linux, navegadores, ficheros borrados. Es lo más completo pero también lo más lento.
- **Forense de memoria.** La RAM del sistema vivo: procesos ocultos, inyecciones, claves,
  conexiones, malware *fileless* que nunca tocó el disco. Es **volátil** — si la máquina se
  apaga, se pierde para siempre. Por eso el orden de adquisición importa tanto.
- **Forense de red.** Capturas, flujos y metadatos: C2, exfiltración, movimiento lateral.
  Ve lo que cruzó el cable aunque el endpoint esté limpio.

Y por encima de toda la técnica está la **cadena de custodia**: el registro documentado de
quién tocó cada pieza de evidencia, cuándo, cómo y con qué integridad (hashes). Sin ella, el
mejor análisis del mundo no vale nada en un procedimiento legal. En DFIR el rigor
procedimental **no es burocracia**: es la mitad del trabajo. Una imagen adquirida sin
verificar su hash, o un disco tocado sin bloqueador de escritura, contamina la evidencia de
forma irreversible.

## 🗓️ Un día en el puesto

Hay dos modos de vida en DFIR, y son muy distintos:

- **Modo calma (la mayoría del tiempo).** Preparas y afinas: escribes y pruebas playbooks,
  mejoras la telemetría con el equipo de detección, revisas casos cerrados, investigas
  incidentes de baja prioridad, montas y documentas herramientas de adquisición, y te formas.
  Es trabajo metódico y de documentación.
- **Modo incidente (cuando salta el grande).** El ritmo cambia por completo. Adquieres
  evidencia contra reloj respetando el orden de volatilidad, dumpeas memoria, construyes
  timelines, correlacionas artefactos, informas a dirección cada pocas horas y coordinas
  contención con IT. Puede durar días, con guardias y noches.

Dicho sin adornos: **el modo incidente es estresante**. Hay presión de negocio (cada hora de
caída cuesta dinero), incertidumbre técnica, y la responsabilidad de no destruir evidencia
mientras todos te piden respuestas ya. Si un incidente puede acabar en litigio o en denuncia,
cada paso que das lo escribes pensando en que un abogado lo va a leer. No es el trabajo
frenético de las películas: es concentración sostenida bajo presión, con disciplina de notario.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **Interioridades de sistemas operativos.** Windows a fondo (registro, MFT, Prefetch, Event
  Logs, ShimCache, Amcache, procesos y servicios) y Linux (logs, sistema de archivos,
  artefactos de usuario). Aquí es donde vive la evidencia.
- **Sistemas de archivos.** NTFS y ext4 al nivel de metadatos: timestamps `$MFT`/`$LogFile`,
  inodos, journaling. Entenderlos es lo que te deja detectar manipulación temporal
  (*timestomping*) y recuperar lo borrado.
- **Memoria y procesos.** Cómo se estructura la RAM: espacios de proceso, DLLs, handles,
  inyección de código. Es la base para leer un volcado con criterio.
- **Redes.** TCP/IP, DNS, HTTP y cómo se ve el C2 y la exfiltración en una captura.
- **Comportamiento de malware y del atacante.** Persistencia, movimiento lateral, *living off
  the land*. Reconocer las técnicas te dice qué buscar y dónde.
- **MITRE ATT&CK.** El lenguaje común para mapear lo que hizo el atacante y estructurar el informe.

### Herramientas del oficio

```text
Adquisición:     FTK Imager, dd/dcfldd, Guymager, KAPE, bloqueadores de escritura
Memoria:         Volatility 3, Rekall, WinPmem, LiME, MemProcFS
Disco/artefactos: Autopsy, The Sleuth Kit, Eric Zimmerman Tools (MFTECmd, EvtxECmd, ...)
Timelines:       Plaso/log2timeline, Timeline Explorer, Timesketch
Red:             Wireshark, Zeek, NetworkMiner, tshark
Malware/triaje:  YARA, CyberChef, PE tools, sandbox
Gestión de caso: cadena de custodia, hashing (MD5/SHA-256), documentación
```

Ninguna herramienta hace forense por ti. Volatility te lista procesos; **interpretar** cuál
es una inyección y cuál un servicio legítimo lo pones tú. Lo que se paga es el criterio, no el
saber apretar botones.

### Habilidades no técnicas

- **Rigor y trazabilidad obsesivos.** Todo se documenta, todo se hashea, nada se toca sin
  registrar. Es el hábito que define al profesional.
- **Escritura clara para audiencias distintas.** El mismo incidente lo cuentas a un ingeniero,
  a un directivo y, eventualmente, a un juez. Saber traducir hallazgos técnicos a un informe
  legible es una habilidad central del rol, no un extra.
- **Aguante bajo presión.** Mantener el método cuando hay caída de producción y todos empujan.
- **Nociones legales.** Saber qué hace admisible una evidencia, cuándo hay que involucrar a
  legal y cómo no contaminar la cadena de custodia.
- **Ética y discreción.** Manejas datos sensibilísimos de la organización y de personas.

## 📚 Tu ruta en el programa

Orden recomendado (según el [índice de rutas](./README.md)):

1. 📚 [**Parte 0** — Fundamentos y prerrequisitos](../classes/parte-0-fundamentos-y-prerrequisitos/README.md) (001–025) · Linux, Windows, redes, Python y sistemas operativos: la base sin la que el forense no se sostiene.
2. 📚 [**Parte 1** — Redes y seguridad de redes](../classes/parte-1-redes-y-seguridad-de-redes/README.md) (026–045) · captura y análisis de tráfico: el frente de red del forense.
3. 📚 [**Parte 6** — Análisis de malware](../classes/parte-6-analisis-de-malware/README.md) (141–160) · reconocer qué hace un binario que encuentres en un endpoint comprometido.
4. 📚 [**Parte 9** — Forense digital y respuesta a incidentes](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/README.md) (201–220) · **el núcleo del rol**.
5. 📚 [**Parte 8** — Blue Team, detección y SOC](../classes/parte-8-blue-team-deteccion-y-soc/README.md) (181–200) · para cerrar el ciclo **detección → respuesta**: entiendes de dónde vienen las alertas que investigas.

Clases concretas por las que empezar (el corazón está en la Parte 9):

- ⚖️ [201 · Fundamentos de DFIR y cadena de custodia](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/201-fundamentos-de-dfir-y-cadena-de-custodia/README.md) — arranca por aquí: sin cadena de custodia, nada de lo demás vale.
- 🔄 [202 · El ciclo de respuesta a incidentes: NIST y SANS](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/202-el-ciclo-de-respuesta-a-incidentes-nist-y-sans/README.md) — el marco que estructura todo el trabajo.
- 💽 [203 · Adquisición forense: discos e imágenes](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/203-adquisicion-forense-discos-e-imagenes/README.md) — copiar evidencia sin alterarla, con verificación de integridad.
- 🧠 [207 · Forense de memoria RAM con Volatility](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/207-forense-de-memoria-ram-con-volatility/README.md) — la joya del oficio: procesos ocultos, inyecciones y malware *fileless*.
- 🕰️ [209 · Análisis de línea de tiempo (timeline)](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/209-analisis-de-linea-de-tiempo-timeline/README.md) — reconstruir el orden exacto de los hechos, el entregable estrella del forense.
- 🚨 [215 · Playbooks de respuesta a incidentes](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/215-playbooks-de-respuesta-a-incidentes/README.md) — el guion que ejecutas cuando salta el incidente.

Refuerzo desde las Partes 6 y 9:

- 🦠 [148 · Análisis de comportamiento](../classes/parte-6-analisis-de-malware/148-analisis-de-comportamiento/README.md) — qué hace un binario, para reconocerlo entre los artefactos.
- 📝 [218 · Reporte forense y aspectos legales](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/218-reporte-forense-y-aspectos-legales/README.md) — traducir hallazgos a un informe que aguante en un tribunal.

### Laboratorio y CTF

- 🧪 [`dfir-memoria`](../labs/dfir-memoria/README.md) — tu laboratorio central: adquiere un
  volcado de memoria, lo analizas con Volatility y reconstruyes qué hizo el malware en un
  sistema comprometido.
- 🧪 [`blue-team-soc`](../labs/blue-team-soc/README.md) — para el lado de detección del ciclo:
  entender cómo nace la alerta que luego investigas como responder.
- 🚩 [CTF de forense](../ctf/README.md) — los retos de **forense** son el entrenamiento más
  directo del rol: leer una imagen, tirar de un timeline, seguir el rastro y contar la historia.

## 🎓 Certificaciones

Con archivo en el programa (mapean a partes concretas):

- 🏛️ [**SANS GCFA / GCIH**](../certificaciones/sans-gcih-gcfa.md) — la **referencia faro** del
  rol. **GCFA** (forense y respuesta avanzada) y **GCIH** (manejo de incidentes) son de las
  credenciales más respetadas para DFIR. Son **caras** — formación SANS de varios miles de
  dólares/euros — pero abren puertas senior como pocas. La **GCFE** (examiner) es su hermana de
  entrada más orientada a forense de Windows.
- 🥇 [**BTL1** (Blue Team Level 1)](../certificaciones/btl1.md) — cien por cien práctica, cubre
  forense, análisis de logs y respuesta a incidentes. Excelente **primer** certificado del área,
  mucho más asequible que SANS y con gran relación calidad/precio.
- 📋 [**CompTIA CySA+** (CS0-003)](../certificaciones/comptia-cysa-plus-cs0-003.md) — analista de
  seguridad con foco en detección, análisis e respuesta. Buen puente teórico muy reconocido en ofertas.
- 🎓 [**CompTIA Security+** (SY0-701)](../certificaciones/comptia-security-plus-sy0-701.md) — la
  certificación **de entrada** al sector. No es específica de forense, pero asienta el vocabulario
  y abre puertas de RRHH.

Como texto, sin archivo en el programa: **CHFI** (*Computer Hacking Forensic Investigator*, de
EC-Council) es otra certificación forense conocida; es una opción, aunque en la comunidad DFIR
las credenciales SANS suelen tener más peso.

Consulta el [mapeo completo a certificaciones](../certificaciones/README.md) para ver cuánto
cubre el programa de cada examen.

## 📈 Progresión de carrera y salario

Ruta habitual: **SOC L2 / sysadmin → Analista DFIR junior → Analista forense / IR → DFIR
senior o líder de IR → Consultor forense / IR Manager**. Muchos llegan a DFIR **desde el blue
team** (tras pasar por el SOC) o desde administración de sistemas; es raro que sea un primer
empleo, porque exige una base amplia de sistemas y redes.

Rangos **orientativos y aproximados** (varían mucho por empresa, sector y experiencia; DFIR
suele **pagar por encima** de muchos roles defensivos por lo especializado y por la presión de
las guardias):

```text
Región            Junior                DFIR senior · consultor IR
----------------  --------------------  --------------------------
LATAM             USD 18k – 35k / año   USD 40k – 70k+ / año
España            EUR 28k – 42k / año   EUR 50k – 80k+ / año
Remoto (USD)      USD 70k – 100k / año  USD 120k – 180k+ / año
```

Los números remotos en USD asumen contratación por empresas de EE. UU./Europa, muy competida y
con listón alto de inglés. La consultoría forense (respuesta a incidentes para terceros) y las
guardias de *retainer* suelen estar en la parte alta — se paga la disponibilidad y la
especialización, pero también la disponibilidad fuera de horario.

## ⚠️ Mitos y errores comunes

- **"El forense es como en las series: le das a un botón y sale el culpable."** No. Es trabajo
  lento, metódico y de documentación. El 90% es preparar, adquirir con cuidado y correlacionar.
- **"Lo importante es la técnica; lo legal es papeleo."** Falso y peligroso. Una evidencia mal
  adquirida o sin cadena de custodia **no sirve** en un procedimiento, por brillante que sea el
  análisis. El rigor procedimental es la mitad del oficio.
- **"Con apagar la máquina infectada basta."** Apagarla destruye toda la **memoria volátil** —
  procesos, claves, malware *fileless*, conexiones. El orden de volatilidad manda: primero la RAM.
- **"DFIR es una primera puerta a la ciberseguridad."** Normalmente no. Exige base sólida de
  sistemas y redes; se suele llegar tras el SOC o la administración de sistemas.
- **"El incidente lo resuelve el forense solo."** Es trabajo de equipo: coordinas con IT,
  detección, legal y dirección. Comunicar bien pesa tanto como analizar bien.

## 🚀 Siguientes pasos

1. **Asienta la base** con las **Partes 0 y 1**: sistemas operativos, sistemas de archivos,
   redes y Python. Sin esto, el forense no tiene dónde apoyarse.
2. Refuerza tu lado defensivo con la **Parte 8** (detección) para entender de dónde vienen las
   alertas que luego investigas como responder.
3. Haz la **Parte 9** completa — es el núcleo — y monta el laboratorio
   [`dfir-memoria`](../labs/dfir-memoria/README.md): adquiere memoria y analízala con Volatility.
4. Practica lectura forense con los [CTF de forense](../ctf/README.md): timelines, artefactos y
   reconstrucción de casos.
5. Apunta a **BTL1** como primer certificado del área; reserva **GCFA/GCIH** (SANS) como meta de
   especialización senior cuando puedas costearlas.
6. Construye **evidencia pública**: writeups de tus casos de laboratorio, informes forenses de
   práctica bien redactados y análisis de volcados de memoria. En DFIR, un informe claro y
   riguroso demuestra más que cualquier título.

---

- ⬅️ [Volver al índice de rutas](./README.md)
- 🏠 [Inicio del programa](../README.md)
