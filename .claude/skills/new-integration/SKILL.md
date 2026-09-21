---
name: new-integration
description: "Usar cuando se pide agregar un nuevo indicador financiero o una nueva integración a una API externa en el proyecto Cambio Hoy. Guía el flujo completo: cliente, schema, endpoint, tests, verificación. Trigger: /new-integration <descripción del dato/API>"
---

# /new-integration

Flujo estándar para agregar una integración nueva a "Cambio Hoy". Sigue las reglas de
`CLAUDE.md` — este skill es el checklist operativo, no las reemplaza.

## Pasos

1. **Investigar la API externa** antes de escribir nada: endpoint público exacto, forma del
   JSON de respuesta, si requiere API key (si la requiere, decírselo al usuario — este proyecto
   solo usa APIs públicas sin autenticación, como datos.gov.co; una API con key es una decisión
   que el usuario debe tomar explícitamente, no asumirla).

2. **Delegar la construcción al agente `integration-builder`** (vía Agent tool) pasándole:
   - Nombre del servicio y URL exacta del endpoint a consumir.
   - Forma esperada del JSON de respuesta (con un ejemplo real si es posible).
   - Qué dato debe exponerse y en qué endpoint/página debe mostrarse.

3. **Revisar con el agente `api-reviewer`** el resultado antes de darlo por terminado.

4. **Verificar manualmente en vivo**: levantar `make dev` y hacer un `curl`/fetch al endpoint
   nuevo contra la API real (no mockeada) al menos una vez, para confirmar que el contrato
   asumido en los tests coincide con la respuesta real de la API.

5. **Actualizar `README.md`** si se agregaron endpoints o archivos nuevos (sección "Endpoints"
   y árbol de `src/app/`).

6. Confirmar que `make check` pasa antes de considerar la tarea completa.

## Cuándo NO usar este flujo

- Cambios puramente visuales/HTML sin nueva fuente de datos → no requieren cliente ni schema
  nuevos, edítalos directamente en `main.py`.
- Si la API requiere autenticación o tiene rate limits estrictos que afecten el diseño (ej.
  necesita caché), pregunta al usuario cómo manejar la key/secreto antes de codificar — nunca
  hardcodees credenciales.
