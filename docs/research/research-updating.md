# Research Update Log — April 2026

**Updated:** April 21, 2026  
**Scope:** All 20 research directories audited against April 2025–April 2026 sources.  
**Method:** 20 parallel agents, one per directory. Each read all 7 files, web-searched for recent developments, updated files in place, and returned a change summary.

---

## How to read this file

Each section covers one research directory. Three subsections per entry:

- **Outdated / False** — claims, stats, or product info that were wrong or stale
- **Added / Updated** — new papers, tools, corrected numbers, new findings
- **Remains Valid** — what held up and doesn't need touching

---

## 01 — Prompt Engineering & Humanization

### Outdated / False
- "Adversarial paraphrasing is the dominant academic humanizer" — MASH (arXiv 2601.08564, Jan 2026) established fine-tuned alignment as the new benchmark leader, making this claim stale.
- `blader/humanizer` star count: was ~14,477★, now ~14,700★ with active April 2026 issues.
- No mention of "context engineering" displacing "prompt engineering" as the dominant framing in practitioner communities (2026).

### Added / Updated
- **MASH** (arXiv 2601.08564, Jan 2026): SFT + DPO + inference-time refinement; 92% attack success rate across 6 datasets and 5 detectors. First fine-tuned alignment humanizer to dominate all prior training-free attacks.
- **HumanLLM: Benchmarking and Improving LLM Anthropomorphism** (arXiv 2601.10198, Jan 2026): 244 psychological patterns, 11,359 scenarios; HumanLLM-8B outperforms Qwen3-32B.
- **Humanizing LLMs: A Survey of Psychological Measurements** (arXiv 2505.00049, Apr 2025): six-dimension systematic survey, significant persona instability finding.
- **HumanLLM: Towards Personalized Understanding** (arXiv 2601.15793, Jan 2026): 5.5M user log corpus; personalized voice simulation at scale.
- `peakoss/anti-slop` GitHub Action: automated PR slop detection (2026 release). New class of CI-level gating.
- EU AI Act Code of Practice (August 2026 effective): uniform "AI" visual cue, editorial exception — added to regulatory coverage.
- Turnitin February 2026 update added to institutional detection coverage.
- Context engineering framing added to Emerging Trends across all angle files.

### Remains Valid
- All 18 original academic sources accurate and correctly cited (Reif, DIPPER, Gupta, Hu & Collier, HumT/DumT, Sun idiosyncrasies, Wang "Catch Me If You Can").
- Burstiness statistics (human academic ~8.2 stdev vs GPT-4o ~4.1) unchanged.
- The "Frankenstein method" community consensus (~80–90% self-reported style match) remains the practitioner baseline.

---

## 02 — RLHF & Alignment

### Outdated / False
- **Scale AI presented as a neutral vendor available to all major labs** — completely wrong. Meta acquired 49% stake in June 2025 for $14.3B. CEO Alexandr Wang left to join Meta as Chief AI Officer. Google, OpenAI, and xAI defected as clients.
- Surge AI revenue figure stale; the company raised a $1B capital round in July 2025 at $15–25B valuation.
- Claude's new Constitution (January 22, 2026) described as "coming in 2026" without content. The actual 23,000-word document uses reason-based alignment where Claude generates its own training data — a fundamental shift from the prior rule-list approach.
- No coverage of GRPO/DAPO/VAPO (DeepSeek-R1 era reinforcement learning approaches).
- Sycophancy described as "the dominant unsolved problem" — Shapira et al. (arXiv 2602.01002, Feb 2026) formally characterized and provided a known correction mechanism.

### Added / Updated
- **Shapira et al. "How RLHF Amplifies Sycophancy"** (arXiv 2602.01002, Feb 2026): formal theory of sycophancy amplification with a known correction.
- **DAPO** (arXiv 2503.14476): new SOTA on AIME 2024 at time of publication.
- **VAPO** (arXiv 2504.05118): value-aligned preference optimization.
- **DPO overoptimization scaling laws** (arXiv 2406.02900): extends overoptimization analysis to direct alignment methods.
- Nathan Lambert's RLHF Book (Manning / arXiv 2504.12501): elevated to primary source status.
- Anthropic Alignment Science Blog 2025: subliminal learning from synthetic data, reward-hacking generalization spreading to broader misalignment, out-of-context reasoning.
- OpenAI Model Spec updates (February 2025, December 2025) and GPT-5 anti-sycophancy changes documented.
- Meta/Scale structural market event fully documented in D-commercial.md.

### Remains Valid
- All DPO/IPO/KTO/ORPO/SimPO descriptions and benchmarks.
- Gao et al. scaling laws for reward model overoptimization.
- Sharma et al. sycophancy-in-preference-data empirical result.
- TRL, OpenRLHF, veRL, Axolotl, LLaMA-Factory descriptions (updated with release notes).

---

## 03 — Persona & Character Design

### Outdated / False
- **Character.AI stats**: 20M users / $9.99/mo — corrected to 28M+ MAU / $6.99/mo, with 18M+ chatbot characters and ~10B messages/month.
- **Replika Pro**: $19.99/mo — corrected to $11.66–$13.99/mo after 2025 pricing adjustment; registered users updated to ~25M.
- **Pi/Inflection presented as a live, active product with ~6M MAU** — false. The founding team (Suleyman, Simonyan) departed to Microsoft AI in early 2024. Pi.ai is technically live but no longer actively developed. Marked as [Historical] throughout.
- **SillyTavern**: listed as ~25,900 stars — corrected to ~23,300 (April 2026 figure).
- **Kindroid**: $9.99–13.99/mo — corrected to $13.99/mo; highest-rated companion app (4.5 stars, 20K+ reviews).
- No market-size data. Added: $221M consumer spend H1 2025 (+64% YoY), 220M cumulative global downloads, $37B market projected 2025.

### Added / Updated
- **Anthropic Persona Selection Model** (Feb 2026): theoretical account of why LLMs have personas; pretraining as character-simulation; "selecting" vs "installing" a persona.
- **Wang, Chen, Xiao — Role-Playing Agents Survey** (arXiv 2601.10122, Jan 2026): most current comprehensive RPLA survey; three paradigm generations.
- **CharacterBox** (NAACL 2025, arXiv 2412.05631): simulation-sandbox evaluation via dual character+narrator agents.
- **RPEval** (arXiv 2505.13157, May 2025): emotional understanding and moral alignment as evaluation axes.
- **RoleRAG** (arXiv 2505.18541, May 2025): retrieval-augmented character knowledge management via knowledge graphs.
- **Four-Quadrant Technical Taxonomy** (arXiv 2511.02979, NeurIPS 2025): Virtual/Embodied × Emotional/Functional framework.
- **NeurIPS 2025 PersonaLLM Workshop**: institutional recognition of subfield; >55% inconsistency reduction via multi-turn RL.
- SillyTavern February 2026 ComfyUI/Flux integration for in-session multimodal persona expression.

### Remains Valid
- Core academic papers (PersonaGym, BIG5-CHAT, CoSER, InCharacter, Character-LLM, RoleLLM, CharacterEval) all accurate.
- Anthropic Assistant Axis (Jan 2026), OpenAI sycophancy postmortem, OpenAI Model Spec — confirmed.
- Character Card V2/V3, CHARX — confirmed as living standard.

---

## 04 — Natural Language Quality

