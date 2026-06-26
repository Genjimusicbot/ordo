# 🔶 ORDO Full — the whole layer

The one install that fixes the annoyances: Lean's compaction **plus** the auto-router, the gates (opt-in), the
bundled tools, and persistence that grows with the project.

## Install
```bash
npx ordo init        # or: /plugin marketplace add SprucetheAI/ordo → /plugin install
```
Drops `.claude/skills/ordo/SKILL.md` + the operating profile + 16 gate-spec references + `.ordo/`
(`ledger.md` + `lessons.md` + `mcp.json.example`).

## What you get (on top of Lean)
- **Auto-router** — `classifyTask()` decides which part fires per task (light → just compress; hard → arm the
  ledger + the right gate). You never pick.
- **The gates (opt-in, honest)** — REFEED / experimentalist / evaluation / autonomy / context-rot, classify-first.
  *Honestly tiered:* on a frontier model the single-pass instincts mostly **wash** (measured, named in the
  scorecard) — they help where you're under-resourced or on specific traps, and stay off by default.
- **Bundled tools, compaction-wrapped (the differentiator):** a web/social **crawler** (firecrawl, needs a key),
  Claude Code's **native PDF**, and a **video add-slot** (no standard server exists yet — honestly marked). The
  value-add is **compacting every tool's output**: crawl **−62%**, transcript **−46%**, PDF **−24%** (measured,
  `python tools/mcp_compact_ab.py` → `tools/mcp-compact-ab.json`). See [`../../spec/mcp-bundle.md`](../../spec/mcp-bundle.md).
- **Persistence that grows with the project** — the skill reads `.ordo/ledger.md` (goal + decisions) at the start
  of a hard task and appends as it works; lessons accrete to `.ordo/lessons.md`. A human-run evidence loop —
  **not** autonomous self-growth (that claim is a measured null).

## What you DON'T get (the honest bounds)
- Not a magic quality/IQ boost (washes on a frontier model). Not "faster" (unclocked). Not a turnkey video MCP
  (add-slot only). Not autonomous growth. Every one of those is named in [`GTM-REALITY.md`](../GTM-REALITY.md).

## For
"The one install for all of it." Auto-fires + auto-routes; mention it once, it runs nonstop.
