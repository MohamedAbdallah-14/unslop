<div align="center">

# unslop

**Make AI output sound like a human wrote it.**

[![Tests](https://github.com/MohamedAbdallah-14/unslop/actions/workflows/ci.yml/badge.svg)](https://github.com/MohamedAbdallah-14/unslop/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/MohamedAbdallah-14/unslop/branch/main/graph/badge.svg)](https://codecov.io/gh/MohamedAbdallah-14/unslop)
[![PyPI](https://img.shields.io/pypi/v/unslop.svg)](https://pypi.org/project/unslop/)
[![Python](https://img.shields.io/pypi/pyversions/unslop.svg)](https://pypi.org/project/unslop/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

A plugin for Claude Code, Cursor, Windsurf, Gemini CLI, OpenAI Codex, and Copilot.
Strips AI-isms (sycophancy, stock vocab, hedging stacks, em-dash pileups), engineers
burstiness, restores voice. Preserves code blocks, URLs, and technical terms.

**New here?** Start with [**GETTING_STARTED.md**](./GETTING_STARTED.md) — a plain-English on-ramp for non-technical users. This README is the developer reference.

</div>

---

## What This Does

You ask the model a question. The default reply opens with "Great question!", uses "delve" twice, stacks three "however"s, and lays out four paragraphs of identical length. That's the AI fingerprint. Every reader spots it. Every detector flags it.

`unslop` makes the model write like a careful human at the end of a real day. Direct on the substance. Specific where it matters. Quiet where nothing needs saying.

### Before

> Great question! When optimizing React performance, it's important to note that there are several factors to consider. Firstly, you should leverage the `useMemo` hook to memoize expensive computations. Additionally, it's worth mentioning that `React.memo` can prevent unnecessary re-renders. However, it's also paramount to consider whether these optimizations are truly necessary, as premature optimization can lead to unnecessary complexity. Generally speaking, profile first, then optimize.

### After

> Profile first. The bottleneck is almost never where you'd guess, and `useMemo` everywhere just adds clutter to a component that re-rendered for a different reason. Once you've found a real hotspot: `React.memo` on the child if its props are stable, `useMemo` on the value if recomputing it is the cost.

Same correctness. Different voice.

### Measured result

Blind LLM-as-judge preference test: Claude Sonnet 4.5 compares each unslop rewrite against the original, without knowing which is which. Seven fixtures, randomized A/B sides, single-run.

| Metric | Baseline | unslop (balanced) |
|---|---|---|
| Blind humanness preference (win rate) | — | **100% (7/7)** |
| AI-ism reduction (rule-counted) | 0% | **89.1%** |
| Flat-paragraph count across suite | 14 | 13 |
| Preservation of code / URLs / headings | — | byte-identical |

Reproduce with `python3 evals/perceived_humanness.py` (requires `ANTHROPIC_API_KEY`). Archived at `benchmarks/results/humanness/first-pass-20260421.json`.

---

## Install

### Claude Code (recommended — two commands, no clone)

In any Claude Code session:

```
/plugin marketplace add MohamedAbdallah-14/unslop
/plugin install unslop
```

The plugin system fetches the manifest from this repo, wires the `SessionStart` and `UserPromptSubmit` hooks, and registers the statusline. Restart Claude Code, then type `/unslop` to activate. Uninstall via `/plugin uninstall unslop`.

### Claude Code (standalone — no plugin system)

For users who want the hooks installed manually (e.g. before a plugin restart, or on a fork):

```bash
git clone https://github.com/MohamedAbdallah-14/unslop.git
cd unslop
bash hooks/install.sh
```

Windows (PowerShell):

```powershell
pwsh hooks/install.ps1
```

What that does:

- Copies hook scripts to `~/.claude/hooks/` (flat, not a subdirectory)
- Registers `SessionStart` (loads the activation rule) and `UserPromptSubmit` (tracks `/unslop <mode>` and `stop unslop`) in `~/.claude/settings.json`, merged safely via Node (never clobbers existing hooks)
- Wires the statusline so `[unslop:FULL]` (uppercase mode suffix) shows when active

Idempotent. Re-run anytime to upgrade. The bash installer re-verifies `settings.json` state on each run; the PowerShell installer checks file presence only, so pass `-Force` on Windows if `settings.json` was hand-edited.

### Cursor / Windsurf / Cline

Bundled rule files at `.cursor/rules/unslop.mdc`, `.windsurf/rules/unslop.md`, `.clinerules/unslop.md`. Open the project in any of them and the rule loads automatically.

### Gemini CLI

```bash
gemini extension install ./
```

Reads `gemini-extension.json` and loads `GEMINI.md` + the unslop skill into context.

### OpenAI Codex

The `plugins/unslop/.codex-plugin/plugin.json` bundle is auto-discovered by the Codex IDE extension.

### Standalone CLI (no IDE needed)

```bash
cd unslop
python3 -m scripts --deterministic /path/to/your/CLAUDE.md
```

Two modes: `--deterministic` (regex, no API) or default LLM mode (calls Claude). See [`unslop/README.md`](./unslop/README.md).

---

## Use

### Toggle modes mid-conversation

| Phrase | Effect |
|--------|--------|
| `/unslop` | Turn on (balanced) |
| `/unslop subtle` | Light touch |
| `/unslop balanced` | Default |
| `/unslop full` | Strong rewrite |
| `/unslop voice-match` | Mimic a provided sample |
| `/unslop anti-detector` | Adversarial paraphrase |
| `stop unslop` | Off |
| `normal mode` | Off |

Mode persists for the whole session.

### Sub-skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| `unslop` | `/unslop` | Active humanization for live responses |
| `unslop-commit` | `/unslop-commit`, `/commit` | Conventional Commits in human voice |
| `unslop-review` | `/unslop-review`, `/review` | Direct, kind PR review comments |
| `humanize` (`unslop`) | `/unslop-file <file>` | Rewrite a markdown file (preserves code, URLs, headings) |
| `unslop-reasoning` | `/unslop-reasoning` | Strip AI slop from chain-of-thought (over-hedging, over-decomposing, loops) |
| `unslop-help` | `/unslop-help` | Reference card |

### Voice-match (persist your style)

LLM mode accepts a voice sample and matches its measured profile (sentence length, contraction rate, pronoun ratios, punctuation rates). The profile can be saved once and reused:

```bash
unslop --save-voice-profile samples/my-writing.md   # one-time
unslop --voice-memory --mode full document.md       # uses saved profile
unslop --clear-voice-profile                        # delete
```

Storage: `$UNSLOP_STYLE_MEMORY`, then `$XDG_CONFIG_HOME/unslop/style-memory.json`, then `~/.config/unslop/style-memory.json`. File is mode-0600; symlinks refused. Profile is numeric metrics only — no prose stored.

### Configure default mode

Env var:

```bash
export UNSLOP_DEFAULT_MODE=full
```

Or `~/.config/unslop/config.json`:

```json
{ "defaultMode": "full" }
```

Resolution: env var > config file > `balanced`.
Set to `"off"` to disable session-start activation entirely.

---

## What Stays Exact

The file-rewriter (`unslop`) placeholder-protects these in deterministic mode and fails the run if the validator detects they changed:

- Fenced code blocks (` ``` ... ``` `) — content and structure
- Indented code blocks (4-space)
- Inline code (`` `foo()` ``)
- URLs and markdown links
- Headings (whole line, text and level)
- YAML frontmatter at file start (`---\n...\n---`)
- Blockquotes (`>` lines and multi-line `>` blocks)
- Markdown tables (pipe tables)
- Quoted single-word examples — `"delve"` or `"tapestry"` stays put, because the word is being discussed, not used (use / mention distinction)

File paths, commands, technical terms, version numbers, and error messages stay exact **when they live inside code blocks / inline code / URLs**. Bare prose references to them are not separately protected; deterministic regexes only target prose patterns, so they usually pass through, but review the diff if your file mixes prose with identifiers.

LLM mode (default) receives the same preservation list as an explicit instruction. It cannot be byte-enforced the way deterministic mode is, so run the file through `python3 -m scripts --deterministic` afterwards if you need a hard guarantee.

---

## What It Drops

`det` = handled by deterministic regex mode. `llm` = requires LLM mode (semantic rewrite, not regex).

| Category | Examples | Mode |
|----------|----------|------|
| Sycophancy openers | "Great question!", "Certainly!", "I'd be happy to help" | det |
| Stock vocab | delve, tapestry, testament, navigate (figurative), embark, journey (figurative), realm, landscape, pivotal, paramount, seamless, holistic, leverage, robust (filler), comprehensive, cutting-edge, state-of-the-art | det |
| Hedging stacks | "It's important to note that", "It's worth mentioning", "Generally speaking", "In essence", "At its core" | det |
| Performative balance | A "however" appended to every claim | det |
| Transition tics | "Furthermore,", "Moreover,", "Additionally,", "In conclusion,", "To summarize," at start of a sentence | det |
| Em-dash pileups | More than two em-dashes per paragraph (bullet lists get a per-item budget) | det |
| Significance inflation | "marks a pivotal moment", "stands as a testament", "enduring legacy", "leaves an indelible mark", "deeply rooted", "contributing to the broader narrative" | det |
| Notability namedropping | "maintains an active social media presence", "a leading expert in", "renowned for his work", "widely cited in", "internationally recognized as" | det |
| Superficial `-ing` tails | ", highlighting the importance", ", emphasizing its role" — filler participle phrases | det (full) |
| Copula avoidance | ", being a reliable platform," → ", a reliable platform," | det |
| Long-sentence run-ons | Sentences ≥20 words in flat-shape paragraphs split at safe boundaries (`;`, `, but `, `, however, `, em-dash) | det (Phase 1) |
| Parallel bullet soup | 3+ bullets sharing first word merged into one sentence | det (Phase 1) |
| Missing contractions | "do not" → "don't", "it is" → "it's" where safe | det (Phase 5) |
| Filler phrases | "in order to" → "to", "due to the fact that" → "because" | det (full) |
| Negative parallelism | "No guesswork, no bloat, no surprises" tricolons | det (full) |
| False-range clichés | "from beginners to experts", "from humble beginnings to" | warning |
| Synonym cycling | utilize + leverage + employ in one paragraph | warning |
| Tricolon padding (general) | "X, Y, and Z" stacks where two would suffice | llm |
| Tidy 5-paragraph essay | Real prose has uneven paragraph length | llm |

**Mode gating.** `subtle` runs stock vocab only. `balanced` (default) runs everything tagged `det` plus Phase 1 structural and Phase 5 contractions. `full` adds filler phrases, negative parallelism, and superficial `-ing`. Use `--no-structural` or `--no-soul` to turn off the newer passes for highly formal content.

---

## When It Actually Matters

Don't humanize everything. The research in `docs/research/` (20 categories, 120+ angle files, and a full [research-to-implementation trace](./docs/research/IMPLEMENTATION_TRACE.md) mapping each finding to the specific line of code it motivates) is blunt about this: humanization trades precision for voice. For code, legal text, medical advice, security warnings, runbooks — you want robotic. Precision beats voice.

Humanize when a human reader is going to judge you on *how it sounds*:

- Resumes, cover letters, personal statements, bios
- College essays and applications
- LinkedIn posts, cold outreach, marketing copy
- Blog posts, newsletters, anything where the voice is the product

### The two real levers

After reading the full compendium, it all comes back to two moves. Everything else is decoration.

**Subtract, don't add.** AI tone isn't a thing you layer on top of pretraining. It's a residue from RLHF — the model was trained on preference data that rewards polite, hedged, tricolon-heavy prose. The fastest path to human-sounding text is removing those patterns, not sprinkling in "warmth". Adding warmth just adds sycophancy, and sycophancy is the loudest AI tell there is.

**Engineer burstiness.** Humans write sentences of wildly uneven length. Seven words. Then a twenty-three word sentence that develops one specific idea with a clause that earns its place. Then four. LLMs default to flat, uniform sentence length, and that's what detectors key on (Category 04). Vary it and half the "AI tell" disappears on its own.

### AI detectors — the honest version

The academic consensus across Categories 05, 15, 16, and 18: **the detection arms race is structurally unwinnable for detectors**. Adversarial Paraphrasing (NeurIPS 2025) drops every tested detector's TPR by ~87%. DIPPER did roughly the same thing in 2023. At the same time, detectors have a huge false-positive problem on non-native English writers (Liang et al. *Patterns* 2023: >50% of TOEFL essays flagged as AI). A flagged score means less than marketing pages suggest.

**What our own testing found.** We ran the TMR AI-text detector (99.28% AUROC on RAID, 125M-param RoBERTa) against the unslop pipeline on four AI-generated fixtures. Result: deterministic surface rewriting — lexical + structural + contractions, every combination — moves the detector score by **0.0 to 0.2 percentage points**. Scores stay pinned above p_ai = 0.98 regardless of what we strip. This matches Adversarial Paraphrasing NeurIPS 2025 predicting exactly this outcome: modern detectors fingerprint on the structural signal that synonym-swap rewriting cannot move.

So unslop is a polish tool, not a detector-defeat tool. The blind LLM-judge test shows it decisively wins the "reads more human" comparison (100% 7/7). It does not fool GPTZero. Two different jobs.

What actually lowers detector scores, ordered by strength:

1. **Paraphrase through a different model family.** If GPT wrote it, have Claude rewrite. Or Gemini. Different stylometric fingerprints. This is the single strongest lever and unslop cannot do it alone.
2. **Burstiness.** Span sentence lengths roughly 4 to 35 words inside a paragraph. Phase 1 structural does this when material exists.
3. **Specificity the model can't fake.** Real dates, real project names, real numbers, first-person anecdotes. Training data doesn't contain *your* specifics.
4. **Contractions and small fragments.** "don't", "won't", the occasional start with "And" or "But". Phase 5 soul does the contraction half.
5. **Break predictable structure.** If every bullet has the same shape (verb + metric + with + tool), vary half of them.
6. **One or two rough edges.** A slightly awkward phrasing, a parenthetical trail, a non-linear logical jump — all of these read human.

Commercial unslop SaaS (Undetectable.ai, StealthGPT, WriteHuman, HIX Bypass, the ~150 products Category 18 audits) mostly don't beat a second pass through a different model plus five minutes of manual editing. Independent audits (DAMAGE COLING 2025; Epaphras & Mtenzi 2026) show wide gaps between their "99.8% undetectable" claims and reality, and the gap shifts monthly.

### Live detector feedback loop

Measurement is available as an opt-in CLI flag. It does not claim to lower scores — it just tells you where you are:

```bash
python3 -m unslop.scripts.fetch_detectors   # one-time: ~500MB of weights
unslop --detector-feedback file.md          # humanize, score, escalate, report
```

First run downloads the TMR detector. Subsequent runs score offline. Escalation ladder: balanced → full → full + structural + soul. Reports the score at each step.

### Resume playbook

The canonical case. Walks through the full stack in order:

1. **Start with raw facts.** Before touching an LLM, jot the bullets as notes. What you did, what changed, what the number was. No prose yet.
2. **Use the LLM for structure, not voice.** Ask it which accomplishment matters most, what's missing, how to order bullets. Don't let it write the final language.
3. **Write the bullets yourself.** Fast. One pass. Short. Specific numbers. Real tool names. The roughness of your own first draft is the feature.
4. **Polish grammar only.** Tell the model: "fix typos and grammar, don't change word choice, don't smooth the voice, don't add adverbs." It will try to misbehave. Be strict.
5. **Vary bullet shapes.** Don't let every bullet read "Verb + metric + by using + tool". Some start with context, some with outcome, some with the action.
6. **Top summary in your real voice.** Not "Results-driven professional with a passion for". Something like: "Backend engineer. Ten years in payments. I like the unsexy systems work nobody volunteers for."
7. **Human-read, not detector-read.** If a friend says "yeah, that sounds like you", you're done. Detector scores are noisy and change weekly.
8. **Optional paranoia pass.** If the ATS is known to run detectors, paraphrase once through a different model family, then manually restore any bullet where the paraphrase killed a specific number or tool name. Never trust a paraphrase blind.

### The warmth-reliability warning

One finding from the research that almost every unslop tool ignores: training (or prompting) a model to sound warmer raises its error rate 8–13% and amplifies sycophancy (Ibrahim/Hafner/Rocher 2025, Category 07). Fluent wrongness is worse than stiff accuracy, especially on a resume where a wrong date or an inflated metric can end the interview.

After humanizing anything factual, re-verify every number, date, title, and tool name against the source. The unslop doesn't hallucinate facts, but the rewrite pass can smooth over a number you misremembered in the first place and make it sound confident.

### `/unslop anti-detector` mode

An LLM-mode procedure. Covers items 2, 4, 5 from the detector list in one pass: burstiness targeting, contraction lift, structural variance. Item 1 (different-model paraphrase) the skill cannot execute alone — it must be requested. Use this mode when the reader might pipe the text into GPTZero or Turnitin. Skip for code, legal, or anything where precision beats voice.

Our own testing: deterministic rewriting moves TMR scores by <0.5pp. Real detector resistance needs the different-model pass that only you can orchestrate. The skill's value in anti-detector mode is doing the local burstiness / contraction / specificity work correctly so the cross-model pass has less to fix.

---

## Architecture

```
.
├── skills/                   # SSOT for the five agent-facing skills
│   ├── unslop/             — main mode
│   ├── unslop-commit/      — commit messages
│   ├── unslop-review/      — PR comments
│   ├── unslop-help/        — reference card
│   └── humanize/              — mirror of unslop file rewriter
├── unslop/       # SSOT for the file-rewriter (Python + skill)
│   └── scripts/              — humanize, validate, structural (Ph1),
│                                soul (Ph5), detector (Ph3), stylometry (Ph4)
├── rules/                    # SSOT for the short always-on activation text
├── commands/                 # Claude Code slash commands (TOML)
├── hooks/                    # SessionStart + UserPromptSubmit + statusline + installers
├── .claude-plugin/           # Claude Code marketplace + plugin manifest
├── .cursor/                  # Cursor rules + skills (mirror)
├── .windsurf/                # Windsurf rules + skills (mirror)
├── .clinerules/              # Cline rules (mirror)
├── .agents/                  # Agents marketplace manifest
├── plugins/unslop/        # Codex plugin bundle
├── tests/                    # pytest unit tests
├── docs/research/            # optional research compendium (not part of the plugin bundle)
└── .github/workflows/        # CI + sync SSOT to mirrored locations
```

Source of Truth: `skills/unslop/SKILL.md`, `rules/unslop-activate.md`, `unslop/SKILL.md`. The `sync.yml` workflow propagates these to every mirrored location on push to main.

---

## Tests

```bash
# Unit + integration tests (humanize + hook install flow)
python3 -m pytest tests/ -v

# Repo integrity (manifests, mirrors, script syntax, fixture round-trips)
python3 tests/verify_repo.py

# Offline benchmark on an AI-slop corpus, with CI gates
python3 benchmarks/run.py --strict
```

Coverage:

- **`tests/unslop/`** — 333 tests covering file-type detection; every deterministic rule family (sycophancy, hedging, stock-vocab, performative, authority, signposting, significance inflation, notability namedropping, copula avoidance, superficial `-ing`, filler, negative parallelism); structural rewriter (Phase 1); soul contractions (Phase 5); detector feedback loop (Phase 3); stylometry (Phase 4); humanness harness (Phase 6); preservation (code, URLs, headings, YAML, tables, blockquotes); end-to-end round trip. LLM tests are opt-in (`UNSLOP_RUN_LLM_TESTS=1`).
- **`tests/test_hooks.py`** — hook installer (fresh, idempotent, preserves custom statusline), `unslop-activate.js` banner, `unslop-mode-tracker.js` slash commands + natural language + stop phrases, statusline badge output, symlink refusal, and `CLAUDE_CONFIG_DIR` honoring.
- **`tests/verify_repo.py`** — every SSOT mirror is byte-identical after sync, JSON manifests parse, all JS / Bash / PowerShell scripts are syntax-clean, fixture pairs round-trip, and the plugin + marketplace manifests are wired.
- **`benchmarks/run.py`** — runs `humanize_deterministic` over a corpus of AI-slop markdown and reports AI-ism reduction, per-paragraph flat count, sentences split, bullet groups merged, and per-file structural integrity. `--strict` fails the build on any regression.
- **`benchmarks/check_regression.py`** — compares latest benchmark output against a pinned `post-phase*.json` baseline. Fails if AI-ism reduction drops >2pp, flat-paragraph total rises >2, or preservation breaks. Runs in CI on every PR.
- **`benchmarks/detector_bench.py`** — opt-in AI-detector benchmark (TMR, Desklib). Downloads HF weights on first run. Scheduled weekly via `.github/workflows/weekly-detector-bench.yml`.
- **`evals/perceived_humanness.py`** — blind LLM-as-judge preference harness. Claude Sonnet 4.5 (default) compares unslop-rewritten vs original without side metadata. Emits per-fixture votes + aggregate win rate. Requires `ANTHROPIC_API_KEY`.
- **`evals/`** — additional LLM-driven A/B harness (`llm_run.py` + `measure.py`) for snapshotting baseline vs deterministic vs LLM unslop on a fixed prompt set.

---

## License

MIT
