# Clase 218 — Reporte forense y aspectos legales

> Parte: **9 — Forense digital y respuesta a incidentes** · Fuente: *SWGDE Best Practices* y NIST SP 800-86
> ⏱️ Duración estimada: **110 min** · Nivel: **Intermedio**

---

## 🎯 Objetivo

Aprender a redactar un **informe forense defendible** y a manejar los aspectos legales de una investigación: admisibilidad de la evidencia, cadena de custodia documentada, testimonio pericial, y consideraciones de privacidad y notificación (GDPR y leyes locales). Al terminar sabrás producir un informe que se sostenga ante un tribunal y comunicarlo a distintas audiencias.

## 📚 Resultados de aprendizaje

Al finalizar, el alumno podrá:

1. **Estructurar** un informe forense completo y trazable.
2. **Escribir** hallazgos que separen hechos de opiniones.
3. **Garantizar** la admisibilidad y la cadena de custodia.
4. **Adaptar** el informe a audiencias técnica, ejecutiva y legal.
5. **Reconocer** obligaciones de privacidad y notificación de brechas.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Estructura del informe | Claridad y trazabilidad |
| 2 | Hechos vs. opinión | Credibilidad pericial |
| 3 | Admisibilidad de evidencia | Que no la rechacen |
| 4 | Cadena de custodia en el informe | Integridad demostrable |
| 5 | Audiencias del informe | Técnico, ejecutivo, legal |
| 6 | Testimonio pericial | Defender los hallazgos |
| 7 | Privacidad y notificación | GDPR, plazos legales |
| 8 | Retención y confidencialidad | Manejo del material |

## 📖 Definiciones y características

- **Informe forense**: documento que expone método, evidencia y conclusiones. Característica: reproducible por un tercero.
- **Hecho vs. opinión**: el hecho es observable y verificable; la opinión es interpretación fundada. Característica: deben distinguirse siempre.
- **Admisibilidad**: que la evidencia sea aceptada en un proceso. Característica: exige método fiable y custodia intacta.
- **Cadena de custodia**: registro de manejo de la evidencia. Característica: un hueco puede invalidarla.
- **Testigo experto**: perito que explica hallazgos técnicos al tribunal. Característica: debe ser claro, imparcial y defendible.
- **Notificación de brecha**: obligación legal de informar (p. ej. GDPR: 72 h a la autoridad). Característica: plazos estrictos.
- **Privacidad**: límites sobre qué datos se pueden recolectar/analizar. Característica: varía por jurisdicción y contexto laboral.

## 🧰 Herramientas y preparación

- **Plantilla de informe**: portada, resumen ejecutivo, alcance, metodología, hallazgos, línea de tiempo, conclusiones, anexos.
- **Trazabilidad**: hashes, capturas y referencias a cada artefacto.
- **Marco legal**: familiarízate con GDPR, y con la normativa de tu país (en Chile, la Ley 19.628 y la Ley 21.459 de delitos informáticos, por ejemplo).
- **Ejercicio aplicado**: redacción, no herramientas técnicas.

## 🧪 Laboratorio guiado

> Redacta el informe de un caso que ya investigaste (por ejemplo el de la clase 220).

1. Crea la **portada**: caso, examinador, fechas, clasificación de confidencialidad.
2. Escribe el **resumen ejecutivo** (media página, sin jerga): qué pasó, impacto y recomendación clave, para dirección.
3. Define **alcance y limitaciones**: qué se analizó, qué no y por qué.
4. Documenta la **metodología**: herramientas, versiones, procedimientos y hashes de las imágenes.
5. Redacta los **hallazgos** separando claramente hecho de interpretación. Ejemplo:
   - *Hecho*: "El artefacto Prefetch registra la ejecución de `x.exe` el 2026-07-10 03:14 UTC (SHA-256: …)."
   - *Opinión*: "En mi opinión profesional, esto es consistente con la ejecución del malware descrito."
6. Incluye la **línea de tiempo** reconstruida y la **cadena de custodia** completa.
7. Añade **conclusiones** y **recomendaciones**, y los **anexos** (hashes, capturas, comandos).
8. Prepara una versión **ejecutiva** y una **técnica** del mismo caso.

## ✍️ Ejercicios

1. Escribe un resumen ejecutivo de media página para un caso.
2. Reescribe tres hallazgos separando hecho de opinión.
3. Documenta la metodología con herramientas y versiones.
4. Redacta la sección de cadena de custodia de un ítem.
5. Adapta un hallazgo técnico para una audiencia legal.
6. Enumera las obligaciones de notificación bajo GDPR.

## 📝 Reto verificable

Redacta un informe forense completo de un caso que investigaste, con todas las secciones, hallazgos que distingan hecho de opinión, cadena de custodia trazable y una versión ejecutiva aparte.

**Criterio de aceptación**: el informe permite a un tercero reproducir el análisis (herramientas, versiones, hashes), cada hallazgo separa hecho de interpretación, la cadena de custodia no tiene huecos, y existe un resumen ejecutivo comprensible sin conocimientos técnicos.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| El tribunal rechaza la evidencia | Custodia rota o método no fiable. Documenta todo y usa procesos reconocidos. |
| Mezclas hecho y opinión | Se pierde credibilidad. Sepáralos explícitamente. |
| Dirección no entiende el informe | Demasiada jerga. Añade resumen ejecutivo claro. |
| No puedes reproducir tu análisis | Faltan versiones/comandos. Registra la metodología completa. |
| Notificaste tarde la brecha | Ignoraste plazos legales. Conoce el marco (72 h en GDPR). |

## ❓ Preguntas frecuentes

**❓ ¿Qué hace admisible la evidencia?**
Un método fiable y documentado, integridad probada por hashes y una cadena de custodia sin huecos.

**❓ ¿Puedo dar opiniones en el informe?**
Sí, como perito, pero identificadas como opinión profesional y fundadas en hechos, separadas de estos.

**❓ ¿Debo notificar toda brecha?**
Depende de la jurisdicción y del dato afectado. GDPR exige notificar a la autoridad en 72 h ciertas brechas de datos personales; consulta la ley local.

**❓ ¿Cuántas versiones del informe hago?**
Al menos una técnica (detallada) y una ejecutiva (breve, sin jerga). La legal puede requerir formato específico.

## 🔗 Referencias

- SWGDE — Best Practices for Digital Forensics: <https://www.swgde.org/>
- NIST SP 800-86: <https://csrc.nist.gov/publications/detail/sp/800-86/final>
- Reglamento (UE) 2016/679 (GDPR): <https://eur-lex.europa.eu/eli/reg/2016/679/oj>
- ISO/IEC 27037 — Digital evidence handling: <https://www.iso.org/standard/44381.html>

## ➡️ Siguiente clase

[Clase 219 - Ejercicios de mesa (tabletop)](../219-ejercicios-de-mesa-tabletop/README.md)
