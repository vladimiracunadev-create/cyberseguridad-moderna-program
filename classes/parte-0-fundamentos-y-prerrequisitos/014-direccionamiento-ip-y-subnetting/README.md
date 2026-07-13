# Clase 014 — Direccionamiento IP y subnetting

> Parte: **0 — Fundamentos y prerrequisitos** · Fuente: *RFC 4632 (CIDR) y W. R. Stevens, TCP/IP Illustrated*
> ⏱️ Duración estimada: **100 min** · Nivel: **Fundamentos**

---

## 🎯 Objetivo

Calcular subredes con soltura, algo que necesitarás constantemente para definir el alcance de un escaneo, segmentar una red o interpretar un rango objetivo. Al terminar sabrás pasar entre notación decimal, binaria y CIDR, calcular direcciones de red, broadcast, rango de hosts y dividir una red en subredes.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Convertir** direcciones IP entre decimal y binario.
2. **Interpretar** máscaras de red y notación CIDR.
3. **Calcular** red, broadcast, primer/último host y número de hosts.
4. **Dividir** una red en subredes (subnetting/VLSM).
5. **Reconocer** rangos privados, especiales y su relevancia en seguridad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | IPv4 y binario | Todo el cálculo vive en bits |
| 2 | Máscara de red | Separa red de host |
| 3 | Notación CIDR | `/24` es el lenguaje del día a día |
| 4 | Red y broadcast | Direcciones no asignables a hosts |
| 5 | Cálculo de hosts | `2^n - 2` utilizables |
| 6 | Subnetting | Partir una red en varias |
| 7 | VLSM | Subredes de tamaño variable |
| 8 | Rangos especiales | Privados, loopback, APIPA, IPv6 básico |

## 📖 Definiciones y características

- **Máscara de red**: patrón de bits que separa la porción de red de la de host. Clave: `/24` = `255.255.255.0` = 24 bits de red.
- **CIDR**: notación `IP/prefijo` que reemplazó las clases A/B/C. Clave: permite prefijos arbitrarios y agregación de rutas.
- **Dirección de red**: primera del bloque, con todos los bits de host a 0. Clave: no se asigna a hosts.
- **Broadcast**: última del bloque, con todos los bits de host a 1. Clave: tampoco es asignable.
- **Hosts utilizables**: `2^(bits de host) − 2`. Clave: se restan red y broadcast (salvo /31, /32).
- **Rangos privados (RFC 1918)**: `10/8`, `172.16/12`, `192.168/16`. Clave: no enrutables en Internet; típicos de laboratorios y LAN.

## 🧰 Herramientas y preparación

Bastan papel y lápiz para aprender de verdad. Para verificar: `ipcalc` (Linux), `sipcalc`, o la calculadora del sistema en modo programador. En Kali:

```bash
sudo apt install ipcalc sipcalc
```

Evita depender de calculadoras online al principio: el objetivo es entender el cálculo, no automatizarlo.

## 🧪 Laboratorio guiado

1. **Decimal a binario**. Convierte a mano `192.168.10.0` y `255.255.255.192` a binario. Verifica:

   ```bash
   ipcalc 192.168.10.0/26
   ```

2. **Analiza un bloque /24**. Para `10.10.10.0/24` determina: máscara, dirección de red, broadcast, primer y último host, número de hosts.
3. **Subnetear**. Divide `192.168.1.0/24` en 4 subredes iguales (/26). Escribe para cada una: red, rango de hosts y broadcast.
4. **Verifica** con la herramienta:

   ```bash
   ipcalc 192.168.1.0/24 -s 62 62 62 62
   sipcalc 192.168.1.0/26
   ```

5. **VLSM**. Dado `172.16.0.0/16`, diseña subredes para: 500 hosts, 100 hosts, 25 hosts y un enlace punto a punto (2 hosts). Elige la máscara mínima adecuada para cada una.
6. **Rangos especiales**. Clasifica: `127.0.0.1`, `169.254.5.5`, `10.0.0.1`, `8.8.8.8`. Indica cuáles son públicos, privados, loopback o APIPA.

## ✍️ Ejercicios

1. ¿Cuántos hosts utilizables tiene un `/22`? ¿Y un `/30`?
2. Para `10.20.30.45/27`, calcula la dirección de red y el broadcast.
3. Divide `192.168.100.0/24` en 8 subredes; da la 3ª subred completa.
4. Diseña con VLSM un plan para 3 departamentos de 60, 30 y 10 hosts partiendo de un /24.
5. Explica por qué un `/31` puede usarse en enlaces punto a punto pese a la regla `−2`.
6. Determina si `192.168.5.130` y `192.168.5.200` están en la misma subred `/26`.

## 📝 Reto verificable

Diseña un plan de direccionamiento para una organización ficticia con cuatro segmentos de distinto tamaño (por ejemplo 200, 60, 12 y un enlace WAN) partiendo de un único bloque `/23`, usando VLSM para no desperdiciar direcciones. Entrega una tabla con red, máscara, rango de hosts y broadcast de cada segmento.

**Criterio de aceptación**: las subredes no se solapan, cada una tiene la máscara mínima que satisface su número de hosts, y la suma cabe en el `/23` asignado. Verificable con `ipcalc`/`sipcalc` sobre cada subred de la tabla.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Olvidar restar red y broadcast | Los hosts utilizables son `2^n − 2`, no `2^n`. |
| Subredes solapadas en VLSM | Asignaste sin ordenar por tamaño. Empieza por la subred más grande. |
| Confundir `/24` con `255.255.0.0` | `/24` es `255.255.255.0`. Cuenta los bits a 1. |
| Poner un host en la dirección de red o broadcast | No son asignables (salvo /31, /32). Usa el rango intermedio. |
| Mezclar bits de red al subnetear | Trabaja en binario para ver claramente la frontera red/host. |

## ❓ Preguntas frecuentes

**❓ ¿Por qué importa el subnetting en seguridad?** Define el alcance: un `/24` son 254 hosts a escanear; equivocarte de máscara deja objetivos fuera o incluye redes que no debías tocar. También es la base de la segmentación defensiva.

**❓ ¿Sigo necesitando saber esto con IPv6?** IPv6 usa prefijos igual (p. ej. `/64`), aunque el cálculo de hosts cambia por su tamaño. Los conceptos de red/prefijo se trasladan.

**❓ ¿Puedo usar siempre una calculadora?** Para trabajar sí, pero entender el cálculo te permite razonar rangos al vuelo durante un pentest y detectar errores de la herramienta.

**❓ ¿Qué es APIPA (169.254.x.x)?** Direcciones autoasignadas cuando falla DHCP. Verlas suele indicar un problema de red, útil como señal diagnóstica.

## 🔗 Referencias

- RFC 4632 (CIDR) — <https://www.rfc-editor.org/rfc/rfc4632>
- RFC 1918 (direcciones privadas) — <https://www.rfc-editor.org/rfc/rfc1918>
- `man 1 ipcalc`, `man 1 sipcalc`
- Cisco: Subnetting básico — <https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html>

## ➡️ Siguiente clase

[Clase 015 - Python para seguridad: fundamentos del lenguaje](../015-python-para-seguridad-fundamentos-del-lenguaje/README.md)
