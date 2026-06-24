# ORDO disclaimers (read before believing any number)

ORDO is experimental research, not a production system or a guaranteed efficiency win. The honest
boundaries:

1. **Not a magic multiplier.** ORDO does not deliver 20x/26x/99x. Those figures in the literature are
   either lossy one-way deletion (LLMLingua ~20x) or weight-locked to a fine-tuned model (gist tokens
   26x), and neither is a reusable lossless language on a frozen API model. ORDO's realistic, *to-be-
   measured* target is a net reduction on the *operational/command* slice of a workload (the verbose
   directives), from grammar + terseness + caching + avoided rework, not from glyph magic.

2. **Tokenizer caveat.** Symbol costs in `spec/lexicon.md` are measured with OpenAI's `tiktoken`
   (`cl100k_base`, `o200k_base`) as PROXIES. Claude's and Gemini's tokenizers are proprietary and can
   differ. A symbol that is 1 token for GPT may be 2-3 for Claude. Always re-validate on your target
   model before trusting a savings number.

3. **Token count is not cost or latency.** A denser token can cost MORE compute to process. Reduction
   in token *count* does not translate 1:1 to cost or wall-clock savings. This is genuinely
   unmeasured and is the largest open risk in the whole idea.

4. **Lossless-to-intent is the goal, not a guarantee.** The round-trip gate (`tools/`) enforces that a
   model reconstructs the original intent from ORDO, but any compression risks meaning loss on edge
   cases. Verify on your own tasks; keep critical reasoning in higher-fidelity form.

5. **The spec must be present.** A model can only read ORDO with the spec/skillstone in context (or
   after fine-tuning). Without it, ORDO is unreadable. The spec costs context; the win is real only
   when amortized over many calls (prompt caching helps).

6. **Private-use, consensual-efficiency only. SAFETY.** A dense private notation is, by nature, also a
   covert-channel primitive (see GLOSSOPETRAE's tokenizer/semantic covert-channel findings). ORDO is
   for single-tenant, consensual, private token-efficiency. It is NOT for evading safety monitoring,
   hiding payloads from moderation, smuggling instructions, or any multi-tenant/monitored pipeline
   where covert signaling is a risk. ORDO deliberately **excludes** invisible-Unicode/steganographic
   mechanisms; it uses only visible, declared, validated symbols. Do not repurpose it to defeat
   oversight.

7. **Provenance.** ORDO builds on public research (GLOSSOPETRAE, LLMLingua, Lojban/CLL, VOKU, classic
   logographic + runic scripts) and cites it. It reuses no proprietary or leaked material.
