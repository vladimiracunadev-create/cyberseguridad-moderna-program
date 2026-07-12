# Clase 064 — Esteganografía y ocultación de datos

> Parte: **2 — Criptografía aplicada** · Fuente: *Serious Cryptography* (Aumasson) y literatura de esteganografía/estegoanálisis
> ⏱️ Duración estimada: **90 min** · Nivel: **Intermedio**

---

## 🎯 Objetivo

Distinguir esteganografía (ocultar la **existencia** de un mensaje) de criptografía (ocultar su **contenido**), y entender cómo se combinan. El alumno aprenderá técnicas clásicas (LSB en imágenes, ocultación en metadatos), el estegoanálisis (detección), y usos legítimos (marcas de agua, watermarking) frente a usos maliciosos (exfiltración, C2 encubierto). Todo se practica sobre archivos propios de laboratorio.

> ⚠️ **Nota ética**: las técnicas de ocultación se practican **solo** con archivos propios y con fines de aprendizaje/defensa. Usarlas para exfiltrar datos o evadir controles sin autorización es ilícito.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Diferenciar** esteganografía de criptografía y explicar cuándo combinarlas.
2. **Ocultar y extraer** datos con LSB en imágenes.
3. **Usar** herramientas de esteganografía y estegoanálisis.
4. **Detectar** indicios de contenido oculto en archivos.
5. **Explicar** usos legítimos (watermarking) y riesgos (exfiltración, C2).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Estego vs cripto | Ocultar existencia vs contenido |
| 2 | LSB en imágenes | Técnica clásica |
| 3 | Ocultación en metadatos/otros formatos | Superficie amplia |
| 4 | Cifrar antes de ocultar | Defensa en profundidad |
| 5 | Estegoanálisis | Detección |
| 6 | Watermarking | Uso legítimo |
| 7 | Exfiltración y C2 encubierto | Amenaza defensiva |

## 📖 Definiciones y características

- **Esteganografía**: ocultar información dentro de otro medio (imagen, audio, texto) para que su existencia pase inadvertida. Característica: la seguridad depende de que nadie sospeche.
- **LSB (Least Significant Bit)**: sustituir el bit menos significativo de cada píxel/byte por bits del mensaje; imperceptible a la vista pero detectable estadísticamente.
- **Estegoanálisis**: conjunto de técnicas para detectar la presencia de datos ocultos (análisis estadístico, chi-cuadrado, herramientas como stegdetect).
- **Cover / stego object**: el medio portador original y el resultante con datos ocultos.
- **Watermarking**: marca embebida (visible o no) para autenticar propiedad o rastrear filtraciones; prioriza robustez sobre capacidad.
- **Capacidad vs imperceptibilidad vs robustez**: trade-off fundamental de toda técnica de ocultación.
- **Cifrar-luego-ocultar**: cifrar el mensaje antes de esconderlo protege el contenido aunque se detecte el portador.

## 🧰 Herramientas y preparación

```bash
pip install pillow numpy
# herramientas dedicadas (opcional)
which steghide zsteg stegseek 2>/dev/null || echo "opcional para el lab"
```

Usa imágenes y archivos generados por ti. No manipules material ajeno.

## 🧪 Laboratorio guiado

1. **Oculta un mensaje con LSB en Python**:

   ```python
   from PIL import Image
   img = Image.open("cover.png").convert("RGB")
   px = img.load()
   msg = "secreto".encode() + b"\x00"
   bits = ''.join(f"{b:08b}" for b in msg)
   i = 0
   for y in range(img.height):
       for x in range(img.width):
           if i < len(bits):
               r, g, b = px[x, y]
               r = (r & ~1) | int(bits[i]); i += 1
               px[x, y] = (r, g, b)
   img.save("stego.png")
   ```

2. **Extrae el mensaje** leyendo el LSB del canal rojo hasta el terminador `\x00`.

3. **Cifra antes de ocultar**. Cifra el mensaje con AES-GCM (clase 059) y luego escóndelo; ahora, aunque se detecte el portador, el contenido permanece protegido.

4. **Estegoanálisis**. Compara histogramas o aplica una prueba chi-cuadrado entre `cover.png` y `stego.png`; observa las anomalías que delatan la manipulación LSB. Prueba herramientas como `zsteg`/`stegseek` sobre tus propios archivos.

5. **Discusión defensiva**. Analiza cómo un atacante podría usar imágenes en un foro para C2 encubierto y qué señales buscaría un defensor (tamaños anómalos, entropía, tráfico a imágenes).

## ✍️ Ejercicios

1. Explica la diferencia entre esteganografía y cifrado con un ejemplo.
2. Oculta y recupera un mensaje LSB en una imagen propia.
3. Aplica una prueba estadística para detectar tu propio stego object.
4. Cifra un mensaje y ocúltalo; razona qué protege cada capa.
5. Investiga un caso real de malware que usó esteganografía.
6. Compara capacidad e imperceptibilidad de LSB en PNG vs JPEG.

## 📝 Reto verificable

Implementa una herramienta que cifre un mensaje con AES-GCM y lo oculte por LSB en una imagen, más un extractor que recupere y descifre el mensaje. **Criterio de aceptación**: el mensaje se recupera intacto solo con la clave correcta, la imagen resultante es visualmente idéntica al portador, y describes qué señal estadística podría delatar la ocultación.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| El mensaje oculto se pierde | Recompresión JPEG destruye LSB; usa formatos sin pérdida (PNG) |
| Confiar solo en la ocultación | Si se detecta, se lee; cifra antes de ocultar |
| Portador visiblemente alterado | Demasiada carga; reduce la capacidad |
| Estego detectable trivialmente | Patrón LSB uniforme; distribuye o usa técnicas robustas |
| Usar estego para evadir controles sin permiso | Ilegal; limítate a laboratorio propio |

## ❓ Preguntas frecuentes

**❓ ¿La esteganografía sustituye al cifrado?**
No; oculta la existencia, no el contenido. Combínala con cifrado para defensa en profundidad.

**❓ ¿Es fácil detectar LSB?**
Sí, con análisis estadístico. La esteganografía robusta es un campo activo; LSB simple es didáctico pero detectable.

**❓ ¿Para qué sirve legítimamente?**
Marcas de agua, trazabilidad de filtraciones, autenticación de contenido y ocultación de metadatos sensibles.

## 🔗 Referencias

- Aumasson, *Serious Cryptography* (contexto de ocultación y aleatoriedad).
- Fridrich, *Steganography in Digital Media* (referencia académica).
- Provos & Honeyman, "Hide and Seek: An Introduction to Steganography".
- Herramientas: steghide, zsteg, stegseek (documentación oficial).

## ➡️ Siguiente clase

[Clase 065 - Implementaciones seguras y errores criptograficos comunes](../065-implementaciones-seguras-y-errores-criptograficos-comunes/README.md)
