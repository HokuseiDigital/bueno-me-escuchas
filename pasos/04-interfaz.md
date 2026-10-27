# Paso 4 — Sal de la consola

## Objetivo

Hablar con el agente desde el navegador, con una interfaz de verdad, sin escribir
código de frontend.

## Qué hay en `frontend/`

Es el template oficial de LiveKit
([agent-starter-react](https://github.com/livekit-examples/agent-starter-react)):
una app de Next.js hecha con [Agents UI](https://livekit.com/products/agents-ui),
la librería de componentes de LiveKit para agentes de voz. Trae el visualizador de
audio, la barra de controles, el chat y la transcripción en vivo
(`frontend/components/agents-ui/`).

Le pusimos la marca de Hokusei Digital: los colores en `frontend/styles/globals.css`
(tema `.dark`), el logo y los textos en `frontend/app/layout.tsx` y
`frontend/components/app/welcome-view.tsx`. Para ponerle la tuya, cambia esos tres.

Ya la instalamos en el paso 0 (`pnpm install`) y ya tiene sus llaves
(`lk app env --write frontend`).

## Comandos

Dos terminales:

```bash
lk agent dev --deployment production
```

```bash
cd frontend
pnpm dev
```

Abre <http://localhost:3000> y dale **Iniciar llamada**.

`lk agent console` corre el agente en tu terminal, con tu micrófono. `lk agent dev`
lo registra en LiveKit Cloud y espera a que alguien entre a una sala: en este caso,
el navegador.

Sin `--deployment production`, `lk agent dev` registra al agente en un deployment de
prueba con nombre al azar (`Using deployment [dev-...]`), aislado del tráfico normal.
El frontend pide al agente solo por nombre, así que LiveKit lo busca en
`production`, no lo encuentra, y la llamada se queda en "Esperando al agente" hasta
que el frontend cuelga.

## Diapositiva: ¿cómo encuentra el navegador a mi agente?

```
Navegador ── pide un token ──▶ frontend/app/api/token/route.ts
Navegador ── entra a una sala con el token ──▶ LiveKit Cloud
LiveKit Cloud ── despacha "bueno-me-escuchas" ──▶ tu laptop (lk agent dev --deployment production)
```

El agente se registra con un nombre en `src/agent.py`:

```python
@server.rtc_session(agent_name="bueno-me-escuchas")
```

y el frontend pide ese mismo nombre en `frontend/.env.local`:

```env
AGENT_NAME=bueno-me-escuchas
```

Si no coinciden, o si olvidaste `--deployment production`, la sala se abre pero el
agente nunca llega.

**Demo:** "¿Qué eventos hay el lunes de Mexico Tech Week?" En la terminal de
`lk agent dev` aparece el mismo `executing tool` del paso 3.

## El problema

Funciona, pero no sabemos qué pasó en el paso del token. ¿Quién decide quién puede
entrar a una sala, y por qué el navegador nunca ve nuestra llave secreta?

## Prompt para el siguiente paso

"Explícame `frontend/app/api/token/route.ts` línea por línea."
