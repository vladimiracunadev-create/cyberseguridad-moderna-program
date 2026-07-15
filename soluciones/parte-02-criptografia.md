# Soluciones — Parte 2: Criptografía aplicada

> Estas son **claves de referencia** para el instructor y para autoevaluación. Intenta resolver cada reto y ejercicio por tu cuenta **antes** de mirar aquí: el valor está en el proceso, no en la respuesta. Puede haber más de una solución correcta; lo que sigue es una guía técnicamente válida.
>
> Volver al índice de la parte: [../classes/parte-2-criptografia-aplicada/README.md](../classes/parte-2-criptografia-aplicada/README.md)

Todos los ejercicios se resuelven en un entorno de laboratorio aislado (VM o contenedor propio), sobre datos propios y sin apuntar herramientas a sistemas de terceros.

---

## Clase 046 — Historia y fundamentos de la criptografía

### Solución del reto verificable

Objetivo: romper una sustitución monoalfabética por análisis de frecuencias + bigramas y recuperar ≥90 % del texto.

Pasos:

1. Normaliza el cifrado (mayúsculas, conserva solo A–Z; trata la Ñ aparte o mapéala).
2. Cuenta frecuencia de cada símbolo y ordénala. Asigna como semilla el orden esperado del español: `E A O S R N I D L C T U M P ...`.
3. Refina con bigramas/trigramas frecuentes del español (`DE`, `LA`, `QUE`, `EN`, `EL`) y palabras cortas de 1–2 letras (`Y`, `A`, `DE`, `EL`).
4. Optimiza el mapeo con *hill climbing*: puntúa cada clave candidata con log-verosimilitud de cuadrigramas del español y acepta permutaciones que mejoren la puntuación (miles de iteraciones con reinicios aleatorios).

```python
import random, math
from collections import Counter

def puntua(txt, logp, N=4):
    s, floor = 0.0, math.log10(0.01/ sum(1 for _ in logp))
    for i in range(len(txt)-N+1):
        s += logp.get(txt[i:i+N], floor)
    return s

def romper(cifrado, logp, iters=20000):
    alf = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    mejor = alf[:]; random.shuffle(mejor)
    def aplica(k): 
        t = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "".join(k))
        return cifrado.translate(t)
    best_s = puntua(aplica(mejor), logp)
    for _ in range(iters):
        c = mejor[:]; a,b = random.sample(range(26),2); c[a],c[b]=c[b],c[a]
        s = puntua(aplica(c), logp)
        if s > best_s: best_s, mejor = s, c
    return "".join(mejor), aplica(mejor)
```

Evidencia de cumplimiento: muestra el mapeo deducido y compara carácter a carácter contra el texto plano real; reporta el porcentaje de aciertos (`>=90%`) sobre un cifrado de ≥500 caracteres.

### Claves de los ejercicios

1. `WKLV LV D WHVW` con desplazamiento 3 hacia atrás → `THIS IS A TEST`.
2. Rota Vigenère con longitud L conocida: divide el cifrado en L columnas (una por posición de clave); cada columna es un César → resuélvelo por frecuencias (la letra más frecuente ≈ `E`/`A`). Reúne las L letras de clave.
3. Modelo de amenaza chat: **activos** = mensajes, metadatos, contactos; **atacante** = red pasiva/activa (MITM), servidor curioso, robo de dispositivo; **capacidades** = intercepta y modifica tráfico, no rompe cripto moderna; **objetivos de seguridad** = confidencialidad E2E, integridad, forward secrecy.
4. Seguridad por oscuridad fallida: A5/1 (GSM), cifrado de DVD (CSS) o Mifare Classic (Crypto-1) — todos rotos al filtrarse/aplicar ingeniería inversa el algoritmo "secreto".
5. Espacios de claves: César 25 ≈ 2^4·6; DES 2^56; AES-128 2^128. AES-128 es 2^72 veces mayor que DES (≈ 4.7×10^21) y astronómicamente mayor que César.
6. Transposición columnar: escribe el texto en filas bajo una clave, lee columnas en el orden alfabético de la clave. Criptoanálisis: anagramación por columnas + análisis de frecuencias de contacto entre columnas (las frecuencias de letra individuales se conservan, lo que delata la transposición).

---

## Clase 047 — Cifrado simétrico: AES y modos de operación

### Solución del reto verificable

Objetivo: cifrar la misma imagen BMP con ECB y CBC; ECB debe mostrar la silueta y CBC debe verse como ruido.

Pasos:

1. Usa un BMP sin comprimir; conserva la cabecera (54 bytes típicos) sin cifrar y cifra solo el cuerpo de píxeles para que siga siendo visualizable.
2. Cifra el cuerpo con ECB y con CBC (IV aleatorio) usando la misma clave.
3. Reensambla `cabecera_original || cuerpo_cifrado` en dos archivos y ábrelos.

```bash
# separa cabecera y cuerpo
head -c 54 tux.bmp > head.bin
tail -c +55 tux.bmp > body.bin
openssl enc -aes-128-ecb -nosalt -K 000102030405060708090a0b0c0d0e0f -in body.bin -out ecb_body.bin
openssl enc -aes-128-cbc -nosalt -K 000102030405060708090a0b0c0d0e0f -iv 00112233445566778899aabbccddeeff -in body.bin -out cbc_body.bin
cat head.bin ecb_body.bin > tux_ecb.bmp
cat head.bin cbc_body.bin > tux_cbc.bmp
```

Evidencia: en `tux_ecb.bmp` la silueta original sigue reconocible (bloques iguales → cifrados iguales); en `tux_cbc.bmp` no hay patrón visible. El encadenamiento de CBC hace que cada bloque dependa del anterior, eliminando la estructura.

### Claves de los ejercicios

