# AGENTS.md — how an AI agent uses ORDO

ORDO upgrades how you (an LLM) handle context, commands, output, and long runs. Load the spec, then
operate by it.

## Activate
Read `OPERATING-PROFILE.md` (or run `npx ordo profile`) and follow it as standing instructions. It is
~1.4k tokens; cache it once. It contains: the honest stance, the compression layers, the gate routing,
the pillars, and the orchestration discipline.

## The contract, in brief
1. **Honesty first.** Solve the real goal, not the prompt. Truth over the pleasing answer. 10 is not the
   target — a right-scoped 9 is optimal; over-engineering scores *down*. Never claim a number above its
   evidence tier.
2. **Compress losslessly.** Commands in readable-ORDO grammar (`spec/grammar.md`); output by data shape
   (tabular → TSV, nested → minified JSON, never pretty-print; prose → ponytail, cut the filler);
   inbound docs via `compressInbound()` for the lossless cases.
3. **Classify, then gate.** Easy/deterministic → single pass. Hard, one answer → REFEED
   (`spec/framework.md`). Hard, real fork → experimentalist (`spec/experimentalist-gate.md`). Before
   "done" → evaluation gate (`spec/evaluation-gate.md`). Long autonomous run → autonomy gate
   (`spec/autonomy.md`). Long/complex context → context-rot gate (ledger + compact, `spec/context-rot.md`).
4. **Persist via a ledger,** not chat: single-writer, append-only, handoffs-as-pointers, the approval
   queue for side effects (`spec/orchestration.md`).

## The runtime you can call (Node)
```js
import { decode, emit, compressInbound, ponytailFlags, getSpec } from "ordo-llm";
decode("σ文3列简");        // ORDO command -> full English instruction
emit(data);                // cheapest faithful format
compressInbound(doc);      // lossless inbound compression
ponytailFlags(text);       // filler the output contract forbids
getSpec("framework");      // load a gate's SOP as text
```
The gates are SOPs you apply, not code that runs — `getSpec()` returns them as instructions.

## Honest limits
GPT-tokenizer proxies (re-validate on your model); no proven wall-clock win; the glyph form is opt-in
(readable-ORDO is canonical and decodes more reliably). See `docs/SELF-EVAL.md`.
