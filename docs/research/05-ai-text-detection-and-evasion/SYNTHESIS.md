# Category 05 — AI Text Detection and Evasion

## Scope

This category covers three interlinked domains: the detectors built to identify AI-generated text (statistical zero-shot methods, trained classifiers, behavioral probes), the watermarking schemes designed to embed provenance in generated output at sampling time, and the evasion and humanization techniques that defeat both. Research spans peer-reviewed literature at ICML/NeurIPS/ICLR/NAACL, vendor and mainstream press commentary, open-source implementations, commercial products, and practitioner communities. For the Unslop project, this category defines the adversarial surface: every major detector is a benchmark to evaluate against, every documented watermark is a constraint to plan around, and every evasion technique is either prior art to absorb or a failure mode to avoid.

---

## Executive Summary

- **Clean-domain detection is solved; out-of-distribution detection is not.** Fast-DetectGPT, Binoculars, Ghostbuster, RAIDAR, and now AdaDetectGPT (NeurIPS 2025 — 12.5–37% AUC improvement over Fast-DetectGPT with formal FPR guarantees) all report same-domain AUROC ≥0.99 (A). M4, MGTBench, and RAID show cross-domain and cross-generator performance drops that consistently manifest as *false negatives* — the model misses AI text once genre or generator shifts (A). Vendor-claimed 97–99% accuracy lands at 68–91% in independent testing (B, D). GPTZero version 4.1b achieved 99.3% recall / 0.1% FPR on the Chicago Booth 2026 benchmark — now the reference external metric replacing Scribbr's 2024 ranking — but drops to 60–80% on humanized content (D). Winston AI's "99.98%" headline produces 71% accuracy at 5% FPR on RAID (D).
- **Paraphrase is the universal solvent.** DIPPER alone drops DetectGPT detection from 70.3% to 4.6% at 1% FPR (A). Recursive paraphrasing (Sadasivan), adversarial GAN-style paraphrasers (RADAR), RL-optimized rewriting (StealthRL — 97.6% attack success rate, transfers to held-out detectors), and second-pass LLM rewording all follow the same pattern (A, C). OpenAI conceded its 99.9%-accurate watermark is "trivial to circumvention by bad actors" via rewording with another model (B).
- **Watermarks are the strategic frontier, and they keep losing — harder.** SynthID-Text is the only at-scale deployed scheme, validated across nearly 20 million Gemini responses (A). Kirchenbauer green-list is the academic reference. Jovanović's watermark-stealing attack spoof/scrubs state-of-the-art schemes for under $50 at 80% average success (A). SIRA (ICML 2025) now achieves ~100% attack success rate on *seven* recent watermarking schemes at $0.88/million tokens — no access to the watermark algorithm needed, any LLM (including mobile-scale models) serves as the attack engine (A). ETH SRI Lab's black-box probing of SynthID-Text (2025) shows it is easier to scrub than other SOTA schemes even for naive adversaries (A). WaterPark (EMNLP 2025) systematizes 10 watermarkers × 12 attacks and finds no single scheme is robust across all attacks (A, C). Christ–Gunn–Zamir's cryptographic construction provides a theoretical counter to Sadasivan's impossibility bound, but editing-attack robustness has not been empirically validated at scale — and SIRA represents the class of attack it would need to survive (A). The EU AI Act Article 50 transparency obligations become binding in August 2026, requiring mandatory machine-readable marking for all generative AI providers — a structural market event not yet reflected in commercial product positioning (B).
- **Detectors fail asymmetrically, and the equity story is the defensible wedge.** Liang et al. showed more than half of TOEFL essays were misclassified as AI-generated while native-English college essays were near-perfectly classified (A). Bloomberg documented named students falsely accused. Vanderbilt, UT Austin, and Northwestern disabled Turnitin's detector (B). The transformation that evades detection is the same transformation that removes the false-positive bias against ESL writers (A, B, E) — a rare case where the attack and the equity fix are the same prompt.
- **Three signals define the detection target.** Perplexity (token-level predictability), burstiness (sentence-length variance), and stylometric fingerprint (model-family signatures) are the shared stack across GPTZero's canonical explainer (B), Copyleaks' "three investigators" ensemble (B, D), open-source humanizer-x (C), and every practitioner tutorial that reports measured scores (E). Humanizers that only rewrite vocabulary lose to ensemble detectors.
- **Retraining cadence is ~30 days; static humanizers decay.** Originality.ai ships Lite 1.0.1 (June 2025), Lite 1.0.2 / Turbo 3.0.2 / Academic 0.0.5 (September 2025) with explicit humanizer-resistance targets. GPTZero maintains a "greylist" of bypass methods and patches within days, and as of January 2026 runs a dedicated humanizer-aware detection layer (B, E). Turnitin's 2026 roadmap explicitly targets AI humanizer tools. A shipped humanizer has a month-scale half-life on any single strategy.
- **Two humanizer castes exist with an obvious gap between them.** The academic caste — DIPPER, StealthRL, RADAR — trains or RL-optimizes a paraphrase policy against a detector ensemble. The practitioner caste — humanizer-x, Mohit1053/Humanizer, most SaaS products — is almost entirely prompt-engineering on top of Llama3-8B, T5, or PEGASUS. No commercial product ships an ensemble-trained, self-calibrating paraphrase policy (C).
- **Grammarly's "Authorship" pivot signals structural weakening on the detection side.** Rebranding from classifier-based detection to keystroke-provenance tracking is the first major vendor concession that the classifier approach has a losing long-term trajectory (D).

