# 04 — Natural Language Quality · Angle E: Practical How-Tos & Forums

**Scope.** Community-facing knowledge on how to actually configure LLM sampling to produce natural, non-slop, human-sounding output. Sources are Reddit (r/LocalLLaMA, r/MachineLearning, r/accelerate), Hacker News threads, engineer rentries/gists, creator-maintained guides, and the PRs/issues where these samplers were first argued into existence.

**Research value: high.** The hobbyist / local-inference community is ~1–2 years ahead of commercial APIs on this topic. There is a coherent, converged playbook for "human-feeling" output built around **min-p + DRY + (optional) XTC / Top-nσ**, with strong cross-source agreement on why the classical `temperature + top_p + top_k + repetition_penalty` stack underperforms for naturalness.

**Last synthesized:** 2026-04-19. Many items were last revised 2024–2025; the field is moving, so treat defaults as starting points, not dogma.

---

## Method

Phased web search → deep-fetch of highest-signal primary sources (guides, PR threads, paper repos, community rentries) → cross-reference for agreement vs. drift. Sampled broadly enough to catch named samplers plus the social narrative around them (what the community calls "slop," why API providers lag, what presets SillyTavern RP users actually ship).

---

## High-Signal Sources (sorted by practical utility)

### 1. "Dummy's Guide to Modern LLM Sampling" — AlpinDale
- **URL:** https://rentry.org/samplers
- **Format:** Long-form rentry (≈70KB). Written by @AlpinDale (Aphrodite Engine dev), undated but references Top-nσ (Feb 2025).
- **Coverage:** Every modern sampler with pseudocode — temperature, presence/frequency/repetition penalty, DRY, top-k, top-p, min-p, top-a, quadratic/smooth, dynamic temp, mirostat, XTC, Top-nσ, typical-p, TFS.
- **Key claim:** Truncation samplers (min-p, top-nσ) should go **before** temperature so the candidate set is chosen from the model's true confidence distribution, not a reshaped one.
- **Why it matters:** Closest thing the open-source community has to a canonical reference.

### 2. HN: "Dummy's Guide to Modern LLM Sampling" discussion
- **URL:** https://news.ycombinator.com/item?id=43887637
- **Format:** HN thread, April 2025. ~200 comments. Min-p paper first author (`menhguin`) answers questions.
- **Money quotes:**
  - *"Top N sigma is currently the best general purpose sampler by far."*
  - *"Temperature can and should be scaled far higher than it is today. Temps of 100 are totally fine with techniques like min-p and top N sigma."*
  - *"Top-n-sigma has been around since mid 2024, min-p since 2023, and we are still waiting for these innovations to be integrated outside of open source stuff… It's being done slowly on purpose by API providers because they don't want to deal with the risk of models being 'too creative' (also high temp likely breaks their watermarking)."*
- **Why it matters:** Direct from the min-p author; confirms the "commercial APIs are deliberately capped" narrative.

### 3. kalomaze — "LLM Samplers Explained" (gist)
- **URL:** https://gist.github.com/kalomaze/4473f3f975ff5e5fade06e632498f73e
- **Format:** Gist + video walkthroughs (Feb 2024, updated through 2026). Author designed min-p and dynamic temperature.
- **Key idea:** Top-P is "too linear" — it will drop a 25% token as easily as a 0.1% token if the cumulative sum crosses the threshold. Min-P fixes this by scaling the cutoff to the top token's probability.
- **Practical tip:** "Temperature last in the sampler order" — if temperature comes first, it distorts what Min-P sees.

### 4. smcleod.net — "LLM Sampling Parameters Guide" (updated Nov 2025)
- **URL:** https://smcleod.net/2025/04/llm-sampling-parameters-guide/
- **Format:** Cross-framework reference (llama.cpp, Ollama, MLX) with default tables and troubleshooting.
- **Critical detail for Ollama users:** Ollama **disables min-p by default (0.0)** and ships `repeat_penalty=1.1` by default; llama.cpp does the opposite (`min_p=0.1`, `repeat_penalty=1.0`). Swapping backends without re-tuning will silently change output character.
- **Default llama.cpp sampler pipeline:** `penalties → dry → top_n_sigma → top_k → typ_p → top_p → min_p → xtc → temperature`

