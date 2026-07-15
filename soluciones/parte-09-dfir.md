# Soluciones — Parte 9: Forense digital y respuesta a incidentes

> Estas son **claves de referencia** para el instructor y para autoevaluación. **Intenta resolver cada reto y ejercicio por tu cuenta antes de mirar aquí**: el valor está en el proceso, no en la respuesta. Puede haber más de una solución correcta; lo que sigue es una guía técnicamente válida.
>
> Volver al índice de la parte: [../classes/parte-9-forense-digital-y-respuesta-a-incidentes/README.md](../classes/parte-9-forense-digital-y-respuesta-a-incidentes/README.md)

Todo el trabajo se realiza en un **laboratorio aislado**, sobre **evidencia propia** (pendrives, imágenes `.img`/`.dd`, VMs) o datasets públicos de entrenamiento. Nunca apuntes las herramientas a sistemas o datos de terceros sin autorización escrita. Registra siempre las horas en **UTC**.

---

## Clase 201 — Fundamentos de DFIR y cadena de custodia

### Solución del reto verificable

Objetivo: adquirir la imagen de un medio propio, documentar su cadena de custodia y probar integridad antes y después de una transferencia simulada.

Pasos:

1. Crea/adquiere la evidencia y su hash de adquisición:

   ```bash
   dd if=/dev/urandom of=evidencia.img bs=1M count=50        # o adquiere un pendrive propio
   sha256sum evidencia.img | tee evidencia.sha256
   ```

2. Redacta el formulario de custodia (ver plantilla del ejercicio 2) con: ID único (`CASO-2026-001-ITEM-01`), descripción/fabricante/serie, fecha-hora UTC de adquisición, quién adquirió + firma, el hash pegado desde `evidencia.sha256`, e historial de transferencias.
3. Registra la transferencia (de → a, fecha UTC, motivo, firmas de ambos).
4. Verifica integridad tras la transferencia:

   ```bash
   sha256sum -c evidencia.sha256      # debe imprimir: evidencia.img: OK
   ```

5. Demuestra la detección de contaminación:

   ```bash
   printf '\x00' | dd of=evidencia.img bs=1 seek=100 count=1 conv=notrunc
   sha256sum -c evidencia.sha256      # ahora imprime: evidencia.img: FAILED
   ```

Evidencia que cumple el criterio: entregas (a) `evidencia.img`, (b) `evidencia.sha256`, (c) el formulario de custodia con al menos una transferencia registrada, y (d) la captura de `sha256sum -c` mostrando `OK`, más la captura del `FAILED` documentada tras alterar un byte.

### Claves de los ejercicios

1. **Orden de volatilidad (RFC 3227)**: (1) registros/caché de CPU, (2) tabla de rutas, caché ARP, procesos, estadísticas de kernel y **RAM**, (3) archivos temporales/sistema de archivos en vivo, (4) disco, (5) logs remotos/monitoreo, (6) configuración física y topología, (7) medios de respaldo/archivado. Se captura primero lo que antes desaparece.
2. **Plantilla (≥10 campos)**: ID del ítem · caso · descripción · fabricante/modelo/serie · método y herramienta de adquisición (versión) · fecha-hora UTC · examinador + firma · hash MD5/SHA-256 · ubicación de almacenamiento · historial de transferencias (de→a, fecha, motivo, firmas) · observaciones.
3. **Apagar "correctamente" destruye evidencia** porque un *shutdown* limpio vacía RAM, cierra procesos, borra archivos temporales y puede disparar scripts de logoff que sobrescriben artefactos; se pierde la evidencia volátil (procesos, conexiones, claves en memoria). Ejemplo: malware *fileless* que solo vive en RAM desaparece al apagar.
4. **MD5 vs SHA-256**: se generan con `md5sum archivo` y `sha256sum archivo`. Preferimos SHA-256 porque MD5 tiene **colisiones prácticas conocidas** (dos entradas distintas con el mismo hash), lo que permitiría cuestionar la evidencia en juicio; SHA-256 no tiene colisiones conocidas.
5. **Procedimiento de etiquetado/foto**: fotografiar cada dispositivo *in situ* antes de tocarlo (con regla/escala y testigo de tiempo), asignar ID único, anotar estado (encendido/apagado, conexiones), guardar en bolsa antiestática etiquetada con marcador indeleble, sellar con precinto numerado y registrar todo en el formulario de custodia.
6. **Cinco errores del arrastrar-y-soltar**: (1) montó/leyó el original sin write-blocker, alterando *access times*; (2) no hizo imagen bit a bit (pierde borrados y espacio no asignado); (3) no calculó hashes de integridad; (4) no documentó la acción (rompe custodia); (5) copió solo archivos vivos (metadatos del FS y slack space perdidos), además de arriesgar ejecución de malware.

---

## Clase 202 — El ciclo de respuesta a incidentes (NIST y SANS)

### Solución del reto verificable

Objetivo: runbook de ransomware en un endpoint con las **seis etapas PICERL**, cada una con ≥3 acciones numeradas, responsable y condición de transición.

Esqueleto que cumple el criterio:

- **Preparación** — (1) EDR desplegado y backups offline verificados; (2) lista de escalado y contactos legales; (3) runbook y credenciales de respuesta a mano. *Responsable*: líder SecOps. *Transición*: capacidades listas y probadas.
- **Identificación** — (1) validar la alerta (¿cifrado real, extensión/nota de rescate?); (2) determinar alcance (hosts, comparticiones); (3) clasificar severidad y abrir ticket. *Responsable*: analista de guardia. *Transición*: incidente confirmado y con severidad asignada.
- **Contención** — (1) aislar el host por red **sin apagarlo** (preserva RAM); (2) bloquear cuentas/credenciales comprometidas; (3) deshabilitar comparticiones afectadas. *Responsable*: analista IR. *Transición*: propagación detenida.
- **Erradicación** — (1) identificar y eliminar el binario y toda la persistencia; (2) cerrar el vector de entrada (parche/GPO); (3) confirmar que no queda C2 activo. *Responsable*: IR + TI. *Transición*: causa y persistencia eliminadas.
- **Recuperación** — (1) restaurar desde backup limpio verificado; (2) reintroducir a producción con monitoreo reforzado; (3) rotar credenciales. *Responsable*: TI. *Transición*: servicio restaurado y estable.
- **Lecciones aprendidas** — (1) post-mortem blameless; (2) acciones correctivas con responsable/fecha; (3) actualizar playbooks. *Responsable*: líder IR. *Transición*: acciones asignadas y cierre formal.

### Claves de los ejercicios

