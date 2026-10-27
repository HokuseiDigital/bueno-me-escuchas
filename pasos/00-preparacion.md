# Paso 0 — Prepara tu laptop

## Objetivo

Llegar al taller con todo instalado. El wifi del lugar no aguanta 30 descargas a la
vez, así que esto es tarea antes del día.

## Qué necesitas

- Una cuenta gratis de [LiveKit Cloud](https://cloud.livekit.io/).
- [uv](https://docs.astral.sh/uv/) para el agente (Python).
- [Node.js 24](https://nodejs.org/) y [pnpm](https://pnpm.io/) para la interfaz web
  del paso 4.
- La [CLI de LiveKit](https://docs.livekit.io/intro/basics/cli/), versión 2.18.8 o
  más nueva. Si ya la tienes, actualízala: las versiones viejas no tienen `lk agent`.

## Comandos

```bash
brew install livekit-cli uv node pnpm
git clone https://github.com/HokuseiDigital/bueno-me-escuchas
cd bueno-me-escuchas
uv sync
(cd frontend && pnpm install)
lk cloud auth
lk app env --write --destination .env.local
lk app env --write frontend
lk agent console
```

- `uv sync` instala el agente y `mxtw`, que vive en `packages/mxtw`.
- `pnpm install` instala la interfaz web de `frontend/`.
- El primer `lk app env` escribe las llaves del agente en `.env.local`.
- El segundo las escribe en `frontend/.env.local`, junto con el nombre del agente
  que viene en `frontend/.env.example`.

Todos los modelos pasan por LiveKit Inference: no hacen falta llaves de OpenAI,
AssemblyAI ni Fish Audio.

## Listo si

Ves el prompt de `lk agent console`.

## Si te atrasas

`main` es el punto de partida. Cada paso terminado tiene su rama, de `paso-2` a
`paso-6`. Para alcanzar al grupo con el paso 3 ya hecho:

```bash
git stash            # guarda tus cambios, si hiciste alguno
git checkout paso-3
uv sync
```
