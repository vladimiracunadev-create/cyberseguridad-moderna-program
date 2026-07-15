# Soluciones — Parte 8: Blue Team, detección y SOC

> Estas son **claves de referencia** para el instructor y para autoevaluación. Intenta resolver cada reto y ejercicio por tu cuenta **antes** de mirar aquí: el valor está en el proceso, no en la respuesta. Puede haber más de una solución correcta; lo que sigue es una guía técnicamente válida.
>
> Volver al índice de la parte: [../classes/parte-8-blue-team-deteccion-y-soc/README.md](../classes/parte-8-blue-team-deteccion-y-soc/README.md)

Todo laboratorio se realiza en un entorno aislado y autorizado (VMs/contenedores propios). Las técnicas ofensivas se ejecutan solo para generar telemetría de detección; nunca contra sistemas de terceros.

---

## Clase 181 — El SOC moderno: roles, niveles y procesos

### Solución del reto verificable

Entregable: documento de 1–2 páginas con organigrama, ciclo de vida de alerta, matriz RACI y 4 métricas.

Pasos concretos:

1. **Organigrama.** Dibuja L1 (triaje), L2 (investigación), L3 (hunting/ingeniería de detección), IR y responsable de SOC. Cada caja lista 1–2 responsabilidades.
2. **Ciclo de vida de la alerta.** Flujo con nodos: `Generación (EDR/SIEM) → Triaje L1 → [¿escala?] → Investigación L2 → [¿incidente?] → Respuesta IR/L3 → Erradicación → Cierre documentado → Lecciones aprendidas`. Marca explícitamente **un punto de escalado** (L1→L2, condición objetiva) y **un punto de cierre** con campo de documentación obligatorio.
3. **Matriz RACI.** Tabla actividad × rol para triaje, hunting, creación de reglas, IR y reporte a dirección. Cada actividad tiene **exactamente un A** y cada rol es **R en al menos una** actividad.

| Actividad | L1 | L2 | L3/Hunter | IR | Jefe SOC |
|-----------|----|----|-----------|----|----------|
| Triaje | R | C | I | I | A |
| Threat hunting | I | C | R | C | A |
| Creación de reglas | I | C | R | I | A |
| Respuesta a incidentes | I | R | C | R | A |
| Reporte a dirección | I | I | C | C | R/A |

4. **4 métricas con fórmula.**
   - MTTD = Σ(t_detección − t_compromiso) / n_incidentes.
   - MTTR = Σ(t_contención − t_detección) / n_incidentes.
   - % falsos positivos = alertas_FP / alertas_totales × 100.
   - Cobertura ATT&CK = técnicas_detectadas / técnicas_relevantes × 100.

**Evidencia que cumple el criterio:** el diagrama muestra al menos un punto de escalado y un cierre documentado, y en la RACI cada rol del organigrama aparece como "R" de al menos una actividad.

### Claves de los ejercicios

1. **L1:** monitorear colas de alertas, clasificar/descartar FP evidentes, escalar según criterios. **Ingeniero de detección:** diseñar y afinar reglas, mapearlas a ATT&CK, gestionar el ciclo de vida de la detección.
2. Runbook "login imposible": (1) confirmar los dos logins y su geolocalización, (2) calcular velocidad viaje vs tiempo, (3) verificar VPN/proxy corporativo que explique el salto, (4) revisar MFA y sesiones activas, (5) contactar/forzar reset si es real, (6) documentar y cerrar o escalar.
3. MTTD mide desde compromiso hasta detección; dwell time es hasta que se detecta/expulsa por completo. Ej.: compromiso día 0, detección día 8 (MTTD=8), erradicación día 11 → dwell time = 11.
4. Escalado L1→L2 si: (a) coincide con IOC de threat intel de alta confianza, (b) afecta a un activo crítico del inventario, o (c) hay evidencia de ejecución/persistencia (no solo un scan).
5. MSSP es mala idea cuando la organización maneja datos muy sensibles/regulados que no puede externalizar, necesita contexto de negocio profundo para triaje, o el coste de integración supera al de un equipo interno pequeño.
6. Métrica manipulable: "alertas cerradas/hora" (incentiva cerrar sin investigar). Contrapeso: tasa de reapertura/reincidencia y auditoría de muestreo de cierres.

---

## Clase 182 — Logging y fuentes de telemetría

### Solución del reto verificable

Entregable: plan de logging de una página + demostración de reenvío sincronizado.

Pasos:

1. **Matriz activo×fuente** con prioridad y retención:

| Fuente | Prioridad | Valor de detección | Retención |
|--------|-----------|--------------------|-----------|
| Sysmon (proc/net/DNS) | Alta | Ejecución, linaje, C2 | 90 días |
| Security.evtx (4624/4625/4688) | Alta | Auth, fuerza bruta | 90 días |
| PowerShell 4104 | Alta | Script ofuscado | 90 días |
| Zeek conn/dns | Alta | Beaconing, tunneling | 30–90 días |
| Proxy/firewall | Media | C2, exfil | 30 días |
| PCAP completo | Baja | Forense puntual | 3–7 días |

2. **3 puntos ciegos + remediación:** sin logging de PowerShell → habilitar ScriptBlock por GPO; sin DNS → Sysmon 22 o Zeek dns.log; nube sin auditar → activar CloudTrail/M365 Unified Audit Log.
3. **Demostración de sincronización.** Configura NTP en todos los hosts (UTC), genera un evento (`whoami /all`) y compara la marca de tiempo local con la del colector.

```bash
# Colector rsyslog (Linux)
module(load="imudp")
input(type="imudp" port="514")
```

```powershell
w32tm /query /status   # Windows: confirmar sincronización
```

**Evidencia que cumple el criterio:** el evento generado en el endpoint aparece en el colector con la misma marca de tiempo (±2 s) que la vista local, demostrando reenvío + NTP correctos.

