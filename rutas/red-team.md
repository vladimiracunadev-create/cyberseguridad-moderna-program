# 🔴 Red Teamer

> Emulación de adversarios, evasión y dominio de Active Directory: no buscas todas las
> vulnerabilidades, buscas cumplir un objetivo sin que te vean.
>
> **Nivel de entrada:** avanzado; parte de la ruta de [Pentester](./pentester.md) · **Foco:** emulación de amenazas, C2, OPSEC y ataque a Active Directory · **Certificación faro:** CRTO / OSEP

## 🧭 Qué es y por qué importa

Un red teamer **no es un pentester con otro nombre**. Es una confusión cara, así que vale la
pena separarlo bien:

- Un **pentest** busca *cobertura*: encontrar y documentar tantas vulnerabilidades como sea
  posible en un alcance definido, en un tiempo acotado, normalmente con el equipo defensor al
  tanto. El éxito se mide en hallazgos.
- Un **red team** busca *un objetivo*: emular a un adversario real (por ejemplo un grupo APT
  concreto) para responder una pregunta de negocio — "¿pueden llegar al servidor de nóminas sin
  que el SOC lo detecte?". El éxito se mide en si alcanzaste el objetivo **y en qué momento te
  detectaron** (si es que te detectaron).

La diferencia clave es el **sigilo**. Al pentester lo puede delatar un escaneo ruidoso y no pasa
nada. Al red teamer lo delata una sola alerta de EDR y el ejercicio pierde parte de su valor. Por
eso el oficio gira alrededor de tres ejes que el pentesting generalista apenas toca: **evasión**
(AV/EDR, AMSI, logging), **infraestructura C2** resiliente y **OPSEC** operativa disciplinada.

Un matiz importante: en banca y sectores regulados esto se formaliza como **TIBER-EU** (y marcos
equivalentes), donde un equipo de inteligencia de amenazas define a qué adversario emular y el red
team lo ejecuta contra el entorno de producción, coordinado con un grupo muy reducido de personas.
No es "hackear por hackear": es una prueba de la capacidad de **detección y respuesta** de la
organización. Si esto te suena más interesante que listar CVEs, este es tu rol.

## 🗓️ Un día en el puesto

No hay un día típico, pero sí fases típicas dentro de una operación de varias semanas:

- **Fase de preparación:** montar y endurecer la infraestructura C2 (redirectores, dominios con
  reputación, perfiles de tráfico que imiten software legítimo), preparar payloads y probarlos
  contra el EDR objetivo en un laboratorio propio antes de tocar nada del cliente.
- **Acceso inicial:** diseñar un pretexto de phishing, generar el payload de entrega, sortear el
  filtrado de correo y esperar (mucho esperar) a que alguien ejecute.
- **Post-explotación sigilosa:** enumerar Active Directory con herramientas que no disparen
  alertas, mapear rutas de ataque con BloodHound, escalar y moverte lateralmente cuidando cada
  comando por su huella en los logs.
- **Trabajo de escritorio:** documentar cada acción con marca de tiempo para el ejercicio de
  **purple team** posterior, escribir el reporte y — a menudo lo más valioso — sentarte con el
  blue team a explicar qué vieron, qué no, y por qué.

Buena parte del tiempo es paciencia, higiene operativa y espera. La imagen de "teclear rápido en
una terminal negra" es marketing; el trabajo real es metódico y aburrido en el buen sentido.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **Active Directory a fondo.** Es el corazón del rol. Kerberos, delegaciones, ACLs, relaciones
  de confianza, DPAPI. La mayoría de las operaciones internas se ganan o se pierden aquí.
- **Windows internals:** procesos, hilos, tokens de acceso, cómo funcionan AMSI, ETW y el
  logging de PowerShell — porque tu trabajo es evadirlos sin romperlos ruidosamente.
- **Desarrollo de payloads y evasión:** entender cómo un AV/EDR detecta (firmas, heurística,
  telemetría de comportamiento) para escribir loaders que no disparen alertas.
- **Redes y C2:** cómo diseñar canales de mando resilientes, domain fronting, redirectores,
  malleable profiles, y cómo mezclar tu tráfico con el legítimo.
- **Base ofensiva sólida** de la ruta de Pentester: sin reconocimiento, web y explotación bien
  asentados, el red team se te queda grande.

### Herramientas del oficio

