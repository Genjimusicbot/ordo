// ORDO runtime in 30 seconds. Run: node examples/basic.mjs
import { decode, emit, bestFormat, compressInbound, ponytailFlags, getOperatingProfile } from "../src/index.js";

// 1. Decode a terse ORDO command to its full English instruction
console.log("decode:", decode("σ文3列简心金业通¬序"));
console.log("decode:", decode("ν码×\"duplication\"据\"behavior\"加\"type hints\""));
console.log("decode (chain):", decode("β5名|★"));

// 2. Output contract: cheapest faithful format by data shape
const tabular = { users: [{ id: 1, name: "Alice", role: "admin" }, { id: 2, name: "Bob", role: "user" }] };
const nested = { cfg: { db: { pool: { min: 2, max: 10 } } } };
console.log("\nbestFormat(tabular):", bestFormat(tabular), "->\n" + emit(tabular));   // TSV
console.log("bestFormat(nested):", bestFormat(nested), "->", emit(nested));            // minified JSON

// 3. Lossless inbound compression (a JSON array -> TSV)
console.log("\ninbound:", compressInbound(JSON.stringify({ rows: [{ a: 1, b: 2 }, { a: 3, b: 4 }] })));

// 4. Ponytail: what filler the output contract forbids
console.log("\nponytail flags:", ponytailFlags("Great question! Here's the answer. I hope this helps!"));

// 5. The methodology: get the operating profile to paste into your LLM's system prompt
console.log("\noperating profile is", getOperatingProfile().length, "chars — paste it into a system prompt.");