### Claves de los ejercicios

1. Taxonomía NSM: Sysmon=endpoint/contenido; Zeek conn=sesión; Suricata=alerta; NetFlow=sesión; top-talkers=estadístico; PCAP=contenido completo; proxy=transacción; 4624=endpoint/identidad.
2. PCAP 100 Mbps al 20% = 20 Mbps ≈ 2,5 MB/s → ~216 GB/día → **~6,5 TB para 30 días** (por eso solo se retiene en segmentos críticos y poco tiempo).
3. Retención por tipo: flow/sesión 90 días, alerta 90 días, endpoint 90 días, PCAP 3–7 días (coste alto).
4. Puntos ciegos pyme: sin DNS logging, sin auditoría de creación de procesos con CommandLine, sin logs de M365/IdP. Se cierran con Sysmon+GPO+auditoría de nube.
5. PowerShell ScriptBlock (4104) registra el script tras des-ofuscar, revelando la intención real de ataques living-off-the-land: máxima señal por byte.
6. De M365/Azure AD: Unified Audit Log (accesos, cambios de permisos), sign-in logs (login imposible, MFA), y cambios de reglas de reenvío (indicio de BEC).

---

## Clase 183 — SIEM: arquitectura y componentes

### Solución del reto verificable

Entregable: recorrido de un evento (crudo → parseado → enriquecido → alerta correlacionada).

Pasos:

1. Captura del **dato crudo** (línea de texto de Sysmon/4625 sin estructura).
2. Captura del **dato parseado** con campos extraídos (`process.command_line`, `Account_Name`, `EventCode`).
3. Captura del **enriquecimiento** (GeoIP sobre la IP pública, propietario del activo vía lookup).
4. **Regla de correlación de fuerza bruta** (múltiples 4625 seguidos de un 4624):

```spl
index=win (EventCode=4625 OR EventCode=4624)
| stats count(eval(EventCode=4625)) as fails count(eval(EventCode=4624)) as success
        min(_time) as t0 max(_time) as t1 by Account_Name
| where fails>=5 AND success>0 AND (t1-t0)<=300
```

**Evidencia que cumple el criterio:** la regla dispara una alerta (notable), y puedes indicar en qué índice quedó el evento y su política de retención (ILM/fase hot→cold a los 7 días).

### Claves de los ejercicios

1. Pipeline: `Forwarder/colector → parsing/normalización → enriquecimiento → indexación → correlación → alertas/notables`.
2. 2.000 EPS × 800 B × 86.400 s = 1,38×10¹¹ B/día ≈ **~128 GB/día** (≈ 3,8 TB/mes).
3. Parser de firewall (regex): extrae `src_ip`, `dst_ip`, `dst_port`, `action` con named groups o `rex` en Splunk / grok en Logstash.
4. On-prem: control total, coste capex, mantenimiento propio; cloud-native: escalado elástico, opex, menos control/soberanía. Criterios: coste, escalado, control, mantenimiento.
5. Enriquecimiento con 3 fuentes: GeoIP (ubicación), threat intel (reputación de IP/dominio), CMDB (criticidad/propietario del activo).
6. Hot (7 d, SSD, consulta frecuente) / warm (30 d) / cold (90 d, barato, histórico) equilibra velocidad de investigación reciente con coste del histórico.

---

## Clase 184 — Splunk para detección

### Solución del reto verificable

Entregable: tres búsquedas SPL de detección + una convertida en alerta con throttling.

Búsqueda 1 — Office lanza intérprete (T1059):

```spl
index=main sourcetype=XmlWinEventLog EventCode=1
  ParentImage="*\\WINWORD.EXE" (Image="*\\powershell.exe" OR Image="*\\cmd.exe")
| table _time, Computer, ParentImage, Image, CommandLine
```

Búsqueda 2 — Fuerza bruta de autenticación:

```spl
index=main (EventCode=4625 OR EventCode=4624)
| stats count(eval(EventCode=4625)) as fails count(eval(EventCode=4624)) as success by Account_Name
| where fails>10 AND success>0
```

Búsqueda 3 — LOLBins con red saliente (regsvr32/mshta):

```spl
index=main sourcetype=XmlWinEventLog EventCode=3
  (Image="*\\regsvr32.exe" OR Image="*\\mshta.exe")
| table _time, Computer, Image, DestinationIp, DestinationPort
```

**Alerta con throttling:** guarda la Búsqueda 1 como alerta cada 5 min, con supresión (`throttle`) por campo `Computer` durante 30 min.

**Evidencia que cumple el criterio:** la Búsqueda 1 detecta la simulación Office→PowerShell sin disparar con la línea base benigna, y la saved search aparece ejecutándose en el listado de alertas.

### Claves de los ejercicios

1. `... EventCode=22 | stats dc(QueryName) count by Computer, QueryName | sort - count | head 10` (top dominios por host).
2. `... EventCode=3 (Image="*\\regsvr32.exe" OR Image="*\\mshta.exe") | table _time Computer Image DestinationIp`.
3. Línea base de horas de login: `... EventCode=4624 | eval h=strftime(_time,"%H") | stats values(h) as horas_normales by Account_Name` y marca logins fuera del rango habitual.
4. `| eval sev=case(EventCode=4104 AND match(CommandLine,"-enc"),"alta", ..., 1==1,"baja")`.
5. Reescribe con `tstats` sobre un data model CIM acelerado (`| tstats count from datamodel=Endpoint.Processes ...`): pasa de escanear eventos crudos a índices tstats, órdenes de magnitud más rápido.
6. Lookup de cuentas de servicio (`svc_*.csv`) + `... | lookup svc_accounts.csv Account_Name OUTPUT es_servicio | where isnull(es_servicio)` para suprimir sus FP.

---

## Clase 185 — Elastic Stack y Wazuh

### Solución del reto verificable