1. **Ciclo NIST (4 fases)**: Preparación → Detección y Análisis → Contención/Erradicación/Recuperación → Actividad post-incidente. Es **iterativo** entre "Detección y Análisis" y "Contención/Erradicación/Recuperación" (se vuelve a analizar al hallar nuevos hosts), y toda lección realimenta la Preparación.
2. **Mapeo PICERL ↔ NIST**: Preparation → Preparación · Identification → Detección y Análisis · Containment/Eradication/Recovery → Contención, Erradicación y Recuperación · Lessons Learned → Actividad post-incidente.
3. **Evento → incidente (5 criterios)**: viola/ amenaza una política de seguridad; hay impacto en confidencialidad/integridad/disponibilidad; involucra acceso o acción no autorizada; requiere respuesta coordinada; y/o supera el umbral de severidad definido.
4. **Matriz P1–P4 (PYME)**: P1 crítico (afecta operación/ datos sensibles a nivel organización; respuesta inmediata; notifica dirección) · P2 alto (varios sistemas; <1 h) · P3 medio (un sistema, contenido; horas) · P4 bajo (sin impacto operativo; siguiente día hábil).
5. **Runbook de detección de phishing reportado**: recibir reporte → preservar el `.eml` con encabezados → analizar `Received`/SPF/DKIM/DMARC y URLs/adjuntos → buscar quién más lo recibió (búsqueda retroactiva por IOC) → bloquear remitente/dominio/URL → resetear credenciales si hubo clic → registrar y cerrar.
6. **Saltarse la contención**: erradicar (borrar malware) antes de contener alerta al atacante, que despliega más persistencia o destruye evidencia; además, sin aislar, el implante sigue propagándose lateralmente mientras "limpias" un host.

---

## Clase 203 — Adquisición forense: discos e imágenes

### Solución del reto verificable

Objetivo: adquirir un pendrive propio en **E01** y demostrar fidelidad comparando hashes.

Pasos (Linux con libewf):

1. Identifica el dispositivo sin montarlo: `lsblk -o NAME,SIZE,TYPE,MOUNTPOINT`.
2. Fija solo lectura (write-blocker por software): `sudo blockdev --setro /dev/sdX`.
3. Adquiere en E01 con metadatos del caso:

   ```bash
   sudo ewfacquire -t caso001 -f encase6 -c deflate:fast \
     -e "Nombre Examinador" -C CASO-2026-01 -D "Pendrive 16GB" /dev/sdX
   ```

4. Verifica que el hash de adquisición = hash de verificación:

   ```bash
   ewfverify caso001.E01     # "MD5/SHA-256 hash calculated over data: ... (match)"
   ```

Alternativa Windows (FTK Imager): `Create Disk Image → Physical Drive → Image Type E01`, rellena info del caso, activa *Verify images after they are created*; al terminar, FTK muestra *Computed hash = Report hash = Verify result: Match*.

Evidencia que cumple el criterio: la imagen `.E01`, el log de adquisición (`caso001.E01.txt`) y la salida de `ewfverify` (o el reporte de FTK) con coincidencia de hashes, acompañados de la cadena de custodia.

### Claves de los ejercicios

1. **Lógica en vez de física**: cuando el disco es enorme y solo importan ciertos archivos vivos, cuando hay tiempo/espacio limitado, cuando la ley restringe el alcance a datos concretos, o cuando el volumen está cifrado y solo tienes acceso descifrado a nivel de archivo (p. ej. buzón de correo).
2. **RAW vs E01**: RAW → universal, sin compresión, sin metadatos ni verificación embebida, tamaño = medio completo. E01 → compresión, metadatos del caso, hash y *checksums* por bloque integrados, verificable con `ewfverify`, pero requiere herramientas compatibles.
3. **Comparar tamaños**: el RAW pesa lo mismo que el dispositivo; el E01 con `deflate` suele ser bastante menor si hay espacio en cero/repetitivo (un pendrive casi vacío comprime mucho; uno con datos aleatorios/cifrados apenas).
4. **Hardware vs `blockdev --setro`**: el write-blocker de hardware intercepta físicamente los comandos de escritura en el bus (SATA/USB) y es independiente del SO (certificable, estándar en juicios); `blockdev --setro` depende del kernel y podría fallar ante *automount* o remontajes, por eso es solo para prácticas.
5. **TRIM en SSD**: al borrar un archivo, el SO envía TRIM y el controlador del SSD **borra físicamente** (garbage collection) los bloques liberados, a veces en segundos, dejando ceros; ya no hay datos que recuperar por carving o metadatos.
6. **Servidor que no se puede apagar**: adquisición **en vivo** siguiendo orden de volatilidad — primero volcado de RAM, conexiones y procesos; luego imagen lógica/física del volumen con el sistema activo (o snapshot si es virtual/SAN), documentando que estaba encendido y los hashes de cada captura.

---

## Clase 204 — Forense de sistemas de archivos: NTFS y ext4

### Solución del reto verificable

Objetivo: probar *timestomping* con la MFT y recuperar el contenido del archivo borrado.

Pasos:

1. Localiza la partición y el archivo borrado:

   ```bash
   mmls imagen_ntfs.dd
   fls -r -o 2048 imagen_ntfs.dd | grep '\*'      # los borrados llevan *
   ```

2. Recupera el contenido por su número de registro MFT (inodo TSK):

   ```bash
   icat -o 2048 imagen_ntfs.dd 128 > recuperado.bin
   ```

3. Extrae la MFT y compara `$STANDARD_INFORMATION` vs `$FILE_NAME`:

   ```bash
   MFTECmd.exe -f "$MFT" --csv salida --csvf mft.csv
   ```

   El *timestomping* se delata cuando los timestamps de `$SI` son **anteriores** (o de precisión distinta / con nanosegundos en cero) frente a los de `$FN`, que solo actualiza el kernel. En uso normal `$SI` es igual o posterior a `$FN`.

Evidencia que cumple el criterio: (a) `recuperado.bin` extraído con `icat` (verifica su contenido/hash), (b) la fila de `mft.csv` mostrando la incoherencia `$SI` < `$FN`, y (c) la explicación de por qué esa incoherencia solo se produce por manipulación (las apps modifican `$SI` pero no pueden retroceder `$FN`).

### Claves de los ejercicios

1. **Residente vs no residente**: un atributo (o archivo) **residente** cabe dentro del propio registro MFT (≈ archivos <700–900 bytes); **no residente** se guarda en clusters externos apuntados por *data runs*. No es lo mismo que "timestamps residentes": la diferencia de tiempos relevante es `$SI` (modificable) vs `$FN` (kernel).
2. **Detección de timestomping**: parsea la MFT y busca entradas donde `$SI.Modified/Created` sean anteriores a `$FN.Created`, o timestamps de `$SI` con subsegundos en `.0000000` (herramientas como `timestomp` truncan la precisión).
3. **Recuperar con `icat`**: `fls -r` para hallar el inodo del borrado, `icat -o <offset> imagen.dd <inodo> > out.bin`, y valida abriéndolo o comparando su SHA-256 con el original conocido.
4. **MACB**: **M**odified (última modificación del **contenido**/datos), **A**ccessed (último acceso), **C**hanged (última modificación de los **metadatos**/entrada MFT — el `ctime`, NO "creación"), **B**orn (creación/nacimiento). Ejemplo: editar un archivo cambia M y C; abrirlo cambia A; crearlo fija B.
5. **Inodos borrados con debugfs**: `debugfs -R "lsdel" imagen_ext4.dd` lista inodos borrados con su tamaño y hora; luego `debugfs -R "dump <inodo> salida" imagen_ext4.dd` intenta volcar el contenido (si los punteros sobreviven).
6. **NTFS vs ext4 al borrar**: NTFS marca el registro MFT como libre pero suele conservar metadatos y *data runs* un tiempo (recuperación por metadatos viable); ext4 **limpia los punteros de bloque del inodo**, dificultando la recuperación por metadatos y forzando a menudo al *carving* o al *journal* (jbd2).

---

## Clase 205 — Análisis de artefactos de Windows

### Solución del reto verificable

Objetivo: demostrar la ejecución de un binario "sospechoso" propio cruzando ≥3 artefactos independientes.

Pasos:

