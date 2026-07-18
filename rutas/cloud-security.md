# ☁️ Cloud Security Engineer

> Seguridad de nube, contenedores y pipelines: proteges la infraestructura que
> ya no vive en un rack, sino en una API que cualquiera puede llamar mal.
>
> **Nivel de entrada:** intermedio; casi nadie llega aquí de cero — se viene de dev, ops o sysadmin · **Foco:** modelo de responsabilidad compartida, IAM, CSPM, contenedores/Kubernetes e IaC · **Certificación faro:** AWS Security Specialty / CKS (Kubernetes Security)

## 🧭 Qué es y por qué importa

La **nube es el nuevo perímetro** — y el perímetro ahora es una consola web, un token
de IAM y un archivo de Terraform. El Cloud Security Engineer es quien evita que esa
superficie, enorme y cambiante, se convierta en la puerta de entrada del próximo incidente.

El concepto que ordena todo el rol es el **modelo de responsabilidad compartida**: el
proveedor (AWS, Azure, GCP) asegura la nube — hardware, hipervisor, red física —, pero
**tú aseguras lo que pones dentro de ella**. La inmensa mayoría de las brechas en la nube
no son culpa del proveedor: son buckets públicos, roles con permisos de más, secretos en
el repo y grupos de seguridad abiertos al mundo. Errores de configuración, no exploits.

Las piezas que dominas a diario:

- **IAM (gestión de identidades y accesos):** el corazón del control en la nube. Roles,
  políticas, permisos, federación. El **mínimo privilegio** aquí no es un eslogan: es la
  diferencia entre un incidente contenido y toda la cuenta comprometida.
- **CSPM (Cloud Security Posture Management):** herramientas que auditan de forma continua
  la configuración de tus cuentas contra buenas prácticas y benchmarks. Tu radar contra el
  drift y las malas configuraciones que aparecen solas.
- **Seguridad de contenedores y Kubernetes:** imágenes sin vulnerabilidades, contenedores
  sin privilegios, y un clúster de K8s endurecido — RBAC, network policies, admission
  control. Es el terreno más técnico y donde la CKS marca la diferencia.
- **IaC (Infrastructure as Code):** si la infra se define en código (Terraform, CloudFormation),
  la seguridad **también se escala en código** — se escanea, se revisa y se corrige antes
  de desplegar, no después.

Importa porque prácticamente toda empresa moderna está en la nube, la superficie crece
más rápido que los equipos, y el talento que sabe asegurarla **de verdad** escasea. Es de
los caminos mejor pagados del sector, y no por moda: por escasez real.

## 🗓️ Un día en el puesto

- **Revisión de postura:** empiezas mirando el tablero de CSPM — qué configuraciones nuevas
  se rompieron desde ayer, qué cuenta abrió un puerto, qué bucket cambió a público.
- **IAM, siempre IAM:** revisas una solicitud de permisos, recortas un rol demasiado ancho,
  investigas por qué un servicio necesita acceso a media cuenta cuando debería tocar un solo
  recurso.
- **Pipeline y código:** revisas los hallazgos que los escáneres de IaC y de imágenes dejaron
  en los pull requests. Bloqueas lo grave, orientas al equipo de dev en cómo arreglarlo.
- **Kubernetes:** endureces un clúster, ajustas una network policy, o investigas por qué un
  pod corre como root cuando no debería.
- **Colaboración con dev y ops:** buena parte del día es *conversación*. En la nube no eres
  un guardián que dice "no": eres quien da a los equipos caminos seguros por defecto para
  que puedan ir rápido sin abrir agujeros.
- **Respuesta y detección:** revisas logs de la nube (CloudTrail y equivalentes), afinas
  alertas, y cuando algo salta, ayudas a contener sin apagar producción.

Dicho sin adornos: gran parte del oficio es **prevenir configuraciones malas a escala**,
no perseguir hackers. Es menos glamuroso que el pentest y más parecido a la ingeniería
que a la película de acción — y justo por eso se paga bien.

## 🧠 Qué necesitas saber

### Conocimiento técnico

- **Nube a nivel de ingeniería, no solo de seguridad.** Este es el punto honesto del rol:
  se espera que sepas **construir** en la nube antes de asegurarla. Redes de nube (VPC,
  subredes, routing), cómputo, almacenamiento, serverless. Si no entiendes cómo funciona
  un servicio, no puedes protegerlo.
- **IAM en profundidad:** políticas, roles, confianza entre cuentas, federación, y el arte
  del mínimo privilegio real.
- **Contenedores y Kubernetes:** cómo funciona Docker por dentro, la arquitectura de un
  clúster, RBAC, admission controllers, aislamiento.
- **IaC:** leer y escribir Terraform, y entender qué riesgos introduce cada recurso.
- **Criptografía aplicada a la nube:** gestión de claves (KMS), cifrado en reposo y en
  tránsito, TLS y PKI. No necesitas ser criptógrafo, pero sí saber elegir y operar bien.
