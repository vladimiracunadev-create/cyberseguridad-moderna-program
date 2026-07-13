# Clase 205 — Análisis de artefactos de Windows

> Parte: **9 — Forense digital y respuesta a incidentes** · Fuente: *SANS FOR500 — Windows Forensic Analysis* y documentación de Microsoft
> ⏱️ Duración estimada: **130 min** · Nivel: **Avanzado**

---

## 🎯 Objetivo

Aprender a extraer e interpretar los artefactos que Windows deja de la actividad del usuario y del sistema: registro (hives), Prefetch, ShimCache/AmCache, Jump Lists, LNK, Event Logs y ShellBags. Al terminar podrás responder "quién ejecutó qué, cuándo y desde dónde" en un equipo Windows.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Localizar y extraer** los hives del registro y los principales artefactos.
2. **Interpretar** Prefetch, ShimCache y AmCache como evidencia de ejecución.
3. **Analizar** Event Logs para autenticación y creación de procesos.
4. **Reconstruir** actividad de usuario con Jump Lists, LNK y ShellBags.
5. **Usar** las herramientas de Eric Zimmerman y RegRipper.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Hives del registro | Configuración y rastros de uso |
| 2 | Prefetch | Prueba de ejecución de programas |
| 3 | ShimCache / AmCache | Ejecución incluso sin Prefetch |
| 4 | Event Logs (EVTX) | Autenticación y procesos |
| 5 | Jump Lists y LNK | Archivos y rutas accedidas |
| 6 | ShellBags | Carpetas navegadas |
| 7 | UserAssist / RecentDocs | Programas y documentos recientes |
| 8 | Herramientas EZ y RegRipper | Automatizan el parseo |

## 📖 Definiciones y características

- **Hive del registro**: archivo binario (SYSTEM, SOFTWARE, NTUSER.DAT…) con configuración y rastros. Característica: NTUSER.DAT es por usuario.
- **Prefetch**: archivos `.pf` en `C:\Windows\Prefetch` que aceleran arranque de apps. Característica: registran nombre, conteo y última ejecución.
- **ShimCache (AppCompatCache)**: caché de compatibilidad en el hive SYSTEM. Característica: evidencia de ejecución/presencia, orden no siempre cronológico.
- **AmCache.hve**: hive con hashes SHA-1 y rutas de ejecutables. Característica: útil para identificar binarios maliciosos.
- **Event Log 4624/4625**: inicio de sesión exitoso/fallido. Característica: base del análisis de autenticación.
- **Jump List**: historial de archivos por aplicación en la barra de tareas. Característica: revela archivos abiertos recientemente.
- **ShellBags**: preferencias de vista de carpetas en el registro. Característica: prueban que una carpeta fue navegada, incluso si ya no existe.

## 🧰 Herramientas y preparación

- **Eric Zimmerman's Tools**: `PECmd` (Prefetch), `AppCompatCacheParser`, `AmcacheParser`, `JLECmd`, `LECmd`, `SBECmd`, `EvtxECmd`, `Registry Explorer`.
- **RegRipper**: parseo masivo de hives.
- **Extracción**: FTK Imager o KAPE para volcar los artefactos de una imagen montada en solo lectura.
- **Entorno**: usa una imagen de una VM Windows PROPIA donde tú generaste la actividad.

## 🧪 Laboratorio guiado

> Genera la actividad tú mismo en una VM Windows propia, luego analiza sus artefactos.

1. Con KAPE o FTK Imager, extrae de la imagen: `C:\Windows\Prefetch`, hives `SYSTEM`/`SOFTWARE`/`NTUSER.DAT`, `Amcache.hve` y `C:\Windows\System32\winevt\Logs`.
2. Analiza Prefetch:

   ```bash
   PECmd.exe -d Prefetch --csv salida --csvf prefetch.csv
   ```

3. Parsea ShimCache:

   ```bash
   AppCompatCacheParser.exe -f SYSTEM --csv salida
   ```

4. Parsea AmCache:

   ```bash
   AmcacheParser.exe -f Amcache.hve --csv salida
   ```

5. Analiza inicios de sesión en los Event Logs:

   ```bash
   EvtxECmd.exe -d Logs --csv salida --csvf events.csv
   ```

   Filtra los IDs 4624 (login), 4625 (fallo), 4688 (creación de proceso).
6. Reconstruye actividad de usuario:

   ```bash
   JLECmd.exe -d "AutomaticDestinations" --csv salida
   SBECmd.exe -d "C:\ruta\hives" --csv salida
   ```

7. Correlaciona: cruza una ejecución de Prefetch con un evento 4688 y un LNK para contar la historia completa de un programa ejecutado.

## ✍️ Ejercicios

1. Explica qué prueba (y qué no) un archivo Prefetch.
2. Diferencia ShimCache de AmCache y di cuándo usar cada uno.
3. Lista cinco Event IDs clave y su significado.
4. Analiza una Jump List propia y di qué archivos abriste.
5. Demuestra con ShellBags que navegaste una carpeta ya borrada.
6. Cruza tres artefactos para probar la ejecución de un binario concreto.

## 📝 Reto verificable

En una VM Windows propia, ejecuta un binario "sospechoso" inofensivo (por ejemplo, una copia renombrada de `calc.exe` en una carpeta rara), luego demuestra su ejecución cruzando al menos tres artefactos independientes.

**Criterio de aceptación**: presentas evidencia de al menos tres fuentes distintas (Prefetch, ShimCache/AmCache, Event 4688, LNK…) que coinciden en nombre, ruta y ventana temporal del binario, con una conclusión escrita.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| No hay Prefetch | Prefetch deshabilitado (común en servidores/SSD). Usa ShimCache/AmCache. |
| ShimCache "desordenada" | Su orden no es estrictamente cronológico. No infieras tiempos exactos de ahí. |
| Event Logs vacíos | Rotación o borrado. Busca en backups o en SIEM. |
| Registry Explorer no abre el hive | Hive en uso o corrupto. Extrae la copia offline de la imagen. |
| Timestamps en hora local confusa | Convierte todo a UTC con la zona horaria del sistema (hive SYSTEM). |

## ❓ Preguntas frecuentes

**❓ ¿Prefetch prueba ejecución?**
Sí: su existencia indica que el programa se ejecutó, con conteo y última fecha. Ausencia no prueba lo contrario.

**❓ ¿AmCache tiene hashes?**
Sí, SHA-1 de ejecutables, muy útil para contrastar contra inteligencia de amenazas.

**❓ ¿Qué hive tiene la actividad del usuario?**
NTUSER.DAT (por perfil) y UsrClass.dat (ShellBags). SYSTEM/SOFTWARE son de máquina.

**❓ ¿Puedo confiar en los ShellBags?**
Sí para probar navegación de carpetas; recuerda que persisten aunque la carpeta ya no exista.

## 🔗 Referencias

- Eric Zimmerman's Tools: <https://ericzimmerman.github.io/>
- RegRipper: <https://github.com/keydet89/RegRipper3.0>
- SANS — Windows Forensic Analysis poster (FOR500): <https://www.sans.org/posters/>
- Microsoft — Windows event IDs: <https://learn.microsoft.com/windows/security/threat-protection/auditing/>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-205-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-205-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 206 - Analisis de artefactos de Linux](../206-analisis-de-artefactos-de-linux/README.md)
