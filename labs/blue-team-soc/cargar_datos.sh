#!/usr/bin/env bash
# Carga los eventos de muestra en Elasticsearch (índice: eventos-auth).
# Uso: ./cargar_datos.sh   (con el lab levantado: docker compose up -d)
set -euo pipefail

ES="http://127.0.0.1:9200"
INDICE="eventos-auth"
DATOS="$(dirname "$0")/datos/auth-events.ndjson"

echo "[*] Esperando a que Elasticsearch responda en ${ES} ..."
until curl -sf "${ES}/_cluster/health" >/dev/null; do sleep 3; done

echo "[*] Recreando el índice ${INDICE} ..."
curl -s -X DELETE "${ES}/${INDICE}" >/dev/null || true

echo "[*] Cargando eventos ..."
curl -s -H "Content-Type: application/x-ndjson" \
  -X POST "${ES}/${INDICE}/_bulk?refresh" \
  --data-binary "@${DATOS}" | grep -o '"errors":[a-z]*' || true

echo
echo "[+] Listo. Documentos indexados:"
curl -s "${ES}/${INDICE}/_count" | tr -d '{}"'
echo "[+] Abre Kibana en http://127.0.0.1:5601  ->  Discover  ->  crea un data view sobre 'eventos-auth'."
