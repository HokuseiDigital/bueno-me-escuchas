# Paso 2 — Que hable español de México

## Objetivo

Quitarle lo gringo al agente: que entienda español, conteste en español y suene
mexicano. Son tres cambios, uno por nodo.

## Los cambios

Todo en `src/agent.py`:

| Nodo | Antes | Después |
|---|---|---|
| STT (oídos) | `language="en"` | `language="es"` |
| LLM (cerebro) | instrucciones solo en inglés | se agrega `You always respond in Spanish.` |
| TTS (voz) | voz americana `fa4c9eb3…` | `voice=VOCES["joss"]` |

```python
stt=inference.STT(model="assemblyai/universal-3-6-pro", language="es"),
```

```python
tts=inference.TTS(model="fishaudio/s2.1-pro", voice=VOCES["joss"]),
```

## Voces de Fish Audio en español de México

Están en el diccionario `VOCES` al inicio de `src/agent.py`. Para probar otra, cambia
la llave y vuelve a correr `lk agent console`. Para escuchar la muestra de cada una:
`https://fish.audio/m/<id>`.

| Llave | Voz | Perfil |
|---|---|---|
| `joss` ⭐ | Joss Mexico | Hombre joven, amigable, expresivo |
| `mexicano_social` | Mexicano | Hombre joven, relajado, de redes sociales |
| `mexicano` | Mexicano | Hombre joven |
| `mexico_narradora` | México | Mujer joven, narración clara |
| `mexico_maestra` | Mexico | Mujer adulta, educativa, calmada |
| `mexico_anuncio` | mexico | Hombre adulto, enérgico, comercial |
| `mexico_radio_grave` | mexico | Hombre adulto, locutor, voz grave |
| `frnt_mexico` | FRNT MEXICO | Hombre mayor, locutor, enérgico |
| `mexico_radio_calido` | mexico | Hombre mayor, locutor, cálido |

Para encontrar más: busca "mexicano" en https://fish.audio, escucha la muestra y copia
el id de la URL (lo que va después de `/m/`). Las etiquetas de acento no son confiables:
decide de oído.

## Diapositiva

Misma cadena del paso 1, ahora con tres nodos en otro color:

```
Micrófono → Noise cancellation → STT (es) → Turn detector → LLM (español) → TTS (voz mexicana) → Bocina
```

Mensaje: **cada nodo es una pieza intercambiable**. Cambiar de idioma no es un
proyecto, son tres líneas.

## Comandos

```bash
lk agent console
```

**Demo:** misma pregunta que en el paso 1, "¿Qué me recomiendas en Mexico Tech Week?",
para comparar.

## El problema

_Por llenar después de probarlo._

## Prompt para el siguiente paso

_Por llenar._
