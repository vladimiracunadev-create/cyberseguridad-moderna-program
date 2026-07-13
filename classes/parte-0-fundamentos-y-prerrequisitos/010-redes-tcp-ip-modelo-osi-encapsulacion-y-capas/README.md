# Clase 010 — Redes TCP/IP: modelo OSI, encapsulación y capas

> Parte: **0 — Fundamentos y prerrequisitos** · Fuente: *W. Richard Stevens, TCP/IP Illustrated Vol. 1*
> ⏱️ Duración estimada: **100 min** · Nivel: **Fundamentos**

---

## 🎯 Objetivo

Entender cómo se comunican los sistemas en red mediante modelos de capas. Al terminar podrás explicar qué hace cada capa, cómo se encapsulan los datos al bajar por la pila y cómo se desencapsulan al subir, y traducir entre el modelo OSI de 7 capas y el modelo TCP/IP real.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Enumerar** las capas de los modelos OSI y TCP/IP y su función.
2. **Explicar** la encapsulación y las PDU de cada capa.
3. **Mapear** protocolos reales a su capa correspondiente.
4. **Relacionar** ataques concretos con la capa que afectan.
5. **Observar** la encapsulación real en una captura de red.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Modelo OSI (7 capas) | Marco de referencia universal |
| 2 | Modelo TCP/IP (4 capas) | El que se usa de verdad en Internet |
| 3 | Encapsulación | Cómo se envuelven los datos capa a capa |
| 4 | PDU por capa | Bits, tramas, paquetes, segmentos |
| 5 | Direccionamiento por capa | MAC, IP, puerto |
| 6 | Protocolos por capa | Ethernet, IP, TCP/UDP, HTTP... |
| 7 | Ataques por capa | Cada capa tiene su superficie |
| 8 | Herramientas de observación | Wireshark, tcpdump |

## 📖 Definiciones y características

- **Modelo OSI**: modelo conceptual de 7 capas (física, enlace, red, transporte, sesión, presentación, aplicación). Clave: referencia para razonar, no una implementación literal.
- **Modelo TCP/IP**: modelo práctico de 4 capas (acceso a red, Internet, transporte, aplicación). Clave: es el que gobierna Internet.
- **Encapsulación**: cada capa añade su cabecera al bajar por la pila. Clave: los datos de aplicación viajan envueltos en segmento → paquete → trama.
- **PDU (Protocol Data Unit)**: nombre del dato en cada capa (trama en enlace, paquete en red, segmento en transporte). Clave: precisa la terminología.
- **MTU**: tamaño máximo de la carga a nivel de enlace (típ. 1500 en Ethernet). Clave: excederla obliga a fragmentar.
- **Multiplexación por puerto**: la capa de transporte usa puertos para distinguir aplicaciones. Clave: permite muchas conexiones simultáneas por host.

## 🧰 Herramientas y preparación

