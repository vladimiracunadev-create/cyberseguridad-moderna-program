# Clase 027 — Análisis de tráfico: filtros, seguimiento de flujos y estadísticas

> Parte: **1 — Redes y seguridad de redes** · Fuente: *Practical Packet Analysis, C. Sanders*
> ⏱️ Duración estimada: **120 min** · Nivel: **Fundamentos**

---

## 🎯 Objetivo

Dominar el lenguaje de **filtros de visualización** de Wireshark, el seguimiento de flujos (Follow Stream) y las herramientas estadísticas para pasar de miles de paquetes a una respuesta en segundos. El alumno aprenderá a formular preguntas precisas sobre una captura y a responderlas con expresiones y vistas agregadas.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Construir** filtros de visualización complejos con operadores lógicos y de comparación.
2. **Seguir** un flujo TCP/UDP/HTTP y leer el diálogo cliente-servidor reconstruido.
3. **Cuantificar** conversaciones y endpoints con las tablas de estadísticas.
4. **Detectar** anomalías con Expert Information y el gráfico de I/O.
5. **Medir** latencia y round-trip time a partir de las marcas de tiempo.
6. **Automatizar** filtros equivalentes en `tshark` para procesamiento por lotes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Sintaxis de filtros de visualización | Es el bisturí del análisis |
| 2 | Operadores y campos de protocolo | Precisión al aislar tráfico |
| 3 | Follow TCP/UDP/HTTP/TLS Stream | Ver la conversación completa |
| 4 | Estadísticas: Conversations y Endpoints | Quién habla y cuánto |
| 5 | Jerarquía de protocolos | Composición del tráfico |
| 6 | Expert Information | Retransmisiones, dup ACK, resets |
| 7 | I/O Graph y RTT | Rendimiento y latencia |
| 8 | `tshark` para filtros por lote | Escalar el análisis |

## 📖 Definiciones y características

- **Filtro de visualización:** expresión booleana sobre campos disecados (`ip.addr == 10.0.0.5 && tcp.port == 443`). No altera la captura, solo la vista.
- **Flujo (stream):** conjunto de paquetes de una misma conversación identificada por `tcp.stream` o `udp.stream`. Follow Stream reensambla su carga útil.
- **Conversación:** par de endpoints que intercambian paquetes; la tabla suma bytes, paquetes y duración.
- **Retransmisión:** reenvío de un segmento TCP no confirmado; señal de pérdida o congestión.
- **Duplicate ACK:** ACKs repetidos que indican huecos en la secuencia; preludio de retransmisión rápida.
- **RTT (Round-Trip Time):** tiempo entre un segmento y su ACK; base para medir latencia.

## 🧰 Herramientas y preparación

- **Wireshark 4.x** y su binario de consola **`tshark`**.
- Una captura de práctica con varios flujos. Puedes generar una así en tu laboratorio:
  ```bash
  sudo tcpdump -i eth0 -w /tmp/lab027.pcapng &
  curl http://192.168.56.101/ ; dig @192.168.56.1 example.com ; ping -c3 192.168.56.1
  sudo pkill tcpdump
  ```
- Referencia de campos: <https://www.wireshark.org/docs/dfref/>.

## 🧪 Laboratorio guiado

1. Abre `lab027.pcapng`. Aplica el filtro `dns` y observa consultas y respuestas.
2. Filtra por método HTTP: `http.request.method == "GET"`.
3. Combina condiciones: `ip.addr == 192.168.56.101 && tcp.flags.syn == 1 && tcp.flags.ack == 0` para ver intentos de conexión salientes.
4. Sobre un paquete HTTP, clic derecho → **Follow → HTTP Stream**. Lee petición y respuesta reensambladas (cliente en rojo, servidor en azul).
5. Cambia a **Follow → TCP Stream** del mismo flujo para ver bytes crudos y el `tcp.stream` asociado.
6. Abre **Estadísticas → Conversaciones**. Ordena por bytes; marca "Limit to display filter" para acotar.
7. Abre **Estadísticas → Jerarquía de protocolos** y anota el porcentaje de cada protocolo.
8. Abre **Analizar → Expert Information**: identifica retransmisiones (`tcp.analysis.retransmission`) y dup ACKs.
9. Abre **Estadísticas → I/O Graph**; añade una serie con filtro `tcp.analysis.retransmission` para visualizar picos de pérdida.
10. Repite un filtro en consola:
    ```bash
    tshark -r /tmp/lab027.pcapng -Y 'http.request' -T fields -e ip.src -e http.host -e http.request.uri
    ```

