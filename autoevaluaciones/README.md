# 📝 Autoevaluaciones

Batería de preguntas por parte para comprobar lo aprendido. Esta es la versión de lectura (con respuestas plegadas). Para la versión **interactiva** con puntuación, abre [`quiz.html`](quiz.html) desde el [sitio del curso](https://vladimiracunadev-create.github.io/modern-cybersecurity-program/autoevaluaciones/quiz.html).

> 🧭 ¿No sabes por dónde empezar? Mira las [rutas por rol](../rutas/README.md).

<a id="progreso"></a>

## Seguimiento de progreso

Lleva la cuenta de todas las clases del programa en [`progreso.html`](progreso.html) (se guarda en tu navegador).

---

## Parte 0 — Fundamentos y prerrequisitos

**1. ¿Qué representa la 'I' de la tríada CIA?**

- a) Identidad
- b) Integridad
- c) Interoperabilidad
- d) Infraestructura

<details><summary>Ver respuesta</summary>

**Correcta: b) Integridad.** CIA = Confidencialidad, Integridad, Disponibilidad (Availability).

</details>

**2. ¿En qué capa del modelo OSI opera TCP?**

- a) Enlace de datos
- b) Red
- c) Transporte
- d) Aplicación

<details><summary>Ver respuesta</summary>

**Correcta: c) Transporte.** TCP y UDP son protocolos de la capa 4 (Transporte).

</details>

**3. ¿Cuál es la principal diferencia entre codificar (Base64) y cifrar?**

- a) Ninguna, son sinónimos
- b) Codificar requiere clave; cifrar no
- c) Cifrar aporta confidencialidad con una clave; codificar es reversible sin clave
- d) Base64 es más seguro que AES

<details><summary>Ver respuesta</summary>

**Correcta: c) Cifrar aporta confidencialidad con una clave; codificar es reversible sin clave.** Base64/hex/ROT no protegen: se revierten sin clave. Cifrar exige una clave secreta.

</details>

**4. El principio de 'mínimo privilegio' consiste en…**

- a) Dar a cada entidad solo los permisos que necesita
- b) Usar contraseñas cortas
- c) Deshabilitar todos los logs
- d) Compartir credenciales de admin

<details><summary>Ver respuesta</summary>

**Correcta: a) Dar a cada entidad solo los permisos que necesita.** Menos privilegios = menor superficie de ataque e impacto ante un compromiso.

</details>

**5. ¿Qué comando/entorno es el adecuado para practicar técnicas ofensivas?**

- a) La red corporativa de producción
- b) Un laboratorio aislado y propio (VMs/red aislada)
- c) Cualquier servidor de Internet
- d) El wifi del vecino

<details><summary>Ver respuesta</summary>

**Correcta: b) Un laboratorio aislado y propio (VMs/red aislada).** Solo en entornos propios o con autorización explícita: lo contrario es delito.

</details>

## Parte 1 — Redes y seguridad de redes

**1. ¿Qué hace `nmap -sS`?**

- a) Escaneo UDP
- b) Escaneo SYN (half-open)
- c) Detección de versión
- d) Escaneo de vulnerabilidades

<details><summary>Ver respuesta</summary>

**Correcta: b) Escaneo SYN (half-open).** -sS es el SYN scan: envía SYN y no completa el handshake.

</details>

**2. El ARP spoofing permite principalmente…**

- a) Cifrar el tráfico
- b) Interceptar tráfico de la LAN (MitM)
- c) Acelerar la red
- d) Bloquear DNS

<details><summary>Ver respuesta</summary>

**Correcta: b) Interceptar tráfico de la LAN (MitM).** Envenena la caché ARP para situarse en medio del tráfico de capa 2.

</details>

**3. Diferencia entre IDS e IPS:**

- a) El IDS bloquea; el IPS solo alerta
- b) El IDS detecta/alerta; el IPS además puede bloquear en línea
- c) Son idénticos
- d) El IPS solo funciona en la nube

<details><summary>Ver respuesta</summary>

**Correcta: b) El IDS detecta/alerta; el IPS además puede bloquear en línea.** IPS está en línea y puede cortar el tráfico; el IDS observa y alerta.

</details>

**4. ¿En qué puerto opera DNS habitualmente?**

- a) 22
- b) 53
- c) 80
- d) 443

<details><summary>Ver respuesta</summary>

**Correcta: b) 53.** DNS usa el 53 (UDP y TCP). Su apertura casi universal habilita el tunneling.

</details>

**5. Un objetivo Windows suele no responder a escaneos FIN/NULL/Xmas porque…**

- a) Tiene el firewall apagado
- b) No sigue estrictamente el RFC 793 en ese comportamiento
- c) Usa IPv6
- d) Nmap no soporta Windows

<details><summary>Ver respuesta</summary>

**Correcta: b) No sigue estrictamente el RFC 793 en ese comportamiento.** Esos escaneos dependen del comportamiento RFC 793 que Windows no implementa igual.

</details>

## Parte 2 — Criptografía aplicada

**1. ¿Cuál es una propiedad esperada de una función hash criptográfica?**

- a) Ser reversible
- b) Resistencia a colisiones
- c) Requerir una clave
- d) Comprimir sin pérdida

