# Clase 214 — Recuperación de datos y file carving

> Parte: **9 — Forense digital y respuesta a incidentes** · Fuente: *Brian Carrier — File System Forensic Analysis*
> ⏱️ Duración estimada: **120 min** · Nivel: **Avanzado**

---

## 🎯 Objetivo

Aprender a recuperar archivos borrados incluso cuando el sistema de archivos ya no los referencia, mediante **file carving**: reconstruir archivos a partir de sus firmas (headers/footers) en el espacio no asignado. Al terminar sabrás usar PhotoRec, Scalpel, foremost y bulk_extractor para rescatar evidencia perdida.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Diferenciar** recuperación por metadatos y recuperación por carving.
2. **Aplicar** carving con PhotoRec, foremost y Scalpel.
3. **Reconocer** las firmas (magic numbers) de formatos comunes.
4. **Extraer** artefactos con bulk_extractor.
5. **Evaluar** las limitaciones del carving (fragmentación, falsos positivos).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Borrado vs. destrucción | Qué se puede recuperar |
| 2 | Recuperación por metadatos | La vía rápida cuando existe |
| 3 | File carving por firmas | Cuando no hay metadatos |
| 4 | Magic numbers | Cómo se reconocen los archivos |
| 5 | PhotoRec / foremost / Scalpel | Herramientas de carving |
| 6 | Fragmentación | El gran enemigo del carving |
| 7 | bulk_extractor | Extraer artefactos a granel |
| 8 | Validación de recuperados | Evitar falsos positivos |

## 📖 Definiciones y características

- **Recuperación por metadatos**: usar el inodo/MFT residual para rescatar el archivo. Característica: rápida y fiable si los punteros sobreviven.
- **File carving**: reconstruir archivos por sus firmas, ignorando el FS. Característica: funciona sin metadatos, pero sufre con la fragmentación.
- **Magic number / firma**: bytes iniciales (y a veces finales) que identifican un formato (`FFD8` JPEG, `%PDF` PDF, `PK` ZIP). Característica: base del carving.
- **Header/footer carving**: extraer entre una firma de inicio y una de fin. Característica: falla si el archivo está fragmentado.
- **Fragmentación**: archivo disperso en clusters no contiguos. Característica: el carving simple lo reconstruye mal.
- **bulk_extractor**: extrae emails, tarjetas, URLs, etc. sin parsear el FS. Característica: veloz y útil para triage.
- **Falso positivo**: dato "recuperado" que no es un archivo válido. Característica: hay que validar cada recuperado.

## 🧰 Herramientas y preparación

- **Carving**: `photorec`, `foremost`, `scalpel`.
- **Triage**: `bulk_extractor`.
- **Metadatos**: The Sleuth Kit (`icat`, `fls -d`), `extundelete` (ext4), `testdisk` (particiones).
- **Entrada**: una imagen `.dd` propia donde borraste archivos a propósito.

## 🧪 Laboratorio guiado

> Usa una imagen propia donde tú borraste archivos conocidos (para verificar la recuperación).

1. Primero intenta recuperación por metadatos con TSK:
   ```bash
   fls -d -r -o 2048 imagen.dd        # lista borrados
   icat -o 2048 imagen.dd 512 > recuperado_meta.bin
   ```
2. Si no hay metadatos, aplica carving con foremost:
   ```bash
   foremost -t jpg,pdf,doc,zip -i imagen.dd -o salida_foremost
   ```
3. Prueba PhotoRec (interactivo, muy potente para imágenes):
   ```bash
   photorec imagen.dd
   ```
4. Usa Scalpel con su archivo de configuración de firmas:
   ```bash
   scalpel -c /etc/scalpel/scalpel.conf -o salida_scalpel imagen.dd
   ```
5. Ejecuta bulk_extractor para triage rápido:
   ```bash
   bulk_extractor -o salida_bulk imagen.dd
   ```
   Revisa `email.txt`, `url.txt`, `ccn.txt`.
6. **Valida** cada archivo recuperado: ábrelo, verifica su firma y compara su hash con el original que borraste. Descarta falsos positivos.
7. Documenta qué recuperó cada herramienta y por qué unas funcionaron mejor (fragmentación, tipo de archivo).

## ✍️ Ejercicios

1. Explica cuándo prefieres metadatos y cuándo carving.
2. Identifica las firmas de JPEG, PDF y ZIP en un editor hex.
3. Recupera imágenes borradas propias con PhotoRec y valídalas.
4. Compara los resultados de foremost y Scalpel sobre la misma imagen.
5. Extrae correos y URLs con bulk_extractor.
6. Explica por qué la fragmentación arruina el carving simple.

## 📝 Reto verificable

Borra cinco archivos conocidos (de tipos distintos) de una imagen propia, recupéralos por carving y demuestra —comparando hashes— cuáles se recuperaron íntegros y cuáles no, explicando la causa.

**Criterio de aceptación**: entregas los archivos recuperados, una tabla con hash original vs. hash recuperado por cada uno, y una explicación de por qué los que fallaron no coincidieron (fragmentación, sobrescritura o formato).

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Muchos archivos corruptos | Fragmentación; el carving por firmas no la maneja. Prueba PhotoRec con validación. |
| Falsos positivos abundantes | Firmas genéricas. Valida cada recuperado por su estructura. |
| No recupera nada | Espacio ya sobrescrito o SSD con TRIM. Busca en otras fuentes. |
| foremost trunca archivos | Tamaño máximo por defecto. Ajusta la config de tipos. |
| bulk_extractor tarda mucho | Imagen grande. Es normal; corre en background. |

## ❓ Preguntas frecuentes

**❓ ¿Metadatos o carving primero?**
Metadatos primero (más fiable y rápido). Carving cuando el FS ya no referencia el archivo.

**❓ ¿Por qué falla el carving con archivos grandes?**
Porque suelen estar fragmentados, y el carving por header/footer asume contigüidad.

**❓ ¿Qué recupera bulk_extractor?**
Artefactos como emails, URLs, números de tarjeta y dominios, sin necesidad de parsear el sistema de archivos. Ideal para triage.

**❓ ¿Cómo sé si un recuperado es válido?**
Ábrelo, verifica su firma/estructura y, si tienes el original, compara hashes. No confíes solo en la extensión.

## 🔗 Referencias

- Carrier, B. — *File System Forensic Analysis*, Addison-Wesley 2005.
- PhotoRec / TestDisk: https://www.cgsecurity.org/wiki/PhotoRec
- foremost / Scalpel: https://foremost.sourceforge.net/
- bulk_extractor: https://github.com/simsong/bulk_extractor

## ➡️ Siguiente clase

[Clase 215 - Playbooks de respuesta a incidentes](../215-playbooks-de-respuesta-a-incidentes/README.md)
