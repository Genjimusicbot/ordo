# 🟢 ordo.md — the paste-in tier (system prompt)

The zero-install option: paste the discipline into your system prompt / `CLAUDE.md` and it's active.

## Install
Paste [`OPERATING-PROFILE.md`](../../OPERATING-PROFILE.md) (the full spine, ~1.4k tokens) — or
[`CONTEXT-SAVER.md`](../../CONTEXT-SAVER.md) (lean prose, ~1k tokens) — into your system prompt, `CLAUDE.md`,
`.cursorrules`, or project rules. Or pipe it: `npx ordo profile`.

## What you get
- The full discipline **as prose**: the classify→route dispatcher, the compression contract (format-by-shape +
  ponytail + inbound), and the gates — all as instructions the model follows.
- Works on **any** LLM surface (Claude, ChatGPT, Cursor, your own code) — it's just text in the context.

## What you DON'T get
- No runtime (`classifyTask`/`compressInbound` as code), no bundled MCP tools, no `.ordo/` persistence. It's the
  methodology, not the install.

## Proven
- Compression **−47–68%** on a structured turn (measured, GPT-proxy; re-validate on your model). The gates are
  honest/opt-in — on a frontier model they mostly wash (named in the scorecard).

## For
"I just want it in my prompt, on whatever model I'm using." Start here if you don't run Claude Code.