---

## Cross-Angle Themes

**The three-signal consensus** appears independently in every angle. Academic papers measure probability curvature (DetectGPT), the observer/performer perplexity ratio (Binoculars), and manifold geometry (Tulchinskii) — all targeting the same underlying signal separation (A). GPTZero's public explainer names perplexity and burstiness explicitly (B). Copyleaks' "three investigators" ensemble adds stylometric fingerprint (B, D). Open-source humanizer-x's README claims to "address all three" (C). Every practitioner tutorial with measured scores names all three as targets (E).

**Paraphrase beats character-level tricks across every generation.** SilverSpeak's homoglyph attack drops the average Matthews Correlation Coefficient from 0.64 to −0.01 across seven detectors (A, C). But `lm-watermarking` ships `normalizers.py` and `homoglyphs.py` to strip homoglyphs before detection (C), and GPTZero patched Cyrillic substitution within days of publication (E). Paraphrase-based evasion — DIPPER, recursive paraphrasing, StealthRL, multi-model routing — is the only attack that has survived two detector generations across academic, open-source, and community evidence (A, B, C, E).

**The ESL/equity narrative runs through every tier.** Liang (academic, A), Bloomberg and MIT Tech Review and Inside Higher Ed (press, B), Turnitin's October 2025 update adding "non-native speaker protections" (vendor, B), and HN/Reddit false-positive threads (practitioner, E) all center the same finding. Originality.ai has a rebuttal post but the narrative has won at the institutional level. Vanderbilt, UT Austin, and Northwestern have disabled Turnitin's detector. The practical implication is that humanizer products have a legitimate public-interest framing available to them.

**Benchmarking is maturing and attack-inclusive.** RAID ships 10 million documents across 11 LLMs, 11 genres, 4 decoding strategies, and 12 adversarial attacks as a Python API (`pip install raid-bench`) (C). MGTBench 2.0 adds 16 academic categories (C). M4 covers multilingual and cross-generator settings (A). "Did you evaluate on RAID with adversarial splits?" is effectively the first review question a new detector paper receives. Humanizer claims like "<10% on GPTZero" are not comparable to academic TPR@1%FPR numbers; no shared eval harness exists (C, E).

**Watermark stealing is empirically tractable.** Jovanović, Staab, and Vechev showed that API queries costing under $50 can reverse-engineer green-list vocabulary splits to both spoof and scrub Kirchenbauer-style watermarks at 80% average success (A). MIT Tech Review covered the result (B). `XuandongZhao/WatermarkAttacker` ships the regeneration attack template (C). This is the research program that humanizer products are the applied layer of.

**Commercial moats are collapsing into pricing and positioning.** Detectors all layer perplexity + burstiness + classifier (B, D). Humanizers all layer sentence reshuffling + vocabulary substitution + burstiness injection + tone modes (D). The $10–20/mo consumer band is crowded; the $20–40/mo range is thin; differentiation has migrated to integrations, guarantees (AIHumanize's credit-back-if-detected clause), and training-data provenance claims (Phrasly's "proprietary models trained on 1M+ pages") (D).

---

## Top Sources

### Must-read papers

