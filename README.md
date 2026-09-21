# 💱 python-arsenal

Este repo es también la demo en vivo de la charla **"Construye tu propio ejército de agentes: Claude Code para tu proyecto Python"** — PyDay Boyacá 2026. El historial de commits muestra el antes y el después de configurarle a Claude Code un arsenal de disciplina de ingeniería (`.claude/`).

Conversor USD → COP con la TRM oficial (Superintendencia Financiera de Colombia, vía [datos.gov.co](https://www.datos.gov.co/)) y el precio de Bitcoin en pesos, vía [CoinGecko](https://www.coingecko.com/).

```
170d31c  Base: conversor USD/COP con TRM oficial, sin arsenal .claude
3c5dde4  feat: arsenal python          ← Claude construye .claude/ con un solo prompt
dab8b79  feat: bitcoin                 ← misma integración, ahora con disciplina
```

---

## 📁 Estructura

```
src/app/
├── main.py                     # FastAPI: home (HTML), /convertir, /trm, /bitcoin, /health
├── schemas.py                   # Contratos Pydantic de request/response
├── http_client.py               # Cliente HTTP compartido con retry/backoff (httpx + tenacity)
└── integrations/
    ├── trm_client.py            # Integración con la TRM oficial
    └── coingecko_client.py      # Integración con CoinGecko (precio de Bitcoin)
```

---

## 🧠 El arsenal: `.claude/`

Nada de esto se escribió archivo por archivo: se le pidió a Claude Code en una sola instrucción en lenguaje natural — "configura un arsenal de disciplina de ingeniería, con las herramientas estándar de la industria Python actual" — y decidió sola qué piezas necesitaba y cómo configurarlas.

```
.claude/
├── CLAUDE.md                        # La constitución del proyecto: siempre presente, sin que se pida.
│                                     # Define el stack obligatorio (uv, httpx, tenacity, Pydantic v2,
│                                     # ruff, mypy --strict, pytest+respx), el patrón exacto para
│                                     # construir una integración nueva, y las reglas de seguridad
│                                     # no negociables (nunca loguear secretos, nunca silenciar un
│                                     # hallazgo `S` de ruff sin justificar).
│
├── agents/
│   ├── integration-builder.md       # Se activa al pedir una integración nueva a una API externa.
│   │                                 # Construye cliente + schema + endpoint + tests siguiendo
│   │                                 # CLAUDE.md al pie de la letra. Antes de escribir, relee el
│   │                                 # patrón vigente en trm_client.py — no asume, verifica.
│   │
│   └── api-reviewer.md              # Se activa antes de dar una integración por terminada.
│                                     # Audita (no edita) el resultado: contrato del cliente, manejo
│                                     # de errores, tipado, seguridad, cobertura de tests. Reporta
│                                     # hallazgos por severidad, o dice "todo limpio" si no hay nada.
│
├── skills/
│   ├── new-integration/             # /new-integration — checklist operativo completo: investigar
│   │   └── SKILL.md                 # la API real → delegar a integration-builder → revisar con
│   │                                 # api-reviewer → verificar contra la API real → make check.
│   │
│   └── preflight-check/             # /preflight-check — verificación mecánica antes de cerrar una
│       └── SKILL.md                 # tarea o commitear: corre lint + tipos + tests, corrige lo que
│                                     # falle, nunca permite silenciar errores sin justificación.
│
└── settings.json                    # Hooks de automatización:
                                      #  · PostToolUse → ruff format + fix en cada Write/Edit de un .py
                                      #  · Stop → ruff + mypy --strict + pytest sobre todo el proyecto
                                      #    al terminar cada tarea, sin que nadie lo pida
```

**El punto central:** se le dio a Claude el contexto del proyecto y el criterio de "disciplina de ingeniería real" — y decidió el resto: qué reglas escribir, qué agentes delegar, qué automatizar con hooks.

---

## 📝 La idea de fondo

El objetivo no era que Claude escribiera Python — para eso ya es bueno por defecto. Era darle el mismo criterio de ingeniería que usa un equipo humano serio: qué patrón seguir, qué verificar antes de terminar, y quién audita el resultado. Ese criterio se puede llevar a **cualquier proyecto Python nuevo**: copia la carpeta `.claude/` completa, ajusta `CLAUDE.md` al dominio nuevo, y el resto ya está listo.
