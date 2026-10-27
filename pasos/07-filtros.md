# Paso 7 — Filtros (de tarea)

_Borrador: este paso todavía no está probado en el repo. Ajustar después de
probarlo con el grupo._

## Objetivo

Que el agente encuentre los eventos que te interesan, no todos los del día.

## La idea

El martes tiene 100 eventos. Desde el paso 6 el guía ya sabe qué tema te interesa,
pero `buscar_eventos` solo recibe el día: le llegan todos y lee demasiados o escoge
al azar. Le damos parámetros a la herramienta:

- **por tema**: "de IA"
- **por zona**: "cerca de la Roma"
- **por hora**: "en la tarde"

El LLM decide qué parámetros mandar; tú decides qué parámetros existen. El filtrado
vive en `packages/mxtw`, que ahora está en este mismo repo.

## El problema

_Por llenar después de probarlo._

## Prompt para el siguiente paso

_Por llenar._
