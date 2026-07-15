# Lab: Seguridad en la nube y contenedores (auditoría)

Laboratorio para la **Parte 10 — Seguridad en la nube y contenedores** (clases 221–235). Un
toolbox con **Prowler, ScoutSuite, trivy y kube-bench** para auditar la postura de seguridad
(CSPM) de tu propia cuenta de nube o de un clúster local — todo con herramientas de **solo lectura**.

> ⚠️ **Solo cuentas propias/autorizadas y de laboratorio.** Usa credenciales con permisos de
> **solo lectura** (p. ej. la política `SecurityAudit` de AWS). Nunca audites una cuenta de
> producción ajena. Estas herramientas no modifican tu infraestructura, pero sí leen su config.

## 🎯 Qué vas a practicar

| Objetivo | Clases |
|---|---|
| Postura de seguridad en la nube (CSPM) | [231](../../classes/parte-10-seguridad-en-la-nube-y-contenedores/231-cloud-security-posture-management-cspm/README.md) |
| IAM y responsabilidad compartida | [221](../../classes/parte-10-seguridad-en-la-nube-y-contenedores/221-fundamentos-de-seguridad-en-la-nube-y-responsabilidad-compartida/README.md), [222](../../classes/parte-10-seguridad-en-la-nube-y-contenedores/222-iam-en-la-nube-identidades-roles-y-permisos/README.md) |
| Hardening de Kubernetes | [229](../../classes/parte-10-seguridad-en-la-nube-y-contenedores/229-kubernetes-hardening-y-ataques/README.md) |
| Seguridad de contenedores | [227](../../classes/parte-10-seguridad-en-la-nube-y-contenedores/227-seguridad-de-contenedores-docker/README.md) |

## 🚀 Levantar el toolbox

```bash
cd labs/cloud-security
docker compose build
docker compose up -d
docker compose exec auditor bash
```

Descomenta en `docker-compose.yml` el volumen de credenciales que uses (`~/.aws`, `~/.kube`…),
**siempre de solo lectura**.

## 🧭 Recorrido guiado

### A) Auditar una cuenta de nube (CSPM)

```bash
# AWS (con un perfil de solo lectura tipo SecurityAudit)
prowler aws --profile lab-readonly -M csv html -o /audit/salida

# Multi-cloud alternativo
scout aws --report-dir /audit/salida
```

Revisa el informe: IAM permisivo, buckets públicos, cifrado ausente, logging desactivado…
Clasifica los hallazgos por severidad y contexto (clase 231).

### B) Auditar contenedores e IaC

```bash
# Vulnerabilidades y misconfig de una imagen
trivy image nginx:latest

# Misconfiguraciones en Infraestructura como Código (Terraform, k8s manifests)
trivy config ./ruta/a/tu/iac
```

### C) Hardening de Kubernetes (con un clúster propio, p. ej. kind)

```bash
# Ejecuta el CIS Benchmark contra tu clúster de laboratorio
kube-bench run --targets master,node
```

## 🏆 Retos verificables

1. **Top hallazgos:** ejecuta Prowler/ScoutSuite sobre tu cuenta de laboratorio y entrega los 5 hallazgos más críticos con su severidad.
2. **Remediación:** corrige 3 de ellos y vuelve a escanear para demostrar que desaparecen. *Aceptación:* diff antes/después.
3. **Contenedor:** encuentra una imagen con CVEs críticos con `trivy` y propón la versión parcheada.
4. **Kubernetes:** de `kube-bench`, elige 3 controles fallidos y explica cómo remediarlos.

## 🧯 Apagar

```bash
docker compose down
```

## 🔗 Referencias

- [Prowler](https://github.com/prowler-cloud/prowler) · [ScoutSuite](https://github.com/nccgroup/ScoutSuite) · [Trivy](https://trivy.dev/) · [kube-bench](https://github.com/aquasecurity/kube-bench)
- Rice — *Container Security* · Martin — *Hacking Kubernetes*.
- Parte 10 del programa — [índice de clases](../../classes/README.md)
