# Lab: Escaneo y enumeración de red (nmap)

Laboratorio para la **Parte 1 — Redes y seguridad de redes** (clases 026–045). Levanta varios
servicios (web, FTP, SSH) como **objetivos en una red aislada** y un contenedor `scanner` con
nmap para descubrirlos, escanearlos, identificar versiones y enumerarlos — como en un recon real.

> ⚠️ **Solo laboratorio.** Escanea únicamente estos contenedores (tuyos) u objetivos autorizados.
> Escanear redes ajenas puede ser ilegal.

## 🎯 Qué vas a practicar

| Objetivo | Clases |
|---|---|
| Descubrimiento de hosts y puertos | [029](../../classes/parte-1-redes-y-seguridad-de-redes/029-nmap-descubrimiento-de-hosts-y-tecnicas-de-ping/README.md), [030](../../classes/parte-1-redes-y-seguridad-de-redes/030-nmap-escaneo-de-puertos-y-tipos-de-escaneo/README.md) |
| Detección de servicios y OS | [031](../../classes/parte-1-redes-y-seguridad-de-redes/031-nmap-deteccion-de-servicios-y-fingerprinting-de-os/README.md) |
| Nmap Scripting Engine (NSE) | [032](../../classes/parte-1-redes-y-seguridad-de-redes/032-nmap-scripting-engine-nse/README.md) |
| Enumeración de servicios | [033](../../classes/parte-1-redes-y-seguridad-de-redes/033-enumeracion-de-servicios-de-red/README.md) |

## 🚀 Levantar el laboratorio

```bash
cd labs/redes-nmap
docker compose up -d
docker compose exec scanner sh      # entra al contenedor con nmap
```

Los objetivos son alcanzables por nombre dentro de la red: `web`, `ftp`, `ssh`.

## 🧭 Recorrido guiado (dentro del `scanner`)

```sh
# 1. Descubrir hosts vivos de la subred del lab
nmap -sn 172.16.0.0/16 2>/dev/null || nmap -sn web ftp ssh

# 2. Escaneo de puertos + versión + scripts por defecto
nmap -sV -sC web ftp ssh

# 3. Detección de OS y escaneo completo de un objetivo
nmap -O -p- web

# 4. NSE: enumerar el servicio FTP (¿login anónimo?) y HTTP
nmap --script ftp-anon,ftp-syst -p 21 ftp
nmap --script http-title,http-headers,http-enum -p 80 web

# 5. Enumerar SSH: algoritmos y métodos de autenticación
nmap --script ssh2-enum-algos,ssh-auth-methods -p 22 ssh
```

Opcional (análisis de tráfico): añade un servicio con `tshark`/`tcpdump` o captura desde el host.

## 🏆 Retos verificables

1. **Inventario:** entrega una tabla host → puertos → servicio → versión de los 3 objetivos. *Aceptación:* coincide con `-sV`.
2. **NSE:** determina si el FTP permite acceso anónimo y documéntalo con la salida del script.
3. **Sigilo vs ruido:** compara `-sS` (SYN) con `-sT` (connect) y explica la diferencia en las clases 030.
4. **Defensa:** propón cómo detectarías este escaneo desde el lado azul (relación con IDS, Parte 1 clase 035).

## 🧯 Apagar

```bash
docker compose down
```

## 🔗 Referencias

- Lyon — *Nmap Network Scanning* · [nmap.org](https://nmap.org/book/)
- Parte 1 del programa — [índice de clases](../../classes/README.md)
