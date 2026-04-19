# Category 05 — AI Text Detection & Evasion

## Scope

Research synthesis across five angles — academic literature, industry/press commentary, open-source code, commercial products, and practitioner how-tos/forums — covering the systems built to distinguish AI-generated text from human writing, the watermarking schemes designed to make generation self-identifying, and the humanization/evasion techniques that defeat both. The category defines the adversarial surface the Unslop product operates on: every detector is a target to measure against, every watermark is a constraint to respect or bypass, and every documented evasion technique is either prior art to absorb or a failure mode to avoid repeating.

## Executive Summary

- **Clean-domain detection is solved; out-of-distribution detection is not.** Fast-DetectGPT, Binoculars, Ghostbuster and RAIDAR all report AUROC ≥0.99 on same-domain benchmarks, but M4, MGTBench, and RAID show sharp cross-domain / cross-generator drops, consistently as *false negatives*. Vendor-claimed 97–99% accuracy lands at 68–91% in independent testing (Scribbr, RAID, Bloomberg, Axis).
- **Paraphrase is the universal solvent.** DIPPER (Krishna NeurIPS 2023) alone drops DetectGPT from 70.3% → 4.6% accuracy at 1% FPR. Recursive paraphrasing (Sadasivan), RADAR-style adversarial paraphrasers, StealthRL (RL-optimized, transfers to held-out detectors), and second-pass LLM rewording all follow the same pattern. OpenAI itself conceded its 99.9% watermark is "trivial to circumvention" by rewording with another model — which is exactly what a humanizer is.
- **Watermarks are the strategic frontier and they keep losing.** SynthID-Text (Google, *Nature* 2024) is the one at-scale deployed scheme; Kirchenbauer green-list is the academic reference. Both degrade under paraphrase, and Jovanović's watermark-stealing attack scrubs/spoofs for under $50 at ~80% success. Christ–Gunn–Zamir's cryptographic "undetectable watermarks" provide a theoretical counter to Sadasivan's impossibility result, but have not been robustness-validated at scale.
- **Detectors fail asymmetrically — and the bias story is the defensible wedge.** Liang et al. (*Patterns* 2023) showed >50% of TOEFL essays misclassified as AI; Bloomberg documented named students falsely flagged; Vanderbilt, UT Austin, Northwestern disabled Turnitin's detector. Every 2024–26 mainstream piece frames this as a civil-rights/equity issue, giving humanizer products a legitimate positioning — "protection from a demonstrably biased system" — rather than pure cheating-assistance.
- **The industry has converged on a shared three-signal target.** Perplexity (token-level predictability), burstiness (sentence-length variance), and stylometric fingerprint (model-family signatures per Copyleaks). Serious humanizers must touch all three; products that only rewrite vocabulary lose to ensemble detectors.
- **Retraining cadence is ~30 days; static humanizers decay.** Originality ships Lite/Turbo/Academic refreshes every 1–3 months with explicit humanizer-resistance targets. GPTZero maintains a "greylist" of bypass methods patched within days. A shipped humanizer has a month-scale half-life on any single strategy.
- **Humanizers have split into two castes with an obvious arbitrage.** Academic caste (DIPPER, StealthRL, RADAR) trains or RL-optimizes against detector ensembles. Practitioner caste (humanizer-x, Mohit1053/Humanizer, ADEMOLA200/Humanize-AI, most SaaS) is almost entirely prompt-engineering on Llama3-8B / T5 / PEGASUS. Nobody in the commercial space ships an ensemble-trained, self-calibrating paraphrase policy.
- **Grammarly's "Authorship" pivot signals structural weakening on the detection side.** By rebranding from detector to keystroke-based provenance tool, Grammarly conceded classifier-based detection is a losing long-term bet — the clearest market signal yet.

## Cross-Angle Themes

**1. The three-signal consensus.** Every angle independently converges on perplexity + burstiness + stylometric fingerprint as the detection target. Academic (DetectGPT curvature, Binoculars ratio, Tulchinskii manifold dim), industry (GPTZero's canonical explainer, Copyleaks' "three investigators"), open-source (humanizer-x "addresses all three"), commercial (every detector layers them), and practitioner threads (Narejo, Insights4UToday, thehumanizeai.pro) all name the same axes.