1. ECB cifra cada bloque de 16 B de forma independiente y determinista: dos bloques de texto plano iguales producen bloques cifrados idénticos, revelando repeticiones/estructura.
2. Reusar IV en CBC con misma clave: los mensajes que comparten prefijo producen el mismo cifrado inicial hasta el primer bloque que difiere → filtra igualdad de prefijos y facilita inferencias.
3. AES-CTR: `keystream = E_k(nonce||contador)`; cifrar y descifrar son la misma operación (XOR con el keystream), por eso no hay padding y `E(k)⊕c = m`. Verifica que descifrar el cifrado devuelve el texto.
4. `openssl speed -evp aes-128-cbc` con AES-NI multiplica el rendimiento (GB/s) frente a la implementación software; compara con `OPENSSL_ia32cap` deshabilitando AES-NI.
5. Documenta las capturas: el BMP en ECB conserva la imagen; anota que es el fallo didáctico canónico (pingüino Tux).
6. CTR permite acceso aleatorio porque el keystream del bloque *i* solo depende de `nonce||i` (no del texto previo); CBC encadena cada bloque con el cifrado anterior, obligando a procesar secuencialmente.

---

## Clase 048 — Cifrado de flujo: ChaCha20 y por qué evitar RC4

### Solución del reto verificable

Objetivo: ataque de nonce reutilizado (crib dragging) para recuperar `m2` conocido parcialmente `m1`, sin la clave.

Fundamento: con (clave, nonce) repetido, `c1 ⊕ c2 = m1 ⊕ m2`. Si conoces un fragmento de `m1` en la posición *i*, obtienes `m2` en esa posición: `m2[i] = c1[i] ⊕ c2[i] ⊕ m1[i]`.

```python
def xor(a, b): return bytes(x ^ y for x, y in zip(a, b))

# c1, c2 cifrados con misma clave y nonce
d = xor(c1, c2)                 # = m1 XOR m2
crib = b" the "                 # fragmento conocido de m1 (crib dragging)
for i in range(len(d) - len(crib) + 1):
    ventana = xor(d[i:i+len(crib)], crib)   # candidato de m2 en esa posición
    if all(32 <= c < 127 for c in ventana):
        print(i, ventana)       # posiciones plausibles (texto imprimible)
```

Evidencia: recuperas el tramo de `m2` solapado con la porción conocida de `m1` y muestras que nunca usaste la clave; ampliando el crib con texto plausible (palabras del idioma) extiendes la recuperación.

### Claves de los ejercicios

1. Un cifrado de flujo procesa byte a byte (XOR con keystream); no rellena a múltiplos de bloque, luego no necesita padding.
2. `c1 = m1 ⊕ ks`, `c2 = m2 ⊕ ks` con el mismo keystream `ks`; entonces `c1 ⊕ c2 = (m1⊕ks)⊕(m2⊕ks) = m1 ⊕ m2` (el keystream se cancela).
3. WEP: reutilizaba IVs de 24 bits con RC4 y una clave concatenada débil; el ataque FMS/PTW recupera la clave observando muchos IVs → RC4+IV corto rompió WEP.
4. Móviles sin AES-NI: AES en software es lento y vulnerable a timing por tablas; ChaCha20 (ARX) es rápido y de tiempo constante por diseño.
5. Modificar un byte del cifrado ChaCha20 cambia exactamente el mismo byte del texto descifrado (maleabilidad XOR), sin detección → hace falta un MAC.
6. Poly1305 añade autenticación/integridad (MAC): ChaCha20 solo da confidencialidad; juntos forman el AEAD ChaCha20-Poly1305.

---

## Clase 049 — Cifrado asimétrico: RSA

### Solución del reto verificable

Objetivo: "sobre digital" — cifrar un archivo de varios MB con AES-GCM y proteger la clave AES con RSA-OAEP; el descifrador recupera el original byte a byte y la clave AES nunca aparece en claro en disco.

Pasos:

1. Genera clave AES aleatoria de 32 B con CSPRNG (en memoria).
2. Cifra el archivo con AES-256-GCM (nonce de 12 B; guarda `nonce || tag || ciphertext`).
3. Cifra la clave AES con RSA-OAEP y la clave pública del destinatario → `clave.enc`.
4. Descifrador: RSA-OAEP descifra la clave AES en memoria, luego AES-GCM descifra el archivo.

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

pub = serialization.load_pem_public_key(open("pub.pem","rb").read())
dek = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)
ct = AESGCM(dek).encrypt(nonce, open("grande.bin","rb").read(), None)
enc_dek = pub.encrypt(dek, padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None))
open("grande.enc","wb").write(nonce + ct)
open("dek.enc","wb").write(enc_dek)   # la DEK solo se persiste cifrada
```

Evidencia: `sha256sum` del archivo descifrado coincide con el original; en disco solo existen `grande.enc` y `dek.enc` (la DEK jamás se escribe en claro).

### Claves de los ejercicios

1. RSA de juguete `p=61, q=53`: `n=3233`, `φ=60·52=3120`, `e=17`, `d=17⁻¹ mod 3120 = 2753`. Cifrado de `m=65`: `65^17 mod 3233 = 2790`.
2. `e=65537 = 2^16+1`: primo, con solo dos bits a 1 → exponenciación rápida (pocas multiplicaciones), evitando además los riesgos de `e=3`.
3. RSA textbook es maleable: `E(m1)·E(m2) mod n = (m1·m2)^e = E(m1·m2)`; multiplicar cifrados multiplica los planos, permitiendo manipulación (OAEP lo impide).
4. 128 bits de seguridad: RSA ≈ 3072 bits vs ECC ≈ 256 bits; ECC da claves ~12× más pequeñas y firmas/operaciones más rápidas.
5. Híbrido en Python: idéntico al reto — `AESGCM` para datos + `OAEP(SHA256)` para la clave; el patrón estándar de sobre digital.
6. RSA-1024: ~80 bits de seguridad; factorizable con recursos estatales/académicos (progreso del GNFS) → mínimo 2048, recomendado 3072.

---

## Clase 050 — Criptografía de curva elíptica (ECC)

### Solución del reto verificable

Objetivo: canal seguro — ECDH (X25519) → HKDF → AES-GCM entre dos partes; un tercero que solo ve las claves públicas no puede descifrar.

```python
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

