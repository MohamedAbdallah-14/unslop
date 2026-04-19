# Commercial Humanizer Tools — Angle C: Open-Source Clones & Self-Hosted Alternatives

**Research value: high** — The OSS humanizer ecosystem is surprisingly crowded (~30+ public repos) and reveals a clear stack of techniques that commercial tools monetize. Quality is uneven, but patterns, dead-ends, and leverage points are visible.

Scope: repositories that clone, self-host, extend, or reverse-engineer commercial humanizers (Undetectable.ai, StealthGPT, StealthWriter, WriteHuman, QuillBot, etc.). Includes full web apps, APIs, CLIs, browser/IDE extensions, and research code.

---

## Repositories (30 total, grouped by archetype)

### A. Full-stack humanizer apps (self-hostable)

| # | Repo | Stack | License | Approach | Notable |
|---|------|-------|---------|----------|---------|
| 1 | [`ksanyok/TextHumanize`](https://github.com/ksanyok/TextHumanize) | Python / PHP / TypeScript | MIT-style dual | 38-stage adaptive pipeline; "PHANTOM" gradient-guided adversarial engine, "ASH" signature humanization, SentenceValidator; 100% offline, zero deps | Marketed as 60–90% detection reduction across 25 languages. Heaviest OSS effort in the space; TM-branded internal stages suggest commercialization intent. |
| 2 | [`rudra496/StealthHumanizer`](https://github.com/rudra496/StealthHumanizer) | TypeScript (web) | MIT | BYOK against 13 LLM providers; 4 rewrite levels, 13 tones, multi-pass "ninja mode"; built-in 12-metric detector (perplexity, burstiness, TTR, etc.) | Closest OSS clone of StealthWriter UX. Vercel/GitHub Pages deploy. No server-side keys. |
| 3 | [`DadaNanjesha/AI-Text-Humanizer-App`](https://github.com/DadaNanjesha/AI-Text-Humanizer-App) | Streamlit + spaCy + NLTK + HF | — | Rule-based: contractions, academic transitions, passive voice, synonym swap | ~245★. Highest-starred pure-Python humanizer. Demonstrates that simple rules ship. |
| 4 | [`DadaNanjesha/AI-content-detector-Humanizer`](https://github.com/DadaNanjesha/AI-content-detector-Humanizer) | Streamlit | — | Combined PDF AI-detector + humanizer | Shows the detect→rewrite loop as a single product. |
| 5 | [`Firdavs-coder/ai_humanizer`](https://github.com/Firdavs-coder/ai_humanizer) | Streamlit + Ollama (phi3) | — | Local LLM rewrite + smart typo insertion + punctuation variance | Fully local, no outbound calls. |
| 6 | [`abdibrokhim/humanaize`](https://github.com/abdibrokhim/humanaize) | Next.js + TypeScript + Clerk | — | BYO AI/ML API (200+ models); SaaS-style web app | ~46★. Template for "commercial clone" with auth built in. |
| 7 | [`vran-sen/ai-detect`](https://github.com/vran-sen/ai-detect) | Streamlit + NLTK | — | 50+ linguistic markers, Bayesian scoring, Light/Medium/Strong strength | Detector-first architecture with humanizer bolted on. |
| 8 | [`ZAYUVALYA/AI-Text-Humanizer`](https://github.com/ZAYUVALYA/AI-Text-Humanizer) | Vanilla JS (client-side) | open | In-browser synonym replacement using Kaggle English synonyms dataset | Demonstrates feasibility of 100% client-side humanization. |

### B. APIs / services (self-hosted drop-ins)

| # | Repo | Stack | Approach |
|---|------|-------|----------|
| 9 | [`ADEMOLA200/Humanize-AI`](https://github.com/ADEMOLA200/Humanize-AI) | Python/Flask (T5 `Vamsi/T5_Paraphrase_Paws`) + Go rewrite service | Microservice split: T5 paraphrase → Go-based synonym/structure/noise injection. Targets Originality.ai, GPTZero, Turnitin. |
| 10 | [`unknownman1244/ai-humanizer-api`](https://github.com/unknownman1244/ai-humanizer-api) | Node.js | MIT-licensed REST API; cross-platform. |
| 11 | [`samrand96/Undetectable-AI`](https://github.com/samrand96/Undetectable-AI) | Python + Ollama (dolphin-mistral) | DOCX ingestion; local LLM + translation + grammar correction. Despite the name, it's a local pipeline, not an API wrapper. |
| 12 | [`takumar-x/AI-Humanizer`](https://github.com/takumar-x/AI-Humanizer) | Python + Ollama | Minimal local humanizer. |

### C. CLI / agent / IDE-skill humanizers

| # | Repo | Stack | Notable |
|---|------|-------|---------|
| 13 | [`itsjwill/humanizer-x`](https://github.com/itsjwill/humanizer-x) | Claude Code Skill | 4-pass engine, 30 AI patterns; manipulates perplexity/burstiness/entropy; SSML disfluency injection for voice agents. Explicitly positioned as OSS replacement for StealthWriter/WriteHuman/Undetectable.ai. |
| 14 | [`lxgicstudios/humanize-cli`](https://github.com/lxgicstudios/humanize-cli) | Node.js npm CLI | Subcommands: `score`, `analyze`, `suggest`, `transform`, `watch`. Dir-level monitoring. |
| 15 | [`brandonwise/humanizer`](https://github.com/brandonwise/humanizer) | Node.js | 29 AI patterns, 500+ vocab terms, burstiness/TTR/readability; cites Wikipedia "Signs of AI Writing". |
| 16 | [`rithulkamesh/humanize`](https://github.com/rithulkamesh/humanize) | Python, GPL-v3 | Deterministic rule-based restructuring; no LLM, no generation. |
| 17 | [`Aboudjem/humanizer-skill`](https://github.com/Aboudjem/humanizer-skill) | Agent skill | Perplexity+burstiness focus, em-dash/vocab bans ("delve", "leverage", "tapestry"). |
| 18 | [`imsv1301/unmask-ai`](https://github.com/imsv1301/unmask-ai) | — | Same vocab-ban + sentence-length-variance playbook. |
| 19 | [`Mohit1053/Humanizer`](https://github.com/Mohit1053/Humanizer) | Python + Ollama Llama3 | Batch CSV processor, resume/progress. Targets <10% detection score. |

### D. Browser & platform extensions

| # | Repo | Target | Notes |
|---|------|--------|-------|
| 20 | [`icarodredd/HumanizeAI`](https://github.com/icarodredd/HumanizeAI) | Chrome MV3 | JS/Tailwind, MIT. |
| 21 | [`SupratimRK/Ai-rewrite`](https://github.com/SupratimRK/Ai-rewrite) | Chrome | Right-click → Gemini/OpenAI rewrite, 21+ modes. |
| 22 | [`birkankervan/ai-text-rewriter`](https://github.com/birkankervan/ai-text-rewriter) | Chrome (Plasmo/React) | BYOK (OpenAI/Gemini/Claude via OpenRouter/Groq); local key storage. |
| 23 | [`sandaru1/chatgpt-chrome-extension`](https://github.com/sandaru1/chatgpt-chrome-extension) | Chrome | Context menu → ChatGPT rewrite in place. |
| 24 | [`dev3mike/ai-rewriter`](https://github.com/dev3mike/ai-rewriter) | Chrome (TS) | OpenAI/OpenRouter BYOK, dark UI. |
| 25 | [`frolvanya/ai-humanizer`](https://github.com/frolvanya/ai-humanizer) | Raycast | ~34★. Wraps external Rephrasy API. |
| 26 | [`raycast/extensions/ai-humanizer`](https://github.com/raycast/extensions/tree/main/extensions/ai-humanizer) | Raycast (official store) | Same upstream; shipped in Raycast's monorepo. |
| 27 | [`Netropolitan/AI-Text-Tools`](https://github.com/Netropolitan/AI-Text-Tools) | Windows hotkey app | OpenAI/Claude/Gemini/Ollama; select-anywhere rewrite. |

### E. Research / adversarial code & reverse engineering

| # | Repo | Notes |
|---|------|-------|
| 28 | [`chengez/Adversarial-Paraphrasing`](https://github.com/chengez/Adversarial-Paraphrasing) | NeurIPS 2025 — "Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text." Training-free: instruction-tuned LLM paraphrases under guidance from a detector; **transfers across detectors** because strong detectors converge on the same human-text distribution. Most academically credible entry in the space. |
| 29 | [`obaskly/AiTextDetectionBypass`](https://github.com/obaskly/AiTextDetectionBypass) | Automates the undetectable.ai web UI (TXT/DOCX/PDF, tone/readability). Effectively a scraper/wrapper, not an engine. |
| 30 | [`Janabi/undetectable-ai`](https://github.com/Janabi/undetectable-ai) (npm `undetectable-api`) | Unofficial TS/Node wrapper of Undetectable.ai's **Detector** endpoints (not the humanizer). Only true API-wrapper found. |

---

## Patterns

1. **Three technique tiers, stacked in every "serious" repo:**
   - Tier 1 — Lexical: contraction expansion/contraction, synonym swap, vocab bans ("delve", "leverage", "tapestry", em-dash removal).
   - Tier 2 — Statistical fingerprint: forced burstiness (mixing 3-word and 40+-word sentences), perplexity variance, TTR/entropy targets.
   - Tier 3 — Adversarial/model-guided: paraphrase loops guided by an embedded detector score (StealthHumanizer's 12-metric engine, humanizer-x, academic `Adversarial-Paraphrasing`).
2. **"Detector + humanizer in one app" is standard.** Almost every serious repo bundles its own detector, both for UX (before/after score) and to drive iterative rewrite loops.
3. **BYOK is dominant.** Most 2024–2026 repos avoid server-side keys and ship as client-side or local-LLM tools. This is a deliberate hedge against both cost and TOS exposure — commercial humanizers, by contrast, monetize exactly this abstraction.
4. **Ollama is the de-facto local backend.** phi3, llama3, dolphin-mistral appear repeatedly. "Humanize locally with Ollama" is effectively a template.
5. **T5-PAWS is the de-facto paraphrase model.** When repos use a dedicated paraphrase head (rather than a general LLM), it's almost always `Vamsi/T5_Paraphrase_Paws` or similar PAWS-finetuned T5.
6. **Heavy overlap with anti-detection research on `burstiness`.** Independent testing (referenced by `humanizerai.com`, and implicit in `Adversarial-Paraphrasing`) shows sentence-length variance is a stronger lever than vocab bans — yet the majority of repos still lead with vocab bans. This is a measurable quality gap.
7. **Skill/agent-native packaging is emerging.** `humanizer-x` (Claude Code skill), `Aboudjem/humanizer-skill`, and CLI-first repos treat the humanizer as an agent tool, not a UI — a newer 2025–2026 pattern.

## Trends (2024 → 2026)

- Shift from **pure regex/rule rewriters** (2023) → **LLM-rewrite + detector-in-the-loop** (2024) → **adversarial, detector-guided paraphrase** (NeurIPS 2025, `humanizer-x`).
- Shift from **server-hosted SaaS clones** → **client-side / BYOK / local-LLM** self-hosts.
- Expansion beyond text: `humanizer-x` adds **SSML disfluencies for voice agents**; this is the first sign of multi-modal humanization in OSS.

## Gaps / leverage points

- **No mature, official reverse engineering of commercial humanizer APIs.** Only Undetectable.ai's *detector* endpoint has an unofficial wrapper (`Janabi/undetectable-ai`). Commercial humanizer endpoints (Undetectable, StealthGPT, WriteHuman) are *not* wrapped in any popular OSS repo — an intentional TOS-driven gap.
- **Benchmarks are absent.** No repo ships a reproducible evaluation set against multiple detectors with published numbers. Claims of "60–90%" or "<10% detection" are self-reported.
- **Style preservation is under-served.** Most repos optimize for detection score only; very few preserve author voice, domain terminology, or citations.
- **No canonical dataset of "AI tells"** — each repo curates its own 29/30/500-term list, with heavy duplication and no shared corpus.
- **Thinking / reasoning-trace humanization is absent.** Every repo targets finished prose. No OSS project attempts to humanize the *reasoning process* or chain-of-thought — directly relevant to your project's framing ("humanizing AI output **and thinking**").
- **Evaluation against modern detectors (GPTZero v2, Pangram, Turnitin 2026) is stale.** Most repos validated against 2023-era detectors.

## Cross-domain analogies

- **SEO content-spinning tools of the 2010s** (Spinner Chief, WordAi) pre-figure this entire stack: synonym DB → sentence restructurer → fingerprint obfuscation. The modern humanizer is a spinner with an LLM and an embedded detector. Treating this space as "spinner 2.0" predicts its trajectory: commoditization, then regulatory/platform-side crackdowns.
- **Adversarial examples in image classifiers** (FGSM, PGD). `chengez/Adversarial-Paraphrasing` is the direct NLP analogue: detector gradient → perturbation. Same transferability property holds.
- **Email spam filter evasion.** Burstiness manipulation ≈ word-stuffing/obfuscation patterns; detector-in-the-loop ≈ Bayesian spam evasion. The arms-race dynamic and eventual reliance on *source-level* signals (DKIM/SPF for email, provenance/C2PA for text) is the likely endgame.

## Sources

- [github.com/ksanyok/TextHumanize](https://github.com/ksanyok/TextHumanize) — largest OSS humanizer pipeline.
- [github.com/rudra496/StealthHumanizer](https://github.com/rudra496/StealthHumanizer) — closest StealthWriter clone.
- [github.com/itsjwill/humanizer-x](https://github.com/itsjwill/humanizer-x) — Claude Code skill, adversarial 4-pass.
- [github.com/chengez/Adversarial-Paraphrasing](https://github.com/chengez/Adversarial-Paraphrasing) — NeurIPS 2025 paper code; theoretical backbone for the whole category.
- [github.com/ADEMOLA200/Humanize-AI](https://github.com/ADEMOLA200/Humanize-AI) — T5-PAWS + Go pipeline; representative microservice split.
- [github.com/DadaNanjesha/AI-Text-Humanizer-App](https://github.com/DadaNanjesha/AI-Text-Humanizer-App) — highest-starred Streamlit humanizer.
- [github.com/obaskly/AiTextDetectionBypass](https://github.com/obaskly/AiTextDetectionBypass) — closest thing to a reverse-engineered Undetectable.ai pipeline (UI automation, not API).
- [github.com/Janabi/undetectable-ai](https://github.com/Janabi/undetectable-ai) — only unofficial wrapper of a commercial humanizer vendor's API (detector only).
- [help.undetectable.ai/en/article/developer-api-1fvasec/](https://help.undetectable.ai/en/article/developer-api-1fvasec/) — official API surface that OSS repos notably do **not** wrap.
- [humanizerai.com/blog/gptzero-bypass-test-2026](https://humanizerai.com/blog/gptzero-bypass-test-2026) — independent test showing vocab bans *hurt* bypass rates; contradicts most repos' playbooks.
