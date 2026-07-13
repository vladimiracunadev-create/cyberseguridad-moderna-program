# Lab: DFIR — Forense de memoria y malware

Estación de análisis para las clases **207** (Volatility), **325** (forense de memoria
avanzado) y **326** (malware para respuesta a incidentes). Prepara la práctica de
certificaciones **SANS GCFA/GCIH** y **BTL1**.

> ⚠️ **Solo laboratorio.** Las muestras de memoria que analizarás contienen malware real
> capturado. Trabaja siempre dentro del contenedor/VM aislada; nunca ejecutes binarios
> extraídos fuera de un entorno controlado.

## 🎯 Qué vas a practicar

| Objetivo | Clases |
|---|---|
| Enumerar procesos y detectar anomalías | [207](../../classes/parte-9-forense-digital-y-respuesta-a-incidentes/207-forense-de-memoria-ram-con-volatility/README.md), [325](../../classes/parte-17-profundizacion-para-certificaciones/325-forense-de-memoria-avanzado/README.md) |
| Detectar inyección de código y ocultamiento | [325](../../classes/parte-17-profundizacion-para-certificaciones/325-forense-de-memoria-avanzado/README.md) |
| Extraer IOCs para el informe de incidente | [326](../../classes/parte-17-profundizacion-para-certificaciones/326-analisis-de-malware-para-respuesta-a-incidentes/README.md) |

## 🧰 Levantar la estación

```bash
cd labs/dfir-memoria
docker compose build          # instala Volatility 3 + YARA (tarda la primera vez)
docker compose up -d
docker compose exec analista bash
```

## 📥 Conseguir una muestra de memoria (pública)

El repo **no** incluye la imagen (pesa cientos de MB). Descarga una muestra pública y
colócala en `labs/dfir-memoria/cases/` (se monta en `/cases`):

- **MemLabs** — retos de forense de memoria con imágenes de Windows: <https://github.com/stuxnet999/MemLabs>
- **Volatility Foundation — sample images** (cridex, zeus, stuxnet…): <https://github.com/volatilityfoundation/volatility/wiki/Memory-Samples>
- **AboutDFIR — listado de imágenes de práctica**: <https://aboutdfir.com/toolsandartifacts/windows/memory-images/>

Verifica el hash de lo que descargues y trátalo como potencialmente malicioso.

## 🧭 Recorrido guiado (dentro del contenedor)

Sustituye `imagen.raw` por tu muestra en `/cases`.

```bash
# 1. Identificar el sistema y listar procesos
vol -f /cases/imagen.raw windows.info
vol -f /cases/imagen.raw windows.pslist
vol -f /cases/imagen.raw windows.pstree        # relaciones padre-hijo (procesos huérfanos)

# 2. Buscar inyección de código / código oculto
vol -f /cases/imagen.raw windows.malfind       # regiones RWX inyectadas
vol -f /cases/imagen.raw windows.ldrmodules    # DLLs no enlazadas (ocultamiento)

# 3. Red y persistencia
vol -f /cases/imagen.raw windows.netscan       # conexiones y puertos (posible C2)
vol -f /cases/imagen.raw windows.cmdline       # líneas de comando sospechosas

# 4. Volcar y escanear un proceso sospechoso
vol -f /cases/imagen.raw windows.dumpfiles --pid <PID>
vol -f /cases/imagen.raw yarascan.YaraScan --yara-rules "malware"
```

## 🏆 Retos verificables

1. **Proceso malicioso:** identifica el proceso inyectado (PID, nombre, padre). *Aceptación:* `malfind` muestra una región RWX con código y lo correlacionas con un proceso anómalo en `pstree`.
2. **C2:** extrae la IP/puerto de comando y control desde `netscan`. *Aceptación:* la conexión sale de un proceso sospechoso.
3. **IOCs para el informe:** entrega una tabla de IOCs (hashes, IPs, rutas, mutex) lista para un informe DFIR. *Aceptación:* mínimo 5 IOCs con su fuente (plugin) — enlaza con la clase 326.
4. **Timeline:** ubica el compromiso en una línea de tiempo aproximada con las evidencias.

## 🧯 Apagar

```bash
docker compose down
```

## 🔗 Referencias

- Ligh, Case, Levy, Walters — *The Art of Memory Forensics*.
- [Volatility 3 — documentación](https://volatility3.readthedocs.io/)
- SANS FOR508 · [MITRE ATT&CK — Process Injection (T1055)](https://attack.mitre.org/techniques/T1055/)
- Parte 9 y Parte 17 del programa — [índice de clases](../../classes/README.md)