**2. Paraphrase dominates over character-level tricks.** SilverSpeak homoglyphs drop MCC from 0.64 → −0.01 *today*, but `lm-watermarking` ships a `normalizers.py` that strips them, and GPTZero patched Cyrillic substitution within days. Paraphrase-based evasion (DIPPER, recursive paraphrasing, StealthRL, multi-model routing, second-pass LLM) is the only attack that has survived two detector generations.

**3. The ESL/equity narrative crosses every tier.** Liang (academic), Bloomberg/MIT TR/Inside Higher Ed (press), Turnitin's October 2025 "non-native speaker protections" (vendor), and HN/Reddit FP discourse (practitioner) all center the same finding. The transformation that evades detection is also the transformation that removes unfair bias — a rare case where the attack and the defense of the attack are the same prompt.

**4. Benchmarking is maturing and attack-inclusive.** RAID (10M docs, 11 LLMs, 12 attacks), MGTBench 2.0 (16 academic domains), M4 (multi-lingual) are the new standard. "Did you evaluate on RAID with adversarial splits?" is the first reviewer question. Humanizer claims like "<10% on GPTZero" are not comparable to academic TPR@1%FPR numbers — a shared eval harness does not yet exist.

**5. Watermark stealing is empirically tractable.** Jovanović ($50, 80% success) + MIT Tech Review coverage + `XuandongZhao/WatermarkAttacker` show that watermark removal is adversarial ML, not prompt engineering. This is the research program that humanizer companies are the applied layer of.

**6. Commercial moats are collapsing into pricing, not technique.** Detectors converge on the same signal stack; humanizers converge on the same rewriting stack. Price bifurcates: free (Humanize AI Pro, ZeroGPT) / $10–20 consumer / $40–200 pro — with a thin $20–40 middle. Differentiation now lives in integrations, guarantees (AIHumanize "credit-back if detected"), and training-data provenance claims (Phrasly).

## Top Sources (Curated)

### Must-read papers

- **Mitchell et al., DetectGPT** — ICML 2023. Zero-shot via probability curvature; template for the whole generation. https://arxiv.org/abs/2301.11305
- **Bao et al., Fast-DetectGPT** — ICLR 2024. 340× speedup; production-deployable zero-shot. https://arxiv.org/abs/2310.05130
- **Hans et al., Binoculars** — ICML 2024. Observer/performer LLM ratio; strongest training-free detector. https://arxiv.org/abs/2401.12070
- **Verma et al., Ghostbuster** — NAACL 2024. Weak-model feature search, black-box compatible. https://aclanthology.org/2024.naacl-long.95/
- **Kirchenbauer et al., A Watermark for LLMs** — ICML 2023 (Outstanding Paper). The green-list/red-list reference. https://arxiv.org/abs/2301.10226
- **Dathathri et al., SynthID-Text** — *Nature* 2024. First at-scale watermark deployment (20M Gemini responses). https://www.nature.com/articles/s41586-024-08025-4
- **Christ, Gunn, Zamir, Undetectable Watermarks** — COLT 2024. Cryptographic undetectability. https://arxiv.org/abs/2306.09194
- **Sadasivan et al., Can AI-Generated Text Be Reliably Detected?** — arXiv 2303.11156. TV-distance impossibility bound. https://arxiv.org/abs/2303.11156
- **Chakraborty et al., Position: Possibilities of AI-Generated Text Detection** — ICML 2024. Sample-complexity possibility counter. https://arxiv.org/abs/2304.04736
- **Krishna et al., DIPPER** — NeurIPS 2023. Canonical paraphrase attack; drops DetectGPT 70.3% → 4.6%. https://arxiv.org/abs/2303.13408
- **Hu, Chen, Ho, RADAR** — NeurIPS 2023. GAN-style adversarial detector training. https://arxiv.org/abs/2307.03838
- **Jovanović, Staab, Vechev, Watermark Stealing** — ICML 2024. $50 / 80% spoof+scrub attack. https://arxiv.org/abs/2402.19361
- **Mao et al., RAIDAR** — ICLR 2024. Detect-by-rewriting behavioral probe. https://arxiv.org/abs/2401.12970
- **Liang et al., GPT Detectors Biased Against Non-Native English Writers** — *Patterns* 2023. Load-bearing equity result. https://arxiv.org/abs/2304.02819
- **Tulchinskii et al., Intrinsic Dimension Detection** — NeurIPS 2023. Manifold-geometry probe. https://arxiv.org/abs/2306.04723
- **Wang et al., M4** — EACL 2024 Best Resource. Multi-lingual/generator/domain benchmark. https://arxiv.org/abs/2305.14902
- **Creo & Pudasaini, SilverSpeak** — arXiv 2406.11239. Homoglyphs drop seven detectors to MCC ≈ 0. https://arxiv.org/abs/2406.11239
- **Dugan et al., RAID** — ACL 2024. 10M docs × 11 LLMs × 12 attacks; the de facto evaluation harness. https://raid-bench.xyz