### 5. rpwithai.com — "Understanding Sampler Settings For AI Roleplay"
- **URL:** https://rpwithai.com/understanding-sampler-settings-for-ai-roleplay/
- **Format:** Opinionated RP-focused guide (2025), written against SillyTavern + KoboldCPP stack.
- **Core recipe:** Start with **Min-P + Temperature + DRY only**. Neutralize everything else. "Simpler is better."
- **Rule of thumb:** Min-P default 0.02; boring → lower by 0.005; incoherent → raise by 0.005. Temperature can go to 1.8+ if Min-P is protecting the floor.
- **DRY tuning:** Default (0.8 multiplier / 1.75 base / 2 allowed length) is solid, but **raise `allowed_length` to 4** to stop DRY from butchering proper nouns.

### 6. r/LocalLLaMA — "What actually works for roleplay (in my experience)"
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1r4zbqf/what_actually_works_for_roleplay_in_my_experience/
- **Format:** Field-report thread, 2025.
- **Take:** Sampler settings alone aren't enough to kill "caricature" feel — the bigger unlock is **randomizing parts of the system prompt (mood, goal, desire) across turns**. Sampling fixes token-level slop; prompt randomization fixes persona-level slop.
- **Relevance:** Useful pairing for a humanizer project — combine sampler changes with state perturbation.

### 7. HN: "XTC — An LLM sampler that boosts creativity, breaks writing clichés"
- **URL:** https://news.ycombinator.com/item?id=41286604
- **Format:** HN discussion of oobabooga PR #6335 (Aug 2024).
- **Core idea:** XTC inverts truncation — it **removes the *most* likely tokens** with probability `p`, keeping one viable above-threshold token for coherence. Directly targets non-verbatim / structural repetition that repetition penalties can't see.
- **Creator quote (from PR):** *"The creativity is off the charts, while the coherence is virtually unchanged."*
- **Typical values:** threshold 0.1, probability 0.5 — applied *after* truncation samplers.

### 8. llama.cpp PR #3841 — Min-P merge (Oct 2023)
- **URL:** https://github.com/ggml-org/llama.cpp/pull/3841
- **Why it matters:** The original argument. Min-P's design rationale is spelled out here and in the paper: top-p includes too many tail tokens under flat distributions, too few under peaked ones; min-p adapts because the cutoff is scaled by the top token's probability.
- **Follow-up paper:** ICLR 2025 Oral — "Turning Up the Heat: Min-p Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., OpenReview `ga46iBDt7E`).

### 9. exllamav2 issue #447 — DRY proposal (p-e-w)
- **URL:** https://github.com/turboderp-org/exllamav2/issues/447
- **Format:** Design doc as a GH issue; the proposal that became DRY.
- **Core claim:** Classical repetition penalty is a "blunt instrument that distorts the grammar of standard language that the model was trained to reproduce, and it doesn't actually prevent looping reliably." DRY penalizes *n-gram continuations*, grows exponentially with sequence length, and has sequence breakers to spare chat template tokens.
- **Testing:** Author reported ≥200k tokens across 100+ contexts without the looping failures classical rep-pen has. Now merged into llama.cpp, KoboldCPP, text-generation-webui; in-flight for vLLM / Aphrodite.

### 10. oobabooga PR #5677 — DRY implementation
- **URL:** https://github.com/oobabooga/text-generation-webui/pull/5677
- **Defaults (author-recommended):** `multiplier=0.8`, `base=1.75`, `allowed_length=2`. Community consensus: raise `allowed_length` to 4 for natural prose, keep defaults for chat.

### 11. Top-nσ — llama.cpp PR #11223 + Tomorrowdawn/top_nsigma
- **URLs:** https://github.com/ggml-org/llama.cpp/pull/11223 · https://github.com/Tomorrowdawn/top_nsigma
- **Mechanism:** `logits[logits < max(logits) - n * std(logits)] = -inf`. Truncates based on standard-deviation distance from the top logit; stays stable as temperature rises.
- **Why community picked it up fast:** Unlike min-p, it doesn't degrade when temperature is aggressively cranked. Min-p author publicly says it outperforms min-p as a general sampler.
- **Ranges:** `n=0.7` conservative, `n=1.3` diverse, `1.5` is rpwithai's recommended starting value.

### 12. oobabooga PR #6335 — XTC (Exclude Top Choices) merge
- **URL:** https://github.com/oobabooga/text-generation-webui/pull/6335
- **Community reception:** Controversial but sticky. Writers report "spice" and less cliché repetition; math/coding users report accuracy loss. Now merged into llama.cpp, MLX, Aphrodite.

