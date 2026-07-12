# Parte 1 — Redes y seguridad de redes

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-2-criptografia-aplicada/README.md)

**20 clases** · rango 026–045 · Análisis de tráfico, escaneo, firewalls, IDS/IPS, VPN y monitoreo

**Fuentes de referencia de esta parte:**

- Chris Sanders — *Practical Packet Analysis* (3rd ed., No Starch Press, 2017).
- Gordon "Fyodor" Lyon — *Nmap Network Scanning* (Insecure.Com LLC, 2009). Referencia oficial también en <https://nmap.org/book/>.
- Richard Bejtlich — *The Practice of Network Security Monitoring* (No Starch Press, 2013).
- Chris Sanders & Jason Smith — *Applied Network Security Monitoring* (Syngress, 2014).
- Michael W. Lucas — *Absolute FreeBSD / PF* y documentación de nftables/iptables del kernel Linux.
- Estándares y proyectos: RFC 791/793 (IP/TCP), RFC 4301 (IPsec), NIST SP 800-207 (Zero Trust), documentación oficial de Wireshark, Suricata, Snort y Zeek.

---

## 🎯 ¿De qué trata esta parte?

Las redes son el sistema circulatorio de cualquier organización: todo dato sensible viaja por ellas en algún momento. Esta parte enseña a **ver** ese tráfico como lo ve un analista de seguridad, a **provocarlo** de forma controlada con herramientas de escaneo y enumeración, y a **defenderlo** con firewalls, sistemas de detección de intrusiones, cifrado de túneles y monitoreo continuo. Es la base técnica sobre la que se construyen el pentesting, la respuesta a incidentes y la ingeniería de detección.

Trabajamos con las herramientas que definen la profesión: Wireshark y tcpdump para análisis de paquetes, Nmap para descubrimiento y escaneo, iptables/nftables para filtrado, Snort y Suricata para detección basada en firmas, Zeek para análisis de metadatos a gran escala, y WireGuard/OpenVPN/IPsec para túneles cifrados. Cada clase combina teoría de protocolos (Ethernet, ARP, IP, TCP, UDP, DNS, TLS) con laboratorios reproducibles.

Sirve tanto al profesional **azul** (defensa, SOC, NSM, hardening de red) como al **rojo** (reconocimiento, pivoting, ataques de capa 2). Comprender ambos lados es el único camino para diseñar redes que resistan ataques reales.

## 🧩 Problemas que resuelve

- No saber qué protocolos y hosts realmente circulan por una red antes de asegurarla.
- Diagnosticar por qué una aplicación falla a nivel de red (retransmisiones, MTU, resets, latencia).
- Descubrir la superficie de ataque expuesta: hosts vivos, puertos abiertos, servicios y versiones.
- Filtrar y segmentar el tráfico con reglas de firewall correctas y auditables.
- Detectar intrusiones y comportamiento malicioso en tiempo casi real con IDS/IPS y NSM.
- Cifrar el tráfico entre sitios y usuarios remotos sin exponer claves ni rutas.
- Reconocer y mitigar ataques clásicos de red: ARP spoofing, MitM, envenenamiento de DNS, rogue AP.

## 🎓 Resultados de aprendizaje

Al terminar la parte, el alumno podrá:

- Capturar y disecar tráfico con Wireshark y tcpdump, aplicando filtros de captura y de visualización.
- Reconstruir flujos TCP/UDP y extraer artefactos (archivos, credenciales en claro, indicadores).
- Ejecutar escaneos Nmap completos: descubrimiento, puertos, versiones, OS y scripts NSE, e interpretar sus resultados.
- Escribir y depurar conjuntos de reglas de firewall con iptables y nftables.
- Desplegar y afinar reglas de Snort/Suricata y pipelines de Zeek para detección.
- Configurar túneles WireGuard, OpenVPN e IPsec con parámetros seguros.
- Identificar, reproducir en laboratorio y defenderse de ataques de capa 2, MitM y de DNS.
- Diseñar segmentación de red y una arquitectura Zero Trust básica alineada con NIST SP 800-207.

## 🧱 Prerrequisitos

Se asume la **Parte 0 — Fundamentos y prerrequisitos**: manejo de línea de comandos Linux, conceptos del modelo OSI/TCP-IP, direccionamiento IP y subredes, y un laboratorio virtualizado (VirtualBox/VMware/KVM) con al menos una VM atacante (Kali/Parrot) y una o dos víctimas aisladas en red interna (host-only). Familiaridad básica con Python ayuda en las clases de scripting.

## 🗺️ Estructura temática

| Bloque | Clases | Foco |
|-------|--------|------|
| Análisis de tráfico | 026–028 | Wireshark, filtros y flujos, tcpdump |
| Escaneo y enumeración (Nmap) | 029–033 | Descubrimiento, puertos, versiones, OS, NSE, enumeración |
| Defensa perimetral | 034–036 | Firewalls, IDS/IPS, VPN y túneles |
| Ataques de red | 037–041 | Proxies/NAT/pivoting, WiFi, capa 2, MitM, DNS |
| Arquitectura y monitoreo | 042–045 | Segmentación/Zero Trust, NSM, Zeek, NetFlow |

## 🔗 Referencias de la parte

- Sanders, C. *Practical Packet Analysis*, 3rd ed. No Starch Press. <https://nostarch.com/packetanalysis3>
- Lyon, G. *Nmap Network Scanning*. <https://nmap.org/book/>
- Bejtlich, R. *The Practice of Network Security Monitoring*. <https://nostarch.com/nsm>
- Sanders, C. & Smith, J. *Applied Network Security Monitoring*. Syngress.
- NIST SP 800-207 *Zero Trust Architecture*. <https://csrc.nist.gov/pubs/sp/800/207/final>
- Documentación oficial: Wireshark <https://www.wireshark.org/docs/>, Suricata <https://docs.suricata.io/>, Zeek <https://docs.zeek.org/>.

## ▶️ Empezar

[Clase 026 — Wireshark: captura y análisis de paquetes](026-wireshark-captura-y-analisis-de-paquetes/README.md)
