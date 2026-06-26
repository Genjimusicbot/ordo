# ORDO v2 — the auto-applied agent layer (architecture + build plan)

The problem this solves: **frameworks die because you have to remember to use them.** ORDO v2 is invisible —
mention it once (a word to Claude, a line in `CLAUDE.md`, a drag-drop, or `/ordo`) and it auto-applies the right
part, persists across the session, and grows with the project. No memorization, no manual invocation.

## The honest product thesis (post-measurement)
Every claim on the page is measured-or-marked. The bold claims are the *proven* ones:
- **Auto compaction** — lossless token compression (measured **−47–68%**, shape-dependent; `tools/ab_smoke.py`).
  This is the spine and it never stops working.
- **One-mention activation, persistent, project-growing** — the UX win: the framework you never have to invoke.
- **The missing tools, bundled** — video/PDF/mp4 vision + a social/web crawler, with ORDO's compaction on their
  output so a transcript or a crawl enters context already shrunk.
- **Honest by construction** — the gates (REFEED/experimentalist/etc.) ship as opt-in discipline, *marked* not
  oversold; the measurements that washed (goal-lock live −3, verify-assert wash on a strong model) are stated, not
  hidden. The honesty IS the conversion lever.

What ORDO v2 is NOT sold as: a magic quality/IQ boost (washes on a frontier model), "faster" (unclocked), or
"self-growing" (human-run loop). Those stay in the scorecard at their true tier.

---

## The three install tiers
A breakdown tab per tier on the wiki; each is one decision the user makes by how much they want.

| | **🟢 ordo.md** (system prompt) | **⚫ ORDO Lean** (install) | **🔶 ORDO Full** (install) |
|---|---|---|---|
| **What it is** | one paste-in file | the compaction core as a skill | the whole layer: core + gates + MCP tools + crawler + vision |
| **Install** | paste `ordo.md` into `CLAUDE.md` / system prompt | `npx ordo init --lean` | `npx ordo init` or `/plugin install ordo` |
| **Gives you** | the discipline as prose (compression + dispatcher) | **token saving only** — format-by-shape + ponytail + inbound, measured-revert | Lean **plus** the classify→route dispatcher, the gates (opt-in), a **crawler + native PDF + a video add-slot** with compaction, persistence + lessons |
| **For** | "I just want it in my prompt" | "I just want fewer tokens / lower bills" | "I want the one install that fixes all the annoyances" |
| **Footprint** | ~1k tokens, zero deps | tiny skill, zero MCP | a plugin + `.mcp.json` (the bundled servers) |
| **Activation** | auto on every turn in that repo | auto-fires on coding/agentic tasks | auto-fires + auto-routes which layer per task |
| **Proven core** | compression (measured) | compression (measured) | compression (measured) + tools (real capability) |

**The lean promise (exactly as scoped):** lean = *only* the compacting + verbosity for token saving. Nothing
that touches quality, no gates, no MCP. The smallest possible thing that pays for itself, as neat and light as
caveman. The full tier is the superset.

---

## Auto-activation — the core mechanism (how it runs nonstop without being invoked)
Three layers, all already partly built; v2 hardens them:
1. **The trigger** — the skill's `description` fires on coding/agentic/research/long-context work (negative
   triggers prevent misfire on trivial replies). One `CLAUDE.md` line or `/ordo` or the plugin loads it once; it's
   then context-resident for the session. Drag-drop = `npx ordo init` drops `.claude/skills/ordo/`.
2. **The router** — `classifyTask()` (the dispatcher) decides *which part* applies per task: LIGHT → just compress
   + answer; STRICT → arm the ledger + the relevant gate. The user never picks; the framework routes. (Note: the
   router's real-world accuracy is being measured via `route_truth.py` — the taxonomy is complete; extraction is
   the open number.)
3. **The persistence** — a project-local `.ordo/ledger.md` + `.ordo/lessons.md` the skill reads at start and
   appends to: it remembers the goal, the decisions, what worked. *That* is "grows with the project" — concrete,
   not aspirational (a human-run evidence loop, marked as such).