```text
C2:            Cobalt Strike, Sliver, Mythic, Havoc
Active Dir.:   BloodHound/SharpHound, Rubeus, Certipy, Impacket, Mimikatz
Evasión:       ofuscadores propios, ScareCrow, Donut, técnicas de AMSI/ETW bypass
Recon interno: PowerView, ADRecon, enumeración "living off the land"
Emulación:     MITRE ATT&CK, Atomic Red Team, CALDERA
Infra:         redirectores (Nginx/Apache), dominios con categorización, VPS efímeros
```

Aviso honesto: dominar Cobalt Strike o Sliver **de verdad** no se aprende en un curso — se
aprende con horas de operación en entornos controlados propios. El curso te enseña el mapa; el
terreno lo caminas tú.

### Habilidades no técnicas

- **Disciplina de OPSEC:** la paciencia de no tocar el botón ruidoso aunque funcione.
- **Redacción de reportes:** un hallazgo que el cliente no entiende no vale nada. El reporte y la
  narrativa del ejercicio son entregables de primera clase.
- **Comunicación con el blue team:** el purple teaming exige explicar sin ego y enseñar.
- **Ética y límites:** operas con permiso explícito, alcance firmado y reglas de enfrentamiento.
  Cruzar esa línea es el fin de tu carrera, no una anécdota.

## 📚 Tu ruta en el programa

Esta ruta **asume que ya completaste la de [Pentester](./pentester.md)**. El red team se construye
encima de esa base ofensiva; no es un atajo para saltártela.

Orden recomendado (según el [índice de rutas](./README.md)):

1. 📚 [**Parte 7** — Red Team y operaciones ofensivas](../classes/parte-7-red-team-y-operaciones-ofensivas/README.md) (161–180) · el núcleo del rol.
2. 📚 [**Parte 6** — Análisis de malware](../classes/parte-6-analisis-de-malware/README.md) (141–160) · para entender payloads, packing y evasión desde el lado del que analiza.
3. 📚 [**Parte 5** — Explotación de sistemas y binarios](../classes/parte-5-explotacion-de-sistemas-y-binarios/README.md) (116–140) · desarrollo de exploits y evasión a bajo nivel.

Clases concretas por las que empezar:

- 🔴 [161 · Red Team vs Pentest: filosofía y objetivos](../classes/parte-7-red-team-y-operaciones-ofensivas/161-red-team-vs-pentest-filosofia-y-objetivos/README.md) — la mentalidad, antes que cualquier herramienta.
- 🎯 [163 · Emulación de adversarios](../classes/parte-7-red-team-y-operaciones-ofensivas/163-emulacion-de-adversarios/README.md) — cómo escoger y replicar a un actor real.
- 📡 [165 · Frameworks C2: Cobalt Strike, Sliver y Mythic](../classes/parte-7-red-team-y-operaciones-ofensivas/165-frameworks-c2-cobalt-strike-sliver-y-mythic/README.md) — el centro de mando.
- 🛡️ [168 · Evasión de defensas: antivirus y EDR](../classes/parte-7-red-team-y-operaciones-ofensivas/168-evasion-de-defensas-antivirus-y-edr/README.md) — el diferenciador del rol.
- 🗺️ [173 · BloodHound y análisis de rutas de ataque](../classes/parte-7-red-team-y-operaciones-ofensivas/173-bloodhound-y-analisis-de-rutas-de-ataque/README.md) — de un pie dentro a Domain Admin.
- 👑 [174 · Compromiso total de dominio: DCSync y Golden Ticket](../classes/parte-7-red-team-y-operaciones-ofensivas/174-compromiso-total-de-dominio-dcsync-y-golden-ticket/README.md) — el objetivo clásico.

Refuerzo desde las Partes 6 y 5:

- 📦 [147 · Ofuscación, packing y unpacking](../classes/parte-6-analisis-de-malware/147-ofuscacion-packing-y-unpacking/README.md) — para construir lo que el defensor intentará abrir.
- 🧩 [138 · Desarrollo de exploits moderno](../classes/parte-5-explotacion-de-sistemas-y-binarios/138-desarrollo-de-exploits-moderno/README.md) — cuando el payload de catálogo no basta.

### Laboratorio

- 🧪 [`red-team-ad`](../labs/red-team-ad/README.md) — tu campo de tiro para Active Directory.
  Complétalo montando además **GOAD** (Game of Active Directory): un bosque deliberadamente
  vulnerable, ideal para practicar Kerberoasting, delegaciones, ACLs y movimiento lateral sin
  arriesgar ningún entorno real.

