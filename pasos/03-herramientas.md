# Paso 3 — La primera herramienta

## Objetivo

Que el agente busque de verdad. Le damos una herramienta que devuelve los eventos
reales de Mexico Tech Week 2026, y él decide cuándo usarla.

## El cambio

Ya está en `src/agent.py`, comentado con `# Paso 3`: descomenta `RunContext` y
`function_tool` en el import de `livekit.agents`, el import de `mxtw` y la herramienta
dentro de `Assistant`. Quedan así. Dos imports:

```python
from livekit.agents import RunContext, function_tool
from mxtw import eventos_del_dia
```

Y un método dentro de la clase `Assistant`:

```python
    @function_tool
    async def buscar_eventos(self, context: RunContext, dia: str) -> str:
        """Busca los eventos reales de Mexico Tech Week 2026 de un día.

        Args:
            dia: La fecha en formato AAAA-MM-DD. Mexico Tech Week va del domingo
                25 al miércoles 28 de octubre de 2026.
        """
        return eventos_del_dia(dia)
```

`mxtw` ya viene instalado desde el paso 0 (`uv sync`). Es nuestro paquete y vive
en este mismo repo, en [`packages/mxtw`](../packages/mxtw): lee el calendario
público de Luma y esconde todo el parseo. Aquí solo escribimos la herramienta.

## Diapositiva: ¿qué es una herramienta?

Una función de Python + un docstring. **El LLM nunca ve el código, solo esto:**

| Lo que escribimos | Lo que lee el LLM |
|---|---|
| `buscar_eventos` | El nombre de la herramienta |
| El docstring | Cuándo usarla y para qué sirve |
| `dia: str` + `Args:` | Qué parámetro mandar y en qué formato |
| `return eventos_del_dia(dia)` | El resultado, que lee antes de contestar |

```
Tú: "¿Qué hay el lunes?"
  → LLM decide: buscar_eventos(dia="2026-10-26")
  → Python corre la función → 36 eventos reales
  → LLM resume y contesta con voz
```

Para la demo, muestra el log lado a lado con el del paso 2: ahora sí aparece
`executing tool {"function": "buscar_eventos", ...}`.

## Comandos

```bash
lk agent console
```

**Demo:** "¿Qué eventos hay el lunes de Mexico Tech Week?"

## El problema

Ya busca de verdad, pero solo en la terminal. Para enseñárselo a alguien más
necesitamos una interfaz.

## Prompt para el siguiente paso

"Conecta el frontend de `frontend/` a mi agente y córrelo."
