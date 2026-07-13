# Lab: Criptografía aplicada — retos

Entorno de práctica para la **Parte 2 — Criptografía aplicada** (clases 046–065).
Cuatro retos que muestran, en la práctica, por qué ciertas construcciones criptográficas
son inseguras. **No necesita Docker ni dependencias**: todo es Python puro (stdlib).

> 🎓 Intenta resolver cada reto **por tu cuenta** antes de mirar `soluciones/`. Las
> soluciones están comentadas y explican la debilidad.

## 🎯 Los retos

| # | Reto | Debilidad que enseña | Clases |
|---|---|---|---|
| 1 | [XOR de clave repetida](retos/reto1_xor.txt) | Un "cifrado" XOR con clave corta se rompe por análisis de frecuencia | [048](../../classes/parte-2-criptografia-aplicada/048-cifrado-de-flujo-chacha20-y-por-que-evitar-rc4/README.md) |
| 2 | [RSA con primos cercanos](retos/reto2_rsa.txt) | Si `p` y `q` son cercanos, `n` se factoriza con Fermat en milisegundos | [049](../../classes/parte-2-criptografia-aplicada/049-cifrado-asimetrico-rsa/README.md) |
| 3 | [Hashes MD5 sin sal](retos/reto3_hashes.txt) | MD5 sin sal + contraseñas débiles = crackeo instantáneo | [051](../../classes/parte-2-criptografia-aplicada/051-funciones-hash-sha-2-sha-3-y-sus-propiedades/README.md), [057](../../classes/parte-2-criptografia-aplicada/057-almacenamiento-seguro-de-contrasenas-bcrypt-scrypt-y-argon2/README.md) |
| 4 | [Detección de AES-ECB](retos/reto4_ecb.txt) | ECB filtra patrones: mismo bloque de texto → mismo bloque cifrado | [047](../../classes/parte-2-criptografia-aplicada/047-cifrado-simetrico-aes-y-modos-de-operacion/README.md) |

## 🚀 Cómo trabajar

```bash
cd labs/cripto
# (opcional) regenerar los datos de los retos de forma determinista:
python _generar_retos.py

# resuelve tú; cuando quieras comprobar, corre la solución:
python soluciones/sol1_xor.py
python soluciones/sol2_rsa.py
python soluciones/sol3_hashes.py
python soluciones/sol4_ecb.py
```

## 🧭 Pistas

- **Reto 1:** la clave es corta y se repite. Prueba longitudes de clave y, para cada
  columna, elige el byte que produzca texto legible (el espacio `0x20` es el carácter
  más frecuente).
- **Reto 2:** `n = p·q` con `p ≈ q`. Escribe `n = a² − b²`; empieza en `a = ⌈√n⌉` y sube.
- **Reto 3:** son MD5 hexadecimales de 32 caracteres. Hashea cada palabra del
  `diccionario.txt` y compara. (Con Hashcat sería `hashcat -m 0`).
- **Reto 4:** parte el ciphertext en bloques de 16 bytes y busca bloques idénticos.

## 🏆 Retos verificables

1. Recupera la clave y la flag del Reto 1. *Aceptación:* imprimes `FLAG{...}` y la clave.
2. Factoriza `n` y descifra el Reto 2. *Aceptación:* obtienes `p`, `q` y la flag.
3. Crackea los 3 hashes del Reto 3. *Aceptación:* las 3 contraseñas en claro.
4. Demuestra que el Reto 4 usa ECB. *Aceptación:* señalas los bloques repetidos y propones el modo correcto (CBC/CTR/GCM).
5. **Defensa:** para cada reto, escribe la construcción correcta (ChaCha20/AES-GCM, RSA-OAEP con primos grandes y aleatorios, Argon2id).

## 🔗 Referencias

- Aumasson — *Serious Cryptography*. · Wong — *Real-World Cryptography*.
- [CryptoHats / CryptoPals Challenges](https://cryptopals.com/) (inspiración para más retos).
- Parte 2 del programa — [índice de clases](../../classes/README.md)