<details><summary>Ver respuesta</summary>

**Correcta: b) Resistencia a colisiones.** Debe ser unidireccional y resistente a colisiones; no usa clave (a diferencia de HMAC).

</details>

**2. ¿Por qué el modo ECB es inseguro para datos con patrones?**

- a) Es muy lento
- b) Bloques de texto idénticos producen bloques cifrados idénticos
- c) No usa clave
- d) Solo cifra texto ASCII

<details><summary>Ver respuesta</summary>

**Correcta: b) Bloques de texto idénticos producen bloques cifrados idénticos.** ECB filtra patrones; usa modos con IV (CBC/CTR) o AEAD (GCM).

</details>

**3. Para almacenar contraseñas, ¿qué es lo recomendado hoy?**

- a) MD5 sin sal
- b) SHA-1
- c) Argon2 / bcrypt / scrypt con sal
- d) Base64

<details><summary>Ver respuesta</summary>

**Correcta: c) Argon2 / bcrypt / scrypt con sal.** Funciones de derivación lentas y con sal frenan el crackeo masivo.

</details>

**4. En criptografía asimétrica (RSA), lo que cifra con la clave pública se descifra con…**

- a) La misma clave pública
- b) La clave privada correspondiente
- c) Un hash
- d) Una sal

<details><summary>Ver respuesta</summary>

**Correcta: b) La clave privada correspondiente.** Par de claves: lo cifrado con la pública solo lo abre la privada.

</details>

**5. ¿Qué garantiza principalmente TLS en una conexión HTTPS?**

- a) Solo velocidad
- b) Confidencialidad, integridad y autenticación del servidor
- c) Que el sitio no tenga bugs
- d) Anonimato total

<details><summary>Ver respuesta</summary>

**Correcta: b) Confidencialidad, integridad y autenticación del servidor.** TLS cifra el canal, verifica integridad y autentica al servidor vía certificado.

</details>

## Parte 3 — Hacking ético y pentesting: metodología

**1. ¿Qué documento define el alcance y lo permitido en un pentest?**

- a) El reporte final
- b) Las reglas de engagement (RoE) / contrato
- c) El exploit
- d) El README

<details><summary>Ver respuesta</summary>

**Correcta: b) Las reglas de engagement (RoE) / contrato.** Las RoE fijan alcance, ventanas, límites y autorización por escrito.

</details>

**2. En la metodología PTES, el reconocimiento va…**

- a) Al final
- b) Antes de la explotación
- c) Nunca
- d) Solo en web

<details><summary>Ver respuesta</summary>

**Correcta: b) Antes de la explotación.** Recon y enumeración preceden a la explotación y post-explotación.

</details>

**3. Meterpreter se usa típicamente en la fase de…**

- a) Reconocimiento pasivo
- b) Post-explotación
- c) Redacción del informe
- d) Escaneo de puertos

<details><summary>Ver respuesta</summary>

**Correcta: b) Post-explotación.** Es un payload de post-explotación de Metasploit.

</details>

**4. ¿Qué NO debe hacer un pentester ético durante un engagement?**

- a) Documentar hallazgos
- b) Respetar el alcance
- c) Borrar los logs para ocultar su actividad
- d) Reportar vulnerabilidades

<details><summary>Ver respuesta</summary>

**Correcta: c) Borrar los logs para ocultar su actividad.** El consultor preserva evidencia y trazabilidad; no destruye registros.

</details>

**5. Lo más importante del entregable final es…**

- a) La cantidad de comandos
- b) El resumen ejecutivo y hallazgos priorizados por riesgo
- c) El color del PDF
- d) El número de páginas

<details><summary>Ver respuesta</summary>

**Correcta: b) El resumen ejecutivo y hallazgos priorizados por riesgo.** Debe permitir a negocio decidir y a los técnicos remediar.

</details>

## Parte 4 — Seguridad de aplicaciones web

**1. La inyección SQL ocurre cuando…**

- a) El servidor es lento
- b) La entrada del usuario se concatena sin parametrizar en la consulta
- c) Se usa HTTPS
- d) El sitio usa cookies

<details><summary>Ver respuesta</summary>

**Correcta: b) La entrada del usuario se concatena sin parametrizar en la consulta.** La defensa principal son las consultas parametrizadas (prepared statements).

</details>

**2. ¿Qué tipo de XSS persiste en el servidor y afecta a otros usuarios?**

- a) Reflejado
- b) Almacenado
- c) Basado en DOM
- d) Ninguno

<details><summary>Ver respuesta</summary>

**Correcta: b) Almacenado.** El XSS almacenado guarda el payload y se sirve a cada visitante.

</details>

**3. SSRF permite a un atacante…**

- a) Cifrar la base de datos
- b) Hacer que el servidor haga peticiones a destinos internos
- c) Acelerar la app
- d) Cambiar el CSS

<details><summary>Ver respuesta</summary>

**Correcta: b) Hacer que el servidor haga peticiones a destinos internos.** Server-Side Request Forgery abusa del servidor como proxy hacia recursos internos.

</details>

**4. IDOR es un fallo de…**

