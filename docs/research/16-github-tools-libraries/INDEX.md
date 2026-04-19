# Category 16 — GitHub Tools & Libraries for Humanization

## Scope

This category maps the open-source tooling layer of AI-text humanization: GitHub repos, companion papers, Claude Code / OpenCode skills, commercial API competitors, and the practitioner conversation around them. Five angles cover it:

- **A. Academic** — research-grade OSS humanizers with peer-reviewed papers (DIPPER, HMGC, HUMPA, StealthRL, AuthorMist, GradEscape, SICO, RAFT, CoPA, StyleRemix, MGTBench, TH-Bench).
- **B. Industry** — blog/listicle/tutorial coverage of OSS humanizer repos, curated lists, and how the OSS scene is splitting into pipelines vs Claude skills vs API wrappers.
- **C. Open-source catalog** — the ~35-repo inventory of named "humanize AI text" projects on GitHub, tiered by activity and technical substance.
- **D. Commercial** — hosted humanizer SaaS (Undetectable.ai, WriteHuman, StealthGPT, HumanizerPro, Humaniser, Apify, etc.) and self-hostable alternatives framed as "libraries-as-managed-services."
- **E. Practical/forums** — Reddit (r/LocalLLaMA, r/BypassAiDetect, r/SEO), HN threads, dev.to tutorials, and GitHub issue debates about whether prompt-only humanization can work at all.

Out of scope: detector research per se (see categories on detection), watermarking protocol design (referenced only where scrubbing humanizers touch it), and non-text modalities.

## Executive Summary

The OSS humanizer landscape as of 2026-04 is sharply bimodal. On one side, a **research tier** (~18 repos, 2023–2026) has converged on four mechanism families — paragraph paraphrase (DIPPER/HMGC), word-level perturbation (RAFT), detector-in-the-loop RL (AuthorMist/StealthRL/HUMPA), and decoding-time guidance (SICO/CoPA) — with benchmarks (TH-Bench, MGTBench-2.0) that let any new humanizer plug in and produce comparable numbers. Small models (GradEscape 139M, AuthorMist 3B) now outperform DIPPER's 11B because the frontier moved from scale to signal quality in the training loop, and attacks **transfer across detectors** — strong empirical evidence that detectors learn overlapping human-text manifolds.