a, b = X25519PrivateKey.generate(), X25519PrivateKey.generate()
sa = a.exchange(b.public_key())        # secreto compartido idéntico
sb = b.exchange(a.public_key())
assert sa == sb
key = HKDF(hashes.SHA256(), 32, None, b"canal-ecdh").derive(sa)
n = os.urandom(12)
ct = AESGCM(key).encrypt(n, b"hola desde A", None)
assert AESGCM(key).decrypt(n, ct, None) == b"hola desde A"
```

Evidencia: ambos derivan la misma `key` y descifran los mensajes del otro; un observador con solo las claves públicas no puede calcular el secreto compartido (ECDLP), por lo que su `decrypt` falla.

### Claves de los ejercicios

1. Suma de puntos sobre reales: traza la recta por `P` y `Q`, corta la curva en un tercer punto y refléjalo sobre el eje X → `P+Q` (para `P=Q`, usa la tangente).
2. El mejor ataque a ECDLP (Pollard rho) cuesta ~2^(n/2); una clave de 256 bits da ~128 bits, equivalente a factorizar RSA-3072.
3. X25519 entre dos pares: `a.exchange(b.pub) == b.exchange(a.pub)` → secreto idéntico (ver reto).
4. Dual_EC_DRBG: DRBG con puntos base cuyo origen (posible puerta trasera NSA) minó la confianza; lección: los parámetros deben ser verificables ("nothing-up-my-sleeve").
5. ECDSA depende de un nonce `k` aleatorio y único (reusarlo/predecirlo revela la clave); Ed25519 deriva `k` deterministamente del mensaje+clave, eliminando ese riesgo.
6. Validar el punto recibido (que está en la curva y en el subgrupo correcto) evita ataques de curva inválida/subgrupo pequeño que filtran la clave privada.

---

## Clase 051 — Funciones hash: SHA-2, SHA-3 y sus propiedades

### Solución del reto verificable

Objetivo: verificador de integridad de un directorio con manifiesto SHA-256 que detecte cualquier byte alterado indicando la ruta.

```bash
# generar manifiesto
find . -type f ! -name SHA256SUMS -exec sha256sum {} + > SHA256SUMS
# verificar más tarde
sha256sum -c SHA256SUMS        # imprime 'OK' o 'FAILED' por archivo
```

Alternativa en Python: recorre el árbol, calcula SHA-256 por archivo, guarda `{ruta: hash}` en JSON y en la verificación compara y lista las rutas cuyo hash cambió (o archivos añadidos/borrados).

Evidencia: modifica un solo byte de cualquier archivo y el verificador reporta `FAILED` con la ruta exacta; sin cambios, todo es `OK`.

### Claves de los ejercicios

1. Colisión al 50 % en SHA-256 (256 bits): por la paradoja del cumpleaños ≈ `2^(256/2) = 2^128` hashes (inviable).
2. Descarga la imagen/binario, calcula su SHA-256 y compáralo con el valor publicado por un canal confiable; deben coincidir exactamente.
3. Un hash es unidireccional y sin clave: no se puede invertir para recuperar el mensaje ni tiene secreto → no cifra (no hay descifrado).
4. `openssl speed`/`b2sum`: BLAKE2b suele ser el más rápido, SHA-256 se acelera con SHA-NI, SHA3-256 (Keccak) suele ir algo más lento en software.
5. SHAttered (2017): primera colisión práctica de SHA-1 (dos PDF distintos, mismo hash); impacto en Git y firmas → Git añadió detección de colisiones y migra a SHA-256.
6. Árbol de Merkle: hashea cada bloque, combina pares hacia arriba hasta una raíz; publicando la raíz cualquiera verifica un bloque con su ruta de Merkle (log n hashes).

---

## Clase 052 — HMAC y autenticación de mensajes

### Solución del reto verificable

Objetivo: canal autenticado `(IV, ciphertext, HMAC)` que rechace cualquier manipulación **antes** de descifrar (Encrypt-then-MAC).

```python
import os, hmac, hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

k_enc, k_mac = os.urandom(32), os.urandom(32)     # claves separadas

def emisor(m):
    iv = os.urandom(16)
    p = padding.PKCS7(128).padder(); data = p.update(m) + p.finalize()
    ct = Cipher(algorithms.AES(k_enc), modes.CBC(iv)).encryptor().update(data)
    tag = hmac.new(k_mac, iv + ct, hashlib.sha256).digest()
    return iv, ct, tag

def receptor(iv, ct, tag):
    esperado = hmac.new(k_mac, iv + ct, hashlib.sha256).digest()
    if not hmac.compare_digest(esperado, tag):    # verifica ANTES de descifrar
        raise ValueError("MAC inválido: rechazado")
    d = Cipher(algorithms.AES(k_enc), modes.CBC(iv)).decryptor().update(ct)
    u = padding.PKCS7(128).unpadder(); return u.update(d) + u.finalize()
```

Evidencia: alterar cualquier byte del IV, del ciphertext o del tag hace fallar `compare_digest` → rechazo sin descifrar; solo los mensajes íntegros se descifran. La verificación previa impide el padding oracle.

### Claves de los ejercicios

1. `hash(clave||mensaje)` con Merkle-Damgård sufre extensión de longitud (se puede añadir sufijo y recalcular el MAC sin la clave); HMAC (doble hash con ipad/opad) lo neutraliza.
2. Encrypt-then-MAC: cifra, calcula MAC sobre el cifrado, verifica el MAC antes de descifrar (ver reto).
3. Claves separadas: reutilizar una clave para cifrar y para MAC puede crear interacciones inseguras entre primitivas; deriva dos claves (p. ej. con HKDF e `info` distinto).
4. JWT HS256 firma `base64url(header).base64url(payload)` con HMAC-SHA256; verifica recomputando el HMAC sobre esas dos partes y comparando con la firma.
5. Cambiar un bit del mensaje cambia el HMAC recomputado → `compare_digest` devuelve falso; demuestra que el tag ya no coincide.
6. En AEAD (GCM/Poly1305) el MAC va integrado en una sola primitiva con nonce; HMAC es un MAC independiente útil para datos que no ciframos (tokens, webhooks).

---

## Clase 053 — Intercambio de claves: Diffie-Hellman

### Solución del reto verificable

Objetivo: handshake ECDHE **autenticado** — cada parte firma su clave pública efímera con Ed25519 (clave de largo plazo) y verifica la del otro antes de derivar la clave de sesión; un MITM que altere los efímeros es detectado.

```python
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization

def parte(id_priv):                     # id_priv: Ed25519 de largo plazo
    eph = X25519PrivateKey.generate()
    raw = eph.public_key().public_bytes(serialization.Encoding.Raw,
                                        serialization.PublicFormat.Raw)
    firma = id_priv.sign(raw)           # firma el efímero
    return eph, raw, firma