- a) Cifrado
- b) Control de acceso (referencia directa a objetos sin autorización)
- c) Rendimiento
- d) Configuración de DNS

<details><summary>Ver respuesta</summary>

**Correcta: b) Control de acceso (referencia directa a objetos sin autorización).** Cambiar un identificador accede a datos de otro usuario por falta de verificación.

</details>

**5. La mejor defensa contra CSRF es…**

- a) Ocultar el formulario
- b) Tokens anti-CSRF y SameSite en cookies
- c) Usar GET para todo
- d) Deshabilitar JavaScript

<details><summary>Ver respuesta</summary>

**Correcta: b) Tokens anti-CSRF y SameSite en cookies.** Token por sesión/petición y cookies SameSite frenan la petición forjada.

</details>

## Parte 5 — Explotación de sistemas y binarios

**1. Un buffer overflow en el stack puede sobrescribir…**

- a) El BIOS
- b) La dirección de retorno guardada
- c) El disco duro
- d) El DNS

<details><summary>Ver respuesta</summary>

**Correcta: b) La dirección de retorno guardada.** Al desbordar, se pisa la saved return address y se desvía el flujo.

</details>

**2. ¿Qué protección aleatoriza las direcciones de memoria?**

- a) DEP/NX
- b) ASLR
- c) Stack canary
- d) PIE

<details><summary>Ver respuesta</summary>

**Correcta: b) ASLR.** ASLR randomiza el mapa de memoria; DEP/NX marca zonas no ejecutables.

</details>

**3. ROP (Return-Oriented Programming) sirve para…**

- a) Compilar más rápido
- b) Ejecutar código reutilizando 'gadgets' cuando NX impide shellcode
- c) Cifrar el binario
- d) Depurar sin GDB

<details><summary>Ver respuesta</summary>

**Correcta: b) Ejecutar código reutilizando 'gadgets' cuando NX impide shellcode.** Encadena gadgets que terminan en `ret` para eludir NX/DEP.

</details>

**4. ¿Qué herramienta es de ingeniería inversa?**

- a) Nmap
- b) Ghidra
- c) Wireshark
- d) Hydra

<details><summary>Ver respuesta</summary>

**Correcta: b) Ghidra.** Ghidra (y IDA/radare2) desensamblan y decompilan binarios.

</details>

**5. El fuzzing busca vulnerabilidades…**

- a) Leyendo el manual
- b) Enviando entradas malformadas/aleatorias para provocar fallos
- c) Cifrando el binario
- d) Escaneando puertos

<details><summary>Ver respuesta</summary>

**Correcta: b) Enviando entradas malformadas/aleatorias para provocar fallos.** AFL++/libFuzzer mutan entradas para encontrar crashes explotables.

</details>

## Parte 6 — Análisis de malware

**1. El análisis estático se diferencia del dinámico en que…**

- a) Ejecuta la muestra
- b) Examina la muestra SIN ejecutarla
- c) Requiere Internet
- d) Solo aplica a Linux

<details><summary>Ver respuesta</summary>

**Correcta: b) Examina la muestra SIN ejecutarla.** Estático = sin ejecutar (strings, PE, desensamblado); dinámico = observar en ejecución.

</details>

**2. ¿Dónde se debe ejecutar malware para analizarlo?**

- a) En tu equipo principal
- b) En una VM aislada sin acceso a la red productiva
- c) En un servidor de producción
- d) En el móvil

<details><summary>Ver respuesta</summary>

**Correcta: b) En una VM aislada sin acceso a la red productiva.** Sandbox/VM aislada con snapshots; nunca en equipos reales o con red abierta.

</details>

**3. Las reglas YARA sirven para…**

- a) Cifrar malware
- b) Detectar/clasificar muestras por patrones
- c) Acelerar el disco
- d) Compilar exploits

<details><summary>Ver respuesta</summary>

**Correcta: b) Detectar/clasificar muestras por patrones.** YARA describe patrones (strings/bytes) para cazar familias de malware.

</details>

**4. El 'packing' de un binario busca…**

- a) Reducir su tamaño y/o ofuscar su contenido
- b) Firmarlo digitalmente
- c) Documentarlo
- d) Traducirlo

<details><summary>Ver respuesta</summary>

**Correcta: a) Reducir su tamaño y/o ofuscar su contenido.** Comprime/cifra el código; hay que 'unpackear' para analizarlo.

</details>

**5. El tráfico C2 de un malware es…**

- a) Su interfaz gráfica
- b) El canal de comando y control con el atacante
- c) Un antivirus
- d) Un instalador

<details><summary>Ver respuesta</summary>

**Correcta: b) El canal de comando y control con el atacante.** Command & Control: recibe órdenes y exfiltra datos; su beaconing es detectable.

</details>

## Parte 7 — Red Team y operaciones ofensivas

**1. MITRE ATT&CK es…**

- a) Un antivirus
- b) Una base de conocimiento de tácticas y técnicas de adversarios
- c) Un lenguaje de programación
- d) Un firewall

<details><summary>Ver respuesta</summary>

**Correcta: b) Una base de conocimiento de tácticas y técnicas de adversarios.** Mapea el comportamiento del adversario; sirve para ofensiva y defensa.

</details>

**2. El Kerberoasting ataca…**

