# Paso 5 — El token dice quién eres

## Objetivo

Entender qué hizo el frontend en el paso 4 antes de entrar a la sala, y usar ese
mismo token para decirle al agente quién eres. Al final, el agente te saluda por tu
nombre sin preguntarlo.

## El recorrido

1. El navegador hace `POST /api/token` y manda la configuración de la sala, que
   incluye el agente que quiere (`AGENT_NAME`).
2. La ruta (`frontend/app/api/token/route.ts`) corre en el servidor de Next.js, no
   en el navegador. Ahí viven `LIVEKIT_API_KEY` y `LIVEKIT_API_SECRET`, que leyó de
   `frontend/.env.local`.
3. Inventa una sala (`voice_assistant_room_1234`).
4. `livekitToken` firma un token (un JWT) con la llave secreta. El token dice:
   - **quién eres**: `identity`, `name` y `attributes`
   - **a qué sala puedes entrar**: `room`, `roomJoin`
   - **qué puedes hacer ahí**: publicar audio, mandar datos, escuchar
   - **cuánto dura**: `ttl: '15m'`
   - **qué agente despachar** cuando entres: `roomConfig`
5. Regresa la URL del servidor y el token. El navegador entra a LiveKit Cloud con
   ese token, y LiveKit Cloud despacha a `bueno-me-escuchas` a la sala.

## El cambio

Ya está comentado con `# Paso 5` (`// Paso 5` en TypeScript) en los dos archivos.

Tu app ya está detrás de un login: tu middleware verificó la sesión (cookie o JWT) y
te dice quién es. Para el taller lo fingimos: al final de
`frontend/app/api/token/route.ts` está `usuarioDeTuSesion()`, que regresa un usuario
fijo (Max). Descomenta esa función, y en `POST` cambia el usuario al azar del
quickstart por el de tu sesión:

```ts
const usuario = usuarioDeTuSesion();
const participant: AccessTokenOptions = {
  identity: usuario.id,
  name: usuario.nombre,
  attributes: { intereses: usuario.intereses },
};
const participantToken = await livekitToken(participant, roomName, roomConfig);
```

`livekitToken` firma el token de LiveKit con `LIVEKIT_API_SECRET`: quién eres, qué
sala, qué puedes hacer y por cuánto tiempo.

En `src/agent.py` son cuatro bloques: la firma de `__init__`, el bloque de "Hablas
con..." en las instrucciones, `on_enter` y la lectura del token en `my_agent`. El agente entra a la sala, espera al participante y lee lo que dice su
token:

```python
await ctx.connect()
participante = await ctx.wait_for_participant()
logger.info(f"Token: identity={participante.identity} name={participante.name} ...")
nombre = participante.name
intereses = participante.attributes.get("intereses", "")

await session.start(agent=Assistant(nombre, intereses), ...)
```

`Assistant` recibe los dos y los pone al principio de sus instrucciones: "Hablas con
Max, a quien le interesa la inteligencia artificial. Salúdalo por su nombre y no le
preguntes cómo se llama".

Para que el agente tome el primer turno hacen falta dos cosas: `on_enter` llama a
`self.session.generate_reply()` en cuanto arranca, y `ctx.connect()` va antes de
`session.start`, porque el agente necesita estar en la sala para hablar.

`lk agent console` y el debugger no traen token: ahí el agente no sabe quién eres
("No sabes con quién hablas") y te saluda sin nombre. Así sabes que, cuando dice
"Hola, Max", el nombre vino del token.

## Diapositiva: del token a la voz

```
Navegador          route.ts           LiveKit Cloud        Tu agente
   │ 1 POST /api/token ▶│                    │                   │
   │◀ 2 token (15 min) ─│                    │                   │
   │ 3 entra a la sala con el token, WebRTC ▶│                   │
   │                    │                    │ 4 despacha ──────▶│
   │                    │                    │◀ 5 entra a la sala│
   │◀═══════════ 6 audio en tiempo real, por LiveKit Cloud ═════▶│
```

