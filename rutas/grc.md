# 🏛️ GRC / Gestión de seguridad

> Gobernanza, riesgo, cumplimiento y auditoría: el rol que traduce el riesgo
> técnico a decisiones y lenguaje que la dirección entiende y firma.
>
> **Nivel de entrada:** medio; rara vez es un primer empleo, pero es alcanzable desde soporte, sistemas, auditoría o SOC · **Foco:** marcos, políticas, gestión de riesgo, auditoría y cumplimiento normativo · **Certificación faro:** CISSP

## 🧭 Qué es y por qué importa

**GRC** son tres disciplinas que trabajan juntas:

- **Gobernanza (G).** Definir *quién decide qué* en seguridad: políticas, roles,
  responsabilidades, comités, apetito de riesgo. Es alinear la seguridad con los objetivos
  del negocio, no al revés.
- **Riesgo (R).** Identificar, medir y priorizar riesgos, y decidir qué se hace con cada uno:
  mitigar, transferir (seguros), aceptar o evitar. Aquí vive el análisis **cualitativo y
  cuantitativo**.
- **Cumplimiento (C).** Demostrar, con evidencia, que la organización respeta los marcos y
  normativas que le aplican: **ISO 27001**, **NIST CSF**, **SOC 2**, y regulaciones como
  **GDPR**, **HIPAA** o **PCI DSS**.

Alrededor de esto gira la **auditoría**: la función que verifica que los controles existen,
funcionan y dejan rastro. Auditoría interna trabaja *contigo*; auditoría externa te *examina*.

El valor real del rol es de **traducción**. Un hallazgo técnico —"tenemos 200 servidores sin
parchear"— no mueve un presupuesto por sí solo. Quien hace GRC lo convierte en algo que la
dirección puede decidir: *"este riesgo tiene esta probabilidad, este impacto en euros y esta
opción de tratamiento; firma aquí para aceptarlo o para financiar el arreglo"*. Sin esa
traducción, la seguridad técnica se queda sin presupuesto y sin respaldo político.

Por eso GRC no es un adorno burocrático: es **la capa que conecta la trinchera técnica con la
sala de juntas**. Y es de los caminos con mejor techo salarial del sector, porque desemboca en
la ruta hacia **CISO**.

## 🗓️ Un día en el puesto

No hay turnos ni alertas a las 3 de la mañana. El ritmo lo marcan los proyectos, las auditorías
y los ciclos de revisión. Un día realista mezcla:

- **Trabajo de riesgo:** actualizar el registro de riesgos, entrevistar a un dueño de sistema
  para entender un proceso, estimar impacto y probabilidad de un riesgo nuevo.
- **Documentación y política:** redactar o revisar una política, un estándar o un procedimiento.
  Sí, se escribe mucho — es una parte central del oficio, no un extra.
- **Evidencia de cumplimiento:** recopilar pruebas para una auditoría (capturas, logs,
  configuraciones, actas) y mapearlas contra los controles de ISO 27001 o SOC 2.
- **Reuniones de traducción:** sentarte con el equipo técnico para entender un hallazgo, y luego
  con negocio o dirección para explicar qué significa y qué decisión requiere.
- **Gestión de terceros:** revisar el cuestionario de seguridad de un proveedor antes de firmar
  un contrato.

Dicho sin adornos: hay mucha **hoja de cálculo, matriz de riesgo y correo de seguimiento**. Si
buscas adrenalina técnica constante, este no es el rol. Si te motiva **ordenar el caos, influir
en decisiones y ver la seguridad de toda la organización desde arriba**, encaja.

## 🧠 Qué necesitas saber

### Conocimiento técnico

GRC **no** es un puesto "no técnico". Los mejores profesionales entienden lo que auditan; si no,
el equipo de sistemas les vende cualquier cosa y la dirección recibe una foto falsa del riesgo.
Necesitas una base sólida, aunque no vayas a explotar nada:

- **Fundamentos de seguridad:** tríada CIA, defensa en profundidad, gestión de identidad,
  cifrado, segmentación de red. Lo justo para dialogar de igual a igual con el equipo técnico.
- **Cómo funciona un SOC y un DFIR:** para escribir políticas de detección y respuesta que sean
  realistas, tienes que saber qué puede y qué no puede hacer un equipo defensivo.
- **Riesgo en el desarrollo (SDLC):** el pipeline de DevSecOps es donde nace mucho riesgo de
  terceros y de código. Entenderlo te permite gobernarlo en vez de bloquearlo.
- **Los marcos de memoria funcional:** ISO 27001, NIST CSF, controles CIS. No de carrerilla, pero
  sí saber qué cubre cada uno y cuándo se usa.

### Herramientas del oficio

