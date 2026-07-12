# Parte 13 — Seguridad móvil, IoT e inalámbrica

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-14-grc-riesgo-y-cumplimiento/README.md)

**15 clases** · rango 261–275 · Android, iOS, firmware, hardware, SDR e ICS/SCADA

**Fuentes de referencia de esta parte:**

- *The Mobile Application Hacker's Handbook* — Dominic Chell, Tyrone Erasmus, Shaun Colley, Ollie Whitehouse (Wiley).
- *Practical IoT Hacking* — Fotios Chantzis, Ioannis Stais, Paulino Calderon, Evangelos Deirmentzoglou, Beau Woods (No Starch Press).
- *Hacking Exposed Wireless, 3rd Edition* — Joshua Wright, Johnny Cache (McGraw-Hill).
- OWASP Mobile Application Security (MASVS/MASTG) y OWASP Internet of Things Project.
- NIST SP 800-82 *Guide to Operational Technology (OT) Security* y ISA/IEC 62443.

---

## 🎯 ¿De qué trata esta parte?

Todo lo que no es un servidor web tradicional vive aquí: el teléfono en tu bolsillo, la cámara IP de la sala, el termostato, el auto conectado, la bomba de insulina y el PLC que controla una planta de agua. Esta parte lleva las técnicas de pentest más allá del navegador y el endpoint clásico hacia el mundo físico y radioeléctrico. Aprenderás a auditar aplicaciones Android e iOS, a extraer y analizar firmware, a "pinchar" cables de depuración con un adaptador de pocos dólares, a capturar y demodular señales de radio con SDR, y a entender por qué los sistemas industriales fallan con un diseño que priorizó disponibilidad sobre confidencialidad.

El hilo conductor es que cada uno de estos dispositivos tiene una **superficie de ataque multicapa**: aplicación, comunicaciones, nube, firmware y hardware físico. Un atacante competente pivota entre capas; un defensor competente las modela todas. Verás herramientas reales y estándares de la industria, no juguetes: Frida, MobSF, apktool, Aircrack-ng, hcxdumptool, GNU Radio, Proxmark3, Ghidra, Bus Pirate y `can-utils`.

Esta parte sirve a pentesters que quieren expandir su alcance, a ingenieros de producto que diseñan dispositivos conectados, a equipos de OT/ICS que heredaron infraestructura crítica insegura, y a investigadores de seguridad que quieren entrar en RE móvil o hardware hacking.

## 🧩 Problemas que resuelve

- Auditar aplicaciones móviles (Android/iOS) contra almacenamiento inseguro, comunicación débil y controles del lado del cliente evadibles.
- Instrumentar apps en tiempo de ejecución para saltar detección de root/jailbreak y certificate pinning en laboratorio.
- Extraer, desempaquetar y analizar firmware de dispositivos embebidos en busca de credenciales, claves y binarios vulnerables.
- Identificar y usar interfaces de depuración físicas (UART, JTAG, SPI) para volcar memoria y obtener consolas root.
- Capturar y analizar tráfico inalámbrico no-WiFi (RFID/NFC, BLE, señales sub-GHz) con SDR y lectores dedicados.
- Ejecutar ataques WiFi modernos (Evil Twin, captura PMKID) y entender por qué WPA2-PSK y WPA3 fallan o resisten.
- Evaluar riesgos en entornos donde un fallo de seguridad tiene consecuencias físicas: plantas industriales, vehículos y dispositivos médicos.

## 🎓 Resultados de aprendizaje

Al terminar la parte, el alumno podrá:

- Describir la arquitectura de seguridad de Android e iOS (sandbox, permisos, Keychain/Keystore, arranque seguro) y sus límites.
- Montar un entorno de pentest móvil con emuladores/dispositivos rooteados o con jailbreak y proxy interceptor.
- Realizar RE estático y dinámico de una app usando apktool, Ghidra/Hopper y Frida.
- Extraer firmware con `binwalk`/`dd` y analizar sistemas de archivos y binarios embebidos.
- Conectar y usar un adaptador UART/JTAG para obtener acceso de bajo nivel a un dispositivo propio.
- Capturar un handshake/PMKID de WiFi y crackearlo offline, y montar un Evil Twin controlado en laboratorio.
- Explicar el modelo Purdue, protocolos ICS (Modbus/DNP3), el bus CAN y los riesgos de dispositivos médicos conectados.
- Redactar hallazgos y recomendaciones alineados a OWASP MASVS, NIST SP 800-82 e IEC 62443.

## 🧱 Prerrequisitos

- Fundamentos de redes y TCP/IP (Parte 3) y de criptografía aplicada (Parte 6).
- Manejo de Linux y línea de comandos (Parte 2).
- Bases de pentest web y de aplicaciones (Partes 8–9): proxies interceptores, Burp Suite.
- Nociones de análisis de malware y RE (Parte 11) ayudan en las clases de RE móvil y firmware.

## 🗺️ Estructura temática

| Bloque | Clases | Enfoque |
|--------|--------|---------|
| Móvil Android | 261–262 | Arquitectura de seguridad y pentest de apps Android |
| Móvil iOS | 263–264 | Arquitectura de seguridad y pentest de apps iOS |
| RE móvil | 265 | Ingeniería inversa estática y dinámica de apps |
| IoT y firmware | 266–267 | Superficie de ataque IoT y hacking de firmware |
| Hardware y radio | 268–271 | UART/JTAG/SPI, SDR, RFID/NFC, Bluetooth/BLE |
| Inalámbrica WiFi | 272 | Evil Twin, captura PMKID y crackeo |
| OT y sistemas críticos | 273–275 | ICS/SCADA, automotriz/CAN y dispositivos médicos |

## 🔗 Referencias de la parte

- OWASP Mobile Application Security — <https://mas.owasp.org/>
- OWASP Internet of Things Project — <https://owasp.org/www-project-internet-of-things/>
- NIST SP 800-82 Rev. 3 — <https://csrc.nist.gov/pubs/sp/800/82/r3/final>
- Frida — <https://frida.re/> · MobSF — <https://github.com/MobSF/Mobile-Security-Framework-MobSF>
- Aircrack-ng — <https://www.aircrack-ng.org/> · hcxdumptool — <https://github.com/ZerBea/hcxdumptool>
- GNU Radio — <https://www.gnuradio.org/> · Proxmark3 — <https://github.com/RfidResearchGroup/proxmark3>

> ⚠️ **Nota ética:** todo el contenido ofensivo de esta parte se practica **solo** en dispositivos, redes y sistemas de tu propiedad o con autorización explícita por escrito. Interceptar comunicaciones ajenas, clonar credenciales de terceros o manipular sistemas industriales/médicos en producción es ilegal y peligroso.

## ▶️ Empezar

[Clase 261 — Seguridad de Android: arquitectura](261-seguridad-de-android-arquitectura/README.md)
