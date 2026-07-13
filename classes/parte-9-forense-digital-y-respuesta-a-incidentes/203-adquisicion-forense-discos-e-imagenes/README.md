# Clase 203 — Adquisición forense: discos e imágenes

> Parte: **9 — Forense digital y respuesta a incidentes** · Fuente: *Brian Carrier — File System Forensic Analysis* y *NIST SP 800-86*
> ⏱️ Duración estimada: **120 min** · Nivel: **Intermedio**

---

## 🎯 Objetivo

Aprender a adquirir imágenes forenses de discos y memoria de forma verificable y sin alterar el original. Al terminar sabrás elegir entre adquisición física y lógica, usar formatos como RAW (dd) y E01, aplicar bloqueo de escritura y verificar integridad con hashes antes y después.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Diferenciar** adquisición física, lógica y de volumen.
2. **Crear** imágenes con `dd`, `dcfldd`, `ewfacquire` y FTK Imager.
3. **Aplicar** bloqueo de escritura por hardware o software.
4. **Verificar** integridad con hashes durante y tras la adquisición.
5. **Elegir** el formato adecuado (RAW vs. E01/EWF) según el caso.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Física vs. lógica vs. volumen | Define qué datos capturas |
| 2 | Formatos RAW y E01/EWF | Compresión, metadatos e integridad |
| 3 | Bloqueo de escritura | Preserva el original |
| 4 | `dd` y `dcfldd` | Adquisición base en Linux |
| 5 | `ewfacquire` y FTK Imager | Formato forense con verificación |
| 6 | Hashing durante adquisición | Prueba de no alteración |
| 7 | Adquisición en vivo vs. apagado | Decisión bajo orden de volatilidad |
| 8 | Discos cifrados y SSD/TRIM | Retos modernos de adquisición |

## 📖 Definiciones y características

- **Adquisición física**: copia bit a bit de todo el medio, incluido espacio no asignado. Característica: recupera datos borrados.
- **Adquisición lógica**: copia de archivos y estructuras vivas. Característica: más rápida pero omite lo borrado.
- **Formato RAW (dd)**: copia cruda sin metadatos. Característica: universal pero sin verificación embebida.
- **Formato E01 (EWF)**: EnCase Evidence Format con compresión, metadatos del caso y hash integrado. Característica: verifica integridad por sí mismo.
- **Write blocker**: dispositivo que impide escritura en el original. Característica: hardware es el estándar de oro.
- **Espacio no asignado (unallocated)**: sectores sin archivo vivo asignado. Característica: fuente de datos borrados y carving.
- **TRIM en SSD**: el disco borra físicamente bloques marcados como libres. Característica: dificulta recuperar borrados en SSD.

## 🧰 Herramientas y preparación

- **Linux**: `dd`, `dcfldd`, `ewfacquire` (paquete `libewf-tools`), `hashdeep`.
- **Windows**: **FTK Imager** (gratuito, de Exterro/AccessData) para crear imágenes E01 con verificación.
- **Hardware simulado**: usa un pendrive propio o un archivo `.img` como "disco". Nunca practiques sobre medios de terceros sin autorización.
- **Recuerda**: laboratorio aislado, evidencia propia, y bloqueo de escritura siempre que toques un original.

## 🧪 Laboratorio guiado

> Usa un pendrive PROPIO o un archivo imagen que tú creas. Nunca medios ajenos sin permiso escrito.

1. Identifica el dispositivo (en Linux) sin montarlo:

   ```bash
   lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
   ```

2. Monta el original en solo lectura si necesitas inspeccionarlo (simula write-blocker por software):

   ```bash
   blockdev --setro /dev/sdX
   ```

3. Adquiere con `dcfldd` calculando hash al vuelo:

   ```bash
   dcfldd if=/dev/sdX of=caso001.dd hash=sha256 hashlog=caso001.hashlog bs=4M
   ```

4. Alternativa en formato forense E01:

   ```bash
   ewfacquire /dev/sdX
   ```

   Rellena caso, examinador y notas cuando lo pida.
5. Verifica la imagen RAW contra el original:

   ```bash
   sha256sum caso001.dd
   cat caso001.hashlog
   ```

6. Verifica una imagen E01:

   ```bash
   ewfverify caso001.E01
   ```

7. En Windows, repite con **FTK Imager**: `Create Disk Image → Physical Drive → E01`, activa verificación y compara los hashes que reporta al terminar.
8. Documenta en la cadena de custodia: dispositivo, método, hashes y hora UTC.

## ✍️ Ejercicios

1. Explica cuándo elegirías adquisición lógica en vez de física.
2. Compara RAW y E01 en una tabla de ventajas/desventajas.
3. Adquiere un pendrive propio en ambos formatos y compara tamaños.
4. Investiga cómo un write-blocker de hardware difiere de `blockdev --setro`.
5. Explica por qué el TRIM de un SSD complica la recuperación de borrados.
6. Diseña el procedimiento para adquirir un servidor que no se puede apagar.

## 📝 Reto verificable

Adquiere una imagen forense de un pendrive propio en formato E01 con FTK Imager o `ewfacquire`, y demuestra que la imagen es fiel al original comparando hashes.

**Criterio de aceptación**: entregas la imagen E01, el log de adquisición y la salida de `ewfverify` (o el reporte de FTK) mostrando que el hash de adquisición coincide con el de verificación. La cadena de custodia acompaña el entregable.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| El SO monta el disco automáticamente | Automount activo alteró tiempos de acceso. Desactiva automount o usa write-blocker antes de conectar. |
| `dd` sin `bs` tarda horas | Bloque por defecto minúsculo. Usa `bs=4M`. |
| Hash de adquisición ≠ verificación | El original cambió o hubo error de lectura. Repite con bloqueo de escritura. |
| Imagen RAW enorme | RAW no comprime. Usa E01 si el espacio importa. |
| `ewfacquire: permission denied` | Falta privilegio de lectura del dispositivo. Ejecuta con `sudo`. |

## ❓ Preguntas frecuentes

**❓ ¿RAW o E01?**
E01 para casos formales (metadatos + integridad integrada); RAW para máxima compatibilidad con herramientas.

**❓ ¿Puedo adquirir un equipo encendido?**
Sí, es adquisición en vivo. Captura primero la RAM (más volátil) y documenta que el sistema estaba activo.

**❓ ¿El bloqueo por software basta?**
Para prácticas sí; en casos legales serios se prefiere un write-blocker de hardware certificado.

**❓ ¿Por qué mi SSD no recupera borrados?**
Por TRIM: el controlador borra físicamente bloques liberados, a veces en segundos.

## 🔗 Referencias

- Carrier, B. — *File System Forensic Analysis*, Addison-Wesley 2005.
- NIST SP 800-86: <https://csrc.nist.gov/publications/detail/sp/800-86/final>
- FTK Imager (Exterro): <https://www.exterro.com/ftk-imager>
- libewf / ewf-tools: <https://github.com/libyal/libewf>

## ➡️ Siguiente clase

[Clase 204 - Forense de sistemas de archivos: NTFS y ext4](../204-forense-de-sistemas-de-archivos-ntfs-y-ext4/README.md)
