#!/usr/bin/env node
import { decode, emit, ponytailFlags, compressInbound, getOperatingProfile, getSkillstone } from "../src/index.js";

const [cmd, ...args] = process.argv.slice(2);
const arg = args.join(" ");

switch (cmd) {
  case "decode": console.log(decode(arg)); break;
  case "inbound": console.log(compressInbound(arg)); break;
  case "ponytail": console.log(JSON.stringify(ponytailFlags(arg))); break;
  case "emit": { try { console.log(emit(JSON.parse(arg))); } catch { console.error("emit needs a JSON arg"); process.exit(1); } break; }
  case "profile": case "spec": console.log(getOperatingProfile()); break;
  case "skillstone": console.log(getSkillstone()); break;
  default:
    console.log(`ORDO — context-engineering framework for LLMs

  ordo decode "σ文3列简"     decode an ORDO-G command to its full English instruction
  ordo inbound <text>        lossless inbound compression (JSON->TSV / whitespace)
  ordo emit '<json>'         re-serialize data in the cheapest faithful format (TSV/minified JSON)
  ordo ponytail <text>       list the filler phrases the output contract forbids
  ordo profile               print the operating profile (paste into your LLM's system prompt)
  ordo skillstone            print the language skillstone (teach an LLM ORDO-G)

The gates (REFEED / experimentalist / evaluation / autonomy / context-rot) are prompt SOPs in spec/*.md,
loaded as text via getSpec(name) — they are methodology you give your LLM, not code that runs here.`);
}