# cada lado verifica la firma del efímero del otro con su Ed25519 pública conocida
# id_pub_otro.verify(firma_otro, raw_otro)  -> lanza si no valida (MITM)
# luego: shared = eph_propio.exchange(X25519PublicKey.from_public_bytes(raw_otro))
# key = HKDF(SHA256, 32, salt, b"handshake").derive(shared)
```

Evidencia: si un MITM sustituye un efímero, la firma Ed25519 no valida (no posee la clave de largo plazo) → el handshake aborta. Solo con firmas válidas ambas partes derivan la misma clave de sesión.

### Claves de los ejercicios

1. DH juguete `p=97, g=5`: elige `a`, `b`; `A=5^a mod 97`, `B=5^b mod 97`; secreto `= B^a mod 97 = A^b mod 97` (coinciden).
2. `g^(xy) = g^(yx)` por conmutatividad de la multiplicación en el exponente → ambas partes calculan el mismo valor.
3. MITM: el atacante intercepta `A` y `B`, envía su propia pública a cada lado; acaba con dos secretos que él conoce y ninguna de las víctimas lo detecta (sin autenticación).
4. Logjam: degradaba DH a grupos de exportación de 512 bits precomputables; evita grupos <2048 bits y primos compartidos débiles → usa X25519 o grupos MODP fuertes.
5. Deriva dos claves con el mismo secreto e `info` distintos: `HKDF(...info=b"enc")` y `HKDF(...info=b"mac")` → claves independientes.
6. ECDHE (X25519) es más rápido y con claves/mensajes más pequeños que DHE clásico de 2048–3072 bits, con la misma o mayor seguridad.

---

## Clase 054 — Firmas digitales

### Solución del reto verificable

Objetivo: verificador de releases — firma artefactos con Ed25519, publica la clave pública y un script valida cada artefacto contra su firma; los alterados se marcan no confiables.

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
import glob, os

# firmar (una vez)
sk = Ed25519PrivateKey.generate()
for f in glob.glob("dist/*"):
    open(f + ".sig", "wb").write(sk.sign(open(f, "rb").read()))
# publicar pk (clave pública en raw/PEM)

# verificar
pk = sk.public_key()   # en la práctica, cargada del archivo publicado
for f in glob.glob("dist/*"):
    if f.endswith(".sig"): continue
    try:
        pk.verify(open(f + ".sig","rb").read(), open(f,"rb").read())
        print("OK", f)
    except InvalidSignature:
        print("NO CONFIABLE", f)
```

Evidencia: cualquier artefacto modificado (o con firma inválida) produce `InvalidSignature` → "NO CONFIABLE"; solo los íntegros pasan. La clave privada nunca se distribuye.

### Claves de los ejercicios

1. Firma digital: verificable con clave pública → da **no repudio** (solo el firmante tiene la privada). HMAC usa clave compartida: ambas partes pueden generar el tag, luego no hay no repudio.
2. `openssl dgst -sha256 -sign priv.pem -sigopt rsa_padding_mode:pss ...` para firmar y `-verify pub.pem` para validar (ver laboratorio de la clase).
3. PS3: Sony reutilizó el mismo nonce `k` en ECDSA para todas las firmas; con dos firmas y `k` fijo se despeja `d` (clave privada de firma de código) → jailbreak total.
4. Ed25519 deriva `k` de `hash(clave_privada || mensaje)`: determinista, sin RNG en la firma → elimina el fallo de nonce reutilizado/predecible.
5. Descarga release + firma `.asc` + clave pública del proyecto; `gpg --verify archivo.asc archivo` debe indicar "Good signature" de la clave esperada.
6. Se firma el hash (no el mensaje): eficiente (firma un digest fijo) y seguro (hash-then-sign liga la firma al contenido exacto y permite mensajes grandes).

---

## Clase 055 — PKI, certificados X.509 y autoridades de certificación

### Solución del reto verificable

Objetivo: PKI de dos niveles (raíz + intermedia); emitir un certificado de servidor firmado por la intermedia y servir la cadena completa.

```bash
# Raíz
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out ca.key
openssl req -x509 -new -key ca.key -sha256 -days 3650 -subj "/CN=Lab Root CA" -out ca.crt
# Intermedia (CSR firmado por la raíz, con CA:TRUE)
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out int.key
openssl req -new -key int.key -subj "/CN=Lab Intermediate CA" -out int.csr
openssl x509 -req -in int.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 1825 -sha256 \
    -extfile <(printf "basicConstraints=critical,CA:TRUE,pathlen:0\nkeyUsage=critical,keyCertSign,cRLSign") -out int.crt
# Servidor (firmado por la intermedia, con SAN)
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out srv.key
openssl req -new -key srv.key -subj "/CN=lab.local" -out srv.csr
openssl x509 -req -in srv.csr -CA int.crt -CAkey int.key -CAcreateserial -days 365 -sha256 \
    -extfile <(printf "subjectAltName=DNS:lab.local") -out srv.crt
# Verificación de la cadena
openssl verify -CAfile ca.crt -untrusted int.crt srv.crt   # => srv.crt: OK
```

Evidencia: el comando `openssl verify` devuelve `OK`; un cliente TLS que reciba `srv.crt || int.crt` valida hasta la raíz de confianza.

### Claves de los ejercicios

