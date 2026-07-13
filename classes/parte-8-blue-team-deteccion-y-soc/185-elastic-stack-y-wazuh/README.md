# Clase 185 — Elastic Stack y Wazuh

> Parte: **8 — Blue Team, detección y SOC** · Fuente: *Applied Network Security Monitoring* — Chris Sanders y Jason Smith
> ⏱️ Duración estimada: **120 min** · Nivel: **Intermedio**

---

## 🎯 Objetivo

Desplegar y operar un SIEM open source con Elastic Stack (Elasticsearch, Kibana, Beats) y Wazuh. Aprenderás a ingerir telemetría, escribir consultas KQL/EQL, y usar las reglas y el motor de detección de Wazuh como alternativa gratuita a soluciones comerciales, ideal para laboratorios y organizaciones con presupuesto limitado.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Desplegar** Elastic Stack y Wazuh en contenedores de forma reproducible.
2. **Ingerir** logs de endpoint y red con Beats y el agente Wazuh.
3. **Consultar** datos con KQL y detección de secuencias con EQL.
4. **Interpretar** las reglas y decoders de Wazuh y su mapeo a MITRE ATT&CK.
5. **Construir** un dashboard de detección en Kibana.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Arquitectura Elastic (ES, Kibana, Beats) | Entender el flujo de datos |
| 2 | ECS: esquema común | Normalización para detección portable |
| 3 | KQL y EQL | Consultas y correlación de secuencias |
| 4 | Elastic Detection Rules | Detecciones listas mapeadas a ATT&CK |
| 5 | Wazuh: manager, indexer, agente | SIEM+HIDS integrado y gratuito |
| 6 | Reglas y decoders de Wazuh | Cómo se generan las alertas |
| 7 | FIM y detección de rootkits | Capacidades de HIDS de Wazuh |
| 8 | Dashboards en Kibana | Visualización operativa |

## 📖 Definiciones y características

- **Elasticsearch:** motor de búsqueda e indexación distribuido. Característica: búsquedas rápidas sobre grandes volúmenes vía índices invertidos.
- **Kibana:** interfaz de visualización y análisis. Característica: dashboards, Discover y el motor de detección de Elastic Security.
- **Beats:** agentes ligeros (Winlogbeat, Filebeat, Packetbeat). Característica: cada uno especializado en un tipo de dato.
- **KQL (Kibana Query Language):** lenguaje de filtrado interactivo. Característica: simple, ideal para exploración.
- **EQL (Event Query Language):** consulta secuencias de eventos ordenados. Característica: perfecto para detectar cadenas de ataque (proceso→red→persistencia).
- **Wazuh:** plataforma open source que combina HIDS, SIEM y gestión de cumplimiento. Característica: motor de reglas con niveles de severidad y mapeo ATT&CK.
- **Decoder (Wazuh):** extrae campos de un log crudo antes de evaluarlo contra reglas. Característica: paso previo a la correlación.

## 🧰 Herramientas y preparación

En laboratorio aislado:

- **Elastic Stack** vía Docker (`docker-compose` oficial de Elastic) o la instalación de Elastic Security.
- **Winlogbeat/Filebeat/Packetbeat** en tus máquinas de prueba.
- **Wazuh** con su despliegue Docker de un solo nodo (manager + indexer + dashboard).
- **Agente Wazuh** instalado en el Windows y el Linux de laboratorio.

Todo dentro de tu red de pruebas; el FIM y la detección se prueban con cambios que tú mismo provocas.

## 🧪 Laboratorio guiado — Doble stack de detección

1. **Levanta Elastic.** `docker compose up -d` con el stack oficial. Accede a Kibana y crea el usuario de kibana.
2. **Ingesta endpoint.** Instala Winlogbeat con el módulo `sysmon` y verifica en *Discover* que llegan eventos ECS (`process.command_line`).
3. **Consulta con KQL.** En Discover: `event.code:1 and process.parent.name:"WINWORD.EXE" and process.name:("powershell.exe" or "cmd.exe")`.
4. **Detecta secuencias con EQL.** En Elastic Security escribe una regla EQL:
   `sequence by host.id [process where process.name=="powershell.exe"] [network where destination.port==443]`