Entregable: una detección EQL en Elastic (secuencia proceso→red) + una alerta Wazuh con técnica ATT&CK.

Regla EQL (Elastic) — proceso PowerShell seguido de conexión:

```eql
sequence by host.id with maxspan=1m
  [ process where process.name == "powershell.exe" ]
  [ network where destination.port == 443 ]
```

Consulta KQL de apoyo:

```kql
event.code:"1" and process.parent.name:"WINWORD.EXE" and process.name:("powershell.exe" or "cmd.exe")
```

Alerta Wazuh: modifica un archivo bajo FIM (`/etc/passwd`) y observa la alerta con su nivel y la técnica ATT&CK asociada (ej. T1565/T1098 según regla).

**Evidencia que cumple el criterio:** ambas alertas disparan con la actividad simulada; muestras en Kibana/Wazuh el evento, la regla que lo detectó y la técnica ATT&CK asociada.

### Claves de los ejercicios

1. KQL PowerShell ofuscado: `process.command_line:*FromBase64String*`, `process.command_line:*-enc*`, `process.command_line:*IEX*`.
2. La SPL Office→PowerShell se traduce al EQL `sequence` de arriba (o un `process where process.parent.name=="WINWORD.EXE" and process.name=="powershell.exe"`).
3. Decoder = extrae campos del log crudo (paso previo); regla = evalúa esos campos y asigna nivel/alerta. Ej.: decoder de sshd parsea el usuario; la regla dispara si hay N fallos.
4. FIM: `<directories check_all="yes" realtime="yes">/ruta</directories>` en `ossec.conf`; documenta la alerta (regla 550/554, archivo, usuario).
5. Elastic: flexible (EQL), curva media, gratis con licencia básica. Wazuh: reglas+agente+ATT&CK listos, arranque rápido. Splunk: potente pero de pago por ingesta.
6. Regla local Wazuh en `local_rules.xml` con `<if_sid>` heredando de la base y `<level>12</level>` para elevar la severidad de un patrón concreto.

---

## Clase 186 — Escritura de reglas de detección con Sigma

### Solución del reto verificable

Entregable: dos reglas Sigma propias (ejecución + persistencia) con tags ATT&CK, falsos positivos y conversiones.

Regla de ejecución (Office→PowerShell, T1059.001):

```yaml
title: Office lanza PowerShell
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    ParentImage|endswith:
      - '\WINWORD.EXE'
      - '\EXCEL.EXE'
    Image|endswith: '\powershell.exe'
  condition: selection
level: high
tags:
  - attack.execution
  - attack.t1059.001
falsepositives:
  - Plantillas corporativas con macros firmadas
```

Regla de persistencia (Run key, T1547.001):

```yaml
title: Persistencia en clave Run
logsource:
  product: windows
  category: registry_set
detection:
  selection:
    TargetObject|contains:
      - '\CurrentVersion\Run\'
      - '\CurrentVersion\RunOnce\'
  filter:
    Image|endswith: '\msiexec.exe'
  condition: selection and not filter
level: medium
tags:
  - attack.persistence
  - attack.t1547.001
falsepositives:
  - Instaladores legítimos
```

Conversión: `sigma convert -t splunk -p splunk_windows regla.yml` y `sigma convert -t esql -p ecs_windows regla.yml`.

**Evidencia que cumple el criterio:** la regla de ejecución convertida dispara sobre la simulación y NO con la línea base; la CLI convierte ambas sin errores de sintaxis.

### Claves de los ejercicios

1. Regla rundll32: `Image|endswith: '\rundll32.exe'` + `CommandLine|contains` de argumentos sospechosos (`javascript:`, `,#1`) con filtro de usos legítimos.
2. `CommandLine|contains: ['-enc','FromBase64String']` y `CommandLine|re: '(?i)i.?e.?x'` para variantes ofuscadas.
3. Convierte a Splunk y a ES|QL/EQL: el mismo YAML genera distinta sintaxis nativa según backend/pipeline — demuestra la portabilidad.
4. FP plausibles: software de despliegue, herramientas de administración firmadas, scripts de logon corporativos → al campo `falsepositives`.
5. Mapeo: T1059.001 (PowerShell), T1547.001 (Run key), T1053.005 (Scheduled Task), T1218.010 (regsvr32), T1071.001 (Web C2).
6. Umbral: en Sigma la agregación se expresa con `condition: selection | count() by Computer > 5` (correlación en pySigma).

---

## Clase 187 — Detección basada en MITRE ATT&CK

### Solución del reto verificable

Entregable: capa de ATT&CK Navigator con la cobertura del laboratorio + plan priorizado de 5 huecos.

Pasos:

1. Inventaria tus reglas Sigma/SIEM y anota su `attack.tXXXX`.
2. En Navigator, crea una capa; colorea **verde** las técnicas cubiertas, **rojo** las críticas sin cobertura.
3. Para 5 técnicas rojas, revisa su *data source* en ATT&CK y verifica si ya recolectas esa telemetría.
4. Plan de huecos (tabla): técnica | data source faltante | detección propuesta | prioridad (justificada con pirámide del dolor y/o grupo relevante).

| Técnica | Data source | Detección propuesta | Prioridad |
|---------|-------------|---------------------|-----------|
| T1053.005 | Process/Scheduled Job | 4698 + Sysmon 1 schtasks | Alta (persistencia común) |
| T1003.001 | Process Access a lsass | Sysmon 10 sobre lsass.exe | Alta (grupo usa credential dumping) |

**Evidencia que cumple el criterio:** la capa distingue claramente cubierto/no cubierto y cada hueco justifica su prioridad con la pirámide del dolor o la relevancia de un grupo de amenaza.

### Claves de los ejercicios

