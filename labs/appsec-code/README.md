# Lab: Code review y SAST

Laboratorio de **revisión de código segura** y **análisis estático (SAST)** para las clases
**238** (SAST), **323** (pruebas de seguridad del software) y **330** (análisis de código y
automatización). Prepara el dominio *Tools and Code Analysis* de **PenTest+** y *Software
Development Security* de **CISSP**.

> ⚠️ La app de `vulnerable_app/` es **insegura a propósito**. No la despliegues; es para
> analizarla estáticamente y corregirla.

## 🎯 Qué vas a practicar

- Encontrar vulnerabilidades con **SAST** (Semgrep, Bandit).
- Hacer **revisión manual** de código y distinguir hallazgos reales de falsos positivos.
- **Corregir** cada fallo con el patrón seguro correspondiente.

## 🚀 Ejecutar el análisis

Sin instalar nada (usa el contenedor de Semgrep) o con herramientas locales:

```bash
cd labs/appsec-code
./escanear.sh
# o directamente:
docker run --rm -v "$(pwd)":/src semgrep/semgrep semgrep --config auto /src/vulnerable_app
```

## 🧭 Recorrido guiado

1. **Corre el SAST** y lee cada hallazgo: regla, línea, severidad.
2. **Revisa el código a mano** (`vulnerable_app/app.py`): hay **8 vulnerabilidades** plantadas. ¿El SAST las encontró todas? ¿Marcó algo que no es explotable (falso positivo)?
3. **Clasifica** cada hallazgo por riesgo (impacto × explotabilidad) como en un informe real.
4. **Corrige** una por una y vuelve a escanear hasta dejar el reporte limpio.
5. **Integra en CI (opcional):** añade Semgrep como paso de un workflow para que falle ante nuevos hallazgos — es justo lo que hace este repo en su propio pipeline.

## 🏆 Retos verificables

1. **Cobertura del SAST:** documenta cuántas de las 8 detecta Semgrep y cuántas Bandit. *Aceptación:* tabla vuln → ¿detectada por qué herramienta?
2. **Falsos negativos:** identifica las que ninguna herramienta detectó y explica por qué (límite del análisis estático).
3. **Remediación:** entrega el `app.py` corregido; un nuevo escaneo no reporta las 8. *Aceptación:* consultas parametrizadas, `subprocess` sin `shell=True`, Argon2/bcrypt, sin `eval`/`pickle` sobre entrada, validación de rutas, sin secretos en código, `debug=False`.
4. **Gestión de secretos:** mueve `DB_PASSWORD`/`AWS_KEY` a variables de entorno o un gestor de secretos.

## 🗺️ Las 8 vulnerabilidades (categorías)

Inyección SQL · Inyección de comandos · Hash débil · Deserialización insegura · Path traversal ·
Ejecución de código (`eval`) · Secretos embebidos · Debug en producción.

La explicación y la corrección de cada una están en [`SOLUCION.md`](SOLUCION.md) — míralo
**después** de intentarlo.

## 🔗 Referencias

- [Semgrep](https://semgrep.dev/) · [Bandit](https://bandit.readthedocs.io/)
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/) · [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- Parte 11 y Parte 17 del programa — [índice de clases](../../classes/README.md)
