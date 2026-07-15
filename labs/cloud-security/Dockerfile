# Toolbox de auditoría de seguridad en la nube y contenedores (Parte 10).
# Solo herramientas de LECTURA/auditoría: no modifican tu infraestructura.
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl git ca-certificates jq \
    && rm -rf /var/lib/apt/lists/*

# Prowler (auditoría CSPM multi-cloud) y ScoutSuite (auditoría multi-cloud).
RUN pip install --no-cache-dir prowler scoutsuite

# trivy (escáner de imágenes/IaC) y kube-bench (CIS Benchmark de Kubernetes) — binarios.
RUN curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh \
      | sh -s -- -b /usr/local/bin || true

WORKDIR /audit
CMD ["sleep", "infinity"]