```text
GRC / riesgo:      Registros de riesgo, matrices, plataformas GRC (Archer, ServiceNow GRC, Vanta, Drata)
Marcos:            ISO 27001, NIST CSF, controles CIS, SOC 2, COBIT
Cumplimiento:      GDPR, HIPAA, PCI DSS, mapeos de controles
Documentación:     Políticas, estándares, procedimientos, hojas de cálculo, Confluence/SharePoint
Métricas:          KPIs y KRIs, cuadros de mando para dirección
Auditoría:         Papeles de trabajo, matrices de evidencia, planes de auditoría
```

La herramienta más infravalorada es una **hoja de cálculo bien hecha**. Las plataformas GRC
ayudan a escalar, pero el criterio para priorizar un riesgo no lo pone el software.

### Habilidades no técnicas

Aquí es donde el rol se gana o se pierde:

- **Comunicación escrita y oral impecable:** vives de redactar con claridad y de explicar riesgo
  a audiencias que no son técnicas.
- **Pensamiento estructurado:** ordenar ambigüedad en marcos, matrices y prioridades.
- **Diplomacia y negociación:** dices "no" a proyectos y pides evidencia a gente ocupada; hacerlo
  sin quemar relaciones es un arte.
- **Visión de negocio:** entender que el riesgo cero no existe y que la seguridad compite por
  presupuesto con todo lo demás.
- **Rigor y trazabilidad:** en auditoría, lo que no está documentado no existe.

## 📚 Tu ruta en el programa

Orden recomendado (según el [índice de rutas](./README.md)):

1. 📚 [**Parte 0** — Fundamentos y prerrequisitos](../classes/parte-0-fundamentos-y-prerrequisitos/README.md) (001–025) · el contexto técnico mínimo para no gobernar a ciegas.
2. 📚 [**Parte 14** — GRC, riesgo y cumplimiento](../classes/parte-14-grc-riesgo-y-cumplimiento/README.md) (276–290) · **el núcleo del rol.**
3. 📚 [**Parte 8** — Blue Team, detección y SOC](../classes/parte-8-blue-team-deteccion-y-soc/README.md) (181–200) · para dialogar con lo técnico defensivo.
4. 📚 [**Parte 9** — Forense y respuesta a incidentes](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/README.md) (201–220) · saber qué ocurre cuando un control falla.
5. 📚 [**Parte 11** — DevSecOps y seguridad del SDLC](../classes/parte-11-devsecops-y-seguridad-del-sdlc/README.md) (236–248) · gestión de riesgo dentro del ciclo de desarrollo.

El corazón está en la **Parte 14**. Clases concretas por las que empezar:

- 🏛️ [276 · Gobernanza de la seguridad de la información](../classes/parte-14-grc-riesgo-y-cumplimiento/276-gobernanza-de-la-seguridad-de-la-informacion/README.md) — el porqué de todo lo demás: políticas, roles y apetito de riesgo.
- 📊 [277 · Gestión de riesgos cuantitativa y cualitativa](../classes/parte-14-grc-riesgo-y-cumplimiento/277-gestion-de-riesgos-cuantitativa-y-cualitativa/README.md) — el músculo central: medir y priorizar riesgo.
- 📘 [278 · ISO/IEC 27001 e implantación de un SGSI](../classes/parte-14-grc-riesgo-y-cumplimiento/278-iso-iec-27001-e-implantacion-de-un-sgsi/README.md) — el marco de gestión más pedido en ofertas.
- 🗺️ [279 · NIST Cybersecurity Framework](../classes/parte-14-grc-riesgo-y-cumplimiento/279-nist-cybersecurity-framework/README.md) — el lenguaje común de madurez y controles.
- ⚖️ [281 · Cumplimiento: GDPR, HIPAA y PCI DSS](../classes/parte-14-grc-riesgo-y-cumplimiento/281-cumplimiento-gdpr-hipaa-y-pci-dss/README.md) — las normativas que más aparecen en la práctica.
- 🔍 [285 · Auditoría de seguridad](../classes/parte-14-grc-riesgo-y-cumplimiento/285-auditoria-de-seguridad/README.md) — cómo se verifica que un control existe y funciona.
- 🔐 [289 · Privacidad y protección de datos](../classes/parte-14-grc-riesgo-y-cumplimiento/289-privacidad-y-proteccion-de-datos/README.md) — la disciplina que crece más rápido dentro de GRC.

Refuerzo desde las Partes 0 y 11:

- 🧩 [003 · Frameworks de seguridad: NIST CSF, ISO 27001, MITRE ATT&CK y Diamond Model](../classes/parte-0-fundamentos-y-prerrequisitos/003-frameworks-de-seguridad-nist-csf-iso-27001-mitre-att-ck-y-diamond-model/README.md) — el mapa de marcos, desde el primer día.
- 🔗 [240 · SCA: dependencias y riesgo de terceros](../classes/parte-11-devsecops-y-seguridad-del-sdlc/240-sca-dependencias-y-riesgo-de-terceros/README.md) — riesgo de supply chain, gobernado desde el pipeline.