1. Cinco campos: `Subject`, `Issuer`, `Validity` (notBefore/notAfter), `Subject Public Key Info`, `Serial Number` (y extensiones como SAN, Basic Constraints, Key Usage).
2. Emite con `subjectAltName=DNS:a.lab,DNS:b.lab,IP:10.0.0.1` en `-extfile` y verifica con `openssl verify`; los navegadores exigen el nombre en SAN, no en CN.
3. CRL: lista completa periódica (alta latencia, sin fugas de privacidad en tiempo real). OCSP: consulta puntual (baja latencia, revela al respondedor qué sitio visitas). OCSP stapling: el servidor adjunta la respuesta firmada (baja latencia + privacidad).
4. CA raíz comprometida: el atacante emite certificados válidos para cualquier dominio → confianza global rota; por eso la raíz se mantiene offline y se usan intermedias revocables.
5. DigiNotar (2011): CA comprometida emitió certificados fraudulentos (p. ej. `*.google.com`) usados para MITM en Irán; resultado: eliminación de su raíz de todos los navegadores y quiebra.
6. ACME (Let's Encrypt): el cliente solicita, la CA plantea un reto (HTTP-01/DNS-01) para probar control del dominio, el cliente lo cumple, la CA valida y emite el certificado automáticamente.

---

## Clase 056 — TLS/SSL en profundidad

### Solución del reto verificable

Objetivo: servidor TLS de laboratorio que solo acepte TLS 1.3 con cipher suites AEAD y forward secrecy, presentando la cadena de la clase 055.

Pasos:

1. Sirve la cadena completa (`srv.crt` + intermedia) y limita a TLS 1.3.

```bash
openssl s_server -cert srv.crt -key srv.key -cert_chain int.crt \
    -tls1_3 -accept 4443 -www
# comprobación de versión y cipher
openssl s_client -connect lab.local:4443 -tls1_3 -servername lab.local </dev/null | \
    grep -E "Protocol|Cipher"
# auditoría
./testssl.sh --protocols --ciphers lab.local:4443
```

2. En un servidor real (nginx), fija `ssl_protocols TLSv1.3;` y confía en las cipher suites AEAD por defecto de TLS 1.3 (`TLS_AES_128_GCM_SHA256`, etc.).

Evidencia: `testssl.sh` no reporta protocolos viejos (SSLv3/TLS 1.0/1.1) ni cifrados débiles (RC4/3DES); la conexión negocia TLS 1.3 con ECDHE (forward secrecy) y el cliente valida la cadena hasta la raíz.

### Claves de los ejercicios

1. `TLS_AES_256_GCM_SHA384`: AEAD = AES-256-GCM (cifrado+autenticación); SHA384 = hash del HKDF/PRF; el intercambio de claves (ECDHE) y la firma se negocian aparte en TLS 1.3.
2. TLS 1.3 fusiona pasos: el cliente envía su key share en el ClientHello, el servidor responde con el suyo y ya deriva claves → 1-RTT frente al ida y vuelta extra de TLS 1.2.
3. Ejecuta `./testssl.sh host:443`; hallazgos típicos: versiones habilitadas, cipher suites, forward secrecy, vulnerabilidades conocidas (BEAST/POODLE/Heartbleed), calidad del certificado.
4. POODLE explotaba el padding de CBC en SSLv3; BEAST atacaba CBC en TLS 1.0 (IV predecible) → se retiraron SSLv3 y TLS 1.0/1.1.
5. Riesgo 0-RTT: los datos tempranos pueden ser reenviados (replay) por un atacante; mitiga limitándolos a peticiones idempotentes y con anti-replay (tickets de un solo uso).
6. En claro (TLS 1.2): ClientHello, ServerHello, certificado. En TLS 1.3 el certificado y el resto del handshake ya viajan cifrados tras el ServerHello.

---

## Clase 057 — Almacenamiento seguro de contraseñas: bcrypt, scrypt y Argon2

### Solución del reto verificable

Objetivo: módulo registro/login con Argon2id (salt automático, parámetros calibrados), verificación en tiempo constante y migrador que rehashea credenciales legacy al iniciar sesión.

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
import hashlib

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)

def registrar(pwd):           # salt aleatorio automático embebido en el hash
    return ph.hash(pwd)

def login(hash_guardado, pwd, es_legacy_sha256=False):
    if es_legacy_sha256:      # migración transparente de hashes viejos
        if hashlib.sha256(pwd.encode()).hexdigest() != hash_guardado:
            return None
        return ph.hash(pwd)   # rehash a Argon2id y persiste el nuevo
    try:
        ph.verify(hash_guardado, pwd)          # comparación en tiempo constante
        if ph.check_needs_rehash(hash_guardado):
            return ph.hash(pwd)                # sube el coste si cambió la política
        return hash_guardado
    except (VerifyMismatchError, InvalidHash):
        return None
```

Evidencia: dos usuarios con la misma contraseña obtienen hashes distintos (salt único); la verificación acepta la correcta y rechaza la incorrecta; las cuentas SHA-256 legacy se actualizan a Argon2id en el primer login exitoso.

### Claves de los ejercicios

1. Un salt único por usuario hace que el mismo password produzca hashes distintos → las rainbow tables precomputadas quedan inservibles (habría que recomputar por cada salt).
2. El pepper es un secreto global que va en un HSM/KMS o variable de entorno, **no** en la BD: si roban solo el dump, les falta el pepper para completar el ataque.
3. SHA-256 crackea a miles de millones de intentos/s (GPU); Argon2id, calibrado a cientos de ms y memory-hard, reduce ese ritmo en varios órdenes de magnitud → el mismo diccionario tarda muchísimo más.
4. Ajusta `time_cost`/`memory_cost` y mide con `timeit` hasta ~300 ms por hash en el hardware objetivo de producción.
5. bcrypt trunca a 72 bytes por su estructura basada en Blowfish; contraseñas más largas ignoran el exceso → usa pre-hash (SHA-256 → base64) o Argon2.
6. Migración: en cada login exitoso verifica con el hash viejo y, si es correcto, rehashea a Argon2id y reemplaza; marca la fila como migrada (rehash "al vuelo").

---

## Clase 058 — Generación de aleatoriedad segura (CSPRNG)

### Solución del reto verificable

Objetivo: utilidad que genere claves, nonces y tokens solo con CSPRNG, más un test que verifique ausencia de nonces repetidos y distribución de bits ~50/50.

```python
import os, secrets

def material():
    return {
        "clave": os.urandom(32),
        "nonce": os.urandom(12),
        "token": secrets.token_urlsafe(32),
    }

def test_no_repeticion(n=1_000_000):
    vistos = set()
    unos = total = 0
    for _ in range(n):
        v = os.urandom(12)
        assert v not in vistos, "nonce repetido!"
        vistos.add(v)
        b = int.from_bytes(v, "big"); unos += bin(b).count("1"); total += 96
    ratio = unos / total
    assert 0.49 < ratio < 0.51, ratio      # ~50 % de unos