- Mitchell et al., **DetectGPT** — ICML 2023. Zero-shot detection via probability curvature; AUROC 0.95 on GPT-NeoX-20B fake news. Template for the entire generation of zero-shot detectors. https://arxiv.org/abs/2301.11305
- Bao et al., **Fast-DetectGPT** — ICLR 2024. Replaces mask-fill perturbations with single-pass conditional sampling; 340× speedup, white-box AUROC 0.9887. https://arxiv.org/abs/2310.05130
- Hans et al., **Binoculars** — ICML 2024. Observer/performer perplexity ratio (Falcon-7B vs Falcon-7B-Instruct); detects >90% of ChatGPT samples at 0.01% FPR with no training data from ChatGPT. https://arxiv.org/abs/2401.12070
- Verma et al., **Ghostbuster** — NAACL 2024. Structured feature search over weak-LM probabilities; 99.0 F1 in-domain, +23.7 F1 over DetectGPT, black-box compatible. https://aclanthology.org/2024.naacl-long.95/
- Kirchenbauer et al., **A Watermark for Large Language Models** — ICML 2023 (Outstanding Paper). Green-list/red-list logit biasing, z-test detection from as few as 25 words. https://arxiv.org/abs/2301.10226
- Kirchenbauer et al., **On the Reliability of Watermarks for LLMs** — ICLR 2024. Watermark detectable from 800 tokens after strong human paraphrasing; sets up the stealing/spoofing attacks. https://arxiv.org/abs/2306.04634
- Dathathri et al., **SynthID-Text** — *Nature* 2024. Tournament-style probability modulation; validated across nearly 20 million Gemini responses with no measurable quality loss. https://www.nature.com/articles/s41586-024-08025-4
- Christ, Gunn, Zamir, **Undetectable Watermarks for Language Models** — COLT 2024. Cryptographic construction computationally indistinguishable from the unwatermarked model; completeness under a secret key; soundness against false positives. https://arxiv.org/abs/2306.09194
- Sadasivan et al., **Can AI-Generated Text Be Reliably Detected?** — arXiv 2303.11156. Total-variation-distance impossibility bound; recursive paraphrasing defeats watermarks, classifiers, zero-shot detectors, and retrieval-based defenses. https://arxiv.org/abs/2303.11156
- Chakraborty et al., **Position: On the Possibilities of AI-Generated Text Detection** — ICML 2024. Sample-complexity counter to Sadasivan: detection is feasible given enough tokens and separable distribution support. https://arxiv.org/abs/2304.04736
- Krishna et al., **DIPPER** — NeurIPS 2023. 11B-parameter controllable paraphraser; drops DetectGPT from 70.3% to 4.6% detection at 1% FPR. https://arxiv.org/abs/2303.13408
- Hu, Chen, Ho, **RADAR** — NeurIPS 2023 (IBM Research). GAN-style co-training of paraphraser and RoBERTa-large detector; minimax formalization of the arms race. https://arxiv.org/abs/2307.03838
- Jovanović, Staab, Vechev, **Watermark Stealing in Large Language Models** — ICML 2024 (ETH SRI Lab). Under $50, >80% average success on spoof+scrub attacks against state-of-the-art watermarks. https://arxiv.org/abs/2402.19361
- Mao et al., **RAIDAR** — ICLR 2024. Detect-by-rewriting: LLMs edit human text more than AI text; up to +29 F1 points across six domains, black-box compatible. https://arxiv.org/abs/2401.12970
- Liang et al., **GPT Detectors Are Biased Against Non-Native English Writers** — *Patterns* 2023. TOEFL essays flagged as AI-generated at a rate >50%; native-English essays near-perfectly classified; the same prompt that evades detection removes the false-positive bias. https://arxiv.org/abs/2304.02819
- Tulchinskii et al., **Intrinsic Dimension Estimation for Robust Detection** — NeurIPS 2023. Persistent-homology geometry: human text sits ~1.5 intrinsic dimensions higher than AI text; stable across domains and models. https://arxiv.org/abs/2306.04723
- Wang et al., **M4** — EACL 2024 (Best Resource Paper). Multi-lingual, multi-generator, multi-domain benchmark; basis for SemEval-2024 Task 8. https://arxiv.org/abs/2305.14902
- Creo & Pudasaini, **SilverSpeak** — arXiv 2406.11239. Homoglyph substitution drops average MCC from 0.64 to −0.01 across seven detectors including all major zero-shot methods. https://arxiv.org/abs/2406.11239
- Dugan et al., **RAID** — ACL 2024. 10 million documents × 11 LLMs × 12 adversarial attacks; `pip install raid-bench`; open leaderboard. https://raid-bench.xyz
- Mamba413 et al., **AdaDetectGPT** — NeurIPS 2025. Adaptive Fast-DetectGPT extension with formal FPR/TPR statistical guarantees; 12.5–37% AUC improvement. https://arxiv.org/abs/2510.01268
- Liang, Wang et al., **WaterPark / Watermark under Fire** — EMNLP 2025 Findings. First unified watermarking benchmark: 10 watermarkers × 12 attacks × 8 metrics; no single scheme robust across all. https://arxiv.org/abs/2411.13425
- Cheng, Guo et al., **SIRA (Self-Information Rewrite Attack)** — ICML 2025. ~100% attack success on seven watermarking schemes at $0.88/million tokens; no watermark access required; transfers to any LLM. https://arxiv.org/abs/2505.05190

### Key essays and posts

