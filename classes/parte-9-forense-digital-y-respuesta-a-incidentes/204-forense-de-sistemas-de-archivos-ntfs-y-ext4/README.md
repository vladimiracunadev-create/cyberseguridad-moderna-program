# Clase 204 — Forense de sistemas de archivos: NTFS y ext4

> Parte: **9 — Forense digital y respuesta a incidentes** · Fuente: *Brian Carrier — File System Forensic Analysis*
> ⏱️ Duración estimada: **130 min** · Nivel: **Avanzado**

---

## 🎯 Objetivo

Entender la anatomía interna de NTFS y ext4 al nivel que permite hacer forense real: la MFT y sus atributos, marcas de tiempo, el `$LogFile` y `$UsnJrnl` en NTFS; inodos, journal y timestamps en ext4. Al terminar podrás reconstruir la historia de un archivo aunque haya sido borrado o manipulado.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Explicar** la estructura de la MFT y sus atributos clave.
2. **Interpretar** los timestamps MACB en NTFS y ext4.
3. **Recuperar** archivos borrados a partir de metadatos residuales.
4. **Analizar** el `$UsnJrnl` y el journal de ext4 para reconstruir cambios.
5. **Usar** The Sleuth Kit para recorrer un sistema de archivos.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | MFT y registros de archivo | Corazón de NTFS |
| 2 | Atributos `$STANDARD_INFORMATION` y `$FILE_NAME` | Dos juegos de timestamps |
| 3 | Timestamps MACB | Reconstruyen actividad |
| 4 | `$LogFile` y `$UsnJrnl` | Historial de cambios NTFS |
| 5 | Inodos y bloques en ext4 | Corazón de ext4 |
| 6 | Journal de ext4 (jbd2) | Cambios recientes |
| 7 | Archivos borrados y residuos | Recuperación de metadatos |
| 8 | The Sleuth Kit | Herramienta de análisis |

## 📖 Definiciones y características

- **MFT (Master File Table)**: base de datos de NTFS donde cada archivo tiene un registro. Característica: incluso los archivos pequeños viven dentro de la MFT (residentes).
- **`$STANDARD_INFORMATION`**: atributo con timestamps que el usuario puede modificar fácilmente. Característica: manipulable por *timestomping*.
- **`$FILE_NAME`**: atributo con timestamps que solo el kernel actualiza. Característica: útil para detectar manipulación de tiempos.
- **MACB**: Modified, Accessed, Changed/Created, Born. Característica: cuatro marcas que permiten ordenar eventos.
- **`$UsnJrnl`**: Update Sequence Number Journal, registra cambios en archivos. Característica: revela creaciones/borrados recientes.
- **Inodo (ext4)**: estructura con metadatos y punteros a bloques de datos. Característica: al borrar, ext4 suele limpiar punteros (dificulta recuperar).
- **Journal (jbd2)**: registro de transacciones de ext4. Característica: puede conservar metadatos ya sobrescritos.

## 🧰 Herramientas y preparación

- **The Sleuth Kit (TSK)**: `fls`, `istat`, `icat`, `mmls`, `fsstat`, `mactime`.
- **NTFS específico**: `analyzeMFT.py`, `MFTECmd` (Eric Zimmerman), `UsnJrnl2Csv`.
- **ext4**: `debugfs`, `extundelete`.
- **Entorno**: monta las imágenes en solo lectura. Trabaja sobre imágenes propias creadas en la clase anterior.

## 🧪 Laboratorio guiado

> Usa una imagen `.dd` propia (por ejemplo de un pendrive formateado en NTFS y otro en ext4).

1. Examina la tabla de particiones:

   ```bash
   mmls caso001.dd
   ```

2. Muestra estadísticas del sistema de archivos:

   ```bash
   fsstat -o 2048 caso001.dd
   ```

3. Lista archivos incluyendo borrados (marcados con `*`):

   ```bash
   fls -r -o 2048 caso001.dd
   ```

4. Inspecciona un inodo/registro MFT concreto:

   ```bash
   istat -o 2048 caso001.dd 128
   ```

5. Recupera el contenido de un archivo por su inodo:

   ```bash
   icat -o 2048 caso001.dd 128 > recuperado.bin
   ```

6. Genera una línea de tiempo del sistema de archivos:

   ```bash
   fls -r -m C: -o 2048 caso001.dd > bodyfile.txt
   mactime -b bodyfile.txt -d > timeline.csv
   ```

7. En NTFS, extrae y parsea la MFT con MFTECmd:

   ```bash
   MFTECmd.exe -f "$MFT" --csv salida --csvf mft.csv
   ```

   Compara los timestamps de `$STANDARD_INFORMATION` y `$FILE_NAME` para detectar *timestomping*.
8. En ext4, explora con `debugfs`:

   ```bash
   debugfs -R "stat <2>" imagen_ext4.dd
   ```

## ✍️ Ejercicios

1. Explica la diferencia entre timestamps residentes y no residentes en la MFT.
2. Detecta *timestomping* comparando `$SI` y `$FN` en una MFT de ejemplo.
3. Recupera un archivo borrado propio con `icat` y verifica su contenido.
4. Interpreta el significado de cada letra en MACB con un ejemplo.
5. Usa `debugfs` para listar los inodos borrados de una imagen ext4.
6. Compara cómo NTFS y ext4 manejan el borrado de un archivo.

## 📝 Reto verificable

A partir de una imagen NTFS propia donde borraste un archivo y le manipulaste los tiempos, demuestra con evidencia de la MFT que hubo *timestomping* y recupera el contenido original del archivo borrado.

**Criterio de aceptación**: presentas (a) el archivo recuperado con `icat`, (b) una comparación `$SI` vs `$FN` que muestra la incoherencia de timestamps, y (c) una explicación de por qué esa incoherencia indica manipulación.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| `fls` no muestra offset correcto | Falta `-o` con el sector de inicio de la partición. Sácalo de `mmls`. |
| `icat` devuelve datos basura | El inodo fue reasignado; los bloques ya se sobrescribieron. |
| Timestamps "imposibles" (futuro) | Timestomping o reloj alterado. Contrasta con `$FN`. |
| `extundelete` no recupera nada | ext4 limpió los punteros del inodo. Prueba carving (clase 214). |
| MFTECmd no encuentra `$MFT` | Debes extraer `$MFT` con FTK Imager primero. |

## ❓ Preguntas frecuentes

**❓ ¿Por qué hay dos juegos de timestamps en NTFS?**
`$STANDARD_INFORMATION` lo actualizan apps y usuarios; `$FILE_NAME` solo el kernel. Compararlos delata manipulación.

**❓ ¿ext4 conserva archivos borrados?**
Menos que NTFS: suele limpiar los punteros del inodo. A veces el journal ayuda, y siempre queda el carving.

**❓ ¿Qué es un archivo residente?**
Uno tan pequeño que sus datos caben dentro del propio registro de la MFT, sin ocupar clusters aparte.

**❓ ¿El `$UsnJrnl` está siempre activo?**
En Windows moderno normalmente sí. Es una fuente riquísima de creaciones, renombres y borrados recientes.

## 🔗 Referencias

- Carrier, B. — *File System Forensic Analysis*, Addison-Wesley 2005.
- The Sleuth Kit: <https://www.sleuthkit.org/>
- Eric Zimmerman's Tools (MFTECmd): <https://ericzimmerman.github.io/>
- Microsoft — NTFS documentation: <https://learn.microsoft.com/windows-server/storage/file-server/ntfs-overview>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-204-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-204-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 205 - Analisis de artefactos de Windows](../205-analisis-de-artefactos-de-windows/README.md)
