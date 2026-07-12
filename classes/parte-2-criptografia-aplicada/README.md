# Parte 2 — Criptografía aplicada

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-3-hacking-etico-y-pentesting-metodologia/README.md)

**20 clases** · rango 046–065 · Simétrica, asimétrica, hashing, PKI, TLS y criptoanálisis

**Fuentes de referencia de esta parte:**

- Jean-Philippe Aumasson, *Serious Cryptography* (2ª ed., No Starch Press).
- David Wong, *Real-World Cryptography* (Manning).
- Niels Ferguson, Bruce Schneier y Tadayoshi Kohno, *Cryptography Engineering* (Wiley).
- Dan Boneh y Victor Shoup, *A Graduate Course in Applied Cryptography* (borrador libre en línea).
- NIST FIPS 197 (AES), FIPS 186-5 (firmas), SP 800-38 (modos), SP 800-90A (DRBG).
- IETF RFC 8446 (TLS 1.3), RFC 5116 (AEAD), RFC 8439 (ChaCha20-Poly1305).

---

## 🎯 ¿De qué trata esta parte?

La criptografía es el pilar sobre el que descansan la confidencialidad, la integridad y la autenticidad de casi todo lo que hacemos en redes: HTTPS, VPN, firma de software, mensajería cifrada, blockchains y almacenamiento de contraseñas. Esta parte te lleva desde los fundamentos históricos hasta las primitivas modernas que usan los sistemas reales, con un enfoque de **ingeniería**: no solo qué es AES o RSA, sino cómo se usan bien, cómo se rompen cuando se usan mal y qué herramientas reales manejar (OpenSSL, la librería `cryptography` de Python, hashcat).

El objetivo no es convertirte en criptógrafo teórico —eso requiere años de matemáticas— sino en un **usuario competente y crítico** de la criptografía. La mayoría de las brechas relacionadas con cripto no provienen de romper AES por fuerza bruta (imposible), sino de errores de implementación: nonces reutilizados, modos inseguros como ECB, padding oracles, comparaciones no constantes en tiempo, generadores de aleatoriedad predecibles y almacenamiento de contraseñas con hashes rápidos. Aprenderás a reconocer y evitar esas trampas.

Esta parte sirve a desarrolladores que integran cripto en sus aplicaciones, a pentesters que auditan implementaciones, a analistas de seguridad que evalúan configuraciones TLS y a cualquiera que quiera entender de verdad por qué "no hagas tu propia cripto" es un consejo tan repetido.

## 🧩 Problemas que resuelve

- Elegir la primitiva correcta para cada objetivo (confidencialidad, integridad, autenticación, intercambio de claves).
- Evitar los errores clásicos: ECB, nonce reutilizado, MAC-then-encrypt mal hecho, hashes rápidos para contraseñas.
- Configurar y auditar TLS moderno (cipher suites, forward secrecy, certificados).
- Entender PKI: cómo se emiten, validan y revocan los certificados X.509.
- Almacenar contraseñas de forma resistente a cracking con Argon2/bcrypt/scrypt.
- Reconocer ataques prácticos (padding oracle, timing) y por qué AEAD los previene.
- Prepararse para la transición post-cuántica y la gestión centralizada de secretos.

## 🎓 Resultados de aprendizaje

Al terminar la parte, podrás:

- Explicar y aplicar cifrado simétrico (AES-GCM, ChaCha20-Poly1305) y de flujo con nonces correctos.
- Usar RSA y ECC para cifrado, firma e intercambio de claves, entendiendo sus límites.
- Elegir y usar funciones hash (SHA-2, SHA-3, BLAKE2) y MAC (HMAC) según el caso.
- Diseñar un esquema de intercambio de claves con Diffie-Hellman y forward secrecy.
- Construir y validar una PKI de laboratorio con OpenSSL, incluyendo revocación.
- Auditar un handshake TLS 1.3 y detectar configuraciones débiles.
- Almacenar contraseñas de forma segura y estimar el coste de un ataque con hashcat.
- Identificar y explicar padding oracle, ataques de timing y por qué AEAD es el estándar.

## 🧱 Prerrequisitos

Se asume haber cursado la **Parte 1 — Redes y seguridad de redes** (modelo TCP/IP, TLS a nivel de red, captura con Wireshark). Conviene manejar la línea de comandos de Linux, Python básico y aritmética modular a nivel intuitivo. No se requieren matemáticas avanzadas: los conceptos numéricos se introducen con analogías y ejemplos ejecutables.

## 🗺️ Estructura temática

| Bloque | Clases | Contenido |
|--------|--------|-----------|
| Fundamentos | 046 | Historia, principios (Kerckhoffs), modelo de amenaza |
| Cifrado simétrico | 047–048 | AES y modos, cifrado de flujo (ChaCha20), por qué no RC4 |
| Cifrado asimétrico | 049–050 | RSA y ECC |
| Integridad y autenticación | 051–052 | Funciones hash (SHA-2/3), HMAC |
| Protocolos de clave | 053–054 | Diffie-Hellman, firmas digitales |
| Infraestructura | 055–056 | PKI y X.509, TLS/SSL en profundidad |
| Robustez práctica | 057–059 | Hash de contraseñas, CSPRNG, AEAD |
| Ataques y análisis | 060–061 | Padding oracle y timing, criptoanálisis |
| Frontera y operación | 062–065 | Post-cuántica, gestión de secretos, esteganografía, errores comunes |

## 🔗 Referencias de la parte

- Aumasson, *Serious Cryptography*, No Starch Press — https://nostarch.com/serious-cryptography-2nd-edition
- Wong, *Real-World Cryptography*, Manning — https://www.manning.com/books/real-world-cryptography
- Ferguson, Schneier, Kohno, *Cryptography Engineering* — https://www.schneier.com/books/cryptography-engineering/
- Boneh & Shoup, *A Graduate Course in Applied Cryptography* — https://toc.cryptobook.us/
- NIST Cryptographic Standards — https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines
- IETF RFC 8446 (TLS 1.3) — https://www.rfc-editor.org/rfc/rfc8446

## ▶️ Empezar

[Clase 046 — Historia y fundamentos de la criptografía](046-historia-y-fundamentos-de-la-criptografia/README.md)