- OpenAI, "New AI classifier for indicating AI-written text" — the retraction post: 26% TP, 9% FP, shut down July 2023. The strongest baseline citation for why naive classifiers fail. https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text
- Wes Davis, The Verge, "OpenAI won't watermark ChatGPT text because its users could get caught" (Aug 2024). OpenAI concedes a second-pass rewording LLM defeats its 99.9% watermark; internal survey shows ~30% of users would use ChatGPT less if watermarked. https://www.theverge.com/2024/8/4/24213268/openai-chatgpt-text-watermark-cheat-detection-tool
- Melissa Heikkilä, MIT Technology Review, "Why detecting AI-generated text is so difficult" (Feb 2023). The canonical "arms race" framing. https://www.technologyreview.com/2023/02/07/1067928/why-detecting-ai-generated-text-is-so-difficult-and-what-to-do-about-it/
- Melissa Heikkilä, MIT Technology Review, "It's easy to tamper with watermarks from AI-generated text" (Mar 2024). Mainstream framing of Jovanović's watermark-stealing result. https://www.technologyreview.com/2024/03/29/1090310/its-easy-to-tamper-with-watermarks-from-ai-generated-text/
- Bloomberg, "Do AI Detectors Work? Students Face False Cheating Accusations" (Oct 2024). Named victims, 1–2% FP on bulk essays, Stanford's 61% ESL false-positive figure. https://www.bloomberg.com/news/features/2024-10-18/do-ai-detectors-work-students-face-false-cheating-accusations
- GPTZero, Edward Tian, "What is perplexity & burstiness?" — canonical industry explainer of the two primary detection signals. https://gptzero.me/news/perplexity-and-burstiness-what-is-it/
- Asifa Narejo, Medium, "I Tested 50+ Prompts to Beat AI Detectors. Only These 3 Actually Worked" (Jan 2026). The only widely-cited source with reproducible prompts × per-detector measured scores (GPTZero 8%, Originality 4%, Turnitin 12%, ZeroGPT 0% on "Human Imperfection Protocol"). https://medium.com/@asifanarejo/i-tested-50-prompts-to-beat-ai-detectors-only-these-3-actually-worked-bc6273fe4fdc
- European Commission, "Code of Practice on Marking and Labelling of AI-Generated Content" (Dec 2025). First draft of binding EU Article 50 Code; proposes mandatory metadata + imperceptible watermarks + fingerprinting for all generative AI providers; binding August 2026. https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
- GPTZero, "GPTZero Tops Accuracy on Chicago Booth Benchmark in 2026." 99.3% recall / 0.1% FPR — the new reference benchmark replacing Scribbr's 2024 ranking. https://gptzero.me/news/chicago-booth-2026/
- Inside Higher Ed, "Professors proceed with caution using AI-detection tools" (Feb 2024). Vanderbilt, UT Austin, Northwestern have disabled Turnitin's detector. https://www.insidehighered.com/news/tech-innovation/artificial-intelligence/2024/02/09/professors-proceed-caution-using-ai
- Ahrefs, "AI-Generated Content Does Not Hurt Your Google Rankings" — 600,000-page study; 86.5% of top-ranking pages contain AI content; Google ranking correlation with AI use is 0.011. https://ahrefs.com/blog/ai-generated-content-does-not-hurt-your-google-rankings/

### Key OSS projects

**Detectors:**
- `baoguangsheng/fast-detect-gpt` (~388★, MIT) — Fast-DetectGPT reference; Jan 2026 update recommends Llama3-8B/Llama3-8B-Instruct scoring models over the original Falcon defaults.
- `ahans30/Binoculars` — minimal drop-in, `Binoculars().predict(text)`; fixed global threshold using Falcon-7B pair.
- `vivek3141/ghostbuster` — README explicitly documents that humanizer-edited text is a known failure case.
- `Mamba413/AdaDetectGPT` (~71★) — NeurIPS 2025 adaptive extension with formal FPR/TPR statistical guarantees; outperforms Fast-DetectGPT by 12.5–37% AUC. The new ceiling for open-source detector evaluation.

**Watermarks:**
- `jwkirchenbauer/lm-watermarking` (~663★, Apache 2.0) — KGW reference; recommended defaults `gamma=0.25, delta=2.0, h=4, selfhash`; ships `normalizers.py`/`homoglyphs.py` to pre-strip character attacks.
- `google-deepmind/synthid-text` (~813★, Apache 2.0) — reference implementation; production version lives in Hugging Face Transformers.
- `THU-BPM/Robust_Watermark` — paraphrase-robust semantic-invariant watermark (SIR); current baseline for watermarks designed to survive paraphrasing.

**Attacks / evasion:**
- `martiansideofthemoon/ai-detection-paraphrases` + `kalpeshk2011/dipper-paraphraser-xxl` — DIPPER 11B T5-XXL; two scalar knobs (lexical diversity, order diversity); ships retrieval-defense code.
- `suraj-ranganath/StealthRL` — GRPO + LoRA on Qwen3-4B trained against a 4-detector ensemble; mean AUROC reduced from 0.79 to 0.43; 97.6% attack success rate; transfers to held-out detectors. M0–M5 attack taxonomy.
- `ACMCMC/silverspeak` — homoglyph library with attack reversal; `pip install silverspeak`.
- `XuandongZhao/WatermarkAttacker` — regeneration attack template (embed → noise → reconstruct).
- `Allencheng97/Self-information-Rewrite-Attack` — SIRA (ICML 2025); ~100% watermark removal via targeted high-entropy token masking at $0.88/million tokens; no watermark access required; commoditizes watermark removal. https://github.com/Allencheng97/Self-information-Rewrite-Attack

**Benchmarks:**
- `liamdugan/raid` — `pip install raid-bench`; 12 adversarial attacks as a Python API.
- `xinleihe/MGTBench` + `Y-L-LIU/MGTBench-2.0` — 16 academic domains, multiple generators.
- `Xianjun-Yang/Awesome_papers_on_LLMs_detection` (~286★) — best single literature entry point.
- WaterPark (EMNLP 2025 Findings, arXiv 2411.13425) — 10 watermarkers × 12 attacks × 8 metrics; the RAID equivalent for watermarking evaluation. https://arxiv.org/abs/2411.13425