5. **Levanta Wazuh.** Despliega el stack Docker de Wazuh; instala el agente en tus máquinas y confírmalo en el dashboard.
6. **Provoca una alerta.** Modifica un archivo monitoreado por FIM (`/etc/passwd` o una carpeta bajo vigilancia) y observa la alerta con su nivel y regla.
7. **Revisa el mapeo ATT&CK.** En Wazuh, abre una alerta y localiza la técnica ATT&CK asociada; en Elastic, activa reglas prebuilt y filtra por táctica.
8. **Dashboard.** Crea en Kibana un dashboard con: top procesos, alertas por severidad y logins fallidos por host.

## ✍️ Ejercicios

1. Escribe 3 consultas KQL para hunting de PowerShell ofuscado.
2. Traduce una detección de la clase 184 (Splunk SPL) a EQL de Elastic.
3. Explica la diferencia entre un decoder y una regla en Wazuh con un ejemplo.
4. Habilita FIM sobre una carpeta y documenta la alerta generada.
5. Compara Elastic vs Wazuh vs Splunk en coste, curva de aprendizaje y capacidades.
6. Crea una regla local de Wazuh que eleve la severidad de un patrón concreto.

## 📝 Reto verificable

Despliega ambos stacks y demuestra una detección en cada uno: una regla EQL en Elastic que capture una secuencia proceso→red, y una alerta de Wazuh (FIM o regla) con su técnica ATT&CK. **Criterio de aceptación:** ambas alertas se disparan con tu actividad simulada y puedes mostrar en Kibana/Wazuh el evento, la regla que lo detectó y la técnica ATT&CK asociada.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Kibana no arranca / `max_map_count` | Falta `vm.max_map_count=262144`; ajústalo en el host |
| Beats no envía datos | Certificados/usuario mal configurados; revisa `output.elasticsearch` |
| EQL no encuentra secuencias | Falta `by` field común o datos sin ECS; normaliza primero |
| Agente Wazuh "Never connected" | Puerto 1514/1515 bloqueado o clave no registrada; re-registra el agente |
| Índice rojo en ES | Disco lleno o shards sin asignar; libera espacio o ajusta réplicas |

## ❓ Preguntas frecuentes

**❓ ¿Elastic o Wazuh para empezar?**
Wazuh trae reglas, agente y mapeo ATT&CK listos, ideal para arrancar rápido. Elastic da más flexibilidad de consulta (EQL) y un ecosistema de detección amplio. En laboratorio, prueba ambos.

**❓ ¿Wazuh usa Elasticsearch?**
Las versiones recientes incluyen su propio Wazuh Indexer (fork de OpenSearch/Elasticsearch), así que funciona de forma autónoma sin depender de Elastic.

**❓ ¿EQL sustituye a las reglas Sigma?**
No. Sigma es un formato portable de reglas (clase 186) que puedes convertir a EQL, KQL o SPL. EQL es el lenguaje nativo de Elastic al que Sigma se traduce.

## 🔗 Referencias

- Elastic Security docs — <https://www.elastic.co/guide/en/security/current/index.html>
- EQL syntax reference — <https://www.elastic.co/guide/en/elasticsearch/reference/current/eql.html>
- Wazuh Documentation — <https://documentation.wazuh.com/>
- Elastic Common Schema (ECS) — <https://www.elastic.co/guide/en/ecs/current/index.html>
- Sanders, C. y Smith, J. *Applied Network Security Monitoring*. Syngress.

## ➡️ Siguiente clase

[Clase 186 - Escritura de reglas de deteccion con Sigma](../186-escritura-de-reglas-de-deteccion-con-sigma/README.md)
