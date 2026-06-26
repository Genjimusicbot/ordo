# ORDO MCP bundle — the missing tools, compacted (Full tier only)

ORDO does NOT build video/PDF/crawler servers. The Full tier **bundles existing MCP tools** and adds the one thing
that makes them cheap: **every tool's output is routed through the lossless inbound compactor before it enters
context.** A transcript or a crawl arrives already shrunk. *That compaction is the differentiator, not the tools.*

## Measured value-add (raw vs ORDO-compacted, o200k, lossless — `tools/mcp_compact_ab.py`)
| bundled-tool output | reduction |
|---|---|
| web / social crawl (result JSON) | **−62%** |
| video transcript (segment JSON) | **−46%** |
| PDF text dump (prose) | **−24%** (whitespace; deep dedup is the opt-in headroom path) |

## The anchor tools (the Full install ships `.ordo/mcp.json.example`)
- **Web crawler** — `firecrawl-mcp` (real; needs `FIRECRAWL_API_KEY`) crawls the open web. Results →
  `compressInbound` (JSON→TSV, dedup) before context.
- **Social media** — `@apify/actors-mcp-server` (real; needs `APIFY_TOKEN`) scrapes the largest socials (X /
  Instagram / TikTok / LinkedIn / etc. via Apify actors). Results → compacted before context.
- **PDF / images** — **native to Claude Code** (the Read tool reads PDFs + images). ORDO adds: route the extracted
  text through the inbound compactor; for a huge PDF keep the load-bearing pages, reference the rest.
- **Video / mp4 (vision)** — ORDO does video the **REAL way, no fake MCP**: `tools/video_frames.py` extracts
  keyframes with ffmpeg, the agent **Reads them as images** (Claude Code's native image vision), and ORDO
  ponytail-compacts the per-frame notes (−46% measured on segment output). That is ORDO teaching the model to *see*
  a video — frames + native vision, no extra service.

## The ORDO rule (the universal value-add)
On ANY tool result — bundled or not — apply the inbound contract: structured → TSV, prose/logs → lossless whitespace
+ dedup, send the *delta* not the whole blob, and the **measured-revert gate** (never inflate). This is why the Full
tier costs fewer tokens than wiring the same MCPs up raw.

## Add-pattern (scoped honestly)
"Bundle every MCP / implement every skill" is unbounded. ORDO ships the **3 anchors + this rule**; to add a server,
put it in `.ordo/mcp.json.example`, point ORDO's compaction at its output, and A/B the raw-vs-compacted delta
(`tools/mcp_compact_ab.py` is the template). Capability grows per measured addition, never in a sweep.
