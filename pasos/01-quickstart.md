# Paso 1 — El quickstart de LiveKit

## Objetivo

Tener un agente de voz funcionando en cinco minutos, exactamente como lo entrega
LiveKit, y preguntarle por Mexico Tech Week.

## Comandos

```bash
brew install livekit-cli uv        # o: brew upgrade livekit-cli (las versiones viejas no tienen `lk agent`)
git clone https://github.com/HokuseiDigital/bueno-me-escuchas
cd bueno-me-escuchas
uv sync
lk cloud auth                                  # crea/elige un proyecto gratis en LiveKit Cloud
lk app env --write --destination .env.local    # escribe LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
lk agent console
```

Solo necesitas una cuenta gratis de LiveKit Cloud. Todos los modelos pasan por
LiveKit Inference, así que no hacen falta llaves de OpenAI, AssemblyAI ni Fish Audio.

**Demo:** pregúntale "¿Qué me recomiendas en Mexico Tech Week?" y escucha cómo contesta.

## Diapositiva: ¿qué está pasando?

```
Micrófono → Noise cancellation → STT → Turn detector → LLM → TTS → Bocina
```

| Nodo | Modelo | Qué hace |
|---|---|---|
| Noise cancellation | ai-coustics `QUAIL_VF_S` | Limpia el ruido del micrófono |
| STT | AssemblyAI `universal-3-6-pro` | Tu voz → texto. **Configurado en inglés** |
| Turn detector | LiveKit `TurnDetector` | Decide cuándo terminaste de hablar |
| LLM | Google `gemma-4-31b-it` | Decide qué contestar |
| TTS | Fish Audio `s2.1-pro` | Texto → voz. **Voz en inglés americano** |

Todo vive en `src/agent.py`. Cada nodo es una pieza intercambiable: una línea de código.

## El problema

**Habla como gringo.** Te entiende y te contesta en español, pero de suerte:
AssemblyAI detecta el idioma solo aunque diga `language="en"`, y el LLM contesta en
el idioma en que le hablas. Lo que sí se oye es la voz: Sawyer, un hombre americano,
leyendo español. Y nada de esto está configurado: las instrucciones siguen en inglés.

## Prompt para el siguiente paso

> Cambia el agente en `src/agent.py` para que hable español de México:
> 1. El STT debe usar `language="es"`.
> 2. Cambia la voz de Fish Audio por una voz en español latinoamericano que funcione con LiveKit Inference.
> 3. Traduce las instrucciones del agente al español y dile que es una guía de Mexico Tech Week que habla de tú, con naturalidad, como alguien de la Ciudad de México.
> 4. Que salude en español al iniciar la sesión.
>
> No cambies nada más. Al terminar, dime exactamente qué líneas cambiaste.
