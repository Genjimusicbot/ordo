// ordo init — drop the ORDO skill into a project's .claude/ so `/ordo` works without pasting anything.
// Copies the bundled skill (skills/ordo/SKILL.md) + the operating profile + the spec/ gate references into
// <target>/.claude/skills/ordo/. Lossless and additive: it changes no behavior, it removes the paste step.
import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

/** Install the ORDO skill into <targetDir or cwd>/.claude/skills/ordo/. Returns a status string. */
export function initProject(targetDir) {
  const target = targetDir || process.cwd();
  const skillDir = join(target, ".claude", "skills", "ordo");
  const refDir = join(skillDir, "references");
  mkdirSync(refDir, { recursive: true });
  writeFileSync(join(skillDir, "SKILL.md"), readFileSync(join(ROOT, "skills", "ordo", "SKILL.md"), "utf8"));
  // 3-tier progressive disclosure: SKILL.md is the on-match body; the profile + gate specs are on-demand refs.
  writeFileSync(join(refDir, "OPERATING-PROFILE.md"), readFileSync(join(ROOT, "OPERATING-PROFILE.md"), "utf8"));
  let n = 0;
  const specDir = join(ROOT, "spec");
  if (existsSync(specDir)) for (const f of readdirSync(specDir)) {
    if (f.endsWith(".md")) { writeFileSync(join(refDir, f), readFileSync(join(specDir, f), "utf8")); n++; }
  }
  return `ORDO installed → ${skillDir}\n  SKILL.md + OPERATING-PROFILE.md + ${n} spec references.\n` +
    "  Claude Code loads /ordo on coding/agentic tasks. Restart the session to pick it up.";
}