## 🎓 Certificaciones

Con archivo en el programa (enlazan a su ficha):

- 🥇 [**CISSP**](../certificaciones/cissp.md) — la **certificación faro** del rol y del liderazgo en
  seguridad. Cubre gestión de riesgo, gobernanza, cumplimiento y arquitectura a nivel gerencial.
  Es cara y exige experiencia, pero es la que más peso tiene en la ruta hacia dirección y CISO.
- 🎓 [**CompTIA Security+** (SY0-701)](../certificaciones/comptia-security-plus-sy0-701.md) — la
  certificación **de entrada** al sector. No es específica de GRC, pero asienta el vocabulario y
  abre puertas de RRHH mientras acumulas experiencia para las mayores.

Otras muy valoradas en GRC (aún sin ficha propia en el programa, pero conviene conocerlas):

- **ISO 27001 Lead Implementer / Lead Auditor** — las certificaciones específicas para *implantar*
  o *auditar* un SGSI. De las más directamente empleables si tu foco es ISO 27001.
- **CISM** (Certified Information Security Manager) — orientada a gestión de seguridad; excelente
  complemento o alternativa a CISSP para el carril gerencial.

Consulta el [mapeo completo a certificaciones](../certificaciones/README.md) para ver cuánto cubre
el programa de cada examen.

## 📈 Progresión de carrera y salario

Ruta habitual: **Analista GRC / de cumplimiento → Especialista en riesgo o auditor de seguridad →
GRC Manager → Responsable de seguridad (ISO/CISO adjunto) → CISO**. Desde GRC también se ramifica
hacia **privacidad (DPO)**, **auditoría interna** y **consultoría**.

Rangos **orientativos y aproximados** (varían mucho por empresa, sector y experiencia):

```text
Región            Analista GRC / entrada   Senior / GRC Manager      CISO track
----------------  -----------------------  ------------------------  ---------------------
LATAM             USD 15k – 32k / año      USD 35k – 65k+ / año       USD 70k – 130k+ / año
España            EUR 25k – 40k / año      EUR 45k – 75k+ / año       EUR 80k – 140k+ / año
Remoto (USD)      USD 55k – 90k / año      USD 100k – 160k+ / año     USD 160k – 250k+ / año
```

El **GRC senior en carril CISO está entre lo mejor pagado** de toda la ciberseguridad, porque el
puesto asume responsabilidad legal y ante el consejo. La contrapartida honesta: la entrada suele
requerir algo de experiencia previa (soporte, sistemas, SOC o auditoría), y los números remotos en
USD asumen contratación por empresas de EE. UU./Europa, muy competida y con listón alto de inglés.

## ⚠️ Mitos y errores comunes

- **"GRC es para quien no sabe de técnica."** Falso, y es el error más caro. Un profesional GRC que
  no entiende lo que audita firma riesgos que no comprende. Los mejores vienen *con* base técnica.
- **"Es solo rellenar plantillas y marcar casillas."** El *checkbox compliance* existe y es un mal
  vicio del sector, pero el buen GRC gestiona riesgo real, no teatro de cumplimiento.
- **"No se programa, así que es fácil."** No se programa, pero se escribe, se negocia y se prioriza
  bajo presión política. La dificultad es distinta, no menor.
- **"Cumplir una norma = estar seguro."** ISO 27001 o PCI DSS son suelos, no techos. Pasar la
  auditoría no significa que no te vayan a comprometer.
- **"Es un callejón alejado de la acción."** Al contrario: es de los pocos caminos que desemboca
  directamente en la dirección de seguridad y en el consejo.

## 🚀 Siguientes pasos

1. **Asienta el contexto técnico** con la **Parte 0**: no puedes gobernar lo que no entiendes,
   aunque sea a alto nivel.
2. Haz la **Parte 14** completa: es el núcleo. Empieza por gobernanza (276) y riesgo (277) antes
   que por normativas concretas.
3. **Aterriza lo técnico** con las Partes 8, 9 y 11: te dan el criterio para escribir políticas
   realistas y para no dejarte vender humo.
4. **Practica la traducción:** coge un hallazgo técnico cualquiera y redacta media página que un
   directivo pueda leer y decidir. Esa habilidad es tu producto.
5. Apunta a **Security+** para abrir puertas ya, y planifica **CISSP** (o ISO 27001 Lead / CISM)
   como meta a medio plazo, cuando tengas la experiencia que exigen.

---

- ⬅️ [Volver al índice de rutas](./README.md)
- 🏠 [Inicio del programa](../README.md)