---

## The bundled MCP layer (Full tier only) — "the missing tools"
ORDO does not *build* these; it **bundles existing MCP servers** in the Full install's `.mcp.json` and wraps their
output in ORDO's compaction, so the expensive part (huge transcripts, crawls, PDFs) enters context already
lossless-shrunk. This is config + a thin compaction wrapper, honestly scoped.
- **Vision for video / mp4** — a video-understanding MCP (frames → described/transcribed), output ponytail+TSV-compacted.
- **PDF / document decode** — a PDF MCP; the extracted text routed through the inbound compactor.
- **Social / web crawler** — a crawler MCP (the largest socials + the open web), results de-duplicated + compacted
  (the headroom/TSV path) before they hit the window.
- **The ORDO value-add on top:** every tool's output passes the measured-revert inbound gate, so the bundled tools
  cost fewer tokens than wiring them up raw. *That* is the differentiator — not the tools, the compaction of them.

**Honest scope flag:** "implement all our skills" and "bundle every MCP" is a large surface. v2 ships the
**3 anchor MCPs above** + a documented pattern for adding more; the existing house skills (ultra-design, ultra-video,
etc.) are *referenced + compaction-wrapped*, not re-implemented. We add capability per phase, measured, never in a sweep.

---

## Prove-it: every new concept A/B'd (the hard requirement)
Nothing ships as a claim without a measured number at its tier. The harness is built (`tools/judge.py` +
`route_truth`/`trap_corpus`/`goal_lock_bench` + `ab_smoke`/`measure`):
- **Compaction** — already COMPUTED (−47–68%, `ab_smoke`). The headline.
- **MCP-compaction** — A/B the token cost of a video transcript / crawl / PDF *raw vs ORDO-compacted* (a clean
  COMPUTED before/after, like the inbound bench).
- **Auto-activation** — a UX fact, not an A/B (it either fires or it doesn't; demonstrated, not claimed).
- **The gates** — keep their honest tier; the live runs (in progress) report washes plainly. No gate is sold as a
  proven win on a strong model.

---

## The build sequence (phased, verified between — never one sweep)
- **Phase A — the 3-tier packaging + auto-activation.** `ordo.md`, `ordo init --lean`, `ordo init` (full),
  the trigger/description hardening, the `.ordo/` persistence (ledger + lessons read/append). Gate: a fresh repo,
  one mention, ORDO active + persisting; the lean install is *only* compaction. Test cold.
- **Phase B — the bundled MCP layer + the compaction wrapper.** `.mcp.json` for the 3 anchor MCPs; the wrapper that
  routes their output through `compressInbound`. A/B the raw-vs-compacted token delta. Gate: a real video/PDF/crawl
  enters context measurably smaller, lossless.
- **Phase C — the wiki / landing rebuild.** Bold honest hero (the xeno-runic banner), the 3-install comparison
  tabs, a breakdown panel per tier, the measured numbers, custom icons/graphs, the honesty scorecard. Gate: a
  stranger gets *what / who / next action* in the first viewport.
- **Phase D — prove + reconcile.** Run/record the owed A/Bs, then sweep ALL docs for version consistency (no
  mismatches): README, OPERATING-PROFILE, AGENTS, llms.txt, the specs, the scorecard — one version, one set of numbers.

## Imagery
Hero = the clean centered xeno-runic emblem (the biomechanical alien-fetus in the runic frame on tattered canvas,
readable "ORDO") — neat, light, the one focal point. The HUD "PROJECT: ORDO / PHASE III" variant is the secondary
"build status" accent for the dev section. (Files placed in `figures/`; can be regenerated via the image MCP to
exact spec.)

## Honesty stance (the one decision that governs the page)
**Bold on the proven, marked on the rest.** The hero claims are compression + activation + bundled tools (all real).
The gates and the washed instincts are present, honestly tiered. The conversion lever is "every number here is
measured, and the parts that don't work are named" — the moat no competitor has.