## ✍️ Ejercicios

1. Escribe un filtro que muestre solo tráfico TLS handshake (`tls.handshake.type == 1`).
2. Encuentra todas las conversaciones que superen 100 KB y anótalas.
3. Usa `tcp.analysis.flags` para listar todos los eventos de análisis de la captura.
4. Con Follow HTTP Stream, extrae el `Server:` de la respuesta de un sitio.
5. Calcula el RTT medio de un flujo añadiendo la columna `tcp.analysis.ack_rtt`.
6. Reproduce la tabla de Endpoints en consola: `tshark -r lab027.pcapng -q -z endpoints,ip`.

## 📝 Reto verificable

Dada una captura con al menos 5 conversaciones, entrega un informe corto (media página) que identifique: la conversación con más bytes, el número de retransmisiones totales, el protocolo de aplicación dominante y una captura de pantalla del I/O Graph. Adjunta también el comando `tshark` que usaste para verificar el conteo de retransmisiones.

**Criterio de aceptación:** los números del informe coinciden con los que el revisor obtiene al aplicar `tcp.analysis.retransmission` y abrir la tabla de Conversaciones sobre la misma captura.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Campo del filtro en rojo | Sintaxis o nombre de campo inválido; consulta el Display Filter Reference |
| Follow Stream muestra basura | Es tráfico cifrado (TLS); necesitas las claves de sesión para descifrar |
| Muchas "retransmisiones" falsas | Capturaste en el emisor con offloading; puede ser reordenamiento, no pérdida real |
| Estadísticas vacías | Tienes un filtro de visualización que no aplicaste o "Limit to display filter" activo sin coincidencias |
| `tshark` no encuentra campos | Nombre de campo mal escrito; usa `tshark -G fields \| grep <nombre>` |

## ❓ Preguntas frecuentes

**❓ ¿`ip.addr == x` o `ip.src == x`?**
`ip.addr` coincide si x es origen **o** destino; `ip.src`/`ip.dst` fijan la dirección. Ojo con la negación: usa `!(ip.addr == x)` en lugar de `ip.addr != x`.

**❓ ¿Puedo descifrar TLS en Follow Stream?**
Sí, si dispones del archivo de claves (variable `SSLKEYLOGFILE` en el cliente) o de la clave privada RSA sin PFS. Se configura en Preferencias → Protocols → TLS.

**❓ ¿Qué diferencia hay entre Conversations y Endpoints?**
Conversations agrupa por pares (A↔B); Endpoints agrupa por host individual con su total de tráfico.

**❓ ¿Cómo cuento paquetes que cumplen un filtro sin abrir la GUI?**
`tshark -r archivo.pcapng -Y 'filtro' \| wc -l`, o mejor `-q -z io,stat,0,'COUNT(frame)filtro'`.

## 🔗 Referencias

- Sanders, C. *Practical Packet Analysis*, 3rd ed., cap. 5–6. No Starch Press.
- Wireshark Display Filter Reference. <https://www.wireshark.org/docs/dfref/>
- tshark man page. <https://www.wireshark.org/docs/man-pages/tshark.html>
- Wireshark Statistics docs. <https://www.wireshark.org/docs/wsug_html_chunked/ChStatistics.html>

## ➡️ Siguiente clase

[Clase 028 - tcpdump y captura de trafico en linea de comandos](../028-tcpdump-y-captura-de-trafico-en-linea-de-comandos/README.md)
