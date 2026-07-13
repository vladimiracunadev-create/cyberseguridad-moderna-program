# Clase 004 — Montaje del laboratorio: virtualización, Kali, snapshots y aislamiento de red

> Parte: **0 — Fundamentos y prerrequisitos** · Fuente: *Kali Linux Documentation / OffSec*
> ⏱️ Duración estimada: **120 min** · Nivel: **Fundamentos**

---

## 🎯 Objetivo

Construir un laboratorio de seguridad **aislado y reversible** en tu propio equipo. Al terminar tendrás una máquina atacante (Kali) y una o más máquinas víctima en una red interna sin salida a Internet ni a tu red doméstica, con snapshots para volver atrás tras cada experimento.

> ⚠️ **Nota ética y de seguridad**: todo lo que se practica en este programa se hace **exclusivamente** dentro de este laboratorio aislado o contra sistemas para los que tengas autorización escrita. Atacar redes o equipos ajenos es ilegal. El aislamiento no es opcional: protege a terceros y te protege a ti.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Instalar** un hipervisor y comprobar la virtualización por hardware.
2. **Desplegar** Kali Linux y una VM víctima desde imágenes oficiales.
3. **Configurar** una red interna/host-only sin acceso a Internet.
4. **Gestionar** snapshots para revertir el estado tras cada práctica.
5. **Verificar** el aislamiento con pruebas de conectividad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Virtualización tipo 1 vs. tipo 2 | Elegir hipervisor adecuado al equipo |
| 2 | VT-x/AMD-V | Sin ella, las VMs van lentísimas o no arrancan |
| 3 | Imágenes oficiales y verificación | Evitar ISOs manipuladas (checksum/firma) |
| 4 | Modos de red | NAT, bridged, host-only, internal |
| 5 | Aislamiento | Impedir fugas del laboratorio a producción |
| 6 | Snapshots | Reversibilidad = experimentar sin miedo |
| 7 | Máquinas víctima | Metasploitable, DVWA, VulnHub |
| 8 | Higiene del lab | Recursos, plantillas, mantenimiento |

## 📖 Definiciones y características

- **Hipervisor**: software que ejecuta VMs. Tipo 1 (ESXi, Hyper-V) corre sobre el hardware; tipo 2 (VirtualBox, VMware Workstation) sobre un SO anfitrión. Clave: para un lab personal, tipo 2 basta.
- **Snapshot**: foto del estado completo de una VM (disco + RAM). Clave: permite volver a un punto limpio en segundos.
- **Red host-only**: red virtual entre el anfitrión y las VMs, sin salida a Internet. Clave: aislamiento parcial (el host la ve).
- **Red interna (internal)**: red solo entre VMs, ni siquiera el host tiene acceso directo. Clave: el mayor aislamiento.
- **Metasploitable**: VM deliberadamente vulnerable para practicar. Clave: nunca exponerla a Internet.
- **Checksum/firma**: verificación de integridad y autenticidad de la ISO. Clave: garantiza que descargaste la imagen real.

## 🧰 Herramientas y preparación

Instala **VirtualBox** (gratuito, multiplataforma) o **VMware Workstation Player**. Descarga la imagen oficial de **Kali Linux** desde <https://www.kali.org/get-kali/> y una víctima como **Metasploitable 2** o **DVWA**. Verifica siempre el checksum SHA-256 publicado. Comprueba que la virtualización esté activada en la BIOS/UEFI.

## 🧪 Laboratorio guiado

1. **Comprobar virtualización**. En Windows, abre el Administrador de tareas → Rendimiento → CPU y confirma "Virtualización: habilitada". Si no, actívala en la UEFI (VT-x/AMD-V).
2. **Verificar la ISO de Kali**. Descarga la imagen y su checksum. En PowerShell:

   ```powershell
   Get-FileHash .\kali-linux-*.iso -Algorithm SHA256
   ```

   Compara el resultado con el valor oficial de kali.org. Si no coincide, no la uses.
