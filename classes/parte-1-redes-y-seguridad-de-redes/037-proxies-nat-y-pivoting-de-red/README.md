# Clase 037 — Proxies, NAT y pivoting de red

> Parte: **1 — Redes y seguridad de redes** · Fuente: *The Hacker Playbook; documentación de OpenSSH, proxychains, Chisel*
> ⏱️ Duración estimada: **130 min** · Nivel: **Avanzado**

---

## 🎯 Objetivo

Entender NAT y proxies como piezas de red, y aprender la técnica ofensiva/defensiva del **pivoting**: usar un host comprometido como trampolín para alcanzar redes internas no accesibles directamente. El alumno practicará túneles SSH, reenvío de puertos, SOCKS y herramientas de pivoting en un laboratorio controlado.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Explicar** SNAT/DNAT/PAT y el papel del NAT en la conectividad.
2. **Diferenciar** proxy directo, inverso y SOCKS.
3. **Crear** túneles SSH: local (`-L`), remoto (`-R`) y dinámico (`-D`).
4. **Encadenar** herramientas a través de un proxy con proxychains.
5. **Pivotar** hacia una segunda red usando un host intermedio.
6. **Detectar** y mitigar pivoting desde el lado defensivo.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | NAT: SNAT, DNAT, PAT | Cómo se traduce el direccionamiento |
| 2 | Tipos de proxy | Control y ocultación del tráfico |
| 3 | Port forwarding SSH local/remoto | Acceso a servicios no expuestos |
| 4 | SSH dynamic (SOCKS) | Túnel genérico para múltiples destinos |
| 5 | proxychains | Enrutar herramientas por el túnel |
| 6 | Pivoting multi-salto | Alcanzar redes segmentadas |
| 7 | Detección defensiva del pivoting | Cerrar el vector |

## 📖 Definiciones y características

- **NAT (Network Address Translation):** traduce direcciones entre redes; PAT (overload) multiplexa muchos hosts internos tras una IP pública usando puertos.
- **Proxy directo (forward):** intermedia las peticiones salientes de clientes hacia Internet; puede filtrar y registrar.
- **Proxy inverso (reverse):** se coloca delante de servidores y distribuye/oculta el backend.
- **Proxy SOCKS:** proxy de nivel de sesión, agnóstico al protocolo de aplicación; ideal para túneles genéricos (SOCKS5).
- **Pivoting:** técnica de usar un host ya controlado como punto de apoyo para acceder a segmentos de red que no son alcanzables directamente desde el atacante.
- **Túnel SSH dinámico (`-D`):** abre un proxy SOCKS local que reenvía por SSH cualquier conexión al otro extremo.

## 🧰 Herramientas y preparación

- **OpenSSH** (cliente y servidor).
- **proxychains-ng**: `sudo apt install proxychains4`.
- **Chisel** (túneles sobre HTTP/WebSocket) y **socat** para casos sin SSH.
- Laboratorio: atacante → host pivote (con dos interfaces) → red interna con una víctima solo alcanzable desde el pivote.

> ⚠️ **Nota ética:** el pivoting es una técnica ofensiva de post-explotación. Practícalo **exclusivamente** en tu laboratorio o en un compromiso con autorización explícita y alcance definido por escrito. Usarlo para saltar a redes ajenas es un delito.

## 🧪 Laboratorio guiado

1. **Port forwarding local** (`-L`): accede a un servicio del pivote/red interna como si fuera local:

   ```bash
   ssh -L 8080:10.20.0.5:80 usuario@pivote
   curl http://127.0.0.1:8080/
   ```

2. **Port forwarding remoto** (`-R`): expón un servicio tuyo en el pivote (útil para reverse shells controladas):

   ```bash
   ssh -R 9000:127.0.0.1:80 usuario@pivote
   ```

3. **Túnel dinámico SOCKS** (`-D`):

   ```bash
   ssh -D 1080 usuario@pivote
   ```

4. **Configura proxychains** (`/etc/proxychains4.conf`):

   ```text
   [ProxyList]
   socks5 127.0.0.1 1080
   ```

