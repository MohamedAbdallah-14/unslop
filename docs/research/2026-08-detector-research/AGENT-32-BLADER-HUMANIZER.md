# Agent #32 — blader/humanizer Claude Skill & Practitioner Humanizer Ecosystem

**Topic:** `blader/humanizer` agent skill, community adoption, philosophy vs unslop, critiques, SKILL.md integration lessons  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop SKILL.md refresh

---

## Executive summary

`blader/humanizer` is the dominant open-source **prompt-only** humanizer in the agent-skills ecosystem: one ~450-line `SKILL.md`, 35 enumerated patterns sourced from Wikipedia's WikiProject AI Cleanup, optional voice calibration, and a two-question self-audit before final output. As of August 2026 it carries **36,385 GitHub stars**, **3,238 forks**, and **~4.4K installs** via the cross-agent `skills.sh` CLI — extraordinary velocity for a repo created **2026-01-18** (~7 months).

It is **not** a detector-bypass tool. Maintainer `@blader` closed GPTZero-related issues explicitly: Humanizer optimizes for human readers, not classifier scores. Independent tests (HumanizerAI 2026, GitHub #2) confirm processed text can score *worse* on GPTZero than the input — expected when the goal is editorial cleanup, not statistical fingerprint evasion.

**vs unslop:** Both share the Wikipedia taxonomy and the two-pass audit prompt pair. unslop goes further: always-on session hooks, five intensity modes, research-backed principles (warmth–reliability tradeoff, role-play frame), deterministic regex pipeline with byte-exact preservation, optional detector feedback loop, and explicit anti-detector mode framed as ESL false-positive defense — not marketing bypass.

**Highest-value integration lessons for unslop `SKILL.md`:**

1. **Adopt Humanizer v2.9+ patterns #34–35** (fake objection answers, rejected fake alternatives) — unslop's regex layer partially covers these via authority tropes but the skill prose doesn't name them.
2. **Port the false-positive guard block** — Humanizer's "What not to flag" section prevents over-correction on deliberate em dashes, letter salutations, and quoted secondhand text; unslop has preservation rules in Python but not equivalent LLM-mode guidance.
3. **Add three output modes** (pasted / file / embedded) — reduces token waste when humanizing PR bodies or commit messages inside another task.
4. **Strengthen no-fabrication audit** — Humanizer v2.9.0 added explicit claim-preservation checks after #187 showed example rewrites inventing dates and places; unslop already has `[VERIFY: ...]` but could mirror Humanizer's dual audit questions verbatim in LLM mode.
5. **Do not copy Humanizer's hard em-dash ban** — unslop correctly caps at two per paragraph; Humanizer §14 removes all dashes unless a voice sample overrides — a known false-positive source (Neodrop, dev.to reviews).
6. **Credit line stays** — unslop already acknowledges blader in README and `RESEARCH_AND_TECH.md`; keep synchronized as Humanizer grows past 35 patterns.

---

## Primary sources (URLs)

| Resource | URL |
|----------|-----|
| **Repository** | https://github.com/blader/humanizer |
| **SKILL.md (runtime artifact)** | https://github.com/blader/humanizer/blob/main/SKILL.md |
| **README (install, pattern table)** | https://github.com/blader/humanizer/blob/main/README.md |
| **Latest release (v2.11.1)** | https://github.com/blader/humanizer/releases/tag/v2.11.1 |
| **Claude Desktop zip package** | https://github.com/blader/humanizer/releases/latest/download/humanizer-skill.zip |
| **skills.sh registry** | https://skills.sh/blader/humanizer |
| **Wikipedia: Signs of AI writing** | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing |
| **WikiProject AI Cleanup** | https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup |
| **Antigravity complete guide (Mar 2026)** | https://antigravity.codes/blog/humanizer-claude-code-skill-guide |
| **DeepWiki architecture** | https://deepwiki.com/blader/humanizer |
| **DEV Community walkthrough** | https://dev.to/vasughanta09/this-claude-skill-fixed-my-ai-writing-3pko |
| **Neodrop honest limitations** | https://neodrop.ai/post/YZo3A0JTCP0 |
| **HumanizerAI GPTZero bypass test** | https://humanizerai.com/blog/gptzero-bypass-test-2026 |
| **GitHub issue #2 (GPTZero regression)** | https://github.com/blader/humanizer/issues/2 |
| **GitHub issue #82 (prompt limits)** | https://github.com/blader/humanizer/issues/82 |
| **GitHub issue #187 (fabrication)** | https://github.com/blader/humanizer/issues/187 |
| **DAMAGE commercial audit (COLING 2025)** | https://arxiv.org/abs/2501.03437 |
| **Adversarial Paraphrasing (NeurIPS 2025)** | https://arxiv.org/abs/2506.07001 |
| **unslop inspirations (README)** | https://github.com/MohamedAbdallah-14/unslop#inspirations |
| **unslop RESEARCH_AND_TECH acknowledgments** | https://github.com/MohamedAbdallah-14/unslop/blob/main/docs/RESEARCH_AND_TECH.md#acknowledgments |

### Practitioner ecosystem (related repos)

| Project | URL | Relation to blader/humanizer |
|---------|-----|------------------------------|
| **brandonwise/humanizer** | https://github.com/brandonwise/humanizer | OpenClaw skill + CLI; 30 patterns, 500+ vocab terms, burstiness/TTR stats; cites blader as upstream |
| **itsjwill/humanizer-x** | https://github.com/itsjwill/humanizer-x | Claude Code skill; 4-pass, severity-ranked patterns, SSML voice disfluency; positions as paid-humanizer replacement |
| **Aboudjem/humanizer-skill** | https://github.com/Aboudjem/humanizer-skill | Agent skill; perplexity/burstiness focus |
| **lxgicstudios/humanize-cli** | https://github.com/lxgicstudios/humanize-cli | npm CLI with score/analyze/transform/watch |
| **rudra496/StealthHumanizer** | https://github.com/rudra496/StealthHumanizer | BYOK web app; 12-metric embedded detector loop |
| **chengez/Adversarial-Paraphrasing** | https://github.com/chengez/Adversarial-Paraphrasing | NeurIPS 2025; detector-guided paraphrase (academic ceiling) |
| **Former OpenClaw registry mirror** | `openclaw/skills/skills/brandonwise/ai-humanizer` *(repository unavailable as of 2026-08-21)* | Historical registry mirror of brandonwise/humanizer |

Full OSS landscape inventory: `docs/research/18-commercial-humanizer-tools/C-opensource.md` (~30 repos).

---

## What blader/humanizer is

### Architecture

```
User invokes /humanizer or "humanize this"
  → Agent loads ~/.claude/skills/humanizer/SKILL.md (or plugin path)
  → Optional: Voice Calibration from 2–3 user paragraphs
  → Phase 1: Pattern scan (35 rules, 5 buckets)
  → Phase 2: Draft rewrite (preserve claims, add personality when fit)
  → Phase 3: Self-audit
        Q1: "What still sounds AI-generated?"
        Q2: "Did the rewrite add or remove any fact, name, number, date, quote, citation?"
  → Phase 4: Final rewrite
  → Output per mode (pasted / file / embedded)
```

**No binaries. No models. No API.** The hosting agent (Claude Code, OpenCode, Cursor, Codex, etc.) executes the instructions using its own tools. Distribution paths:

- `npx skills add blader/humanizer --global` (cross-agent CLI)
- Claude Code plugin: `/plugin marketplace add blader/humanizer` → `/humanizer:humanizer`
- Claude Desktop: release zip with flat `humanizer/SKILL.md` (no symlinks — #224)
- Manual git clone into any harness skill directory

### Pattern taxonomy (v2.11.1 — 35 patterns)

| Bucket | # | Examples |
|--------|---|----------|
| **Content** | 1–6 | Significance inflation, media name-dropping, shallow -ing analysis, sales language, vague sources, formulaic challenges/outlook |
| **Language & grammar** | 7–13 | AI vocab (`delve`, `tapestry`, `landscape`, figurative `gate`), copula avoidance (`serves as`), not-X-but-Y, rule of three, synonym cycling, false ranges, passive voice |
| **Style** | 14–19, 26–35 | Em/en dash removal (hard ban unless voice sample), bold spam, emoji headings, title case, hyphenated buzzword pairs, fake deeper truths, signposting, repeated headings, retrospective doc voice, forced punchlines, formulaic sayings, fake-candid openings, **#34 objection no one raised**, **#35 rejected fake alternatives** |
| **Chatbot artifacts** | 20–22 | "I hope this helps", knowledge-limit disclaimers, sycophancy openers |
| **Filler & hedging** | 23–25 | "In order to", qualifier stacks, generic positive endings |

Each pattern ships with **before/after examples** — the pedagogical layer that drove star velocity. Users can fork and add custom patterns in minutes (DEV Community author added "It's worth noting that" in five minutes).

### Voice calibration

When the user supplies 2–3 paragraphs of their own writing, Humanizer:

1. Extracts rhythm, word choice, paragraph openings, punctuation tics
2. **Overrides global style rules** — em-dash ban (§14) suspended if the sample uses dashes
3. Matches deliberate quirks instead of regressing to a generic "clean human baseline"

This directly addresses the **sterile-output critique**: without a sample, Humanizer converges on Wikipedia-editor neutral prose — voiceless but pattern-clean.

### Version evolution (selected)

| Version | Date (approx) | Change |
|---------|---------------|--------|
| 1.0.0 | Jan 2026 | Initial release |
| 2.0.0 | — | Full rewrite from Wikipedia source |
| 2.2.0 | — | Two-pass "obviously AI generated" audit |
| 2.4.0 | — | Voice calibration |
| 2.9.0 | Jul 2026 | **No-fabrication rule** (#187); three output modes; writing sample overrides §14 |
| 2.10.0 | — | Patterns #34–35 (drafting artifacts left in final text) |
| 2.11.0 | Aug 2026 | Plain Language rewrite of all instructions |
| 2.11.1 | 2026-08-18 | Claude Desktop release zip; plugin symlink fix (#224) |

---

## Community adoption

### Quantitative signals (2026-08-19)

| Metric | Value | Source |
|--------|-------|--------|
| GitHub stars | **36,385** | `gh api repos/blader/humanizer` |
| Forks | 3,238 | GitHub API |
| Open issues | 6 | GitHub API |
| Created | 2026-01-18 | GitHub API |
| skills.sh installs | ~4.4K | https://skills.sh/blader/humanizer |
| Latest release | v2.11.1 (2026-08-18) | GitHub releases |

Star trajectory is the story: ~16.8k by March 2026 (Antigravity guide) → 36k+ by August — faster than almost any other single-file agent skill. Antigravity compares it to `obra/superpowers` as the closest analog in the Claude Code ecosystem.

### Qualitative adoption

- **Claude Desktop GUI path** — non-developers install via Skills upload + release zip (DEV Community tutorial, Jan 2026)
- **Cross-harness** — documented for Claude Code, OpenCode, Codex, Cursor via `npx skills`
- **Third-party guides** — Antigravity, DeepWiki, Neodrop, Claudeers registry, SkillsLLM catalog
- **Fork culture** — users add personal pattern lists; brandonwise/humanizer builds deterministic CLI on top
- **Commercial humanizer vendors** — Rephrasy opened #82 promoting fine-tuned API bypass; closed by maintainer as off-topic

### What adoption is *not*

- Not PyPI/npm library usage (no package beyond skills CLI wrapper)
- Not enterprise procurement — no SLA, no support contract
- Not detector-bypass community — GPTZero seekers get redirected to editorial framing

---

## Critiques and maintainer responses

### 1. GPTZero scores worsen after humanization

**Report:** #2 — human text went from 50% human to 98% AI; "Possible AI paraphrasing" flag.  
**Maintainer (@blader, Jul 2026):** Closed. "Humanizer is designed to improve prose for human readers, not to bypass GPTZero… detector scores are not a supported success criterion."  
**Independent:** HumanizerAI 2026 test — vocabulary-blocklist skills scored ~23% GPTZero bypass vs ~67% for burstiness-targeting rewrite; structural variation beats lexical bans.

**unslop implication:** Aligns with unslop's published TMR movement (0.0–0.2 pp deterministic) and anti-detector mode's explicit cross-model second-pass recommendation.

### 2. Sterile output without voice calibration

**Sources:** Neodrop review, dev.to (Dann Waniéri quoted): passes every pattern check, sounds nothing like the author's published work.  
**Root cause:** Generic human baseline ≠ personal voice. Humanizer acknowledges: "Sterile, voiceless writing is just as obvious as slop."

**unslop implication:** unslop's voice-match procedure (6 signals) and numeric-only style memory are the architectural answer. EMNLP 2025 "Catch Me If You Can?" limits should stay cited — neither tool does production stylometric cloning.

### 3. Hard em-dash ban false positives

**Report:** Users who deliberately use em dashes lose them regardless of context (unless voice sample provided).  
**Humanizer rule:** §14 removes all em/en dashes in final output.  
**unslop rule:** Cap at two per paragraph — preserves intentional dash users.

### 4. Fabricated specifics in examples and early rewrites (#187)

**Report:** Pattern examples and Lisbon demo added dates, neighborhoods, survey citations not in source.  
**Fix:** v2.9.0 explicit no-fabrication rule + dual audit question on claim preservation.  
**Residual risk:** LLM-mode humanizers always risk fluent wrongness — unslop's `[VERIFY: ...]` and warmth–reliability principle address the same failure mode.

### 5. Information loss from shape rules (#212, related)

Rule-of-three and hedging removals can delete ranking or simultaneity claims when treated as "padding." Humanizer v2.10+ tightened: remove unsupported defense, keep real claims; rewrite paragraph around main point instead of phrase patching.

### 6. English-only / domain misfires

Neodrop: pattern catalog is English-specific. Technical docs lose useful structure (numbered lists, cautious hedging) when run through content-pattern rules.

**unslop implication:** Auto-Clarity suspension for legal/medical/security text partially covers this; consider explicit **"do not humanize API docs / RFC prose"** carve-out mirroring Humanizer's "reference, technical, legal, and factual text neutral."

### 7. Prompt-based ceiling (#82)

Rephrasy argued fine-tuned humanization models beat prompts on perplexity/burstiness. @blader closed as commercial promotion. Greg-randall counter: "output *reads* less like AI to a human audience" — the editorial vs adversarial framing split.

**Research alignment:** Adversarial Paraphrasing (NeurIPS 2025), DAMAGE audit, Chicago Booth 2026 — surface humanizers underperform detector-trained rewriters; both Humanizer and unslop accept this for different reasons.

---

## Philosophy comparison: blader/humanizer vs unslop

| Dimension | blader/humanizer | unslop |
|-----------|------------------|--------|
| **Primary goal** | Editorial cleanup for human readers | Same + always-on assistant voice + optional detector defense |
| **Runtime** | On-demand skill invocation | Session hooks + slash commands + file CLI |
| **Execution** | LLM interprets SKILL.md only | Deterministic regex (`humanize.py`) + optional LLM + detector loop |
| **Pattern count** | 35 named rules in one file | Overlapping vocab/hedging lists + structural/stylometry phases |
| **Intensity** | Implicit (personality when fits) | 5 modes: subtle → anti-detector |
| **Voice** | Optional writing-sample calibration | voice-match mode + numeric style memory (no free-text prefs) |
| **Audit** | Two questions, two passes | Same prompt pair in LLM mode (ported from blader) |
| **Preservation** | Prose-only in file mode; "keep code/YAML" instruction | Contract-tested byte preservation (`TestPreservation` suite) |
| **Detector stance** | Explicitly not a bypass tool | Anti-detector mode with ESL false-positive framing + regulatory boundaries |
| **Research grounding** | Wikipedia taxonomy only | 38+ citations; principles cite Ibrahim, SycEval, DivEye, TempParaphraser |
| **Warmth** | "Add personality when it fits" | **Subtract, don't add** — warmth = sycophancy risk |
| **Em dashes** | Hard remove (unless sample) | Cap 2/paragraph |
| **Distribution** | Single-repo skill | Multi-platform plugin + PyPI + mirrors |

### Shared DNA

Both trace patterns to **Wikipedia: Signs of AI writing**. unslop's `humanize.py` comments cite `blader/humanizer taxonomy (MIT)` alongside Wikipedia. The two-pass audit (`"What makes this obviously AI generated?"` → revise) is documented in `docs/RESEARCH_AND_TECH.md` as ported from blader.

### Deliberate unslop divergences (keep)

1. **Always-on persistence** — Humanizer is episodic; unslop fights mid-session drift via hooks.
2. **Deterministic first** — Reproducible, testable, no API cost for file rewrites.
3. **Anti-warmth principle** — Humanizer's "add soul" can reintroduce sycophancy unless constrained; unslop bans warmth-as-filler explicitly.
4. **No detector score promises** — Both agree; unslop adds measured bench numbers.
5. **Regulatory/watermark boundaries** — Humanizer silent; unslop documents EU AI Act Art. 50 side effects.

---

## Practitioner humanizer tools ecosystem (2024–2026)

Three tiers repeat across ~30 OSS repos (see Category 18 research):

```
Tier 1 — Lexical:     vocab bans, em-dash strip, contraction inject
Tier 2 — Statistical: burstiness σ, TTR, perplexity variance targets
Tier 3 — Adversarial: detector-in-the-loop paraphrase (StealthHumanizer, Adversarial-Paraphrasing)
```

**blader/humanizer sits at Tier 1+, prompt-executed Tier 2 opportunistically** (agent may vary sentence length but has no numeric σ target). **unslop anti-detector mode** documents Tier 2 explicitly (σ ≥ 6, contraction rate ~0.17) and recommends Tier 3's cross-model pass.

### Agent-skill cluster (direct peers)

| Tool | Stack | Differentiator |
|------|-------|----------------|
| blader/humanizer | SKILL.md | Wikipedia 35-pattern catalog; largest community |
| brandonwise/humanizer | JS CLI + SKILL | Transparent scoring, 128 tests, burstiness metrics |
| humanizer-x | SKILL.md | 4-pass severity ranks, voice SSML |
| Aboudjem/humanizer-skill | SKILL.md | Burstiness/perplexity wording |

### Commercial adjacency

- **DAMAGE (COLING 2025):** 19 commercial humanizers audited; self-reported vs independent gaps 20–100 points.
- **Turnitin Aug 2025:** Explicit anti-humanizer training; pre-2025 bypass stats stale (unslop SKILL.md already notes this).
- **HumanizerAI blog:** Vocab blocklists *hurt* GPTZero bypass vs burstiness-only rewrite — caution for importing more word bans into unslop regex.

---

## Integration lessons for unslop `SKILL.md`

Prioritized by impact vs diff size. File: `skills/unslop/SKILL.md` (SSOT).

### P0 — Adopt now

| # | Lesson | Humanizer source | unslop action |
|---|--------|------------------|---------------|
| 1 | **False-positive guard** | SKILL.md § "What not to flag" + "Human details to keep" | Add compact `## False positives` section: don't flag polish alone, one transition word, curly quotes from CMS, quoted secondhand phrases, deliberate repetition |
| 2 | **Dual claim audit** | Rewrite process Q2 (v2.9+) | Align LLM-mode wording with Humanizer's exact fact-preservation question; already partially present — unify |
| 3 | **Patterns #34–35** | Drafting artifacts in final text | Add to Rules drop-list: "Answering objections no one raised", "Rejecting fake alternatives" — mirrors authority tropes in `humanize.py` but names them for LLM mode |
| 4 | **Output modes** | pasted / file / embedded | Add `## Output modes` for file-only write + embedded-in-PR behavior |

### P1 — Consider next release

| # | Lesson | Action |
|---|--------|--------|
| 5 | **Voice sample overrides dash rule** | voice-match procedure: "Sample em-dash rate overrides default cap" |
| 6 | **Technical prose carve-out** | Extend Auto-Clarity: API docs, RFCs, changelogs — pattern rules misfire |
| 7 | **Plain Language instruction style** | v2.11.0 rewrote Humanizer in plain language; unslop rules are already terse — optional pass for non-maintainer readability |
| 8 | **Claude Desktop zip parity** | unslop ships plugin bundles; document flat SKILL path for Desktop upload if users ask |

### P2 — Do not import

| # | Humanizer feature | Why skip |
|---|-------------------|----------|
| 1 | Hard em-dash zero tolerance | Conflicts with unslop cap; causes voice false positives |
| 2 | "Add soul" without subtract-first framing | Risks sycophancy (Ibrahim 2025) |
| 3 | Detector score as success metric | Both projects reject this |
| 4 | 35-pattern prose duplication in SKILL.md | unslop uses categorized drop rules + deterministic engine; duplicating full before/after table bloats hook context |

### Suggested SKILL.md patch sketch (P0 #1)

```markdown
## False positives

Do not treat these as AI tells by themselves:

- Professional polish or consistent grammar
- One formal transition word (*however*, *additionally*)
- Curly quotes from macOS/Word/CMS defaults
- Em dashes when the rate matches the writer's sample or ≤2 per paragraph
- Deliberate repeated openings for rhythm ("She came. She saw.")
- Quoted phrases, titles, or use/mention examples (e.g. explaining why "delve" is overused)
- Real scope limits, safety notices, and named objections with sources

Flag clusters: several stock patterns in the same passage matter more than any single hit.
```

### Cross-reference hygiene

- README inspirations table: update pattern count **29 → 35** when touching README next.
- `RESEARCH_AND_TECH.md` acknowledgments: note v2.9+ no-fabrication rule as parallel to unslop `[VERIFY: ...]`.
- Fix any lingering **`blader/unslop`** references in CHANGELOG — that repo does not exist (404); intended source is **`blader/humanizer`**.

---

## unslop verdict

**blader/humanizer is the category-defining editorial humanizer skill** — not because it beats detectors, but because it made the Wikipedia taxonomy legible, forkable, and installable in every agent harness in under seven months. unslop is a superset product: same cultural source, heavier engineering (tests, preservation, hooks, bench), and explicit refusal to sell bypass.

For SKILL.md maintenance, treat Humanizer as a **living upstream pattern catalog** to diff on each major release (currently v2.11.1). Port new numbered patterns into unslop's drop rules and regex where deterministic coverage helps; keep unslop's subtract-first principles, em-dash cap, and research citations as non-negotiable differentiators.

---

## Open questions for follow-up agents

1. **Agent #12 (DAMAGE):** Where do prompt-only skills like Humanizer sit vs the 19 commercial humanizers in TPR/FPR tables?
2. **Agent #33 (Antislop ICLR 2026):** Generation-time antislop vs Humanizer's post-hoc cleanup — complementary or competing install?
3. **Benchmark gap:** No public A/B of unslop deterministic vs Humanizer LLM-only on the same fixtures with blind human preference — unslop has 21/21 humanness bench; Humanizer has none.

---

*Agent #32 complete. Manifest row 32 → done.*
