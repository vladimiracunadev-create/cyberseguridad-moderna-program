# 💥 Pwn / Rev — Reversa el check ⭐⭐

Este validador acepta una única contraseña correcta. No hay fuerza bruta: **razona** qué
entrada lo hace devolver `True`. Esa contraseña es la flag.

```python
def check(password: bytes) -> bool:
    objetivo = bytes.fromhex(
        "6c666b6d5152455875184b75584f5c4f58594348464f57"
    )
    transformado = bytes(b ^ 0x2a for b in password)
    return transformado == objetivo
```

**Pista:** la transformación es un XOR byte a byte con una constante. El XOR es su propia
inversa: `(x ^ k) ^ k == x`.

➡️ ¿Atascado? Mira [`solucion.md`](solucion.md).