1 y 2 son HTTP contra nuestro servidor de Next.js. 3 y 5 son WebRTC. El navegador
y el agente nunca se conectan directo: los dos entran a la misma sala en LiveKit
Cloud, que reparte el audio.

## Diapositiva: lo que ya sabes no se pregunta

```
Tu login ──▶ route.ts firma identity, name, attributes
          ──▶ el navegador entra con el token
          ──▶ el agente lee participante.name y participante.attributes
          ──▶ "Hola, Max"
```

El agente confía en esos datos porque los firmó tu servidor con una llave que solo
él tiene. El navegador no puede cambiarlos sin romper la firma.

## ¿Y en una app de verdad?

1. `/api/token` se protege igual que el resto de tu app: tu cookie de sesión o tu
   JWT. Si no hay sesión, no hay token.
2. La ruta saca `identity` de tu usuario (su id), no de un número al azar, y pone en
   `name` y `attributes` lo que el agente necesita saber.
3. El agente nunca ve el JWT de tu app. Solo ve lo que firmaste en el token de
   LiveKit.
4. Si el agente necesita tu API (reservas, perfil), la llama de servidor a servidor
   con sus propias credenciales y el `identity` del usuario.

No le pases el JWT de tu app al agente: caduca a media llamada, puede hacer más de
lo que el agente necesita, y puede terminar en un log o en el contexto del LLM.

Dos detalles:

- Los `attributes` del participante los ve **todo el que esté en la sala**. Lo que
  solo debe ver el agente va en la metadata del despacho (`metadata` en el agente de
  `RoomConfiguration`), que el agente lee como `ctx.job.metadata`.
- Si el agente actúa en otro servicio a nombre del usuario (su Google Calendar, por
  ejemplo), esos tokens de OAuth se quedan en tu backend. El agente se los pide con
  el `identity`.

Ver [Token generation in production](https://docs.livekit.io/frontends/build/authentication/).

## Comandos

Igual que el paso 4:

```bash
lk agent dev --deployment production
```

```bash
cd frontend
pnpm dev
```

**Demo:** dale **Iniciar llamada**. El agente habla primero: "Hola, Max. He oído que
te interesa la inteligencia artificial...". En la terminal del agente aparece
`Token: identity=usuario_max name=Max attributes={'intereses': 'inteligencia artificial'}`.
Cambia el nombre en `usuarioDeTuSesion()`, vuelve a llamar y escucha la diferencia.

## Para probar

Abre las herramientas de desarrollador del navegador, pestaña **Network**, inicia
una llamada y busca la petición a `/api/token`. Copia el `participantToken` de la
respuesta y pégalo en <https://jwt.io>: ahí están `name: "Max"` y
`attributes: { "intereses": ... }`, junto con los permisos de la sala.

## Antes de producción

La ruta se niega a correr fuera de desarrollo (`NODE_ENV !== 'development'`): hoy
cualquiera que la llame recibe un token a nombre de Max. En producción va detrás de
tu login, como dice arriba.

Alternativa sin código propio: el
[development token server](https://docs.livekit.io/frontends/build/authentication/development-token-server/)
de LiveKit Cloud. Se prende en la configuración del proyecto y se pone su ID en
`LIVEKIT_TOKEN_SERVER_ID`. Es solo para desarrollo, igual que esta ruta.

## El problema

El agente ya sabe quién eres, pero un solo agente con un solo prompt hace todo:
recibe, confirma y recomienda, con la misma voz.

## Prompt para el siguiente paso

"Pon una recepción antes del agente, con otra voz: que confirme que está hablando
conmigo, me pregunte a qué me dedico, y luego me pase con el agente que recomienda
eventos sin volver a preguntar nada."

O sin agente de código: sigue `pasos/06-recepcion.py`, que trae la clase para copiar y
pegar y los otros tres cambios.
