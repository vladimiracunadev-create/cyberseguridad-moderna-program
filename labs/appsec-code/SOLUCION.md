# Solución — Code review y SAST

Las 8 vulnerabilidades de `vulnerable_app/app.py`, su categoría (CWE) y la corrección.

| # | Línea (aprox.) | Vulnerabilidad | CWE | Corrección |
|---|---|---|---|---|
| 1 | `DB_PASSWORD` / `AWS_KEY` | Secretos embebidos en el código | CWE-798 | Leer de variables de entorno o un gestor de secretos; rotar y escanear con gitleaks. |
| 2 | `/user` | Inyección SQL por concatenación | CWE-89 | Consulta parametrizada: `conn.execute("SELECT * FROM users WHERE name = ?", (name,))`. |
| 3 | `/ping` | Inyección de comandos (`shell=True`) | CWE-78 | `subprocess.check_output(["ping","-c","1", host])` sin `shell=True` y validando `host`. |
| 4 | `/hash` | Hash débil sin sal (MD5) | CWE-327/916 | Usar Argon2id / bcrypt / scrypt con sal para contraseñas. |
| 5 | `/load` | Deserialización insegura (`pickle`) | CWE-502 | No deserializar datos no confiables; usar JSON o formatos con esquema. |
| 6 | `/read` | Path traversal | CWE-22 | Normalizar y validar que la ruta resuelta esté dentro del directorio permitido (`os.path.realpath` + prefijo). |
| 7 | `/calc` | Ejecución de código (`eval`) | CWE-95 | Nunca `eval` sobre entrada; usar un parser seguro (p. ej. `ast.literal_eval` o una librería de expresiones). |
| 8 | `app.run(debug=True)` | Debug en producción | CWE-489 | `debug=False`; el debugger de Werkzeug permite RCE si queda expuesto. |

## Qué suele detectar cada herramienta

- **Semgrep (`--config auto`)** detecta con fiabilidad: SQLi (2), command injection (3), `pickle` (5), `eval` (7), MD5 (4), `debug=True` (8) y los secretos (1) con sus reglas de secrets.
- **Bandit** marca: `subprocess`/`shell=True` (B602), `md5` (B303/B324), `pickle` (B301), `eval` (B307), `flask debug` (B201), hardcoded password (B105/B106).
- **Path traversal (6)** es el más propenso a **falso negativo**: muchas reglas genéricas no lo detectan sin taint-tracking configurado. Enséñalo como límite del SAST → por eso hace falta también revisión manual y DAST.

## Lección

El SAST es excelente como primera red (y como *gate* en CI), pero **no sustituye** la revisión
humana ni las pruebas dinámicas. La combinación SAST + code review + DAST/SCA es lo que pide
un SDLC seguro (clases 236–248 y 323).