1. En la VM propia, ejecuta el binario de prueba (p. ej. `calc.exe` renombrado a `svch0st.exe` en `C:\Temp\`). Genera actividad.
2. Extrae artefactos (KAPE/FTK Imager) y parséalos con las EZ Tools:

   ```bash
   PECmd.exe -d C:\Windows\Prefetch --csv out --csvf prefetch.csv
   AppCompatCacheParser.exe -f SYSTEM --csv out
   AmcacheParser.exe -f Amcache.hve --csv out
   EvtxECmd.exe -d "C:\...\winevt\Logs" --csv out --csvf events.csv    # filtra 4688
   ```

3. Correlaciona: el `.pf` en Prefetch (nombre, conteo, última ejecución), la entrada de AmCache (ruta + SHA-1) y el Event **4688** (creación de proceso con línea de comandos) deben **coincidir en nombre, ruta y ventana temporal**.

Evidencia que cumple el criterio: tres fuentes distintas (Prefetch + AmCache/ShimCache + Event 4688, o un LNK) que concuerdan en `svch0st.exe`, ruta `C:\Temp\` y la misma franja horaria UTC, con una conclusión escrita: "el binario se ejecutó a las HH:MM UTC del <fecha>".

### Claves de los ejercicios

1. **Qué prueba Prefetch**: prueba que el programa **se ejecutó** (existe el `.pf`), con nombre, conteo de ejecuciones y hasta 8 últimas fechas de ejecución. **No** prueba quién lo ejecutó ni con qué privilegios, y su **ausencia no prueba** que no se ejecutó (Prefetch puede estar deshabilitado).
2. **ShimCache vs AmCache**: ShimCache (AppCompatCache, hive SYSTEM) registra ruta, tamaño y a veces última modificación de binarios "vistos" por el sistema; su orden **no es cronológico fiable**. AmCache (`Amcache.hve`) añade **SHA-1** y más metadatos, mejor para contrastar contra inteligencia de amenazas. Usa ShimCache para presencia amplia; AmCache cuando necesitas hash.
3. **Cinco Event IDs**: 4624 (login exitoso), 4625 (login fallido), 4688 (creación de proceso), 4672 (privilegios especiales asignados a un login), 4634/4647 (logoff); también 1102 (log de seguridad borrado), 7045 (servicio instalado).
4. **Jump List**: parsea con `JLECmd.exe -d AutomaticDestinations --csv out`; muestra los archivos/rutas abiertos recientemente por cada aplicación (AppID) y sus timestamps.
5. **ShellBags de carpeta borrada**: `SBECmd.exe -d <ruta_hives> --csv out` sobre `UsrClass.dat`/`NTUSER.DAT`; una entrada ShellBag de `E:\secreto\` prueba que se **navegó** esa carpeta aunque ya no exista, con su marca de tiempo.
6. **Cruce de tres artefactos**: Prefetch (ejecución) + Event 4688 (proceso con línea de comandos) + LNK/AmCache (ruta + hash), coincidentes en nombre/ruta/tiempo → prueba sólida de ejecución.

---

## Clase 206 — Análisis de artefactos de Linux

### Solución del reto verificable

Objetivo: en una VM Linux propia, plantar 3 mecanismos de persistencia (usuario UID 0, clave SSH, cron) y detectarlos desde la imagen.

Pasos (imagen montada `ro,noexec,nodev`):

1. **Usuario malicioso UID 0**:

   ```bash
   awk -F: '$3==0 {print $1, $3}' /mnt/evidencia/etc/passwd    # cualquiera != root con UID 0
   ```

2. **Clave SSH añadida**:

   ```bash
   cat /mnt/evidencia/home/*/.ssh/authorized_keys /mnt/evidencia/root/.ssh/authorized_keys
   stat /mnt/evidencia/root/.ssh/authorized_keys              # ctime/mtime del cambio
   ```

3. **Cron de persistencia**:

   ```bash
   cat /mnt/evidencia/var/spool/cron/crontabs/* /mnt/evidencia/etc/cron.d/*
   ls -la /mnt/evidencia/etc/systemd/system/                  # timers/servicios sospechosos
   ```

Evidencia que cumple el criterio: el informe nombra el usuario (con su línea de `/etc/passwd` y UID 0), la clave SSH (archivo, `ctime`, huella de la clave) y la tarea cron/systemd (ruta, comando, hora), cada uno con el comando que lo reveló y el timestamp relevante (contrastado con `auth.log`).

### Claves de los ejercicios

1. **Logins SSH exitosos + IP**: `grep "Accepted" /mnt/evidencia/var/log/auth.log` → líneas `Accepted password/publickey for <user> from <IP> port ...`.
2. **Fuerza bruta en btmp**: `lastb -f /mnt/evidencia/var/log/btmp | head`; un pico de fallos del mismo origen/usuario en segundos indica *brute force* (también `grep -c "Failed password" auth.log`).
3. **Cron maliciosa**: aparece en `/var/spool/cron/crontabs/<user>`, `/etc/cron.d/`, `/etc/crontab` o `cron.{hourly,daily}`; búscala por comando anómalo (curl a IP, reverse shell) y por su `ctime` reciente.
4. **UID 0 distinto de root**: `awk -F: '$3==0' /etc/passwd`; cualquier cuenta con UID 0 que no sea `root` es una puerta trasera (privilegios de superusuario).
5. **atime/mtime/ctime**: *atime* = último acceso (lectura); *mtime* = última modificación del **contenido**; *ctime* = última modificación de los **metadatos del inodo** (permisos, dueño, nombre) — se actualiza también al cambiar mtime y es más difícil de falsear con `touch`.
6. **Reconstruir comandos**: ordena `~/.bash_history`/`~/.zsh_history`; si `HISTTIMEFORMAT` estaba activo tendrás horas, si no, solo el orden; correlaciona con `auth.log` y timestamps de archivos creados.

---

## Clase 207 — Forense de memoria RAM con Volatility

### Solución del reto verificable

Objetivo: identificar un proceso malicioso inyectado en un volcado, documentar la detección y extraer su código.

Pasos (Volatility 3):

1. Enumera y compara procesos (ocultamiento por DKOM):

   ```bash
   vol -f memoria.raw windows.pslist
   vol -f memoria.raw windows.psscan     # PIDs en psscan y no en pslist = sospechosos
   vol -f memoria.raw windows.pstree     # relaciones padre-hijo anómalas
   ```

2. Detecta inyección de código (regiones RWX / PE sin archivo asociado):

   ```bash
   vol -f memoria.raw windows.malfind --pid <PID>
   ```

3. Conexión C2 y línea de comandos:

   ```bash
   vol -f memoria.raw windows.netscan
   vol -f memoria.raw windows.cmdline --pid <PID>
   ```

4. Extrae el código. Lo más preciso es volcar la **región inyectada** con malfind, o la **imagen del proceso** con pslist:

   ```bash
   vol -f memoria.raw -o ./salida windows.malfind --pid <PID> --dump
   vol -f memoria.raw -o ./salida windows.pslist --pid <PID> --dump
   ```

   > Nota técnica: para extraer el ejecutable del proceso, `windows.malfind --dump` (región RWX) o `windows.pslist --pid X --dump` (PE del proceso) son lo correcto. `windows.dumpfiles --pid X` vuelca *objetos de archivo* mapeados (DLLs, ficheros abiertos), útil como complemento pero no es la vía directa para el binario inyectado. Ver "Errores técnicos" al pie.

Evidencia que cumple el criterio: (a) PID y nombre del proceso, (b) salida de `malfind` con la región `PAGE_EXECUTE_READWRITE`, (c) la conexión de `netscan` hacia la IP C2, y (d) el binario/región extraído.

### Claves de los ejercicios

1. **RAM antes que disco**: es la evidencia más volátil (se pierde al apagar) y contiene lo que el disco no muestra: procesos, claves de cifrado, malware *fileless*, conexiones activas y credenciales.
2. **Proceso oculto**: `windows.pslist` recorre la lista enlazada del SO (manipulable por rootkit); `windows.psscan` escanea memoria cruda por firmas de `_EPROCESS`. Un PID solo visible en `psscan` = ocultamiento.
3. **Conexión sospechosa (netscan)**: busca conexiones a IP externas por procesos que no deberían tener red (p. ej. `notepad.exe` hablando por 443 a una IP rara), puertos altos y estados `ESTABLISHED`.
4. **Región RWX (malfind)**: `windows.malfind` marca regiones privadas ejecutables+escribibles con cabecera PE (`MZ`) sin archivo mapeado → inyección clásica.
5. **Extraer el ejecutable**: `windows.pslist --pid X --dump` (imagen del proceso) o `windows.malfind --pid X --dump` (código inyectado).
6. **Línea de comandos**: `windows.cmdline --pid X` revela argumentos (p. ej. PowerShell con `-enc`/`-nop -w hidden`) que delatan la intención.

---

## Clase 208 — Forense de red

### Solución del reto verificable

Objetivo: en un PCAP, identificar la IP del C2, el intervalo de beaconing y qué se exfiltró.

Pasos:

1. Conversaciones y candidatos a C2 (destinos muy repetidos, poca variación):

   ```bash
   tshark -r captura.pcap -q -z conv,tcp
   ```

2. Intervalo de beaconing hacia la IP sospechosa (mide deltas entre conexiones):

   ```bash
   tshark -r captura.pcap -Y "ip.dst==<C2> && tcp.flags.syn==1 && tcp.flags.ack==0" \
     -T fields -e frame.time_epoch | awk 'NR>1{print $1-prev} {prev=$1}'
   ```

   Deltas casi constantes (p. ej. ~60 s ± jitter) confirman el beacon; RITA sobre `conn.log` de Zeek lo automatiza.
3. Exfiltración:
   - **DNS**: `tshark -r captura.pcap -Y "dns" -T fields -e dns.qry.name | sort | uniq -c | sort -rn | head` → muchos subdominios largos/aleatorios (TXT) hacia un dominio = túnel.
   - **HTTP**: `File → Export Objects → HTTP` en Wireshark o pestaña *Files* de NetworkMiner para recuperar lo transferido y su tamaño.

Evidencia que cumple el criterio: IP/puerto del C2, intervalo aproximado del beacon con evidencia de periodicidad (lista de deltas), método de exfiltración (DNS o HTTP) y el contenido o tamaño de lo exfiltrado.

### Claves de los ejercicios

1. **Filtro IP+puerto**: en Wireshark `ip.addr == 10.0.0.5 && tcp.port == 443` (display filter).
2. **Extraer archivo HTTP**: `File → Export Objects → HTTP`, elige el objeto y *Save*; o `tshark --export-objects http,carpeta -r captura.pcap`.
3. **Beaconing por periodicidad**: intervalos regulares hacia el mismo destino (histograma de deltas concentrado); el jitter aleatorio se ve como distribución estrecha, no valores idénticos.
4. **Túnel DNS**: gran volumen de consultas a un mismo dominio, subdominios largos codificados (base32/hex), tipos TXT/NULL/CNAME y respuestas grandes.
5. **Diez conversaciones más largas (zeek-cut)**: `zeek -r captura.pcap` y luego `cat conn.log | zeek-cut duration id.orig_h id.resp_h | sort -rn | head`.
6. **TLS: qué se ve / qué no**: **ves** IPs, puertos, SNI, certificado, versión TLS, huellas JA3/JA3S, tamaños y tiempos; **no ves** el contenido descifrado salvo que tengas las claves o el `SSLKEYLOGFILE`.

---

## Clase 209 — Análisis de línea de tiempo (timeline)

### Solución del reto verificable

Objetivo: super-timeline de una imagen propia y narrativa entrada → exfiltración con ≥6 eventos fechados de fuentes distintas.

Pasos:

1. Genera el storage de plaso y acótalo:

   ```bash
   log2timeline.py --storage-file caso.plaso imagen.E01
   pinfo.py caso.plaso
   psort.py -o l2tcsv -w timeline.csv caso.plaso
   psort.py -o l2tcsv -w recorte.csv caso.plaso \
     "date > '2026-07-10 00:00:00' AND date < '2026-07-11 00:00:00'"
   ```

2. Pivotea desde un evento conocido (una ejecución de Prefetch de la clase 205) y examina el entorno temporal.
3. Detecta timestomping: eventos del FS cuyos tiempos no cuadran con `$UsnJrnl` o con los logs que registran el mismo hecho.
4. Reconstruye: entrada (login/phishing) → ejecución (Prefetch/4688) → persistencia (clave Run/tarea) → exfiltración (conexión de red/navegador).

Evidencia que cumple el criterio: narrativa con ≥6 eventos con fecha/hora **UTC**, cada uno respaldado por una fuente identificada (FS, registro, EVTX, navegador…), y las fuentes concuerdan entre sí (o explicas las incoherencias como timestomping).

### Claves de los ejercicios

1. **Contar fuentes**: `pinfo.py caso.plaso` lista *parsers* y contadores por fuente (FILE, WinEVTX, WinReg, etc.); cuenta cuántas distintas aportaron eventos.
2. **Ventana de 2 h**: `psort.py -o l2tcsv -w out.csv caso.plaso "date > '2026-07-10 02:00:00' AND date < '2026-07-10 04:00:00'"`.
3. **Pivote login → malware**: parte del Event 4624/4625, filtra ±minutos y localiza la primera ejecución (Prefetch/4688) del binario.
4. **Timestomping por incoherencia**: un archivo con `$SI` en el pasado pero `$FN`/`$UsnJrnl` recientes; las fuentes que registran el mismo hecho no concuerdan.
5. **Etiquetar en Timesketch**: importa el CSV, crea un *sketch* y marca (star/label) los 5 eventos clave (ejecución, persistencia, movimiento, exfiltración, borrado).
6. **Narrativa (párrafo)**: relato cronológico causal — cómo entró, qué ejecutó, cómo persistió, qué exfiltró y cuándo — sostenido solo con eventos fechados.

---

## Clase 210 — Forense de navegadores y correo

### Solución del reto verificable

Objetivo: demostrar spoofing en un correo propio (servidor de origen real + SPF/DKIM/DMARC) y correlacionar una URL con el historial.

Pasos:

1. Abre el `.eml` como texto y lee la cadena `Received` **de abajo hacia arriba**; el `Received` más antiguo (inferior) revela el servidor/IP de origen real.
2. Lee `Authentication-Results`: `spf=fail`/`softfail`, `dkim=fail` o `none`, y `dmarc=fail` con `From` suplantado = spoofing confirmado (SPF valida el *envelope*, DMARC alinea el `From` visible).
3. Correlaciona la URL del correo con el historial (copia la base con el navegador cerrado):

   ```sql
   -- Chrome/Edge (History)
   SELECT url, title, visit_count,
          datetime(last_visit_time/1000000 - 11644473600,'unixepoch') AS visita_utc
   FROM urls WHERE url LIKE '%dominio-malicioso%' ORDER BY last_visit_time DESC;
   ```

Evidencia que cumple el criterio: (a) servidor de origen real desde la cadena `Received`, (b) resultados SPF/DKIM/DMARC que prueban el spoofing, y (c) evidencia de si el usuario visitó la URL (fila en `urls`/`moz_places`) o no.

### Claves de los ejercicios

1. **WebKit → UTC**: fórmula `unix = webkit/1000000 - 11644473600` (WebKit = microsegundos desde 1601-01-01). Ej.: `SELECT datetime(last_visit_time/1000000 - 11644473600,'unixepoch')`.
2. **Top 10 URLs**: `SELECT url, visit_count FROM urls ORDER BY visit_count DESC LIMIT 10;` (Chrome) o `moz_places` en Firefox.
3. **Reconstruir descarga**: en Chrome, tabla `downloads` (`target_path`, `tab_url`, `start_time`, `total_bytes`) → origen (URL) y destino (ruta local).
4. **Trazar origen por `Received`**: se leen de abajo (origen) hacia arriba (destino); los superiores pueden estar falsificados, los añadidos por tus propios servidores son de confianza.
5. **Spoofing con `Authentication-Results`**: `spf=fail`/`dkim=fail`/`dmarc=fail` junto a un `From` de dominio legítimo suplantado.
6. **Hashear adjunto sin abrirlo**: extrae el adjunto (decodifica base64 del MIME) a un archivo y `sha256sum adjunto` — nunca lo ejecutes; contrasta solo el hash contra VirusTotal.

---

## Clase 211 — Forense móvil

### Solución del reto verificable

Objetivo: en un Android propio, generar actividad, extraerla y reconstruir una timeline (≥5 eventos) desde SQLite + ALEAPP.

Pasos:

1. Conecta y verifica: `adb devices` (autoriza la clave RSA en el móvil).
2. Extracción lógica por backup:

   ```bash
   adb backup -all -f backup.ab
   java -jar abe.jar unpack backup.ab backup.tar    # android-backup-extractor
   ```

3. Info del dispositivo: `adb shell getprop ro.product.model`.
4. Analiza una base SQLite de mensajes **propia** (los timestamps suelen venir en milisegundos):

   ```sql
   SELECT datetime(timestamp/1000,'unixepoch') AS ts_utc, sender, body
   FROM messages ORDER BY timestamp;
   ```

5. Procesa con **ALEAPP** para consolidar ubicación, apps, notificaciones y uso; extrae los eventos y ordénalos.

Evidencia que cumple el criterio: timeline con ≥5 eventos fechados (mensajes, aperturas de app, ubicaciones), cada uno con su base/artefacto de origen, y una nota del **nivel de extracción** logrado (lógica) y por qué (bloqueo/cifrado FBE limitaron un nivel superior).

> Nota: `adb backup` está deprecado y muchas apps modernas (y Android 12+) lo restringen; si falla, documenta la limitación y recurre a ALEAPP sobre un *filesystem dump* (requiere root) o a herramientas comerciales.

### Claves de los ejercicios

1. **Lógica / FS / física**: lógica = archivos que el SO expone vía API/backup (rápida, limitada); sistema de archivos = partición `/data` completa (requiere root/exploit); física = imagen bit a bit de la NAND (máxima, casi inviable con cifrado moderno).
2. **BFU vs AFU**: en *Before First Unlock* las claves de descifrado por archivo (FBE) aún no están en memoria → casi todo cifrado; en *After First Unlock* las claves ya están cargadas → más datos accesibles.
3. **Backup ADB**: `adb backup -all -f backup.ab` y luego `abe.jar unpack` para obtener el `.tar` y listar su contenido.
4. **SQLite de mensajes**: `SELECT datetime(timestamp/1000,'unixepoch'), sender, body FROM messages ORDER BY timestamp;` (divide entre 1000 si es ms).
5. **Informe ALEAPP/iLEAPP**: apunta la herramienta a la extracción (`aleapp.py -i extraccion -o salida -t fs`) y genera el HTML con ubicación, apps y uso.
6. **Requisitos legales**: consentimiento informado del titular **o** orden judicial; documentar cadena de custodia; respetar proporcionalidad y privacidad. Sin autorización, la extracción es ilegal e inadmisible.

---

## Clase 212 — Forense en la nube

### Solución del reto verificable

Objetivo: simular un compromiso de credenciales IAM y reconstruir, solo desde logs, qué hizo/cuándo/desde dónde, preservando la evidencia de forma inmutable.

Pasos (AWS):

1. Simula: usa una clave IAM de prueba desde otra "sesión"/IP para hacer acciones (crear recursos, listar S3).
2. Reconstruye desde CloudTrail:

   ```bash
   aws cloudtrail lookup-events \
     --lookup-attributes AttributeKey=Username,AttributeValue=usuario-prueba
   ```

   De cada evento extrae `eventTime` (UTC), `sourceIPAddress`, `eventName`, `userIdentity` y `resources`.
3. Aísla la instancia comprometida cambiando su *security group* a uno sin tráfico **sin apagarla** (preserva RAM).
4. Preserva: exporta los logs relevantes a un bucket S3 con **Object Lock** (modo *compliance*/retención) o a una cuenta de logging separada.

