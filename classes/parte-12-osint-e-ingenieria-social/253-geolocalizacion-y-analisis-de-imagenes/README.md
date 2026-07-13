# Clase 253 — Geolocalización y análisis de imágenes

> Parte: **12 — OSINT e ingeniería social** · Fuente: Bellingcat *Online Investigation Toolkit* · *Open Source Intelligence Techniques* (M. Bazzell)
> ⏱️ Duración estimada: **110 min** · Nivel: **Intermedio**

---

## 🎯 Objetivo

Aprender a extraer y verificar la ubicación y autenticidad de imágenes mediante metadatos EXIF,
búsqueda inversa y análisis visual (chronolocation y geolocation). El alumno terminará capaz de
determinar dónde y cuándo se tomó una foto pública y de detectar imágenes manipuladas o
descontextualizadas, una habilidad clave en verificación e investigación.

## ⚖️ Nota ética

Trabaja con **tus propias imágenes o material público de prueba**. No uses estas técnicas para
localizar físicamente a personas sin autorización: la geolocalización de individuos puede facilitar
acoso o daño y ser delito.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Extraer** y leer metadatos EXIF, incluida geolocalización cuando existe.
2. **Ejecutar** búsqueda inversa de imágenes en varios motores.
3. **Geolocalizar** una foto por pistas visuales (señales, arquitectura, vegetación, sombras).
4. **Cronolocalizar** una imagen estimando fecha/hora por sombras y contexto.
5. **Detectar** manipulación o descontextualización de imágenes.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Metadatos EXIF | GPS, cámara y fecha en el archivo |
| 2 | Limpieza de metadatos | Las redes suelen borrarlos |
| 3 | Búsqueda inversa | Encuentra origen y reusos |
| 4 | Geolocalización visual | Ubicar sin GPS |
| 5 | Cronolocalización | Estimar cuándo por sombras |
| 6 | Detección de manipulación | Distinguir real de falso |
| 7 | Verificación cruzada | Confirmar con mapas/satélite |

## 📖 Definiciones y características

- **EXIF:** metadatos incrustados por la cámara (GPS, modelo, fecha). Característica: muy revelador, pero eliminado por muchas plataformas.
- **Búsqueda inversa de imágenes:** buscar dónde más aparece una foto. Característica: revela origen y descontextualización.
- **Geolocation (visual):** deducir ubicación por elementos de la escena. Característica: no necesita metadatos.
- **Chronolocation:** estimar fecha/hora por sombras y contexto. Característica: usa geometría solar.
- **Descontextualización:** imagen real usada fuera de su contexto original. Característica: desinformación frecuente.
- **ELA (Error Level Analysis):** técnica para detectar zonas editadas. Característica: indicio, no prueba concluyente.

## 🧰 Herramientas y preparación

- **Metadatos:** `exiftool foto.jpg`; para lote, `exiftool -csv *.jpg > meta.csv`.
- **Búsqueda inversa:** Google Lens, Yandex Images (muy fuerte en geolocalización), TinEye, Bing Visual.
- **Mapas y satélite:** Google Earth, Google Street View, Mapillary, OpenStreetMap.
- **Sombras/sol:** SunCalc (`https://www.suncalc.org`) para chronolocation.
- **Manipulación:** FotoForensics (ELA), InVID/WeVerify para vídeo.
- **Recordatorio:** usa fotos propias o de bancos públicos; no persigas a personas reales.

## 🧪 Laboratorio guiado

Objetivo: **una foto tuya** con GPS y una foto pública "misteriosa" de práctica.

1. Extrae metadatos: `exiftool foto.jpg` — localiza `GPS Position` y `Create Date`.
2. Convierte las coordenadas y ábrelas en Google Maps; confirma el lugar.
3. Sube la foto a un servicio y descárgala: vuelve a correr `exiftool` y observa que el GPS desapareció.
4. Con una foto sin EXIF, haz búsqueda inversa en Yandex y Google Lens; anota coincidencias.
5. Geolocaliza por pistas: idioma de carteles, tipo de enchufes, señales de tráfico, vegetación.
6. Verifica con Street View: encuadra el mismo edificio o esquina.
7. Cronolocaliza: mide la dirección/longitud de sombras y usa SunCalc para estimar hora y fecha.
8. Pasa la imagen por FotoForensics (ELA) y documenta si hay indicios de edición.
9. Redacta un informe de verificación con ubicación, fecha estimada y nivel de confianza.

## ✍️ Ejercicios

1. Compara el EXIF de una foto antes y después de subirla a dos redes distintas.
2. Geolocaliza una foto pública solo con pistas visuales y documenta el razonamiento.
3. Usa SunCalc para estimar la hora de una foto con sombras claras.
4. Detecta una imagen descontextualizada mediante búsqueda inversa.
5. Explica por qué el ELA no es prueba concluyente de manipulación.
6. Redacta una guía de 5 pasos para verificar una imagen viral antes de compartirla.

## 📝 Reto verificable

Geolocaliza y cronolocaliza una **foto pública de práctica** sin metadatos GPS, aportando: ubicación
(con captura de Street View coincidente), fecha/hora estimada y análisis de autenticidad.
**Criterio de aceptación:** la ubicación se corrobora con al menos dos pistas visuales
independientes y una imagen de mapa/satélite que coincide con la escena.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|------------------------|
| "No EXIF data found" | La plataforma lo eliminó. Pasa a geolocalización visual. |
| Búsqueda inversa sin resultados | Google es débil en lugares. Prueba Yandex y Bing. |
| Coordenadas apuntan al océano | Confusión lat/long o formato. Verifica orden y signo. |
| Hora mal estimada | No se consideró zona horaria/DST. Ajusta con SunCalc y la ubicación. |
| Falso positivo de manipulación | ELA malinterpretado por recompresión. Corrobora con más señales. |

## ❓ Preguntas frecuentes

**❓ ¿Todas las fotos tienen GPS?**
No. Depende de la cámara/ajustes y casi todas las redes lo eliminan al subir. Por eso la
geolocalización visual es imprescindible.

**❓ ¿Yandex es mejor que Google para geolocalizar?**
A menudo sí para reconocimiento de lugares y rostros/escenas. Usa varios motores y combina resultados.

**❓ ¿El ELA prueba que una imagen es falsa?**
No. Es un indicio. La verificación seria combina metadatos, búsqueda inversa, análisis visual y
coherencia contextual.

## 🔗 Referencias

- Bellingcat — Online Investigation Toolkit. <https://www.bellingcat.com/resources/>
- ExifTool. <https://exiftool.org/>
- SunCalc. <https://www.suncalc.org/>
- FotoForensics. <https://fotoforensics.com/>
- InVID/WeVerify. <https://www.invid-project.eu/>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-253-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-253-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 254 - OSINT tecnico: Shodan y Censys](../254-osint-tecnico-shodan-y-censys/README.md)
