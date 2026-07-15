#!/usr/bin/env bash
# Compila el reto con las protecciones DESACTIVADAS (solo laboratorio didáctico):
#   -fno-stack-protector : sin stack canary
#   -z execstack         : stack ejecutable
#   -no-pie              : direcciones fijas (sin PIE)  · -m32 : 32 bits (más simple)
set -e
gcc -m32 -fno-stack-protector -z execstack -no-pie -o reto1_overflow reto1_overflow.c
echo "[+] Compilado: reto1_overflow (32-bit, sin canary, NX off, sin PIE)"