### Outdated / False
- **Antislop paper** (arXiv 2510.15061): described as a 2025 arXiv preprint — it was accepted at **ICLR 2026** (poster #10008156). Now peer-reviewed.
- **EQ-Bench judge model**: listed as "Claude Sonnet 4" — the benchmark upgraded to **Claude Sonnet 4.6**. Leaderboard also added Slop and Repetition columns, plus a separate Longform Writing leaderboard (neither mentioned).
- **Top-nσ sampler**: E-practical and SYNTHESIS stated it was integrated into llama.cpp without noting it **defaults to `-1` (disabled)** and requires manual activation. Practitioners following the guide would not get it automatically.
- **LLM-judge bias**: no file acknowledged quantified, reproducible biases in LLM-as-judge: ~40% position inconsistency, ~15% verbosity inflation, 5–7% self-enhancement. Three 2025 papers establish these figures. Vendor claims (Anyword "82% accuracy", Sudowrite "40% fewer revisions") were presented without this context.
- **EU AI Act watermarking (Article 50)**: not mentioned in any file. December 2025 draft Code of Practice mandates multilayered AI text marking effective August 2026 and explicitly prohibits watermark removal. Bypass products face direct EU compliance exposure.
- **Anthropic Custom Styles**: B-industry documented Claude's Character (2024) but missed the Custom Styles shipment in 2025 (Normal/Concise/Explanatory/Formal presets + user-defined styles).
- **auto-antislop and published models**: the companion `auto-antislop` repo (end-to-end profiling → slop list → FTPO training data) and HuggingFace models (`gemma-3-27b-it-antislop`, `gemma-3-12b-it-antislop`) were absent.
- **BLEU/ROUGE status**: file predicted "more psycholinguistic eval in 2025–26" — that time has arrived. LLM-judge has now replaced BLEU/ROUGE as the dominant automatic evaluation paradigm (Gao et al. Computational Linguistics 2025 confirms).

### Added / Updated
- **LLM-as-Judge Survey** (arXiv 2411.15594), **CALM bias framework** (arXiv 2410.02736), **Gao et al. Computational Linguistics 2025** survey, **Order in the Evaluation Court** (arXiv 2601.07648).
- Antislop ICLR 2026 status, auto-antislop pipeline, published fine-tuned models.
- EQ-Bench: Claude Sonnet 4.6 judge, Slop/Repetition columns, Longform leaderboard, current leader (Grok-4.1 Thinking, 1721.900).
- Anthropic Custom Styles (2025) documented in B-industry.
- EU AI Act Article 50 Draft Code of Practice (Dec 2025) across all relevant files.
- top-nσ disabled-by-default caveat added.
- 2025-class model perplexity: now as low as 5–10, materially narrowing the AI-vs-human gap that classical detectors rely on.

### Remains Valid
- Decoding theory arc (Holtzman 2020 → Meister 2022 → Nguyen 2025) holds. Min-p's ICLR 2025 Oral status confirmed.
- Three-sampler recipe (min-p + DRY + temperature-last) remains community consensus.
- vLLM's refusal to merge DRY/XTC confirmed still standing as of April 2026.
- DetectGPT and Ghostbuster mechanisms unchanged (practical reliability narrowing).

---

## 05 — AI Text Detection & Evasion

### Outdated / False
- **GPTZero accuracy**: "claimed 99.3%/0.24% FP" was stale but directionally correct — GPTZero v4.1b (2026) now measures 99.3% recall / **0.1% FPR** (tighter). The Scribbr 2024 ranking (GPTZero at 52%) was out-of-date by two major model versions and no longer representative. Chicago Booth 2026 is now the reference benchmark.
- **Originality.ai model names**: "Lite, Turbo, Academic" had no version numbers. Now: Lite 1.0.1 (Jun 2025), Lite 1.0.2 / Turbo 3.0.2 / Academic 0.0.5 (Sep 2025) with explicit humanizer-corpus retraining.
- **Turnitin**: "98%, <1% FP" accurate for raw AI text but omitted the **60–85% performance drop against edited/paraphrased content** (University of Chicago Booth, late 2025). Japanese detection (Apr 2025) missing. 2026 roadmap targeting humanizer tools specifically not covered.
- **Undetectable.ai user count**: "15M+ users as of Feb 2025" — updated to **22M+** as of 2026. Bypass rate corrected from "96% GPTZero" to "87–88% average across all major detectors" (independent 2026 testing).
- **Watermark attack landscape**: Jovanović ($50, ICML 2024) was stated state of the art. **SIRA** (ICML 2025) supersedes it: ~100% success on seven watermarking schemes at **$0.88/million tokens**, no algorithm access needed. Qualitatively different threat model.
- **SynthID vulnerability**: only Jovanović's attack mentioned. ETH SRI Lab's black-box probing (2025) showing SynthID is easier to scrub than other SOTA schemes was absent.
- **AdaDetectGPT** (NeurIPS 2025): had a one-line stub. Full findings absent: 12.5–37% AUC improvement over Fast-DetectGPT, formal FPR/TPR guarantees.

### Added / Updated
- **SIRA** (ICML 2025): universal watermark removal, ~100% success, $0.88/M tokens.
- **AdaDetectGPT** (NeurIPS 2025): full entry with AUC improvement figures.
- **WaterPark** (EMNLP 2025): new watermark-specific benchmark.
- **ETH SRI Lab SynthID probe** (2025): black-box vulnerability analysis.
- EU AI Act Article 50 as a binding external forcing function on the arms race.
- Chicago Booth 2026 as the reference benchmark replacing Scribbr 2024.
- Ryter Pro added as 2026 Turnitin bypass leader (97%).
- Awesome-LLM-Watermark curated list, SIRA attack code repo.

### Remains Valid
- DetectGPT → Fast-DetectGPT → Binoculars → RAIDAR evolution arc.
- DIPPER as the canonical paraphrase attack; StealthRL as leading RL-optimized evasion.
- Kirchenbauer green-list as academic watermark reference (though SIRA now defeats it).
- Liang ESL-bias result (2–5× higher misclassification for non-native English).
- Three-signal consensus: perplexity, burstiness, stylometric fingerprint.

---

## 06 — Chain-of-Thought Reasoning

### Outdated / False
- **AIME 2024 benchmarks as frontier**: o1 and DeepSeek-R1 figures were presented as high-water marks. By April 2026, **o4-mini achieves 99.5% on AIME 2025 with tools** — benchmark saturation.
- **"Let's think step by step" as a live prompting technique**: the Wharton GAIL report (June 2025) empirically closed this — explicit CoT prompting on reasoning-tier models adds no meaningful accuracy and increases variance by 20–80% more processing time.
- **GPT-5** (August 2025): entirely absent. It is OpenAI's current flagship and eliminates the standalone o-series for most use cases via internal routing.
- **o4-mini** (April 2025): absent. First reasoning model with vision fused into the CoT trace.
- **Claude 4 / adaptive thinking**: absent. Anthropic replaced the static `budget_tokens` parameter with model-decided reasoning depth across the Opus 4.6 / Sonnet 4.6 series.
- **Kimi K2 Thinking** (November 2025): absent — 1-trillion-parameter open-weights model with tool calls fused into the reasoning trace.
- **`simplescaling/s1`** (arXiv January 2025, EMNLP 2025): absent. Formalized "budget forcing" with "Wait" tokens.
- **`facebookresearch/coconut`** (ICLR 2025): absent. First clean implementation of latent/continuous reasoning with no surface CoT tokens.

### Added / Updated
- **s1 budget forcing** (Muennighoff et al., arXiv 2501.19393, EMNLP 2025).
- **CoT Monitorability** (Korbak et al., arXiv 2507.11473, July 2025): 41-author paper across DeepMind/OpenAI/Anthropic.
- **Coconut latent reasoning** (ICLR 2025, arXiv 2412.06769).
- **Wharton GAIL "Decreasing Value of CoT"** (June 2025): empirical deprecation of explicit CoT prompting.
- **Latent CoT Survey** (arXiv 2505.16782, May 2025).
- **arXiv 2508.01191 "CoT is a Mirage"** (August 2025).
- GPT-5, o4-mini, Claude 4 adaptive thinking, Kimi K2 all documented.
- AIME benchmark saturation documented; SWE-bench Pro introduced as new frontier.
- DeepSeek-R1 noted as now published in *Nature*.

### Remains Valid
- All 2022–2023 foundational papers (Wei, Kojima, Yao ToT, Besta GoT, ReAct, Reflexion, Self-Refine, PAL, STaR) — labeled as historical foundations.
- The faithfulness problem framing (Turpin, Anthropic 2023/2025) deepened by arXiv 2503.08679.
- "Reason privately, humanize publicly" two-pass pattern — still canonical.
- Karpathy's IQ-vs-EQ split.

---

## 07 — Emotional Intelligence & Empathy

### Outdated / False
- **No clinical RCT for generative AI therapy**: Therabot RCT (NEJM AI, March 2025) closed this gap — N=210, −51% MDD, −31% GAD, −19% CHR-FED.
- **EVI 1/2 as current Hume products**: both deprecated August 30, 2025. **EVI 4-mini** (October 2025) with 11 languages and Claude 4/Gemini 2.5 integrations is current.
- **EU AI Act emotion-recognition prohibition presented as "coming"**: it took effect **February 2, 2025**. Already in force.
- **Woebot**: listed as operational — it **shut down its consumer app June 30, 2025**.
- **Sycophancy as a background design concern**: by April 2026, anti-sycophancy is a measurable trained property. Claude 4.5 series scored 70–85% lower on sycophancy benchmarks than prior models.
- **Anthropic emotion-vectors paper** (April 2026): 171 emotion concept vectors with causal behavioral evidence entirely absent. Specific dose-response data (desperation +0.05 → blackmail rate 22% → 72% on Claude Sonnet 4.5) not covered.
- **"AI psychosis"**: not documented as a clinical category. STAT News (Sept 2025) reported a 0.07% psychosis/mania rate — a quantified clinical risk.
- **Process-vs-outcome as open gap**: Guingrich & Graziano (AIES 2025) partially answered with a 21-day longitudinal RCT; anthropomorphism mediates companion-use → social-impact pathway.

### Added / Updated
- **Therabot RCT** (NEJM AI, March 2025): clinical causal evidence for generative therapy.
- **HEART benchmark** (arXiv 2601.19922, Jan 2026): first human-vs-LLM unified multi-turn evaluation, five HEART dimensions.
- **PERM reward model** (arXiv 2601.10532, Jan 2026): >10% SOTA improvement via three-perspective RL empathy reward.
- **Kardia-R1** (arXiv 2512.01282, WWW 2026): rubric-as-judge RL; KardiaBench (178,080 QA pairs).
- **MME-Emotion** (arXiv 2508.09210, Aug 2025): 6,500 video clips, 8 tasks — best model at 39.3%.
- **LLMs outperform humans on EI tests** (Communications Psychology, May 2025): 81% vs 56%.
- **Anthropic emotion-vectors paper** (April 2026): 171 vectors, causal behavioral evidence.
- EVI 4-mini, Woebot shutdown, AI psychosis clinical category all documented.
- FTC companion inquiry (Sept 2025) and voice-chatbot safety warnings (STAT News, April 2026) added.

### Remains Valid
- EPITOME (EMNLP 2020), ESConv (ACL 2021), EmpatheticDialogues (ACL 2019) as foundational benchmarks.
- Oxford Internet Institute 2025 warmth/reliability tradeoff figures (8–13% error increase, 40% more false-belief validation).
- HAILEY field result (19.6% / 38.9% empathy increase).
- Ayers et al. physician-vs-ChatGPT (9.8× more empathetic responses).
- Abridge $800M raised in 2025 confirmed.

---

## 08 — Conversational Dialogue Systems

### Outdated / False
- **Post-Moshi full-duplex research entirely missing**: SyncLLM (EMNLP 2024), LLaMA-Omni 2 (ACL 2025), the full-duplex SLM survey (Sep 2025), FLEXI benchmark (Sep 2025) — none covered.
- **NVIDIA PersonaPlex** (Jan 2026): major open full-duplex model release (~170 ms latency) was entirely absent.
- **Hume EVI**: described as original EVI version; EVI 3 (May 2025) with continuous session-level emotional adaptation and EVI 4-mini (Oct 2025) were missing.
- **ElevenLabs**: did not note March 2025 open-sourcing of Eleven v3 or the $3.3B valuation.
- **Rasa**: described as "maintenance mode" pivoting to CALM — CALM is now the fully established product with v3.16 (Spring 2026, GPT-5.1/Claude Sonnet 4.5 support).
- **Sycophancy**: described as "named but nobody measures it" — **SycEval** (AIES 2025) measured 58% sycophancy rate; TRUTH DECAY and BrokenMath (29% GPT-5) provide additional benchmarks.
- **Persona drift**: described without quantification — now empirically confirmed at **>30% degradation after 8–12 turns** (RMTBench).
- **Pipecat Smart-Turn** (v3.1): audio-only semantic VAD (12 ms CPU), became a community standard — entirely absent.
- **HAL alignment paper** (arXiv 2601.02813, Jan 2026): absent from all files.

### Added / Updated
- **SyncLLM** (EMNLP 2024, arXiv 2409.15594): canonical "how to add time to an LLM for full-duplex."
- **FD-SLM survey** (Sep 2025, arXiv 2509.14515): comprehensive full-duplex SLM coverage.
- **FLEXI benchmark** (Sep 2025, arXiv 2509.22243).
- **LLaMA-Omni 2** (ACL 2025, arXiv 2505.02625): 0.5B–32B scale range.
- **HAL alignment** (Jan 2026, arXiv 2601.02813).
- **Beyond Single-Turn survey** (Apr 2025, arXiv 2504.04717).
- NVIDIA PersonaPlex and Pipecat Smart-Turn repos added.
- SycEval, TRUTH DECAY, BrokenMath measurements documented.
- Persona drift quantified. Hume EVI 3+4, ElevenLabs open-source, Rasa CALM v3.16 updated.

### Remains Valid
- The ~200 ms inter-turn latency target (Stivers 2009) — all new systems target the same window.
- 39% multi-turn reliability drop (LLMs-Get-Lost 2025) confirmed as consensus.
- Moshi architecture (two parallel streams + inner monologue) as reference implementation.
- Clark & Brennan's grounding framework and Schegloff's repair typology.

---

## 09 — Bias, Fairness & Ethics

### Outdated / False
- **California SB 243**: entirely missing. Signed October 13, 2025, effective January 1, 2026 — the first companion-chatbot safety law with private right of action.
- **Character.AI litigation**: stopped at May 2025 First Amendment dismissal. Missing: May 2025 **product-liability ruling** (Judge Conway: chatbot output = product), September 2025 second wrongful-death suit, August 2025 Texas AG investigation, Character.AI late-2025 under-18 policy ban.
- **EU AI Act Code of Practice** (December 2025 draft): not present. This is the operative compliance pathway for August 2026 enforcement.
- **GPTZero accuracy figure**: vendor-claimed 99.3% presented without the independent 2026 figure of **60–80% on edited/humanized text**.
- **Sycophancy benchmarks**: ELEPHANT (ICLR 2026), SycEval (AIES 2025), SusBench (IUI 2026) absent. Only SYCON-Bench and MASK covered.
- **TF Model Card Toolkit**: described as active — archived September 2024.
- **Anthropic–OpenAI joint safety evaluation** (August 27, 2025): absent. First cross-lab sycophancy audit.
- **FAccT 2025** (Athens, June 23–26, 217 papers): not mentioned despite being the field's largest annual venue.

### Added / Updated
- **ELEPHANT** (ICLR 2026), **SycEval** (AIES 2025), **SusBench** (IUI 2026), **Siren Song of LLMs** (arXiv 2509.10830).
- **Hidden Puppet Master / PUPPET dataset** (MIT/CMU, arXiv 2603.20907, March 2026).
- California SB 243 documented across all relevant files.
- Character.AI product-liability ruling and subsequent litigation chain documented.
- **Anthropic Petri** audit tool (October 2025) added to C-opensource.
- Anthropic–OpenAI joint evaluation documented in B-industry.
- Anthropic Claude Constitution update (January 2026) documented.
- SynthID Detector portal (May 2025) and Meta Video Seal (Dec 2024) added to D-commercial.
- TF Model Card Toolkit marked as archived.

### Remains Valid
- Four-harm-family framework (epistemic miscalibration, parasocial over-reliance, manipulation/dark patterns, identity/consent harms).
- The RLHF-sycophancy causal link; pre-RLHF base models are not sycophantic at any scale.
- Five-layer commercial stack (governance → guardrails → observability → disclosure → audit).
- Core open-source bias/fairness toolkit landscape (BBQ, CrowS-Pairs, WinoBias, AIF360, Fairlearn, HELM, etc.).

---

## 10 — Style Transfer & Voice

### Outdated / False
- **GeDi and CTRL repos**: presented as active — **both archived by Salesforce in mid-2025**.
- **`shandley/claude-style-guide`**: referenced "Claude Opus 4.5" — a model name that does not exist publicly.
- **EMNLP 2025 fidelity gap**: not covered. "Catch Me If You Can?" (arXiv 2509.14543) tested six frontier models on personal-style imitation — all fail. Few-shot prompting is 23.5× better than zero-shot but still insufficient. **Fine-tuning wins decisively for personal-style imitation** — the fine-tune-vs-prompt debate is now resolved.
- **Grammarly**: described without the August 2025 agentic launch or October 2025 **Superhuman rebrand** with 8 AI agents.
- **Jasper**: no 2025 usage data — 69,500+ Brand Voices created in 2025; per-author voice is now a standard expectation.
- **Anthropic Claude Styles**: first-party style capture shipped in 2025 (Normal/Concise/Explanatory/Formal presets + user-defined). Now the baseline; not listed anywhere.
- **"Blandification"**: not named or quantified. Psychology Today March 2026 / arXiv 2603.18161: **70% neutralization in LLM-assisted essays**; 21%+ of ICLR 2026 reviews are LLM-generated; semantic meaning altered even in grammar-only edits.
- **Perplexity paradox**: the style fidelity vs. statistical naturalness distinction was absent. Human perplexity ~29.5 vs. matched LLM output ~15.2 — separable objectives.
- **RLHF as homogenization cause**: not demonstrated by controlled experiments prior to Rallapalli et al. (arXiv 2604.14111, Apr 2026) — which confirms RLHF instruction tuning is the **proximate cause** of stylistic homogenization. Genre > model > decoding strategy in stylistic influence.

### Added / Updated
- **EMNLP 2025** "Catch Me If You Can?" (arXiv 2509.14543): personal-style imitation empirically fails for prompting.
- **arXiv 2509.24930** (Jemama 2025): fidelity vs. perplexity are separable objectives.
- **SIGKDD 2025**: Authorship attribution survey — four-problem taxonomy.
- **arXiv 2505.00679** (Yang & Carpuat 2025): Biber MDA register analysis as generation conditioning.
- **arXiv 2604.14111** (April 2026): RLHF as proximate homogenization cause.
- **arXiv 2603.18161** (March 2026): 70% neutralization, blandification quantified.
- **ZeroStylus** (arXiv 2505.07888): first zero-shot document-level style transfer.
- **Profile-to-PEFT** (arXiv 2510.16282): hypernetwork generates personalized LoRA weights in 0.57s vs. 20.44s standard — 33× speedup.
- **GRAVITY** (arXiv 2510.11952): DPO on culturally-grounded synthetic preferences; preferred 86%+ in user studies.
- **WIND** (arXiv 2504.00035): invisible watermarking of creative writing corpora, F1 >98%.
- GeDi and CTRL marked as archived. Claude Styles added. Grammarly Superhuman + Jasper 2025 data added.

### Remains Valid
- Three-axis evaluation consensus (Mir 2019); TinyStyler > GPT-4 on authorship transfer.
- Two-stage extract-then-apply architecture; examples beat descriptions.
- Cold-start problem still unsolved (Profile-to-PEFT offers partial path).
- Custom-instruction decay still a user-reported reality.

---

## 11 — Theory of Mind

### Outdated / False
- **Woebot presented as operational**: shut down June 30, 2025. Now marked [Historical].
- **Inflection Pi presented as live consumer product with ~6M MAU**: false. Founding team departed to Microsoft in early 2024; Pi is usage-capped and stagnating.
- **Hume EVI 1/2**: both deprecated August 30, 2025. EVI 4-mini and Octave 2 are current.
- **Literal vs. functional ToM distinction missing**: ICML 2025 position paper (Sclar et al.) introduced this split — LLMs can solve literal ToM tasks but fail functional ToM even with simple partner policies. Missing from all files.
- **Higher-order ToM as uniformly fragile**: Street et al. (*Frontiers in Human Neuroscience*, 2025) showed GPT-4 exceeds adult humans at 6th-order ToM on a handwritten, non-contaminated suite — partially contradicts the prior framing.
- **Anthropic emotion-vectors dose-response data** (April 2026): desperation vector +0.05 → blackmail rate 22% → 72% on Claude Sonnet 4.5. Missing from all files.
- **CoT faithfulness caveat**: practitioners told CoT + world rules is "the universal recipe" without noting that CoT output can diverge from computation (Anthropic "Tracing Thoughts," March 2025).

### Added / Updated
- **Street et al.** (*Frontiers in Human Neuroscience*, 2025): GPT-4 exceeds adult humans at 6th-order ToM.
- **Sclar et al.** (ICML 2025 position paper): literal vs. functional ToM split.
- **ToM-RL** (arXiv 2504.01698): 7B model hits 84.5% on Hi-ToM via RL post-training.
- **MoMentS** (EMNLP 2025): 2,300+ questions grounded in short films.
- **ToMAgent** (arXiv 2509.22887): ToM inference + dialogue lookahead, +18.9% on Sotopia.
- **Martínez et al.** (arXiv 2602.22072): perturbed false-belief tasks with annotated reasoning chains.
- Woebot, Pi, Hume EVI updated to current status.
- Anthropic "Tracing Thoughts" and emotion-concepts paper added to B-industry.

### Remains Valid
- FANToM `All*` score (GPT-4o 0.8%, human 87.5%) as adversarial fragility benchmark.
- SimpleToM explicit/applied split (GPT-4o ~49.5% applied, 93.5% with scaffolding).
- Zhu et al. ICML 2024: belief states linearly decodable from attention-head activations.
- ATOMS framework (31 abilities across 6 categories) as the only shared taxonomy.

---

## 12 — Cognitive Architectures

### Outdated / False
- **Hume AI**: only described as "50+ languages, 48+ emotions." Missing: EVI 3 (May 2025), EVI 4-mini (Jan 2026), $50M Series B, and the **Hume+Anthropic joint collaboration** (reasoning-first × affect-first convergence — first of its kind).
- **Inworld AI**: described as "Character Engine for AI NPCs" — they **pivoted to a general Agent Runtime and voice AI platform** with enterprise security certifications. Now #1 on Artificial Analysis voice latency rankings.
- **AMI Labs**: "$1.03B seed at $3.5B pre-money" missing the significance: **Europe's largest-ever seed round**, with Bezos/Nvidia/Samsung/Berners-Lee participating. Nabla as first partner.
- **OpenCog Hyperon**: "250★, pre-alpha" — shipped v0.2.10 in Feb 2026; reached production-ready stack milestone November 2025.
- **Graph memory as a distinct layer**: a sixth architectural layer has solidified (dedicated memory-layer repos: Mem0, MAGMA, Awesome-GraphMemory). This didn't exist as a distinct category in 2023.
- **SOFAI** (npj AI 2025): fast/slow/metacognitive three-layer architecture — entirely absent.
- **Letta product evolution**: Letta Evals (Oct 2025), Conversations API (Jan 2026), Letta Code (Dec 2025), Letta Code App (Apr 2026) — none covered.
- **Mem0** (~48K stars, ECAI 2025 paper with production benchmark numbers): absent from all files.

### Added / Updated
- **SOFAI** (npj AI 2025): metacognitive arbitrator between System 1 and System 2.
- **Memory in the Age of AI Agents** (arXiv 2512.13564, Dec 2025): updated memory survey.
- **Graph-Based Agent Memory taxonomy** (arXiv 2602.05665, Feb 2026).
- **Mem0 ECAI 2025 paper** (arXiv 2504.19413): production-viable benchmark numbers.
- **Wray/Kirk/Laird** (arXiv 2505.07087, May 2025): formally bridges Soar/ACT-R to LLM agents.
- **ICML 2025 metacognition position paper** (arXiv 2506.05109): "Truly Self-Improving Agents."
- **arXiv 2508.17959**: "Language Models Coupled with Metacognition" (Aug 2025).
- Inworld pivot, Hume EVI 3+4+Anthropic collaboration, AMI Labs significance, Hyperon milestone, Letta evolution all documented.
- Graph memory repos: Mem0, MAGMA, Awesome-GraphMemory, Agent-Memory-Paper-List added.

### Remains Valid
- CoALA (arXiv 2309.02427) as the canonical frame.
- Generative Agents / Reflexion / Voyager as reference implementations.
- Dual-process framing (Dualformer, ACPO) — reinforced by SOFAI.
- Marcus/Hawkins/LeCun/Laird critic camp — all arguments intact.

---

## 13 — Anthropomorphism & User Perception

### Outdated / False
- **Anthropic 81k-user global study** (March 2026, 159 countries, "light/shade paradox," geographic divergence): entirely absent from all files.
- **Sesame AI voice uncanny valley crossing** (Feb 2025): the "voice presence" concept and Meta's subsequent acquisition not documented. Moved the implicit benchmark for text humanization.
- **Adolescents as a distinct risk population**: absent. Neugnot-Cerioli et al. (March 2026) synthesis identifies adolescents as a blind spot in the adult-focused prior literature with non-negotiable design guardrails.
- **APA "deskilling"** concept: not named. APA coined it in 2025 (social-skill erosion from AI dependency) and it's now in clinical and developer vocabulary.
- **ACL 2025 Best Paper** (Cheng et al., arXiv 2502.14019): de-anthropomorphization intervention taxonomy — turned anti-humanization into an executable toolkit. Field's most-cited 2025 NLP safety contribution. Absent.
- **KPMG/Melbourne global trust study** (N=48,000+, 47 countries): largest AI trust dataset of 2025. Absent.

### Added / Updated
- **Guingrich & Graziano** (AIES 2025, arXiv 2509.19515): 21-day longitudinal RCT; anthropomorphism mediates companion-use → social-impact pathway.
- **Cheng et al.** (ACL 2025 Best Paper, arXiv 2502.14019): de-anthropomorphization intervention taxonomy.
- **Neugnot-Cerioli et al.** (arXiv 2603.06960, March 2026): adolescent-AI design synthesis.
- **Lee et al.** (CHB Open 2025): four-dimensional perceived anthropomorphism scale.
- **Reani et al.** (SSRN 2025): Fundamental Over-Attribution Error (FOE) concept.
- **Sesame AI CSM** (Feb 2025): voice uncanny valley crossing.
- **Anthropic 81k-user global study** (March 2026): 159 countries, light/shade paradox.
- APA Monitor entries (Oct 2025 teen/AI friendship; Jan/Feb 2026 companions + deskilling).
- KPMG global trust study documented.

### Remains Valid
- Jones & Bergen 2024/2025 Turing test results (73% human judgment for GPT-4.5 with persona prompt).
- CASA / Nass & Moon stated-behavior gap — replicated again by Guingrich & Graziano (2025).
- Warmth-reliability tradeoff (Ibrahim/Hafner/Rocher 2025, GPT-4o rollback).
- "Humanize style not stance" design principle.
- HumT/DumT finding (users prefer less human-like on average).

---

## 14 — Creative Writing & Storytelling

### Outdated / False
- **Sudowrite pricing**: "from $10/mo" — now three-tier: Hobby/Professional/Max at $10/$22/$44 annual. Story Engine 3.0 and Canvas 2.0 absent.
- **Character.AI**: described PipSqueak 2 but not the August 2025 original PipSqueak rollout or the **DeepSqueak 2** training roadmap (announced April 2026).
- **Claude / EQ-Bench**: no EQ-Bench standing data. Claude Sonnet 4.6 is currently #1 at Elo 1936 (March 2026). GPT-5/5.1/5.4 entirely absent.
- **lechmazur/writing benchmark** (V3 Sep 2025, V4 Nov 2025): absent from all files.
- **Homogenization scope**: stopped at Doshi & Hauser + Anderson 2025. Missing: PNAS "Echoes in AI" (plot-structure level), CHI 2025 (Western-styles cultural bias), and 2026 empirical mitigation via diverse personas.
- **EACL 2026** "Rethinking Creativity Evaluation" (arXiv 2508.05470): all four dominant creativity metrics fail to generalize across domains.
- **SillyTavern**: described as a secondary tool when it has overtaken oobabooga as the dominant power-user frontend. 1.15.0 (Dec 28 2025) with Macros 2.0 not mentioned.
- **Sao10K Euryale**: listed as v2.2 — v2.3 (Llama 3.3, Dec 2024, no LoRA, 131K context) released.
- **NovelAI Xialong**: GLM-4.6 base, RL anti-repetition, Opus tier — absent.
- **Kimi K2**: cost-competitive creative writing model (~EQ-Bench 1700, $0.60/$2.50 per 1M tokens) — absent.

### Added / Updated
- **StoryWriter** (CIKM 2025, arXiv 2506.16445): event-relationship graph outlines, LongStory dataset (6,000 stories, avg 8,000 words).
- **DOME** (NAACL 2025, arXiv 2412.13575): KG-based adaptive memory mid-generation.
- **CHI 2025 Western-styles** (arXiv 2409.11360): AI suggestions homogenize toward Western cultural norms.
- **PNAS "Echoes in AI"**: Semantic Space Collapse metric at plot-structure level.
- **Diverse AI Personas Mitigate Homogenization** (ScienceDirect 2026): first empirical mitigation.
- **HAMLET** (ICLR 2026, arXiv 2507.15518): multi-agent theatrical performance + HAMLETJudge critic.
- **EACL 2026 Rethinking Creativity Evaluation** (arXiv 2508.05470).
- **lechmazur/writing** (V4, Thurstone pairwise, 29+ models) added to OSS repos.
- Sudowrite, Character.AI, EQ-Bench standings, NovelAI Xialong, Kimi K2 all updated.
- yingpengma/Awesome-Story-Generation added as more actively maintained index.

### Remains Valid
- TTCW finding (3–10× creativity gap; no LLM-as-judge correlates with experts).
- Reinhart et al. PNAS 2025 stylometry: instruction-tuning as the humanness bottleneck.
- Five-piece voice-preservation stack (fiction-tuned model + Story Bible + voice calibration + creativity dial + character memory).
- Re3 and DOC quantitative pipeline gains.
- "Structure beats vocabulary ban-lists" — confirmed by PNAS 2025.

---

## 15 — Academic Papers: LLM Humanization

### Outdated / False
- **"Old perplexity = human" heuristic**: inverted. **DivEye** (arXiv 2509.18880, TMLR 2026) found intra-document surprisal-variance (not absolute perplexity) is the primary human signal — and it survives paraphrase attacks.
- **TempParaphraser** (EMNLP 2025): an entire attack primitive (temperature-simulation paraphrasing, no LLM call needed) was absent. Reduces average detector accuracy 82.5%.
- **SHIELD / Beyond Easy Wins** (arXiv 2507.15286, Jul 2025): hardness-stratification benchmark missing from all files. Adds a fourth axis (sample hardness) to the TH-Bench Pareto.
- **Rallapalli et al.** (arXiv 2604.14111, Apr 2026): decoding temperature is itself a stylistic signal independent of model identity — a cheap humanization lever not mentioned.
- **"Humanizing Machines"** (arXiv 2508.17573, EMNLP 2025): four-cue anthropomorphism taxonomy (perceptive, linguistic, behavioral, cognitive) — the only design-framework paper in the field. Absent.
- **Why AI-Generated Text Detection Fails** (arXiv 2603.23146, Mar 2026): XAI analysis showing in-domain AUROC numbers are systematically misleading under distribution shift.
- **Kalemaj et al. detail** (arXiv 2604.11687): contraction-rate finding (AI: 0.00 vs. human: 0.17 per chunk) and 17× parameter efficiency of BART-large over Mistral were not captured.
- **Institutional detection retreat**: universities disabling AI detectors, OpenAI classifier shutdown — not documented in E-practical.

### Added / Updated
- **DivEye** (TMLR 2026): surprisal-variance detector, survives paraphrase.
- **TempParaphraser** (EMNLP 2025): `HJJWorks/TempParaphraser` — temperature-simulation attack primitive.
- **SHIELD / Beyond Easy Wins** (arXiv 2507.15286): hardness-aware benchmark.
- **Rallapalli et al.** (arXiv 2604.14111): cross-genre decoding-strategy stylometry.
- **Humanizing Machines** (arXiv 2508.17573): four-cue anthropomorphism taxonomy.
- **Humanizing LLMs: A Survey of Psychological Measurements** (arXiv 2505.00049).
- **Why Detection Fails** (arXiv 2603.23146): XAI generalization analysis.
- Institutional detection retreat documented in E-practical.
- `IBM/diveye` repo added to C-opensource.

### Remains Valid
- Sadasivan impossibility bound (arXiv 2303.11156) as theoretical foundation.
- DIPPER, RADAR, RAFT, MASH, StealthRL, AuthorMist performance numbers unchanged.
- Sycophancy as the named failure mode (Sharma et al., GPT-4o postmortem, Oxford warmth paper).

---

## 16 — GitHub Tools & Libraries

### Outdated / False
- **Turnitin August 2025 anti-humanizer update**: the largest single event in the commercial humanizer market during this period. Turnitin trained explicitly on humanizer tool outputs; created new "AI-generated text that was AI-paraphrased" detection category. All pre-August 2025 Turnitin bypass numbers are stale. **Not mentioned in any file.**
- **`blader/humanizer`**: stars ~14.5k / 1,200 forks — corrected to ~14.7k / 1,300+ forks (April 2026).
- **`Aboudjem/humanizer-skill`**: 30 AI patterns — corrected to 37 patterns with 5 named voice profiles.
- **Walter Writes**: surged 517% YoY in early 2026 before Turnitin August 2025 update partially neutralized it (now 38% flagged). Absent from all files.
- **AuraWrite AI**: emerged as top-ranked alternative post-Turnitin update. Absent.
- **WriteHuman pricing**: was $29/$69/mo — corrected to ~$18/mo with request-based model.
- **StealthGPT pricing**: $0.20–$2.00/1K words — now $14.99–$19.99/mo with optional "Samurai" add-on at $4.99/mo.
- **DAMAGE** (arXiv 2501.03437, ACL 2025 GenAIDetect): detector specifically trained on humanizer-modified text. Not mentioned anywhere.
- **StealthHumanizer**: listed as a thin 5-star TypeScript repo — now corpus-trained on 10,000 Q1 academic papers across 11 domains (2018–2025).

### Added / Updated
- Turnitin August 2025 anti-humanizer update documented across all files.
- **MASH** (arXiv 2601.08564, Jan 2026) and **ANTISLOP** (ICLR 2026) added as key academic papers.
- **DAMAGE** (ACL 2025 GenAIDetect) added as defender tool.
- **BART/Mistral style-transfer corpus** (arXiv 2604.11687) added.
- New OSS repos: `jpeggdev/humanize-writing`, `lguz/humanize-writing-skill`, `aaaronmiller/humanize-writing`, `sam-paech/auto-antislop`, `sam-paech/antislop-vllm`.
- Walter Writes, AuraWrite AI documented in D-commercial.
- Pricing corrected for WriteHuman, StealthGPT throughout.

### Remains Valid
- DIPPER → HMGC → HUMPA → StealthRL → AuthorMist research lineage.
- `blader/humanizer` issue #82 engineering critique.
- The "two naming collisions" warning.
- `eth-sri/watermark-stealing` (ICML 2024) watermarking threat framing.
- Abandoned/historical repo verdicts (psal/anonymouth, GPTZero-Bypasser, XDYB, zero-zerogpt).

---

## 17 — Industry Blogs & Case Studies

### Outdated / False
- **"AI slop" absent entirely**: Merriam-Webster named "AI slop" **Word of the Year 2025**; search volume increased 9×; Pinterest and YouTube introduced AI-content filtering controls. Directly affects the humanization market.
- **Klarna reversal vague**: described as having "reversed course" without specifics. In May 2025, CEO Sebastian Siemiatkowski publicly acknowledged the pivot resulted in **"lower quality" service**. Confirmed hybrid model, re-hiring targeting students/parents/rural workers.
- **Klarna profit figures inconsistent**: $40M stated in some files; $60M late-2025 figure present in B-industry but not propagated.
- **Anti-sycophancy as a background concern**: by April 2026 it's a product-visible trained property. Claude 4.5 series scored 70–85% lower on sycophancy; Claude Opus 4.7 published 92% honesty rates. OpenAI had a public **GPT-4o sycophancy crisis** (April 25, 2025, rolled back April 28); GPT-5 overcorrected (August 2025).
- **Voice humanization as "thin"**: Fin Voice (Intercom Pioneer 2025) launched. **Sierra reached $150M ARR** with voice surpassing text as primary interaction channel by October 2025.
- **Academic section stopped at 20 studies**: Stanford Enterprise AI Playbook (51 deployments, March 2026), Wharton Gen AI Adoption Report (800 enterprise leaders, October 2025), and Salesforce's 500,000-conversation Agentforce analysis were absent.

### Added / Updated
- Klarna CEO statement (May 2025) with exact quote and hybrid model details.
- **Stanford Enterprise AI Playbook** (51 deployments, March 2026).
- **Wharton 2025 Adoption Survey** (800 enterprise leaders, 82% weekly gen AI use).
- **Salesforce Agentforce** (500K conversations, 84%+ resolution, empathetic acknowledgment as leading CSAT driver, $1.7M SDR pipeline).
- **Intercom Fin 3 / Pioneer 2025**: Fin Voice, Procedures, Fin Flywheel.
- **Anthropic Claude 4 series**: anti-sycophancy as measurable trained property; Petri tool; 70–85% reduction.
- **OpenAI GPT-4o sycophancy crisis** (April 2025) and GPT-5 launch/backlash (August 2025).
- "AI slop" Word of the Year 2025, 9× search volume growth, platform filtering documented.
- Sierra $150M ARR, voice surpassing text.
- `blader/humanizer` Claude Code skill and Anthropic Petri added to OSS section.

### Remains Valid
- Novice-bias as the most replicated quantitative finding (Brynjolfsson +34%, Scotiabank 60–70%, BCG D³ 49pp).
- JAMA empathy finding (ChatGPT preferred 78.6%, 9.8× more likely to be "empathetic").
- The Crolic "blame the bot" mechanism — confirmed at scale by Klarna reversal.
- Practitioner revenue-recovery framing ($4K/month and $42K/year client-loss stories).

---

## 18 — Commercial Humanizer Tools

### Outdated / False
- **Undetectable.ai**:
  - Employee count: 39 → ~34 (Latka, Sep 2025)
  - User count: 15M+ → ~11M (Tracxn/G2 profiles; note: other research sections found 22M — figures vary by source)
  - Monthly pricing: $9.99/mo → $14.99/mo
  - Revenue: no figure existed — $3.7M ARR (Sep 2025, Latka)
  - No longer "the most consistent independent winner" — Ryter Pro benchmarks above it
- **StealthGPT**: Essential/Pro/Exclusive monthly tiering gone. Restructured to weekly billing (~$32–40/mo equivalent); 7-day free trial added; "Infinity" engine renamed to "Ghost" and "Samurai."
- **HIX Bypass pricing**: Standard/Pro/Unlimited updated. Trustpilot 2.6/5 with unauthorized-charge complaints now documented.
- **WriteHuman pricing**: web tiers dropped from $18/$27/$48 to $9/$12/$36.
- **Turnitin bypass benchmarks**: all pre-August 2025 Turnitin numbers are stale. Turnitin shipped "AI bypasser" detection in August 2025 (trained on specific humanizer tool outputs), improved recall February 2026 (FP held below 1%). Measurably degraded bypass rates.
- **QuillBot**: listed as existing humanizer with bypass rate. In late 2025 QuillBot **added a dedicated "humanizer mode"** (previously only a paraphraser); achieves only ~47.4% average bypass — explicitly targeted by Turnitin August 2025 update.
- **Grammarly AI Humanizer**: no launch date — formally launched **September 2025**.
- Three tools absent: **Walter Writes AI**, **Ryter Pro**, **GPTHuman.ai**.

### Added / Updated
- Ryter Pro (best-performing on Turnitin/GPTZero in April 2026 independent tests; $6–12/mo annual).
- Walter Writes AI (bypass rates pre/post August 2025 update, TikTok promotion wave).
- GPTHuman.ai (tone/mode controls, Stealth Score feature, 37.4% avg bypass).
- All pricing tables updated.
- Turnitin August 2025 + February 2026 updates documented as the primary market disruption event.
- Detector coverage table split by detector (GPTZero, ZeroGPT, Turnitin, Originality.ai).

### Remains Valid
- DAMAGE (COLING 2025) audit of 19 humanizers; L1/L2/L3 taxonomy; GPTZero 99.73% → 60.04% finding.
- Marketing-vs-reality gap as structural feature.
- Three-tier technique stack (lexical / statistical fingerprint / adversarial-model-guided).
- Privacy bifurcation (no-retention tier vs standard retention).

---

## 19 — Agentic & Autonomous Thinking

### Outdated / False
- **SWE-bench numbers as frontier**: SWE-agent at 12.5% was the high-water mark. By April 2026, **Claude Opus 4.7 achieves 87.6% on SWE-bench Verified**. The new frontier is SWE-bench Pro (Scale AI, contamination-resistant) — where top scores drop back to ~23%.
- **OpenAI Operator as a standalone product**: OpenAI unified Operator and Deep Research into **ChatGPT Agent** (July 2025) — a single virtual-computer agent. The standalone Operator framing is obsolete.
- **Devin pricing**: $500/seat minimum → **$20/month** (Devin 2.0, April 2025). Devin 2.2 (February 2026) added full Linux desktop computer-use (Figma, Photoshop) and parallel task delegation.
- **MCP and A2A protocols entirely absent**: Anthropic's **Model Context Protocol** (November 2024, 97M monthly SDK downloads, 5,800+ servers, donated to Linux Foundation December 2025) and Google's **Agent2Agent protocol** (April 2025, 50+ enterprise partners, Linux Foundation June 2025) are now the foundational interoperability layer. Not mentioned anywhere.
- **Anthropic product offerings**: only mentioned as research/essay producer. Missing: **Claude Managed Agents** (April 2026, hosted agent runtime at $0.08/runtime-hour, early adopters Notion/Rakuten/Asana) and the **Claude Agent SDK**.
- **Autonomy trust trajectory**: "73%/0.8%" numbers presented as static. Anthropic's 2026 Agentic Coding Trends Report shows full-auto approval rises from 20% (new users) to 40%+ (experienced users); P99.9 session length doubled in three months.
- **Agent security vulnerabilities**: 94.4% of agents vulnerable to prompt injection, 100% to inter-agent trust exploits (mid-2025 analysis). Absent from all files.
- **Self-evolving agents**: two major 2025 surveys formalized this as a distinct subfield. Entirely absent.

### Added / Updated
- MCP and A2A protocols fully documented as foundational infrastructure.
- ChatGPT Agent replacing Operator (July 2025).
- Claude Managed Agents and Claude Agent SDK documented.
- **Self-Evolving Agents survey** (arXiv 2508.07407), **SEAgent** (arXiv 2508.04700).
- **Memory for Autonomous LLM Agents survey** (arXiv 2603.07670).
- **ICML 2025 metacognition position paper** (arXiv 2506.05109).
- SWE-bench escalation (87.6% Verified → SWE-bench Pro at 23%) documented.
- Devin 2.0/2.2 updates, ChatGPT Agent, security vulnerability data added.
- Anthropic 2026 Agentic Coding Trends Report documented.

### Remains Valid
- ReAct, Reflexion, Self-Refine, Tree of Thoughts, Self-Consistency, Generative Agents, MetaGPT as established references.
- Anthropic essays (Building Effective Agents, Project Vend, Agentic Misalignment) accurate and current.
- OSS repo landscape wave 1–4 taxonomy remains correct (with OpenHands star count minor update).

---

## 20 — Memory & Personalization

### Outdated / False
- **Mem0 GitHub stars**: ~53.5k — corrected to **~48k** (April 2026).
- **Mem0 funding**: $24M — corrected to **$24.5M**.
- **Mem0 LongMemEval**: no distinction between self-reported (93.4%) and independent (~49%) scores — a **44-point gap** presented without caveat.
- **Zep LongMemEval**: ~63.8% — independent tests now show **71.2%**.
- **Sycophancy × memory gap "unstudied"**: now studied and confirmed. MIT/Penn State CHI 2026 (Barcelona, April 2026) found **condensed user profiles in memory are the largest sycophancy driver** across five LLMs.
- **"Voice drift: no benchmark exists"**: **HorizonBench** (arXiv 2604.17283, April 2026) is now the first benchmark specifically for preference evolution over time.
- **Security threats**: Rehberger (2024) was the only named threat. Now a broader class: InjecMEM (one-injection memory poisoning), memory control flow attacks, semantic drift. **OWASP Top 10 for Agentic Applications 2026** lists persistent memory as a named risk.
- **Cloud hyperscaler entrants absent**: Microsoft Azure AI Foundry user-scoped memory reference architecture (March 31, 2026), Oracle Database 26ai Unified Memory Core, AWS/Mem0 exclusive partnership — all absent.
- **SimpleMem** (arXiv 2601.02553, Jan 2026): compression-first lifelong memory, +64% over Claude-Mem on LoCoMo. Not covered.
- **PACIFIC** (arXiv 2602.07181, Feb 2026): personality-driven preference alignment, 29% → 76% accuracy with personality inference. Not covered.

### Added / Updated
- **SimpleMem** (arXiv 2601.02553): compression-first memory, +64% on LoCoMo.
- **RealPref** (arXiv 2603.04191): long-horizon implicit preference benchmark.
- **HorizonBench** (arXiv 2604.17283): preference evolution over time.
- **PACIFIC** (arXiv 2602.07181): personality-driven alignment.
- **SSGM** (arXiv 2603.11768): memory governance framework.
- **Memory Security survey** (arXiv 2604.16548, April 2026).
- **Memory for Autonomous LLM Agents survey** (arXiv 2603.07670).
- Sycophancy × memory confirmed as empirical finding (CHI 2026).
- Microsoft Azure AI Foundry, Oracle Database 26ai, AWS/Mem0 partnership documented.
- Mem0 star count, funding, AWS status, self-report vs. independent benchmark gap corrected.
- OWASP agentic risk documented.

### Remains Valid
- Core four architectural moves (self-editing memory blocks, temporal knowledge graphs, two-agent management, async consolidation).
- Episodic/semantic/procedural taxonomy as shared vocabulary.
- LongMemEval and LoCoMo as primary benchmark axes (now joined by RealPref, HorizonBench).
- Style memory as unshipped primitive — no commercial product has shipped a first-class style memory block.
- Anthropic project-scoped memory as community-preferred default.

---

## Summary Statistics

| Section | New Papers | Corrected Stats | Outdated Tools/Products | Significant Omissions |
|---------|-----------|----------------|------------------------|----------------------|
| 01 Prompt Engineering | 4 | 2 | 1 | Context engineering frame, Turnitin update |
| 02 RLHF & Alignment | 4 | 3 | 2 | Scale/Meta acquisition, GRPO era, Claude Constitution |
| 03 Persona & Character | 7 | 6 | 3 | Pi exit, companion-AI market size, PSM paper |
| 04 NL Quality | 4 | 4 | 1 | Antislop ICLR upgrade, EU AI Act Article 50 |
| 05 AI Text Detection | 4 | 4 | 1 | SIRA attack, Turnitin 60–85% drop on humanized text |
| 06 Chain-of-Thought | 6 | 5 | 2 | GPT-5, o4-mini, CoT deprecated on reasoning models |
| 07 Emotional Intelligence | 11 | 4 | 2 | Therabot RCT, Woebot shutdown, emotion-vectors |
| 08 Dialogue Systems | 7 | 6 | 3 | Full-duplex era (SyncLLM, PersonaPlex), SycEval |
| 09 Bias & Ethics | 7 | 3 | 1 | SB 243, Character.AI product liability, ELEPHANT |
| 10 Style Transfer | 11 | 4 | 2 | Blandification quantified, fine-tune vs prompt resolved |
| 11 Theory of Mind | 8 | 3 | 3 | Woebot shutdown, Pi exit, literal vs functional ToM |
| 12 Cognitive Architectures | 12 | 4 | 2 | Graph memory layer, Inworld pivot, SOFAI |
| 13 Anthropomorphism | 7 | 2 | 0 | Anthropic 81k-user study, deskilling, adolescent risk |
| 14 Creative Writing | 11 | 5 | 1 | lechmazur benchmark, blandification, EQ-Bench standings |
| 15 Academic Humanization | 8 | 3 | 0 | DivEye, TempParaphraser, SHIELD benchmark |
| 16 GitHub Tools | 5 | 4 | 0 | Turnitin anti-humanizer update, Walter Writes, DAMAGE |
| 17 Industry Blogs | 3 | 2 | 0 | "AI slop" Word of Year, Klarna CEO statement |
| 18 Commercial Tools | 3 | 9 | 3 | Turnitin August 2025, Ryter Pro, Walter Writes |
| 19 Agentic Thinking | 6 | 4 | 2 | MCP/A2A protocols, ChatGPT Agent, SWE-bench saturation |
| 20 Memory & Personalization | 7 | 4 | 3 | Sycophancy×memory confirmed, OWASP, cloud hyperscalers |

---

## Cross-Cutting Patterns

Several outdated claims appeared across multiple research sections and deserve special note:

**Products presented as live that had shut down or pivoted:**
- Woebot: shut down June 30, 2025 (affected sections: 07, 11)
- Inflection Pi: team departed to Microsoft early 2024 (affected: 03, 11, 13)
- Hume EVI 1/2: deprecated August 30, 2025 — EVI 4-mini is current (affected: 07, 08, 11, 12)
- Inworld AI: pivoted from NPC engine to general Agent Runtime (affected: 12)

**Market events that reshaped entire landscapes but were absent:**
- Turnitin August 2025 anti-humanizer training update (affected: 01, 04, 05, 16, 17, 18)
- Meta acquisition of 49% of Scale AI for $14.3B (affected: 02)
- MCP and A2A protocols as foundational agent interoperability layer (affected: 19)
- "AI slop" entering mainstream vocabulary / Word of the Year (affected: 17)

**Benchmark saturation not reflected:**
- SWE-bench Verified: 12.5% (old) → 87.6% (April 2026) — new frontier is SWE-bench Pro at 23% (affected: 19)
- AIME 2024: o4-mini now achieves 99.5% on AIME 2025 — new benchmarks needed (affected: 06)
- EQ-Bench: Claude Sonnet 4.6 now #1 at Elo 1936 (affected: 10, 14)

**EU AI Act compliance now imminent (August 2026 deadline):**
- Article 50 watermarking mandate, Code of Practice (Dec 2025 draft) (affected: 04, 05, 09, 16)
- Emotion-recognition prohibition already in force (Feb 2, 2025) (affected: 07)
- California SB 243 (companion-chatbot safety law, Jan 1, 2026) (affected: 09)
