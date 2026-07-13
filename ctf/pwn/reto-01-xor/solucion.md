# Solución — Reversa el check

El `check` transforma la entrada con `b ^ 0x2a` y la compara con `objetivo`. Como el XOR es
involutivo, la contraseña correcta es `objetivo` XOR `0x2a`:

```python
objetivo = bytes.fromhex("6c666b6d5152455875184b75584f5c4f58594348464f57")
password = bytes(b ^ 0x2a for b in objetivo)
print(password.decode())
```

O en una línea de shell con Python:

```bash
python3 -c "print(bytes(b^0x2a for b in bytes.fromhex('6c666b6d5152455875184b75584f5c4f58594348464f57')).decode())"
```

Verificación: `check(password)` devuelve `True`.

## Flag

```text
FLAG{xor_2a_reversible}
```

**Lección:** una comprobación "ofuscada" con XOR/const no protege nada: se revierte con la
misma operación. Es exactamente lo que harás al analizar strings XOR-eadas en malware
([Clase 147](../../../classes/parte-6-analisis-de-malware/147-ofuscacion-packing-y-unpacking/README.md)) o en un
reto de reversing ([Clase 140](../../../classes/parte-5-explotacion-de-sistemas-y-binarios/140-ctfs-de-pwn-e-ingenieria-inversa/README.md)).
