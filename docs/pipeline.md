# ORDO full pipeline — the three sides of the token triangle

A request to an LLM has three token pools, and until now ORDO only worked two of them:

```
   ┌─ INBOUND CONTEXT ─┐   ┌─ COMMAND ─┐        ┌─ OUTPUT ──────────┐
   files · tool output ·   the instruction       what the model
   logs · RAG · history    you type               writes back
        │                       │                      │
   headroom (NEW)          ORDO-G grammar         ponytail + caveman + format
   60-95% (lossy/rev)      ~32% (lossless)        up to 77% (ponytail lossless)
```

Headroom (`pip install headroom-ai`, Apache-2.0) fills the missing INBOUND side: it compresses what the
model *reads* (content-type-aware: SmartCrusher for JSON, CodeCompressor for AST, an entropy/structure
mask + an HF model for prose), and is **reversible** (CCR caches originals; the model retrieves on
demand). It is LOSSY, so every ratio is comprehension-tested, not trusted.

## How the three multiply (the honest recalculation model)
The three layers act on **different token pools**, so they do not simply add — total reduction is
pool-weighted:

```
total_saved = 1 − (inbound·(1−Ri) + command·(1−Rc) + output·(1−Ro)) / (inbound + command + output)
```
where R = the measured reduction of each layer and the pools are the token counts. In a typical agent
turn INBOUND dominates (a 10k-token file dump vs a 20-token command vs a 200-token answer), so the
inbound layer (headroom) is the biggest single multiplier on real workloads — which is exactly why the
user flagged it. Measured per-layer numbers (this repo):
- **Inbound** — headroom: 60-95% claimed (agent workloads); **to be measured on our content** below.
  Built-in fallback floor (lossless): JSON→TSV 72%, prose-whitespace ~33%.
- **Command** — ORDO-G readable grammar: **32%** (decode 2.00/2).
- **Output** — ponytail **77%** lossless + format-by-shape (TSV) ~55% + caveman 68% (operational).

## Measured on OUR content (`harness/inbound.py` take-best, `headroom-ai` 0.27.0)
| content | before | after | cut | engine | note |
|---|---:|---:|---:|---|---|
| logs / tool-output | 3119 | 236 | **92%** | headroom | its sweet spot (redundant) — but LOSSY (see below) |
| structured JSON | 2824 | 1268 | **55%** | our TSV | base-headroom noop'd it; our format-rule wins, lossless |
| code | 2221 | 2049 | 7% | builtin | headroom CodeCompressor noop'd on base install |
| dense prose doc | 3185 | 3162 | 0% | builtin | ML prose (Kompress) needs onnxruntime and is lossy + modest even then |

**Recalculated total (`tools/pipeline_recalc.py`):** a realistic mixed agent turn = **~47% combined**
across all three layers; a **log/tool-heavy turn ≈ 88%** (inbound dominates); a **dense-prose-library
turn ≈ 13%** (inbound resists — the win shifts to output + the novel levers).

**The honest headroom finding.** Its 92% is **lossy sampling**: it keeps ~5 representative lines and a
marker — `[40 matches compressed to 5. Retrieve more: hash=…]` — with a CCR retrieval handle. So it is
**gist-preserving but aggregate-lossy**: "what do these log lines look like?" survives; "how many
status-500 errors?" / "what's the max latency?" do **not**, unless the model retrieves the originals.
Routing consequence baked into `inbound.py`: **lossless (our TSV) when the model must ANALYZE the data;
headroom's sampling only when it just needs the SHAPE** (with CCR retrieval as the safety net). The
"90% on docs" claim is really "90% on redundant agent context," not dense prose.

A worked example with realistic pool sizes is in `tools/pipeline_recalc.py`.

## The integration (clean separation, no double-work)
Headroom's verbosity-steering **overlaps** our output layer — so we do NOT stack both on output (that
would double-compress and risk quality). The division of labour:
- **INBOUND → headroom** (its strength: docs/tools/code/logs/history). `harness/inbound.py` wraps it
  with a lossless built-in fallback.
- **COMMAND → ORDO-G** (lossless, unambiguous, our grammar).
- **OUTPUT → our ponytail/caveman/format** (measured, lossless ponytail). Headroom's output-shaper is
  an alternative we benchmark against, not a second pass.

## Non-thought-about inbound levers (beyond what headroom does)
Headroom already does content-routing, JSON/AST/prose compression, entropy masking, CCR, cache
alignment, cross-agent dedup. These are the levers it does **not** lean on — ranked by upside:

1. **Don't-send-it (lazy / just-in-time context).** The biggest lever is not compressing a doc but not
   sending it until the model asks. Replace an inlined doc with a 1-line index entry + a retrieval tool;
   most context is never actually read. (CCR is adjacent but still sends a compressed copy; true JIT
   sends ~nothing until requested.) **Upside: the headline 90% on doc-heavy workloads.**
2. **Delta / diff context across turns.** In an agent loop the same file is re-read every turn; send the
   *diff* since last turn, not the full restated file. Compounds over a session.
3. **Glossary substitution turned INWARD (uniquely ours).** Apply ORDO's phrase-map + macros to the
   *document*, not just the command: recurring long phrases → short codes, the legend sent once
   (amortized). This is the one lever that *composes* with the language and stacks on headroom.
4. **Identifier aliasing.** A 36-char UUID / long file path repeated 50× → `u1` + a one-line legend.
   Pure structural win, lossless, common in logs/traces.
5. **Relevance-gated inclusion (quality-IMPROVING compression).** Embed the query + chunks, include only
   top-k by relevance, drop distractors. LongLLMLingua measured **+17% RAG accuracy at 4×** — less
   context, *better* answers (the lost-in-the-middle effect). The rare compression that helps quality.
6. **Structural skeletonization (browse-then-drill).** For a big doc send the outline (headings + first
   sentence per section) + a retrieval handle; the model drills only the sections it needs.
7. **Boilerplate stripping.** License headers, repeated imports, copyright blocks, base64 blobs, ASCII
   art → a 1-line marker. Lossless, ubiquitous in code dumps.
8. **Image/diagram → dense caption** (headroom has image compression; the text-caption variant is often
   cheaper when the model needs the *content*, not the pixels).
9. **Precision downcasting (gated, lossy).** Long float tables / over-precise numbers rounded to the
   precision the task needs.

The two we should build because they are novel AND compose with ORDO: **#3 glossary-inward** (turns our
own phrase/macro map into an inbound compressor) and **#5 relevance-gating** (compression that improves
quality, the strongest "more than tokens" story). #1 (JIT) is the biggest but is a runtime/harness
concern, not a transform — it belongs in the auto-apply runtime.

## Honesty
Headroom is lossy-but-reversible; we comprehension-test every compressed inbound (a TSV/TOON-style
QA check) before trusting a ratio. The three-layer total is pool-weighted, not additive, and dominated
by inbound on doc-heavy turns. No wall-clock speed claim — only token reduction (the standing caveat).