```

Evidencia: sobre una muestra grande no hay nonces repetidos y la proporción de unos/ceros se desvía menos del umbral; el código no importa `random` (ningún PRNG estadístico).

### Claves de los ejercicios

1. `random` (Mersenne Twister) es un PRNG estadístico predecible si se conoce el estado; `secrets`/`os.urandom` usan el CSPRNG del SO → el correcto para seguridad.
2. `secrets.token_bytes(32)` = 256 bits: espacio de 2^256, imposible de adivinar o colisionar por fuerza bruta.
3. "Mining your Ps and Qs" (Heninger et al.): dispositivos con baja entropía en arranque generaron claves RSA que comparten un primo; con `gcd(n1, n2)` se factorizan al instante.
4. El kernel recolecta entropía de eventos con jitter (interrupciones, temporización de E/S, ruido de HW/RDRAND) y la mezcla en su pool para sembrar el CSPRNG.
5. Fija `random.seed(t)` con `t` conocido y muestra que `random.getrandbits` produce exactamente la misma secuencia → predecible si el atacante conoce el instante.
6. Genera datos con un CSPRNG y con un PRNG mal sembrado y corre `dieharder`/frecuencias: el PRNG débil muestra sesgos/patrones; el CSPRNG pasa las pruebas.

---

## Clase 059 — Cifrado autenticado (AEAD)

### Solución del reto verificable

Objetivo: contenedor de archivos con AES-GCM que autentique metadatos (nombre y versión) en el AAD y verifique integridad al abrir.

```python
import os, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def empaquetar(ruta, key, nombre, version):
    aad = json.dumps({"nombre": nombre, "version": version}, sort_keys=True).encode()
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, open(ruta, "rb").read(), aad)
    open(ruta + ".aead", "wb").write(len(aad).to_bytes(2,"big") + aad + nonce + ct)

def abrir(ruta_aead, key):
    blob = open(ruta_aead, "rb").read()
    la = int.from_bytes(blob[:2], "big")
    aad, nonce, ct = blob[2:2+la], blob[2+la:2+la+12], blob[2+la+12:]
    return AESGCM(key).decrypt(nonce, ct, aad)   # InvalidTag si algo cambió
```

Evidencia: el archivo se descifra solo con nonce, clave y AAD correctos; alterar un byte del cifrado o de los metadatos del AAD lanza `InvalidTag` sin exponer datos (fallo cerrado).

### Claves de los ejercicios

1. AEAD combina cifrado + autenticación en una primitiva probada, evitando errores de composición de "cifrar y luego HMAC" (orden incorrecto, claves mal separadas, MAC sobre el texto plano).
2. Cifra con AAD `b"v1"` y descifra con AAD `b"v2"`: lanza `InvalidTag` → el AAD se autentica aunque no se cifre.
3. En GCM, reutilizar nonce no solo revela `m1⊕m2` (como en CTR), sino que permite recuperar la clave de autenticación H y **forjar** tags → compromete también la integridad, no solo la confidencialidad.
4. `openssl speed`/benchmarks: AES-GCM gana con AES-NI+PCLMULQDQ; ChaCha20-Poly1305 gana en CPUs sin esas instrucciones (móviles/embebidos).
5. Formato `nonce(12) || ciphertext || tag(16)` autoexplicativo: el receptor separa por longitudes fijas y descifra.
6. AEAD verifica el tag antes de tocar el padding y falla de forma uniforme → no existe el oráculo de "padding válido/inválido" de CBC.

---

## Clase 060 — Ataques criptográficos: padding oracle y timing

### Solución del reto verificable

Objetivo: recuperar un texto plano completo de un oráculo de padding de laboratorio sin la clave, y luego mostrar que migrar a AEAD anula el ataque.

Fundamento (CBC + PKCS#7): para cada byte del bloque objetivo, modifica el byte correspondiente del bloque previo `C[i-1]` hasta que el oráculo diga "padding válido". Entonces el valor intermedio `I = C'[i-1] ⊕ padding_esperado`, y el texto plano `P[i] = I ⊕ C[i-1]_original`.

```python
# oracle(iv, ct) -> True si el padding descifrado es válido
def recupera_bloque(prev, blk, oracle):
    inter = bytearray(16)
    for pad in range(1, 17):
        forj = bytearray(16)
        for k in range(1, pad): forj[-k] = inter[-k] ^ pad
        for b in range(256):
            forj[-pad] = b
            if oracle(bytes(forj), blk):
                inter[-pad] = b ^ pad
                break
    return bytes(p ^ i for p, i in zip(prev, inter))   # texto plano del bloque
```

Evidencia: entregas el texto plano recuperado de la versión CBC vulnerable; tras reescribir el servicio con AES-GCM, cualquier manipulación devuelve solo `InvalidTag` uniforme y el ataque no recupera información.

### Claves de los ejercicios

1. CBC + verificación de padding: el servicio responde distinto según el padding sea válido o no → ese bit de información permite despejar byte a byte el valor intermedio.
2. Aplica `recupera_bloque` a cada par (bloque previo, bloque objetivo) del mensaje; documenta cómo cada byte válido revela un byte del intermedio y de ahí el plano.
3. Comparación ingenua byte a byte con salida temprana: mide miles de repeticiones y verás que un token con más prefijo correcto tarda ligeramente más (diferencia estadística).
4. Reescribe con AES-GCM: el `decrypt` verifica el tag antes del padding y falla uniforme → el oráculo desaparece.
5. Lucky 13 explotó diferencias de timing en el cálculo del MAC sobre el padding en TLS-CBC (MAC-then-Encrypt); mitigado con tiempo constante o AEAD.
6. Unifica los mensajes de error (mismo texto y mismo tiempo para "padding inválido" y "MAC inválido") y no reveles la causa al cliente ni en logs accesibles.

---

## Clase 061 — Introducción al criptoanálisis

### Solución del reto verificable

Objetivo: demostrar empíricamente la paradoja del cumpleaños — para varios `n`, generar valores aleatorios hasta la primera colisión, repetir y comparar la media con 2^(n/2).

```python
import os, statistics

def hasta_colision(n_bits):
    vistos, c = set(), 0
    while True:
        v = int.from_bytes(os.urandom(8), "big") % (1 << n_bits)
        c += 1
        if v in vistos: return c
        vistos.add(v)

for n in (16, 24, 32):
    medias = [hasta_colision(n) for _ in range(200)]
    print(n, round(statistics.mean(medias)), "~2^(n/2)=", 2 ** (n/2))
```

