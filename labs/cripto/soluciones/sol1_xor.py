# -*- coding: utf-8 -*-
"""Solución Reto 1 — XOR de clave repetida (Python puro)."""
import os

RETO = os.path.join(os.path.dirname(__file__), "..", "retos", "reto1_xor.txt")
VOCALES = set(b"aeiou")


def puntua_byte(b: int) -> int:
    """Puntúa un carácter de texto plano candidato en español."""
    if b == 0x20:            # el espacio es el carácter más frecuente
        return 8
    if 0x61 <= b <= 0x7A:    # minúsculas
        return 5 if b in VOCALES else 3
    if 0x41 <= b <= 0x5A:    # mayúsculas
        return 1
    if b in b"_{}.,":        # puntuación esperada
        return 1
    if 0x20 <= b <= 0x7E:    # resto imprimible
        return 0
    return -6                # no imprimible: penaliza fuerte


def descifrar(ct: bytes, keylen: int) -> tuple[bytes, bytes]:
    clave = bytearray(keylen)
    for col in range(keylen):
        cuerpo = ct[col::keylen]
        mejor_b, mejor_score = 0, -(10 ** 9)
        for k in range(256):
            score = sum(puntua_byte(c ^ k) for c in cuerpo)
            if score > mejor_score:
                mejor_score, mejor_b = score, k
        clave[col] = mejor_b
    pt = bytes(c ^ clave[i % keylen] for i, c in enumerate(ct))
    return pt, bytes(clave)


def main() -> None:
    ct = bytes.fromhex(open(RETO, encoding="utf-8").read().strip())
    for keylen in range(1, 16):
        pt, clave = descifrar(ct, keylen)
        if b"FLAG{" in pt:
            print(f"[+] Longitud de clave: {keylen}")
            print(f"[+] Clave: {clave!r}")
            print(f"[+] Texto: {pt.decode(errors='replace')}")
            flag = pt[pt.index(b'FLAG{'):]
            print(f"[+] {flag[:flag.index(b'}')+1].decode()}")
            return
    print("[-] No se recuperó la flag; amplía el rango de longitudes de clave.")


if __name__ == "__main__":
    main()