1. Pirámide (fácil→difícil de cambiar): hash MD5 (trivial), IP (fácil), dominio (medio), artefacto de red/host (molesto), herramienta (difícil), TTP (muy difícil).
2. T1053 Scheduled Task: data source = Scheduled Job / Process creation; detección = 4698 o Sysmon 1 de `schtasks.exe`.
3. Se genera exportando la capa JSON con las técnicas coloreadas según reglas reales.
4. Detectar por hash es frágil porque recompilar/repackar cambia el hash en segundos sin cambiar el comportamiento; base de la pirámide.
5. Ej.: phishing (T1566) → macro ejecuta PowerShell (T1059.001) → tarea programada (T1053.005) → C2 HTTPS (T1071.001) → exfil (T1041).
6. De IP a TTP: en vez de bloquear la IP del C2, detecta el **comportamiento** de beaconing (periodicidad + proceso responsable), que persiste aunque cambie la infraestructura.

---

## Clase 188 — Threat hunting: metodología

### Solución del reto verificable

Entregable: una cacería completa documentada sobre una técnica ATT&CK, con detección resultante.

Ejemplo T1053.005 (Scheduled Task):

1. **Hipótesis:** "un adversario ha creado tareas programadas para persistir en algún host".
2. **Datos/ámbito:** Sysmon 1 (`schtasks.exe`), Security 4698, últimos 7 días.
3. **Baseline:** tareas y creadores legítimos (SCCM, admins conocidos, cuentas de servicio).
4. **Búsqueda de outliers** (Splunk):

```spl
index=main (EventCode=4698 OR (EventCode=1 Image="*\\schtasks.exe" CommandLine="*/create*"))
| stats count values(CommandLine) as cmd by Computer, SubjectUserName, TaskName
| search NOT [| inputlookup tareas_legitimas.csv | fields TaskName ]
| sort - count
```

5. **Control con Atomic Red Team:** ejecuta el test de T1053.005 y confirma que la búsqueda lo captura, distinguible de la baseline.
6. **Capitaliza:** convierte el hallazgo en regla Sigma/saved search.

**Evidencia que cumple el criterio:** la actividad de control de Atomic aparece en los resultados (separada de la baseline) y entregas una detección nueva derivada del hallazgo.

### Claves de los ejercicios

1. Ej.: (a) "hay PowerShell descargando payloads (T1105)", (b) "hay tareas programadas maliciosas (T1053.005)", (c) "hay WMI para ejecución remota (T1047)".
2. HMM: sitúa tu SOC (HM0 solo alertas → HM1 IOCs → HM2 análisis de datos → HM3 procedimientos → HM4 automatizado); paso siguiente = automatizar la búsqueda repetible previa.
3. Baseline de conexiones salientes: `... EventCode=3 | stats dc(DestinationIp) values(DestinationPort) by Image` para conocer qué procesos hacen red normalmente.
4. Caza LOLBins: busca ejecución de `certutil`, `bitsadmin`, `mshta`, `regsvr32` con argumentos de red/descarga y correlaciona con Event 3.
5. Se convierte el SPL del hallazgo en una regla Sigma con su `logsource`/`detection`/tags ATT&CK.
6. Métricas de caza: nº de detecciones nuevas creadas, nº de puntos ciegos hallados, tiempo medio por cacería.

---

## Clase 189 — Análisis de endpoints con EDR

### Solución del reto verificable

Entregable: árbol de procesos, línea de tiempo, evidencia recolectada y acción de contención.

Pasos:

1. Genera la cadena benigna-anómala: `cmd.exe → powershell -enc <base64 inofensivo>`.
2. **Reconstruye el árbol** con Velociraptor o Sysmon (padre→hijo→nieto por `ProcessGuid`/`ParentProcessGuid`).
3. **osquery** para procesos y conexiones:

```sql
SELECT p.name, p.path, p.parent, s.remote_address, s.remote_port
FROM processes p LEFT JOIN process_open_sockets s ON p.pid = s.pid
WHERE p.name = 'powershell.exe';
```

4. **Línea de tiempo** ordenada por `_time`: creación de proceso → archivo escrito (Sysmon 11) → conexión de red (Sysmon 3).
5. **Contén:** flujo de aislamiento de host en Velociraptor; verifica que solo el agente conserva conectividad.
6. **Recolecta** antes de remediar (procesos, autoruns, prefetch).

**Evidencia que cumple el criterio:** reconstruyes la cadena padre→hijo hasta el proceso sospechoso, muestras al menos una conexión de red asociada y demuestras que tras el aislamiento el host solo mantiene el canal del agente.

### Claves de los ejercicios

1. osquery hunting: procesos sin firma (`SELECT ... FROM processes JOIN signature ...`), autoruns (`SELECT * FROM startup_items;`), usuarios (`SELECT * FROM users;`).
2. Matar proceso detiene la ejecución pero destruye evidencia volátil; aislar el host contiene la propagación conservando el estado para forense. Usa aislar por defecto; matar solo si hay daño activo en curso.
3. Se ordenan los eventos Sysmon 1 por `ProcessGuid`/`ParentProcessGuid` para dibujar padre→hijo→nieto.
4. AV firma-based no ve un binario nuevo/empaquetado ni un ataque fileless (PowerShell en memoria); el EDR lo detecta por comportamiento (proceso→red→persistencia).
5. Artefacto Velociraptor con VQL sobre `Artifact: Windows.System.TaskScheduler` o consulta `wmi`/registro de tareas.
6. Tamper de EDR: matar el servicio (mitigar con protección de proceso/tamper protection), desinstalar el agente (permisos + alerta de agente offline), unhooking de userland (mitigar con telemetría kernel/ETW).

---

## Clase 190 — Análisis de logs de Windows: Event Logs y Sysmon

### Solución del reto verificable

Entregable: tres detecciones (autenticación, ejecución, persistencia) con Event ID, lógica y técnica ATT&CK.

