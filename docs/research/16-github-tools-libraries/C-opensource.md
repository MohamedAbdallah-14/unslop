# C — The Core Open-Source Catalog: GitHub "Humanize AI Text" Repos

**Research value: high** — Named open-source landscape is real but shallow: one dominant skill-pack, a thick middle of forks and hackathon apps, a small research tail (DIPPER, SICO, watermark-stealing), and few repos that actually move detector scores meaningfully.

**Scope.** Repos that explicitly target "humanize AI text" behavior: pattern-stripping skills, paraphrase-based rewriters (PEGASUS/T5/BART), stylometry/perplexity/burstiness manipulators, detector-evasion scripts, and curated lists. Activity reviewed as of 2026-04. Star counts are approximate snapshots and move quickly for the top skill repos.

---

## 1. Inventory (35 repos, roughly by stars / activity)

### Tier A — Dominant / frequently referenced

| # | Repo | Stars | Language | What it is | Status |
|---|---|---:|---|---|---|
| 1 | [`blader/humanizer`](https://github.com/blader/humanizer) | ~14.5k | Markdown / prompt | Claude Code + OpenCode skill that removes "signs of AI writing" via a 29-pattern list derived from Wikipedia's "Signs of AI writing" guide. Voice calibration + 2-pass audit. | **Active**, very viral in late 2025 / 2026. |
| 2 | [`psal/anonymouth`](https://github.com/psal/anonymouth) | ~1.9k | Java | Classic stylometric obfuscation tool (Drexel PSAL). Uses JStylo to flag features the author should change to mask identity. Predates LLMs but is still the canonical stylometry-lowering reference. | **Abandoned** (last real update 2021); historical reference. |
| 3 | [`PrithivirajDamodaran/Parrot_Paraphraser`](https://github.com/PrithivirajDamodaran/Parrot_Paraphraser) | ~916 | Python | T5-based paraphrase framework with adequacy/fluency/diversity knobs. Not branded as "humanizer" but is the most commonly forked NLP-grade paraphraser behind DIY humanizers. | **Semi-active**, widely depended on. |
| 4 | [`DadaNanjesha/AI-Text-Humanizer-App`](https://github.com/DadaNanjesha/AI-Text-Humanizer-App) | ~258 | Python | Streamlit app using NLTK + `transformers` to rewrite AI text into "formal / academic" style with detector avoidance as an explicit goal. | **Active**. |
| 5 | [`martiansideofthemoon/ai-detection-paraphrases`](https://github.com/martiansideofthemoon/ai-detection-paraphrases) | ~195 | Python | NeurIPS 2023 paper code: paraphrasing (using DIPPER, 11B params) evades detectors; plus retrieval defense. | **Semi-active** (research). |
| 6 | [`obaskly/AiTextDetectionBypass`](https://github.com/obaskly/AiTextDetectionBypass) | ~116 | Python | Automates the commercial `undetectable.ai` site via Selenium: chunking, TXT/DOCX/PDF I/O, Gmail registration. | **Active** (last touched Apr 2025). Not a humanizer in itself — a scraper. |

### Tier B — Hackathon apps, clones, small humanizers

| # | Repo | Stars | Language | Notes |
|---|---|---:|---|---|
| 7 | [`sanjaysah101/humanize-ai`](https://github.com/sanjaysah101/humanize-ai) | ~51 | TypeScript | Next.js 15 + HuggingFace Inference + `compromise` NLP. Tone control, Markov-chain pattern preservation. 3rd place in Hackathon Raptors' "Humanizing AI Text" hackathon (Nov 2024). MIT. |
| 8 | [`abdibrokhim/humanaize`](https://github.com/abdibrokhim/humanaize) | ~46 | TypeScript | Next.js + Clerk auth, powered by AIML API (200+ models). Apache-2.0. |
| 9 | [`ZAYUVALYA/AI-Text-Humanizer`](https://github.com/ZAYUVALYA/AI-Text-Humanizer) | ~40 | JS / HTML | Pure-browser synonym replacer with proper-noun awareness and change-highlighting. Self-described as "early stages". |
| 10 | [`Firdavs-coder/ai_humanizer`](https://github.com/Firdavs-coder/ai_humanizer) | ~34 | Python | Streamlit + Ollama (phi3). Features smart typo insertion, natural punctuation variation, organic repetition. Local-only. |
| 11 | [`CBIhalsen/text-rewriter`](https://github.com/CBIhalsen/text-rewriter) | ~29 | Python | NLTK + TextBlob synonym rewriter. MIT. Minimal. |
| 12 | [`ADEMOLA200/Humanize-AI`](https://github.com/ADEMOLA200/Humanize-AI) | ~25 | Go + Python | Microservice split: Go/Fiber rewriter, Flask T5 paraphrase (`Vamsi/T5_Paraphrase_Paws`). Noise insertion, synonym replacement, sentence restructuring. "Still in development" (Mar 2025). |
| 13 | [`ArshVermaGit/RAW.AI`](https://github.com/ArshVermaGit/RAW.AI) | ~17 | React + Supabase | Claims "99.8% success bypassing major detectors", 50+ languages, <3s response. Marketing-forward README. |
| 14 | [`ksanyok/TextHumanize`](https://github.com/ksanyok/TextHumanize) | ~12 | Python/PHP/TS | 38-stage adaptive pipeline, proprietary PHANTOM™ / ASH™ / SentenceValidator™ trademarks, 100% offline, 25 languages, claims 60-90% detection-score reduction, "235,000+ lines, 2,073 tests". |
| 15 | [`vardhin/Humanizer`](https://github.com/vardhin/Humanizer) | ~8 | Python + SvelteKit | Flask back end + HuggingFace Transformers (T5, BART, Pegasus), two-step pipeline (paraphrase → rewrite). |
| 16 | [`samrand96/Undetectable-AI`](https://github.com/samrand96/Undetectable-AI) | low | Python | DOCX-oriented CLI using Ollama (default `dolphin-mistral`), optional ChatGPT. Translation + humanize + grammar + evaluation modes. |
| 17 | [`rudra496/StealthHumanizer`](https://github.com/rudra496/StealthHumanizer) | ~5 | TypeScript | 13 provider connectors, 4 rewrite levels, 13 tone presets, 16 languages, 12-metric internal detector for self-grading. |
| 18 | [`Mohit1053/Humanizer`](https://github.com/Mohit1053/Humanizer) | ~1 | Python | Ollama + Llama3, multi-prompt targeting "<10% AI detection" on GPTZero/ZeroGPT. CSV batch + resume. README explicitly cites "perplexity variation, burstiness, human quirks" from 2025 research. |
| 19 | [`itsjwill/humanizer-x`](https://github.com/itsjwill/humanizer-x) | ~2 | Claude skill | 4-pass engine: 30 severity-ranked AI patterns + statistical-fingerprint manipulation (perplexity, burstiness, entropy) + SSML disfluencies for voice agents. Positioned as free replacement for paid humanizers. |
| 20 | [`Aboudjem/humanizer-skill`](https://github.com/Aboudjem/humanizer-skill) | low | Claude skill | 30 AI patterns + 5 voice profiles, explicitly targets burstiness and perplexity. |
| 21 | [`humanizerai/agent-skills`](https://github.com/humanizerai/agent-skills) | low | Claude/Cursor | `/detect-ai` and `/humanize` commands; claims to bypass GPTZero/Turnitin/Originality. API-key + paid subscription (commercial skill wrapped around an external API). |
| 22 | [`trailofbits/skills-curated`](https://github.com/trailofbits/skills-curated/tree/main/plugins/humanizer) | (meta) | Markdown | Security-org curated plugin; humanizer plugin detects 24 pattern categories across content, language, style, communication artifacts. Notable as a non-hype source picking it up. |
| 23 | [`imsv1301/unmask-ai`](https://github.com/imsv1301/unmask-ai) | low | HTML + Claude | 3-pass pipeline on Claude Sonnet 4 claiming to bypass GPTZero, Turnitin, Originality.ai, QuillBot. |

### Tier C — Research (usually more load-bearing than the skill repos)

| # | Repo | Stars | What it is |
|---|---|---:|---|
| 24 | [`google-research/google-research` (`dipper/`)](https://github.com/google-research/google-research/tree/master/dipper) | monorepo | **DIPPER** — 11B paraphraser with lexical-diversity + order-diversity knobs. Reduces DetectGPT accuracy 70.3% → 4.6% at 1% FPR. The reference attack used by almost every "paraphrasing evades detectors" paper. |
| 25 | [`cvlab-columbia/RaidarLLMDetect`](https://github.com/cvlab-columbia/raidarllmdetect) | ~34 | ICLR 2024 RAIDAR detector — asks an LLM to rewrite the text and measures edit distance. A defender's tool, but exposes the pattern humanizers actually need to defeat. |
| 26 | [`JamesLWang/RAFT`](https://github.com/jameslwang/raft) | low | "Realistic Attacks to Fool Text detectors" — adversarial word substitutions that keep semantics and beat several detectors including RAIDAR. |
| 27 | [`ColinLu50/Evade-GPT-Detector`](https://github.com/ColinLu50/Evade-GPT-Detector) | low | SICO (Substitution-based In-Context Optimization, TMLR 2024). Optimizes in-context examples so the LLM itself writes human-looking text — no paraphrase post-hoc. Works on GPTZero and the OpenAI classifier. |
| 28 | [`charlottttee/llm-detector-evasion`](https://github.com/charlottttee/llm-detector-evasion) | low | "Language Model Detectors are Easily Optimized Against" — DPO-tunes Llama2-7B to evade OpenAI's RoBERTa-large detector. Fine-tuning attack, not a wrapper. |
| 29 | [`EricX003/ALISON`](https://github.com/EricX003/ALISON) | low | AAAI 2024 — stylometric authorship obfuscation using neural attribution + integrated gradients. The modern heir to Anonymouth. |
| 30 | [`XuandongZhao/WatermarkAttacker`](https://github.com/XuandongZhao/WatermarkAttacker) | ~100s | NeurIPS 2024 — regeneration attacks on **image** watermarks, but the pattern (embed → add noise → reconstruct) transfers directly to text-watermark evasion thinking. |
| 31 | [`eth-sri/watermark-stealing`](https://github.com/eth-sri/watermark-stealing) | low | ICML 2024 — reverse-engineers LLM watermark rules via API queries (~$50), enabling both **spoofing** and **scrubbing**. Directly relevant if targets start watermarking. |

### Tier D — Detector-specific bypass scripts (mostly abandoned / single-trick)

| # | Repo | What it is |
|---|---|---|
| 32 | [`Oct4Pie/zero-zerogpt`](https://github.com/Oct4Pie/zero-zerogpt) | JS trick: inject zero-width / Unicode spaces to disrupt ZeroGPT tokenization. One-trick, trivially patched upstream. |
| 33 | [`ZyluxXD/zerobypass`](https://github.com/ZyluxXD/zerobypass) | Playwright typing-animation bypass for GPTZero's behavioral heuristics. WIP. |
| 34 | [`jayyt12161/GPTZero-Bypasser`](https://github.com/jayyt12161/GPTZero-Bypasser) | Python 3.8 script; transforms flagged text to pass GPTZero. Dead-simple regex + substitution. |
| 35 | [`XDYB/Anti-AI-detect`](https://github.com/XDYB/Anti-AI-detect) | Minimal JS/HTML text obfuscator (homoglyphs / invisible chars). |

### Curated lists

- [`Brandon689/best-ai-humanizer`](https://github.com/Brandon689/best-ai-humanizer) — explicitly ranks commercial humanizers for Turnitin/Originality/GPTZero bypass. Not code.
- [`ToolkitlyAI/awesome-ai-tools` → `Category/AI_Humanize.md`](https://github.com/ToolkitlyAI/awesome-ai-tools/blob/master/Category/AI_Humanize.md) — marketing-style directory of commercial tools (Humbot, AI Humanizer, etc.).

---

## 2. Representative README quotes

- `blader/humanizer`: "removes signs of AI-generated writing from text" — 29 patterns derived from Wikipedia's *Signs of AI writing*, with voice calibration to match personal writing styles.
- `itsjwill/humanizer-x`: "4-pass AI text humanizer… 30 severity-ranked patterns, statistical fingerprint manipulation, SSML disfluency patterns… Free Claude Code skill — replaces $10-20/mo paid humanizers."
- `Aboudjem/humanizer-skill`: "focusing on burstiness (sentence length variance) and perplexity (word predictability)."
- `Mohit1053/Humanizer`: "Designed based on 2025 research about AI detection bypass using perplexity variation, burstiness, and human quirks."
- `ksanyok/TextHumanize`: "100% offline · 25 languages · Zero dependencies · PHANTOM™ · ASH™".
- `martiansideofthemoon/ai-detection-paraphrases` (paper abstract): "Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense" — DetectGPT accuracy 70.3% → 4.6%.
- `eth-sri/watermark-stealing`: attackers can "reverse-engineer watermarks from watermarked LLMs through API queries" for "over 80% average success rate for under $50".

---

## 3. Patterns, Trends, Gaps

### Patterns (what almost everyone does)

1. **Pattern-stripping lists are the new lingua franca.** `blader/humanizer` (29 patterns), `itsjwill/humanizer-x` (30), `Aboudjem/humanizer-skill` (30), `trailofbits` plugin (24 categories) all converge on the same taxonomy: *significance inflation* ("It's important to note…"), AI vocabulary ("delve", "tapestry", "testament"), copula avoidance, rule-of-three constructions, hedging clichés. This is effectively a shared informal standard descending from Wikipedia's "Signs of AI writing".
2. **Perplexity + burstiness is the marketed metric pair.** Nearly every Tier B/C repo invokes the same two GPTZero-era statistics as the thing it manipulates, even when the implementation is just synonym swap + sentence-length shuffling.
3. **Two implementation modes dominate.**
   - *Agent-skill* (prompt bundle for Claude Code / Cursor / OpenCode): `blader`, `humanizer-x`, `humanizer-skill`, `unmask-ai`, `humanizerai/agent-skills`, trailofbits plugin. Low effort, high reach — `blader/humanizer`'s ~14.5k stars is an order of magnitude above everything else.
   - *Hackathon web app* (Next.js/Streamlit + HuggingFace API or Ollama): `sanjaysah101`, `abdibrokhim`, `vardhin`, `Firdavs-coder`, `DadaNanjesha`, `StealthHumanizer`.
4. **T5 / Pegasus / BART are the boring workhorses.** Every repo that does real NLP rather than regex ends up at the same three checkpoints: `tuner007/pegasus_paraphrase`, `Vamsi/T5_Paraphrase_Paws`, or `humarin/chatgpt_paraphraser_on_T5_base`, usually wrapped behind `Parrot_Paraphraser`.
5. **"Offline / local / privacy" is a rising sell.** `ksanyok/TextHumanize`, `Firdavs-coder` (Ollama phi3), `Mohit1053/Humanizer` (Ollama Llama3), `samrand96/Undetectable-AI` (Ollama dolphin-mistral). Likely driven by users not wanting academic work going to OpenAI/Anthropic logs.

### Trends (what changed in 2024 → 2026)

- **Detection accuracy claims in READMEs have exploded and are mostly unverified.** RAW.AI's "99.8% bypass" and TextHumanize's "60-90% reduction" are typical. Only the research tier (DIPPER, SICO, DPO-evasion) ships reproducible benchmarks.
- **Statistical-fingerprint framing has replaced synonym-swap framing.** 2023-era repos (GPTZero-Bypasser, Anti-AI-detect, XDYB) were about character-level tricks and synonym tables. 2025-2026 repos explicitly advertise perplexity/burstiness/entropy manipulation, even if the underlying code is the same.
- **Agent skill packs ate the long tail.** Dedicated web apps have plateaued around 50 stars; a new Claude skill can hit thousands in weeks. Implication: distribution, not model quality, is the moat.
- **Commercial players publish thin OSS shells around paid APIs.** `humanizerai/agent-skills` is open source but requires a $19.99-$49.99/mo subscription; the intelligence is server-side. Expect more of this.

### Gaps (what's missing)

1. **No repo ships a reproducible, multi-detector eval harness.** DIPPER has one, RAFT has one, but none of the humanizer skills measure themselves against GPTZero + Originality + Turnitin + Pangram + BinocularsPlus + Raidar on public corpora. Claimed numbers are aspirational.
2. **No strong coupling of stylometry-lowering with humanization.** Anonymouth (2021) and ALISON (2024) address *authorial* stylometry; the humanizer repos address *AI-vs-human* stylometry. Nobody has combined them into a "preserve my voice while destroying the model's voice" pipeline. This is the most obvious untouched niche.
3. **Voice calibration is advertised but barely implemented.** `blader/humanizer` and `humanizer-x` describe voice modes; under the hood most of these reduce to 3-5 prompt presets. No repo ingests a user's writing corpus and fits a per-user profile.
4. **Watermark-aware humanization is absent.** Google SynthID, OpenAI's watermark research, Stanford's undetectable watermarks — none of the Tier A/B repos reference them. `eth-sri/watermark-stealing` exists in a separate world. When watermarking lands in production, every current humanizer becomes obsolete overnight.
5. **No first-class "explain what it changed and why" output.** Users get rewritten text with no auditable diff. Academic users who need defensibility would pay for this.
6. **No multilingual evaluation.** `ksanyok/TextHumanize` claims 25 languages and `RAW.AI` claims 50+, but public AI-text detectors are English-biased, so "bypass" in non-English is trivial for reasons unrelated to humanization quality.

---

## 4. What actually works vs. what's abandoned

### Works (has real technical substance + is maintained)

- **`google-research/dipper` (via `ai-detection-paraphrases`)** — peer-reviewed, reproducible, devastating against DetectGPT/GPTZero-era detectors. Still the strongest single technique.
- **`ColinLu50/Evade-GPT-Detector` (SICO)** — in-context optimization that produces text that *starts* human, rather than paraphrasing afterward. Architecturally cleaner and beats paraphrase-only attacks.
- **`charlottttee/llm-detector-evasion`** — DPO fine-tuning. Expensive to run but wipes out RoBERTa-family detectors. The baseline any serious humanizer needs to beat.
- **`PrithivirajDamodaran/Parrot_Paraphraser`** — the most widely reused NLP primitive under the hood of every non-toy humanizer.
- **`blader/humanizer`** — works at its stated job (readability + pattern removal). Does *not* bypass calibrated detectors on its own; it's an editor's skill, not an evasion tool.
- **`obaskly/AiTextDetectionBypass`** — works because it reuses an actual paid humanizer (undetectable.ai). The automation is the value, not the humanization.
- **`eth-sri/watermark-stealing`** — works; strategically important.

### Partially works / high-noise / unverified claims

- `itsjwill/humanizer-x`, `Aboudjem/humanizer-skill`, `unmask-ai`, `rudra496/StealthHumanizer`, `Mohit1053/Humanizer`, `ksanyok/TextHumanize`, `ArshVermaGit/RAW.AI` — likely reduce naive-detector scores via paraphrase passes, but their "99%" style claims are self-reported against unnamed detector versions. Use as prompt inspiration, not as evidence of efficacy.

### Abandoned / historical / obsolete

- `psal/anonymouth` and `psal/jstylo` — important history; not usable against modern LLM detectors.
- `jayyt12161/GPTZero-Bypasser`, `XDYB/Anti-AI-detect`, `Oct4Pie/zero-zerogpt`, `ZyluxXD/zerobypass` — single-trick (Unicode spoofing, typing animation, regex substitutions). Patched by detectors years ago; kept for archaeology.
- `CBIhalsen/text-rewriter`, `ZAYUVALYA/AI-Text-Humanizer` — toy NLTK/synonym projects.
- `jehna/humanify` — widely cited in searches because of the name collision, but it *de-obfuscates minified JavaScript*. Not a text humanizer. Worth flagging so future searches don't waste time.

---

## 5. Implications for the Humazier project

1. **Differentiation from `blader/humanizer` et al. requires a real evaluation loop, not another pattern list.** Ship a harness that scores output against ≥3 live detectors on every change — no one else does this in OSS.
2. **Lean on the research tier, not the skill tier, for technique.** DIPPER-style paraphrase + SICO-style in-context optimization + DPO-evasion fine-tuning together cover the known-good evasion space. Skill-pack repos are UX reference at best.
3. **Combine author-stylometry preservation (ALISON-style) with AI-stylometry removal.** This is the one clearly empty niche in OSS.
4. **Assume watermarking is coming.** Track `eth-sri/watermark-stealing` and SynthID publications now; a humanizer that doesn't address watermarks will be obsolete within the project's lifetime.
5. **Prefer a diff-with-rationale output mode over opaque rewrites.** Trust and defensibility are the under-served axes in this market.

---

## Sources

- [github.com/blader/humanizer](https://github.com/blader/humanizer) — dominant Claude Code humanizer skill.
- [github.com/itsjwill/humanizer-x](https://github.com/itsjwill/humanizer-x) — 4-pass skill with explicit burstiness/perplexity framing.
- [github.com/Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) — 30-pattern Claude skill.
- [github.com/trailofbits/skills-curated/tree/main/plugins/humanizer](https://github.com/trailofbits/skills-curated/tree/main/plugins/humanizer) — security-org curated humanizer plugin.
- [github.com/sanjaysah101/humanize-ai](https://github.com/sanjaysah101/humanize-ai) — Hackathon Raptors 3rd-place entry; reference hackathon app.
- [github.com/abdibrokhim/humanaize](https://github.com/abdibrokhim/humanaize) — Next.js humanizer app.
- [github.com/DadaNanjesha/AI-Text-Humanizer-App](https://github.com/DadaNanjesha/AI-Text-Humanizer-App) — NLTK + transformers academic-style rewriter.
- [github.com/ksanyok/TextHumanize](https://github.com/ksanyok/TextHumanize) — offline, trademarked-pipeline Python humanizer.
- [github.com/Mohit1053/Humanizer](https://github.com/Mohit1053/Humanizer) — Ollama/Llama3 multi-prompt humanizer with GPTZero/ZeroGPT targeting.
- [github.com/ADEMOLA200/Humanize-AI](https://github.com/ADEMOLA200/Humanize-AI) — Go + Flask T5 paraphrase microservice.
- [github.com/vardhin/Humanizer](https://github.com/vardhin/Humanizer) — T5 + BART + Pegasus two-step pipeline.
- [github.com/rudra496/StealthHumanizer](https://github.com/rudra496/StealthHumanizer) — 13-provider TS humanizer with a built-in 12-metric detector.
- [github.com/obaskly/AiTextDetectionBypass](https://github.com/obaskly/AiTextDetectionBypass) — automates undetectable.ai.
- [github.com/PrithivirajDamodaran/Parrot_Paraphraser](https://github.com/PrithivirajDamodaran/Parrot_Paraphraser) — T5 paraphrase framework under most humanizers.
- [github.com/martiansideofthemoon/ai-detection-paraphrases](https://github.com/martiansideofthemoon/ai-detection-paraphrases) — NeurIPS 2023 DIPPER evaluation.
- [github.com/google-research/google-research/tree/master/dipper](https://github.com/google-research/google-research/tree/master/dipper) — DIPPER source.
- [github.com/cvlab-columbia/RaidarLLMDetect](https://github.com/cvlab-columbia/raidarllmdetect) — ICLR 2024 RAIDAR rewrite-distance detector.
- [github.com/jameslwang/raft](https://github.com/jameslwang/raft) — adversarial attacks on detectors.
- [github.com/ColinLu50/Evade-GPT-Detector](https://github.com/ColinLu50/Evade-GPT-Detector) — SICO (TMLR 2024).
- [github.com/charlottttee/llm-detector-evasion](https://github.com/charlottttee/llm-detector-evasion) — DPO-based detector evasion.
- [github.com/EricX003/ALISON](https://github.com/EricX003/ALISON) — AAAI 2024 stylometric obfuscation.
- [github.com/psal/anonymouth](https://github.com/psal/anonymouth), [`psal/jstylo`](https://github.com/psal/jstylo) — historical stylometric obfuscation.
- [github.com/eth-sri/watermark-stealing](https://github.com/eth-sri/watermark-stealing) — ICML 2024 watermark stealing.
- [github.com/XuandongZhao/WatermarkAttacker](https://github.com/XuandongZhao/WatermarkAttacker) — NeurIPS 2024 watermark regeneration attacks.
- [github.com/Brandon689/best-ai-humanizer](https://github.com/Brandon689/best-ai-humanizer), [`ToolkitlyAI/awesome-ai-tools`](https://github.com/ToolkitlyAI/awesome-ai-tools/blob/master/Category/AI_Humanize.md) — curated lists.
- [github.com/topics/ai-humanizer](https://github.com/topics/ai-humanizer), [`/topics/humanizer`](https://github.com/topics/humanizer) — GitHub topic indexes.