- a) Certificados TLS
- b) Cuentas de servicio pidiendo tickets TGS crackeables offline
- c) El BIOS
- d) El DNS

<details><summary>Ver respuesta</summary>

**Correcta: b) Cuentas de servicio pidiendo tickets TGS crackeables offline.** Solicita TGS de cuentas con SPN y crackea su hash fuera de línea.

</details>

**3. Pass-the-Hash permite autenticarse…**

- a) Con la contraseña en claro
- b) Usando el hash NTLM sin conocer la contraseña
- c) Solo con biometría
- d) Con un OTP

<details><summary>Ver respuesta</summary>

**Correcta: b) Usando el hash NTLM sin conocer la contraseña.** Reutiliza el hash como credencial para moverse lateralmente.

</details>

**4. BloodHound se usa para…**

- a) Cifrar el dominio
- b) Graficar rutas de ataque en Active Directory
- c) Escanear puertos
- d) Analizar malware

<details><summary>Ver respuesta</summary>

**Correcta: b) Graficar rutas de ataque en Active Directory.** Modela relaciones AD y encuentra caminos hacia Domain Admins.

</details>

**5. Un Golden Ticket se forja con el hash de…**

- a) Administrator local
- b) La cuenta krbtgt
- c) El usuario invitado
- d) La cuenta SYSTEM

<details><summary>Ver respuesta</summary>

**Correcta: b) La cuenta krbtgt.** Con el hash de krbtgt se firman TGTs arbitrarios (control total del dominio).

</details>

## Parte 8 — Blue Team, detección y SOC

**1. Un SIEM sirve principalmente para…**

- a) Cifrar discos
- b) Centralizar, correlacionar y alertar sobre logs/telemetría
- c) Escanear puertos
- d) Compilar exploits

<details><summary>Ver respuesta</summary>

**Correcta: b) Centralizar, correlacionar y alertar sobre logs/telemetría.** Agrega eventos de múltiples fuentes y dispara detecciones.

</details>

**2. Sigma es…**

- a) Un SIEM propietario
- b) Un formato genérico de reglas de detección portable entre SIEMs
- c) Un malware
- d) Un protocolo de red

<details><summary>Ver respuesta</summary>

**Correcta: b) Un formato genérico de reglas de detección portable entre SIEMs.** Describe detecciones en YAML y se traduce a la query de cada SIEM.

</details>

**3. El 'threat hunting' es…**

- a) Esperar alertas pasivamente
- b) Buscar proactivamente amenazas no detectadas por las alertas
- c) Apagar el SIEM
- d) Instalar parches

<details><summary>Ver respuesta</summary>

**Correcta: b) Buscar proactivamente amenazas no detectadas por las alertas.** Hipótesis + datos para hallar lo que las reglas no marcaron.

</details>

**4. Un exceso de falsos positivos en detección provoca…**

- a) Mejor seguridad siempre
- b) Fatiga de alertas y riesgo de ignorar lo importante
- c) Menos logs
- d) Más CPU en el atacante

<details><summary>Ver respuesta</summary>

**Correcta: b) Fatiga de alertas y riesgo de ignorar lo importante.** Hay que afinar reglas para no saturar al analista.

</details>

**5. El Event ID 1102 de Windows indica…**

- a) Inicio de sesión correcto
- b) Que se limpió el registro de auditoría (Security log)
- c) Actualización del sistema
- d) Cambio de contraseña

<details><summary>Ver respuesta</summary>

**Correcta: b) Que se limpió el registro de auditoría (Security log).** Es una señal fuerte de anti-forense: borrado del log de seguridad.

</details>

## Parte 9 — Forense digital y respuesta a incidentes

**1. Según el orden de volatilidad, ¿qué se adquiere primero?**

- a) El disco duro
- b) La memoria RAM y el estado volátil
- c) Los backups
- d) El CD-ROM

<details><summary>Ver respuesta</summary>

**Correcta: b) La memoria RAM y el estado volátil.** Lo más volátil (RAM, conexiones) se captura antes de apagar.

</details>

**2. La cadena de custodia garantiza…**

- a) Que la evidencia se pueda alterar
- b) La trazabilidad e integridad de la evidencia desde su recolección
- c) Mayor velocidad de análisis
- d) Cifrado del disco

<details><summary>Ver respuesta</summary>

**Correcta: b) La trazabilidad e integridad de la evidencia desde su recolección.** Documenta quién, cuándo y cómo manipuló la evidencia (validez legal).

</details>

**3. Volatility es una herramienta de…**

- a) Escaneo de red
- b) Análisis forense de memoria RAM
- c) Cracking de contraseñas
- d) Fuzzing

<details><summary>Ver respuesta</summary>

**Correcta: b) Análisis forense de memoria RAM.** Analiza volcados de memoria para procesos, conexiones, inyecciones, etc.

</details>

**4. El ciclo de respuesta a incidentes (NIST/SANS) incluye, entre otras, las fases de…**

- a) Compilación y linkeo
- b) Preparación, detección, contención, erradicación y recuperación
- c) Escaneo y explotación
- d) Diseño y despliegue

<details><summary>Ver respuesta</summary>

