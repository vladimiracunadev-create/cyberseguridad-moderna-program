# Solución — Cebolla de encodings

Tres capas, de fuera hacia dentro: **Base64 → hex → ROT13**.

```bash
echo 'NTM1OTRlNTQ3YjcwNzI2ZjYyNzk3OTZlNWY3MTcyNWY3MjYxNzA2MjcxNzY2MTc0NjY3ZA==' \
  | base64 -d \            # capa 1: base64  -> una cadena hexadecimal
  | xxd -r -p \            # capa 2: hex      -> texto ROT13
  | tr 'A-Za-z' 'N-ZA-Mn-za-m'   # capa 3: ROT13 -> flag
```

En Python:

```python
import base64, codecs
s = "NTM1OTRlNTQ3YjcwNzI2ZjYyNzk3OTZlNWY3MTcyNWY3MjYxNzA2MjcxNzY2MTc0NjY3ZA=="
hexs = base64.b64decode(s).decode()          # capa 1
rot  = bytes.fromhex(hexs).decode()          # capa 2
print(codecs.decode(rot, "rot_13"))          # capa 3
```

## Flag

```text
FLAG{cebolla_de_encodings}
```

**Lección:** codificar (Base64, hex, ROT13) **no** es cifrar. No aporta confidencialidad;
cualquiera revierte las capas sin clave. Ver [Clase 020](../../../classes/parte-0-fundamentos-y-prerrequisitos/020-sistemas-de-numeracion-y-encoding-binario-hex-base64-y-url/README.md).
