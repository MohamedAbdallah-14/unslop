<div align="center">

# humanizer

**Make AI output sound like a human wrote it.**

A plugin for Claude Code, Cursor, Windsurf, Gemini CLI, OpenAI Codex, and Copilot.
Strips AI-isms (sycophancy, stock vocab, hedging stacks, em-dash pileups), engineers
burstiness, restores voice. Preserves code blocks, URLs, and technical terms.

**New here?** Start with [**GETTING_STARTED.md**](./GETTING_STARTED.md) — a plain-English on-ramp for non-technical users. This README is the developer reference.

</div>

---

## What This Does

You ask the model a question. The default reply opens with "Great question!", uses "delve" twice, stacks three "however"s, and lays out four paragraphs of identical length. That's the AI fingerprint. Every reader spots it. Every detector flags it.

`humanizer` makes the model write like a careful human at the end of a real day. Direct on the substance. Specific where it matters. Quiet where nothing needs saying.

### Before

> Great question! When optimizing React performance, it's important to note that there are several factors to consider. Firstly, you should leverage the `useMemo` hook to memoize expensive computations. Additionally, it's worth mentioning that `React.memo` can prevent unnecessary re-renders. However, it's also paramount to consider whether these optimizations are truly necessary, as premature optimization can lead to unnecessary complexity. Generally speaking, profile first, then optimize.

### After

> Profile first. The bottleneck is almost never where you'd guess, and `useMemo` everywhere just adds clutter to a component that re-rendered for a different reason. Once you've found a real hotspot: `React.memo` on the child if its props are stable, `useMemo` on the value if recomputing it is the cost.

Same correctness. Different voice.

---

## Install

### Claude Code (recommended)

```bash
git clone https://github.com/MohamedAbdallah-Hu/humanizer.git
cd humanizer
bash hooks/install.sh
```

Windows (PowerShell):

```powershell
pwsh hooks/install.ps1
```

What that does:

- Copies hook scripts to `~/.claude/hooks/` (flat, not a subdirectory)
- Registers `SessionStart` (loads the activation rule) and `UserPromptSubmit` (tracks `/humanizer <mode>` and `stop humanizer`) in `~/.claude/settings.json`, merged safely via Node (never clobbers existing hooks)
- Wires the statusline so `[humanizer:FULL]` (uppercase mode suffix) shows when active

Idempotent. Re-run anytime to upgrade. The bash installer re-verifies `settings.json` state on each run; the PowerShell installer checks file presence only, so pass `-Force` on Windows if `settings.json` was hand-edited.

### Cursor / Windsurf / Cline

Bundled rule files at `.cursor/rules/humanizer.mdc`, `.windsurf/rules/humanizer.md`, `.clinerules/humanizer.md`. Open the project in any of them and the rule loads automatically.

### Gemini CLI

```bash
gemini extension install ./
```

Reads `gemini-extension.json` and loads `GEMINI.md` + the humanizer skill into context.

### OpenAI Codex

The `plugins/humanizer/.codex-plugin/plugin.json` bundle is auto-discovered by the Codex IDE extension.

### Standalone CLI (no IDE needed)

```bash
cd humanizer-humanize
python3 -m scripts --deterministic /path/to/your/CLAUDE.md
```

Two modes: `--deterministic` (regex, no API) or default LLM mode (calls Claude). See [`humanizer-humanize/README.md`](./humanizer-humanize/README.md).

---

## Use

### Toggle modes mid-conversation

| Phrase | Effect |
|--------|--------|
| `/humanizer` | Turn on (balanced) |
| `/humanizer subtle` | Light touch |
| `/humanizer balanced` | Default |
| `/humanizer full` | Strong rewrite |
| `/humanizer voice-match` | Mimic a provided sample |
| `/humanizer anti-detector` | Adversarial paraphrase |
| `stop humanizer` | Off |
| `normal mode` | Off |

Mode persists for the whole session.

### Sub-skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| `humanizer` | `/humanizer` | Active humanization for live responses |
| `humanizer-commit` | `/humanizer-commit`, `/commit` | Conventional Commits in human voice |
| `humanizer-review` | `/humanizer-review`, `/review` | Direct, kind PR review comments |
| `humanize` (`humanizer-humanize`) | `/humanize <file>` | Rewrite a markdown file (preserves code, URLs, headings) |
| `humanizer-help` | `/humanizer-help` | Reference card |

### Configure default mode

Env var:

```bash
export HUMANIZER_DEFAULT_MODE=full
```

Or `~/.config/humanizer/config.json`:

```json
{ "defaultMode": "full" }
```

Resolution: env var > config file > `balanced`.
Set to `"off"` to disable session-start activation entirely.

---

## What Stays Exact

The file-rewriter (`humanizer-humanize`) placeholder-protects these in deterministic mode and fails the run if the validator detects they changed:

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
| Stock vocab | delve, tapestry, testament, navigate (figurative), embark, journey (figurative), realm, landscape, pivotal, paramount, seamless, holistic, leverage (filler), robust (filler), comprehensive (filler), cutting-edge, state-of-the-art | det |
| Hedging stacks | "It's important to note that", "It's worth mentioning", "Generally speaking", "In essence", "At its core" | det |
| Performative balance | A "however" appended to every claim | det |
| Transition tics | "Furthermore,", "Moreover,", "Additionally,", "In conclusion,", "To summarize," at start of a sentence | det |
| Em-dash pileups | More than two em-dashes per paragraph (bullet lists get a per-item budget) | det |
| Tricolon padding | "X, Y, and Z" stacks where two would suffice | llm |
| Bullet soup | Three bullets that say the same thing → one sentence | llm |
| Tidy 5-paragraph essay | Real prose has uneven paragraph length | llm |

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

