# Solución — El JWT indiscreto

El *payload* de un JWT solo está **codificado** en Base64URL, no cifrado. Se lee sin la clave.

```bash
echo 'eyJ1c2VyIjogImd1ZXN0IiwgInJvbGUiOiAiYWRtaW4iLCAiZmxhZyI6ICJGTEFHe2p3dF9wYXlsb2FkX25vX2NpZnJhZG99In0' \
  | base64 -d 2>/dev/null; echo
```

(Si falla el padding, añade `=` al final hasta que la longitud sea múltiplo de 4.)

Salida:

```json
{"user": "guest", "role": "admin", "flag": "FLAG{jwt_payload_no_cifrado}"}
```

## Flag

```text
FLAG{jwt_payload_no_cifrado}
```

**Lección:** nunca pongas secretos en el *payload* de un JWT: es legible por el cliente. La
firma garantiza **integridad**, no **confidencialidad**. Además, ojo con `alg: none` y con
claves HS256 débiles. Ver [Clase 103](../../../classes/parte-4-seguridad-de-aplicaciones-web/103-ataques-y-seguridad-de-jwt/README.md).