**Correcta: b) Preparación, detección, contención, erradicación y recuperación.** Es el flujo estándar de IR, más lecciones aprendidas.

</details>

**5. El 'timestomping' consiste en…**

- a) Sincronizar relojes
- b) Manipular las marcas de tiempo de archivos para despistar
- c) Acelerar el disco
- d) Cifrar timestamps

<details><summary>Ver respuesta</summary>

**Correcta: b) Manipular las marcas de tiempo de archivos para despistar.** Se detecta comparando $STANDARD_INFORMATION vs $FILE_NAME en NTFS.

</details>

## Parte 10 — Seguridad en la nube y contenedores

**1. El modelo de responsabilidad compartida dice que…**

- a) El proveedor es responsable de todo
- b) El cliente es responsable de todo
- c) El proveedor asegura la nube y el cliente la seguridad EN la nube
- d) Nadie es responsable

<details><summary>Ver respuesta</summary>

**Correcta: c) El proveedor asegura la nube y el cliente la seguridad EN la nube.** El reparto varía según IaaS/PaaS/SaaS, pero el cliente siempre configura su parte.

</details>

**2. Una causa muy común de brechas en la nube es…**

- a) Cifrado fuerte
- b) Configuraciones erróneas (p. ej. buckets públicos, IAM laxo)
- c) Usar MFA
- d) Rotar claves

<details><summary>Ver respuesta</summary>

**Correcta: b) Configuraciones erróneas (p. ej. buckets públicos, IAM laxo).** El misconfiguration domina los incidentes cloud.

</details>

**3. En Kubernetes, RBAC controla…**

- a) El ancho de banda
- b) Quién puede hacer qué sobre los recursos del clúster
- c) El cifrado de disco
- d) La CPU de los pods

<details><summary>Ver respuesta</summary>

**Correcta: b) Quién puede hacer qué sobre los recursos del clúster.** Role-Based Access Control define permisos por sujeto y recurso.

</details>

**4. Un 'container escape' es…**

- a) Reiniciar el contenedor
- b) Salir del aislamiento del contenedor hacia el host
- c) Borrar una imagen
- d) Exportar logs

<details><summary>Ver respuesta</summary>

**Correcta: b) Salir del aislamiento del contenedor hacia el host.** Abusa de configuraciones (privileged, mounts) para llegar al host.

</details>

**5. Para IAM en la nube, la buena práctica es…**

- a) Usar siempre la cuenta root
- b) Permisos amplios por comodidad
- c) Mínimo privilegio y roles temporales
- d) Claves compartidas por equipo

<details><summary>Ver respuesta</summary>

**Correcta: c) Mínimo privilegio y roles temporales.** Menos privilegio + credenciales efímeras reducen el impacto.

</details>

## Parte 11 — DevSecOps y seguridad del SDLC

**1. 'Shift-left' significa…**

- a) Mover la seguridad al final
- b) Integrar la seguridad temprano en el ciclo de desarrollo
- c) Eliminar las pruebas
- d) Desplegar sin revisar

<details><summary>Ver respuesta</summary>

**Correcta: b) Integrar la seguridad temprano en el ciclo de desarrollo.** Detectar y corregir antes = más barato y seguro.

</details>

**2. SAST vs DAST:**

- a) SAST prueba en ejecución; DAST lee el código
- b) SAST analiza el código fuente; DAST prueba la app en ejecución
- c) Son lo mismo
- d) Ambos requieren producción

<details><summary>Ver respuesta</summary>

**Correcta: b) SAST analiza el código fuente; DAST prueba la app en ejecución.** SAST = estático (código); DAST = dinámico (app corriendo).

</details>

**3. SCA (Software Composition Analysis) se enfoca en…**

- a) El estilo del código
- b) Vulnerabilidades en dependencias/terceros
- c) El diseño de la UI
- d) La velocidad de compilación

<details><summary>Ver respuesta</summary>

**Correcta: b) Vulnerabilidades en dependencias/terceros.** Clave contra ataques de cadena de suministro; complementa con SBOM.

</details>

**4. STRIDE es un método de…**

- a) Cifrado
- b) Modelado de amenazas
- c) Escaneo de puertos
- d) Gestión de logs

<details><summary>Ver respuesta</summary>

**Correcta: b) Modelado de amenazas.** Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation.

</details>

**5. Los secretos (API keys, contraseñas) en el código se deben…**

- a) Commitear al repo
- b) Gestionar en un vault/secret manager y escanear con pre-commit
- c) Poner en el README
- d) Enviar por chat

<details><summary>Ver respuesta</summary>

**Correcta: b) Gestionar en un vault/secret manager y escanear con pre-commit.** gitleaks/detect-secrets + gestores de secretos evitan filtraciones.

</details>

## Parte 12 — OSINT e ingeniería social

**1. OSINT es…**

- a) Hackear con exploits
- b) Inteligencia a partir de fuentes abiertas y públicas
- c) Un tipo de malware
- d) Un firewall

<details><summary>Ver respuesta</summary>

**Correcta: b) Inteligencia a partir de fuentes abiertas y públicas.** Open Source Intelligence: recolección y análisis de información pública.

</details>

**2. Shodan es útil para…**

