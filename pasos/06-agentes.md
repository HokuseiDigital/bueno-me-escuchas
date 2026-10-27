# Paso 6 — De un agente a dos

## Objetivo

Separar el trabajo en dos agentes. Ponemos una recepción enfrente: saluda con su
propia voz, confirma que habla contigo (tu nombre ya viene en el token del paso 5),
pregunta a qué te dedicas y te pasa con el guía de eventos, que es el agente que ya
teníamos. El guía recibe todo: nombre e intereses del token, y trabajo de la
recepción.

## El cambio

Está todo en [`pasos/06-recepcion.py`](06-recepcion.py): la clase para copiar y pegar y,
arriba, los otros cambios paso por paso. Son cuatro, todos en `src/agent.py`:

1. Pega la clase `Recepcion` antes de `server = AgentServer()`.
2. Importa `ChatContext`.
3. `Assistant` se vuelve el guía: su `__init__` recibe también `trabajo` y `chat_ctx`,
   la línea de "Hablas con..." pasa a "Eres el guía de eventos...", y le pasa
   `chat_ctx=chat_ctx` a `super().__init__`.
4. La sesión arranca en la recepción: `agent=Recepcion(nombre, intereses)`.

La recepción:

```python
class Recepcion(Agent):
    def __init__(self, nombre: str, intereses: str) -> None:
        super().__init__(
            llm=inference.LLM(model="google/gemma-4-31b-it"),        # su propio LLM
            tts=inference.TTS(model="fishaudio/s2.1-pro",
                              voice=VOCES["mexico_narradora"]),       # su propia voz
            instructions=f"... Según su registro, hablas con {nombre}. Confirma que "
                         f"hablas con {nombre} y pregunta a qué se dedica. ...",
        )

    async def on_enter(self) -> None:
        self.session.generate_reply()  # saluda primero

    @function_tool
    async def perfil_listo(self, context: RunContext, nombre: str, trabajo: str,
                           intereses: str):
        """Pasa la llamada al guía de eventos. ..."""
        guia = Assistant(nombre, intereses, trabajo,
                         chat_ctx=self.chat_ctx.copy(exclude_instructions=True))
        return guia, f"Le paso la llamada al guía, que ya sabe que {nombre} es {trabajo}."
```

El guía es el `Assistant` de siempre, con su herramienta del paso 3, su `on_enter` del
paso 5 y la voz de Joss de la sesión. Lo único nuevo es que recibe el trabajo y la
plática.

En `scenarios.yaml` hay un escenario nuevo, `Recepcion hands off to the guide`, que
revisa el handoff de punta a punta.

## Diapositiva: el handoff es una herramienta

| Qué | Por qué |
|---|---|
| Un agente, un trabajo | Instrucciones cortas y enfocadas: el LLM se equivoca menos. |
| Cada uno con su configuración | Su propio LLM, voz y herramientas. La recepción ni ve `buscar_eventos`. |
| Regresar un `Agent` desde una herramienta | Eso es el handoff. El LLM decide cuándo pasar el control. |
| `chat_ctx.copy(exclude_instructions=True)` | El guía recibe la plática sin el prompt de la recepción, y no te vuelve a preguntar nada. |
| Lo del token, a la recepción; lo nuevo, al guía | La recepción no pregunta lo que el token ya dice: solo confirma. El guía recibe las dos cosas. |

```
Token: name="Max", intereses="inteligencia artificial"
Recepción (voz: mexico_narradora)
  "¿Hablo con Max?" → "¿A qué te dedicas?"
  → LLM decide: perfil_listo(nombre="Max", trabajo="desarrollador",
                             intereses="inteligencia artificial")
  → la herramienta regresa un Assistant             ← handoff
Assistant, el guía (voz: joss), con nombre, intereses y trabajo
  "Soy tu guía de eventos. ¿Qué día quieres ir?"
  → buscar_eventos(dia="2026-10-27")
```

## Comandos

```bash
lk agent console
```

o, con la interfaz del paso 4 (que ya manda a Max en el token), `lk agent dev --deployment production`
y `pnpm dev` en `frontend/`.

Para probarlo sin hablar:

```bash
lk agent debugger start
lk agent debugger say "Me llamo Max"
lk agent debugger say "Soy desarrollador, me interesa la inteligencia artificial"
```

El debugger imprime `tool: perfil_listo(...)` y luego `handoff: recepcion → assistant`.

El debugger no trae token, así que la recepción no sabe quién eres: te pregunta tu
nombre, tu trabajo y qué te interesa.

**Demo:** la recepción (voz de mujer) pregunta "¿Hablo con Max?" y a qué te dedicas.
Luego la voz cambia a media llamada: el guía (Joss) se presenta y recomienda según
tus intereses y tu trabajo.

## El problema

El guía ya sabe que te interesa la inteligencia artificial y a qué te dedicas, pero
`buscar_eventos` solo recibe el día. El martes tiene 100 eventos: le llegan todos y lee demasiados o
escoge al azar.

## Prompt para el siguiente paso

"Agrégale filtros a `buscar_eventos`: por tema, por zona y por hora. El filtrado va
en `packages/mxtw`."