Evidencia: la media de intentos hasta colisión queda en el orden de `2^(n/2)` (constante ≈ 1.25·√(2^n)); se concluye que un hash de `n` bits ofrece solo ~`n/2` bits frente a colisiones (por eso SHA-256 da ~128).

### Claves de los ejercicios

1. Ejemplos: interceptar tráfico cifrado sin más = COA; conocer un fichero y su versión cifrada = KPA; poder cifrar textos elegidos (oráculo de cifrado) = CPA; poder descifrar cifrados elegidos (oráculo de descifrado) = CCA.
2. Para `n=32`, genera valores de 32 bits hasta colisión: la media ronda `2^16 ≈ 65.536`, no `2^32`.
3. 128 bits: `2^128 ≈ 3.4×10^38` operaciones; incluso a 10^18 ops/s son ~10^13 años → inviable.
4. DES (56 bits): `2^56` es forzable por hardware moderno en horas/días; AES-128 (`2^128`) queda fuera de alcance por muchos órdenes de magnitud.
5. Criptoanálisis diferencial: se introducen pares de entradas con una diferencia fija y se estudia qué diferencias de salida aparecen con probabilidad sesgada, distinguiendo el cifrado de una permutación aleatoria y recuperando bits de clave.
6. "Roto académicamente" = existe un ataque mejor que la fuerza bruta aunque siga siendo impracticable (p. ej. AES reducido a 7 rondas); "roto en la práctica" = explotable con recursos reales (MD5, SHA-1, DES).

---

## Clase 062 — Criptografía post-cuántica

### Solución del reto verificable

Objetivo: intercambio de claves **híbrido** (X25519 + KEM post-cuántico) que derive la clave de sesión con HKDF y cifre con AES-GCM; documentar por qué sigue seguro si una familia cae.

Estrategia: concatena los dos secretos compartidos y pásalos por HKDF (no XOR simple), de modo que romper el canal exija romper **ambos** esquemas.

```python
# Requiere oqs (liboqs-python) para ML-KEM; X25519 vía cryptography
import oqs, os
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Clásico
a = X25519PrivateKey.generate()
# ... intercambio de claves públicas ...
# ss_x = a.exchange(pub_b)

# Post-cuántico (ML-KEM / Kyber)
with oqs.KeyEncapsulation("ML-KEM-768") as kem:
    pk = kem.generate_keypair()
    ct, ss_pq = oqs.KeyEncapsulation("ML-KEM-768").encap_secret(pk)
    # ss_pq_dec = kem.decap_secret(ct)   # el otro lado

# Combinación híbrida: HKDF sobre ss_x || ss_pq
# secreto = ss_x + ss_pq
# key = HKDF(hashes.SHA256(), 32, None, b"hibrido").derive(secreto)
# AESGCM(key).encrypt(os.urandom(12), b"mensaje", None)
```

Evidencia: ambas partes derivan la misma `key` y descifran; se documenta que, al mezclar ambos secretos en el HKDF, un adversario que rompa solo X25519 (cuántica) o solo ML-KEM sigue sin conocer la clave de sesión.

### Claves de los ejercicios

1. Shor resuelve factorización y logaritmo discreto en tiempo polinómico → rompe RSA/DH/ECC. Grover solo da aceleración cuadrática en búsqueda → reduce AES-n a ~n/2 bits, no lo rompe.
2. Contra Grover, duplica el tamaño de clave simétrica: AES-256 conserva ~128 bits de seguridad post-cuántica.
3. ML-DSA (Dilithium) tiene claves y firmas de varios KB (p. ej. firma ~2–4 KB) frente a Ed25519 (clave 32 B, firma 64 B) → mucho mayores.
4. Handshake híbrido: cada parte hace X25519 y ML-KEM; se combinan ambos secretos en un KDF y de ahí sale la clave de sesión (seguro salvo que caigan los dos).
5. "Harvest now, decrypt later": prioriza datos con vida útil larga (historiales médicos, secretos de Estado, claves de firma raíz) que hoy se capturan y se descifrarían con cuánticas futuras.
6. FIPS 203 = ML-KEM (KEM, ex-Kyber); FIPS 204 = ML-DSA (firma, ex-Dilithium); FIPS 205 = SLH-DSA (firma basada en hash, ex-SPHINCS+); publicados por NIST en 2024.

---

## Clase 063 — Gestión de secretos: Vault y KMS

### Solución del reto verificable

Objetivo: envelope encryption — DEK por objeto cifrando datos con AES-GCM y protegiendo la DEK con el motor `transit` de Vault; solo se persisten el dato cifrado y la DEK cifrada; rotar la KEK no impide leer lo antiguo.

```bash
vault server -dev &
export VAULT_ADDR='http://127.0.0.1:8200'
vault secrets enable transit
vault write -f transit/keys/kek-maestra
```

```python
import os, base64, requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
H = {"X-Vault-Token": os.environ["VAULT_TOKEN"]}
BASE = "http://127.0.0.1:8200/v1/transit"

def guardar(dato):
    dek = AESGCM.generate_key(bit_length=256)
    n = os.urandom(12)
    ct = AESGCM(dek).encrypt(n, dato, None)
    # cifra la DEK con la KEK de Vault (la DEK en claro nunca se persiste)
    r = requests.post(f"{BASE}/encrypt/kek-maestra", headers=H,
                      json={"plaintext": base64.b64encode(dek).decode()})
    return {"nonce": n, "ct": ct, "dek_cifrada": r.json()["data"]["ciphertext"]}
```

Evidencia: para leer se pide a Vault descifrar `dek_cifrada` (endpoint `transit/decrypt`), se reconstruye la DEK en memoria y se descifra el dato; la DEK en claro nunca se escribe; tras `transit/keys/kek-maestra/rotate` los datos viejos siguen descifrándose (Vault conserva versiones anteriores de la KEK).

### Claves de los ejercicios