1. **Autenticación (fuerza bruta, T1110):** ráfaga de 4625 seguida de 4624 por la misma cuenta.

```spl
index=win (EventCode=4625 OR EventCode=4624)
| stats count(eval(EventCode=4625)) as fails count(eval(EventCode=4624)) as ok by Account_Name, Logon_Type
| where fails>=10 AND ok>0
```

2. **Ejecución (Office→intérprete, T1059):** Sysmon Event 1 con `ParentImage` de Office; correlaciona con Event 3 del mismo `ProcessGuid`.
3. **Persistencia (T1053.005 / T1547.001):** alerta ante 4698 (tarea) o Sysmon 13 (Run key) fuera de la ventana de mantenimiento.

**Evidencia que cumple el criterio:** las tres disparan con la actividad generada y no con la línea base; demuestras que capturas la CommandLine completa (no truncada) y la relación padre-hijo.

### Claves de los ejercicios

1. Mapeo: 4624/4625→T1110/T1078, 4688/Sysmon1→T1059, 4104→T1059.001, 4698→T1053.005, 4720→T1136, 7045→T1543.003, Sysmon13→T1547.001, Sysmon3→T1071.
2. Logon Type 2 (interactivo local), 3 (red/SMB — PtH), 9 (NewCredentials — runas/overpass), 10 (RemoteInteractive/RDP — movimiento lateral interactivo).
3. Config Sysmon: añade `<Image condition="end with">proceso_ruidoso.exe</Image>` en un `<ProcessCreate onmatch="exclude">` para la línea base legítima.
4. IEX + Net.WebClient: detecta `4104` con `New-Object Net.WebClient`, `DownloadString`, `IEX` (T1059.001 + T1105).
5. 4688 es nativo (requiere GPO para CommandLine); Sysmon 1 añade hash, `ProcessGuid`, integridad de linaje y `OriginalFileName`. Se complementan.
6. Cuenta local sospechosa: `EventCode=4720` fuera de proceso de provisión, especialmente añadida a Administradores (4732).

---

## Clase 191 — Análisis de logs de red y proxy

### Solución del reto verificable

Entregable: detección de tunneling DNS o exfiltración HTTP con Zeek/proxy, correlacionada con el endpoint origen.

Pasos:

1. **DNS tunneling** en `dns.log`: dominios de alta entropía y muchos subdominios únicos por dominio padre.

```spl
index=zeek sourcetype=dns
| eval sub=mvindex(split(query,"."),0)
| stats dc(query) as subdominios avg(len(query)) as long_media by parent_domain
| where subdominios>50 AND long_media>30
```

2. **Justificación basada en datos:** entropía alta, volumen de subconsultas, longitud, o fingerprint JA3.
3. **Correlación red↔endpoint:** enlaza la conexión saliente (Zeek/proxy) con el proceso responsable vía Sysmon Event 3 (`ProcessGuid` + mismo host/momento).

**Evidencia que cumple el criterio:** identificas el dominio/destino anómalo con justificación por datos (entropía/volumen/periodicidad/fingerprint) y lo enlazas con el proceso concreto del host.

### Claves de los ejercicios

1. `... dns.log | stats dc(query) as subs by parent_domain | sort - subs | head 10` (posible tunneling).
2. Descarga de ejecutable desde IP sin dominio: `http.log` con `resp_mime_types` de ejecutable y `host` que sea una IP literal (sin DNS previo).
3. JA3 hashea el handshake TLS del cliente (versión, cipher suites, extensiones): identifica la herramienta aunque el contenido esté cifrado, porque el fingerprint del implante difiere de un navegador.
4. User-agent anómalo: alertar sobre UAs vacíos, `python-requests`, `curl`, o cadenas no vistas en tu baseline de navegadores corporativos.
5. Se une la alerta de red (IP/puerto/hora) con Sysmon Event 3 del mismo host y ventana temporal para atribuir el proceso.
6. RITA beaconing: score alto + intervalo regular + bajo volumen sostenido → escalar; si el destino es un servicio de update legítimo (allowlist) → descartar.

---

## Clase 192 — Detección de movimiento lateral

### Solución del reto verificable

Entregable: generar y detectar ≥3 técnicas de movimiento lateral, cada una con telemetría, detección y técnica ATT&CK.

1. **PsExec (T1021.002):** Event 7045 (servicio `PSEXESVC`), 4624 tipo 3, acceso a `\\B\ADMIN$`.

```spl
index=win EventCode=7045 Service_File_Name="*PSEXESVC*"
| table _time, Computer, Service_Name, Account_Name
```

2. **WMI (T1047):** Sysmon Event 1 con `ParentImage="*\\WmiPrvSE.exe"` lanzando `cmd/powershell`.
3. **WinRM (T1021.006):** procesos hijos de `wsmprovhost.exe`.
4. **Pass-the-Hash (T1550.002):** 4624 NTLM tipo 3 + 4648 sin actividad Kerberos coherente, workstation→workstation.

**Evidencia que cumple el criterio:** cada detección dispara con su técnica y no con la administración legítima de la baseline; distingues PsExec (servicio 7045) de WMI (hijo de WmiPrvSE) de WinRM (hijo de wsmprovhost).

### Claves de los ejercicios

1. Mapeo: PsExec→7045+4624t3; WMI→Sysmon1 hijo WmiPrvSE; WinRM→hijo wsmprovhost; RDP→4624t10; PtH→4624 NTLM t3 + 4648.
2. Workstation→workstation SMB admin$: `4624 Logon_Type=3` donde origen y destino son estaciones (no servidores) y la cuenta no es de administración conocida.
3. Tabla de artefactos: PsExec = servicio + ADMIN$; WMI = WmiPrvSE, sin servicio; WinRM = wsmprovhost, puerto 5985/5986.
4. PtH: correlaciona logon NTLM tipo 3 (4624) con 4648 (credenciales explícitas) en contextos donde se esperaría Kerberos; es detección por anomalía, no hay "evento PtH".
5. Baseline de admin legítima: cuentas admin conocidas, hosts de salto (jump hosts), ventanas horarias y tickets de cambio → allowlist.
6. Grafo de logons origen→destino: un pivote anómalo es un nodo que de pronto inicia sesión hacia muchos hosts o hacia hosts que nunca tocó.

