# -*- coding: utf-8 -*-
"""Solución Reto 2 — RSA con primos cercanos (factorización de Fermat)."""
import math
import os

RETO = os.path.join(os.path.dirname(__file__), "..", "retos", "reto2_rsa.txt")


def leer_params(path: str) -> dict[str, int]:
    d = {}
    for linea in open(path, encoding="utf-8"):
        if "=" in linea:
            k, v = linea.split("=")
            d[k.strip()] = int(v.strip())
    return d


def fermat(n: int) -> tuple[int, int]:
    """Factoriza n = p*q cuando p y q son cercanos: n = a^2 - b^2 = (a-b)(a+b)."""
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1


def main() -> None:
    p_ = leer_params(RETO)
    n, e, c = p_["n"], p_["e"], p_["c"]
    p, q = fermat(n)
    print(f"[+] p = {p}")
    print(f"[+] q = {q}")
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, n)
    flag = m.to_bytes((m.bit_length() + 7) // 8, "big")
    print(f"[+] {flag.decode(errors='replace')}")


if __name__ == "__main__":
    main()
