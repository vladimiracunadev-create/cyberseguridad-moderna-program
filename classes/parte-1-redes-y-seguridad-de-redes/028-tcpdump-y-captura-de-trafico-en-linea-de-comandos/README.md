# Clase 028 — tcpdump y captura de tráfico en línea de comandos

> Parte: **1 — Redes y seguridad de redes** · Fuente: *Practical Packet Analysis, C. Sanders*
> ⏱️ Duración estimada: **90 min** · Nivel: **Fundamentos**

---

## 🎯 Objetivo

Capturar y filtrar tráfico desde la terminal con **tcpdump**, la herramienta imprescindible cuando no hay entorno gráfico (servidores, contenedores, dispositivos remotos por SSH). El alumno aprenderá la sintaxis BPF, la rotación de archivos y el flujo de trabajo "capturar en el servidor, analizar en Wireshark".

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Seleccionar** interfaz, tamaño de snap y verbosidad adecuados para cada captura.
2. **Escribir** filtros BPF por host, red, puerto, protocolo y flags TCP.
3. **Guardar** capturas en `.pcap` y rotarlas por tamaño o tiempo con un ring buffer.
4. **Leer** capturas guardadas y aplicar filtros de lectura sin recapturar.
5. **Combinar** tcpdump con SSH para capturar en remoto y ver en local.
6. **Reconocer** los límites de tcpdump frente a analizadores gráficos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Selección de interfaz (`-i`) | Capturar en el punto correcto |
| 2 | Snap length (`-s`) y verbosidad (`-v`) | Equilibrio detalle/tamaño |
| 3 | Filtros BPF primitivos y compuestos | Reducir ruido en origen |
| 4 | Escritura y lectura de pcap (`-w`/`-r`) | Analizar después con otras herramientas |
| 5 | Rotación con `-C`, `-G`, `-W` | Capturas de larga duración |
| 6 | Filtrado por flags TCP | Ver handshakes, resets, escaneos |
| 7 | tcpdump sobre SSH | Capturar donde no hay GUI |

## 📖 Definiciones y características

- **BPF (Berkeley Packet Filter):** lenguaje de filtrado compilado en kernel; muy eficiente porque descarta paquetes antes de copiarlos a espacio de usuario.
- **Snap length (`-s`):** bytes capturados por paquete. `-s 0` (o el valor por defecto moderno) captura el paquete completo.
- **Ring buffer:** conjunto rotatorio de archivos (`-C` tamaño, `-W` número) que evita llenar el disco.
- **Primitiva BPF:** unidad básica del filtro: `host`, `net`, `port`, `tcp`, `udp`, `src`, `dst`.
- **`-n`:** desactiva resolución DNS/puertos; acelera y evita generar tráfico extra durante la captura.

## 🧰 Herramientas y preparación

- **tcpdump** (Linux/macOS/BSD): `sudo apt install tcpdump` o viene preinstalado.
- Requiere privilegios para capturar: `sudo` o capacidad `CAP_NET_RAW` (`sudo setcap cap_net_raw+ep $(which tcpdump)`).
- Para analizar después: Wireshark o `tshark`.

> ⚠️ **Nota ética:** captura solo en interfaces de sistemas que administras o con autorización escrita. En servidores compartidos, tcpdump puede exponer datos de terceros.

## 🧪 Laboratorio guiado

1. Lista interfaces disponibles:

   ```bash
   sudo tcpdump -D
   ```

2. Captura básica sin resolución de nombres:

   ```bash
   sudo tcpdump -i eth0 -n
   ```

3. Filtra por host y puerto:

   ```bash
   sudo tcpdump -i eth0 -n host 192.168.56.101 and tcp port 80
   ```

4. Captura solo paquetes SYN (inicio de conexión) usando el offset de flags:

   ```bash
   sudo tcpdump -i eth0 -n 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack == 0'
   ```

5. Guarda a archivo con snap completo:

   ```bash
   sudo tcpdump -i eth0 -s 0 -w /tmp/lab028.pcap port 53
   ```

   Genera tráfico DNS en otra terminal (`dig example.com`) y detén con Ctrl-C.
6. Lee lo capturado con filtro de lectura:

   ```bash
   tcpdump -n -r /tmp/lab028.pcap 'udp port 53'
   ```

7. Captura larga con rotación (archivos de 10 MB, máximo 5):

   ```bash
   sudo tcpdump -i eth0 -s 0 -C 10 -W 5 -w /tmp/rot.pcap
   ```