Evidencia que cumple el criterio: informe con la credencial comprometida, timeline de acciones con marcas UTC, IP de origen, recursos afectados, y prueba de que los logs quedaron con retención/inmutabilidad (config de Object Lock).

### Claves de los ejercicios

1. **Evidencia inaccesible**: el hipervisor, el hardware físico, la red del proveedor y (normalmente) la memoria del host subyacente — trabajas solo con lo que APIs y logs exponen (modelo de responsabilidad compartida).
2. **CloudTrail 24 h de una identidad**: `aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=<id> --start-time <hace 24h> --end-time <ahora>`.
3. **Snapshot de evidencia**: `aws ec2 create-snapshot --volume-id vol-xxxx --description "Evidencia CASO-..."` (etiqueta con el caso).
4. **Login inusual en Azure**: `SigninLogs | where ResultType != 0 | project TimeGenerated, UserPrincipalName, IPAddress, ResultDescription` (o filtra por país/IP no habitual).
5. **Exportar auditoría GCP**: `gcloud logging read 'logName:"cloudaudit.googleapis.com"' --limit 50 --format json > audit.json`.
6. **Aislar sin perder RAM**: cambia el *security group*/NSG a uno que solo permita al analista (o desasócialo de la red) **sin detener** la instancia; captura memoria vía agente antes de cualquier apagado.