### 13. llama.cpp PR #6445 / oobabooga #5403 — Smooth (Quadratic) Sampling
- **URLs:** https://github.com/ggml-org/llama.cpp/pull/6445 · https://github.com/oobabooga/text-generation-webui/pull/5403
- **Idea (kalomaze):** Instead of truncating, apply a quadratic transform to logits based on distance from top logit. Tight top pairs stay tight, far tail gets suppressed smoothly.
- **Recommended smoothing factor for creative work:** 0.2–0.3. <0.1 isn't useful; 10.0 approaches near-deterministic.

### 14. rentry.org/dynamic_temperature — kalomaze
- **URL:** https://rentry.org/dynamic_temperature
- **Idea:** Temperature scales per-token based on the *concentration* of the probability distribution (HHI / Herfindahl-Hirschman Index). When the model is confident, temperature drops automatically; when uncertain, it rises.
- **Community usage:** SillyTavern's Dynamic-Temp RP preset; `dynatemp_range` parameter in llama.cpp.
- **Caveat from Virt-io SillyTavern preset:** Don't set exponent > 1; lower exponent + min-p bumped to 0.075 is the known-good combo.

### 15. SillyTavern presets (Virt-io, sphiratrioth666)
- **URLs:** https://huggingface.co/Virt-io/SillyTavern-Presets · https://huggingface.co/sphiratrioth666/SillyTavern-Presets-Sphiratrioth
- **Take-away:** The actual shipped presets for the largest "humanizing LLM output" community (roleplay/creative writing, ~300+ likes) neutralize *everything* except **Min-P + DRY + Temperature**. This is the de facto production recipe.

### 16. sam-paech/antislop-sampler + Antislop paper (arXiv 2510.15061)
- **URLs:** https://github.com/sam-paech/antislop-sampler · https://arxiv.org/abs/2510.15061
- **Mechanism:** String/regex matching with *backtracking* — when the model emits a banned phrase like "a tapestry of" or "testament to," the sampler rewinds and resamples the prior tokens with that branch masked.
- **Finding (paper):** Some slop patterns appear **>1000× more frequently in LLM output than in human text**. Sampler achieves ~90% slop reduction on benchmarks while preserving creative-writing quality. Also introduces FTPO fine-tuning for permanent removal.
- **Why it matters for this project:** The first community tool that directly targets naturalness defects rather than token distribution shape.

### 17. r/accelerate — "AI slop is a skill problem, not a model problem"
- **URL:** https://www.reddit.com/r/accelerate/comments/1r20y1c/ai_slop_is_a_skill_problem_not_a_model_problem/
- **Format:** Reddit essay, 2025.
- **Counter-narrative:** Slop reduces with taste, not tooling. A user who knows good writing will prompt and post-edit around it; users who can't detect slop can't be saved by better samplers. Useful to hold alongside the purely mechanistic threads.

### 18. YouTube / DEV.to tutorials (orientation tier)
- **"LLM Parameters Explained: Temperature, Top-P, Top-K & More"** — https://www.youtube.com/watch?v=CPs_PGELoMY
- **DEV.to — "How LLMs Actually Generate Text: Temperature, Top-K, Top-P, and the Dice Rolls You Never See"** — https://dev.to/thousand_miles_ai/how-llms-actually-generate-text-temperature-top-k-top-p-and-the-dice-rolls-you-never-see-jop
- **Note:** Both cover the basics well but are mostly silent on min-p/DRY/XTC — reflects the lag between frontier community knowledge and mainstream tutorial content.

---

## Cross-cutting patterns

### Pattern 1 — The "naturalness stack" has converged
Across rpwithai, SillyTavern presets (Virt-io, sphiratrioth666), kalomaze's advice, the rentry guide, and HN comments, the recommended stack is the same three samplers:

> **Min-P (or Top-nσ) for quality floor · DRY for repetition · Temperature for creativity** — with everything else neutralized unless you have a specific reason.

This is a real convergence, not echo-chamber repetition — the sources cite different authorities and disagree on edge cases.

### Pattern 2 — "Temperature alone does not remove tokens"
Every serious guide explicitly flags this. High temperature without a truncation floor amplifies the tail. Before min-p, top-p was the default — but top-p is cumulative-probability based, so under flat distributions it admits 50+ tokens, many of them garbage. Min-p (scale-to-top) and Top-nσ (std-dev cutoff) exist specifically to fix this. Implication for humanizing output: temperature is useful, but only behind a dynamic floor.

### Pattern 3 — Repetition penalties hurt naturalness; DRY doesn't
Classical `repetition_penalty` over ~1.1 distorts grammar because it penalizes tokens the model *should* reuse (pronouns, articles, common prefixes). DRY penalizes *repeated n-gram continuations* with a growing penalty, preserving natural repetition while cutting loops. Multiple independent testers (p-e-w, oobabooga, Virt-io) came to the same conclusion within weeks of each other.