- a) Editar fotos
- b) Buscar dispositivos y servicios expuestos en Internet
- c) Cifrar correos
- d) Compilar código

<details><summary>Ver respuesta</summary>

**Correcta: b) Buscar dispositivos y servicios expuestos en Internet.** Indexa banners de servicios expuestos (cámaras, ICS, servidores).

</details>

**3. El pretexting en ingeniería social es…**

- a) Un exploit de kernel
- b) Construir un escenario/identidad falsa creíble para manipular
- c) Un algoritmo de hash
- d) Un escaneo de red

<details><summary>Ver respuesta</summary>

**Correcta: b) Construir un escenario/identidad falsa creíble para manipular.** Base de vishing y muchos fraudes; explota la confianza.

</details>

**4. Los metadatos EXIF de una foto pueden revelar…**

- a) Nada relevante
- b) Coordenadas GPS, dispositivo y fecha
- c) La contraseña del autor
- d) El código fuente

<details><summary>Ver respuesta</summary>

**Correcta: b) Coordenadas GPS, dispositivo y fecha.** Antes de publicar conviene eliminarlos.

</details>

**5. La ingeniería social solo debe practicarse…**

- a) Contra cualquiera
- b) Con autorización explícita y por escrito (engagement)
- c) En redes sociales ajenas
- d) Sin límites

<details><summary>Ver respuesta</summary>

**Correcta: b) Con autorización explícita y por escrito (engagement).** Sin permiso es fraude/acoso; en pentest va acotada en las RoE.

</details>

## Parte 13 — Seguridad móvil, IoT e inalámbrica

**1. Un APK de Android se puede analizar estáticamente con…**

- a) Volatility
- b) apktool / jadx / MobSF
- c) Hashcat
- d) Snort

<details><summary>Ver respuesta</summary>

**Correcta: b) apktool / jadx / MobSF.** Descompilan y revisan el manifest, permisos y código.

</details>

**2. Un ataque 'Evil Twin' de WiFi consiste en…**

- a) Clonar una tarjeta SIM
- b) Levantar un punto de acceso falso que imita a uno legítimo
- c) Cifrar el router
- d) Bloquear el 5G

<details><summary>Ver respuesta</summary>

**Correcta: b) Levantar un punto de acceso falso que imita a uno legítimo.** La víctima se conecta al AP del atacante, que intercepta el tráfico.

</details>

**3. El análisis de firmware de un dispositivo IoT suele empezar por…**

- a) Pintar la carcasa
- b) Extraer y descomprimir la imagen del firmware para buscar binarios/credenciales
- c) Cambiar el color del LED
- d) Actualizar el reloj

<details><summary>Ver respuesta</summary>

**Correcta: b) Extraer y descomprimir la imagen del firmware para buscar binarios/credenciales.** binwalk y similares extraen sistemas de archivos y secretos embebidos.

</details>

**4. Interfaces de hardware como UART/JTAG sirven para…**

- a) Cargar el móvil
- b) Acceder a consola/depuración del dispositivo
- c) Conectar a WiFi
- d) Enviar SMS

<details><summary>Ver respuesta</summary>

**Correcta: b) Acceder a consola/depuración del dispositivo.** Dan acceso de bajo nivel muy útil para el hacking de hardware.

</details>

**5. BLE (Bluetooth Low Energy) es relevante en seguridad porque…**

- a) No existe
- b) Muchos dispositivos lo usan y puede tener emparejamiento/cifrado débil
- c) Solo lo usan impresoras
- d) Es imposible de interceptar

<details><summary>Ver respuesta</summary>

**Correcta: b) Muchos dispositivos lo usan y puede tener emparejamiento/cifrado débil.** Wearables/IoT lo usan; hay ataques de sniffing y suplantación.

</details>

## Parte 14 — GRC, riesgo y cumplimiento

**1. En términos simples, el riesgo se estima como…**

- a) Solo el impacto
- b) Probabilidad × impacto
- c) Número de servidores
- d) Cantidad de logs

<details><summary>Ver respuesta</summary>

**Correcta: b) Probabilidad × impacto.** Se prioriza combinando la probabilidad de ocurrencia y su impacto.

</details>

**2. ISO/IEC 27001 define…**

- a) Un lenguaje de programación
- b) Requisitos para un Sistema de Gestión de Seguridad de la Información (SGSI)
- c) Un antivirus
- d) Un protocolo de red

<details><summary>Ver respuesta</summary>

**Correcta: b) Requisitos para un Sistema de Gestión de Seguridad de la Información (SGSI).** Marco certificable de gestión de la seguridad basado en riesgos.

</details>

**3. GDPR regula principalmente…**

- a) El cifrado militar
- b) La protección de datos personales en la UE
- c) Los puertos TCP
- d) El diseño web

<details><summary>Ver respuesta</summary>

**Correcta: b) La protección de datos personales en la UE.** Derechos de los titulares y obligaciones de quien trata datos personales.

</details>

**4. Un plan de continuidad de negocio (BCP) busca…**

- a) Vender más
- b) Mantener/recuperar las operaciones críticas ante una disrupción
- c) Instalar juegos
- d) Cifrar correos

<details><summary>Ver respuesta</summary>