5. **Enruta herramientas** por el túnel para alcanzar la red interna:

   ```bash
   proxychains4 nmap -sT -Pn -p 22,80,445 10.20.0.0/24
   proxychains4 curl http://10.20.0.5/
   ```

6. **Pivote sin SSH con Chisel** (esquema): en el pivote `chisel server -p 8000 --reverse`; en el atacante `chisel client <pivote>:8000 R:socks` para obtener un SOCKS.
7. **Lado defensivo**: en el pivote, detecta el túnel observando conexiones anómalas:

   ```bash
   ss -tnp | grep -E "ESTAB"
   ```

   y revisa reglas de firewall que impidan reenvíos no autorizados.

## ✍️ Ejercicios

1. Alcanza un servicio web de la red interna únicamente con un túnel `-L`.
2. Usa `-D` + proxychains para escanear la red interna con Nmap (`-sT`, sin raw).
3. Explica por qué con SOCKS conviene `-sT` y no `-sS` en Nmap.
4. Configura un reenvío remoto `-R` y describe un caso legítimo de uso (administración).
5. Con Chisel, establece un pivote cuando el pivote solo permite salida HTTP.
6. Desde el lado azul, escribe una regla de firewall/IDS que detecte un túnel SOCKS sospechoso.

## 📝 Reto verificable

Partiendo de un host pivote con dos interfaces (una hacia ti, otra hacia una red interna aislada), establece un túnel que te permita escanear y acceder a un servicio de la red interna que **no** es alcanzable directamente. Entrega los comandos usados, evidencia del escaneo a través del túnel y una explicación del camino que sigue un paquete desde tu máquina hasta la víctima interna.

**Criterio de aceptación:** demuestras acceso a un servicio interno inaccesible sin el túnel, el escaneo por proxychains devuelve puertos de la red interna, y la explicación del recorrido del paquete es correcta (atacante → SOCKS local → SSH → pivote → red interna).

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| proxychains "denied" o sin salida | Puerto SOCKS mal configurado; verifica que `-D 1080` está activo y coincide con el conf |
| Nmap por proxychains no ve nada | Usaste `-sS` (raw no funciona por SOCKS); usa `-sT -Pn` |
| `-R` no expone el puerto | Falta `GatewayPorts yes` en el sshd del pivote |
| Túnel se cae por inactividad | Añade `ServerAliveInterval` o usa `autossh` |
| DNS no resuelve por el túnel | proxychains no proxifica DNS UDP por defecto; usa `proxy_dns` o resuelve por IP |

## ❓ Preguntas frecuentes

**❓ ¿Qué diferencia hay entre `-L` y `-R`?**
`-L` reenvía un puerto **local** hacia un destino accesible desde el servidor SSH (acceso entrante a un servicio remoto). `-R` reenvía un puerto **del servidor** hacia un destino accesible desde tu máquina (útil para exponerte hacia dentro).

**❓ ¿Por qué SOCKS y no un proxy HTTP?**
SOCKS es agnóstico al protocolo: túnela cualquier TCP (y SOCKS5 también UDP). Un proxy HTTP solo entiende HTTP.

**❓ ¿El pivoting es siempre malicioso?**
No. Los administradores usan túneles SSH y bastiones legítimamente. La técnica es neutra; el contexto y la autorización determinan la legalidad.

**❓ ¿Cómo se defiende una red del pivoting?**
Con segmentación estricta (clase 042), egress filtering, detección de túneles (tráfico cifrado anómalo, SOCKS), y principio de mínimo privilegio en los hosts que podrían servir de trampolín.

## 🔗 Referencias

- OpenSSH manual (port forwarding). <https://man.openbsd.org/ssh#L>
- proxychains-ng. <https://github.com/rofl0r/proxychains-ng>
- Chisel. <https://github.com/jpillora/chisel>
- MITRE ATT&CK — Proxy (T1090). <https://attack.mitre.org/techniques/T1090/>

## ➡️ Siguiente clase

[Clase 038 - Seguridad WiFi: WPA2, WPA3 y superficie de ataque](../038-seguridad-wifi-wpa2-wpa3-y-superficie-de-ataque/README.md)
