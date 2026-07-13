# Parte 5 — Explotación de sistemas y binarios

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-6-analisis-de-malware/README.md)

**25 clases** · rango 116–140 · Assembly, buffer overflows, ROP, heap, fuzzing e ingeniería inversa

**Fuentes de referencia de esta parte:**

- Jon Erickson — *Hacking: The Art of Exploitation, 2nd Edition* (No Starch Press).
- Dennis Andriesse — *Practical Binary Analysis* (No Starch Press).
- Anley, Heasman, Lindner, Richarte — *The Shellcoder's Handbook, 2nd Edition* (Wiley).
- Bratus, Locasto et al. y la comunidad — *Nightmare* / *pwn.college* como currículos abiertos de explotación.
- Intel — *Intel 64 and IA-32 Architectures Software Developer's Manual* (referencia de arquitectura).
- System V Application Binary Interface — *AMD64 Architecture Processor Supplement* (convenciones de llamada).

---

## 🎯 ¿De qué trata esta parte?

Esta parte baja al nivel más profundo de la seguridad ofensiva: la memoria de un proceso, el
juego de registros de la CPU y los bytes de un binario compilado. Aquí aprenderás cómo un
programa escrito en C se convierte en instrucciones máquina, dónde viven el stack y el heap,
y por qué un simple error al copiar datos puede darle a un atacante el control del flujo de
ejecución. Es el corazón del *binary exploitation* (pwn) y de la ingeniería inversa.

Importa porque las vulnerabilidades de corrupción de memoria siguen siendo, décadas después,
una de las clases de fallos más críticas: alimentan exploits de kernel, cadenas de 0-day en
navegadores y escapes de sandbox. Entender cómo funcionan por dentro te convierte en mejor
defensor (sabes qué mitigar y por qué), mejor desarrollador (escribes código que no rompe la
memoria) y mejor investigador (descubres y reportas fallos antes que los adversarios).

Sirve a pentesters que quieren ir más allá de la web, a analistas de malware que necesitan leer
ensamblador, a investigadores de vulnerabilidades y a cualquiera que aspire a competir en CTFs
de categoría *pwn* y *reversing*. El recorrido va de los fundamentos de la arquitectura x86/x64
hasta técnicas modernas de ROP, explotación de heap, fuzzing con AFL++ e introducción al kernel.

> ⚠️ **Nota ética.** Todo el contenido ofensivo de esta parte se practica exclusivamente en
> **laboratorios propios** (máquinas virtuales aisladas, binarios que tú compilas, retos de CTF
> con permiso) o con **autorización explícita por escrito**. Desarrollar o desplegar exploits
> contra sistemas de terceros sin consentimiento es ilegal en la mayoría de jurisdicciones.

## 🧩 Problemas que resuelve

- Leer y razonar sobre código ensamblador x86/x64 para entender qué hace un binario sin fuente.
- Depurar procesos a nivel de instrucción y examinar el estado exacto de memoria y registros.
- Identificar y explotar corrupciones de memoria: stack overflow, format string, heap, integer bugs.
- Evadir mitigaciones modernas (ASLR, DEP/NX, canarios, PIE) con ret2libc y ROP.
- Realizar ingeniería inversa de binarios con Ghidra, IDA y radare2 para análisis y CTFs.
- Descubrir vulnerabilidades desconocidas mediante fuzzing y auditoría de código.
- Construir exploits reproducibles y automatizados con pwntools.

## 🎓 Resultados de aprendizaje

Al terminar la parte, el alumno podrá:

1. Explicar la arquitectura x86/x64: registros, modos, el stack y las convenciones de llamada.
2. Depurar binarios con GDB+pwndbg y con radare2, inspeccionando memoria, stack y registros.
3. Diagnosticar y explotar un stack buffer overflow controlando `RIP`/`EIP`.
4. Escribir shellcode funcional y minimizar bytes nulos.
5. Describir y evadir ASLR, DEP/NX, stack canaries y PIE con ret2libc y cadenas ROP.
6. Explotar format strings, use-after-free, double free e integer overflows en laboratorio.
7. Aplicar ingeniería inversa con Ghidra/IDA/radare2 y automatizar análisis dinámico.
8. Encontrar bugs con fuzzing (AFL++/libFuzzer) y construir exploits con pwntools.

## 🧱 Prerrequisitos

- **Parte 0 — Fundamentos**: línea de comandos de Linux, compilación básica y C elemental.
- **Parte 3 — Hacking ético y pentesting**: metodología, mentalidad ofensiva y ética/legalidad.
- Recomendable **Parte 4 — Seguridad de aplicaciones web** para contrastar bugs de memoria vs. lógica.
- Programación en C y nociones de cómo el sistema operativo gestiona procesos y memoria virtual.

## 🗺️ Estructura temática

| Bloque | Clases | Contenido |
| --- | --- | --- |
| Fundamentos de bajo nivel | 116–118 | Arquitectura, stack/registros/ABI, debugging con GDB+pwndbg |
| Stack overflows y shellcode | 119–121 | Teoría, explotación práctica y escritura de shellcode |
| Mitigaciones y su evasión | 122–124 | ASLR/DEP/canaries/PIE, ret2libc y ROP |
| Otras clases de bugs | 125–128 | Format string, heap, UAF/double free, integer overflows |
| Windows y reversing | 129–135 | SEH, RE, Ghidra, IDA/radare2, estático/dinámico, anti-reversing |
| Descubrimiento y avanzado | 136–140 | Fuzzing, hallazgo de vulns, exploits modernos, kernel, CTFs |

## 🔗 Referencias de la parte

- Erickson, J. *Hacking: The Art of Exploitation, 2e*. No Starch Press — <https://nostarch.com/hacking2.htm>
- Andriesse, D. *Practical Binary Analysis*. No Starch Press — <https://practicalbinaryanalysis.com/>
- Anley et al. *The Shellcoder's Handbook, 2e*. Wiley.
- pwn.college — currículo abierto de explotación — <https://pwn.college/>
- Nightmare (guyinatuxedo) — <https://guyinatuxedo.github.io/>
- System V AMD64 ABI — <https://gitlab.com/x86-psABIs/x86-64-ABI>

## ▶️ Empezar

[Clase 116 — Arquitectura x86/x64 y lenguaje ensamblador](116-arquitectura-x86-x64-y-lenguaje-ensamblador/README.md)