8. Aumenta verbosidad para ver TTL, opciones y checksums:

   ```bash
   sudo tcpdump -i eth0 -vvv -n icmp
   ```

9. **Captura remota vía SSH** y análisis en tu Wireshark local:

   ```bash
   ssh usuario@servidor 'sudo tcpdump -i eth0 -s 0 -U -w - not port 22' | wireshark -k -i -
   ```

   (El filtro `not port 22` evita capturar tu propia sesión SSH y un bucle infinito.)

## ✍️ Ejercicios

1. Captura solo tráfico ICMP entre dos hosts de tu laboratorio y guárdalo en `icmp.pcap`.
2. Escribe un filtro que capture tráfico HTTP y HTTPS (`port 80 or port 443`).
3. Captura paquetes con el flag RST activo e interpreta qué conexiones se rechazan.
4. Usa `-c 100` para limitar la captura a 100 paquetes y explica cuándo conviene.
5. Rota capturas cada 60 segundos con `-G 60` y nómbralas con `%Y%m%d-%H%M%S`.
6. Convierte tu `.pcap` a `.pcapng` con `editcap` y ábrelo en Wireshark.

## 📝 Reto verificable

Desde un servidor de laboratorio (o VM) sin entorno gráfico, captura durante 30 segundos todo el tráfico **excepto** tu sesión SSH, guárdalo con rotación en archivos de 5 MB, y entrega el primer archivo junto con el comando exacto usado. Documenta cuántos paquetes contiene según `tcpdump -r archivo -n | wc -l`.

**Criterio de aceptación:** el archivo abre sin errores en Wireshark, no contiene tráfico del puerto 22 hacia/desde tu IP, y el conteo declarado coincide con el del revisor.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| `tcpdump: <iface>: You don't have permission` | Falta privilegio; usa `sudo` o asigna `cap_net_raw` |
| La captura por SSH nunca termina o se dispara | No excluiste el puerto 22; añade `not port 22` |
| Paquetes truncados en Wireshark | Snap length bajo; captura con `-s 0` |
| Filtro no captura nada | Sintaxis BPF incorrecta; prueba el filtro por partes y usa comillas |
| Disco lleno en captura larga | Sin rotación; usa `-C`/`-W` o `-G`/`-W` |
| No resuelve nombres y va lento | Al contrario, `-n` acelera; si va lento probablemente falta `-n` y hay DNS inverso |

## ❓ Preguntas frecuentes

**❓ ¿tcpdump o Wireshark?**
tcpdump para capturar donde no hay GUI y para filtros rápidos; Wireshark para el análisis profundo. El flujo típico es capturar con tcpdump y disecar en Wireshark.

**❓ ¿Por qué usar `-w` en vez de leer la salida de texto?**
El texto pierde información. `-w` guarda el paquete íntegro para análisis posterior con cualquier herramienta.

**❓ ¿Los filtros BPF de tcpdump y Wireshark son iguales?**
Los filtros de **captura** de Wireshark sí son BPF (idénticos a tcpdump). Los de **visualización** de Wireshark son un lenguaje distinto y más rico.

**❓ ¿Cómo capturo sin que la captura afecte el rendimiento del servidor?**
Filtra en origen con BPF, usa snap length moderado si solo necesitas cabeceras (`-s 96`) y evita `-vvv` en producción.

## 🔗 Referencias

- tcpdump man page y ejemplos. <https://www.tcpdump.org/manpages/tcpdump.1.html>
- pcap-filter (sintaxis BPF). <https://www.tcpdump.org/manpages/pcap-filter.7.html>
- Sanders, C. *Practical Packet Analysis*, apéndice de tcpdump.
- Wireshark: capturas remotas. <https://wiki.wireshark.org/CaptureSetup/Pipes>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-028-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-028-presentacion.pptx) — deck para proyectar en clase.

## ⬅️ Clase anterior

[Clase 027 — Análisis de tráfico: filtros, seguimiento de flujos y estadísticas](../027-analisis-de-trafico-filtros-seguimiento-de-flujos-y-estadisticas/README.md)

## ➡️ Siguiente clase

[Clase 029 — Nmap: descubrimiento de hosts y técnicas de ping](../029-nmap-descubrimiento-de-hosts-y-tecnicas-de-ping/README.md)