---

## Clase 193 — Detección de C2 y beaconing

### Solución del reto verificable

Entregable: detectar un beacon combinando análisis temporal y correlación con el proceso de endpoint.

Pasos:

1. Genera un beacon benigno (intervalo 60 s, jitter 20%) a un servidor propio.
2. Acumula tráfico en Zeek `conn.log` varios minutos.
3. **Detección estadística** por baja varianza de los deltas de tiempo:

```spl
index=zeek sourcetype=conn
| sort 0 id.orig_h id.resp_h _time
| streamstats current=f last(_time) as prev by id.orig_h, id.resp_h
| eval delta=_time-prev
| stats count avg(delta) as intervalo stdev(delta) as jitter avg(orig_bytes) as vol by id.orig_h, id.resp_h
| where count>20 AND intervalo>0 AND (jitter/intervalo)<0.25 AND vol<2000
```

4. **RITA** confirma el score de beaconing e intervalo estimado.
5. **Correlación:** enlaza el par origen-destino con el proceso responsable (Sysmon Event 3, `ProcessGuid`).

**Evidencia que cumple el criterio:** identificas el par origen-destino con su intervalo y jitter aproximados, justificas con baja varianza estadística, y enlazas la conexión con el proceso concreto del host.

### Claves de los ejercicios

1. El jitter dispersa el intervalo pero, sobre suficientes muestras, un beacon sigue siendo mucho más regular que la navegación humana → el análisis estadístico lo revela.
2. Varianza: calcula desviación estándar de los deltas; baja stdev/media (< ~0,25) = beacon; alta = tráfico humano irregular.
3. C2 DNS: alta cadencia de subdominios únicos, entropía elevada, respuestas TXT largas → detección por volumen + entropía.
4. JA3 identifica el framework por el fingerprint del handshake TLS aunque el contenido esté cifrado (el implante negocia distinto que un navegador).
5. Domain fronting: el SNI muestra un dominio de CDN benigno pero el Host header apunta al destino real; discrepancia SNI≠Host lo delata.
6. Se enlaza el beacon (par IP/puerto periódico) con Sysmon Event 3 del proceso que origina la conexión.

---

## Clase 194 — Deception: honeypots y honeytokens

### Solución del reto verificable

Entregable: ≥2 mecanismos de deception (honeypot + honeytoken/cuenta trampa) integrados al SIEM con alertas de máxima prioridad.

Pasos:

1. **Honeypot SSH (Cowrie)** en VLAN aislada con salida controlada (no puede pivotar).
2. **Canary token** (documento con nombre atractivo, ej. `nóminas_2026.xlsx`) que avisa al abrirse.
3. **Cuenta trampa** en AD (`svc_backup_admin`) con auditoría de logon y sin uso legítimo.
4. **Regla SIEM de máxima prioridad:** cualquier evento de estos señuelos = incidente.

```spl
index=deception (source="cowrie" OR TokenName="canary_nominas" OR Account_Name="svc_backup_admin")
| eval severity="critical"
| table _time, origen, señuelo, severity
```

**Evidencia que cumple el criterio:** cada interacción simulada dispara una alerta de máxima prioridad identificando origen y señuelo, y el honeypot está segmentado de modo que no sirva de pivote.

### Claves de los ejercicios

1. Baja interacción: emula servicios, seguro, datos limitados; alta interacción: SO real, datos ricos, mayor riesgo de abuso.
2. 3 honeytokens: documento cebo en fileshare de RRHH, credencial falsa en un script/config, fila trampa en la base de datos de clientes.
3. Cuenta trampa + regla: cualquier 4624/4625 con esa cuenta → alerta crítica inmediata.
4. Deception tiene pocos FP porque el señuelo no tiene uso legítimo: por definición, cualquier interacción es sospechosa.
5. Riesgos de honeypot mal segmentado: pivote a la red real, uso como trampolín de ataque saliente, consumo por el atacante como C2 → mitigar con VLAN aislada y salida controlada.
6. Canary token para repositorio: clave AWS falsa o webhook en un README/CI que avise al ser usada por quien clone/escanee el repo.

---

## Clase 195 — Threat intelligence operacional

### Solución del reto verificable

Entregable: operacionalizar indicadores desde el TIP hasta una detección funcional, con scoring y caducidad.

Pasos:

1. Levanta MISP/OpenCTI en Docker; ingesta 2–3 feeds abiertos (abuse.ch, listas OSINT).
2. Crea el IOC (ej. el dominio del beacon de la clase 193) con contexto, TLP y campaña/ATT&CK.
3. Asigna **score** y **fecha de expiración**; verifica la degradación de indicadores viejos.
4. Conecta STIX/TAXII al SIEM y configura un lookup de **threat match** sobre DNS/red.

```spl
index=zeek sourcetype=dns
| lookup threat_intel_domains domain AS query OUTPUT ti_source, ti_tlp, ti_campaign
| where isnotnull(ti_source)
| table _time, id.orig_h, query, ti_source, ti_tlp, ti_campaign
```

**Evidencia que cumple el criterio:** un evento que coincide con un indicador dispara una alerta enriquecida (fuente, TLP, campaña/ATT&CK), y demuestras que un indicador caducado deja de generar ruido.

### Claves de los ejercicios

