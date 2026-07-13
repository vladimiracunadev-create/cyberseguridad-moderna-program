# Solución — Lo que esconde el binario

Deshaz el Base64 a binario y busca cadenas imprimibles:

```bash
echo 'iVBORw0KGgoAA/8AA/8AA/8AA/9tZXRhOmF1dG9yPWxhYjtGTEFHe3N0cmluZ3NfcmV2ZWxhX3RvZG99O2VuZAABAAEAAQAB' \
  | base64 -d > muestra.bin
strings muestra.bin
```

Entre los bytes aparece:

```text
meta:autor=lab;FLAG{strings_revela_todo};end
```

(La cabecera `\x89PNG` es un señuelo: el archivo no es una imagen válida.)

## Flag

```text
FLAG{strings_revela_todo}
```

**Lección:** `strings` es el primer paso del triaje forense y del análisis estático de
malware: revela rutas, dominios, claves y mensajes embebidos sin ejecutar nada
([Clase 143](../../../classes/parte-6-analisis-de-malware/143-analisis-estatico-basico/README.md)).