- **Logging y detección en la nube:** qué genera cada servicio, cómo centralizarlo y qué
  vigilar.

### Herramientas del oficio

```text
Nubes:        AWS, Azure, GCP (domina una a fondo, conoce el resto)
IAM/Policy:   políticas nativas, OPA, análisis de permisos
CSPM:         Prowler, ScoutSuite, Steampipe, herramientas nativas
Contenedores: Docker, Trivy, Grype (escaneo de imágenes)
Kubernetes:   kube-bench, kubescape, Falco, OPA Gatekeeper
IaC:          Terraform, tfsec, Checkov, Terrascan
Secretos:     Vault, KMS/Secrets Manager de cada nube
Detección:    CloudTrail, GuardDuty, y SIEM para correlacionar
```

Ninguna herramienta te vuelve ingeniero: el CSPM te entrega hallazgos, pero el criterio
para saber **cuál importa y cómo arreglarlo sin romper producción** lo pones tú.

### Habilidades no técnicas

- **Mentalidad de ingeniero:** automatizas, versionas y tratas la seguridad como código.
- **Comunicación con equipos de dev:** tu impacto se mide en cuántos equipos adoptan lo
  seguro *por defecto*, no en cuántos tickets abres.
- **Pragmatismo:** la nube cambia cada semana; hay que priorizar el riesgo real sobre la
  checklist perfecta.
- **Aprendizaje continuo:** los servicios de nube salen y mutan sin parar. Quedarte quieto
  es quedarte obsoleto.

## 📚 Tu ruta en el programa

Orden recomendado (según el [índice de rutas](./README.md)):

1. 📚 [**Parte 0** — Fundamentos y prerrequisitos](../classes/parte-0-fundamentos-y-prerrequisitos/README.md) (001–025) · Linux, redes, Python, Docker y Git: la base de ingeniería sin la que la nube no se sostiene.
2. 📚 [**Parte 2** — Criptografía aplicada](../classes/parte-2-criptografia-aplicada/README.md) (046–065) · claves, KMS, TLS y PKI: lo que cifra y autentica todo lo que despliegas.
3. 📚 [**Parte 4** — Seguridad de aplicaciones web](../classes/parte-4-seguridad-de-aplicaciones-web/README.md) (086–115) · APIs y superficie web: lo que corre *dentro* de tus contenedores.
4. 📚 [**Parte 10** — Seguridad en la nube y contenedores](../classes/parte-10-seguridad-en-la-nube-y-contenedores/README.md) (221–235) · **el núcleo del rol.**
5. 📚 [**Parte 11** — DevSecOps y seguridad del SDLC](../classes/parte-11-devsecops-y-seguridad-del-sdlc/README.md) (236–248) · llevar la seguridad al pipeline y automatizarla.

Clases concretas por las que empezar (el corazón está en la Parte 10):

- ☁️ [221 · Fundamentos de seguridad en la nube y responsabilidad compartida](../classes/parte-10-seguridad-en-la-nube-y-contenedores/221-fundamentos-de-seguridad-en-la-nube-y-responsabilidad-compartida/README.md) — el concepto que ordena todo el rol.
- 🔑 [222 · IAM en la nube: identidades, roles y permisos](../classes/parte-10-seguridad-en-la-nube-y-contenedores/222-iam-en-la-nube-identidades-roles-y-permisos/README.md) — el control más importante de la nube, y el más maltratado.
- 🟧 [223 · Seguridad en AWS](../classes/parte-10-seguridad-en-la-nube-y-contenedores/223-seguridad-en-aws/README.md) — la nube más pedida en ofertas; domínala a fondo primero.
- 🐳 [227 · Seguridad de contenedores Docker](../classes/parte-10-seguridad-en-la-nube-y-contenedores/227-seguridad-de-contenedores-docker/README.md) — imágenes y contenedores sin agujeros.
- ⎈ [228 · Seguridad de Kubernetes: arquitectura](../classes/parte-10-seguridad-en-la-nube-y-contenedores/228-seguridad-de-kubernetes-arquitectura/README.md) — la base para endurecer un clúster y para la CKS.
- 🏗️ [230 · Seguridad de Infrastructure as Code (Terraform)](../classes/parte-10-seguridad-en-la-nube-y-contenedores/230-seguridad-de-infrastructure-as-code-terraform/README.md) — asegurar la infra antes de que exista.
- 🛰️ [231 · Cloud Security Posture Management (CSPM)](../classes/parte-10-seguridad-en-la-nube-y-contenedores/231-cloud-security-posture-management-cspm/README.md) — tu radar continuo contra las malas configuraciones.

### Laboratorio

- 🧪 [`cloud-security`](../labs/cloud-security/README.md) — tu entorno de práctica de nube:
  levantas infraestructura, la rompes con malas configuraciones típicas, la detectas con
  CSPM y la corriges como código. Es donde la teoría del modelo compartido se vuelve reflejo.