1. Estratégica (tendencias del sector para dirección), operacional (campaña de un actor), táctica (IOCs: hash, IP, dominio).
2. Los IOCs caducan porque el atacante rota infraestructura en segundos; se gestiona con scoring de fiabilidad + fecha de expiración que los degrada automáticamente.
3. Ciclo: dirección (qué necesito) → recolección (feeds) → análisis/enriquecimiento → difusión (al SIEM/EDR) → feedback.
4. Lookup de threat match: cruza campo de evento (dominio/IP/hash) con la tabla de IOCs y alerta ante coincidencia (hit).
5. MISP: colaborativo, orientado a IOCs/eventos y compartición comunitaria; OpenCTI: modelo de conocimiento con relaciones (actores↔TTPs↔campañas), grafo.
6. TLP: RED (solo destinatarios nombrados), AMBER (organización/need-to-know), GREEN (comunidad), CLEAR (público). Respetarlo condiciona con quién compartes.

---

## Clase 196 — Automatización con SOAR

### Solución del reto verificable

Entregable: playbook funcional que enriquece una alerta, decide severidad y propone contención con aprobación humana.

Flujo (Shuffle/Tines/n8n):

1. **Trigger:** alerta de "posible phishing" vía webhook/API.
2. **Enriquecimiento automático:** extrae URLs/adjuntos → reputación (MISP/Cortex), WHOIS del dominio, hash del adjunto.
3. **Decisión:** dominio/hash malicioso conocido → severidad alta; dudoso → caso para revisión humana.
4. **Contención con human-in-the-loop:** propón bloquear dominio en proxy; **ejecuta solo tras aprobación** explícita del analista.
5. **Alcance:** consulta al SIEM quién más recibió/hizo clic; añade al caso en TheHive.
6. **Notifica y documenta.**

**Evidencia que cumple el criterio:** ante una alerta de prueba, el playbook enriquece automáticamente, clasifica correctamente y NO ejecuta ninguna acción destructiva sin pasar por el punto de aprobación humana; el caso queda documentado.

### Claves de los ejercicios

1. Playbook "host comprometido": trigger EDR → enriquecer (proceso, hash, red) → decidir → **[aprobación]** aislar host → recolectar evidencia → notificar.
2. Automatizables: enriquecimiento de IOCs, deduplicación de alertas, apertura de casos, geolocalización, sandbox de adjuntos. NO: aislar producción, deshabilitar cuenta de directivo, borrar datos.
3. Enriquecimiento de IP: llamada API a VirusTotal/AbuseIPDB/MISP → añade score de reputación al caso.
4. Salvaguardas "deshabilitar cuenta": lista de exclusión (cuentas VIP/servicio), aprobación humana obligatoria, acción reversible/con log de auditoría, ventana de reversión.
5. Ahorro MTTR: si el triaje manual de phishing tarda 30 min y el automatizado 3 min → 27 min ahorrados por caso × volumen diario.
6. Riesgo de aislar sin control: cortar un servidor de producción crítico; mitigar con allowlist de activos críticos + human-in-the-loop.

---

## Clase 197 — Métricas y madurez del SOC

### Solución del reto verificable

Entregable: cuadro de mando con ≥6 métricas (fórmula, fuente, valor), contrapesos anti-gaming y evaluación de madurez con 3 mejoras.

| Métrica | Fórmula | Fuente | Contrapeso anti-gaming |
|---------|---------|--------|------------------------|
| MTTD | Σ(t_det−t_comp)/n | tickets/SIEM | — |
| MTTR | Σ(t_cont−t_det)/n | tickets | Tasa de reincidencia |
| Dwell time | t_erradicación−t_compromiso | forense | — |
| % FP | FP/total×100 | SIEM | — |
| Cobertura ATT&CK | detectadas/relevantes | Navigator | Profundidad (eficacia real) |
| % con causa raíz | con_RCA/total×100 | tickets | Auditoría de muestreo |

Pasos: define fórmula+fuente por métrica, calcula con datos de laboratorio (o CSV simulado), añade el contrapeso, completa una autoevaluación SOC-CMM en 2–3 dominios y prioriza 3 mejoras justificadas con los valores medidos.

**Evidencia que cumple el criterio:** cada métrica tiene fórmula y origen verificable, al menos una detecta explícitamente un intento de manipulación (p. ej. MTTR bajo + reincidencia alta), y las mejoras se justifican con los valores, no con opiniones.

### Claves de los ejercicios

1. Ej.: MTTD, MTTR, dwell time, %FP, cobertura ATT&CK — cada una con su fórmula y log/ticket de origen (ver tabla).
2. Vanidosas → útil: "alertas procesadas" → % detecciones verdaderas; "reglas creadas" → precisión de detección; "horas trabajadas" → dwell time.
3. MTTD/MTTR de 10 incidentes: suma los tiempos individuales y divide entre 10; muestra el cálculo por caso.
4. Contrapeso de MTTR: parear con tasa de reincidencia/reapertura, para que cerrar rápido sin erradicar penalice.
5. Autoevaluación SOC-CMM en un dominio (p. ej. "Detección"): puntúa personas/proceso/tecnología en la escala del modelo.
6. KPI de calidad: precisión de detección = TP/(TP+FP), mide calidad no cantidad.

---

## Clase 198 — Casos de estudio de detección

### Solución del reto verificable

Entregable: caso completo con timeline+ATT&CK por fase, puntos de detección perdidos y ≥3 detecciones nuevas.

Pasos:

1. Carga el dataset (Splunk BOTS o EVTX-ATTACK-SAMPLES) en el SIEM.
2. Fija **T0** en el acceso inicial (phishing/adjunto/primer proceso anómalo).
3. Pivota fase a fase: ejecución (Sysmon 1 + CommandLine), persistencia (4698/Sysmon13/7045), movimiento lateral (4624 t3/t10), C2 (beaconing), exfiltración.
4. Construye la **timeline** en una tabla con la técnica ATT&CK de cada evento (tiempos en UTC, ordenados).

