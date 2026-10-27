"""Los eventos de Mexico Tech Week 2026, desde el snapshot incluido en el paquete."""

import json
from dataclasses import dataclass
from datetime import date
from functools import cache
from pathlib import Path

SNAPSHOT = Path(__file__).resolve().parent / "eventos_2026.json"

# Mexico Tech Week 2026, de domingo a miércoles
DIAS = ("2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28")

_DIAS_SEMANA = [
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
    "domingo",
]
_MESES = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


@dataclass(frozen=True)
class Evento:
    id: str
    titulo: str
    dia: str
    inicio: str | None  # "HH:MM", hora de la CDMX; None si es de todo el día
    fin: str | None
    lugar: str  # vacío cuando el anfitrión ocultó la dirección
    url: str


@cache
def todos() -> tuple[Evento, ...]:
    """Todos los eventos de la edición 2026, en orden cronológico."""
    datos = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    return tuple(Evento(**d) for d in datos)


def eventos(dia: str) -> list[Evento]:
    """Los eventos de un día, en formato AAAA-MM-DD."""
    return [e for e in todos() if e.dia == dia]


def _fecha_hablada(dia: str) -> str:
    d = date.fromisoformat(dia)
    return f"{_DIAS_SEMANA[d.weekday()]} {d.day} de {_MESES[d.month - 1]}"


def _linea(e: Evento) -> str:
    horario = f"{e.inicio}–{e.fin}" if e.inicio and e.fin else e.inicio or "todo el día"  # noqa: RUF001
    lugar = e.lugar or "lugar privado"
    return f"- {horario} · {e.titulo} · {lugar}"


def eventos_del_dia(dia: str) -> str:
    """Los eventos de un día como texto, listo para devolverlo desde una herramienta.

    El LLM lee este texto: una línea por evento con horario, título y lugar.
    """
    try:
        fecha = _fecha_hablada(dia)
    except ValueError:
        return f"'{dia}' no es una fecha válida. Usa AAAA-MM-DD, uno de: {', '.join(DIAS)}."
    del_dia = eventos(dia)
    if not del_dia:
        return f"No hay eventos de Mexico Tech Week el {fecha}. Los días son: {', '.join(DIAS)}."
    cuantos = "1 evento" if len(del_dia) == 1 else f"{len(del_dia)} eventos"
    lineas = [f"Mexico Tech Week, {fecha}: {cuantos}."]
    lineas += [_linea(e) for e in del_dia]
    return "\n".join(lineas)