1. No guardar secretos en Git: quedan en el histórico para siempre (aunque se borren), se replican en cada clon y forks, y se filtran en repos públicos/logs de CI.
2. Jerarquía KEK/DEK: una DEK por tabla/objeto cifra los datos; la KEK (en KMS/HSM) cifra las DEKs; rotar la KEK solo re-cifra las DEKs, no todos los datos.
3. `vault kv put secret/app clave=valor` y desde el script `vault kv get -field=clave secret/app` (o vía API con el token).
4. HSM: hardware que custodia claves no exportables (ancla física). KMS: servicio gestionado de claves (a menudo sobre HSM) con cifrado como servicio. Vault: gestor de secretos con KV, secretos dinámicos y motor transit.
5. Detección de secretos filtrados: `gitleaks`/`git-secrets`/`trufflehog` escanean el árbol y el histórico buscando patrones (claves AWS, tokens) y entropía alta.
6. Política de rotación de API keys: expiración corta, rotación automatizada periódica, rotación inmediata ante sospecha, y solapamiento (dos claves válidas) para rotar sin downtime.

---

## Clase 064 — Esteganografía y ocultación de datos

### Solución del reto verificable

Objetivo: herramienta que cifre un mensaje con AES-GCM y lo oculte por LSB en una imagen PNG, más un extractor que recupere y descifre; describir la señal estadística que delata la ocultación.

```python
from PIL import Image
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def ocultar(cover, salida, mensaje, key):
    nonce = os.urandom(12)
    payload = nonce + AESGCM(key).encrypt(nonce, mensaje, None)
    payload = len(payload).to_bytes(4, "big") + payload    # prefijo de longitud
    bits = "".join(f"{b:08b}" for b in payload)
    img = Image.open(cover).convert("RGB"); px = img.load()
    i = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y]
            if i < len(bits): r = (r & ~1) | int(bits[i]); i += 1
            px[x, y] = (r, g, b)
    img.save(salida, "PNG")     # PNG: sin pérdida, preserva el LSB
```

Evidencia: el extractor lee los LSB del canal rojo, reconstruye `longitud || nonce || ct`, descifra con AES-GCM y recupera el mensaje intacto solo con la clave correcta; la imagen se ve idéntica. Señal delatora: el LSB deja de ser aleatorio → un test chi-cuadrado o el análisis de pares de valores (Sample Pairs) detecta la anomalía estadística.

### Claves de los ejercicios

1. Cifrado oculta el **contenido** (se ve que hay un mensaje cifrado); esteganografía oculta la **existencia** (parece una imagen normal). Ejemplo: un `.zip` cifrado es evidente; el mismo dato en el LSB de una foto, no.
2. Oculta con la función del reto y extrae leyendo los LSB hasta el terminador/longitud; verifica que el mensaje recuperado coincide.
3. Aplica chi-cuadrado sobre la distribución de LSB (o compara histogramas cover vs stego): el stego muestra desviación de la uniformidad esperada.
4. Cifrar-luego-ocultar: el cifrado protege el contenido si se detecta el portador; la esteganografía reduce la probabilidad de que sospechen. Defensa en profundidad de dos capas independientes.
5. Caso real: malware como Stegoloader, Lurk o campañas que ocultan payloads/C2 en imágenes PNG/JPEG o en publicaciones de redes sociales.
6. PNG (sin pérdida) preserva el LSB → alta capacidad e imperceptibilidad; JPEG recomprime con DCT y destruye los LSB espaciales → hay que ocultar en coeficientes DCT (menor capacidad).

---

## Clase 065 — Implementaciones seguras y errores criptográficos comunes

### Solución del reto verificable

Objetivo: corregir un módulo con ≥5 fallos criptográficos aplicando AEAD, nonces del CSPRNG, claves fuera del código, Argon2id y comparación en tiempo constante, con versión de formato para criptoagilidad.

Fallos del fragmento vulnerable y su corrección:

| Fallo | Corrección |
| --- | --- |
| Clave hardcodeada `KEY = b"..."` | Cárgala de variable de entorno / KMS / Vault |
| `modes.ECB()` | AES-GCM (AEAD) con nonce único |
| IV fijo `b"\x00"*16` | Nonce de 12 B con `os.urandom` por mensaje |
| `random.random()` para tokens | `secrets.token_urlsafe()` |
| Comparación `a == b` | `hmac.compare_digest(a, b)` |
| `md5(p)` para contraseña | Argon2id (`argon2-cffi`) |

```python
import os, secrets, hmac
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

VERSION = b"v1"                              # criptoagilidad: prefijo de formato
KEY = bytes.fromhex(os.environ["APP_KEY"])   # clave fuera del código
ph = PasswordHasher()

def cifrar(m):
    n = os.urandom(12)
    return VERSION + n + AESGCM(KEY).encrypt(n, m, VERSION)   # AAD = versión
def token():   return secrets.token_urlsafe(32)
def check(a, b): return hmac.compare_digest(a, b)
def pwd_hash(p): return ph.hash(p)
```

Evidencia: `bandit` no reporta fallos cripto de severidad media/alta en el módulo corregido; los tests de cifrado/descifrado y de autenticación pasan; `gitleaks`/grep confirman que ninguna clave o secreto aparece en el código.

### Claves de los ejercicios

1. Siete anti-patrones → corrección: clave en código → KMS/env; ECB → AEAD; IV/nonce fijo → CSPRNG único; `random` para tokens → `secrets`; `==` de secretos → `compare_digest`; MD5/SHA-256 para password → Argon2id; cripto casera → librería auditada.
2. Reescritura segura: ver el bloque de código del reto (AES-GCM, nonce CSPRNG, Argon2id, `compare_digest`, clave desde entorno, versión de formato).
3. `bandit archivo.py`: marca `B303` (MD5), `B311` (`random` inseguro), `B105/B106` (secreto hardcodeado); cada advertencia señala uno de los fallos del fragmento.
4. Formato con versión: `version(2B) || nonce(12B) || ciphertext || tag`; el prefijo permite cambiar algoritmo/parámetros sin ambigüedad al descifrar (criptoagilidad).
5. Audita TLS con `testssl.sh` (protocolos/cifrados) y el almacenamiento de contraseñas (que use Argon2id/bcrypt con salt y coste adecuado) → reporta ambos conjuntos de hallazgos.
6. "Reglas de oro": usa librerías auditadas, AEAD por defecto, nonces únicos del CSPRNG, KDFs lentas para contraseñas, comparación en tiempo constante, secretos fuera del código y criptoagilidad; nunca inventes tu propia cripto.