Instala **Wireshark** en tu equipo o VM (<https://www.wireshark.org>) y ten `tcpdump` disponible en Kali. Practica sobre tu red de laboratorio o sobre tráfico propio. Un diagrama impreso de las capas OSI/TCP-IP junto a los protocolos ayuda mucho durante la clase.

## 🧪 Laboratorio guiado

1. **Dibuja el mapeo**. En una tabla, alinea las 7 capas OSI con las 4 de TCP/IP y coloca al menos un protocolo por capa.
2. **Captura tráfico** de una petición web sencilla. En Kali:

   ```bash
   sudo tcpdump -i eth0 -c 20 -w captura.pcap host <ip-victima>
   ```

   Genera tráfico con `curl http://<ip-victima>/`.
3. **Abre la captura en Wireshark** y selecciona un paquete HTTP.
4. **Observa la encapsulación**. En el panel de detalle verás las capas anidadas: Ethernet (enlace) → IP (red) → TCP (transporte) → HTTP (aplicación). Expande cada una.
5. **Identifica direcciones por capa**: la MAC en Ethernet, la IP en la capa de red y el puerto en TCP. Anota los tres para el mismo paquete.
6. **Relaciona PDU**: confirma que lo que Wireshark llama "frame" contiene el "packet" IP que contiene el "segment" TCP.
7. **Ataque por capa** (conceptual): junto a cada capa, escribe un ataque típico (ARP spoofing en enlace, IP spoofing en red, SYN flood en transporte, inyección en aplicación).

> ⚠️ **Nota ética**: captura únicamente tráfico de tu propio laboratorio o del que tengas permiso. Interceptar comunicaciones ajenas es ilegal.

## ✍️ Ejercicios

1. Ordena de menor a mayor nivel: TCP, Ethernet, HTTP, IP.
2. Explica qué cabecera añade cada capa a un mensaje "hola" que envía una app.
3. ¿En qué PDU y capa actúa un switch? ¿Y un router?
4. Da un ejemplo de ataque para cada una de las 4 capas TCP/IP.
5. Calcula cuánta sobrecarga (bytes de cabeceras) añaden Ethernet+IP+TCP a un payload.
6. Explica por qué el modelo OSI tiene capas (sesión, presentación) que TCP/IP no separa.

## 📝 Reto verificable

A partir de una captura propia, entrega un documento que "diseccione" un único paquete HTTP mostrando, capa por capa, la cabecera añadida y sus campos clave (MAC origen/destino, IP origen/destino, puertos, y la primera línea HTTP). Incluye una captura de pantalla del árbol de Wireshark.

**Criterio de aceptación**: el documento identifica correctamente las cuatro capas del paquete con al menos un campo relevante de cada una, y las direcciones (MAC, IP, puerto) coinciden con las de la captura mostrada. Verificable abriendo el `.pcap` adjunto.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Confundir OSI con TCP/IP | Son modelos distintos; TCP/IP colapsa varias capas OSI. Aprende el mapeo. |
| `tcpdump` no captura nada | Interfaz equivocada o sin permisos. Usa `sudo` y verifica la interfaz con `ip a`. |
| Ver tráfico cifrado ilegible | HTTPS oculta la capa de aplicación. Usa HTTP en el lab o descifra con claves propias. |
| Creer que un switch enruta por IP | Un switch opera en capa 2 (MAC); el router en capa 3 (IP). |
| Pensar que la encapsulación cambia los datos | Solo los envuelve con cabeceras; el payload original se preserva. |

## ❓ Preguntas frecuentes

**❓ ¿Aprendo OSI o TCP/IP?** Ambos: TCP/IP es el modelo real, pero OSI da el vocabulario que usa toda la industria ("un ataque de capa 7", "un balanceador L4").

**❓ ¿Por qué importa la encapsulación en seguridad?** Porque cada capa se puede inspeccionar, filtrar o falsificar. Firewalls, IDS y ataques operan en capas concretas; sin este modelo no se entienden.

**❓ ¿Las capas de sesión y presentación existen en la práctica?** Sus funciones (gestión de sesión, cifrado/codificación) existen, pero en TCP/IP se realizan dentro de la capa de aplicación o de protocolos como TLS.

**❓ ¿Wireshark o tcpdump?** tcpdump para capturar rápido en servidores sin GUI; Wireshark para analizar en profundidad con su árbol y filtros. Se complementan.

## 🔗 Referencias

- W. Richard Stevens, *TCP/IP Illustrated, Vol. 1*.
- Wireshark User's Guide — <https://www.wireshark.org/docs/>
- RFC 1122, *Requirements for Internet Hosts* — <https://www.rfc-editor.org/rfc/rfc1122>
- Cloudflare Learning: OSI model — <https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-010-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-010-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 011 - Protocolos de red: IP, TCP, UDP e ICMP en profundidad](../011-protocolos-de-red-ip-tcp-udp-e-icmp-en-profundidad/README.md)
