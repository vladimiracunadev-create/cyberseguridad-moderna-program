# 🎓 Examen final por rol

Cada [ruta por rol](../rutas/README.md) cierra con un **examen final** que combina teoría,
práctica y comunicación — igual que una entrevista técnica o una certificación real. Todos
comparten la misma estructura; cambia el contenido.

## Estructura común (100 puntos)

| Bloque | Peso | Formato |
|---|---:|---|
| **Teoría** | 25 | Quiz de la(s) parte(s) de la ruta ([autoevaluación](../autoevaluaciones/README.md)) ≥ 70%. |
| **Práctica** | 50 | Un ejercicio en laboratorio, con evidencia reproducible. |
| **Informe/comunicación** | 25 | Documento entregable (informe, playbook o política) evaluado con la [rúbrica](rubrica-evaluacion.md). |

**Aprobado:** ≥ 70/100 y práctica ≥ 30/50.

---

## 🎯 Pentester / Ethical Hacker

- **Teoría:** quizzes de las Partes 1, 3, 4, 5.
- **Práctica:** compromete la VM del lab [`appsec-web`](../labs/appsec-web/README.md) o una VM propia: recon → explotación de una vuln → PoC de bajo impacto.
- **Informe:** informe de pentest (resumen ejecutivo + hallazgos con CVSS + remediación), clase 085.

## 🔴 Red Teamer

- **Teoría:** Parte 7 (+ 5, 6).
- **Práctica:** en el lab [`red-team-ad`](../labs/red-team-ad/README.md)/GOAD: enumeración AD → Kerberoasting → ruta a Domain Admin con BloodHound.
- **Informe:** narrativa de la operación mapeada a MITRE ATT&CK + recomendaciones de detección.

## 🔵 Analista SOC / Blue Team

- **Teoría:** Partes 8, 6, 1.
- **Práctica:** en el lab [`blue-team-soc`](../labs/blue-team-soc/README.md): detecta la fuerza bruta + movimiento lateral y escribe una regla (Sigma) que dispare.
- **Informe:** informe de incidente + regla de detección validada.

## 🛡️ Analista de Gestión de Vulnerabilidades

- **Teoría:** Partes 3 (071), 17 (318, 324), 8.
- **Práctica:** escanea el lab, prioriza con CVSS/EPSS/KEV, define SLAs y valida un parcheo.
- **Informe:** reporte semanal de VM + plan de remediación priorizado.

## 🕵️ DFIR / Analista forense

- **Teoría:** Partes 9, 6.
- **Práctica:** en el lab [`dfir-memoria`](../labs/dfir-memoria/README.md): identifica el proceso malicioso, el C2 y extrae IOCs.
- **Informe:** informe forense con línea de tiempo y cadena de custodia.

## 🕸️ AppSec / Bug Bounty

- **Teoría:** Partes 4, 2, 11.
- **Práctica:** encuentra y explota (en tu lab) 3 vulns del OWASP Top 10 en [`appsec-web`](../labs/appsec-web/README.md); haz code review con [`appsec-code`](../labs/appsec-code/README.md).
- **Informe:** 3 reportes tipo bug bounty (impacto, PoC, remediación).

## ☁️ Cloud Security Engineer

- **Teoría:** Partes 10, 11, 2.
- **Práctica:** en el lab [`cloud-security`](../labs/cloud-security/README.md): audita una configuración con Prowler/kube-bench y corrige 3 hallazgos.
- **Informe:** informe CSPM con hallazgos priorizados y remediación como código.

## 🏛️ GRC / Gestión de seguridad

- **Teoría:** Partes 14, 17.
- **Práctica (aplicada):** construye una matriz de riesgo, un SoA de ISO 27001 y un perfil NIST CSF para una organización ficticia.
- **Informe:** política de seguridad + análisis de riesgo cuantitativo (FAIR).

---

## 🤖 Complemento IA (para cualquier rol)

Quien complete la **Parte 18** puede añadir el [capstone 340](../classes/parte-18-ia-aplicada-a-la-ciberseguridad/340-capstone-pentest-autorizado-asistido-por-ia-con-mcp/README.md): repetir el examen práctico **asistido por IA** (kali-mcp) y comparar — con retrospectiva sobre qué aportó la IA y qué tuvo que corregir.

## 🔗 Relacionado

- [Rutas por rol](../rutas/README.md) · [Rúbrica de evaluación](rubrica-evaluacion.md) · [Syllabus](syllabus.md) · [Certificaciones](../certificaciones/README.md)
