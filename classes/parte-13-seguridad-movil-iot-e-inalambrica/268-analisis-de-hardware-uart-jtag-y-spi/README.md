# Clase 268 — Análisis de hardware: UART, JTAG y SPI

> Parte: **13 — Seguridad móvil, IoT e inalámbrica** · Fuente: *Practical IoT Hacking* (Chantzis et al.) y *The Hardware Hacking Handbook* (Woudenberg, O'Flynn)
> ⏱️ Duración estimada: **150 min** · Nivel: **Experto**

---

## 🎯 Objetivo

Acceder al nivel más bajo de un dispositivo embebido a través de sus interfaces de depuración físicas: UART para obtener una consola serie, JTAG/SWD para control del procesador y volcado de memoria, y SPI para leer/escribir el chip de flash directamente. El alumno aprenderá a identificar puntos de prueba en una PCB, conectar un adaptador, y extraer firmware o consolas root del hardware propio.

> ⚠️ **Nota ética y de seguridad:** trabaja solo con dispositivos de tu propiedad. Manipular electrónica implica riesgo de dañar el equipo o de descarga; respeta voltajes (3.3 V típico) y nunca alimentes pines a ciegas.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Identificar** interfaces UART, JTAG/SWD y SPI en una placa por inspección y medición.
2. **Conectar** un adaptador USB-serie/lógico y obtener una consola UART.
3. **Usar** JTAG/SWD con OpenOCD para detener el CPU y volcar memoria.
4. **Leer** un chip de flash SPI con un programador (CH341A/Bus Pirate/flashrom).
5. **Interpretar** señales con un analizador lógico para identificar protocolos.
6. **Extraer** firmware o credenciales aprovechando el acceso físico.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Seguridad eléctrica y voltajes | Evita dañar el equipo y a ti mismo |
| 2 | Identificación de puertos en PCB | Localiza los puntos de acceso |
| 3 | UART: consola serie | Suele dar shell/logs de arranque |
| 4 | Analizador lógico | Descubre pinout y protocolo |
| 5 | JTAG/SWD con OpenOCD | Control total del procesador |
| 6 | SPI y volcado de flash | Extrae el firmware completo |
| 7 | Contramedidas del fabricante | Fusibles, deshabilitar JTAG |

## 📖 Definiciones y características

- **UART:** comunicación serie asíncrona (TX, RX, GND, VCC) usada para consolas de depuración. Característica: a menudo expone un shell root sin autenticación.
- **JTAG/SWD:** interfaz de depuración que controla el procesador (leer/escribir registros y memoria). Característica: permite volcar RAM/flash y saltar protecciones.
- **SPI:** bus serie síncrono (MOSI, MISO, CLK, CS) que conecta el CPU al chip de flash. Característica: se puede leer el flash directamente con un programador.
- **Analizador lógico:** dispositivo que captura señales digitales para decodificar protocolos. Característica: identifica baud rate y pinout desconocidos.
- **OpenOCD:** software que habla JTAG/SWD con adaptadores para depuración y volcado. Característica: soporta multitud de targets ARM/MIPS.
- **flashrom:** utilidad para leer/escribir chips de flash SPI. Característica: soporta muchos programadores (CH341A, Bus Pirate).

## 🧰 Herramientas y preparación

- **Adaptador USB-UART** (FTDI/CP2102), **multímetro**, **analizador lógico** (Saleae/clon), **programador SPI** (CH341A) o **Bus Pirate**, **JTAG/SWD** (J-Link, FT2232, ST-Link).
- Cables Dupont, pinza de test (SOIC clip) para leer flash sin desoldar.

```bash
# UART: abrir consola serie
screen /dev/ttyUSB0 115200          # o: picocom -b 115200 /dev/ttyUSB0

# JTAG/SWD con OpenOCD
openocd -f interface/jlink.cfg -f target/<soc>.cfg
# luego, en telnet 4444:  halt ; dump_image dump.bin 0x0 0x100000

# SPI: leer el chip de flash
flashrom -p ch341a_spi -r flash_dump.bin
```

## 🧪 Laboratorio guiado

1. **Inspecciona la PCB** de un dispositivo propio: busca cabeceras de 4 pines (UART) y de 2x5/10 pines (JTAG), y el chip de flash (SOIC-8).
2. **Identifica el pinout UART:** con el multímetro localiza GND (continuidad al plano de tierra), VCC (~3.3 V), y usa el analizador lógico para hallar TX (actividad al arrancar) y el baud rate.
3. **Conecta el adaptador UART** (TX↔RX cruzados, GND común, sin conectar VCC si el equipo se auto-alimenta) y abre la consola con `screen`.
4. **Captura el arranque:** observa los logs de U-Boot; intenta interrumpirlo para entrar a su consola.
5. **Busca shell:** al terminar el arranque, comprueba si hay una consola root sin contraseña.
6. **JTAG/SWD:** conecta el adaptador, lanza OpenOCD, `halt` el CPU y `dump_image` de la flash/RAM.
7. **SPI directo:** con la pinza SOIC sobre el chip de flash, vuelca su contenido con `flashrom` y analízalo con binwalk (clase 267).
8. **Documenta** pinout, comandos y hallazgos.

## ✍️ Ejercicios

1. Identifica y etiqueta el pinout UART de una placa propia usando multímetro y analizador lógico.
2. Captura y guarda el log de arranque completo por UART.
3. Interrumpe U-Boot y lista sus variables de entorno.
4. Vuelca el flash SPI con flashrom y verifica su tamaño esperado.
5. Con OpenOCD, detén el CPU y lee una región de memoria.
6. Compara el firmware obtenido por SPI con la descarga oficial (si existe).

## 📝 Reto verificable

Extrae el firmware de un dispositivo propio **por dos vías físicas distintas** (por ejemplo, consola UART que permite `cat` de una partición y volcado directo por SPI), o consigue una consola root por UART. **Criterio de aceptación:** obtienes un shell interactivo por UART **o** un volcado de flash que binwalk desempaqueta correctamente, documentando el pinout que usaste.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Consola serie muestra basura | Baud rate incorrecto; prueba 9600/57600/115200 |
| No hay salida por UART | TX/RX invertidos o pin equivocado; cruza TX↔RX y reidentifica |
| Dispositivo se reinicia al conectar | Alimentaste VCC indebidamente; no conectes VCC si se auto-alimenta |
| OpenOCD no detecta el target | Archivo de config equivocado o JTAG deshabilitado por fusible |
| flashrom no reconoce el chip | Mal contacto de la pinza o chip no soportado; especifica `-c` manualmente |

## ❓ Preguntas frecuentes

**❓ ¿Cómo sé qué pin es UART sin documentación?**
Mide con multímetro (GND por continuidad, VCC ~3.3 V estable) y con el analizador lógico observa qué pin tiene ráfagas de datos al encender: ese es TX.

**❓ ¿Puedo dañar el dispositivo?**
Sí, si aplicas voltaje incorrecto o cortocircuitas pines. Trabaja a 3.3 V, verifica antes de conectar VCC y usa un adaptador con el mismo nivel lógico.

**❓ ¿Por qué usar SPI si ya tengo UART?**
UART puede no dar shell o exponer solo parte del sistema; leer el flash por SPI extrae la imagen completa aunque el software lo impida.

## 🔗 Referencias

- *The Hardware Hacking Handbook* — Jasper van Woudenberg, Colin O'Flynn (No Starch Press).
- OpenOCD: <https://openocd.org/> · flashrom: <https://www.flashrom.org/>
- *Practical IoT Hacking*, caps. de hardware — Chantzis et al.
- JTAGulator (identificación de pinout): <http://www.grandideastudio.com/jtagulator/>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-268-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-268-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 269 - Radio definida por software (SDR)](../269-radio-definida-por-software-sdr/README.md)