---

## Clase 213 — Anti-forense y sus contramedidas

### Solución del reto verificable

Objetivo: aplicar 3 técnicas anti-forense en laboratorio propio y detectarlas con fuentes independientes.

Ejemplo de las tres técnicas y su detección:

1. **Timestomping** → aplica cambiando el mtime de un archivo; **detecta** comparando `$SI` vs `$FN` en la MFT (`MFTECmd.exe -f "$MFT" --csv out`), donde `$SI` < `$FN` es imposible en uso normal. *Fuente redundante*: `$UsnJrnl` y logs registran la creación real.
2. **Limpieza de log** → `wevtutil cl Application`; **detecta** por el **Event 1102** ("audit/log cleared") y por el hueco/salto de secuencia (`EvtxECmd`). *Fuente redundante*: SIEM/reenvío externo conserva lo borrado.
3. **ADS (Alternate Data Stream)** → `echo secreto > archivo.txt:oculto.txt`; **detecta** con `dir /r` o `streams.exe` (Sysinternals). *Fuente redundante*: el `$UsnJrnl`/MFT registra el stream.

Evidencia que cumple el criterio: por cada técnica, (a) cómo la aplicaste, (b) la evidencia que la delató y (c) la fuente redundante independiente usada para detectarla pese a la manipulación.