### Must-read posts/essays

- **OpenAI, "New AI classifier for indicating AI-written text"** — the retraction post itself is the strongest baseline citation. https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text
- **Wes Davis, The Verge, "OpenAI won't watermark ChatGPT text because its users could get caught"** (Aug 2024). OpenAI publicly concedes a second-pass LLM defeats their 99.9% watermark. https://www.theverge.com/2024/8/4/24213268/openai-chatgpt-text-watermark-cheat-detection-tool
- **Melissa Heikkilä, MIT Tech Review, "It's easy to tamper with watermarks from AI-generated text"** (Mar 2024). Mainstream framing of Jovanović. https://www.technologyreview.com/2024/03/29/1090310/
- **Melissa Heikkilä, MIT Tech Review, "Why detecting AI-generated text is so difficult"** (Feb 2023). The canonical "arms race" frame. https://www.technologyreview.com/2023/02/07/1067928/
- **Bloomberg, "Do AI Detectors Work? Students Face False Cheating Accusations"** (Oct 2024). Named-victim anchor citation. https://www.bloomberg.com/news/features/2024-10-18/do-ai-detectors-work-students-face-false-cheating-accusations
- **Inside Higher Ed, "Professors proceed with caution using AI-detection tools"** (Feb 2024). Elite universities exiting. https://www.insidehighered.com/news/tech-innovation/artificial-intelligence/2024/02/09/professors-proceed-caution-using-ai
- **GPTZero, Edward Tian, "What is perplexity & burstiness?"** The canonical industry explainer. https://gptzero.me/news/perplexity-and-burstiness-what-is-it/
- **Google DeepMind, "Watermarking AI-generated text and video with SynthID"** (May 2024). https://deepmind.google/discover/blog/watermarking-ai-generated-text-and-video-with-synthid/
- **Ahrefs, "AI-Generated Content Does Not Hurt Your Google Rankings"** (600K pages). Defangs the SEO fear. https://ahrefs.com/blog/ai-generated-content-does-not-hurt-your-google-rankings/
- **Grammarly, "From AI Detection to Authorship"** — the first major detector-side concession. Included in Grammarly Premium.
- **Asifa Narejo, Medium, "I Tested 50+ Prompts to Beat AI Detectors"** (Jan 2026). Only widely-cited piece with reproducible prompts × detector scores. https://medium.com/@asifanarejo/i-tested-50-prompts-to-beat-ai-detectors-only-these-3-actually-worked-bc6273fe4fdc

### Key open-source projects

**Detectors**
- `baoguangsheng/fast-detect-gpt` — Fast-DetectGPT reference; use Llama3-8B scoring models (2026 update).
- `ahans30/Binoculars` — Drop-in zero-shot detector, `Binoculars().predict(text)`.
- `vivek3141/ghostbuster` — Weak-model feature search; README explicitly documents humanizer failure mode.
- `Mamba413/AdaDetectGPT` — NeurIPS 2025 adaptive extension with formal FPR guarantees.

**Watermarks**
- `jwkirchenbauer/lm-watermarking` — KGW reference (`gamma=0.25`, `delta=2.0`, `h=4`, `selfhash`); ships `normalizers.py`/`homoglyphs.py`.
- `google-deepmind/synthid-text` — SynthID-Text reference (production lives in HF Transformers).
- `THU-BPM/Robust_Watermark` — Paraphrase-robust SIR watermark.

