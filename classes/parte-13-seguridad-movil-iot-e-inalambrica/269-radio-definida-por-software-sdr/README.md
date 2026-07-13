# Clase 269 — Radio definida por software (SDR)

> Parte: **13 — Seguridad móvil, IoT e inalámbrica** · Fuente: *Practical IoT Hacking* (Chantzis et al.) y documentación de GNU Radio
> ⏱️ Duración estimada: **120 min** · Nivel: **Avanzado**

---

## 🎯 Objetivo

Introducir la radio definida por software (SDR) como herramienta para descubrir, capturar y analizar señales inalámbricas más allá de WiFi y Bluetooth: mandos remotos sub-GHz, sensores ISM, telemetría y protocolos propietarios. El alumno aprenderá conceptos de RF (IQ, frecuencia, ancho de banda, modulación), capturará señales con un RTL-SDR/HackRF y las demodulará para entender su contenido, respetando siempre la legalidad del espectro.

> ⚠️ **Nota ética y legal:** recibir/escuchar puede estar restringido según jurisdicción; **transmitir** requiere licencia y equipo homologado. Practica solo con dispositivos propios y bandas permitidas, y nunca interfieras servicios ajenos. Muchos SDR económicos (RTL-SDR) solo reciben.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Explicar** conceptos de RF: muestras IQ, frecuencia central, ancho de banda y modulación.
2. **Configurar** un SDR (RTL-SDR/HackRF) con GQRX/SDR#.
3. **Descubrir** y localizar señales en el espectro (waterfall).
4. **Capturar** señales a fichero IQ para análisis offline.
5. **Demodular** señales simples (OOK/ASK, FSK) con GNU Radio o Universal Radio Hacker.
6. **Analizar** un protocolo sub-GHz de un dispositivo propio (p. ej. un mando).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Fundamentos de RF e IQ | Base para entender cualquier captura |
| 2 | Hardware SDR (RTL-SDR/HackRF) | Determina bandas y capacidades |
| 3 | Waterfall y descubrimiento | Localizar la señal objetivo |
| 4 | Modulaciones (OOK/ASK, FSK) | Elegir el demodulador correcto |
| 5 | Captura IQ | Análisis reproducible offline |
| 6 | GNU Radio y URH | Demodular y decodificar |
| 7 | Legalidad del espectro | Evita infracciones graves |

## 📖 Definiciones y características

- **SDR:** radio cuyo procesamiento se hace en software sobre muestras digitalizadas. Característica: flexible para muchas bandas y protocolos.
- **Muestras IQ:** representación compleja (in-phase/quadrature) de la señal. Característica: contienen amplitud y fase para demodular cualquier esquema.
- **OOK/ASK:** modulación por presencia/ausencia o amplitud de portadora, típica de mandos baratos. Característica: fácil de demodular visualmente.
- **FSK:** modulación por desplazamiento de frecuencia. Característica: común en sensores y telemetría.
- **GNU Radio:** framework de flujogramas para procesar señales. Característica: construye demoduladores por bloques.
- **Universal Radio Hacker (URH):** herramienta que descubre, demodula y decodifica protocolos inalámbricos. Característica: acelera el análisis de tramas.

## 🧰 Herramientas y preparación

- **RTL-SDR** (recepción, ~24–1766 MHz) o **HackRF One** (TX/RX 1 MHz–6 GHz, solo TX en laboratorio propio y bandas permitidas).
- **GQRX**/**SDR#** para exploración, **GNU Radio Companion** y **URH** para análisis.

```bash
# Verificar el SDR
rtl_test -t                         # prueba del RTL-SDR
gqrx                                # exploración con waterfall

# Captura IQ desde línea de comandos
rtl_sdr -f 433920000 -s 2048000 -g 40 captura.iq

# Análisis con Universal Radio Hacker
urh
```

## 🧪 Laboratorio guiado

1. **Conecta el SDR** y verifica con `rtl_test` que funciona sin pérdidas de muestras.
2. **Explora el espectro:** en GQRX, sintoniza la banda ISM de 433 MHz y observa el waterfall mientras accionas un mando propio.
3. **Localiza la señal:** identifica la frecuencia central exacta de la ráfaga del mando.
4. **Captura IQ:** graba la transmisión con `rtl_sdr` o desde URH a la frecuencia adecuada.
5. **Determina la modulación:** en URH, visualiza la señal y decide si es OOK/ASK o FSK.
6. **Demodula y decodifica:** ajusta parámetros (samples/símbolo, umbral) hasta obtener los bits; identifica preámbulo y payload.
7. **Interpreta el protocolo:** compara varias pulsaciones para ver qué campos cambian (contador rolling code vs. código fijo).
8. **Documenta** frecuencia, modulación, tasa de símbolo y estructura de la trama.

## ✍️ Ejercicios

1. Identifica la frecuencia central de un mando propio con GQRX.
2. Captura tres pulsaciones del mismo botón a fichero IQ.
3. Clasifica la modulación observando la forma de onda en URH.
4. Decodifica los bits de la trama y localiza el preámbulo.
5. Compara pulsaciones para determinar si usa código fijo o rolling code.
6. Documenta los parámetros necesarios para reproducir la captura.

## 📝 Reto verificable

Captura y decodifica la señal de un dispositivo sub-GHz **propio** (mando de garaje viejo, estación meteorológica, sensor). **Criterio de aceptación:** entregas la frecuencia, la modulación y la tasa de símbolo correctas, y una decodificación de los bits del payload con identificación de al menos el preámbulo y un campo de datos. No se requiere ni se permite retransmitir señales.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| `rtl_test` reporta pérdidas | USB saturado o ganancia mal; baja el sample rate |
| No veo la señal en el waterfall | Frecuencia/ganancia incorrectas; ajusta y amplía el span |
| Demodulación da bits aleatorios | Samples/símbolo o umbral mal; recalíbralos en URH |
| Señal muy débil | Antena inadecuada; usa una sintonizada a la banda |
| Frecuencia ligeramente desviada | Error de PPM del SDR; calíbralo con `rtl_test -p` |

## ❓ Preguntas frecuentes

**❓ ¿Puedo capturar cualquier frecuencia con un RTL-SDR?**
No: cubre aproximadamente 24 MHz–1.7 GHz y solo recibe. Para bandas más altas o transmitir necesitas hardware como HackRF, siempre dentro de la ley.

**❓ ¿Es legal escuchar señales de radio?**
Depende del país y de la banda. Escuchar tus propios dispositivos en bandas ISM suele ser aceptable; interceptar comunicaciones ajenas o transmitir sin licencia no lo es.

**❓ ¿Qué es un rolling code y por qué importa?**
Un código que cambia en cada uso para evitar ataques de repetición; distinguirlo de un código fijo es clave al analizar mandos y sistemas de acceso.

## 🔗 Referencias

- GNU Radio: <https://www.gnuradio.org/>
- Universal Radio Hacker: <https://github.com/jopohl/urh>
- RTL-SDR: <https://www.rtl-sdr.com/> · GQRX: <https://gqrx.dk/>
- *Practical IoT Hacking*, caps. de radio — Chantzis et al.

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-269-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-269-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 270 - Ataques a RFID y NFC](../270-ataques-a-rfid-y-nfc/README.md)
