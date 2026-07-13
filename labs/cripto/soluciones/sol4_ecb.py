# -*- coding: utf-8 -*-
"""Solución Reto 4 — detección de modo AES-ECB por bloques repetidos."""
import os

RETO = os.path.join(os.path.dirname(__file__), "..", "retos", "reto4_ecb.txt")


def main() -> None:
    ct = bytes.fromhex(open(RETO, encoding="utf-8").read().strip())
    bloques = [ct[i:i + 16] for i in range(0, len(ct), 16)]
    vistos: dict[bytes, list[int]] = {}
    for i, b in enumerate(bloques):
        vistos.setdefault(b, []).append(i)
    repetidos = {b: pos for b, pos in vistos.items() if len(pos) > 1}
    print(f"[+] Bloques totales: {len(bloques)} | únicos: {len(vistos)}")
    if repetidos:
        print("[+] MODO ECB DETECTADO: hay bloques de 16 bytes idénticos.")
        for b, pos in repetidos.items():
            print(f"    bloque {b.hex()} aparece en posiciones {pos}")
        print("[i] En ECB, plaintext idéntico -> ciphertext idéntico. Usa un modo con IV (CBC/CTR) o AEAD (GCM).")
    else:
        print("[-] No hay bloques repetidos: no parece ECB.")


if __name__ == "__main__":
    main()