**Attacks / evasion**
- `martiansideofthemoon/ai-detection-paraphrases` + `kalpeshk2011/dipper-paraphraser-xxl` — DIPPER 11B, two-knob lexical/order diversity control.
- `suraj-ranganath/StealthRL` — RL-optimized paraphraser, GRPO + LoRA on Qwen3-4B; transfers to held-out detectors. M0–M5 attack taxonomy.
- `ACMCMC/silverspeak` — Homoglyph library + its own *reversal* utilities.
- `XuandongZhao/WatermarkAttacker` — Regeneration attack template.

**Benchmarks**
- `liamdugan/raid` — `pip install raid-bench`; 10M docs × 12 attacks; open leaderboard.
- `xinleihe/MGTBench` and `Y-L-LIU/MGTBench-2.0` — 16 academic domains.
- `Xianjun-Yang/Awesome_papers_on_LLMs_detection` — best single literature entry point.

**Humanizers (practitioner)**
- `itsjwill/humanizer-x` — 4-pass prompt taxonomy (pattern removal → voice → statistical tuning → verification); severity-ranked 30-tell catalog.
- `Mohit1053/Humanizer` — Ollama/Llama3-8B reference implementation.
- `ADEMOLA200/Humanize-AI`, `vardhin/Humanizer`, `fatimaazfar/Pegasus-Paraphraser`, `tuner007/pegasus_paraphrase` — API-shaped / T5 / PEGASUS references.

### Notable commercial tools

**Detectors**
- **GPTZero** — perplexity+burstiness canonical; educator brand; ~$20M ARR; claimed 99.3%/0.24% FP.
- **Originality.ai** — the detector humanizers most consistently fail against; monthly retraining (Lite/Turbo/Academic cadence); humanizer-aware training corpus.
- **Copyleaks** — multilingual + "three investigators" ensemble; 99.88% model-attribution claim; explicit anti-humanizer marketing.
- **Turnitin** — institutional default in 10,700+ institutions; October 2025 rebuild softened verdicts to "conversation starters"; scores 1–19% hidden by default.
- **Winston AI** — "99.98%" headline but 71% at 5% FP on RAID; bundles image/OCR.
- **Sapling, ZeroGPT, Writer.com detector** — secondary.
- **Grammarly Authorship** — the strategic pivot: provenance via keystroke tracking, not classification.

**Humanizers**
- **Undetectable.ai** — 15M+ users (Feb 2025, Reuters); 96% bypass against GPTZero in 2026 head-to-heads; category leader.
- **Phrasly** — claims proprietary models trained on 1M+ pages; only tool marketing on training-data provenance.
- **HIX Bypass** — "Latest" mode explicitly tuned against Originality 3.0 and newest Turnitin.
- **Humanize AI Pro** — free/unlimited; disrupts the consumer band.
- **StealthGPT** — fails against Originality (35% flagged) despite "Samurai Engine" branding.
- **Surfer AI Humanizer** — only tool explicitly positioned for SEO, not cheating; custom voice training.
- **AIHumanize** — money-back-if-detected guarantee; 1.28B words/mo.
- **BypassGPT, WriteHuman, Humbot** — mid-tier.

### Notable community threads

- **HN #36182912** — "You can literally ask ChatGPT to evade AI detectors" (Jun 2023).
- **HN #35535174** — "Teacher failed kid for essay because AI-detection tool flagged his work" (Apr 2023).
- **r/ApplyingToCollege** — "I reviewed 100 essays. Here's how I could tell which were ChatGPT" (gwern mirror). The canonical 7-tells list: *delve/tapestry*, extended metaphors (weaving/cooking/painting/dance), em-dash curly/straight mismatches, ascending tricolons, "not only Y, it's also Z," "As I [advance] I will [carry] this [lesson]," LOTR multi-endings.
- **OpenAI Developer Community, "GPTZero bypasser Program"** — canonical character-substitution prior art, patched Feb 2, 2023.
- **r/BypassAiDetect, r/BestAIHumanizer_, r/college, r/teachers, r/SEO, r/copywriting** — ongoing community leaderboards.
- **BlackHatWorld, "Prompt to beat GPTZero… to rank in Google"** — SEO-affiliate subculture; $50 bounty threads.
- **Cristina Cabal teacher blog, "Tyranny of Triplets"** — teacher-side mirror of the 7-tells list.

## Key Techniques & Patterns

### Detectors (named families)