### Claves de los ejercicios

1. **Timestomping `$SI`/`$FN`**: parsea la MFT y busca `$SI` anterior a `$FN` o subsegundos en cero → manipulación (el kernel solo mueve `$FN`).
2. **Crear/encontrar ADS**: `echo dato > archivo.txt:secreto` y `dir /r` (o `Get-Item archivo.txt -Stream *` en PowerShell) para listarlo.
3. **Limpieza de log (1102)**: filtra el Security log por Event **1102**; su sola presencia indica que alguien borró el registro.
4. **Datos ocultos en imagen**: `zsteg imagen.png` (LSB en PNG) y `binwalk imagen.png` (payloads anexados); compara con el portador original si lo tienes.
5. **TRIM ayuda al atacante**: en SSD, al borrar, TRIM hace que el controlador **borre físicamente** los bloques, eliminando lo que el analista podría recuperar por carving — el borrado seguro "gratis".
6. **Redundancia por técnica**: contra timestomping → `$FN`/`$UsnJrnl`/logs; contra limpieza de logs → SIEM externo/Event 1102; contra ADS/esteganografía → MFT/análisis estadístico; contra wiping → shadow copies, backups, journal, RAM.

---

## Clase 214 — Recuperación de datos y file carving

### Solución del reto verificable

Objetivo: borrar 5 archivos de tipos distintos, recuperarlos por carving y demostrar con hashes cuáles quedaron íntegros.

Pasos:

1. Registra el SHA-256 de los 5 originales antes de borrarlos.
2. Intenta primero metadatos (TSK) y luego carving:

   ```bash
   fls -d -r -o 2048 imagen.dd                 # borrados con metadatos vivos
   foremost -t jpg,pdf,doc,zip,png -i imagen.dd -o salida_foremost
   photorec imagen.dd                          # interactivo, potente en imágenes
   ```

3. Valida cada recuperado: ábrelo, comprueba su firma y compara `sha256sum` con el original.

Evidencia que cumple el criterio: los archivos recuperados + una tabla `hash original vs hash recuperado` por cada uno, y la explicación de los que no coincidieron (fragmentación → carving por header/footer asume contigüidad; sobrescritura parcial; o formato sin footer claro).

### Claves de los ejercicios

1. **Metadatos vs carving**: metadatos primero (rápido y fiable si el inodo/MFT sobrevive); carving cuando el FS ya no referencia el archivo (espacio no asignado).
2. **Firmas (magic numbers)**: JPEG `FF D8 FF` (footer `FF D9`), PDF `25 50 44 46` (`%PDF`), ZIP `50 4B 03 04` (`PK..`); visibles en un editor hex.
3. **PhotoRec + validación**: `photorec imagen.dd`, elige tipos, recupera a una carpeta y valida cada imagen por firma y hash contra el original.
4. **foremost vs Scalpel**: ambos hacen carving por firmas; foremost trae tipos predefinidos, Scalpel usa `/etc/scalpel/scalpel.conf` personalizable — compara qué recupera cada uno sobre la misma imagen (cobertura y falsos positivos).
5. **bulk_extractor**: `bulk_extractor -o salida_bulk imagen.dd` y revisa `email.txt`, `url.txt`, `ccn.txt`, `domain.txt` (triage sin parsear el FS).
6. **Fragmentación arruina el carving**: el carving por header/footer asume que el archivo es **contiguo**; si está disperso en clusters no contiguos, une bloques equivocados y produce archivos corruptos.

---

## Clase 215 — Playbooks de respuesta a incidentes

### Solución del reto verificable

Objetivo: playbook de "cuenta de correo corporativa comprometida" con 6 fases PICERL, ≥4 puntos de decisión, mapeo ATT&CK, escalado y 3 pasos automatizables.

Esqueleto que cumple el criterio:

- **Preparación**: MFA y logging de buzones activos; contactos de escalado; acceso a consola de identidad.
- **Identificación**: validar la alerta (login imposible/geográfico, reglas de reenvío nuevas). *Decisión 1*: ¿login anómalo confirmado? sí→continúa / no→cerrar.
- **Contención**: revocar sesiones/tokens, forzar reset de contraseña, bloquear temporalmente la cuenta. *Decisión 2*: ¿hay regla de reenvío/filtro malicioso? sí→eliminar y buscar exfiltración.
- **Erradicación**: quitar reglas maliciosas, apps OAuth no autorizadas, delegaciones; revisar buzones tocados. *Decisión 3*: ¿se enviaron correos desde la cuenta? sí→notificar destinatarios.
- **Recuperación**: rehabilitar la cuenta con MFA reforzada y monitoreo. *Decisión 4*: ¿reincidencia en X días? sí→reabrir.
- **Lecciones aprendidas**: post-mortem, endurecer políticas (bloqueo de reenvío externo), actualizar el playbook.

Mapeo ATT&CK: **T1078** (Valid Accounts), **T1114** (Email Collection), **T1564.008** (Email Hiding Rules), **T1566** (Phishing, si fue el vector). Automatizables con SOAR: revocar sesiones, enriquecer IOCs (IP de login), notificar al usuario y al SOC.

### Claves de los ejercicios

1. **Contención de ransomware**: aislar host(s) por red sin apagar; deshabilitar comparticiones/cuentas afectadas; bloquear IOCs (hash/IP/C2) en EDR y firewall; preservar RAM y disco antes de limpiar.
2. **Cinco puntos de decisión (cuenta comprometida)**: ¿login anómalo confirmado? ¿MFA comprometida? ¿reglas de reenvío creadas? ¿se accedió a datos sensibles? ¿es cuenta privilegiada/ejecutiva (escalar)?
3. **Malware → 3 ATT&CK**: p. ej. T1566 (Phishing, acceso inicial), T1059 (Command and Scripting Interpreter, ejecución), T1547 (Boot/Logon Autostart, persistencia).
4. **Escalado a legal/dirección**: datos personales/regulados afectados; múltiples víctimas o ejecutivos; posible obligación de notificación (GDPR 72 h); extorsión/mención en prensa; impacto financiero sobre umbral.
5. **Tres pasos automatizables (SOAR)**: enriquecer IOCs (reputación de IP/hash/dominio), bloquear en gateway/EDR/firewall, y notificar/crear ticket — repetibles, deterministas y sin criterio humano.
6. **Diagrama de flujo phishing**: reporte → validar → ¿es phishing? (no→cerrar / sí→) extraer IOCs → búsqueda retroactiva → ¿hizo clic? (sí→reset credenciales+revisar sesión / no→) bloquear remitente/URL → lecciones.

---

## Clase 216 — Contención, erradicación y recuperación

### Solución del reto verificable

Objetivo: sobre una VM comprometida por ti, ejecutar contención con preservación, erradicación completa y validación.