**Practitioner humanizers:**
- `itsjwill/humanizer-x` — 4-pass prompt pipeline (pattern removal → voice injection → statistical tuning → verification); severity-ranked 30-tell catalog; six voice modes.
- `Mohit1053/Humanizer` — Ollama/Llama3-8B; minimal reference implementation of "humanizer = carefully crafted system prompt + batch runner."

### Notable commercial tools

**Detectors:** GPTZero (99.3% recall / 0.1% FPR on Chicago Booth 2026 — new reference benchmark; humanizer-aware detection layer added Jan 2026; ~$20M ARR); Originality.ai (Lite 1.0.2 / Turbo 3.0.2 / Academic 0.0.5 as of September 2025, 96% accuracy in independent November 2025 study, consistently the hardest detector for humanizers); Copyleaks (multilingual, "three investigators" ensemble, 99.88% model-attribution claim, Japanese added April 2025); Turnitin (10,700+ institutions, October 2025 update softened verdicts, 2026 roadmap targets humanizer tools, 1–19% scores hidden by default); Winston AI ("99.98%" claim, RAID measures 71% at 5% FPR); Grammarly Authorship (keystroke/paste provenance tracking — the strategic pivot away from classification).

**Humanizers:** Undetectable.ai (22M+ users as of 2026, 87–88% average bypass across major detectors, category leader by user volume); Ryter Pro (97% GPTZero / 94% Turnitin bypass in Alammyan 2026 testing — current top performer by measured bypass rate); Phrasly (only tool marketing training-data provenance: "proprietary models trained on 1M+ pages"); HIX Bypass ("Latest" mode advertises explicit tuning against Originality 3.0 and newest Turnitin); AIHumanize (money-back-if-detected guarantee, 1.28B words/month); Surfer AI Humanizer (only tool framed for SEO rather than academic evasion, custom voice training); StealthGPT (fails against Originality at 35% flagged despite "Samurai Engine" branding).

### Notable community threads

- HN #36182912 — "You can literally ask ChatGPT to evade AI detectors. GPTZero says 0%" (Jun 2023). Foundational "just ask" prior art; later detectors patched the obvious version.
- HN #35535174 — "Teacher failed kid for essay because an AI-detection tool flagged his work" (Apr 2023). Engineers and teachers reach consensus that proctored in-class writing is the only reliable answer.
- r/ApplyingToCollege (gwern mirror, Nov 2024) — "I reviewed 100 essays. Here's how I could tell which were ChatGPT." The canonical 7-tells list: *delve/tapestry*, extended metaphors (weaving, cooking, painting, dance), em-dash/curly-quote mismatch, ascending tricolons, "not only Y, it's also Z," "As I advance I will carry this lesson," Lord-of-the-Rings multi-endings.
- OpenAI Developer Community, "GPTZero bypasser Program" — canonical early evidence that Cyrillic homoglyphs dropped scores to ~0%; GPTZero patched Feb 2, 2023.
- Cristina Cabal teacher blog, "Is Your Student Writing or Just Prompting?" — teacher-side taxonomy including "Tyranny of Triplets" (AI groups in threes, not twos or fives), robot rhythm of 15–22 words, suspiciously uniform 150–250-word paragraphs.

---

## Key Techniques & Patterns

### Detection families

1. **Statistical / zero-shot, likelihood-based:** DetectGPT (probability curvature via mask-fill perturbations), Fast-DetectGPT (conditional curvature, 340× faster), Binoculars (base/instruct perplexity ratio), GLTR (token-rank visualization, legacy). All exploit that LLM samples sit at lower-curvature / lower-perplexity points of the source model's landscape.
2. **Behavioral / structural probes:** RAIDAR (rewrite-and-measure edit distance — LLMs edit human text more than AI text), Tulchinskii intrinsic-dimension (persistent-homology geometry of contextual embeddings, stable across domains and models). Both work on closed APIs with no logit access.
3. **Weak-model feature probes:** Ghostbuster (structured search over combinations of weak-LM token probabilities, black-box compatible). Does not require access to the generating model.
4. **Fine-tuned classifiers:** OpenAI RoBERTa detector (retracted 2023), Originality Turbo/Lite/Academic, Copyleaks "AI Logic" three-investigator ensemble, Winston HUMN-1, GPTZero layered stack, Turnitin proprietary academic-corpus classifier.
5. **Retrieval / provenance:** Krishna et al.'s provider-side store-and-retrieve defense; Grammarly Authorship's keystroke/paste-event tracking.

### Watermark families

