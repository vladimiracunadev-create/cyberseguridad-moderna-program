#!/usr/bin/env bash
# Ejecuta SAST sobre la app vulnerable. Usa el contenedor oficial de Semgrep
# (no requiere instalar nada) y, si está disponible, también Bandit.
set -euo pipefail
cd "$(dirname "$0")"

echo "== Semgrep (reglas automáticas) =="
if command -v semgrep >/dev/null 2>&1; then
  semgrep --config auto vulnerable_app || true
else
  docker run --rm -v "$(pwd)":/src semgrep/semgrep \
    semgrep --config auto /src/vulnerable_app || true
fi

echo
echo "== Bandit (SAST específico de Python) =="
if command -v bandit >/dev/null 2>&1; then
  bandit -r vulnerable_app || true
else
  echo "(bandit no instalado: 'pip install bandit' para esta parte)"
fi

echo
echo "Compara los hallazgos con SOLUCION.md. ¿Encontró el SAST las 8? ¿Algún falso positivo?"
