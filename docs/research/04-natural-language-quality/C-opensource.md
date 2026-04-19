# Natural Language Generation Quality — Angle C: Open-Source & GitHub

**Research value: high** — The OSS sampling/decoding ecosystem has ~8–10 named, production-ready techniques (min‑p, DRY, XTC, mirostat, typical, top‑n‑sigma, dynatemp, tail‑free, antislop backtracking) that directly translate into levers for humanizing AI output, plus a measurable evaluation stack (MAUVE, EQ‑Bench Creative Writing, burstiness/lmscan) that a Humanizer project can adopt almost verbatim.

**Project context:** Humanizing AI output and thinking. This digest focuses on what the open-source inference/sampling/eval community has shipped on GitHub that a humanizer can either run locally or borrow design patterns from.

---

## Prior Art — Core Repositories

The OSS ecosystem has converged on a pipeline shape: `penalties → repetition-avoidance (DRY) → statistical truncation (top‑k / top‑p / min‑p / top‑n‑σ / typical) → creativity injection (XTC / dynatemp) → temperature → sample`. Every serious inference engine now exposes most of these.

### 1. `ggml-org/llama.cpp` — Reference implementation of the modern sampler stack
- **What it is:** C/C++ inference engine; de-facto reference for samplers beyond the classic top-k/top-p.
- **Relevance to humanization:** Ships DRY, XTC, min-p, typical, tail-free, top-n-σ, mirostat, dynatemp, and customizable `--samplers` ordering. Default order documented as `penalties → dry → top_n_sigma → top_k → typ_p → top_p → min_p → xtc → temperature`. ([smcleod.net guide](https://smcleod.net/2025/04/llm-sampling-parameters-guide/))
- **Key PRs to study:** [#3841 min-p](https://github.com/ggerganov/llama.cpp/pull/3841), [#9702 DRY](https://github.com/ggerganov/llama.cpp/pull/9702), [#9742 XTC](https://github.com/ggerganov/llama.cpp/pull/9742), top-n-σ integration commit [`233461f`](https://github.com/ggml-org/llama.cpp/commit/233461f8121455f957a47e6a22a77b3bc88277b0).
- **Quote (min-p PR #3841):** "Min P… measures the token probability percentages and sets a base min p value… scaled by the top token's probability… filtering tokens before temperature is applied" — positioned as improving "coherent creativity."

### 2. `turboderp-org/exllamav2` — GPU-optimized, sampler-rich backend
- **What:** Fast quantized-inference library popular for creative/roleplay deployments.
- **Relevance:** Exposes min-p, mirostat (tau/eta), tail-free, typical, DRY, XTC plus temperature/top-k/top-p, and notably **does not auto-disable other samplers when mirostat is on** ([tabbyAPI issue #25](https://github.com/theroyallab/tabbyAPI/issues/25)) — a design choice that lets users stack samplers rather than being forced into one mode.

### 3. `vllm-project/vllm` — Production throughput engine
- **What:** `SamplingParams` class in [`vllm/sampling_params.py`](https://github.com/vllm-project/vllm/blob/main/vllm/sampling_params.py); covers temperature, top_p, top_k, min_p, presence/frequency/repetition penalties, beam search, seed, logprobs.
- **Gap worth noting:** DRY/XTC are **not** in mainline. [PR #11368](https://github.com/vllm-project/vllm/pull/11368) proposing DRY was eventually closed despite the community calling DRY "completely mandatory" for creative writing ([issue #8581](https://github.com/vllm-project/vllm/issues/8581)). **Implication for a humanizer:** if targeting vLLM at serving time, creativity samplers must be bolted on externally (e.g., via antislop-vllm or custom logits processors).

### 4. `sgl-project/sglang` — Structured generation + standard sampling
- **What:** ~25k★ serving framework. Supports temperature/top-p/top-k/min-p, frequency/presence penalties, custom logits processors, and — critically — JSON-schema / regex / grammar constraints via compressed finite-state machines.
- **Relevance:** Humanization often needs *structured* output (e.g., emit a JSON of rewritten paragraphs). SGLang makes that coexist with stochastic sampling, something raw HF `generate()` doesn't do natively.

### 5. `huggingface/transformers` — `GenerationConfig` + `LogitsProcessor`
- **What:** The lingua franca. `GenerationConfig` dispatches greedy / multinomial / beam / beam-multinomial / assisted decoding; `LogitsProcessorList` is the extension point for custom samplers (min-p was upstreamed here; anti-slop and top-n-σ ship as community `LogitsProcessor` classes).
- **Relevance:** Any novel humanizer sampler should be implemented as a `LogitsProcessor` for maximum reuse.

### 6. `oobabooga/text-generation-webui` — De-facto sampler UI
- **What:** Exposes every sampler in a Gradio UI: temperature, top_p, top_k, min_p, typical_p, tfs, top_a, repetition_penalty, presence_penalty, frequency_penalty, dry_multiplier, XTC, mirostat, plus **custom sampler order** ([PR #5443](https://github.com/oobabooga/text-generation-webui/pull/5443)). Community-voted presets (Divine Intellect, Big O, Midnight Enigma, Yara) live in the repo as ready-made humanization baselines.
- **Relevance to humanizer UI:** The Parameters tab is the reference design for "give users dozens of knobs without overwhelming them."

### 7. `LostRuins/koboldcpp` (+ `kalomaze/koboldcpp` fork) — Creative-writing-first
- **What:** llama.cpp-derived backend that historically ships experimental samplers first. Default sampler order `[6, 0, 1, 3, 4, 2, 5]`, supports DRY, XTC, typical, dynamic temperature, mirostat.
- **Relevance:** `kalomaze/koboldcpp` is where min-p and much sampler research was first prototyped; good source of "what's next" signals.

### 8. `aphrodite-engine/aphrodite-engine` — vLLM fork with creativity samplers
- **What:** Large-scale inference engine that explicitly keeps DRY, XTC, NO_REPEAT_NGRAM, TOP_NSIGMA, mirostat in its `SamplingType`/sampler-ID modular system.
- **Relevance:** The pragmatic answer to "vLLM but with creative samplers." If a humanizer needs both throughput and modern samplers, this is the path of least resistance.

---

## Prior Art — Named Sampling Algorithms (with paper + repo pairs)

| Sampler | Origin | Reference repo | Humanization use |
|---|---|---|---|
| **Mirostat** | Basu et al., ICLR 2021 | [`basusourya/mirostat`](https://github.com/basusourya/mirostat) | Directly controls *perplexity* (“surprise”) to avoid the "boredom trap" (repetition) and "confusion trap" (incoherence). Target human-text perplexity levels. |
| **Locally Typical** | Meister et al., TACL 2022 ([arXiv 2202.00666](https://arxiv.org/abs/2202.00666)) | integrated into HF/llama.cpp | Selects tokens whose information content matches conditional entropy — explicitly modeled on psycholinguistic human communication efficiency. |
| **Min-P** | Nguyen et al. ([arXiv 2407.01082](https://huggingface.co/papers/2407.01082)) | [`menhguin/minp_paper`](https://github.com/menhguin/minp_paper) | Dynamic threshold scales with top-token confidence. Enables high-temperature creative generation while keeping coherence. |
| **DRY** (Don’t Repeat Yourself) | `p-e-w` (2024) | [oobabooga PR #5677](https://github.com/oobabooga/text-generation-webui/pull/5677) | Exponential penalty `multiplier * base^(n - allowed_length)` on tokens that would extend a previously-seen sequence. Kills verbatim/structural loops without the awkward side-effects of blunt repetition_penalty. |
| **XTC** (Exclude Top Choices) | `p-e-w` (2024) | [oobabooga PR #6335](https://github.com/oobabooga/text-generation-webui/pull/6335) | *Inverts* standard truncation: probabilistically drops the highest-probability tokens. Explicitly advertised as "boosts creativity, breaks writing clichés, and inhibits non-verbatim repetition." |
| **Top-nσ** | Tang et al. 2024 ([arXiv 2411.07641](https://arxiv.org/abs/2411.07641)) | [`Tomorrowdawn/top_nsigma`](https://github.com/Tomorrowdawn/top_nsigma) | Truncates at `max_logit − n·σ`. Stable across temperatures — useful when a humanizer varies temperature by segment. |
| **Tail-Free Sampling (TFS)** | trurl2 / 2020 | in llama.cpp, textgen-webui | Uses second derivative of the sorted probability curve to cut the tail. Older but still in most stacks as a top-p alternative. |
| **Top-A** | community | in textgen-webui | Threshold = `top_a × p_top²`. Quadratic sensitivity to confidence. |
| **Dynamic Temperature** | kalomaze | llama.cpp `dynatemp_*` | Adjusts temperature by distribution entropy — low-entropy (confident) → lower temp, high-entropy (uncertain) → higher temp. Natural fit for "be factual on facts, be creative on prose." |

**Quoted design intent (XTC, [PR #6335 description](https://github.com/oobabooga/text-generation-webui/pull/6335)):** *"XTC inverts this approach by removing the most likely tokens under certain circumstances… removes all tokens except the least probable one meeting a given threshold, with a given probability. This keeps at least one viable choice available, preserving coherence while enabling unprecedented creativity."* This is the closest thing the community has to a dedicated "anti-AI-voice" sampler.

---

## Adjacent Solutions — Humanization-Specific Tooling

### 9. `sam-paech/antislop-sampler` (342★) & `sam-paech/antislop-vllm`
- **What:** Backtracking sampler that detects disallowed words/phrases during inference, rewinds to the problem token, and resamples with adjusted probabilities. Ships `slop_phrase_prob_adjustments.json` (over-represented LLM-isms like "tapestry," "testament," "voice barely above a whisper"). `antislop-vllm` variant does this via OpenAI-compatible APIs using cached logprobs — no custom kernel needed.
- **FTPO (Final Token Preference Optimization) method referenced in the repo reports 90% slop reduction with preserved benchmark performance.** ([arxiv 2510.15061](https://arxiv.org/pdf/2510.15061))
- **Why it matters:** This is the single OSS project most directly targeted at the humanization problem — not just "creative sampling" but *explicitly* "de-AI-ify the token stream." The backtracking architecture is a pattern a Humanizer product can reuse.

### 10. `blader/humanizer` (~14k★) and siblings (`lguz/humanize-writing-skill`, `puneethkotha/humanizer-workbench`, `brandonwise/humanizer`)
- **What:** Claude-Code-era prompt/skill packages — not samplers but prompt-layer rewriters. blader/humanizer is based on Wikipedia's "Signs of AI Writing" guide and detects 29 patterns (significance inflation, AI vocabulary, negative parallelisms, rule-of-three). brandonwise/humanizer adds statistical scoring (burstiness, type-token ratio, readability). lguz/humanize-writing-skill runs a 3-pass pipeline (36+ banned words → 10 structural patterns → human texture).
- **Relevance:** Demonstrates the "post-hoc rewrite" school that complements the "sample-time" school — both are viable architectures for a humanizer. The banned-word/pattern lists are directly reusable corpora.

### 11. `humania-org/humanize`
- **What:** Claude Code plugin applying RLCR (Reinforcement Learning with Code Review) pattern for iterative self-critique rewriting.
- **Relevance:** Illustrates the agent-loop humanization pattern: draft → critique against humanness rubric → revise.

---

## Measurement / Evaluation Stack

### 12. `krishnap25/mauve` + `krishnap25/mauve-experiments` (MAUVE, NeurIPS 2021 Outstanding Paper)
- **Quote (README):** *"MAUVE is a library built on PyTorch and HuggingFace Transformers to measure the gap between neural text and human text with the eponymous MAUVE measure… a measure of the statistical gap between two text distributions."*
- **How:** KL-divergence in a quantized embedding space; captures Type I error (text that doesn't look human) and Type II (lack of diversity). Single-scalar score, also exposed via HuggingFace Evaluate, 16k+ downloads/month on PyPI.
- **Humanizer fit:** Gold-standard distributional metric. Needs "a few thousand generations" per side — so useful as an offline evaluation harness, not a per-request score.

### 13. `EQ-bench/creative-writing-bench` (EQ-Bench Creative Writing v3)
- **What:** 32 prompts × 3 iterations (96 items) at temp 0.7, judged by Claude Sonnet 4, combining isolated rubric scoring with pairwise Elo via Glicko-2. Explicit bias-mitigation for length/position/verbosity/poetic-incoherence.
- **Public leaderboard:** [eqbench.com/creative_writing.html](https://eqbench.com/creative_writing.html).
- **Humanizer fit:** Best-fit external benchmark for *creative* prose quality, not just fluency. A humanizer should be A/B-tested through it.

### 14. Burstiness/statistical-fingerprint libraries — `lmscan` and `BurhanUlTayyab/GPTZero`
- **`lmscan`** (pip-installable): computes 12 statistical features — burstiness, entropy, Zipf deviation, vocabulary richness, slop-word density, etc. Fingerprints 9 LLM families (GPT-4, Claude, Gemini, Llama, Mistral, Qwen, DeepSeek, Cohere, Phi). No neural model, no API key, <50 ms. Ideal as an **inner-loop guard / reward signal** during humanization.
- **`BurhanUlTayyab/GPTZero`**: open-source reimplementation of the GPTZero perplexity-based detector using GPT-2. Useful as an adversarial detector to optimize against.
- **Quote (GPTZero methodology, echoed in multiple sources):** *"Humans naturally vary their sentence construction and diction, writing with short punchy sentences followed by longer ones. In contrast, language models write with consistent sentence lengths and uniform AI-likeness, resulting in low burstiness."* — validating burstiness as a primary target metric.

### 15. `openai/human-eval`
- **Scope caveat:** Code-generation only (pass@k), but worth naming because it's the canonical "HumanEval" — a humanizer project explicitly *writing*-focused should not confuse stakeholders. The writing analogue is EQ-Bench Creative Writing (above), not this.

---

## Market and Competitor Signals

- **Sampler convergence is essentially complete.** Every major OSS inference engine (llama.cpp, exllamav2, vLLM/aphrodite, sglang, textgen-webui, koboldcpp, MLX) ships ~the same 8–12 samplers with the same names. Differentiation is now in (a) sampler *ordering* UX, (b) creativity samplers (DRY/XTC) mainline support, and (c) constrained decoding.
- **The DRY/XTC split is a market tell.** Enterprise-serving stacks (vLLM, SGLang) hesitated to merge DRY/XTC; creative-writing stacks (textgen-webui, exllamav2, aphrodite, koboldcpp, llama.cpp) shipped them. A humanizer sits squarely on the creative-writing side and should assume these are table stakes.
- **"Slop" has a shared vocabulary now.** The existence of `antislop-sampler`, `lmscan`'s slop-density feature, `blader/humanizer`'s 29-pattern list, and the "Signs of AI Writing" Wikipedia article means there's a convergent community definition of what humanization must remove. A humanizer that does not explicitly filter this corpus will be trivially detectable.
- **Pricing/packaging:** Everything above is MIT/Apache/permissive. The commoditization of samplers means a humanizer cannot defensibly sell "we have a better sampler"; differentiation must come from **combination, measurement, and UX**, not sampler invention.

---

## Gaps / Open Problems Visible from the OSS Angle

1. **No mainline "humanness" reward model.** MAUVE is distributional and slow; lmscan is fast but statistical/surface-level. Nothing open-source trains on human-vs-AI preference at paragraph granularity with a public checkpoint, despite the need being obvious.
2. **Sampler composition is still trial-and-error.** Community presets (Divine Intellect, Midnight Enigma) are vibes-based; no repository publishes a grid-search of sampler combinations against MAUVE or EQ-Bench.
3. **Backtracking architecture is underused.** Only `antislop-sampler` backtracks. DRY/XTC/min-p all operate forward-only. A humanizer that combines a forward sampler stack with multi-criterion backtracking (slop + burstiness target + phrase-repetition) has open design space.
4. **Structured humanization is absent.** SGLang's grammar-constrained sampling + antislop-style backtracking would let a humanizer enforce *structural* human-likeness (e.g., target sentence-length variance distribution), but nobody has shipped this combination.
5. **Burstiness as a sampling-time target, not a post-hoc metric.** lmscan quantifies burstiness after the fact; no sampler explicitly biases generation toward a target burstiness trajectory.

---

## Cross-Domain Analogies

- **Network traffic shaping ↔ sampler ordering.** The llama.cpp sampler pipeline (`penalties → dry → filters → xtc → temperature`) is structurally identical to a QoS traffic-shaping chain: classify → police → mark → shape → queue. Lessons from token-bucket/leaky-bucket design (fairness across classes, hysteresis to avoid oscillation) map onto avoiding sampler "fighting" (e.g., mirostat oscillating against min-p).
- **Image-gen classifier-free guidance ↔ XTC.** XTC's "drop the top choice with probability p" is analogous to CFG negative prompting in diffusion — push the distribution *away* from the most-likely mode to escape the mean. The diffusion community's guidance-scale scheduling (higher early, lower late) suggests XTC could be scheduled across a generation rather than constant.
- **Genetic algorithms ↔ antislop backtracking.** The detect-slop-then-resample loop is a fitness-function-driven mutation operator. The GA literature on escaping local optima (simulated annealing schedules, novelty search) is directly applicable to tuning backtrack depth vs. resample temperature.

---

## Sources

- [smcleod.net — LLM Sampling Parameters Guide (Nov 2025)](https://smcleod.net/2025/04/llm-sampling-parameters-guide/) — comprehensive, current parameter-by-parameter reference across llama.cpp/Ollama/MLX.
- [ggml-org/llama.cpp PR #3841 — Min-P sampler](https://github.com/ggerganov/llama.cpp/pull/3841) — original min-p motivation.
- [ggml-org/llama.cpp PR #9702 — DRY sampler merge](https://github.com/ggerganov/llama.cpp/pull/9702) — port of Koboldcpp DRY.
- [ggml-org/llama.cpp PR #9742 — XTC sampler](https://github.com/ggerganov/llama.cpp/pull/9742) — XTC integration.
- [oobabooga/text-generation-webui PR #6335 — XTC original](https://github.com/oobabooga/text-generation-webui/pull/6335) — canonical XTC design note.
- [oobabooga/text-generation-webui PR #5677 — DRY original](https://github.com/oobabooga/text-generation-webui/pull/5677) — canonical DRY design note.
- [oobabooga/text-generation-webui Wiki — Parameters Tab](https://github.com/oobabooga/text-generation-webui/wiki/03-%E2%80%90-Parameters-Tab) — reference UI for sampler exposure.
- [turboderp-org/exllamav2](https://github.com/turboderp-org/exllamav2) — GPU sampler stack reference.
- [vllm-project/vllm `sampling_params.py`](https://github.com/vllm-project/vllm/blob/main/vllm/sampling_params.py) — production sampling surface.
- [vllm-project/vllm issue #8581 — DRY request](https://github.com/vllm-project/vllm/issues/8581) — community signal that creative samplers are "mandatory."
- [sgl-project/sglang](https://github.com/sgl-project/sglang/) — structured generation + sampling.
- [aphrodite-engine/aphrodite-engine](https://github.com/aphrodite-engine/aphrodite-engine) — vLLM fork with creative samplers.
- [basusourya/mirostat](https://github.com/basusourya/mirostat) — original mirostat implementation.
- [menhguin/minp_paper](https://github.com/menhguin/minp_paper) — min-p paper code + benchmarks.
- [Tomorrowdawn/top_nsigma](https://github.com/Tomorrowdawn/top_nsigma) — top-n-σ reference.
- [Locally Typical Sampling — arXiv 2202.00666](https://arxiv.org/abs/2202.00666) — Meister et al. information-theoretic rationale.
- [sam-paech/antislop-sampler](https://github.com/sam-paech/antislop-sampler) — backtracking slop-filter sampler.
- [krishnap25/mauve](https://github.com/krishnap25/mauve) — MAUVE metric library.
- [EQ-bench/creative-writing-bench](https://github.com/EQ-bench/creative-writing-bench) — creative-writing LLM leaderboard.
- [GPTZero — perplexity & burstiness explainer](https://gptzero.me/news/perplexity-and-burstiness-what-is-it) — canonical burstiness framing.
- [BurhanUlTayyab/GPTZero](https://github.com/burhanultayyab/gptzero) — OSS GPTZero implementation.
- [openai/human-eval](https://github.com/openai/human-eval/) — HumanEval (code-only) for naming clarity.
- [blader/humanizer](https://github.com/blader/humanizer), [lguz/humanize-writing-skill](https://github.com/lguz/humanize-writing-skill) — prompt-layer humanization reference implementations.
