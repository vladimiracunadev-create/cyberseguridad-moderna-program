# Parte 10 — Seguridad en la nube y contenedores

> [⬅️ Volver al programa](../../README.md) · [📚 Índice completo](../README.md) · [⏭️ Parte siguiente](../parte-11-devsecops-y-seguridad-del-sdlc/README.md)

**15 clases** · rango 221–235 · AWS, Azure, GCP, IAM, Docker, Kubernetes e IaC

**Fuentes de referencia de esta parte:**

- Liz Rice — *Container Security* (O'Reilly, 2020).
- Andrew Martin & Michael Hausenblas — *Hacking Kubernetes* (O'Reilly, 2021).
- Chris Farris, Rich Mogull et al. — *AWS Well-Architected Framework: Security Pillar* (documentación oficial de AWS).
- Microsoft — *Azure Security Benchmark* y *Microsoft Cloud Security Benchmark*.
- Google — *Google Cloud Security Foundations Guide*.
- CIS — *CIS Benchmarks* para AWS, Azure, GCP, Docker y Kubernetes.
- NIST — *SP 800-190 Application Container Security Guide* y *SP 800-204 Microservices*.

---

## 🎯 ¿De qué trata esta parte?

La infraestructura moderna vive en la nube y se empaqueta en contenedores. Esta parte enseña a
asegurar los tres grandes proveedores (AWS, Azure, GCP) y el stack de contenedores (Docker,
Kubernetes) desde una perspectiva tanto defensiva como ofensiva. Verás por qué la mayoría de las
brechas en la nube no son fallos del proveedor sino errores de configuración del cliente: buckets
públicos, roles con permisos excesivos, claves filtradas y superficies de gestión expuestas.

Partimos del **modelo de responsabilidad compartida** —la frontera exacta entre lo que asegura el
proveedor y lo que te toca a ti— y de **IAM**, el verdadero perímetro de la nube. A partir de ahí
recorremos la seguridad específica de cada proveedor, el pentest de entornos cloud, la seguridad
de contenedores (aislamiento por namespaces y cgroups, imágenes, runtime), Kubernetes (arquitectura,
hardening con CIS y ataques reales a etcd, kubelet y RBAC), Infrastructure as Code con Terraform,
CSPM, serverless, gestión de secretos, logging y respuesta a incidentes en la nube.

Sirve a arquitectos de seguridad cloud, ingenieros DevSecOps, pentesters que auditan infraestructura
moderna y equipos SRE que deben endurecer plataformas Kubernetes en producción. Toda la práctica usa
herramientas reales y de código abierto: **Prowler**, **ScoutSuite**, **kube-bench**, **Trivy**,
**Terraform**, **tfsec/Checkov** y las CLIs oficiales de cada nube.

## 🧩 Problemas que resuelve

- Configuraciones inseguras por defecto (buckets públicos, security groups abiertos, secretos en texto plano).
- Roles y políticas IAM con permisos excesivos y rutas de **escalada de privilegios**.
- Imágenes de contenedor con vulnerabilidades y secretos incrustados.
- Clústeres Kubernetes con API server, kubelet o etcd expuestos y RBAC laxo.
- Drift entre lo definido en código (Terraform) y lo desplegado realmente.
- Falta de visibilidad: sin CloudTrail/Activity Logs no hay detección ni forense.
- Gestión de secretos manual y no rotada que termina filtrada en repositorios o logs.

## 🎓 Resultados de aprendizaje

Al terminar la parte, el alumno podrá:

- Explicar el modelo de responsabilidad compartida por tipo de servicio (IaaS/PaaS/SaaS) y aplicarlo a decisiones de arquitectura.
- Diseñar y auditar políticas IAM con privilegio mínimo, y detectar rutas de escalada.
- Ejecutar auditorías automatizadas de postura con **Prowler** y **ScoutSuite** e interpretar sus hallazgos.
- Endurecer imágenes y hosts Docker según el **CIS Docker Benchmark** y escanearlas con **Trivy**.
- Describir la arquitectura de Kubernetes y endurecer un clúster usando **kube-bench** y NetworkPolicies.
- Reproducir y mitigar ataques cloud y a Kubernetes en laboratorios controlados.
- Escanear código Terraform con **tfsec/Checkov** e integrar controles en el pipeline.
- Diseñar estrategias de gestión de secretos, logging centralizado y respuesta a incidentes en la nube.

## 🧱 Prerrequisitos

- Parte 1–2 (fundamentos, redes y protocolos).
- Parte 4 (pentest y explotación) para las clases ofensivas cloud/Kubernetes.
- Parte 9 (forense y respuesta a incidentes) como base para la clase 235.
- Manejo de línea de comandos Linux, Docker básico y nociones de HTTP/APIs REST.

## 🗺️ Estructura temática

| Bloque | Clases | Foco |
|--------|--------|------|
| Fundamentos e identidad | 221–222 | Responsabilidad compartida, IAM |
| Seguridad por proveedor | 223–225 | AWS, Azure, GCP |
| Ofensiva cloud | 226 | Pentest en entornos cloud |
| Contenedores | 227 | Docker: aislamiento, imágenes, runtime |
| Kubernetes | 228–229 | Arquitectura, hardening y ataques |
| Automatización y postura | 230–231 | IaC/Terraform, CSPM |
| Cargas modernas | 232–233 | Serverless, gestión de secretos |
| Operación y defensa | 234–235 | Logging/detección, respuesta a incidentes |

## 🔗 Referencias de la parte

- Liz Rice, *Container Security*, O'Reilly. <https://www.oreilly.com/library/view/container-security/9781492056690/>
- Martin & Hausenblas, *Hacking Kubernetes*, O'Reilly. <https://www.oreilly.com/library/view/hacking-kubernetes/9781492081722/>
- AWS Well-Architected — Security Pillar. <https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html>
- Microsoft Cloud Security Benchmark. <https://learn.microsoft.com/security/benchmark/azure/>
- Google Cloud Security Foundations. <https://cloud.google.com/architecture/security-foundations>
- CIS Benchmarks. <https://www.cisecurity.org/cis-benchmarks>
- NIST SP 800-190. <https://csrc.nist.gov/pubs/sp/800/190/final>

## ▶️ Empezar

[Clase 221 — Fundamentos de seguridad en la nube y responsabilidad compartida](221-fundamentos-de-seguridad-en-la-nube-y-responsabilidad-compartida/README.md)