Practica siempre **contra tu propio laboratorio**. Probar payloads o evasiones fuera de un
entorno autorizado no es aprender, es cometer un delito.

## 🎓 Certificaciones

Con archivo en el programa (mapean a partes concretas):

- 🥇 [**OSCP** (PEN-200)](../certificaciones/oscp-pen-200.md) — la base ofensiva. No es una cert de
  red team, pero es el prerrequisito de facto: sin ella, lo de abajo se te hará cuesta arriba.
- 📋 [**CompTIA PenTest+** (PT0-002)](../certificaciones/comptia-pentest-plus-pt0-002.md) — alternativa
  más teórica para asentar metodología si vienes de otro perfil.
- 🏛️ [**CISSP**](../certificaciones/cissp.md) — no técnica, pero útil si aspiras a liderar un equipo
  o dialogar con la capa de gestión y GRC.

Las **certificaciones faro del rol** existen fuera del catálogo del curso, pero apunta a ellas:

- **CRTO** (Certified Red Team Operator, de Zero-Point Security) — la puerta de entrada real al
  oficio: Cobalt Strike, AD, evasión práctica. Excelente relación calidad/precio.
- **OSEP** (PEN-300, de OffSec) — evasión avanzada y desarrollo de payloads. Dura y muy respetada.
- Más adelante: CRTL, y las de especialización en AD.

Consulta el [mapeo completo a certificaciones](../certificaciones/README.md) para ver cuánto cubre
el programa de cada examen.

## 📈 Progresión de carrera y salario

Ruta habitual: **Pentester → Red Team Operator → Red Team Lead → Head of Offensive Security**. Casi
nadie entra directo al red team; se llega tras años de ofensiva generalista.

Rangos **orientativos y aproximados** (varían mucho por empresa, sector y tu portfolio real; el
red team suele pagar **por encima** del pentesting generalista):

```text
Región            Junior/entrada*      Senior red teamer
----------------  -------------------  -----------------------
LATAM             USD 18k – 35k / año  USD 40k – 70k+ / año
España            EUR 30k – 45k / año  EUR 55k – 85k+ / año
Remoto (USD)      USD 70k – 100k / año USD 120k – 180k+ / año
```

`*` "Junior de red team" casi no existe como tal: normalmente es un pentester senior dando el
salto. Los números remotos en USD asumen contratación por empresas de EE. UU./Europa, muy
competida y con listón alto de inglés y experiencia demostrable.

Lo que de verdad mueve el salario en este rol no es el título: es un **historial verificable** de
operaciones, aportes a herramientas open source, charlas y un buen manejo del inglés.

## ⚠️ Mitos y errores comunes

- **"Es un pentest más elegante."** No. Es una disciplina distinta con otros objetivos, otras
  métricas y una obsesión por el sigilo que el pentest no tiene.
- **"Con Cobalt Strike ya soy red teamer."** La herramienta es el 10%. El 90% es OPSEC,
  entender AD y saber qué NO hacer para no delatarte.
- **"El curso me convierte en operador listo para producción."** Falso, y conviene decirlo claro:
  el programa te da una **base sólida** (mentalidad, AD, evasión conceptual, C2 introductorio),
  pero un red teamer real necesita **muchas horas de C2 y OPSEC en entornos controlados propios**
  antes de operar contra un cliente. El curso abre la puerta; no te sienta en la silla.
- **"Más ruido, más resultados."** Al revés. Un solo escaneo ruidoso puede quemar semanas de
  preparación. La contención es la habilidad.
- **"El reporte es el trámite final."** El reporte y el purple teaming son el producto. Si el blue
  team no aprende nada, la operación fracasó aunque llegaras a Domain Admin.

## 🚀 Siguientes pasos

1. **Cierra la ruta de [Pentester](./pentester.md)** si aún no lo has hecho. Sin esa base, para.
2. Haz la **Parte 7** completa y monta el laboratorio [`red-team-ad`](../labs/red-team-ad/README.md)
   junto con **GOAD**.
3. Practica evasión y payloads con el refuerzo de las **Partes 6 y 5**, siempre en tu laboratorio.
4. Apunta a **CRTO** como primera certificación de rol; deja **OSEP** para después.
5. Construye **historial público**: repos, writeups de laboratorios propios, aportes a
   herramientas. En este oficio, lo que demuestras vale más que lo que dices.

---

- ⬅️ [Volver al índice de rutas](./README.md)
- 🏠 [Inicio del programa](../README.md)
