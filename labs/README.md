# 🧪 Laboratorios ejecutables

Entornos de práctica reproducibles para el **Programa de Ciberseguridad Moderna**.
Cada laboratorio se levanta con un comando (Docker) y está ligado a las clases que
lo usan. Aquí **practicas** lo que leíste en las clases.

> ⚠️ **Seguridad y ética.** Estos entornos son **deliberadamente vulnerables**.
> Nunca los expongas a Internet ni a una red compartida: todos escuchan solo en
> `127.0.0.1` (tu propia máquina) por diseño. Practica únicamente contra estos
> objetivos de laboratorio o contra sistemas para los que tengas **autorización
> explícita**. Atacar sistemas ajenos es delito (ver [Clase 025](../classes/parte-0-fundamentos-y-prerrequisitos/025-etica-legalidad-alcance-y-divulgacion-responsable/README.md)).

## Requisitos

- [Docker](https://docs.docker.com/get-docker/) y Docker Compose v2 (`docker compose version`).
- 4 GB de RAM libres recomendados.
- Opcional: [Burp Suite](https://portswigger.net/burp/communitydownload) o [OWASP ZAP](https://www.zaproxy.org/) para interceptar tráfico.

## Cómo usar un laboratorio

```bash
cd labs/<nombre-del-lab>
docker compose up -d        # levantar en segundo plano
# ... practicar ...
docker compose down         # apagar (borra los contenedores)
docker compose down -v      # apagar y borrar también los volúmenes/datos
```

## Catálogo

| Lab | Descripción | Clases relacionadas | Estado |
|---|---|---|---|
| [`appsec-web`](appsec-web/README.md) | OWASP Juice Shop + DVWA para practicar el OWASP Top 10 (SQLi, XSS, CSRF, IDOR…) | Parte 4 (086–115) | ✅ Disponible |
| _(próximamente)_ `blue-team-soc` | Wazuh + generación de telemetría para detección | Parte 8 (181–200) | ⏳ Planificado |
| _(próximamente)_ `red-team-ad` | Laboratorio de Active Directory vulnerable | Parte 7 (161–180) | ⏳ Planificado |
| _(próximamente)_ `cripto` | Retos de criptografía aplicada | Parte 2 (046–065) | ⏳ Planificado |

## Convención de cada laboratorio

Cada carpeta `labs/<lab>/` contiene:

- `docker-compose.yml` — el entorno, con puertos atados a `127.0.0.1` y red aislada.
- `README.md` — objetivo, cómo levantarlo, **recorrido guiado** paso a paso ligado a las clases, retos con criterio de aceptación y cómo apagarlo.
