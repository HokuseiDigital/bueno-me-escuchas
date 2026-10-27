"""Regenera el snapshot de eventos desde el calendario público de Luma.

    python -m mxtw.actualizar

Basado en el parser de Carlos (mex-tech-week-spike/compass-agent/src/eventos.py).
Solo usa la librería estándar.
"""

import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

FEED_URL = "https://api.luma.com/ics/get?entity=calendar&id=cal-jWh40NRx2vB56Tu"
SNAPSHOT = Path(__file__).resolve().parent / "eventos_2026.json"

# El feed mezcla las ediciones 2024, 2025 y 2026
EDICION = 2026

# México quitó el horario de verano en 2022: un offset fijo es exacto
CDMX = timezone(timedelta(hours=-6), "CST")

_LUMA_URL = re.compile(r"https://luma\.com/\S+")
_ESCAPADO = re.compile(r"\\([\\;,nN])")
_ESPACIOS = re.compile(r"\s+")
MAX_TITULO = 140


def _desescapar(valor: str) -> str:
    return _ESCAPADO.sub(lambda m: "\n" if m.group(1) in "nN" else m.group(1), valor)


def _limpiar(texto: str, maximo: int | None = None) -> str:
    # Los títulos vienen de la comunidad: sin saltos de línea ni textos enormes,
    # para que no puedan colar instrucciones en el contexto del LLM
    limpio = _ESPACIOS.sub(" ", texto).strip()
    return limpio[:maximo].rstrip() if maximo else limpio


def _lugar(location: str) -> str:
    # Si el anfitrión ocultó la dirección, Luma pone la URL del evento
    if location.startswith("http"):
        return ""
    # Nombre y calle bastan para voz: "Casita Solosé, Altata 310"
    return ", ".join(p.strip() for p in location.split(",")[:2])


def _hora(valor: str) -> datetime:
    utc = datetime.strptime(valor, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    return utc.astimezone(CDMX)


def parsear_ics(texto: str, edicion: int = EDICION) -> list[dict]:
    lineas = re.sub(r"\r?\n[ \t]", "", texto).splitlines()
    eventos, props = [], None
    for linea in lineas:
        if linea == "BEGIN:VEVENT":
            props = {}
        elif linea == "END:VEVENT" and props is not None:
            evento = _a_evento(props)
            if evento["dia"].startswith(str(edicion)):
                eventos.append(evento)
            props = None
        elif props is not None and ":" in linea:
            llave, _, valor = linea.partition(":")
            props[llave.split(";")[0]] = _desescapar(valor)
    return sorted(eventos, key=lambda e: (e["dia"], e["inicio"] or "", e["id"]))


def _a_evento(props: dict[str, str]) -> dict:
    inicio_raw = props["DTSTART"]
    if "T" in inicio_raw:
        inicio = _hora(inicio_raw)
        fin = _hora(props["DTEND"]) if "DTEND" in props else None
        dia = inicio.date().isoformat()
    else:  # evento de todo el día
        inicio = fin = None
        dia = datetime.strptime(inicio_raw, "%Y%m%d").date().isoformat()
    url = _LUMA_URL.search(props.get("DESCRIPTION", ""))
    return {
        "id": props["UID"],
        "titulo": _limpiar(props.get("SUMMARY", ""), MAX_TITULO),
        "dia": dia,
        "inicio": inicio.strftime("%H:%M") if inicio else None,
        "fin": fin.strftime("%H:%M") if fin else None,
        "lugar": _limpiar(_lugar(props.get("LOCATION", ""))),
        "url": url.group(0) if url else "",
    }


def descargar() -> str:
    # Luma contesta 403 al User-Agent por defecto de urllib
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "mxtw"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def guardar(eventos: list[dict], ruta: Path = SNAPSHOT) -> None:
    ruta.write_text(
        json.dumps(eventos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    # Sin argumentos descarga de Luma; con una ruta, usa un .ics local
    texto = Path(sys.argv[1]).read_text("utf-8") if len(sys.argv) > 1 else descargar()
    eventos = parsear_ics(texto)
    guardar(eventos)
    print(f"{len(eventos)} eventos de {EDICION} guardados en {SNAPSHOT}")