**Statistical / likelihood-ratio (zero-shot, training-free)**
- *DetectGPT* — probability-curvature (mask-fill perturbations).
- *Fast-DetectGPT* — conditional curvature, 340× faster.
- *Binoculars* — ratio of base-model perplexity to instruct-sibling cross-perplexity.
- *GLTR* — per-token rank visualization (legacy).
- *Log-likelihood, Log-Rank, Entropy, LRR, NPR* — MGTBench baselines.

**Feature-based / weak-model probes**
- *Ghostbuster* — structured search over multiple weak-LM feature combinations; black-box compatible.
- *RAIDAR* — rewrite-and-measure-edit-distance behavioral probe.
- *Tulchinskii intrinsic-dimension* — manifold geometry of contextual embeddings.

**Fine-tuned classifiers**
- *OpenAI RoBERTa detector* (retracted 2023), *Ghostbuster* linear head, *Copyleaks "AI Logic" three-investigator ensemble*, *Originality Turbo/Lite/Academic*, *Winston HUMN-1*, *GPTZero* layered stack, *Turnitin* proprietary academic-corpus classifier.

**Retrieval / provenance**
- Krishna et al.'s provider-side retrieval (store-and-check).
- *Grammarly Authorship* — keystroke/paste tracking (not classification).

### Watermarks

- *Kirchenbauer green-list/red-list (KGW)* — soft logit biasing, z-test detection. Default `gamma=0.25, delta=2.0, h=4, selfhash`.
- *Aaronson Gumbel-max* (OpenAI talk, unshipped) — cryptographic sampling with `argmax log P − log U`.
- *SynthID-Text (Google)* — tournament-style probability modulation; composable with speculative sampling; shipped in Gemini.
- *Christ–Gunn–Zamir* — undetectable cryptographic watermarks (one-way-function assumption).
- *THU-BPM SIR* — semantic-invariant robust watermark.

### Evasion strategies (ranked by survivability)

1. **Paraphrase (neural)** — DIPPER (lexical-diversity + order-diversity knobs), RADAR-style GAN paraphraser, recursive paraphrasing, StealthRL (RL vs ensemble, transfers). *Primary tool; survives two detector generations.*
2. **Second-pass LLM rewording** — OpenAI concedes this defeats their 99.9% watermark. The architectural primitive of consumer humanizers.
3. **Multi-model / "hybrid" routing** — outline in GPT-5 → flow through Claude → facts through Grok; breaks per-model stylometric fingerprints.
4. **Statistical tuning** — deliberate burstiness injection (short/long sentence alternation), controlled perplexity via uncommon word choices, contractions 70–80%, conjunction-initial sentences, rhetorical questions with self-answers, parenthetical asides, backtracking phrases, one-sentence fragments.
5. **Anti-tell prompt rules** — strip *delve, utilize, leverage, harness, streamline, fundamentally, arguably*; avoid tricolons, extended metaphors, "not only Y, it's also Z," LOTR multi-endings.
6. **Persona framing + sensory/POV injection** — "tired 28-year-old copywriter on third espresso"; first-person specificity; real anecdotes.
7. **Watermark stealing (Jovanović)** — reverse-engineer green-list via API queries; then spoof or scrub.
8. **Homoglyph / whitespace / Unicode tricks** — effective *today* (SilverSpeak MCC 0.64→−0.01) but trivially reversed; patched within days by major detectors.

### Humanizer pipeline patterns (commercial convergence)

1. Sentence-structure reshuffling.
2. Vocabulary substitution.
3. Burstiness injection.
4. Tone/persona modes (University / Journalist / Marketing / High School / Doctorate).
5. Built-in pre-check dashboard running 6–7 detectors (Undetectable.ai, Phrasly, BypassGPT, HIX, AIHumanize all ship this).

## Controversies & Debates

**False positives and civil harm.** Liang's TOEFL result (61% of non-native essays misclassified) is load-bearing across academic, press, and institutional literature. Bloomberg names individual students falsely accused. Vanderbilt, UT Austin, Northwestern have disabled Turnitin's detector. OpenAI's classifier was retracted specifically because 9% FP on human text was unacceptable. Originality has a rebuttal blog up but the narrative has won at the institutional level.

**Impossibility vs possibility.** Sadasivan's TV-distance bound (detection collapses to chance as models approach human text) vs. Chakraborty's sample-complexity result (detection is consistently feasible given enough tokens *and* separable support) are the two poles. Both are correct — they describe opposite ends of the same curve. Christ–Gunn–Zamir shows cryptographic watermarks can exist without quality loss, but their robustness under editing is not empirically validated at scale.

