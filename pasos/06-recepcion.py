# Paso 6 — Copia y pega: una recepción enfrente del guía
#
# Parte del paso 5 terminado (o de la rama paso-5). Son cuatro cambios en src/agent.py:
#
# 1. Pega la clase Recepcion de abajo justo antes de `server = AgentServer()`.
#
# 2. En `from livekit.agents import (...)`, agrega `ChatContext`.
#
# 3. En la clase Assistant (que ahora es el guía de eventos):
#
#    a) Cambia la firma de __init__ por:
#
#           def __init__(
#               self, nombre: str, intereses: str, trabajo: str, chat_ctx: ChatContext
#           ) -> None:
#
#    b) En instructions, cambia el bloque de "Hablas con {nombre}..." (lo que va
#       entre paréntesis) por:
#
#           f"Eres el guía de eventos de Mexico Tech Week 2026. Hablas con "
#           f"{nombre}, que es {trabajo} y le interesa {intereses}. No le vuelvas "
#           "a preguntar su nombre, su trabajo ni sus intereses. Preséntate en una "
#           "frase y pregunta qué día quiere ir. Llama a buscar_eventos antes de "
#           "mencionar cualquier evento.",
#
#    c) Agrega `chat_ctx=chat_ctx,` al final de super().__init__(...), después de
#       instructions, para que el guía recuerde la plática con la recepción.
#
# 4. En my_agent, la sesión arranca en la recepción:
#
#           agent=Recepcion(nombre, intereses),
#
# Para probarlo sin micrófono (el debugger no trae token, así que la recepción te
# pregunta tu nombre en vez de confirmarlo):
#
#     lk agent debugger start
#     lk agent debugger say "Me llamo Max"
#     lk agent debugger say "Soy desarrollador, me interesa la inteligencia artificial"
#     lk agent debugger say "El martes veintisiete"
#
# El debugger imprime `tool: perfil_listo(...)` y luego `handoff: recepcion → assistant`.
# Si te atoras: `git checkout paso-6 -- src/agent.py`.


class Recepcion(Agent):
    """Confirma con quién habla, pregunta a qué se dedica y pasa la llamada al guía."""

    def __init__(self, nombre: str, intereses: str) -> None:
        # Lo que ya sabemos por el token. Sin token (console, debugger) no sabemos nada.
        lo_que_sabes = (
            f"Tus datos dicen que hablas con {nombre}, a quien le interesa {intereses}."
            if nombre
            else "No sabes con quién hablas."
        )
        super().__init__(
            # Cada agente trae su propio LLM y su propia voz
            llm=inference.LLM(model="google/gemma-4-31b-it"),
            tts=inference.TTS(
                model="fishaudio/s2.1-pro", voice=VOCES["mexico_narradora"]
            ),
            instructions=textwrap.dedent(
                f"""\
                You always respond in Spanish, in plain spoken text: no markdown, lists
                or emojis, one or two sentences, one question at a time.

                Eres la recepción de Mexico Tech Week 2026: das la bienvenida y pasas la
                llamada a un guía que recomienda eventos. {lo_que_sabes}

                Haz solo esto, en orden:
                1. Saluda. Si sabes su nombre, confírmalo; si no, pregúntalo. Una sola vez.
                2. Pregunta a qué se dedica, una sola vez. Si no sabes qué temas le
                   interesan, pregúntalo en la misma frase.
                3. Llama a perfil_listo. Si no te dio algún dato, usa "desconocido".

                Si te preguntan qué puedes hacer, contesta que lo pasas con un guía que le
                recomienda eventos de Mexico Tech Week, y llama a perfil_listo. No
                recomiendes eventos ni digas que registraste algo.
                """
            ),
        )

    async def on_enter(self) -> None:
        # La recepción habla primero, sin esperar a que el usuario diga algo
        self.session.generate_reply()

    @function_tool
    async def perfil_listo(
        self, context: RunContext, nombre: str, trabajo: str, intereses: str
    ):
        """Pasa la llamada al guía de eventos. Llámala cuando ya sepas su nombre y a qué se dedica.

        Args:
            nombre: El nombre de la persona.
            trabajo: A qué se dedica, por ejemplo "desarrollador de software".
            intereses: Los temas que le interesan, por ejemplo "inteligencia artificial".
        """
        logger.info(f"Perfil listo: {nombre}, {trabajo}, {intereses}")
        # Regresar un Agent desde una herramienta es el handoff. La plática viaja con
        # chat_ctx, sin las instrucciones de la recepción.
        guia = Assistant(
            nombre,
            intereses,
            trabajo,
            chat_ctx=self.chat_ctx.copy(exclude_instructions=True),
        )
        return (
            guia,
            f"Le paso la llamada al guía, que ya sabe que {nombre} es {trabajo}.",
        )
