# Clase 243 — Imágenes y contenedores seguros en el pipeline

> Parte: **11 — DevSecOps y seguridad del SDLC** · Fuente: *Securing DevOps* (Julien Vehent) y NIST SP 800-190 (Application Container Security Guide)
> ⏱️ Duración estimada: **120 min** · Nivel: **Avanzado**

---

## 🎯 Objetivo

Construir imágenes de contenedor seguras dentro del pipeline: mínimas (distroless/multi-stage),
sin ejecutar como root, escaneadas por vulnerabilidades y firmadas para garantizar su integridad.
Una imagen es un artefacto que llega a producción; si está inflada, vulnerable o no verificada,
es un vector directo de ataque. Usaremos **Trivy** para escanear, **hadolint** para el
Dockerfile, y **cosign** para firmar.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Escribir** Dockerfiles seguros y mínimos con builds multi-stage y usuario no-root.
2. **Escanear** imágenes por vulnerabilidades de OS y de aplicación con Trivy.
3. **Lintar** Dockerfiles con hadolint aplicando buenas prácticas.
4. **Firmar y verificar** imágenes con cosign (keyless con OIDC).
5. **Aplicar** un gate que impida promover imágenes vulnerables o no firmadas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Superficie de ataque de una imagen | Menos paquetes = menos CVE y menos exploits |
| 2 | Multi-stage builds y distroless | Imágenes mínimas de producción |
| 3 | Usuario no-root y capabilities | Limitar el daño de un contenedor comprometido |
| 4 | Escaneo con Trivy | Detectar CVE de OS y librerías |
| 5 | hadolint | Buenas prácticas del Dockerfile |
| 6 | Firma con cosign | Integridad y procedencia del artefacto |
| 7 | Gate de admisión | Solo imágenes firmadas y limpias a producción |

## 📖 Definiciones y características

- **Multi-stage build**: separar la fase de compilación de la imagen final. *Característica*: la imagen de producción no lleva compiladores ni herramientas de build.
- **Distroless**: imagen base sin shell ni gestor de paquetes, solo el runtime. *Característica*: reduce drásticamente la superficie de ataque.
- **Usuario no-root**: correr el proceso con un UID sin privilegios. *Característica*: un escape de aplicación no obtiene root en el contenedor.
- **Escaneo de imagen**: cruzar los paquetes de la imagen con bases de CVE. *Característica*: cubre capa de OS y dependencias de la app.
- **Firma (cosign)**: firma criptográfica de la imagen y su digest. *Característica*: verifica integridad y procedencia; keyless usa OIDC + transparency log.
- **Admission control**: política que solo admite imágenes que cumplen requisitos. *Característica*: bloquea en el registry o en Kubernetes lo no firmado/vulnerable.

## 🧰 Herramientas y preparación

- **Docker/BuildKit** o **buildah** para construir.
- **Trivy** para escanear imágenes.
- **hadolint** para lintar Dockerfiles.
- **cosign** (Sigstore) para firmar y verificar.

```bash
# Escanear una imagen:
trivy image --severity HIGH,CRITICAL miapp:1.0

# Lintar un Dockerfile:
docker run --rm -i hadolint/hadolint < Dockerfile

# Firmar (keyless con OIDC):
cosign sign miregistry/miapp@sha256:<digest>
```

## 🧪 Laboratorio guiado

1. **Parte de un Dockerfile "malo"** (imagen base pesada, root, sin pin) y lintéalo:

```bash
docker run --rm -i hadolint/hadolint < Dockerfile
```

2. **Reescríbelo seguro** con multi-stage, base distroless y usuario no-root:

```dockerfile
# build stage
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app .

# runtime stage
FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

3. **Escanea la imagen resultante** y compárala con la original:

```bash
trivy image --severity HIGH,CRITICAL miapp:seguro
```

Observa la caída de CVE al usar distroless.
4. **Firma la imagen con cosign** (keyless):

```bash
cosign sign --yes miregistry/miapp@sha256:<digest>
cosign verify miregistry/miapp@sha256:<digest> \
  --certificate-identity-regexp '.*' \
  --certificate-oidc-issuer-regexp '.*'
