# mxtw

Los eventos de Mexico Tech Week 2026, listos para darle a un agente de voz.

Es parte del taller **Bueno, ¿me escuchas?**
([HokuseiDigital/bueno-me-escuchas](https://github.com/HokuseiDigital/bueno-me-escuchas)).
Esconde todo el trabajo de leer el calendario de Luma para que en el taller solo
escribamos la herramienta.

## Uso

Viene en el repo del taller, en `packages/mxtw`, como miembro del workspace de uv.
`uv sync` en la raíz del repo lo instala junto con el agente.

```python
from mxtw import eventos_del_dia

print(eventos_del_dia("2026-10-27"))
# Mexico Tech Week, martes 27 de octubre: 100 eventos.
# - 09:00–11:30 · ... · Av. Veracruz 73, Colonia Condesa
```

Como herramienta de un agente de LiveKit, dentro de la clase del agente:

```python
from livekit.agents import RunContext, function_tool
from mxtw import eventos_del_dia


class Assistant(Agent):
    ...

    @function_tool
    async def buscar_eventos(self, context: RunContext, dia: str) -> str:
        """Busca los eventos reales de Mexico Tech Week 2026 de un día.

        Args:
            dia: La fecha en formato AAAA-MM-DD. Mexico Tech Week va del domingo
                25 al miércoles 28 de octubre de 2026.
        """
        return eventos_del_dia(dia)
```

## API

| Nombre | Qué es |
|---|---|
| `eventos_del_dia(dia) -> str` | Los eventos de un día como texto para el LLM. Nunca truena: con una fecha inválida o sin eventos, devuelve una pista |
| `eventos(dia) -> list[Evento]` | Los mismos eventos como datos |
| `todos() -> tuple[Evento, ...]` | Toda la edición 2026 |
| `DIAS` | `("2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28")` |

Las horas están en hora de la Ciudad de México. Cuando el anfitrión ocultó la
dirección en Luma, `lugar` viene vacío y no se publican coordenadas.

## Actualizar los eventos

Los eventos vienen en un snapshot dentro del paquete (`src/mxtw/eventos_2026.json`),
así el agente no depende del internet del lugar. Para refrescarlo desde Luma:

```bash
python -m mxtw.actualizar
git commit -am "Actualizar eventos" && git push
```

Luego, en el proyecto que lo usa: `uv lock --upgrade-package mxtw && uv sync`.

Basado en el parser de eventos de Carlos en `mex-tech-week-spike`.