Pasos:

1. **Contén sin perder evidencia**: aísla por red (acción "aislar" del EDR o regla que solo permita la IP del analista) **sin apagar**.
2. **Captura evidencia** antes de limpiar: volcado de RAM (clase 207) e imagen de disco E01 (clase 203), con hashes y custodia.
3. **Enumera TODA la persistencia**:

   ```powershell
   autorunsc.exe -a * -c > autoruns.csv   # servicios, tareas, claves Run, WMI, drivers
   ```

   En Linux: cron, `systemd` timers/services, `rc.local`, perfiles de shell, `authorized_keys`.
4. **Erradica** cada mecanismo + el binario; si el compromiso fue a nivel SYSTEM/root, planifica **reconstrucción desde cero**.
5. **Rota credenciales**: contraseñas, tokens, sesiones y claves API que el atacante pudo ver.
6. **Valida**: periodo de observación con criterios objetivos (cero IOCs, cero conexiones al C2, cero reintentos de persistencia).

Evidencia que cumple el criterio: (a) cómo aislaste sin perder evidencia, (b) lista completa de persistencia hallada y eliminada, (c) rotación de credenciales, (d) criterios cumplidos para declarar erradicado.

### Claves de los ejercicios

1. **Aislar vs observar (3 escenarios)**: ransomware cifrando → **aislar ya**; robo silencioso de datos donde quieres alcance completo y puedes contener el daño → **observar** brevemente con captura; host crítico de producción con impacto de negocio → aislar por red preservando RAM. Ante la duda, aislar.
2. **Cinco persistencias Windows**: claves Run/RunOnce, tareas programadas, servicios, suscripciones WMI de eventos, carpeta Startup / DLL search-order hijacking.
3. **Cuándo reconstruir**: cuando hubo compromiso con privilegios altos (SYSTEM/root) o rootkits/bootkits — no puedes confiar en que la limpieza fue total; reinstalar desde cero es la única garantía.
4. **Rotación de credenciales**: inventariar todo lo que el atacante pudo ver (contraseñas de usuarios/servicio, tokens, claves API, secretos), cambiarlas, revocar sesiones/tokens vigentes y forzar re-autenticación con MFA.
5. **Criterios de validación**: cero IOCs activos, cero conexiones al C2, cero reintentos de la persistencia eliminada, EDR sin alertas durante el periodo de observación definido.
6. **Contener sin perder RAM**: aislar por **red** (EDR/firewall/VLAN de cuarentena) manteniendo el equipo encendido — nunca apagar antes de volcar la memoria.

---

## Clase 217 — Análisis de causa raíz

### Solución del reto verificable

Objetivo: RCA completo de un incidente investigado: árbol de 5 Porqués, Ishikawa, kill chain y ≥3 acciones correctivas contra causas raíz con criterio de verificación.

Ejemplo (ransomware por macro):

- **5 Porqués**: se cifraron archivos → se ejecutó ransomware → un usuario abrió un adjunto con macro → las macros no estaban bloqueadas por política → el gateway no filtró el adjunto → la cuenta tenía privilegios excesivos que permitieron el cifrado en red.
- **Ishikawa**: Personas (falta de concienciación) · Proceso (sin filtrado de correo) · Tecnología (sin EDR/bloqueo de macros) · Configuración (privilegios excesivos, sin segmentación).
- **Kill chain**: acceso inicial (phishing) → ejecución (macro) → persistencia → movimiento lateral → impacto (cifrado).
- **Acciones correctivas verificables**: (1) bloquear macros de Office por **GPO** — verificable abriendo un doc con macro y comprobando que no corre; (2) filtrado de adjuntos en el gateway — verificable enviando una prueba; (3) principio de **mínimo privilegio** y segmentación — verificable auditando permisos de la cuenta. Cada una con responsable y fecha.

Evidencia que cumple el criterio: cada acción ataca una **causa raíz** (no un síntoma), con responsable, fecha y verificación objetiva; el post-mortem es **blameless** (no señala individuos).

### Claves de los ejercicios

1. **5 Porqués (phishing)**: hubo credenciales robadas → el usuario las metió en una web falsa → el correo llegó a la bandeja → el filtro no lo bloqueó → no había DMARC/entrenamiento → falta de controles de correo e identidad (raíz).
2. **Ishikawa (4 categorías)**: Personas, Proceso, Tecnología, Configuración (o Entorno) — cada rama con causas concretas.
3. **Próxima vs raíz (3 casos)**: para cada incidente, la próxima es el disparo inmediato (macro ejecutada) y la raíz la condición de fondo (macros no bloqueadas / falta de control).
4. **Tres acciones verificables**: cada una concreta y medible (GPO aplicada, regla de filtrado activa, permisos reducidos), con forma objetiva de comprobar su implementación.
5. **MTTD/MTTR**: MTTD = t(detección) − t(inicio del incidente); MTTR = t(resolución) − t(detección), leídos de la timeline.
6. **Reescribir blameless**: cambia "Juan hizo clic" por "el control de correo permitió que un adjunto malicioso llegara y no había bloqueo de macros"; enfoca en el sistema, no en la persona.

---

## Clase 218 — Reporte forense y aspectos legales

### Solución del reto verificable

Objetivo: informe forense completo, con hallazgos que separan hecho de opinión, custodia trazable y versión ejecutiva aparte.

Estructura que cumple el criterio:

1. **Portada**: caso, examinador, fechas, clasificación de confidencialidad.
2. **Resumen ejecutivo** (media página, sin jerga): qué pasó, impacto y recomendación clave.
3. **Alcance y limitaciones**: qué se analizó, qué no y por qué.
4. **Metodología**: herramientas **con versiones**, procedimientos y **hashes** de las imágenes (reproducibilidad).
5. **Hallazgos** separando explícitamente:
   - *Hecho*: "Prefetch registra la ejecución de `x.exe` el 2026-07-10 03:14 UTC (SHA-256: …)."
   - *Opinión*: "En mi opinión profesional, es consistente con la ejecución del malware descrito."
6. **Timeline** y **cadena de custodia** completa (sin huecos).
7. **Conclusiones**, **recomendaciones** y **anexos** (hashes, capturas, comandos).
8. **Versión ejecutiva** independiente.

Evidencia que cumple el criterio: un tercero puede reproducir el análisis (herramientas/versiones/hashes), cada hallazgo separa hecho de interpretación, la custodia no tiene huecos y hay un resumen ejecutivo comprensible sin conocimientos técnicos.

### Claves de los ejercicios

1. **Resumen ejecutivo**: media página, sin jerga — qué ocurrió, alcance/impacto, y recomendación principal para dirección.
2. **Hecho vs opinión (3 hallazgos)**: el hecho cita el artefacto y su hash/hora UTC; la opinión, marcada como tal, interpreta ("consistente con…").
3. **Metodología**: lista herramientas con versión (FTK Imager x.y, Volatility 3.x, plaso x.y), comandos y hashes de las imágenes.
4. **Cadena de custodia de un ítem**: ID, descripción, adquisición (fecha UTC, examinador, hash) e historial de transferencias firmadas.
5. **Adaptar hallazgo a audiencia legal**: traducir lo técnico a lenguaje claro, ligado a la pregunta legal, distinguiendo hecho de opinión y evitando afirmaciones no sostenidas por la evidencia.
6. **Notificación GDPR**: notificar a la autoridad de control en **72 h** desde el conocimiento de una brecha de datos personales con riesgo; y a los afectados sin dilación indebida si el riesgo es alto (arts. 33–34).