### Pattern 4 — High temperature is safe *if* you protect the distribution
Min-p author (`menhguin`) on HN: temperatures of **100** are fine with min-p or top-nσ. rpwithai confirms Temp 1.8+ stays coherent with min-p; Top-nσ extends this to Temp 3+. This flips the common heuristic "keep T ≤ 1.2 for coherence" — that ceiling exists because top-p breaks first, not because the model can't handle it.

### Pattern 5 — Community 12–24 months ahead of commercial APIs
All advanced samplers (min-p, DRY, XTC, Top-nσ, dynamic temp, XTC, antislop) are available only in open-source stacks (llama.cpp, vLLM, Aphrodite, ExLlamaV2, KoboldCPP, text-generation-webui, SillyTavern). OpenAI / Anthropic / Google expose only temperature + top-p + top-k + frequency/presence penalties. Multiple HN commenters and the min-p author attribute this to (a) alignment risk, (b) watermarking fragility at high temperature, and (c) inertia.

### Pattern 6 — Sampler order is load-bearing
llama.cpp default is `penalties → dry → top_n_sigma → top_k → typ_p → top_p → min_p → xtc → temperature`. Kalomaze, rpwithai, smcleod all reiterate: **temperature last**, otherwise truncation samplers judge a reshaped distribution instead of the model's native confidence.

### Pattern 7 — Structural vs. lexical slop are different problems
DRY + frequency penalty handle *lexical* repetition. XTC and Antislop handle *structural / stylistic* slop ("tapestry," "testament," "delve," "it's not X, it's Y"). Writer-oriented users consistently stack them. Min-p alone does not address stylistic slop — that's a common misunderstanding the community has corrected repeatedly.

---

## Practical parameter recipes

All values are starting points; the convention in every guide is "tune by ear, isolate one change at a time."

### A. Natural chat / balanced humanization (safe default)
```
temperature    = 1.0
min_p          = 0.05
top_p          = 1.0    (disabled)
top_k          = 0      (disabled)
dry_multiplier = 0.8
dry_base       = 1.75
dry_allowed_length = 4   # raise from default 2 to protect proper nouns
repeat_penalty = 1.0     # disabled
sampler_order  = default llama.cpp (temp last)
```

### B. Creative writing / storytelling
```
temperature    = 1.2 — 1.8
min_p          = 0.02 — 0.05
dry_multiplier = 0.8
dry_base       = 1.75
dry_allowed_length = 4
xtc_threshold  = 0.1
xtc_probability = 0.5    # applied AFTER truncation
(optionally) smoothing_factor = 0.2–0.3 instead of temperature
```

### C. High-temperature creative (Top-nσ unlocks)
```
temperature    = 2.0 — 3.0+
top_n_sigma    = 1.5     # start here; raise for less coherence, lower for more
min_p          = 0.0     # disabled (conflicts)
dry_multiplier = 0.8
```

### D. Factual / code-leaning (less relevant for humanizer, for completeness)
```
temperature    = 0.3 — 0.7
min_p          = 0.1 — 0.15
repeat_penalty = 1.0 — 1.05 (longer repeat_last_n for code: 128–512)
DRY off for strict structured output
```

### E. Dynamic temperature (less manual tuning)
```
dynatemp_range = 0.5     # temperature oscillates ±0.5 around base
dynatemp_exponent = 1.0 (default)
min_p = 0.05–0.075
DRY on with defaults
```

### F. Anti-slop hardening (post-sampler)
Layer Antislop on top of the above if the target is natural prose specifically — it is orthogonal to the token-distribution samplers and targets named patterns directly.

---

## Gaps & open questions

1. **No standardized "naturalness" benchmark.** Sam Paech's EQ-Bench creative-writing and Antislop eval are the closest; everything else is vibes. This is exactly the gap the Humanizer project can fill.
2. **Min-p / Top-nσ on non-creative tasks.** HN commenter: min-p and XTC underperform default top-p on math/reasoning. The dials that humanize prose may degrade reasoning — needs empirical validation per use case.
3. **Sampling can't overcome training bias.** Antislop paper shows 90% reduction but not 100%. A phrase the model has been RLHF'd to love will resist even backtracking. The long-term humanization path likely requires fine-tuning (FTPO) *in addition to* sampling.
4. **Commercial APIs remain a dead end for advanced samplers.** Anyone building a humanizer on top of OpenAI/Anthropic/Gemini has access to only the weakest tools. The project should assume open-weights or self-hosted inference for full control.
5. **Sampler interactions are under-studied.** e.g. "DRY + XTC + high-temp + dynatemp" has no published ablation — it's community folklore. Someone should actually A/B these.
6. **Burstiness / human rhythm specifically.** The community optimizes for "creative" and "not repetitive" — not explicitly for the sentence-length-variance signal that AI detectors target. There's a research-value gap here for the Humanizer project.