On the other side, a **practitioner tier** dominated by `blader/humanizer` (~14.5k stars, a Claude Code skill built on Wikipedia's *Signs of AI Writing*) has spawned a cottage industry of near-identical `.skill` / `AGENTS.md` / `.mdc` pattern-stripping clones (`humanizer-x`, `slop-humanizer`, `Aboudjem/humanizer-skill`, `brandonwise/humanizer`, `talk-normal`, `anti-slop-writing`). These repos market themselves on perplexity/burstiness manipulation but, in practice, are mostly 29–30-pattern ban-lists wrapped in prompts. **None of them ship reproducible multi-detector eval harnesses**, and calibrated detectors (GPTZero premium, Pangram, Binoculars) still flag most of their output.

The commercial layer (Undetectable.ai, WriteHuman, StealthGPT, HumanizerPro, HumanizerAI, BypassGPT, Humbot, Phrasly, Stealthly, Apify, Deceptioner) has converged on `POST /v1/humanize` with bearer auth, intensity ladders (light/medium/aggressive) or tone ladders (HighSchool→PhD), and per-1K-word pricing. The spread is two orders of magnitude — from Apify's deterministic $0.003/text rules engine to StealthGPT Business's $2.00/1K — which means SaaS margins are defensible only through UX and detection-tuning, not compute. Strikingly, **no commercial player publicly wraps a named OSS library**; the "libraries offered as managed services" thesis is, for now, aspirational.

The practitioner critique (Peggy Kang, `blader/humanizer` issue #82, `@voidborne-d`) is the most important intellectual development of 2025–26: it argues prompt-only humanization is statistically self-defeating because the attacker and the source are the same distribution. Two credible escape hatches exist — (a) rule-based syntactic restructuring (`voidborne-d/humanize-chinese`, `rithulkamesh/humanize`) that produces genuinely non-LLM statistics at per-language cost, and (b) inference-time sampling (`sam-paech/antislop-sampler`, shipped into koboldcpp and open-webui) that backtracks on ~8,000 banned phrases when you control the model. Both are niche relative to skill-pack volume but represent the intellectual frontier.

## Cross-Angle Themes

1. **The research tier and the skill tier barely talk to each other.** DIPPER, HUMPA, StealthRL, GradEscape produce reproducible benchmarks; `blader/humanizer` et al. produce `README` marketing claims. No popular Claude skill imports a DIPPER checkpoint or runs itself against TH-Bench. This is the single biggest structural gap — and the most obvious differentiation niche — across all five angles.
2. **Pattern-stripping has become an informal standard.** ~30-item ban-lists derived from Wikipedia's *Signs of AI Writing* appear in A (BART/Mistral corpus markers), B (clawhub 16-pattern skill), C (`blader/humanizer` 29, `humanizer-x` 30, `Aboudjem` 30, `brandonwise` 29, trailofbits 24), and E (`mbodkebiz/slop-humanizer` "synthesized from 8 humanizer repos"). "Significance inflation," AI vocabulary ("delve", "tapestry"), copula avoidance, and rule-of-three constructions show up across every source.
3. **Perplexity + burstiness is the universal marketing metric pair.** Every Tier B/C repo (`humanizer-x`, `Aboudjem`, `Mohit1053`, `StealthHumanizer`, `unmask-ai`, `TextHumanize`, `brandonwise`) invokes these two GPTZero-era statistics as the thing being manipulated, even when the implementation is just synonym swap + sentence-length shuffling. The academic tier (HUMPA, StealthRL, GradEscape) treats them as incidental.
4. **Four-pass pipelines dominate practitioner UX.** (1) strip AI patterns, (2) inject voice/personality, (3) manipulate statistical fingerprint, (4) verify/score. Explicit in `humanizer-x`, `slop-humanizer`, `StealthHumanizer`'s ninja mode, and the commercial `/v1/humanize` intensity ladder. Academic work achieves the same effect in a single RL policy (StealthRL, HUMPA).
5. **Two order-of-magnitude price spread is real.** Apify's $0.003/text deterministic pipeline vs StealthGPT Business's $2.00/1K vs OSS BYO-key at ~$0.07/1K (unmask-ai) implies the commercial layer's moat is UX and detection-tuning, not compute. OSS repos rarely compete on per-call price; they compete on "free + local + no login."
6. **The naming collision problem is chronic.** `Humanizr/Humanizer` (.NET string formatting, 9.5k stars) and `jehna/humanify` (JS deobfuscation via LLM naming, 3k+ stars) are routinely mis-recommended on Reddit and pollute GitHub topic pages. Every angle calls this out; it's a durable signal-to-noise drag on the category.
7. **Ethical pushback concentrates on HN and is absent from OSS READMEs.** Reddit and dev.to are operational ("how do I…"); HN is normative ("should you…"). SaaS reviewers routinely add "don't use this to deceive evaluators"; OSS posts mostly skip it.
8. **Watermarking is a looming exogenous threat that almost no humanizer repo addresses.** `eth-sri/watermark-stealing` and `XuandongZhao/WatermarkAttacker` exist, but none of the Tier A/B skill repos reference SynthID or Stanford undetectable watermarks. When watermarking lands in production, every current humanizer becomes obsolete overnight.

## Top Sources (Curated)

### Must-read papers

- **DIPPER** — Krishna et al., NeurIPS 2023 (arXiv 2303.13408). The de-facto baseline paraphrase attack; 70.3% → 4.6% on DetectGPT. Everyone benchmarks against it.
- **HUMPA** — Wang et al., ICLR 2025 (arXiv 2410.19230). Small-LM decoding-time proxy in front of frontier LLMs; –70.4% avg AUROC, best-in-class for "small humanizer head" pattern.
- **StealthRL** — arXiv 2602.08934 (2026). GRPO on Qwen3-4B rewarded by joint detector loss; 97.6% ASR, transfers to held-out detectors.
- **AuthorMist** — arXiv 2503.08716 (2025). Pioneered the *commercial-detector-API-as-reward* pattern that every 2025 follow-up copies.
- **GradEscape** — Meng et al., USENIX Security 2025 (arXiv 2506.08188). First gradient-based evader; 139M params beat 11B DIPPER; tested in the wild on Sapling and Scribbr.
- **Adversarial Paraphrasing** — NeurIPS 2025 (arXiv 2506.07001). Training-free universal attack; argues detectors converge on the same human distribution.
- **TH-Bench** — arXiv 2503.08708 (2025). First benchmark explicitly for humanization attacks; 6 attacks × 13 detectors × 6 datasets × 19 domains × 11 LLMs. Headline finding: **no single attack wins effectiveness ↔ quality ↔ cost simultaneously**.
- **Watermark Stealing** — Jovanović et al., ICML 2024. Reverse-engineers watermark rules via API queries for <$50; enables both spoofing and scrubbing.

### Must-read posts/essays

- **Peggy Kang, "Building an AI Humanizer: why we stopped trying to fix prompts"** ([dev.to](https://dev.to/peggggykang/building-an-ai-humanizer-why-we-stopped-trying-to-fix-prompts-bi9)). The rigorous engineering critique: prompts don't fix distributions, sentence-level rewriting does. Two-stage pipeline argument.
- **dannwaneri, "Why I Built My Own Humanizer (And Why You Should Too)"** ([dev.to](https://dev.to/dannwaneri/why-i-built-my-own-humanizer-and-why-you-should-too-2a9e)). Critiques `blader/humanizer` as calibrated against a "generic human baseline"; introduces corpus-grounded voice calibration via `CORPUS.md`.
- **retrorom, "Teaching AI to Write Like a Human: Inside the Humanizer Skill"** ([dev.to](https://dev.to/retrorom/teaching-ai-to-write-like-a-human-inside-the-humanizer-skill-20od)). Before/after tables for common AI patterns; two-pass approach.
- **thehumanizeai.pro, "Why AI Humanizers Don't Work (And the One Thing That Does)"**. 14 tools tested; 12 "did almost nothing." Only structural rewriters move detector scores.
- **`blader/humanizer` issue #82 — "Prompt-based humanization won't solve detection"**. `@voidborne-d`'s synthesis of three viable approaches (fine-tune, rule-based, hybrid) is the most lucid engineering analysis in the OSS space.

### Key open-source projects

- **`martiansideofthemoon/ai-detection-paraphrases` / `google-research/dipper`** — reference DIPPER implementation.
- **`blader/humanizer`** (~14.5k★) — the dominant Claude Code skill; MIT; Wikipedia-*Signs-of-AI* foundation + voice calibration.
- **`itsjwill/humanizer-x`** — 4-pass skill with explicit burstiness/perplexity framing and SSML disfluency for voice agents.
- **`PrithivirajDamodaran/Parrot_Paraphraser`** (~916★) — the T5 paraphrase framework most DIY humanizers wrap.
- **`ColinLu50/Evade-GPT-Detector`** (SICO, TMLR 2024) — in-context optimization; cheapest humanization recipe in the research tier.
- **`suraj-ranganath/StealthRL`**, **`zhouying20/HMGC`**, **`JamesLWang/RAFT`**, **`chengez/Adversarial-Paraphrasing`**, **`ffhibnese/CoPA_Contrastive_Paraphrase_Attacks`** — the active research attack repos.
- **`jfisher52/StyleRemix`** — interpretable per-axis LoRA style controls; AuthorMix + DiSC datasets.
- **`DrenfongWong/TH-Bench`** and **`xinleihe/MGTBench` / `Y-L-LIU/MGTBench-2.0`** — the scaffolding the field now runs on.
- **`sam-paech/antislop-sampler`** (~340★) — inference-time backtracking sampler with 8,000+ banned phrases; shipped into koboldcpp 1.76+ and open-webui.
- **`eth-sri/watermark-stealing`** — watermark scrubbing primitive; strategically important if watermarks roll out.
- **`voidborne-d/humanize-chinese`**, **`rithulkamesh/humanize`** — rule-based non-LLM transforms; the "actually different statistics" approach.
- **`ksanyok/TextHumanize`** — dual-licensed (free non-commercial + paid commercial), 25 languages, claimed 38-stage pipeline.
- **`mbodkebiz/slop-humanizer`**, **`Aboudjem/humanizer-skill`**, **`brandonwise/humanizer`**, **`hexiecs/talk-normal`**, **`adenaufal/anti-slop-writing`** — the skill-pack long tail.

### Notable commercial tools

- **Undetectable.ai** (`/v2`, `/v11`, `/v11sr`, $9.99–$49.99/mo, 86% avg detection reduction claim) — market incumbent; everyone positions against it.
- **WriteHuman** ($29/$69, `POST /v1/humanize`, "Best of 3" scored outputs, 40+ languages) — cleanest developer API shape.
- **StealthGPT** ($0.20–$2.00/1K words, `/api/stealthify`, HS→PhD tone ladder) — student-facing flavor.
- **AI Humanizer API** (free/$29/$99/custom, SOC 2, VPC, 99.99% SLA) — cleanest enterprise pricing grid with SSE streaming + batch.
- **Humaniser** (privacy-first, zero retention, JS+Python SDKs, $19/mo) — only mainstream vendor leading on trust rather than price.
- **Deceptioner** — per-detector profile as a first-class API parameter; unusually honest design.
- **Apify AI Text Humanizer** ($0.003/text, <500 ms, deterministic 12-pass, no LLM) — closest thing to "OSS rules engine as managed service"; the price-floor outlier.
- **HumanizerPro** ($37–$1,100+/mo, humanize + detect + plagiarism bundle) — agency-bundle pattern.

### Notable community threads

- **r/LocalLLaMA** — `sam-paech/antislop-sampler` announcement + [llama.cpp SLOP Removal #9699](https://github.com/ggml-org/llama.cpp/discussions/9699). The "intercept at the token level" wing.
- **`blader/humanizer` issue #82** (with referenced #55, #78) — engineering-critique locus.
- **r/BypassAiDetect "What AI humanizer is actually working in 2026"** — structural rewriters win (Walter Writes, Aurawrite), pure paraphrasers lose (QuillBot); OSS repos not mentioned.
- **HN 46694489** (`blader/humanizer`) — sole comment: *"I think we also need a /dehumanizer skill"* — the hostile-framing signal.
- **HN 46106966** ("Ask HN: in-browser humanizer?") — *"Machines pretending to be human speaking to machines that pretend to ignore the fact they've guessed they're speaking to a machine?"* — the normative HN position.
- **HN 47357745 "Slop or not"** — crowdsourced 16k-pair benchmark; Reddit posts are easier to detect than HN content.

## Key Techniques & Patterns

- **Paragraph paraphrase** (DIPPER and descendants) — two knobs (lexical diversity, content reordering) find the minimum edit to flip a detector. Reference attack in every paper.
- **Word-level grammar-preserving perturbation** (RAFT, Shi et al.) — greedy token substitution via auxiliary embedding; black-box; keeps text error-free.
- **Detector-in-the-loop RL** (AuthorMist, StealthRL, HUMPA) — GRPO/PPO against a joint detector loss; **API-as-reward** has become standard since AuthorMist (early 2025).
- **Decoding-time guidance** (SICO, CoPA, HUMPA proxy) — in-context optimization or contrastive decoding that produces human-looking text at generation time; no paraphrase post-hoc.
- **Gradient-based evasion** (GradEscape) — weighted embeddings over discrete tokens; handles tokenizer mismatches via model extraction.
- **Interpretable per-axis LoRA modules** (StyleRemix) — formality, length, function-word use, grade level, sarcasm, voice composed at inference. Planning-friendly.
- **Pattern stripping + voice injection + statistical manipulation + verification** (the practitioner 4-pass canon) — `humanizer-x`, `slop-humanizer`, StealthHumanizer ninja mode, `/v1/humanize` intensity ladders.
- **Skill/prompt packaging cascade** — `SKILL.md` → `AGENTS.md` → `.cursor/rules/*.mdc` → `.github/copilot-instructions.md` → `GEMINI.md`. Same prompt, per-host envelope. Documented by `adenaufal/anti-slop-writing` and `blader/humanizer`.
- **Voice calibration from writing samples** — paste 2–3 paragraphs, extract style profile, rewrite against it. First-class in `blader/humanizer`; corpus-grounded version in `dannwaneri/voice-humanizer`.
- **Inference-time backtracking sampler** (`antislop-sampler`) — retries tokens when output matches any of 8,000+ banned phrases; requires raw logits; shipped in koboldcpp and open-webui.
- **Rule-based non-LLM transforms** (`voidborne-d/humanize-chinese`, Apify) — the only approach that produces genuinely non-LLM statistics; per-language scaling cost.
- **Watermark scrubbing via query-based rule recovery** (`eth-sri/watermark-stealing`) — reverse-engineer green-list, paraphrase around watermarked tokens.
- **API conventions** — `POST /v1/humanize` with bearer auth; intensity ladder (light/medium/aggressive); tone ladder (HS→PhD or readability levels); 0–100 detection score in response; 1–7 s latency working band.
- **Post-generation CI regressions** (`brandonwise/humanizer`) — grep-style lint passes (`grep -iE "Certainly!|delve|It's important to note"`) in 153-test suite.

## Controversies & Debates

- **Can prompt-only humanization work at all?** `blader/humanizer` #82 and Peggy Kang argue no: the attacker and the source are the same distribution, so any LLM-sampled rewrite stays within the detector's trained manifold. Counter (`@greg-randall`): the goal is often "sounds human to readers," not "defeats Turnitin" — and for the reader-facing goal, pattern-stripping works. **Both are right about different goals**; the field hasn't cleanly separated them.
- **Fine-tune vs rule-based vs hybrid.** The #82 synthesis: fine-tuned humanizer models (Rephrasy, Walter Writes) are effective but expensive and fragile to detector retraining; rule-based is genuinely different statistics but has per-language cost; hybrid is the likely winner. No OSS project ships a credible fine-tuned humanizer.
- **Is "humanization" ethical at all?** HN consistently treats this as a problem ("machines pretending to be human"); Reddit and dev.to treat it as a how-to. SaaS reviewers add disclaimers; OSS READMEs mostly don't. GitHub/LinkedIn content policy is tightening.
- **Reader-facing "sounds human" vs detector-facing "evasion."** The same repo often claims both; they're increasingly understood as different technical problems with different metrics. TH-Bench measures evasion only; no public benchmark measures "humanness" against human preference rankings.
- **Are detector bypass-rate claims trustworthy?** Almost every OSS README ("60–90% reduction," "99.8% bypass," "<10% AI detection") self-reports against unnamed detector versions. Only the research tier (DIPPER, StealthRL, HUMPA, GradEscape, TH-Bench) ships reproducible numbers. Commercial reviewers are heavily self-interested. **Treat any bypass-rate number not from an independent academic test as marketing.**
- **Detector convergence: cat-and-mouse or general problem?** Multiple 2025 papers (Adversarial Paraphrasing, StealthRL) report attacks transfer to unseen detectors, implying detectors share a human-text manifold and humanization is a general problem rather than per-detector. Defenders dispute this on calibrated production detectors.
- **Statistical fingerprint (perplexity/burstiness) as a real mechanism or marketing.** Every practitioner repo invokes them; most implementations only affect them indirectly via synonym swap + sentence length shuffling. The research tier rarely measures them directly — they're not load-bearing in modern detectors.
- **The naming collision problem.** `Humanizr/Humanizer` (.NET) and `jehna/humanify` (JS deobfuscation) are constantly confused with AI-text humanizers. Multiple listicles conflate them.

## Emerging Trends

- **Small models winning on signal quality.** GradEscape (139M) and AuthorMist (3B) outperform DIPPER (11B). The frontier moved from scale to training-loop signal.
- **API-as-reward has replaced surrogate-detector-as-reward.** Since AuthorMist, treating GPTZero/WinstonAI/Originality.ai as opaque reward functions is standard — sidesteps gradient access and aligns training with production surface.
- **Transferability theorem is empirical now.** Attacks trained on one detector family beat unseen detectors; implies humanization is tractable as a general problem. Strongest argument against per-detector cat-and-mouse framing.
- **Skill-file consolidation.** OSS humanization shifted from "paste this prompt" to installable artifacts (Claude `.skill`, OpenCode skill, Cursor `.mdc`, `AGENTS.md`). `blader/humanizer`'s 14k stars suggests this format crossed the chasm.
- **Two-layer architecture winning.** Generation (clarity/correctness) split from post-processing (distribution/flow). Explicit in Kang's piece, implicit in every 4-pass repo. Prompt-only humanization is being quietly conceded as weakest.
- **Rule-based + hybrid gaining as the credible alternative.** `voidborne-d/humanize-chinese`, `rithulkamesh/humanize`, Apify's 12-pass deterministic pipeline. Expect more language-specific rule-based forks.
- **Sampler-level humanization stabilizing in LocalLLaMA.** `antislop-sampler` is treated as the "correct" layer to solve the problem when you control the model. Won't cross into Claude Code / SaaS because it requires raw logits.
- **Commercial-OSS shells wrapping paid APIs.** `humanizerai/agent-skills` and similar publish thin OSS façades around $19.99–$49.99/mo server-side humanizer APIs. Expect more of this — OSS as distribution channel, not source of truth.
- **Privacy-first positioning as a credible SaaS niche.** Only Humaniser leads with zero retention. OSS has this as a default — a named-OSS-library-backed commercial product with zero-retention promise could undercut Undetectable.ai on trust.
- **Market-positioning copy convergence.** Every launch now says: "tried existing humanizers, my method goes beyond synonym swaps, restructures sentences, adjusts cadence." Verbatim across HN, Indie Hackers, dev.to.

## Open Questions / Research Gaps

1. **No open "production-grade" humanizer.** Commercial Undetectable.ai / WriteHuman / Originality are closed; research repos are demos. A well-engineered OSS humanizer combining StealthRL's training recipe + StyleRemix's per-axis knobs + TH-Bench-scored eval is an empty niche.
2. **No repo ships a reproducible multi-detector eval harness.** DIPPER and RAFT have them in papers; no practitioner humanizer measures itself against GPTZero + Originality + Turnitin + Pangram + Binoculars + Raidar on public corpora. This is the #1 differentiation opportunity.
3. **No standard "humanness" benchmark.** TH-Bench measures evasion, not humanness. A benchmark whose ground truth is human preference rankings — a cleaner training signal than API reward — is missing.
4. **Stylometry-preservation + AI-stylometry-removal are never combined.** Anonymouth (2021) and ALISON (2024) address authorial stylometry; humanizer repos address AI-vs-human stylometry. Nobody has shipped "preserve my voice while destroying the model's voice." Most obvious untouched niche.
5. **Voice calibration is advertised but barely implemented.** Under the hood most "voice modes" reduce to 3–5 prompt presets. No repo ingests a user's corpus and fits a persistent per-user profile (vector or JSON style card reused across rewrites).
6. **Watermark-aware humanization absent.** None of the Tier A/B skill repos reference SynthID, OpenAI watermark research, or Stanford undetectable watermarks. `eth-sri/watermark-stealing` lives in a separate world. When watermarking ships, current humanizers obsolete overnight.
7. **No first-class diff-with-rationale output.** Users get rewritten text with no auditable explanation. Academic users who need defensibility would pay for this.
8. **Multilingual evaluation is absent.** `ksanyok/TextHumanize` claims 25 languages, `RAW.AI` claims 50+; public detectors are English-biased, so non-English "bypass" is trivial for reasons unrelated to humanization quality. Honest multilingual humanizer testing is open territory.
9. **Defense-aware humanization.** Most attacks evaluated against static detectors. Adaptive/active defenses (Raidar, retrained Binoculars) are where the 2026 arms race will move; almost nothing targets them.
10. **Domain-conditioned humanizers.** All OSS repos are domain-general. Student essays, SEO blog posts, LinkedIn posts, academic writing, customer-support replies, and fiction have different "human" signatures. Domain presets barely exist.
11. **Fine-tuned OSS humanizer checkpoint.** No HF model card, no training set, no LoRA recipe for a "humanizer fine-tune" that competes with closed SaaS. Claimed by paid services (Rephrasy, Walter Writes) but not shipped OSS.
12. **Honest quality reporting.** "12-metric detection engine," "60–90% detection reduction" are README marketing. An OSS project shipping negative results and reproducible methodology would differentiate immediately.

## How This Category Fits in the Bigger Picture

This category is the **implementation substrate** of the humanization research program. Other categories (detection, prompt engineering, RL fine-tuning, watermarking, stylometry) produce techniques; this category tracks which of those techniques have running code, where adoption lives, and what the cost/quality/effort trade-offs look like in practice.

Three positioning implications for Unslop:

- **The research tier is the technique source; the skill tier is the UX reference.** Lean on DIPPER + SICO + StealthRL + StyleRemix for the mechanism stack; lean on `blader/humanizer` and the 4-pass skill pipeline for what users actually expect to see in an interface.
- **The empty niche is the bridge between them.** Nobody has shipped a production-grade OSS humanizer that (a) uses research-tier mechanisms, (b) runs TH-Bench / MGTBench-2.0 as a standing eval, (c) offers StyleRemix-style interpretable knobs in the UX, and (d) preserves authorial voice while destroying AI signals. That bridge is the unique position.
- **Commercial pricing ($0.17–$2.00 per 1K words) and rules-engine pricing ($0.003) bracket the cost model.** Any OSS project with honest eval, interpretable controls, and a credible self-host story can undercut the top of the commercial band on trust while sitting above the rules-engine floor on quality.

This category should also inform the categories on detection (detector transferability findings from StealthRL / Adversarial Paraphrasing directly constrain what detection can ever achieve), watermarking (`eth-sri/watermark-stealing` is the existential threat to any humanizer that ignores watermarks), and evaluation methodology (TH-Bench is the scaffolding the rest of the field should adopt).

## Recommended Reading Order

1. **A-academic.md** — grounds the mechanism space. Without this, every skill-pack README reads as magic.
2. **C-opensource.md** — the concrete inventory: what exists, who's maintaining it, what actually works.
3. **E-practical.md** — the engineering critique (Kang, issue #82) and the reality of how the community talks about this. The intellectual center of the category.
4. **D-commercial.md** — pricing, API conventions, and the "library as managed service" gap.
5. **B-industry.md** — listicle/tutorial coverage; mostly signal about what the market misses rather than what it delivers.

If short on time: read `blader/humanizer` issue #82 + Peggy Kang's dev.to piece + the TH-Bench paper + the DIPPER abstract. That's 80% of the intellectual content of the category.

## File Index

| File | Angle | Research value | Focus |
|---|---|---|---|
| [A-academic.md](./A-academic.md) | Academic / research-grade OSS | High | ~18 peer-reviewed humanizer repos (DIPPER, HMGC, HUMPA, StealthRL, AuthorMist, GradEscape, SICO, RAFT, CoPA, StyleRemix, TH-Bench, MGTBench). Mechanism lineage and benchmarks. |
| [B-industry.md](./B-industry.md) | Industry / blog coverage | Moderate | Listicles, curated lists (`Brandon689`, `ToolkitlyAI`), tutorials (HF Pegasus/T5, AI/ML API), critical reviews (`thehumanizeai.pro`), Claude-specific skill coverage. Signal: what the market misses. |
| [C-opensource.md](./C-opensource.md) | Core OSS catalog | High | The ~35-repo inventory tiered A/B/C/D by activity + substance. `blader/humanizer`, `Parrot_Paraphraser`, `TextHumanize`, `humanizer-x`, research-tier repos, detector-specific scripts. |
| [D-commercial.md](./D-commercial.md) | Commercial SaaS + self-hostable APIs | High | Undetectable.ai, WriteHuman, StealthGPT, HumanizerAI, HumanizerPro, AI Humanizer API, Humaniser, Apify, Deceptioner, BypassGPT, Humbot, Phrasly. Pricing, API conventions, OSS alternatives. |
| [E-practical.md](./E-practical.md) | Practical / forums / engineering critique | High | Reddit (r/LocalLLaMA, r/BypassAiDetect, r/SEO), HN threads, dev.to tutorials, `blader/humanizer` issue #82, `antislop-sampler`, rule-based vs prompt-based debate. |