**Vendor claims vs independent benchmarks.** Every vendor clusters at 97–99%; independent testing lands at 68–91%. Turnitin claims <1% FP vs Bloomberg's 1–2% on bulk essays and Stanford's 61% on ESL. Winston's "99.98%" lands at 71% on RAID. Sapling's "97%+" lands at 90% FP in one peer-reviewed study. Scribbr's rank order and RAID are the only widely-accepted independent benchmarks.

**Watermark ethics.** OpenAI built a 99.9% watermark and shelved it because ~30% of ChatGPT users said they'd use it less if watermarked. Google DeepMind shipped SynthID as "a building block," not a solution. The industry is not converging on provenance as a universal default, which leaves detector-only enforcement structurally incomplete.

**The unwinnable arms race.** Medium's "Arms Race Is Unwinnable," MIT TR's "Why Detecting Is So Difficult," and Originality's own 30-day retrain cadence describe the same structural instability: detectors claim 98%, independent tests land at 70–80%, humanizers update, detectors retrain, cycle repeats weekly. Grammarly's pivot to Authorship is the first major vendor to concede the game.

**Ethics of the humanizer category itself.** BlackHatWorld's SEO-affiliate culture, r/BypassAiDetect, and Reuters-reported 15M Undetectable.ai users coexist with institutional honor-code violations and equity-framed "protect ESL writers" narratives. Every angle notes this tension; no angle resolves it.

## Emerging Trends

- **Behavioral / structural probes replace logit-access probes.** RAIDAR (rewrite edit-distance), Binoculars (two-model contrast), Tulchinskii (manifold dimension) all work on black-box APIs. A direct response to closed models and watermark stealing.
- **RL-optimized, ensemble-trained evasion.** StealthRL's cross-detector transfer (trained on 4, beats 2 held-out) shifts evasion from "beat detector X" to "exploit family-level weakness."
- **Attack-inclusive benchmarks as the default.** RAID's 12-attack API and MGTBench 2.0's 16-domain coverage are the new bar. Peak in-domain AUROC is no longer a credible single metric.
- **Institutional exit.** Vanderbilt, UT Austin, Northwestern disabling Turnitin's detector; Turnitin itself softening to "conversation starters"; Grammarly pivoting to Authorship. Pressure is migrating from student-cheating to B2B content-QA.
- **Guarantee-as-marketing.** AIHumanize's credit-back-if-detected clause is the first explicit risk-transfer mechanism; expected to spread as technical differentiation narrows.
- **Multilingual gap widening.** Copyleaks reports English accuracy 93% vs 74–84% Chinese/Japanese/Arabic. No humanizer publishes non-English quality benchmarks despite all claiming 50+ languages.
- **Academic-domain specialization.** Originality launched Academic 0.0.5; no humanizer has launched a matched academic mode preserving citation integrity.
- **Monthly retraining cadence institutionalizing.** Originality ships model refreshes every 1–3 months; HIX Bypass advertises detector-version-specific tuning. Humanizer decay is now a product-lifecycle constraint, not a bug.

## Open Questions / Research Gaps