1. **Green-list/red-list (KGW):** Kirchenbauer — hash prior token to split vocabulary, softly boost green logits, detect via z-test. Reference defaults: `gamma=0.25, delta=2.0, h=4, selfhash`. Detectable from 25 words. Vulnerable to stealing, spoofing, and DIPPER-level paraphrase.
2. **Gumbel-max (Aaronson):** Sample via `argmax log P − log U` with pseudo-random `U` from a secret-key hash; unshipped from OpenAI. Basis of GumbelSoft and Ruan et al. refined detection.
3. **Tournament / SynthID (Google):** Probability modulation composable with speculative sampling; deployed in Gemini; reference implementation open-sourced but production version lives in HF Transformers.
4. **Cryptographic (Christ–Gunn–Zamir):** Output computationally indistinguishable from the unwatermarked model under one-way-function assumption; complete under secret key, sound against false positives. Editing-attack robustness not yet empirically validated at scale.
5. **Semantic-invariant (SIR, THU-BPM):** Paraphrase-robust design; current best open baseline for watermarks that survive paraphrasing.

### Evasion techniques, ranked by durability

1. **Neural paraphrase (DIPPER, StealthRL, recursive):** Survives two detector generations. DIPPER drops DetectGPT 70.3%→4.6%; StealthRL cuts mean AUROC 0.79→0.43 and transfers to held-out detectors. Primary attack.
2. **Second-pass LLM rewording:** OpenAI's own admission. The core architectural primitive of all consumer humanizer products.
3. **Multi-model / "hybrid" routing:** Draft in one model family, rewrite for flow in another, inject facts from a third. Breaks per-model stylometric fingerprints that Copyleaks targets (99.88% model-attribution claim implies the vulnerability is real).
4. **Statistical tuning:** Deliberate burstiness injection (dramatic short/long sentence alternation), controlled perplexity via uncommon word choices, contractions in 70–80% of sentences, conjunction-initial sentences, rhetorical questions, parenthetical asides, one-sentence fragments, backtracking phrases.
5. **Anti-tell rules:** Strip *delve, utilize, leverage, harness, streamline, fundamentally, arguably*; eliminate ascending tricolons, extended metaphors (weaving/cooking/dance), "not only Y, it's also Z," LOTR multi-endings, robot-rhythm sentence uniformity.
6. **Persona framing:** "Tired 28-year-old copywriter on third espresso" meta-prompt; first-person specificity; real named examples. Reported to further reduce detection by ~5–8 percentage points post-edit.
7. **Watermark removal (Jovanović stealing + SIRA):** Two complementary approaches. Jovanović: reverse-engineer green-list partitions via API queries (<$50, 80% success). SIRA (ICML 2025): calculate per-token self-information, mask high-entropy positions, fill in with any LLM (~100% success on 7 schemes, $0.88/million tokens, no watermark access needed). SIRA has commoditized watermark removal.
8. **Homoglyph / whitespace / Unicode tricks:** Effective today (SilverSpeak drops seven detectors to MCC −0.01) but trivially reversed by `normalizers.py`; patched within days by major detectors. Dead end.

---

## Controversies & Debates

**False positives and civil harm.** Liang's finding that >50% of TOEFL essays are misclassified as AI-generated is load-bearing across academic, press, and institutional literature. Bloomberg documents named students — Olmsted, Quarterman, Stivers — falsely accused. Vanderbilt, UT Austin, Northwestern have disabled Turnitin's detector. Turnitin's October 2025 release adds "non-native English speaker protections" and hides scores in the 1–19% range where its own testing found "a higher incidence of false positives." Originality.ai has a rebuttal post but the broader narrative has won at the institutional level.

**Detection impossibility vs possibility.** Sadasivan's TV-distance bound says detection collapses toward chance as models approach human text quality — empirically demonstrated with recursive paraphrasing. Chakraborty's ICML 2024 position paper counters that detection is "consistently feasible" given enough tokens and separable distribution support. Both are correct; they describe opposite ends of the same curve. The practical question is whether any given deployment has long enough text and a wide enough distribution gap. Christ–Gunn–Zamir shows cryptographic watermarks can theoretically exist without a quality tradeoff, but editing robustness is not validated at scale.

**Vendor claims vs independent benchmarks.** Every major detector clusters its marketing at 97–99%. Independent 2026 testing: GPTZero 88–95% raw / 60–80% humanized (MPG ONE); Originality 96% (most consistent; November 2025 study); Turnitin 92–100% raw / 60–85% edited. The Chicago Booth 2026 benchmark has largely replaced Scribbr's 2024 ranking as the community reference — but Chicago Booth tests clean AI text, not humanized content, so it still inflates apparent performance. RAID and WaterPark are the only adversarial-split benchmarks. The gap between vendor numbers (clean-domain) and real-world numbers (humanized content) is 15–30 percentage points.

**Watermark deployment ethics.** OpenAI built a 99.9%-accurate watermark and declined to ship it after an internal survey found ~30% of ChatGPT users would use the product less if watermarked. Google DeepMind shipped SynthID-Text but positioned it as "a building block, not a solution." Neither the incumbent consumer LLM nor the dominant enterprise LLM has adopted watermarking as a default. Detector-only enforcement is therefore structurally incomplete.

**The arms race loop.** MIT Technology Review (Feb 2023), Hayim Salomon's Medium essay (Apr 2026), and Originality's own 30-day retrain changelog all describe the same cycle: detectors claim 98%, independent tests land at 70–80%, humanizers update, detectors retrain, cycle repeats on a monthly cadence. Grammarly's pivot to Authorship is the first major vendor to concede the cycle is not winnable by classifiers.