---

## Sources (consolidated)

| # | Source | URL |
|---|---|---|
| 1 | Dummy's Guide to Modern Samplers (AlpinDale) | https://rentry.org/samplers |
| 2 | HN discussion of the guide | https://news.ycombinator.com/item?id=43887637 |
| 3 | kalomaze — LLM Samplers Explained | https://gist.github.com/kalomaze/4473f3f975ff5e5fade06e632498f73e |
| 4 | smcleod — LLM Sampling Parameters Guide | https://smcleod.net/2025/04/llm-sampling-parameters-guide/ |
| 5 | rpwithai — Sampler Settings For AI Roleplay | https://rpwithai.com/understanding-sampler-settings-for-ai-roleplay/ |
| 6 | r/LocalLLaMA — What actually works for roleplay | https://www.reddit.com/r/LocalLLaMA/comments/1r4zbqf/ |
| 7 | HN — XTC sampler discussion | https://news.ycombinator.com/item?id=41286604 |
| 8 | llama.cpp PR #3841 — Min-P | https://github.com/ggml-org/llama.cpp/pull/3841 |
| 9 | exllamav2 #447 — DRY proposal (p-e-w) | https://github.com/turboderp-org/exllamav2/issues/447 |
| 10 | oobabooga PR #5677 — DRY | https://github.com/oobabooga/text-generation-webui/pull/5677 |
| 11 | llama.cpp PR #11223 — Top-nσ | https://github.com/ggml-org/llama.cpp/pull/11223 |
| 12 | oobabooga PR #6335 — XTC | https://github.com/oobabooga/text-generation-webui/pull/6335 |
| 13 | llama.cpp PR #6445 / oobabooga #5403 — Smooth/Quadratic | https://github.com/ggml-org/llama.cpp/pull/6445 |
| 14 | kalomaze — Dynamic Temperature rentry | https://rentry.org/dynamic_temperature |
| 15 | Virt-io SillyTavern presets | https://huggingface.co/Virt-io/SillyTavern-Presets |
| 16 | sphiratrioth666 SillyTavern presets | https://huggingface.co/sphiratrioth666/SillyTavern-Presets-Sphiratrioth |
| 17 | sam-paech/antislop-sampler | https://github.com/sam-paech/antislop-sampler |
| 18 | Antislop paper (arXiv 2510.15061) | https://arxiv.org/abs/2510.15061 |
| 19 | Min-p paper — ICLR 2025 Oral (Nguyen et al.) | https://openreview.net/forum?id=ga46iBDt7E |
| 20 | r/accelerate — "AI slop is a skill problem" | https://www.reddit.com/r/accelerate/comments/1r20y1c/ |
| 21 | DEV.to — How LLMs Actually Generate Text | https://dev.to/thousand_miles_ai/how-llms-actually-generate-text-temperature-top-k-top-p-and-the-dice-rolls-you-never-see-jop |
| 22 | YouTube — LLM Parameters Explained | https://www.youtube.com/watch?v=CPs_PGELoMY |

---

## Implications for the Humanizer project

1. **Default stack to implement first:** Min-P 0.05 + DRY (defaults, allowed_length=4) + Temperature 1.0 + temperature-last ordering. This matches the community consensus and gives the best naturalness-per-effort ratio.
2. **Sampler support matters more than model choice.** Any backend (Ollama, hosted APIs) that doesn't expose DRY / min-p / XTC will cap the ceiling of what the humanizer can do at the decoding stage. Target llama.cpp / vLLM / SGLang as primary runtimes.
3. **Sampling + prompt-state perturbation + Antislop = three-layer defense.** Token distribution (min-p), n-gram repetition (DRY), and stylistic cliché (Antislop) are orthogonal failure modes; all three need treatment for "human-feeling" output.
4. **Own the benchmark.** The field has no shared naturalness benchmark beyond EQ-Bench Creative. Producing one is defensible differentiation.
5. **Expect drift.** The community moved from top-p → min-p → top-nσ in ~18 months. Design the humanizer's sampler config as a pluggable recipe, not hardcoded parameters.
