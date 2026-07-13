# Lab: Blue Team / SOC — detección y threat hunting

Entorno de práctica para la **Parte 8 — Blue Team, detección y SOC** (clases 181–200).
Levanta un mini-SIEM (Elasticsearch + Kibana), carga un conjunto de eventos de
autenticación que **contiene un ataque real de fuerza bruta con éxito y movimiento
lateral**, y practica cazarlo y escribir la detección.

> ⚠️ **Solo laboratorio local.** El stack corre sin autenticación a propósito para
> simplificar; escucha únicamente en `127.0.0.1`. No lo uses así en producción.

## 🎯 Qué vas a practicar

| Objetivo | Clases |
|---|---|
| Ingesta y exploración de telemetría | [182](../../classes/parte-8-blue-team-deteccion-y-soc/182-logging-y-fuentes-de-telemetria/README.md), [183](../../classes/parte-8-blue-team-deteccion-y-soc/183-siem-arquitectura-y-componentes/README.md) |
| Threat hunting de fuerza bruta | [188](../../classes/parte-8-blue-team-deteccion-y-soc/188-threat-hunting-metodologia/README.md) |
| Detección de movimiento lateral | [192](../../classes/parte-8-blue-team-deteccion-y-soc/192-deteccion-de-movimiento-lateral/README.md) |
| Escribir una regla (Sigma / consulta) | [186](../../classes/parte-8-blue-team-deteccion-y-soc/186-escritura-de-reglas-de-deteccion-con-sigma/README.md), [199](../../classes/parte-8-blue-team-deteccion-y-soc/199-ingenieria-de-deteccion-como-disciplina/README.md) |

## 🚀 Levantar el laboratorio

```bash
# Requisito (una vez) en Linux/WSL para que Elasticsearch arranque:
sudo sysctl -w vm.max_map_count=262144

cd labs/blue-team-soc
docker compose up -d
docker compose ps                 # espera a que elasticsearch esté "healthy"
./cargar_datos.sh                 # carga los eventos de muestra
```

- **Kibana** → <http://127.0.0.1:5601> · **Elasticsearch** → <http://127.0.0.1:9200>
- En Kibana: **Discover** → crea un *data view* sobre el índice `eventos-auth` (campo de tiempo `@timestamp`). Ajusta el rango de fechas a **marzo de 2026**.

## 🧭 Recorrido guiado

### 1. Explora los datos

Cada documento es un intento de autenticación SSH con campos `source.ip`, `user.name`,
`event.action` (`login_success` / `login_failed`), `host.name` y `source.geo.country_iso_code`.
Empieza por ver el volumen por acción y por IP.

### 2. Caza la fuerza bruta

Filtra los fallos de login y agrúpalos por IP de origen. En la consola de Elasticsearch
(o Kibana → Dev Tools) puedes correr:

```json
GET eventos-auth/_search
{
  "size": 0,
  "query": { "term": { "event.action": "login_failed" } },
  "aggs": {
    "por_ip": { "terms": { "field": "source.ip.keyword", "size": 5 },
      "aggs": { "usuarios": { "cardinality": { "field": "user.name.keyword" } } } }
  }
}
```

Verás una IP (`203.0.113.66`, geolocalizada fuera de lo normal) con **muchos fallos**
contra varios usuarios: patrón de *password spraying* / fuerza bruta.

### 3. ¿Tuvo éxito?

Busca un `login_success` desde **esa misma IP** justo después de la ráfaga de fallos.
Ese es el compromiso. Anota la hora y el usuario (`root`).

### 4. Sigue el movimiento lateral

Tras el compromiso de `srv-db01`, busca un `login_success` hacia **otro host**
(`srv-app01`) originado desde la red interna en los minutos siguientes: el atacante
pivotó. Relaciónalo con la [Clase 192](../../classes/parte-8-blue-team-deteccion-y-soc/192-deteccion-de-movimiento-lateral/README.md).

## 🏆 Retos verificables

1. **Identifica al atacante:** entrega la IP, el usuario comprometido y la marca de tiempo del `login_success` malicioso. *Aceptación:* coinciden con la ráfaga de fallos previa desde la misma IP.
2. **Regla de detección:** escribe una regla (en formato Sigma o como consulta de Elasticsearch) que dispare ante **≥ 10 `login_failed` de una misma IP en 5 minutos**. *Aceptación:* la regla marca a `203.0.113.66` y no a las IPs internas normales.
3. **Umbral + geo:** mejora la regla para elevar la severidad si la IP está fuera de `CL`. *Aceptación:* razonas por qué reduce falsos positivos y qué falsos negativos introduce.
4. **Cadena completa:** dibuja la línea de tiempo fuerza bruta → acceso → movimiento lateral citando las horas de cada evento.

## 🧯 Apagar y limpiar

```bash
docker compose down          # detiene y elimina los contenedores
docker compose down -v       # además borra los índices/datos
```

## 🛠️ Problemas comunes

| Síntoma | Causa y solución |
|---|---|
| Elasticsearch se reinicia en bucle | Falta `vm.max_map_count`. Ejecuta `sudo sysctl -w vm.max_map_count=262144`. |
| `curl: connection refused` al cargar datos | El contenedor aún arranca; espera a `healthy` (`docker compose ps`) y reintenta. |
| Kibana no muestra datos | No creaste el *data view* sobre `eventos-auth` o el rango de fechas no cubre marzo 2026. |
| Poca RAM / OOM | Baja `ES_JAVA_OPTS` a `-Xms512m -Xmx512m` en el `docker-compose.yml`. |

## 🔗 Referencias

- [Elastic — Getting started](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html)
- [Sigma — reglas de detección genéricas](https://github.com/SigmaHQ/sigma)
- [MITRE ATT&CK — Brute Force (T1110)](https://attack.mitre.org/techniques/T1110/) · [Lateral Movement (TA0008)](https://attack.mitre.org/tactics/TA0008/)
- Parte 8 del programa — [índice de clases](../../classes/README.md)
