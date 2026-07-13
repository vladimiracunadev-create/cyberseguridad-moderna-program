# Solución — Postal sin remitente

Convierte DMS → decimal:

```text
Lat = 48 + 51/60 + 30.13/3600 = 48.8584  N
Lon =  2 + 17/60 + 40.20/3600 =  2.2945  E
```

Busca `48.8584, 2.2945` en OpenStreetMap / Google Maps: cae exactamente en el **Campo de
Marte, junto a la Torre Eiffel**, en **París**.

```bash
# Si tuvieras la imagen original:
exiftool -gpslatitude -gpslongitude foto.jpg
```

## Flag

```text
FLAG{paris}
```

**Lección:** las fotos suelen llevar geolocalización en el EXIF; es OSINT de primer nivel para
ubicar personas o eventos. Al publicar, **elimina los metadatos**
([Clase 253](../../../classes/parte-12-osint-e-ingenieria-social/253-geolocalizacion-y-analisis-de-imagenes/README.md)).
