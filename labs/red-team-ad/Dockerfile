# Caja de operaciones del atacante (toolbox) para el laboratorio de Active Directory.
# Trae las herramientas ofensivas habituales para AD ya instaladas.
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        ldap-utils \
        smbclient \
        dnsutils \
        iputils-ping \
        netcat-openbsd \
        curl \
        git \
        build-essential \
        libkrb5-dev \
    && rm -rf /var/lib/apt/lists/*

# Impacket (secretsdump, GetUserSPNs, psexec...), ingestor de BloodHound y netexec.
RUN pip install --no-cache-dir \
        impacket \
        bloodhound \
        netexec

WORKDIR /work
CMD ["sleep", "infinity"]
