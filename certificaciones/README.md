# 🎓 Certificaciones

Cómo se alinea el **Programa de Ciberseguridad Moderna** con las certificaciones más relevantes. Para cada una se cruza **cada dominio oficial del examen** con las **partes/clases** que lo cubren y se calcula un **porcentaje de cobertura ponderado** por el peso del dominio en el examen.

Mapeo entre las certificaciones de ciberseguridad y las partes/clases del programa. La 'cobertura' de cada dominio es una estimación honesta del grado en que el programa lo prepara (0-100). El total es la suma ponderada por el peso oficial del dominio en el examen. NO es una garantía de aprobar: las certificaciones prácticas requieren, además, laboratorios y práctica propia.

| Certificación | Código | Nivel | Cobertura estimada | Detalle |
|---|---|---|---|---|
| CompTIA Security+ | SY0-701 | Fundacional | `█████████░` 91% | [ver mapeo](comptia-security-plus-sy0-701.md) |
| CompTIA PenTest+ | PT0-002 | Intermedio (ofensivo) | `█████████░` 91% | [ver mapeo](comptia-pentest-plus-pt0-002.md) |
| CompTIA CySA+ | CS0-003 | Intermedio (defensivo) | `█████████░` 92% | [ver mapeo](comptia-cysa-plus-cs0-003.md) |
| OSCP — Offensive Security Certified Professional | PEN-200 | Avanzado (ofensivo, práctico) | `█████████░` 86% | [ver mapeo](oscp-pen-200.md) |
| CISSP — Certified Information Systems Security Professional | CISSP | Avanzado (gerencial, amplio) | `█████████░` 90% | [ver mapeo](cissp.md) |
| BTL1 — Blue Team Level 1 | BTL1 | Fundacional (defensivo, práctico) | `█████████░` 91% | [ver mapeo](btl1.md) |
| SANS GCIH / GCFA (Incident Handler / Forensic Analyst) | GCIH · GCFA | Avanzado (DFIR) | `█████████░` 87% | [ver mapeo](sans-gcih-gcfa.md) |

## ¿Cómo se calcula la cobertura?

Para cada dominio del examen se estima, de forma honesta, en qué grado el programa prepara ese dominio (0–100%). El total es la **media ponderada** por el peso oficial de cada dominio: `Σ (peso_dominio × cobertura_dominio) / 100`. El cálculo se genera con [`scripts/generar_certis.py`](../scripts/generar_certis.py) a partir de [`_mapeo.json`](_mapeo.json), así que es reproducible y auditable.

## Certificaciones mapeadas

- **[CompTIA Security+ (SY0-701)](comptia-security-plus-sy0-701.md)** — Fundacional.
- **[CompTIA PenTest+ (PT0-002)](comptia-pentest-plus-pt0-002.md)** — Intermedio (ofensivo).
- **[CompTIA CySA+ (CS0-003)](comptia-cysa-plus-cs0-003.md)** — Intermedio (defensivo).
- **[OSCP — Offensive Security Certified Professional (PEN-200)](oscp-pen-200.md)** — Avanzado (ofensivo, práctico).
- **[CISSP — Certified Information Systems Security Professional (CISSP)](cissp.md)** — Avanzado (gerencial, amplio).
- **[BTL1 — Blue Team Level 1 (BTL1)](btl1.md)** — Fundacional (defensivo, práctico).
- **[SANS GCIH / GCFA (Incident Handler / Forensic Analyst) (GCIH · GCFA)](sans-gcih-gcfa.md)** — Avanzado (DFIR).

---

> Los pesos por dominio provienen de las guías oficiales de examen de cada proveedor y pueden actualizarse; verifica siempre la versión vigente. Este mapeo es orientativo y no está avalado por CompTIA, Offensive Security, ISC2, Security Blue Team ni SANS/GIAC.