The academic consensus across Categories 05, 15, 16, and 18: **the detection arms race is structurally unwinnable for detectors**. Adversarial Paraphrasing (NeurIPS 2025) drops every tested detector's TPR by ~87%. DIPPER did roughly the same thing in 2023. At the same time, detectors have a huge false-positive problem on non-native English writers (Liang et al. *Patterns* 2023: >50% of TOEFL essays flagged as AI). So a flagged score means less than marketing pages suggest.

What actually lowers detector scores, ordered by strength:

1. **Paraphrase through a different model family.** If GPT wrote it, have Claude rewrite. Or Gemini. Different stylometric fingerprints. This is the single strongest lever.
2. **Burstiness.** Span sentence lengths roughly 4 to 35 words inside a single paragraph.
3. **Specificity the model can't fake.** Real dates, real project names, real numbers, first-person anecdotes. Training data doesn't contain *your* specifics.
4. **Contractions and small fragments.** "don't", "won't", the occasional start with "And" or "But".
5. **Break predictable structure.** If every bullet has the same shape (verb + metric + with + tool), vary half of them.
6. **One or two rough edges.** A slightly awkward phrasing, a parenthetical trail, a non-linear logical jump — all of these read human.

Commercial humanizer SaaS (Undetectable.ai, StealthGPT, WriteHuman, HIX Bypass, the ~150 products Category 18 audits) mostly don't beat a second pass through a different model plus five minutes of manual editing. Independent audits (DAMAGE COLING 2025; Epaphras & Mtenzi 2026) show wide gaps between their "99.8% undetectable" claims and reality, and the gap shifts monthly.

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

One finding from the research that almost every humanizer tool ignores: training (or prompting) a model to sound warmer raises its error rate 8–13% and amplifies sycophancy (Ibrahim/Hafner/Rocher 2025, Category 07). Fluent wrongness is worse than stiff accuracy, especially on a resume where a wrong date or an inflated metric can end the interview.

After humanizing anything factual, re-verify every number, date, title, and tool name against the source. The humanizer doesn't hallucinate facts, but the rewrite pass can smooth over a number you misremembered in the first place and make it sound confident.

### `/humanizer anti-detector` mode

Covers items 1, 2, 4, 5 from the detector list in one pass. Slower than `full` because it does adversarial paraphrase and burstiness targeting explicitly. Use it for resumes, essays, and anything where the reader might pipe the text into GPTZero or Turnitin. Skip it for code, legal, or anything where precision beats voice.

---

## Architecture

```
.
├── skills/                   # SSOT for the five agent-facing skills
│   ├── humanizer/             — main mode
│   ├── humanizer-commit/      — commit messages
│   ├── humanizer-review/      — PR comments
│   ├── humanizer-help/        — reference card
│   └── humanize/              — mirror of humanizer-humanize file rewriter
├── humanizer-humanize/       # SSOT for the file-rewriter (Python + skill)
├── rules/                    # SSOT for the short always-on activation text
├── commands/                 # Claude Code slash commands (TOML)
├── hooks/                    # SessionStart + UserPromptSubmit + statusline + installers
├── .claude-plugin/           # Claude Code marketplace + plugin manifest
├── .cursor/                  # Cursor rules + skills (mirror)
├── .windsurf/                # Windsurf rules + skills (mirror)
├── .clinerules/              # Cline rules (mirror)
├── .agents/                  # Agents marketplace manifest
├── plugins/humanizer/        # Codex plugin bundle
├── tests/                    # pytest unit tests
├── docs/research/            # optional research compendium (not part of the plugin bundle)
└── .github/workflows/        # CI + sync SSOT to mirrored locations
```

Source of Truth: `skills/humanizer/SKILL.md`, `rules/humanizer-activate.md`, `humanizer-humanize/SKILL.md`. The `sync.yml` workflow propagates these to every mirrored location on push to main.

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

- **`tests/humanizer-humanize/`** — file-type detection, sycophancy / hedging / stock-vocab / performative-balance strip, code + URL + heading preservation, end-to-end round trip, and fixture-pair regression. LLM tests are opt-in (`HUMANIZER_RUN_LLM_TESTS=1`).
- **`tests/test_hooks.py`** — hook installer (fresh, idempotent, preserves custom statusline), `humanizer-activate.js` banner, `humanizer-mode-tracker.js` slash commands + natural language + stop phrases, statusline badge output, symlink refusal, and `CLAUDE_CONFIG_DIR` honoring.
- **`tests/verify_repo.py`** — every SSOT mirror is byte-identical after sync, JSON manifests parse, all JS / Bash / PowerShell scripts are syntax-clean, fixture pairs round-trip, and the plugin + marketplace manifests are wired.
- **`benchmarks/run.py`** — runs `humanize_deterministic` over a corpus of AI-slop markdown and reports AI-ism reduction, word delta, and per-file structural integrity. `--strict` fails the build on any regression.
- **`evals/`** — optional LLM-driven A/B harness (`llm_run.py` + `measure.py`) for snapshotting baseline vs deterministic vs LLM humanizer on a fixed prompt set. Requires `ANTHROPIC_API_KEY` or the `claude` CLI.

---

## License

MIT
