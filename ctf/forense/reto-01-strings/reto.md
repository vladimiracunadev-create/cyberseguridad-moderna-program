# 🔬 Forense — Lo que esconde el binario ⭐

Recuperamos un archivo sospechoso de un disco. Te lo damos en Base64 (para transportarlo
como texto). Dentro, entre bytes binarios, hay una cadena legible con la flag.

```text
iVBORw0KGgoAA/8AA/8AA/8AA/9tZXRhOmF1dG9yPWxhYjtGTEFHe3N0cmluZ3NfcmV2ZWxhX3RvZG99O2VuZAABAAEAAQAB
```

**Pista:** primero deshaz el Base64 y guárdalo como binario; luego extrae las cadenas
imprimibles (`strings`).

➡️ ¿Atascado? Mira [`solucion.md`](solucion.md).