| Hora (UTC) | Evento | Fase | ATT&CK |
|------------|--------|------|--------|
| T0 | Adjunto abierto | Acceso inicial | T1566.001 |
| T0+2m | WINWORD→powershell | Ejecución | T1059.001 |
| T0+5m | Tarea programada | Persistencia | T1053.005 |
| T0+30m | PsExec a host B | Lateral | T1021.002 |
| T0+2h | Beacon HTTPS | C2 | T1071.001 |
| T0+4h | POST voluminoso | Exfiltración | T1041 |

5. Marca los **puntos de detección perdidos** (por qué no disparó: falta de telemetría/regla ausente/FN) y propón ≥3 detecciones nuevas.

**Evidencia que cumple el criterio:** la timeline cubre desde acceso inicial hasta exfiltración de forma coherente y ordenada, cada fase mapeada a su técnica correcta, y las detecciones propuestas son verificables (Sigma/SIEM concretas).

### Claves de los ejercicios

1. Acceso inicial: correo de phishing (T1566) → adjunto → primer proceso hijo anómalo de Office.
2. 6 fases → T1566 (acceso), T1059 (ejecución), T1053/T1547 (persistencia), T1021 (lateral), T1071 (C2), T1041 (exfil).
3. Punto de detección más temprano: la ejecución Office→PowerShell (T1059.001), regla de la clase 184/186.
4. Lecciones: habilitar ScriptBlock logging, cerrar hueco de DNS, crear regla de PsExec, afinar baseline de tareas, añadir threat match.
5. Detección nueva del hueco: p. ej. Sysmon 1 de `certutil` con `-urlcache`/`-f` (T1105).
6. Todos los eventos ordenados por timestamp UTC en una única tabla con columna ATT&CK.

---

## Clase 199 — Ingeniería de detección como disciplina

### Solución del reto verificable

Entregable: mini repo de detection-as-code con ≥3 reglas documentadas, pipeline de validación/conversión y evidencia de validación con Atomic.

Estructura y pipeline:

```text
detections/
  office_powershell.yml
  scheduled_task.yml
  certutil_download.yml
  metadata_template.yml
```

```yaml
# .github/workflows/detections.yml
name: detections-ci
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install sigma-cli
      - run: sigma check detections/          # falla si hay sintaxis inválida
      - run: sigma convert -t splunk -p splunk_windows detections/*.yml
```

Pasos: cada regla incluye metadatos (autor, ATT&CK, data source, falsos positivos, respuesta esperada). Valida con Atomic Red Team (ej. T1105 certutil) y confirma que la regla dispara en el SIEM. Marca una regla vieja/ruidosa para retiro con registro en Git.

**Evidencia que cumple el criterio:** el pipeline **falla** ante una regla con sintaxis inválida y **pasa** con las correctas; cada detección incluye metadatos y respuesta; la técnica ejecutada con Atomic dispara su regla.

### Claves de los ejercicios

1. Plantilla de metadatos: título, autor, fecha, `attack.tXXXX`, data source, lógica, falsos positivos, nivel, respuesta esperada, estado (dev/prod/retirada).
2. Pipeline CI: pasos `sigma check` (sintaxis) → `sigma convert` (compilación) → fail si alguno rompe; opcional test de despliegue.
3. Validar con el test Atomic de la técnica (p. ej. `Invoke-AtomicTest T1105`) y confirmar el hit en el SIEM.
4. Criterios de retiro: FP insostenibles, técnica ya no aplica, otra regla la cubre mejor → documentar la decisión.
5. Precisión = TP/(TP+FP); ej. 18 TP y 2 FP → 18/20 = 90%.
6. El versionado (Git) da historial, revisión por pares, blame y reversión: se audita quién cambió qué detección y cuándo, evitando degradación silenciosa.

---

## Clase 200 — Purple team desde el lado defensivo

### Solución del reto verificable

Entregable: ciclo purple completo sobre ≥8 técnicas con scorecard antes/después y cierre de huecos.

Pasos:

1. **Planifica:** elige un grupo ATT&CK relevante y selecciona 8–10 técnicas suyas.
2. **Scorecard inicial:** capa de Navigator con esas técnicas en estado "por probar".
3. **Ejecuta pruebas atómicas** (Atomic Red Team): ej. T1059.001, T1053.005, T1105, T1003.001, T1021.002, T1547.001, T1071.001, T1041.
4. **Observa** por técnica: prevenida / detectada / solo registrada / no vista.
5. **Encadena con Caldera** una operación que combine varias técnicas y comprueba si detectas la cadena.
6. **Puntúa:** verde=detectado, amarillo=solo registrado, rojo=no visto.
7. **Cierra huecos:** por cada rojo/amarillo crea o afina una detección (Sigma) y re-ejecuta hasta que dispare.
8. **Documenta** con antes/después y define la cadencia del próximo ejercicio.

**Evidencia que cumple el criterio:** la scorecard antes/después muestra mejora medible de cobertura, cada técnica inicialmente "no vista" acaba con una detección que dispara al re-ejecutarla, y todo está documentado con su alcance y ejecutado en entorno autorizado.

### Claves de los ejercicios

1. Selección de grupo: elige uno cuyas víctimas/sector coincidan con tu organización (relevancia por intel), y emula sus TTPs documentados.
2. 3 pruebas atómicas clasificadas: p. ej. T1059.001 detectado, T1105 solo registrado, T1003.001 no visto.
3. Operación Caldera de 4 técnicas encadenadas (acceso→ejecución→persistencia→C2) con agentes.
4. Scorecard en Navigator coloreando cada técnica según su resultado observado.
5. Cierre de hueco: técnica no vista → nueva regla Sigma → re-ejecutar Atomic → confirmar disparo.
6. Programa purple: alcance por ciclo, cadencia (mensual/trimestral), métrica de cobertura antes/después como indicador de mejora sostenida.
