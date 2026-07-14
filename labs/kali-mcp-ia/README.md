# Lab: Pentest asistido por IA con MCP (kali-mcp)

Laboratorio para la **Parte 18 — IA aplicada a la ciberseguridad** (clases 331–340). Monta un
agente de IA que orquesta herramientas de Kali mediante **MCP**, usando el proyecto de código
abierto **[kali-mcp](https://github.com/pabpereza/kali-mcp)** (de *pabpereza*, licencia **MIT**).

> 🙏 **Atribución.** Este lab **usa y referencia** kali-mcp; no lo redistribuye. Todo el crédito
> del servidor MCP y sus playbooks es de su autor. Consulta el repositorio oficial para la
> documentación, los comandos y la licencia.
>
> ⚠️ **Solo objetivos propios o autorizados.** Que la IA automatice el trabajo no cambia la ley:
> ejecuta **únicamente** contra tus propias VMs en una red aislada o con autorización explícita
> por escrito. La autorización y la responsabilidad son **humanas**.

## 🎯 Qué vas a practicar

| Objetivo | Clases |
|---|---|
| Entender MCP y los agentes con herramientas | [332](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/332-agentes-de-ia-y-el-model-context-protocol-mcp-para-seguridad/README.md) |
| Montar y operar kali-mcp | [333](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/333-kali-mcp-orquestar-herramientas-de-kali-desde-un-agente-de-ia/README.md) |
| Recon, OSINT y auditoría web asistidos | [334](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/334-reconocimiento-y-escaneo-asistidos-por-ia/README.md), [336](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/336-osint-y-auditoria-web-con-agentes-de-ia/README.md) |
| Informe y guardrails | [338](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/338-generacion-de-informes-y-flujos-de-trabajo-con-ia/README.md), [339](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/339-riesgos-guardrails-opsec-y-etica-del-hacking-con-ia/README.md) |
| Operación completa (capstone) | [340](../../classes/parte-18-ia-aplicada-a-la-ciberseguridad/340-capstone-pentest-autorizado-asistido-por-ia-con-mcp/README.md) |

## 🧰 Requisitos

- **Docker y Docker Compose** (ver [Clase 022](../../classes/parte-0-fundamentos-y-prerrequisitos/022-docker-y-contenedores-para-laboratorios-de-seguridad/README.md)).
- Un **cliente de IA con soporte MCP** (p. ej. Claude Code, Gemini CLI).
- Un **objetivo autorizado propio**: una VM vulnerable (Metasploitable, DVWA, o el
  [lab appsec-web](../appsec-web/README.md)) en **red aislada**.

## 🚀 Montaje (según el proyecto oficial)

kali-mcp trae su propia infraestructura Docker; se instala desde su repositorio:

```bash
git clone https://github.com/pabpereza/kali-mcp.git
cd kali-mcp
./init.sh            # levanta el contenedor Kali + el gateway MCP (ver su README)
```

Luego configura tu cliente de IA para usar el servidor MCP de kali-mcp (archivo `.mcp.json` del
proyecto). Sigue **siempre** la documentación oficial del repo para los pasos exactos y la
resolución de problemas (carpeta `docs/`).

## 🧭 Flujo de trabajo guiado

Con tu VM de laboratorio como **único** objetivo del alcance:

1. **Inicio y alcance** — declara tu VM como objetivo autorizado (comando de inicio del proyecto).
2. **Recon supervisado** — pide descubrimiento de hosts/puertos y **valida** a mano (clase 334).
3. **Auditoría web** — sobre tu app propia; clasifica hallazgos en confirmado / falso positivo (clase 336).
4. **PoC de bajo impacto** — apruébala tú explícitamente; registra comando y resultado (clase 335).
5. **Informe** — genera el borrador y verifica cada hallazgo contra la evidencia (clase 338).

## 🏆 Retos verificables

1. **Aislamiento:** demuestra que el contenedor de Kali no puede alcanzar redes fuera de tu laboratorio.
2. **Validación:** de los hallazgos del agente, confirma manualmente al menos el 50% y marca los falsos positivos.
3. **Trazabilidad:** entrega el registro de acciones aprobadas/ejecutadas de la sesión.
4. **Guardrails:** entrega tu matriz de permisos (auto / aprobación / prohibido) del agente.

## 🧯 Apagar

Sigue las instrucciones del proyecto para detener sus contenedores (p. ej. `docker compose down`
en su carpeta `docker/`).

## 🔗 Referencias

- **kali-mcp (MIT)** — <https://github.com/pabpereza/kali-mcp>
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/)
- Parte 18 del programa — [índice de clases](../../classes/README.md)