```

5. **Integra el gate en CI**. El job de build debe (a) lintar con hadolint, (b) escanear con Trivy y fallar con CRITICAL, (c) firmar solo si pasa, (d) publicar el digest.
6. **Admission en el clúster** (conceptual/opcional). Configura una política (cosign policy-controller o Kyverno) que solo admita imágenes firmadas por tu identidad.
7. **Genera SBOM de la imagen** (enlaza con clase 246):

```bash
trivy image --format cyclonedx -o sbom.json miapp:seguro
```

> Nota ética: escanear y endurecer imágenes propias es defensivo. No publiques imágenes con
> malware ni las uses para atacar; el laboratorio se hace con imágenes tuyas.

## ✍️ Ejercicios

1. Convierte un Dockerfile de una sola etapa a multi-stage y mide la reducción de tamaño.
2. Cambia una imagen base `ubuntu` por distroless y compara los CVE con Trivy.
3. Configura el contenedor para correr como usuario no-root y verifícalo.
4. Firma una imagen con cosign y verifica la firma.
5. Añade un gate de Trivy que rompa el build con vulnerabilidades CRITICAL.
6. Genera el SBOM de la imagen en formato CycloneDX.

## 📝 Reto verificable

Construye un pipeline que produzca una imagen mínima, escaneada y firmada.

**Criterio de aceptación**: (a) la imagen final usa multi-stage y base mínima/distroless y corre
como no-root; (b) hadolint no reporta errores; (c) Trivy no reporta CVE CRITICAL y el gate falla
si aparecen; (d) la imagen se firma con cosign y la firma se verifica; y (e) se genera y publica
un SBOM de la imagen.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Imagen de 1.2 GB con cientos de CVE | Base pesada y build en una etapa. Usa multi-stage + distroless/alpine. |
| El contenedor corre como root | No definiste `USER`. Añade un usuario no-root o usa base `:nonroot`. |
| `cosign verify` falla | Identidad/issuer no coinciden. Ajusta `--certificate-identity` al del firmante real. |
| Trivy reporta CVE sin fix disponible | No hay parche aún. Documenta como riesgo aceptado/VEX y monitoriza. |
| La imagen firmada se puede sustituir por otra | Firmaste el tag, no el digest. Firma y despliega por digest inmutable. |

## ❓ Preguntas frecuentes

**❓ ¿Distroless o Alpine?**
Distroless minimiza al máximo (sin shell, ideal para producción y para reducir superficie). Alpine es más pequeña que Debian y conserva shell/apk, útil para depurar. Elige según necesidad de troubleshooting vs mínima superficie.

**❓ ¿Firmar la imagen impide que sea vulnerable?**
No. La firma garantiza integridad y procedencia, no ausencia de CVE. Necesitas escanear además de firmar.

**❓ ¿Debo escanear en build o en el registry?**
Ambos. En build para bloquear temprano; en el registry de forma continua porque aparecen CVE nuevos sobre imágenes ya publicadas.

**❓ ¿Keyless de cosign es seguro sin gestionar claves?**
Sí: usa identidad OIDC efímera y un transparency log público (Rekor). Elimina la gestión de claves de larga vida, aunque puedes usar claves propias si lo prefieres.

## 🔗 Referencias

- NIST SP 800-190 Container Security — <https://csrc.nist.gov/pubs/sp/800/190/final>
- Trivy — <https://trivy.dev/>
- hadolint — <https://github.com/hadolint/hadolint>
- Sigstore cosign — <https://docs.sigstore.dev/cosign/overview/>
- Distroless images — <https://github.com/GoogleContainerTools/distroless>

## 📥 Material descargable

- 📄 [Guía en PDF](./clase-243-guia.pdf) — versión imprimible de esta clase.
- 🎞️ [Presentación (PPTX)](./clase-243-presentacion.pptx) — deck para proyectar en clase.

## ⬅️ Clase anterior

[Clase 242 — Seguridad en pipelines CI/CD](../242-seguridad-en-pipelines-ci-cd/README.md)

## ➡️ Siguiente clase

[Clase 244 — Políticas como código con OPA](../244-politicas-como-codigo-con-opa/README.md)
