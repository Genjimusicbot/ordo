# ORDO

**A measured, honest context-engineering framework for LLMs.** It cuts tokens, enforces output and
quality discipline, and keeps long autonomous runs safe, with an honest scorecard that tells you exactly
what's proven and what isn't. No magic-multiplier claims; the parts that don't work are named.

Two things ship in one package:
1. **A runtime** (real, tested JavaScript): decode an ORDO command to English, serialize data in the
   cheapest faithful format, compress inbound context losslessly, flag verbosity.
2. **A paste-in operating spec**: the gates and pillars as prompt SOPs your LLM follows.

## What it actually does — and doesn't (the honest scorecard)
| layer | result | evidence |
|---|---|---|
| input command grammar | ~32% fewer tokens | computed (both tokenizers) |
| output contract (format-by-shape + ponytail) | ~55-77% lossless | computed |
| end-to-end (prompt + output) | ~47-64% on a real mix | computed |
| output quality vs plain English | ORDO won 6 / tied 2 / lost 1 (blind) | agent-judged |
| REFEED loop (hard tasks) | first-pass flaws 4→0, at 3.3× tokens | agent-judged |
| **NULLS — do not believe otherwise** | | |
| single-word substitution | ~1% (dead lever) | computed |
| exotic-glyph surface | *inflates* tokens; doesn't transfer to NL | computed + GLOSSOPETRAE |
| wall-clock speed | **no proven win** — only an output-token proxy | unmeasured |
| hallucination on a strong model | **no reduction** (baseline already at floor) | agent-judged |

All token costs are GPT-tokenizer (`tiktoken`) proxies — Claude/Gemini tokenizers are proprietary;
**re-validate on your target model.** A blunt self-evaluation (ORDO scoring *itself* with its own
evaluation gate: **6.5/10 as a product**, with the holes) is in `docs/SELF-EVAL.md`.

## Install
```bash
npm install ordo-llm
```
```js
import { decode, emit, compressInbound, getOperatingProfile } from "ordo-llm";

decode("σ文3列简心金业通¬序");
// -> "summarize the following text in 3 bullet points concisely focusing on the financial figures
//     for a non-expert; do not include any preamble"

emit({ users: [{ id: 1, name: "A" }, { id: 2, name: "B" }] });  // -> TSV (≈55% fewer tokens than JSON)
```
CLI: `npx ordo decode "σ文3列简"` · `npx ordo profile` (prints the spec to paste into your LLM).
Python research/measurement tools live in `tools/` and `harness/` (`pip`-free; stdlib + `tiktoken`).

## Runtime vs methodology (be clear about what executes)
- **RUNTIME** (this package *runs*): `decode`, `emit` / `bestFormat`, `compressInbound`, `ponytailFlags`,
  and the spec loaders. Deterministic, **11/11 tests green** (`npm test`).
- **METHODOLOGY** (prompt SOPs in `spec/*.md`, loaded as text via `getSpec(name)`, **not executed**):
  the gates — REFEED, experimentalist, evaluation, autonomy, context-rot. You hand these to your LLM as
  instructions; ORDO does not run them for you. Calling them "code" would be a lie; they are a
  disciplined system prompt.

## How an AI uses it
Paste `getOperatingProfile()` (or `npx ordo profile`) into your system prompt. The model then: writes
terse ORDO commands, applies the output contract (TSV/minified-JSON/ponytail), and runs the right gate
per task (single pass → REFEED → experimentalist → evaluation → autonomy → context-rot). See
`AGENTS.md` and `llms.txt`.

## The framework
- **Language:** `ORDO.md` (skillstone), `spec/grammar.md`, `spec/lexicon.md`, `spec/macros.md`.
- **Compression:** `spec/output.md`, `spec/pipeline.md` (inbound), `spec/compression-map.md`.
- **Gates:** `spec/framework.md` (REFEED), `spec/experimentalist-gate.md`, `spec/evaluation-gate.md`,
  `spec/autonomy.md`, `spec/context-rot.md`, `spec/orchestration.md`.
- **Pillars + scorecard:** `spec/pillars.md`, `tools/pillars.py` (status-honest: COMPUTED vs
  AGENT-JUDGED vs GROUNDED vs PROXY).
- **The whole thing on one page:** `OPERATING-PROFILE.md`.

## Honesty
`DISCLAIMERS.md` (what it is and is not; private-use ethics — not for evading safety/monitoring),
`VERDICT.md` (every measured number + the cut list), `docs/BUILD-LOG.md` (per-phase what/how/verified),
`docs/SELF-EVAL.md` (the 6.5/10 critique). The moat here is honesty: if a number isn't backed by its
stated evidence tier, it doesn't count. MIT licensed.
