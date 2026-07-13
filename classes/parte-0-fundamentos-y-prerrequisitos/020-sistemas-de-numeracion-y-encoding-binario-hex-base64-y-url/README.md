# Clase 020 — Sistemas de numeración y encoding: binario, hex, base64 y URL

> Parte: **0 — Fundamentos y prerrequisitos** · Fuente: *RFC 4648 (Base16/32/64) y RFC 3986 (URI)*
> ⏱️ Duración estimada: **90 min** · Nivel: **Fundamentos**

---

## 🎯 Objetivo

Entender cómo se representan y transforman los datos, base para leer volcados hex, decodificar payloads, ofuscar/desofuscar cargas y trabajar con protocolos. Al terminar distinguirás con claridad **codificación** de **cifrado** y **hashing**, un error conceptual muy extendido.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Convertir** entre binario, decimal, octal y hexadecimal.
2. **Explicar** ASCII/Unicode y la diferencia bytes/texto.
3. **Codificar y decodificar** en Base64, hex y URL/percent.
4. **Distinguir** codificación, cifrado y hashing con criterio.
5. **Analizar** payloads codificados en un contexto de seguridad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Bases numéricas | Binario y hex están en todas partes |
| 2 | Conversión entre bases | Leer memoria, direcciones, máscaras |
| 3 | ASCII y Unicode | Texto ↔ bytes |
| 4 | Hex dump | Ver datos crudos |
| 5 | Base64 | Transportar binario como texto |
| 6 | URL/percent encoding | Datos en URLs y web |
| 7 | Encoding vs. cifrado vs. hash | Distinción conceptual crítica |
| 8 | Cadenas de encoding | Payloads con varias capas |

## 📖 Definiciones y características

- **Hexadecimal**: base 16 (0-9, A-F). Clave: cada dígito = 4 bits (nibble); 1 byte = 2 hex. Prefijo `0x`.
- **ASCII/Unicode**: mapeos de caracteres a números. Clave: UTF-8 codifica Unicode en bytes; distinguir carácter de byte es esencial.
- **Base64**: representa binario con 64 caracteres imprimibles. Clave: **no** cifra; es reversible por cualquiera. Aumenta el tamaño ~33%.
- **URL/percent encoding**: sustituye caracteres reservados por `%XX`. Clave: `%20` = espacio; usado para evadir filtros y en inyecciones web.
- **Codificación**: transformación reversible sin secreto. Clave: cualquiera la revierte; no aporta confidencialidad.
- **Hashing**: función unidireccional a un valor fijo. Clave: no reversible; verifica integridad, no oculta datos recuperables.

## 🧰 Herramientas y preparación

Herramientas: `xxd`/`hexdump`, `base64`, `python3` (`base64`, `binascii`, `urllib.parse`), y **CyberChef** (<https://gchq.github.io/CyberChef/>) para experimentar con cadenas de operaciones. Todo disponible en Kali o en el navegador.

## 🧪 Laboratorio guiado

1. **Conversión de bases** en Python:

   ```python
   n = 0xFF
   print(bin(n), oct(n), n)      # binario, octal, decimal
   print(int("11111111", 2), hex(255))
   ```

2. **Hex dump** de un archivo:

   ```bash
   echo -n "admin:1234" | xxd
   ```

   Relaciona cada byte con su carácter ASCII.
3. **Base64 ida y vuelta**:

   ```bash
   echo -n "usuario:secreto" | base64
   echo -n "dXN1YXJpbzpzZWNyZXRv" | base64 -d
   ```

   Observa que es trivialmente reversible (¡no es cifrado!).
4. **URL encoding** en Python:

   ```python
   from urllib.parse import quote, unquote
   print(quote("a b&c=1"))       # a%20b%26c%3D1
   print(unquote("%3Cscript%3E")) # <script>
   ```

5. **Cadena de encodings**. En CyberChef, toma un texto, aplícale Base64 y luego URL-encode; después reviértelo. Así se ven payloads "en capas".
6. **Diferenciar hashing**. Calcula el SHA-256 de "admin" y comprueba que **no** puedes recuperar "admin" de él (a diferencia de Base64).

## ✍️ Ejercicios

1. Convierte a mano `192` y `168` a binario y a hex; verifica con Python.
2. Decodifica una cabecera HTTP `Authorization: Basic ...` (Base64) y explica el riesgo.
3. Identifica si `5f4dcc3b5aa765d61d8327deb882cf99` es un hash o un encoding y de qué tipo.
4. Toma un payload XSS y aplícale URL encoding y HTML entity encoding; explica para qué sirve cada uno.
5. Escribe una función que detecte automáticamente si una cadena parece Base64, hex o URL-encoded.
6. Decodifica una cadena con doble Base64 y documenta cada capa.

## 📝 Reto verificable

Escribe `decoder.py`, una utilidad que reciba una cadena e intente detectar y decodificar automáticamente su capa externa (Base64, hex o percent-encoding), aplicándolo de forma recursiva hasta obtener texto legible o datos binarios. Debe informar de cada capa detectada y **negarse** a "decodificar" un hash, explicando por qué.

**Criterio de aceptación**: sobre una cadena con dos capas (p. ej. URL-encode de un Base64) la herramienta revela el texto original indicando ambas capas; ante un SHA-256 responde que es un hash irreversible en vez de intentar decodificarlo. Reproducible con ejemplos verificables en CyberChef.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Llamar "cifrado" a Base64 | Base64 es codificación reversible sin clave, no ofrece confidencialidad. Corrige el concepto. |
| Base64 no decodifica (padding) | Faltan `=` de relleno. Ajusta el padding o usa variantes URL-safe. |
| Caracteres raros al decodificar | Confundes bytes con texto. Trabaja en `bytes` y decodifica con la codificación correcta. |
| Intentar "revertir" un hash | Los hashes no se revierten; a lo sumo se comparan o se craquean por diccionario. |
| URL encode/decode inconsistente | `+` vs `%20` según contexto (form vs. path). Usa la función adecuada. |

## ❓ Preguntas frecuentes

**❓ ¿Base64 aporta algo de seguridad?** No en confidencialidad: cualquiera lo decodifica. Solo sirve para transportar binario por canales de texto. Nunca lo uses para "proteger" datos.

**❓ ¿Por qué los atacantes codifican payloads?** Para evadir filtros, WAFs o detección por firma. Ver una cadena Base64/hex/URL en un log suele merecer decodificarla y analizarla.

**❓ ¿Hashing es lo mismo que cifrado?** No. El cifrado es reversible con clave (confidencialidad); el hash es unidireccional (integridad). Lo vemos a fondo en la Clase 021.

**❓ ¿Qué es CyberChef?** Una "navaja suiza" web para encadenar operaciones de codificación, cifrado y análisis. Ideal para desofuscar payloads paso a paso.

## 🔗 Referencias

- RFC 4648, *Base16/Base32/Base64 Encodings* — <https://www.rfc-editor.org/rfc/rfc4648>
- RFC 3986, *URI Generic Syntax* — <https://www.rfc-editor.org/rfc/rfc3986>
- CyberChef — <https://gchq.github.io/CyberChef/>
- Unicode / UTF-8 (The Unicode Standard) — <https://home.unicode.org/>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-020-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-020-presentacion.pptx) — deck para proyectar en clase.

## ➡️ Siguiente clase

[Clase 021 - Criptografia: conceptos fundamentales e intuicion](../021-criptografia-conceptos-fundamentales-e-intuicion/README.md)