---

## Clase 219 — Ejercicios de mesa (tabletop)

### Solución del reto verificable

Objetivo: paquete de tabletop completo listo para ejecutar por otro facilitador.

Contenido que cumple el criterio:

- **Objetivos medibles**: p. ej. "validar el playbook de ransomware y los criterios de escalado".
- **Escenario** realista para el contexto (ransomware que cifra un servidor de archivos y exige rescate + amenaza de filtración).
- **MSEL** cronometrada con ≥5 injects: T+0 EDR alerta cifrado masivo · T+15 usuarios sin acceso a archivos · T+30 nota de rescate + amenaza de filtración · T+45 periodista pide comentarios · T+60 el atacante publica una muestra de datos.
- **Roles**: facilitador, participantes (IR, TI, legal, comunicación, dirección) y observador.
- **Puntos de decisión**: ¿se paga el rescate? ¿se notifica a la autoridad? ¿quién habla con prensa? ¿se activa DRP?
- **Rúbrica** de evaluación (tiempo de decisión, uso del playbook, comunicación, escalado correcto).

Evidencia que cumple el criterio: otro facilitador puede correrlo sin ayuda; incluye objetivos medibles, MSEL con 5 injects, roles claros, puntos de decisión y rúbrica.

### Claves de los ejercicios

1. **Tres objetivos medibles**: validar playbook X; verificar criterios de escalado; medir tiempo hasta la primera decisión de contención.
2. **MSEL con 5 injects**: eventos progresivos con tiempo (T+0…T+60) que obligan a decidir (ver reto).
3. **Escenario de brecha de datos con prensa**: exfiltración de datos de clientes; inject de periodista a T+X que fuerza a comunicación/legal a decidir el mensaje.
4. **Preguntas para dirección/legal**: ¿se notifica a la autoridad y en qué plazo? ¿se paga? ¿comunicación pública? ¿implicaciones contractuales/regulatorias?
5. **Rúbrica**: criterios (detección, contención, comunicación, escalado, decisión) × niveles (deficiente/adecuado/excelente) con descriptores observables.
6. **Guion de hotwash (15 min)**: qué funcionó, qué no, qué faltó en los playbooks, y acciones de mejora con responsable — en caliente, sin culpas.

---

## Clase 220 — Caso completo de respuesta a incidentes end-to-end

### Solución del reto verificable

Objetivo: resolver el incidente completo (alerta de PowerShell ofuscado con C2) y entregar el paquete final correlacionando memoria, disco y red.

Pasos:

1. **Triage/identificación**: valida la alerta, clasifica severidad (clase 202), decide **aislar por red preservando RAM** (clase 216).
2. **Adquisición multi-fuente**: RAM con WinPmem y disco con FTK Imager→E01 (hashes + custodia, clases 201/203/207); captura de red si el atacante sigue activo (clase 208).
3. **Memoria (Volatility 3)**:

   ```bash
   vol -f memoria.raw windows.malfind      # inyección RWX
   vol -f memoria.raw windows.netscan      # IP/puerto C2
   vol -f memoria.raw windows.cmdline      # PowerShell ofuscado (-enc)
   ```

4. **Disco (Autopsy/TSK + EZ Tools)**: Prefetch, ShimCache/AmCache, tareas programadas, claves Run (clases 204/205).
5. **Red (Zeek/Wireshark)**: confirma C2, beaconing y exfiltración (clase 208).
6. **Timeline maestra (plaso)**: super-timeline y secuencia entrada → ejecución → persistencia → movimiento → exfiltración (clase 209).
7. **Contención/erradicación**: enumera toda la persistencia, elimínala, rota credenciales, valida (clase 216).
8. **RCA e informe**: 5 Porqués + Ishikawa (clase 217) e informe forense + post-mortem blameless (clases 217/218).

Evidencia que cumple el criterio: la narrativa se apoya en las **tres fuentes** (memoria, disco, red) concordantes; la timeline maestra tiene ≥8 eventos fechados en UTC; el informe permite reproducir el análisis; y las acciones correctivas atacan causas raíz.

### Claves de los ejercicios

1. **Decisión de triage**: aislar por red preservando RAM; severidad alta porque hay ejecución con C2 externo y posible exfiltración en un endpoint corporativo.
2. **Correlación memoria/disco/red**: el proceso inyectado (memoria) coincide con el binario/persistencia (disco) y con la conexión al C2 (red) en la misma ventana temporal.
3. **Timeline maestra (≥8 eventos)**: login → ejecución PowerShell → descarga payload → creación de persistencia (tarea/Run) → inyección → beaconing C2 → movimiento lateral → exfiltración, todos en UTC.
4. **Persistencia del atacante**: tareas programadas, claves Run, servicio, suscripción WMI, o clave SSH/cron si hubo Linux — enumeradas con Autoruns/cron/systemd.
5. **Cinco IOCs**: hash SHA-256 del binario, IP/puerto del C2, dominio del C2, nombre/ruta del archivo malicioso, y la cadena de PowerShell ofuscado (o mutex/clave de registro).
6. **Tres acciones correctivas (causas raíz)**: restringir/loguear PowerShell (Constrained Language + ScriptBlock logging), bloquear el C2 y aplicar EDR con detección de inyección, y mínimo privilegio + segmentación para frenar el movimiento lateral.

---

## Errores técnicos detectados

Revisión de los README 201–220. La calidad técnica general es alta; los puntos siguientes son imprecisiones a corregir, no fallos graves:

1. **Clase 207 (y clase 220), reto y laboratorio** — el README indica extraer el ejecutable del proceso malicioso con `windows.dumpfiles --pid <PID>`. En Volatility 3, `windows.dumpfiles` vuelca **objetos de archivo** mapeados en memoria (DLLs, ficheros abiertos), no la imagen del proceso ni la región inyectada. Para el objetivo del reto lo correcto es `windows.malfind --pid <PID> --dump` (región RWX inyectada) o `windows.pslist --pid <PID> --dump` (PE del proceso). Cita: *"vol -f memoria.raw -o ./salida windows.dumpfiles --pid 1337"* con criterio *"el binario extraído con `dumpfiles`"*. Corrección: usar `malfind --dump`/`pslist --dump` para el binario y reservar `dumpfiles` como complemento.

2. **Clase 204, sección Definiciones** — MACB se define como *"Modified, Accessed, Changed/Created, Born"*. La **C** de MACB es **Changed** (cambio de metadatos / `ctime`, en NTFS la modificación de la entrada MFT), **no** "Created"; la creación es la **B** (Born). Etiquetar la C como "Changed/Created" mezcla dos conceptos distintos. Corrección: C = Changed (metadatos), B = Born (creación).

Observaciones menores (no bloqueantes, conviene matizar en clase, no las cuento como errores):

- **Clase 203, laboratorio paso 2**: *"Monta el original en solo lectura … `blockdev --setro /dev/sdX`"*. `blockdev --setro` marca el **dispositivo de bloque** como solo lectura; no "monta" nada. Es correcto para el fin (write-blocker por software) pero la palabra "monta" es imprecisa.
- **Clase 211**: `adb backup` está **deprecado** y restringido en Android 12+ y por apps con `allowBackup=false`; el propio README lo reconoce en "Errores comunes", conviene señalarlo también en el laboratorio.
