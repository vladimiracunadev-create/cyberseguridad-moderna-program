# Clase 053 — Intercambio de claves: Diffie-Hellman

> Parte: **2 — Criptografía aplicada** · Fuente: *Real-World Cryptography* (Wong) y *Serious Cryptography* (Aumasson)
> ⏱️ Duración estimada: **100 min** · Nivel: **Avanzado**

---

## 🎯 Objetivo

Comprender cómo dos partes que nunca se han visto pueden acordar una clave secreta compartida sobre un canal público, mediante Diffie-Hellman (DH) y su variante de curva elíptica (ECDH). El alumno entenderá el problema del logaritmo discreto, la diferencia entre DH estático y efímero, el concepto de **forward secrecy** y por qué DH sin autenticación es vulnerable a un ataque de intermediario (MITM).

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Ejecutar** el protocolo DH paso a paso con números y explicar por qué funciona.
2. **Distinguir** DH estático de efímero (DHE/ECDHE) y su relación con forward secrecy.
3. **Demostrar** por qué DH sin autenticación cae ante MITM.
4. **Derivar** una clave de sesión a partir del secreto compartido con HKDF.
5. **Elegir** parámetros seguros (grupos MODP fuertes o X25519).

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Problema del logaritmo discreto | Base de la seguridad |
| 2 | DH clásico (grupos multiplicativos) | Protocolo fundacional |
| 3 | ECDH / X25519 | Variante moderna eficiente |
| 4 | Efímero vs estático | Forward secrecy |
| 5 | Derivación de clave (HKDF) | Del secreto bruto a claves útiles |
| 6 | MITM y necesidad de autenticación | DH solo no autentica |
| 7 | Parámetros seguros | Evitar grupos débiles (Logjam) |

## 📖 Definiciones y características

- **Diffie-Hellman**: protocolo donde cada parte elige un secreto, publica `gˣ mod p` y ambos calculan `gˣʸ`. Característica: acuerdan clave sin transmitirla.
- **Problema del logaritmo discreto**: dado `g`, `p` y `gˣ mod p`, hallar `x` es inviable con parámetros grandes.
- **DHE / ECDHE (efímero)**: se genera un par nuevo por sesión; aporta forward secrecy.
- **Forward secrecy**: comprometer la clave de largo plazo no descifra sesiones pasadas, porque los efímeros ya se descartaron.
- **HKDF**: función de derivación (extract-then-expand) que convierte el secreto compartido en claves de longitud y propósito adecuados.
- **MITM**: sin autenticación, un atacante intercepta y sustituye las claves públicas, estableciendo dos canales que él controla.
- **Grupos MODP / Curve25519**: parámetros recomendados; evitar primos pequeños o de origen dudoso (Logjam).

## 🧰 Herramientas y preparación

```bash
openssl version
pip install cryptography
```

Laboratorio local. El MITM se simula solo entre procesos propios.

## 🧪 Laboratorio guiado

1. **DH de juguete a mano**. Con `p=23`, `g=5`, Alice elige `a=6` y Bob `b=15`. Calcula `A=5⁶ mod 23`, `B=5¹⁵ mod 23` y verifica que `Bᵃ mod 23 = Aᵇ mod 23`. Ese es el secreto compartido.

2. **ECDH con X25519 y HKDF en Python**:

   ```python
   from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
   from cryptography.hazmat.primitives.kdf.hkdf import HKDF
   from cryptography.hazmat.primitives import hashes
   a = X25519PrivateKey.generate(); b = X25519PrivateKey.generate()
   shared = a.exchange(b.public_key())
   key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
              info=b"canal").derive(shared)
   print(key.hex())
   ```

3. **Simula un MITM**. Coloca un "atacante" entre A y B que reemplaza cada clave pública por la suya. Comprueba que A y B acaban con claves distintas que el atacante conoce → demuestra la necesidad de autenticar (certificados/firmas).

4. **Forward secrecy**. Genera efímeros por sesión y razona por qué revelar la clave estática no compromete sesiones antiguas.

## ✍️ Ejercicios

1. Repite el DH de juguete con `p=97, g=5` y valores propios.
2. Explica por qué `gˣʸ = gʸˣ` permite el acuerdo.
3. Implementa el MITM y muéstralo funcionando en tu laboratorio.
4. Investiga el ataque Logjam y qué grupos evitar.
5. Deriva dos claves (cifrado y MAC) del mismo secreto con HKDF e `info` distintos.
6. Compara DHE clásico con ECDHE en rendimiento y tamaño.

## 📝 Reto verificable

Implementa un handshake ECDHE **autenticado**: cada parte firma su clave pública efímera con Ed25519 (clave de largo plazo) y verifica la del otro antes de derivar la clave de sesión. **Criterio de aceptación**: un MITM que altere las claves efímeras es detectado porque la firma no valida, y el canal solo se establece entre las partes legítimas.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| DH sin autenticación | Vulnerable a MITM; añade firmas o certificados |
| Usar el secreto DH directamente como clave | Deriva con HKDF; el secreto bruto no es uniforme |
| Grupos DH pequeños o compartidos débiles | Logjam; usa ≥2048 bits o X25519 |
| DH estático sin forward secrecy | Compromiso futuro descifra el pasado; usa efímeros |
| Reutilizar el par efímero | Anula forward secrecy; genera uno por sesión |

## ❓ Preguntas frecuentes

**❓ ¿DH cifra datos?**
No; solo acuerda una clave. Luego cifras con AES/ChaCha20 usando esa clave derivada.

**❓ ¿Qué es forward secrecy y por qué importa?**
Que capturar tráfico hoy y robar la clave del servidor mañana no permite descifrarlo, gracias a los efímeros. TLS 1.3 lo exige.

**❓ ¿DH resiste cuántica?**
No; cae ante Shor, igual que RSA/ECC. De ahí la cripto post-cuántica.

## 🔗 Referencias

- Wong, *Real-World Cryptography*, cap. 5.
- Aumasson, *Serious Cryptography*, cap. 11.
- RFC 5869 (HKDF) — <https://www.rfc-editor.org/rfc/rfc5869>
- Adrian et al., "Imperfect Forward Secrecy / Logjam" — <https://weakdh.org/>

## ➡️ Siguiente clase

[Clase 054 - Firmas digitales](../054-firmas-digitales/README.md)
