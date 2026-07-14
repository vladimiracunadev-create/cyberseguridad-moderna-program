# Lab: Triaje forense de Windows con RootCause

Laboratorio de **respuesta en vivo (live response)** y **diagnóstico de causa raíz** en Windows
usando **[RootCause Windows Inspector](https://github.com/vladimiracunadev-create/rootcause-windows-inspector)**
— un sensor forense de comportamiento escrito en **Rust** (licencia **Apache-2.0**). Complementa
las clases de **Blue Team** (Parte 8), **DFIR** (Parte 9) y **análisis de comportamiento** (Parte 6).

> 🛠️ **Herramienta del propio autor del programa** (proyecto de código abierto, Apache-2.0). Este
> lab la **usa y referencia**; consulta el repositorio oficial para la documentación, la
> descarga y la licencia.
>
> ℹ️ **Qué es (y qué no).** RootCause es un **sensor forense y de apoyo a la decisión**: detecta
> **indicios de comportamiento anómalo** (persistencia, tráfico saliente inusual, ejecución en
> rutas sospechosas, escritura agresiva tipo ransomware, cryptojacking, degradación de recursos)
> y **explica la causa raíz con evidencia**. **No** es un antivirus ni un EDR: no elimina malware
> ni bloquea por firma — **complementa** a tu AV/EDR indicando *dónde mirar*.

## 🎯 Qué vas a practicar

| Objetivo | Clases |
|---|---|
| Entender arquitectura, procesos y servicios de Windows | [008](../../classes/parte-0-fundamentos-y-prerrequisitos/008-windows-esencial-para-seguridad-arquitectura-registro-y-servicios/README.md) |
| Análisis de comportamiento de un proceso sospechoso | [148](../../classes/parte-6-analisis-de-malware/148-analisis-de-comportamiento/README.md) |
| Endpoint y detección (complemento a EDR) | [189](../../classes/parte-8-blue-team-deteccion-y-soc/189-analisis-de-endpoints-con-edr/README.md) |
| Artefactos de Windows y respuesta en vivo | [205](../../classes/parte-9-forense-digital-y-respuesta-a-incidentes/205-analisis-de-artefactos-de-windows/README.md) |

## 🧰 Requisitos

- **Windows 10/11** (idealmente una **VM propia** de laboratorio; algunas funciones piden admin).
- Para compilar desde fuente: **Rust** (edición 2024) y, para captura de evidencia, **WPR/ETW**
  (incluido en Windows). Alternativamente, usa un **release** publicado del proyecto.

> ⚠️ **Solo en equipos propios/autorizados.** Un sensor forense observa el sistema en detalle;
> ejecútalo únicamente en máquinas tuyas o con autorización.

## 🚀 Obtener y ejecutar RootCause

Desde el repositorio oficial (ver su README para los pasos exactos):

```powershell
git clone https://github.com/vladimiracunadev-create/rootcause-windows-inspector.git
cd rootcause-windows-inspector
cargo build --release
.\target\release\rootcause.exe        # algunas funciones requieren administrador
```

O descarga el ZIP portable / instalador desde los *releases* del proyecto.

## 🧭 Recorrido guiado

> Trabaja en tu **VM de Windows**. Idea: generar "ruido" controlado y usar RootCause para
> localizar la causa raíz, como en una respuesta en vivo.

1. **Línea base.** Abre RootCause y observa el semáforo de estado, los sparklines de CPU/RAM/IO y el top de procesos en reposo.
2. **Genera una anomalía de recursos.** Lanza un proceso que escriba mucho en disco o consuma CPU (un script propio) y observa cómo RootCause lo destaca por severidad y tendencia.
3. **Correlación proceso ↔ servicio ↔ red.** Identifica qué proceso mantiene conexiones salientes y a qué servicio se asocia. Contrasta con `Get-Process`, `netstat -ano` y el Visor de eventos.
4. **Rutas y autoarranque sospechosos.** Coloca (en tu VM) un ejecutable inocuo en una ruta inusual y en el autoarranque; comprueba si RootCause lo marca como indicio de persistencia.
5. **Captura de evidencia.** Usa la integración WPR/ETW para capturar un intervalo y revisa el resumen del ETL sin salir de la app.
6. **Causa raíz.** Redacta la conclusión: qué proceso/carpeta/servicio/conexión explica la anomalía, con la evidencia que lo respalda.

## 🏆 Retos verificables

1. **Diagnóstico de rendimiento:** identifica el proceso que degrada el equipo y la carpeta/servicio de origen. *Aceptación:* lo confirmas con una segunda herramienta (Process Explorer / `netstat`).
2. **Indicio de persistencia:** provoca (en tu VM) una entrada de autoarranque y detéctala. *Aceptación:* explicas por qué es un indicio y cómo lo verificarías en un caso real.
3. **Evidencia:** entrega un resumen de una captura WPR/ETW y qué muestra.
4. **Complemento al EDR:** explica, con un ejemplo, qué aporta RootCause que un EDR por firma podría no señalar (comportamiento agnóstico), y viceversa.

## 🔗 Referencias

- **RootCause Windows Inspector (Apache-2.0)** — <https://github.com/vladimiracunadev-create/rootcause-windows-inspector>
- [Página del producto](https://vladimiracunadev-create.github.io/rootcause-windows-inspector/) · Manual de usuario en su repo.
- Parte 6 (comportamiento), Parte 8 (endpoint/EDR) y Parte 9 (DFIR) del programa — [índice de clases](../../classes/README.md)
