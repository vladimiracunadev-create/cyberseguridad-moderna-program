# 📅 Syllabus y cronograma

Planificación temporal del **Programa de Ciberseguridad Moderna** (340 clases · 19 partes).
Las horas son estimadas a partir de la duración de cada clase (~1,5–2,5 h) más práctica.

> Ritmo de referencia: **~10 h/semana**. A ese ritmo el programa completo son **~14 meses**;
> a tiempo completo (~30 h/semana), **~5 meses**. No es obligatorio hacerlo entero: usa las
> [rutas por rol](../rutas/README.md) para un subconjunto.

## Horas por parte

| Parte | Tema | Clases | Horas aprox. | Semanas @10h |
|---|---|---:|---:|---:|
| 0 | Fundamentos y prerrequisitos | 25 | ~45 | 4,5 |
| 1 | Redes y seguridad de redes | 20 | ~38 | 3,8 |
| 2 | Criptografía aplicada | 20 | ~38 | 3,8 |
| 3 | Hacking ético y pentesting | 20 | ~40 | 4,0 |
| 4 | Seguridad de aplicaciones web | 30 | ~58 | 5,8 |
| 5 | Explotación de sistemas y binarios | 25 | ~55 | 5,5 |
| 6 | Análisis de malware | 20 | ~42 | 4,2 |
| 7 | Red Team y operaciones ofensivas | 20 | ~42 | 4,2 |
| 8 | Blue Team, detección y SOC | 20 | ~40 | 4,0 |
| 9 | Forense digital y respuesta a incidentes | 20 | ~42 | 4,2 |
| 10 | Seguridad en la nube y contenedores | 15 | ~30 | 3,0 |
| 11 | DevSecOps y seguridad del SDLC | 13 | ~24 | 2,4 |
| 12 | OSINT e ingeniería social | 12 | ~22 | 2,2 |
| 13 | Seguridad móvil, IoT e inalámbrica | 15 | ~28 | 2,8 |
| 14 | GRC, riesgo y cumplimiento | 15 | ~26 | 2,6 |
| 15 | Seguridad de IA y machine learning | 10 | ~18 | 1,8 |
| 16 | Capstones y preparación de certificaciones | 10 | ~30 | 3,0 |
| 17 | Profundización para certificaciones | 20 | ~36 | 3,6 |
| 18 | IA aplicada a la ciberseguridad | 10 | ~22 | 2,2 |
| | **Total** | **340** | **~675 h** | **~68 sem** |

*(Las horas incluyen leer la clase, hacer los ejercicios/laboratorio y el reto verificable.)*

## Dependencias entre partes

- **Parte 0** es prerrequisito de todo.
- **1 → 3 → 4 → 5 → 7** (línea ofensiva).
- **1 → 6 → 8 → 9** (línea defensiva/DFIR).
- **2** (cripto) apoya 4, 10, 11.
- **10, 11** asumen 0, 1, 2, 4.
- **14** (GRC) es independiente pero se enriquece con 8, 9.
- **17** profundiza 2, 8, 9, 11, 14; **18** asume 3–9 y 15.
- **16** (capstones) va al final de cada ruta.

## Cronograma sugerido de 30 semanas (ruta "generalista")

Un plan realista para cubrir el núcleo empleable en ~2 trimestres a 10 h/semana:

| Semanas | Contenido | Hito |
|---|---|---|
| 1–5 | Parte 0 (fundamentos) + montar laboratorio | Laboratorio operativo |
| 6–9 | Parte 1 (redes) + lab `redes-nmap` | Mapa de red validado |
| 10–13 | Parte 2 (cripto) + lab `cripto` | 4 retos de cripto resueltos |
| 14–18 | Parte 3 + Parte 4 (pentest + web) + labs `appsec-web`/`appsec-code` | Mini-informe de pentest web |
| 19–22 | Parte 8 + Parte 9 (SOC + DFIR) + labs `blue-team-soc`/`dfir-memoria` | Caso de detección + IR |
| 23–25 | Parte 10 + Parte 11 (cloud + DevSecOps) + lab `cloud-security` | Auditoría cloud/CI |
| 26–28 | Parte 14 + Parte 17 (GRC + gestión de vulnerabilidades) | Matriz de riesgo + programa VM |
| 29–30 | Parte 16 (capstone de tu ruta) | **Capstone + portafolio** |

> Ajusta según tu [ruta por rol](../rutas/README.md): un pentester profundiza 3–7; un analista SOC, 6–9; un GRC, 14.

## Evaluación y progreso

- Cada clase trae **ejercicios** y un **reto verificable** con criterio de aceptación (ver [rúbrica](rubrica-evaluacion.md)).
- Autoevaluación por parte: [quiz interactivo](../autoevaluaciones/README.md) (97 preguntas).
- Seguimiento: [progreso de las 340 clases](../autoevaluaciones/README.md#progreso).
- Cierre por rol: [examen final por rol](examen-final-por-rol.md).

## 🔗 Relacionado

- [Índice de clases](../classes/README.md) · [Rutas por rol](../rutas/README.md) · [Laboratorios](../labs/README.md) · [Certificaciones](../certificaciones/README.md)