## 🎓 Certificaciones

Certificaciones **faro** del rol (aún sin archivo en el programa, pero son el objetivo a apuntar):

- 🏅 **AWS Certified Security – Specialty** — la referencia para seguridad en AWS, la nube más
  demandada. Exige saber IAM, cifrado, detección y respuesta *en la práctica*, no de memoria.
- 🛡️ **CKS (Certified Kubernetes Security Specialist)** — cien por cien práctica y con clúster
  real. Es la que mejor demuestra que sabes endurecer Kubernetes de verdad.

Con archivo en el programa, útiles como base y como respaldo:

- 🎓 [**CompTIA Security+** (SY0-701)](../certificaciones/comptia-security-plus-sy0-701.md) — la
  certificación **de entrada** al sector. No es de nube, pero asienta el vocabulario y abre
  puertas de RRHH mientras preparas las específicas.
- 🏛️ [**CISSP**](../certificaciones/cissp.md) — de gestión y arquitectura, más senior. Suma
  peso cuando aspiras a roles de arquitecto de seguridad en la nube o a liderar.

Consulta el [mapeo completo a certificaciones](../certificaciones/README.md) para ver cuánto
cubre el programa de cada examen.

## 📈 Progresión de carrera y salario

Ruta habitual: **DevOps / SysAdmin / Dev → Cloud Security Engineer → Cloud Security Architect →
Head of Cloud Security / Principal**. También abre caminos hacia **DevSecOps Engineer** y
**Security Architect**. Casi nadie entra aquí como primer empleo: se llega con base de
ingeniería en la nube ya construida.

Rangos **orientativos y aproximados** (varían mucho por empresa, experiencia y nube; cloud
security está **entre los roles mejor pagados** del sector por la escasez real de talento):

```text
Región            Entrada (con base cloud)  Senior · arquitecto
----------------  ------------------------  -----------------------
LATAM             USD 25k – 45k / año       USD 55k – 90k+ / año
España            EUR 35k – 50k / año       EUR 60k – 90k+ / año
Remoto (USD)      USD 80k – 120k / año      USD 140k – 220k+ / año
```

Los números remotos en USD asumen contratación por empresas de EE. UU./Europa, muy competida
y con listón alto de inglés. El diferencial de este rol es doble: la nube paga más que la
media, y **la escasez de gente que la sepa asegurar de verdad** empuja los números hacia arriba.

## ⚠️ Mitos y errores comunes

- **"Puedo hacer cloud security sin saber construir en la nube."** No. Es el error más caro
  del camino. Se espera que sepas la nube **a nivel de ingeniería** antes de asegurarla; si no
  entiendes cómo funciona un servicio, no puedes protegerlo.
- **"La nube es segura porque la asegura AWS/Azure/GCP."** El proveedor asegura *su* parte.
  Casi todas las brechas ocurren en *tu* parte del modelo compartido: configuración, IAM y
  secretos.
- **"Con un buen CSPM ya está resuelto."** El CSPM te da hallazgos, no decisiones. Priorizar
  el riesgo real y arreglarlo sin romper producción es donde entras tú.
- **"IAM es un detalle administrativo."** IAM es *el* control central de la nube. Un rol con
  permisos de más es la ruta más común desde un fallo pequeño hasta la cuenta entera.
- **"Contenedor y máquina virtual dan el mismo aislamiento."** No. Un contenedor mal
  configurado comparte kernel con el host; entender eso es media seguridad de contenedores.

## 🚀 Siguientes pasos

1. **Asienta la base de ingeniería** con la **Parte 0**: Linux, redes, Python, Docker y Git.
   Sin esto, la nube se te hará cuesta arriba.
2. Refuerza con las **Partes 2 y 4**: criptografía aplicada (KMS, TLS) y seguridad de APIs —
   lo que cifra y lo que corre dentro de tus despliegues.
3. Haz la **Parte 10** completa y monta el laboratorio [`cloud-security`](../labs/cloud-security/README.md):
   rompe configuraciones, detéctalas y corrígelas como código.
4. Lleva la seguridad al pipeline con la **Parte 11** (DevSecOps): escaneo de IaC, de imágenes
   y de secretos, integrado en CI/CD.
5. Elige **una nube** (AWS es la apuesta más segura por demanda) y ve a por la **AWS Security
   Specialty**; para la parte de contenedores, apunta a la **CKS**.
6. Construye **evidencia pública**: un repo de Terraform seguro, writeups de tus hallazgos de
   laboratorio, políticas de IAM bien diseñadas. En la nube, mostrar que sabes construir *y*
   asegurar vale más que cualquier título.

---

- ⬅️ [Volver al índice de rutas](./README.md)
- 🏠 [Inicio del programa](../README.md)
