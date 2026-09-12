---
name: preflight-check
description: "Usar antes de dar por terminada cualquier tarea de código en Cambio Hoy, o antes de hacer commit/PR. Corre la verificación completa del proyecto (lint, tipos, tests) y resume el resultado. Trigger: /preflight-check"
---

# /preflight-check

Verificación mínima antes de cerrar una tarea o commitear en "Cambio Hoy". No es una revisión de
diseño (para eso está el agente `api-reviewer` o `/code-review`) — es la barra de calidad
mecánica que el proyecto exige siempre.

## Pasos

1. Correr `make check` (equivale a `lint` + `typecheck` + `test`).
2. Si algo falla:
   - `ruff check` → corregir los hallazgos; nunca silenciar una regla `S` sin justificar por qué
     es un falso positivo en el propio comentario `# noqa`.
   - `mypy` → corregir los tipos; no usar `# type: ignore` como atajo salvo con justificación.
   - `pytest` → arreglar el test o el código, nunca marcar el test como `skip`/`xfail` para
     esquivar el problema.
3. Volver a correr `make check` hasta que pase limpio.
4. Confirmar que no quedaron archivos generados o temporales fuera de lugar (`git status`).
5. Reportar en una línea: qué se verificó y el resultado (todo verde, o qué quedó pendiente y por
   qué requiere decisión del usuario).

No hagas commit ni push como parte de este skill — solo deja el árbol de trabajo verde y
reporta el estado; commitear sigue siendo una decisión explícita del usuario.
