# Lab: AppSec Web — OWASP Juice Shop + DVWA

Entorno de práctica para la **Parte 4 — Seguridad de aplicaciones web** (clases 086–115).
Levanta dos aplicaciones deliberadamente vulnerables para practicar el OWASP Top 10 con
herramientas reales (navegador + Burp/ZAP).

> ⚠️ **Solo laboratorio local.** Ambas apps son inseguras a propósito. Escuchan únicamente
> en `127.0.0.1`. No las expongas a ninguna red ni las uses como plantilla de producción.
> Practica solo aquí o en sistemas con autorización explícita.

## 🎯 Qué vas a practicar

| Objetivo | App | Clases |
|---|---|---|
| Reconocimiento y mapeo de la app | Ambas | [090](../../classes/parte-4-seguridad-de-aplicaciones-web/090-mapeo-spidering-y-descubrimiento-de-contenido/README.md) |
| Inyección SQL (login bypass, extracción) | DVWA / Juice Shop | [091](../../classes/parte-4-seguridad-de-aplicaciones-web/091-inyeccion-sql-fundamentos/README.md), [092](../../classes/parte-4-seguridad-de-aplicaciones-web/092-inyeccion-sql-avanzada-y-ciega-blind/README.md) |
| XSS reflejado / almacenado / DOM | DVWA / Juice Shop | [096](../../classes/parte-4-seguridad-de-aplicaciones-web/096-cross-site-scripting-xss-reflejado/README.md), [097](../../classes/parte-4-seguridad-de-aplicaciones-web/097-xss-almacenado-y-basado-en-dom/README.md) |
| Control de acceso roto (IDOR) | Juice Shop | [105](../../classes/parte-4-seguridad-de-aplicaciones-web/105-control-de-acceso-roto-idor-y-path-traversal/README.md) |
| Command injection | DVWA | [095](../../classes/parte-4-seguridad-de-aplicaciones-web/095-inyeccion-de-comandos-del-sistema-operativo/README.md) |
| Uso de Burp Suite | Ambas | [088](../../classes/parte-4-seguridad-de-aplicaciones-web/088-burp-suite-configuracion-y-flujo-de-trabajo/README.md) |

## 🚀 Levantar el laboratorio

```bash
cd labs/appsec-web
docker compose up -d
docker compose ps          # verifica que ambos estén "running"
```

Luego abre en el navegador:

- **OWASP Juice Shop** → <http://127.0.0.1:3000>
- **DVWA** → <http://127.0.0.1:8080>

### Configuración inicial de DVWA (una sola vez)

1. Entra a <http://127.0.0.1:8080>; te redirige a `setup.php`.
2. Pulsa **Create / Reset Database**.
3. Inicia sesión con el usuario por defecto **`admin`** / **`password`** (credenciales del propio lab).
4. Ve a **DVWA Security** y pon el nivel en **Low** para empezar; súbelo a *Medium*/*High* conforme avances.

Juice Shop no requiere configuración: arranca listo.

## 🧭 Recorrido guiado

> Ten [Burp Suite](../../classes/parte-4-seguridad-de-aplicaciones-web/088-burp-suite-configuracion-y-flujo-de-trabajo/README.md) o ZAP interceptando el tráfico para ver y modificar las peticiones.

### 1. Inyección SQL — bypass de login (DVWA, nivel Low)

En DVWA → **SQL Injection**, prueba en el campo de ID el clásico payload de tautología:

```text
1' OR '1'='1
```

Observa cómo la consulta devuelve todos los registros. Repasa el *por qué* en la
[Clase 091](../../classes/parte-4-seguridad-de-aplicaciones-web/091-inyeccion-sql-fundamentos/README.md)
y luego sube DVWA a **Medium** para ver cómo cambia (y por qué las consultas
parametrizadas lo eliminan).

### 2. XSS reflejado y almacenado (DVWA / Juice Shop)

En DVWA → **XSS (Reflected)**, introduce en el campo de nombre:

```html
<script>alert(document.domain)</script>
```

En Juice Shop, busca el campo de búsqueda y prueba XSS basado en DOM. Contrasta reflejado vs
almacenado con la [Clase 097](../../classes/parte-4-seguridad-de-aplicaciones-web/097-xss-almacenado-y-basado-en-dom/README.md).

### 3. Command injection (DVWA)

En DVWA → **Command Injection**, en el campo de IP prueba a encadenar un comando:

```text
127.0.0.1; whoami
```

Relaciónalo con la [Clase 095](../../classes/parte-4-seguridad-de-aplicaciones-web/095-inyeccion-de-comandos-del-sistema-operativo/README.md)
y prueba los separadores alternativos cuando subas el nivel de seguridad.

### 4. Control de acceso roto — IDOR (Juice Shop)

Inicia sesión, abre tu cesta y observa el identificador en la petición (`/rest/basket/<id>`).
Cámbialo con Burp para intentar ver la cesta de otro usuario. Repasa la
[Clase 105](../../classes/parte-4-seguridad-de-aplicaciones-web/105-control-de-acceso-roto-idor-y-path-traversal/README.md).

## 🏆 Retos verificables

1. **Login bypass:** entra a DVWA SQL Injection y extrae los hashes de contraseñas de la tabla de usuarios. *Aceptación:* obtienes al menos un hash y explicas la consulta inyectada.
2. **XSS persistente:** logra que un `alert()` se ejecute para cualquier visitante de una página (no solo para ti). *Aceptación:* el payload sobrevive a recargar la página desde otra sesión.
3. **Juice Shop scoreboard:** encuentra el panel de puntuación oculto y resuelve al menos **3 retos** de dificultad ⭐. *Aceptación:* aparecen resueltos en el *Score Board*.
4. **Defensa:** por cada vulnerabilidad anterior, escribe la corrección (consulta parametrizada, codificación de salida, control de acceso del lado servidor) citando la clase correspondiente.

## 🧯 Apagar y limpiar

```bash
docker compose down          # detiene y elimina los contenedores
docker compose down -v       # además borra volúmenes/datos del lab
```

## 🛠️ Problemas comunes

| Síntoma | Causa y solución |
|---|---|
| `port is already allocated` | Otro servicio usa el 3000/8080. Cambia el mapeo host en `docker-compose.yml` (p. ej. `127.0.0.1:3001:3000`). |
| DVWA muestra error de base de datos | No pulsaste **Create / Reset Database** en `setup.php`. Hazlo una vez. |
| Juice Shop tarda en responder | El contenedor aún arranca; espera a que el `healthcheck` pase (`docker compose ps`). |
| No veo el tráfico en Burp | El navegador no está usando el proxy (127.0.0.1:8080 de Burp) o falta el certificado CA de Burp. Revisa la [Clase 088](../../classes/parte-4-seguridad-de-aplicaciones-web/088-burp-suite-configuracion-y-flujo-de-trabajo/README.md). |

## 🔗 Referencias

- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) · [DVWA](https://github.com/digininja/DVWA)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- Parte 4 del programa — [índice de clases](../../classes/README.md)
