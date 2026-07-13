# Solución — Autenticación a la vista

HTTP *Basic Auth* transmite `usuario:contraseña` **solo en Base64**, sin cifrar. Sobre HTTP
plano (sin TLS), cualquiera que capture el tráfico lo lee.

```bash
echo 'YWRtaW46RkxBR3tiYXNpY19hdXRoX2VzX2Jhc2U2NH0=' | base64 -d; echo
# admin:FLAG{basic_auth_es_base64}
```

Usuario `admin`, contraseña (la flag) a continuación de los dos puntos.

## Flag

```text
FLAG{basic_auth_es_base64}
```

**Lección:** Basic Auth sin TLS = credenciales en claro para cualquier sniffer
([Clase 026](../../../classes/parte-1-redes-y-seguridad-de-redes/026-wireshark-captura-y-analisis-de-paquetes/README.md)).
Usa siempre HTTPS y prefiere mecanismos con tokens de vida corta.