3. **Crear la VM Kali** en VirtualBox: 2 vCPU, 4 GB RAM, 40 GB disco. Monta la ISO y completa la instalación gráfica.
4. **Crear la red interna**. En VirtualBox → Herramientas → Red, o por VM en Configuración → Red → "Red interna" con nombre `lab-net`. Asigna ese adaptador a Kali y a la víctima.
5. **Desplegar la víctima** (Metasploitable) importando el OVA/OVF y conectándola a `lab-net`.
6. **Direccionar**. Configura IPs estáticas en la misma subred, p. ej. Kali `10.10.10.5` y víctima `10.10.10.6`, máscara `/24`.
7. **Probar conectividad interna**:

   ```bash
   ping -c 3 10.10.10.6
   ```

8. **Verificar aislamiento**. Desde Kali intenta salir a Internet; **no** debe haber ruta:

   ```bash
   ping -c 2 8.8.8.8   # debe fallar: destino inalcanzable
   ```

9. **Tomar snapshot** de cada VM en estado limpio recién instalado. Etiqueta: `base-limpia`.
10. **Prueba de reversión**: crea un archivo en Kali, apaga, restaura el snapshot y confirma que el archivo desapareció.

## ✍️ Ejercicios

1. Explica cuándo usar NAT, bridged, host-only e internal, y por qué el laboratorio usa internal.
2. Documenta el proceso de verificación de checksum y qué harías si no coincide.
3. Crea un tercer nodo (una VM Windows de evaluación) en la misma red y verifica que ve a Kali.
4. Diseña una convención de nombres y de IPs para tu laboratorio (subredes por escenario).
5. Toma un snapshot con RAM y otro sin RAM; explica la diferencia práctica.
6. Escribe un pequeño checklist de "higiene" para mantener el lab (actualizaciones, plantillas, limpieza).

## 📝 Reto verificable

Entrega un laboratorio funcional con al menos dos VMs (Kali + una víctima) en red interna aislada, con IPs estáticas documentadas y un snapshot `base-limpia` por VM. Adjunta capturas de: (a) `ping` interno exitoso, (b) `ping` a Internet fallido, y (c) la lista de snapshots.

**Criterio de aceptación**: Kali alcanza a la víctima por la red interna pero **ninguna** VM alcanza Internet, y restaurar el snapshot devuelve la VM a un estado limpio verificable. Cualquiera con tus notas puede reproducir el montaje.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| "VT-x is not available" / VM muy lenta | Virtualización desactivada en UEFI o Hyper-V acaparando VT-x. Actívala; en Windows desactiva Hyper-V si usas VirtualBox. |
| Las VMs no se ven entre sí | Adaptadores en redes distintas o IPs en subredes diferentes. Ponlas en el mismo `internal` y subred. |
| La víctima tiene salida a Internet | Adaptador en NAT/bridged por error. Cámbialo a red interna. |
| Snapshot enorme / disco lleno | Snapshots acumulados sin limpiar. Consolida o elimina los antiguos. |
| ISO no arranca | Descarga corrupta. Verifica el checksum y vuelve a bajarla. |

## ❓ Preguntas frecuentes

**❓ ¿Puedo usar Kali como sistema principal?** No es recomendable para empezar: Kali está pensado como herramienta, no como escritorio diario. Úsalo dentro de una VM aislada.

**❓ ¿VirtualBox o VMware?** Ambos sirven para el curso. VirtualBox es gratuito y multiplataforma; VMware suele rendir algo mejor. Elige uno y sé consistente.

**❓ ¿Por qué red interna y no host-only?** Host-only deja al host en la red; interna aísla aún más. Para prácticas ofensivas con malware, cuanto más aislado, mejor.

**❓ ¿Necesito mucha RAM?** Con 8 GB puedes correr Kali + una víctima. Con 16 GB trabajas cómodo con varios nodos.

## 🔗 Referencias

- Kali Linux — Get Kali y documentación — <https://www.kali.org/docs/>
- Oracle VirtualBox Manual — <https://www.virtualbox.org/manual/>
- Rapid7 Metasploitable — <https://docs.rapid7.com/metasploit/metasploitable-2/>
- OWASP DVWA — <https://github.com/digininja/DVWA>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-004-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-004-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 005 - Linux esencial para seguridad: filesystem, permisos y usuarios](../005-linux-esencial-para-seguridad-filesystem-permisos-y-usuarios/README.md)
