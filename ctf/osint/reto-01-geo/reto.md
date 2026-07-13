# 🔎 OSINT — Postal sin remitente ⭐⭐

Nos llegó una foto sin descripción. Su metadato EXIF (extraído con `exiftool`) trae las
coordenadas GPS donde se tomó. ¿En qué **ciudad** fue? La flag es `FLAG{ciudad_en_minusculas}`.

```text
GPS Latitude Ref              : North
GPS Longitude Ref             : East
GPS Latitude                  : 48 deg 51' 30.13" N
GPS Longitude                 : 2 deg 17' 40.20" E
GPS Altitude                  : 45 m
Make                          : Canon
Model                         : Canon EOS 250D
```

**Pista:** convierte los grados/minutos/segundos (DMS) a decimal y búscalo en un mapa. El
punto está junto a un monumento muy famoso.

➡️ ¿Atascado? Mira [`solucion.md`](solucion.md).
