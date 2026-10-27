# Bueno, ¿me escuchas? — Taller paso a paso

Construimos un agente de voz para Mexico Tech Week desde el quickstart de LiveKit,
un problema a la vez. Cada paso tiene su archivo con:

- **Objetivo**: qué vamos a lograr
- **Comandos**: cómo correrlo
- **Diapositiva**: qué explicar
- **El problema**: lo que descubrimos al probarlo, y que motiva el siguiente paso
- **Prompt para el siguiente paso**: lo que le pedimos al agente de código para avanzar

| Paso | Tema | Problema que descubre |
|---|---|---|
| [00](00-preparacion.md) | Prepara tu laptop (tarea antes del taller) | |
| [01](01-quickstart.md) | Quickstart de LiveKit, sin cambios | Habla como gringo |
| [02](02-espanol.md) | Español de México: STT, instrucciones y voz | Finge que busca |
| [03](03-herramientas.md) | Primera herramienta: eventos reales con `mxtw` | Solo vive en la terminal |
| [04](04-interfaz.md) | Sal de la consola: interfaz web con Agents UI | ¿Qué pasó con el token? |
| [05](05-tokens.md) | El token dice quién eres | Un agente hace todo |
| [06](06-agentes.md) | De un agente a dos: recepción que confirma y handoff | El martes tiene 100 eventos |
| [07](07-filtros.md) | Filtros (de tarea) | _Por llenar_ |

## Ramas

`main` es el punto de partida: el quickstart, con el código de los pasos 2, 3 y 5 ya
escrito y comentado (`# Paso 2`, `# Paso 3`, `# Paso 5`). En cada paso lo descomentas.
El paso 6 cambia más cosas, así que trae su propio archivo para copiar y pegar:
`pasos/06-recepcion.py`. Cada paso terminado tiene su rama (`paso-2`, `paso-3`, … `paso-6`), con todo lo anterior incluido. El paso 4 no
cambia código (la interfaz ya está en `frontend/`), así que `paso-4` trae lo mismo que
`paso-3`. Para ver qué cambió en un paso: `git diff paso-2 paso-3`.

## Qué hay en el repo

```
src/agent.py        el agente (pasos 1 a 3, 5 a 7)
tests/              pruebas del agente
scenarios.yaml      simulaciones de conversaciones (lk agent simulate)
packages/mxtw/      el paquete que lee el calendario de Mexico Tech Week
frontend/           la interfaz web: Next.js con Agents UI (pasos 4 y 5)
pasos/              esta guía
```

El agente y `mxtw` son un workspace de uv: `uv sync` instala los dos. El frontend
tiene sus propias dependencias: `cd frontend && pnpm install`.