**Ethics of the humanizer category.** BlackHatWorld's SEO-affiliate culture, r/BypassAiDetect, and 22M Undetectable.ai users (2026, up from 15M in Feb 2025) coexist with documented honor-code violations and the equity framing of "protect ESL writers from false flags." The EU AI Act Article 50 adds a third axis: jurisdictional legality in the EU market once mandatory watermarking is binding from August 2026. Every angle acknowledges the tension. None resolves it.

---

## Emerging Trends

**Behavioral and structural probes replacing logit-access probes.** RAIDAR, Binoculars, and Tulchinskii all operate without access to the generating model's log-probabilities. AdaDetectGPT (NeurIPS 2025) continues this trend with formal statistical guarantees rather than empirical thresholds. The next generation of detectors is likely to be fully black-box and provably bounded by design.

**RL-optimized ensemble evasion.** StealthRL trains a Qwen3-4B LoRA policy using GRPO against four detectors and achieves 97.6% attack success rate with cross-detector transfer to two held-out detectors. This reframes evasion from "beat detector X" to "exploit a family-level architectural weakness" — structurally different from the previous generation of per-detector prompt tricks.

**SIRA reframes watermark attacks as commodity.** SIRA (ICML 2025) makes ~100% watermark removal available to any developer with an API key and $0.88/million tokens, using any LLM as the attack engine. This is qualitatively different from Jovanović's $50 watermark-stealing attack, which required domain expertise in vocabulary-split reverse-engineering. SIRA requires none — it exploits token entropy universally. The watermarking research program's practical viability is now in question.

**Attack-inclusive benchmarks as the default bar.** RAID's 12-attack Python API, MGTBench 2.0's 16-domain academic coverage, and now WaterPark's 10-watermarker × 12-attack unified platform are fast becoming baseline expectations in detector paper reviews. Peak in-domain AUROC is no longer a credible solo metric. WaterPark for watermarks, RAID for detectors.

**Institutional exit from detection.** Major universities disabling Turnitin's detector, Turnitin itself softening to "conversation starters," Grammarly's Authorship pivot, and Inside Higher Ed's coverage of university policy drift all point the same way. Institutional pressure is migrating from student-cheating detection toward B2B content-QA pipelines and process-based grading.

**EU regulatory pressure enters the market.** The EU AI Act Article 50 transparency obligations are binding from August 2026. A December 2025 draft Code of Practice proposes mandatory multilayer watermarking (metadata + imperceptible watermarks + fingerprinting) for all generative AI providers. This is the first binding legal mandate that could force OpenAI and Anthropic to ship watermarks regardless of user preference. The Verge's "shelved because users would use it less" rationale is now legally moot in the EU market.

**Guarantee-as-marketing spreading.** AIHumanize's credit-back-if-detected clause converts detection risk into a vendor liability. Undetectable.ai reaching 22M users signals the humanizer category is mainstream consumer software, not niche. As technical differentiation narrows further, risk-transfer mechanisms and market-share moats are the surviving differentiators.

**Multilingual gap widening.** Turnitin added Japanese detection in April 2025. Copyleaks reports English accuracy at 93% and Chinese/Japanese/Arabic at 74–84%. No humanizer publishes non-English quality benchmarks despite all claiming 50+ language support. A humanizer that can document non-English performance would hold uncrowded ground.

**Academic-domain specialization opening.** Originality launched Academic 0.0.5 (September 2025) targeting academic prose at <1% FP. No humanizer has launched a matching academic mode that preserves citation integrity and disciplinary register.

---

## Open Questions & Research Gaps