- **Quality-controlled humanization benchmarks don't exist.** The literature evaluates detection-reduction or paraphrase attack success; nothing measures semantic/stylistic distortion per bit of detection reduction. This is the specific gap a humanizer product lives in.
- **No public, dated, cross-detector × cross-prompt × cross-model benchmark.** Community leaderboards are vendor-run. RAID is a static corpus. A rolling benchmark would be the single highest-leverage content artifact.
- **Adaptive-adversary detector evaluation is rare.** Most detector papers test against DIPPER or GPT-3.5 paraphrase; few retrain against adaptively-optimized evaders. BIRA-style query-free optimization is not standard.
- **ESL-fairness as a reporting axis.** Liang is cited but rarely rerun on new detectors. Per-demographic confusion matrices are absent from vendor reporting.
- **Humanized hybrid content (50/50 human+AI).** Scribbr notes detectors return bimodal verdicts on hybrids — the most realistic use mode. Under-discussed in both vendor and academic literature.
- **SynthID-aware humanization is absent from the open humanizer ecosystem.** All public humanizers target GPTZero/ZeroGPT/Originality. SynthID is what's actually on Gemini output in the wild.
- **No trained-policy open humanizer since DIPPER (2023).** Distilling DIPPER into a smaller model, or RL-training Qwen/Llama against a modern detector ensemble à la StealthRL, is an unclaimed slot.
- **Retrieval-defense attacks are under-studied.** DIPPER's own paper argues retrieval is the strongest defense; few evasion papers attack stateful retrieval-based detection.
- **Cross-model stylometric blending.** Copyleaks' model-attribution claim suggests humanizers that only change surface tokens leave model-family syntax intact. Multi-model roundtripping as an evasion primitive is under-evaluated.
- **Score-variance / stability.** The most-cited user complaint on r/BypassAiDetect is score drift across reruns; no tool advertises variance bounds. A stable-across-reruns humanizer would be differentiated.
- **Practical robustness of cryptographic watermarks.** Christ–Gunn–Zamir shows undetectability in theory; editing-attack robustness has not been empirically validated at scale.

## How This Category Fits in the Bigger Picture

Category 05 defines the adversarial envelope the Unslop product operates inside. Every other research category in the project depends on assumptions that are either confirmed or bounded here:

- The **"AI tells"** taxonomy that drives rewriting-pass design (em-dashes, tricolons, *delve/tapestry*, rule-of-three, extended metaphors, LOTR multi-endings) is most precisely enumerated in the practitioner threads (r/ApplyingToCollege, Cristina Cabal) and codified in open-source prompt lists (humanizer-x, Mohit1053). Unslop's rewriting rules should inherit this taxonomy.
- The **target signals** (perplexity, burstiness, stylometric fingerprint) define what a humanizer must measurably move. Any humanization pass that does not move all three is category-weak.
- The **detector landscape** specifies the evaluation harness: Fast-DetectGPT (white-box-ish, Llama3-8B scoring), Binoculars (zero-shot black-box), Ghostbuster (weak-model probes), RAID (attack-inclusive benchmark), plus commercial GPTZero/Originality/Turnitin/Copyleaks/Winston for market credibility.
- The **ethical and positioning wedge** — ESL-bias protection, "gray-band" Turnitin suppression (1–19%), auditability as the positive counter-narrative — is the defensible framing that Category 05 uniquely supplies. Without it, the product is a cheating tool; with it, the product is protection from a demonstrably biased system.
- The **retraining cadence** (monthly on the detector side) sets a hard architectural constraint: Unslop cannot ship-and-forget; it needs continuous detector-panel evaluation and strategy refresh. This is a product-lifecycle requirement the other categories don't impose.
- The **watermark horizon** (SynthID in production, OpenAI's shelved 99.9% scheme, Christ–Gunn–Zamir's cryptographic possibility) defines a 12–24 month horizon where provenance, not detection, becomes the dominant enforcement mechanism. Unslop's long-term roadmap should assume watermark-resistance, not just classifier-evasion.

## Recommended Reading Order

**1. Orientation (30 min)**
- GPTZero, "What is perplexity & burstiness?" — canonical signal stack.
- MIT Tech Review, "Why detecting AI-generated text is so difficult" — arms-race frame.
- Liang et al., "GPT Detectors Are Biased Against Non-Native English Writers" — the equity anchor.

**2. Detector state of the art (60 min)**
- Mitchell et al., DetectGPT → Bao et al., Fast-DetectGPT → Hans et al., Binoculars → Verma et al., Ghostbuster → Mao et al., RAIDAR. This is the detector evolution arc.
- Wang et al., M4 and Dugan et al., RAID for how they're evaluated in 2024–26.

**3. Watermarking (45 min)**
- Kirchenbauer 2023 (green-list) → Kirchenbauer 2024 (reliability) → Dathathri 2024 (SynthID-Text in *Nature*) → Christ–Gunn–Zamir (COLT 2024).
- DeepMind SynthID blog + The Verge OpenAI-watermark-shelved article for the market reality.

**4. Evasion and impossibility (60 min)**
- Krishna et al., DIPPER (the attack everyone cites) → Sadasivan et al. (impossibility) → Chakraborty et al. (possibility counter) → Jovanović et al., Watermark Stealing → Creo & Pudasaini, SilverSpeak → StealthRL paper and repo.