**Correcta: b) Mantener/recuperar las operaciones críticas ante una disrupción.** El DRP es su componente tecnológico de recuperación.

</details>

**5. Un control 'compensatorio' es…**

- a) Un control que elimina el activo
- b) Una medida alternativa cuando el control principal no es viable
- c) Un ataque
- d) Un tipo de malware

<details><summary>Ver respuesta</summary>

**Correcta: b) Una medida alternativa cuando el control principal no es viable.** Reduce el riesgo cuando no se puede aplicar el control ideal.

</details>

## Parte 15 — Seguridad de IA y machine learning

**1. La 'prompt injection' en una app con LLM consiste en…**

- a) Cifrar el prompt
- b) Introducir instrucciones que manipulan el comportamiento del modelo
- c) Acelerar la inferencia
- d) Entrenar más rápido

<details><summary>Ver respuesta</summary>

**Correcta: b) Introducir instrucciones que manipulan el comportamiento del modelo.** Es el riesgo #1 del OWASP Top 10 para LLM; incluye inyección indirecta.

</details>

**2. El envenenamiento de datos (data poisoning) ataca…**

- a) La GPU
- b) Los datos de entrenamiento para sesgar/backdoorear el modelo
- c) El firewall
- d) El DNS

<details><summary>Ver respuesta</summary>

**Correcta: b) Los datos de entrenamiento para sesgar/backdoorear el modelo.** Datos maliciosos en el entrenamiento comprometen el modelo resultante.

</details>

**3. Un ejemplo adversarial es…**

- a) Un dataset limpio
- b) Una entrada perturbada sutilmente para engañar al modelo
- c) Un modelo más grande
- d) Un optimizador

<details><summary>Ver respuesta</summary>

**Correcta: b) Una entrada perturbada sutilmente para engañar al modelo.** Pequeñas perturbaciones causan clasificaciones erróneas.

</details>

**4. OWASP mantiene un Top 10 específico para…**

- a) Impresoras
- b) Aplicaciones con LLM
- c) Routers
- d) Bases de datos

<details><summary>Ver respuesta</summary>

**Correcta: b) Aplicaciones con LLM.** Cataloga los riesgos típicos de apps que integran modelos de lenguaje.

</details>

**5. Al integrar un LLM con herramientas/agentes, un riesgo clave es…**

- a) Que responda rápido
- b) Que una inyección logre ejecutar acciones no deseadas
- c) Que use poca RAM
- d) Que hable español

<details><summary>Ver respuesta</summary>

**Correcta: b) Que una inyección logre ejecutar acciones no deseadas.** Hay que limitar permisos del agente y validar entradas/salidas.

</details>

## Parte 16 — Capstones y preparación de certificaciones

**1. La certificación OSCP es conocida por…**

- a) Ser 100% teórica
- b) Su examen práctico de 24h con mentalidad 'Try Harder'
- c) No tener examen
- d) Ser solo defensiva

<details><summary>Ver respuesta</summary>

**Correcta: b) Su examen práctico de 24h con mentalidad 'Try Harder'.** Evalúa explotación práctica en un laboratorio bajo tiempo.

</details>

**2. El CISSP se estructura en…**

- a) 3 laboratorios
- b) 8 dominios de conocimiento
- c) 1 examen práctico de pwn
- d) Solo criptografía

<details><summary>Ver respuesta</summary>

**Correcta: b) 8 dominios de conocimiento.** Cubre seguridad de forma amplia y gerencial (8 dominios).

</details>

**3. Un buen 'home lab' permanente sirve para…**

- a) Nada útil
- b) Practicar de forma continua y segura sin depender de terceros
- c) Solo ver películas
- d) Minar cripto

<details><summary>Ver respuesta</summary>

**Correcta: b) Practicar de forma continua y segura sin depender de terceros.** Es la base del aprendizaje continuo y del portafolio.

</details>

**4. Para construir portafolio, es recomendable…**

- a) Copiar writeups ajenos
- b) Documentar tus propios labs, CTFs y proyectos
- c) No mostrar nada
- d) Solo listar cursos

<details><summary>Ver respuesta</summary>

**Correcta: b) Documentar tus propios labs, CTFs y proyectos.** Evidencia práctica > lista de certificados sin contexto.

</details>

**5. En ciberseguridad, el aprendizaje…**

- a) Termina con una cert
- b) Es continuo: el panorama de amenazas cambia constantemente
- c) No es necesario
- d) Solo importa la teoría

<details><summary>Ver respuesta</summary>

**Correcta: b) Es continuo: el panorama de amenazas cambia constantemente.** Comunidad, práctica y actualización constante son parte del oficio.

</details>

## Parte 17 — Profundización para certificaciones

**1. En la clasificación de datos, ¿quién define el nivel de clasificación de un activo?**

- a) El custodio (custodian)
- b) El propietario del dato (data owner)
- c) Cualquier usuario
- d) El proveedor de nube

<details><summary>Ver respuesta</summary>

**Correcta: b) El propietario del dato (data owner).** El data owner clasifica y define requisitos; el custodio los implementa/mantiene.

</details>

**2. Según NIST SP 800-88, 'purge' frente a 'clear' implica…**