- **Quality-controlled humanization benchmarks do not exist.** The literature evaluates attack success (paraphrase rate, watermark-removal rate); nothing measures semantic or stylistic distortion per unit of detection reduction. This is the specific measurement gap a humanizer product lives in.
- **No public, dated, rolling benchmark** across detectors × prompts × models. Community leaderboards are vendor-run. RAID is a static corpus. A continuously-updated benchmark would be the highest-leverage research artifact in this space.
- **Adaptive-adversary evaluation is rare.** Most detector papers test against DIPPER or GPT-3.5 paraphrase; few retrain their detector against an adaptively-optimized evader. BIRA-style query-free optimization is not yet standard practice.
- **ESL-fairness is not a standard reporting axis.** Liang is cited in nearly every survey but rarely replicated on new detectors. Per-demographic confusion matrices are absent from vendor reporting.
- **Hybrid content (50% human + 50% AI) is under-studied.** Scribbr found detectors produce bimodal verdicts on hybrid documents — effectively the most common real-world use mode for AI-assisted writing. Neither vendor nor academic literature addresses this well.
- **No SynthID-aware humanizer exists — but SIRA makes this technically trivial.** All public humanizers test against GPTZero/ZeroGPT/Originality. SynthID is deployed on Gemini output at scale. SIRA (ICML 2025) achieves ~100% removal at commodity cost. The gap is regulatory/PR risk, not technical difficulty. ETH SRI Lab's probing confirms SynthID is easier to scrub than other SOTA schemes.
- **No trained-policy open humanizer since DIPPER (2023).** Distilling DIPPER into a 3–7B model, or RL-training a Qwen/Llama variant against a modern detector ensemble in the manner of StealthRL, is an unclaimed position. AdaDetectGPT's formal guarantees raise the bar: a trained evasion policy must now defeat provably-bounded detection.
- **Retrieval-defense attacks are under-studied.** DIPPER's own paper argues that provider-side retrieval is the strongest defense against paraphrase attacks. Very few evasion papers attack stateful retrieval; most assume a stateless detector.
- **Cross-model stylometric blending.** Copyleaks claims 99.88% model-attribution accuracy. Humanizers that only change surface tokens while leaving model-family syntax intact remain detectable. Multi-model roundtripping (e.g. GPT-5.2 → Claude 4.5 → Grok 4.1 as documented by practitioner guides in 2026) as a systematic evasion primitive is under-evaluated in the research literature.
- **Score variance / stability.** The most common complaint in r/BypassAiDetect is score drift across reruns of the same detector on the same text. No humanizer product advertises variance bounds. A demonstrably stable humanizer would have a real differentiating claim.
- **Cryptographic watermark robustness under SIRA-class attacks.** Christ–Gunn–Zamir shows computational undetectability in theory. SIRA achieves ~100% removal on seven current schemes. Whether a truly cryptographic watermark can survive SIRA's targeted high-entropy token masking is the central unresolved question in the watermarking literature as of April 2026.
- **EU Article 50 compliance tooling does not exist.** The August 2026 binding obligations require machine-readable watermarking from all generative AI providers operating in the EU. No compliance tooling, audit framework, or humanizer positioning addresses what "bypassing mandatory EU watermarking" means legally or technically. This is either a significant new risk or a significant new opportunity depending on how the market evolves.

---

## How This Category Fits

Category 05 defines the adversarial envelope the Unslop project operates inside. The "AI tells" taxonomy that drives rewriting-pass design — em-dashes, tricolons, *delve/tapestry*, rule-of-three, extended metaphors, LOTR-style multi-endings — is most precisely documented in the practitioner threads (angle E) and codified in open-source humanizer prompt lists (angle C). The three detection signals (perplexity, burstiness, stylometric fingerprint) specify what a humanization pass must measurably shift; any rewriting that only touches vocabulary without moving burstiness or cross-model fingerprint is category-weak. The equity and ESL-bias framing (angles A and B) is the only positioning that converts a "bypass tool" into a product with a legitimate public-interest rationale. The monthly retraining cadence on the detector side (angles B and D) sets a hard architectural constraint: Unslop cannot ship a static strategy. The watermark horizon — SynthID in production, OpenAI's shelved scheme, Christ–Gunn–Zamir's theoretical construction — defines a 12–24 month window where provenance mechanisms, not classifiers, become the dominant enforcement layer. Category 05 intersects most directly with Category 06 (AI writing style and voice characteristics, which defines what the three signals actually measure in prose), Category 02 (evaluation methodology, where the benchmark-gap problem between vendor claims and RAID-style attack-inclusive evaluation lives), and Category 08 (NLP paraphrase and style transfer, which covers the technical lineage of DIPPER and StealthRL).

---

## Recommended Reading Order

1. **GPTZero, "What is perplexity & burstiness?"** (B) — canonical two-signal explainer; takes 10 minutes, establishes the vocabulary for everything else.
2. **Liang et al., "GPT Detectors Are Biased Against Non-Native English Writers"** (A) — the equity anchor; explains why the bypass and the fairness-fix are the same transformation.
3. **Melissa Heikkilä, MIT Technology Review, "Why detecting AI-generated text is so difficult"** (B) — the arms-race frame that the entire press and vendor discourse runs on.
4. **Mitchell et al., DetectGPT → Bao et al., Fast-DetectGPT → Hans et al., Binoculars → Mao et al., RAIDAR** (A) — the detector evolution arc from probability curvature (2023) to behavioral probes (2024).
5. **Krishna et al., DIPPER** (A) — the canonical paraphrase attack; every subsequent evasion paper cites it.
6. **Sadasivan et al. + Chakraborty et al.** (A) — the impossibility/possibility theoretical pair; read them together.
7. **Jovanović, Staab, Vechev, Watermark Stealing** (A, B via MIT TR) — shows watermark removal is adversarial ML at $50 cost.
8. **Dathathri et al., SynthID-Text + The Verge watermark-shelved article** (A, B) — the market reality of watermarking: one shipped, one shelved.
9. **r/ApplyingToCollege 7-tells post (gwern mirror) + Narejo Medium "50+ prompts"** (E) — the practitioner playbook; the only source with reproducible prompt × detector score pairs.
10. **`suraj-ranganath/StealthRL` README + Originality.ai "2025: Year in Review"** (C, B) — the current state of RL-optimized evasion and the monthly-retraining cadence that determines humanizer shelf life.
