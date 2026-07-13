# -*- coding: utf-8 -*-
"""
Genera los artefactos de los retos de criptografía (datos de entrada).
Reproducible y en Python puro (sin dependencias externas). No es parte del reto;
documenta cómo se crearon los datos de retos/.

Uso: python labs/cripto/_generar_retos.py
"""
from __future__ import annotations
import hashlib
import os
import random

AQUI = os.path.dirname(os.path.abspath(__file__))
RETOS = os.path.join(AQUI, "retos")
os.makedirs(RETOS, exist_ok=True)

# Semilla fija -> generación determinista (no usar aleatoriedad real de reloj).
rnd = random.Random(1337)


def escribir(nombre: str, contenido: str) -> None:
    with open(os.path.join(RETOS, nombre), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)


# ---------- Reto 1: XOR de clave repetida ----------
def reto_xor() -> None:
    clave = b"llave"
    flag = b"Este mensaje se cifro con XOR de clave repetida. FLAG{xor_no_es_cifrado_seguro}"
    ct = bytes(b ^ clave[i % len(clave)] for i, b in enumerate(flag))
    escribir("reto1_xor.txt", ct.hex() + "\n")


# ---------- Reto 2: RSA con módulo factorizable (primos cercanos -> Fermat) ----------
def es_primo(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def sig_primo(n: int) -> int:
    n |= 1
    while not es_primo(n):
        n += 2
    return n


def reto_rsa() -> None:
    p = sig_primo(rnd.getrandbits(256))
    q = sig_primo(p + rnd.randint(2, 5000) * 2)  # q MUY cercano a p -> Fermat trivial
    n = p * q
    e = 65537
    flag = b"FLAG{rsa_con_primos_cercanos_cae_con_fermat}"
    m = int.from_bytes(flag, "big")
    assert m < n
    c = pow(m, e, n)
    escribir("reto2_rsa.txt", f"n = {n}\ne = {e}\nc = {c}\n")


# ---------- Reto 3: cracking de hashes MD5 sin sal ----------
def reto_hashes() -> None:
    diccionario = [
        "123456", "password", "qwerty", "letmein", "dragon", "monkey",
        "correcthorsebatterystaple", "P@ssw0rd", "verano2026", "ninja",
        "admin123", "s3cr3t", "hunter2", "iloveyou", "trustno1",
    ]
    escribir("diccionario.txt", "\n".join(diccionario) + "\n")
    # Estas 3 contraseñas SÍ están en el diccionario; la gracia es identificarlas.
    objetivo = ["P@ssw0rd", "correcthorsebatterystaple", "verano2026"]
    hashes = [hashlib.md5(p.encode()).hexdigest() for p in objetivo]
    escribir("reto3_hashes.txt", "\n".join(hashes) + "\n")


# ---------- Reto 4: detección de AES-ECB ----------
def reto_ecb() -> None:
    # Ciphertext hexadecimal de 8 bloques de 16 bytes. Dos bloques son IDÉNTICOS
    # (delatan modo ECB: mismo plaintext -> mismo ciphertext).
    bloques = [bytes(rnd.getrandbits(8) for _ in range(16)) for _ in range(6)]
    repetido = bloques[2]
    ct = bloques[0] + bloques[1] + repetido + bloques[3] + repetido + bloques[4] + bloques[5] + bloques[1]
    escribir("reto4_ecb.txt", ct.hex() + "\n")


if __name__ == "__main__":
    reto_xor()
    reto_rsa()
    reto_hashes()
    reto_ecb()
    print("Retos generados en", RETOS)