- a) Lo mismo
- b) Un borrado más resistente a ataques de laboratorio (p. ej. criptoborrado)
- c) Solo borrar la papelera
- d) Cifrar el disco

<details><summary>Ver respuesta</summary>

**Correcta: b) Un borrado más resistente a ataques de laboratorio (p. ej. criptoborrado).** Clear resiste ataques simples; purge resiste incluso recuperación de laboratorio; destroy es físico.

</details>

**3. En IAM, el patrón 'joiner-mover-leaver' se refiere a…**

- a) Un ataque de fuerza bruta
- b) El ciclo de vida de una identidad (alta, cambios, baja)
- c) Un tipo de MFA
- d) Un modelo de cifrado

<details><summary>Ver respuesta</summary>

**Correcta: b) El ciclo de vida de una identidad (alta, cambios, baja).** Gestiona aprovisionamiento, cambios de rol y desaprovisionamiento oportuno de accesos.

</details>

**4. SAML y OpenID Connect se usan para…**

- a) Cifrar discos
- b) Federación de identidad y single sign-on (SSO)
- c) Escanear puertos
- d) Analizar malware

<details><summary>Ver respuesta</summary>

**Correcta: b) Federación de identidad y single sign-on (SSO).** SAML (XML) y OIDC (sobre OAuth2) permiten autenticación federada entre dominios.

</details>

**5. El modelo Bell-LaPadula se enfoca en proteger la…**

- a) Integridad
- b) Disponibilidad
- c) Confidencialidad (no leer arriba, no escribir abajo)
- d) Velocidad

<details><summary>Ver respuesta</summary>

**Correcta: c) Confidencialidad (no leer arriba, no escribir abajo).** Bell-LaPadula = confidencialidad; Biba y Clark-Wilson se enfocan en integridad.

</details>

**6. Para priorizar la remediación de vulnerabilidades, además de CVSS conviene usar…**

- a) El orden alfabético
- b) EPSS y la lista KEV de CISA (explotación real)
- c) El tamaño del archivo
- d) El color del reporte

<details><summary>Ver respuesta</summary>

**Correcta: b) EPSS y la lista KEV de CISA (explotación real).** CVSS mide severidad; EPSS estima probabilidad de exploit y KEV marca lo explotado activamente.

</details>

**7. En el análisis de un correo de phishing, SPF, DKIM y DMARC sirven para…**

- a) Cifrar el cuerpo
- b) Autenticar el origen del correo y detectar suplantación
- c) Comprimir adjuntos
- d) Acelerar la entrega

<details><summary>Ver respuesta</summary>

**Correcta: b) Autenticar el origen del correo y detectar suplantación.** Validan que el remitente esté autorizado y que el mensaje no fue alterado; DMARC define la política.

</details>

## Parte 18 — IA aplicada a la ciberseguridad

**1. ¿Cuál es el mayor riesgo operativo al usar un LLM en seguridad?**

- a) Que sea lento
- b) Las alucinaciones (salidas falsas con aplomo) sin verificación
- c) Que use mucha RAM
- d) Que no tenga interfaz gráfica

<details><summary>Ver respuesta</summary>

**Correcta: b) Las alucinaciones (salidas falsas con aplomo) sin verificación.** Un LLM genera lo plausible, no lo cierto; hay que verificar toda salida.

</details>

**2. El Model Context Protocol (MCP) sirve para…**

- a) Cifrar prompts
- b) Estandarizar cómo un agente de IA usa herramientas externas
- c) Entrenar modelos
- d) Escanear puertos

<details><summary>Ver respuesta</summary>

**Correcta: b) Estandarizar cómo un agente de IA usa herramientas externas.** MCP conecta clientes de IA con servidores que exponen tools/resources/prompts.

</details>

**3. En kali-mcp, las herramientas de Kali se ejecutan…**

- a) En tu host directamente
- b) Dentro de un contenedor Docker aislado
- c) En la nube de OpenAI
- d) En el navegador

<details><summary>Ver respuesta</summary>

**Correcta: b) Dentro de un contenedor Docker aislado.** kali-mcp aísla las herramientas en un contenedor; el agente habla con un gateway MCP.

</details>

**4. En un pentest asistido por IA, ¿quién decide y autoriza las acciones con impacto?**

- a) El agente de IA de forma autónoma
- b) El humano (el agente propone, la persona aprueba)
- c) El servidor MCP
- d) Nadie, se automatiza todo

<details><summary>Ver respuesta</summary>

**Correcta: b) El humano (el agente propone, la persona aprueba).** Human-in-the-loop: la IA propone y acelera; la autorización y responsabilidad son humanas.

</details>

**5. La 'prompt injection' contra tu propio agente de seguridad consiste en…**

- a) Un ataque de fuerza bruta
- b) Contenido malicioso en los datos que el agente procesa que intenta secuestrar sus instrucciones
- c) Un fallo de red
- d) Un cifrado débil

<details><summary>Ver respuesta</summary>

**Correcta: b) Contenido malicioso en los datos que el agente procesa que intenta secuestrar sus instrucciones.** Datos no confiables (banners, webs) pueden manipular al agente; por eso mínimo privilegio y aislamiento.

</details>
