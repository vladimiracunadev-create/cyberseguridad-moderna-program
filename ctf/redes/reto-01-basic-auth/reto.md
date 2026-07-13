# 🌐 Redes — Autenticación a la vista ⭐

Capturaste esta petición HTTP en una red sin TLS. El servidor pide *Basic Auth*.
¿Qué credenciales viajaron? La contraseña es la flag.

```http
GET /admin HTTP/1.1
Host: intranet.lab
Authorization: Basic YWRtaW46RkxBR3tiYXNpY19hdXRoX2VzX2Jhc2U2NH0=
User-Agent: curl/8.5.0
Accept: */*
```

**Pista:** en HTTP *Basic Auth*, el valor tras la palabra `Basic` es `usuario:contraseña` en Base64.

➡️ ¿Atascado? Mira [`solucion.md`](solucion.md).