**5. Market landscape (45 min)**
- Originality.ai "Year in Review 2025" (retraining cadence).
- Turnitin "October 2025 Updates" (vendor-side softening).
- Bloomberg "Do AI Detectors Work?" (consumer harm narrative).
- Scribbr and Ahrefs comparisons for consumer benchmarking norms.
- Grammarly "Authorship" (the strategic pivot).

**6. Practitioner playbook (45 min)**
- r/ApplyingToCollege 7-tells post (gwern mirror).
- Narejo Medium "50+ prompts tested" — reproducible prompts with scores.
- Insights4UToday YouTube + thehumanizeai.pro score tables.
- `itsjwill/humanizer-x` README — 4-pass taxonomy + 30-tell catalog.
- OpenAI community "GPTZero bypasser Program" for what doesn't work.

**7. Depth and gaps (as needed)**
- Tulchinskii intrinsic-dimension paper (structural probes).
- Aaronson Gumbel-watermark talk + Ruan refined detection.
- RAID benchmark attack catalog (`get_attack("homoglyph")`).
- MGTBench 2.0 for academic-domain breadth.

## File Index

- `A-academic.md` — 20 peer-reviewed / preprint papers covering detectors (DetectGPT → Fast-DetectGPT → Binoculars → Ghostbuster → RAIDAR → Tulchinskii), watermarks (Kirchenbauer, SynthID-Text, Christ–Gunn–Zamir, Aaronson), evasion (DIPPER, RADAR, Sadasivan, Jovanović, SilverSpeak), theory (Sadasivan vs Chakraborty), fairness (Liang), and benchmarks (M4, MGTBench). Venues: ICML, ICLR, NeurIPS, NAACL, EACL, COLT, *Nature*, *Patterns*.
- `B-industry.md` — ~20 vendor blogs and mainstream-press essays: OpenAI classifier retraction, GPTZero perplexity/burstiness explainers, Originality year-in-review + RAID + ESL-response posts, Copyleaks stylistic-fingerprint research, Turnitin launch + October 2025 softening, DeepMind SynthID post, The Verge watermark-shelved story, MIT Tech Review (×2), WIRED, Bloomberg, Inside Higher Ed, Scribbr, Ahrefs, Nerdbot/Seven Solvers humanizer reviews, and the Medium "unwinnable arms race" essay.
- `C-opensource.md` — ~25 GitHub repos and HF models: detectors (Fast-DetectGPT, DetectGPT, AdaDetectGPT, Binoculars, Ghostbuster, GLTR), watermarks (lm-watermarking, synthid-text, Robust_Watermark, WatermarkAttacker), attacks (DIPPER ×2, SilverSpeak, StealthRL), practitioner humanizers (humanizer-x, Mohit1053/Humanizer, ADEMOLA200/Humanize-AI, vardhin/Humanizer, fatimaazfar/Pegasus-Paraphraser, StealthHumanizer, tuner007/pegasus_paraphrase), and benchmarks (RAID, MGTBench v1/v2, Awesome_papers_on_LLMs_detection, datamllab/awsome-LLM-generated-text-detection).
- `D-commercial.md` — 18 products: 9 detectors (GPTZero, Originality.ai, Copyleaks, Turnitin, Winston AI, Sapling, ZeroGPT, Writer.com, Grammarly Authorship) and 9 humanizers (Undetectable.ai, Humanize AI Pro, StealthGPT, BypassGPT, Phrasly, HIX Bypass, Surfer AI Humanizer, WriteHuman, AIHumanize). Pricing, claimed vs measured performance, technique stack, and marketing framing for each.
- `E-practical.md` — 19 threads/tutorials/posts: HN, r/ChatGPT, r/ApplyingToCollege, r/ChatGPTPromptGenius, r/PromptEngineering, r/BypassAiDetect, r/BestAIHumanizer_, r/college, r/teachers, r/copywriting, r/SEO, OpenAI Developer Community, BlackHatWorld, Medium (Narejo "50+ prompts"), YouTube (Insights4UToday), vendor blogs (thehumanizeai.pro, TwainGPT, GPTZero bypassers, glbgpt hybrid routing, Originality SEO-subreddit study), teacher blogs (Cristina Cabal), and Threads. Includes reproducible prompts with per-detector measured scores.
