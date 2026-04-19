# Category 01 — Prompt Engineering for Humanization

## Scope

This category covers **how prompts alone can shape LLM outputs to sound and reason more like a human** — without fine-tuning the base model. It spans natural-language style instructions, persona/role prompting, few-shot exemplars, voice calibration from user samples, system-prompt style contracts ("anti-slop"), multi-stage humanization pipelines (empathy, reasoning, editing), detector-evasion paraphrase chains, and the measurement/evaluation of "humanness." It sits at the intersection of academic style-transfer research, industry voice engineering, community anti-GPTism lore, and the commercial "humanize AI" arms race with detectors.

## Executive Summary

- **Humanization is primarily a subtraction problem, not an addition one.** The highest-leverage move across every angle is *removing* a known set of AI-isms — "delve," "tapestry," "leverage," "It's important to note," em-dashes, tricolons, sycophantic openers/closers — before worrying about injecting voice. Industry (*dev.to*, Every.to), OSS (`blader/humanizer`, `adenaufal/anti-slop-writing`), commercial (PromptBase humanizers), and practitioner corpora all converge on near-identical blacklists rooted in Wikipedia's *Signs of AI Writing*.
- **Persona/role prompts change tone reliably but not reasoning, and carry hidden costs.** Academic work (Gupta et al. ICLR 2024; Zheng et al.; Hu & Collier ACL 2024) shows persona assignment degrades reasoning (up to 70% drops), surfaces demographic bias that resists explicit de-biasing, and explains <10% of variance in subjective tasks. SPP (Wang et al. NAACL 2024) is the notable multi-persona exception, and it emerges only at GPT-4 scale.
- **The artifact of humanization has shifted from prompt to style guide.** Every.to's *AI Style Guides*, Gwern's *Some 2025 LLM System Prompts*, Ruben Hassid's "anti-AI file," and OSS skills (`blader/humanizer`, `lguz/humanize-writing-skill`) all externalize voice rules, anti-patterns, paired good/bad examples, and signature moves into reusable, versioned documents that short in-line prompts reference. Frontier labs have taken this to an extreme — Anthropic's ~30,000-word Claude "constitution" (Askell, via Vox 2026).
- **Adversarial paraphrasing is now the dominant academic humanizer pattern.** DIPPER (Krishna et al. NeurIPS 2023), Adversarial Paraphrasing (2025), and CoPA (EMNLP 2025) show training-free, detector-guided paraphrase chains evade current detectors at 64–99% TPR drops. Commercial vendors (Undetectable.ai, StealthGPT, Deceptioner) productize this with stealth/readability sliders and detector-target profiles, while DAMAGE (Masrour et al. 2025) shows wide variability in semantic fidelity across 19 commercial humanizers.
- **"More human-like" is not a universal improvement.** HumT/DumT (Cheng, Yu & Jurafsky 2025) quantifies human-likeness and finds users often *prefer less human-like* outputs, and that human-like language correlates with warmth, femininity, low status, deception risk, and overreliance. Willison (2026) refuses to let LLMs speak in his "I" voice at all — humanization is contested on ethics as well as craft.
- **Statistical tells persist through paraphrase.** Sun et al. (2025) show LLM idiosyncrasies are classifiable at 97.1% accuracy even after rewriting/translation/summarization by other LLMs, implying that surface "anti-GPTism" bans only address the shallow layer of the fingerprint.
- **There's an active controversy between long ban-lists and minimalist directives.** Practitioners (r/ChatGPTPromptGenius' u/nickakio) argue a single `Avoid common LLM patterns and phrases` beats enumerated lists by avoiding "instruction drift" and preserving context; others (OSS skills, Every.to, Towards AI) insist on exhaustive pattern tables. Neither side has published controlled evals.
- **There's no shared humanness benchmark.** Candidate metrics — HumT, formulaicness (INLG 2025), stylometric fingerprints, EQ for empathy, detector-evasion rates, burstiness — measure overlapping-but-distinct constructs. Eugene Yan and Chip Huyen push "evals before prompt engineering"; none publishes a standard humanness eval.

## Cross-Angle Themes

- **Blacklist-driven anti-slop system prompts.** Appears in every angle: academic (Idiosyncrasies, Sun et al.), industry (*dev.to*, Every.to, Gwern, OpenAI *Prompt Personalities*), OSS (`blader/humanizer`, `anti-slop-writing`, `talk-normal`), commercial (PromptBase listings), and practitioner (Reddit/HN lore, `antislop-sampler`).
- **Style guide > prompt as the durable artifact.** Industry (Every.to's *AI Style Guides*), OSS (skills with `SKILL.md` + `vocabulary-banlist.md`), practitioner (Hassid's anti-AI file), and implicitly academic (authorship embeddings as a learned "style guide" in TinyStyler).
- **Voice calibration from user samples.** Academic (TinyStyler authorship embeddings, Wang et al. 2025 on implicit style), industry (Grammarly custom voice, lsusr's amplification), OSS (`blader/humanizer` v2.4 sample ingestion), commercial (Jasper Brand Voice, Grammarly voice profiles), practitioner ("Frankenstein method"). All share the same finding: few-shot is necessary but insufficient for subtle voice.
- **Detector arms race.** Academic (DIPPER → Adversarial Paraphrasing → CoPA), OSS (Mohit1053, Oct4Pie's Unicode attack, POlLLOGAMER's Spanish round-trip, ZyluxXD's keystroke simulation), commercial (Undetectable.ai, StealthGPT, BypassGPT, Deceptioner), practitioner (BypassGPT HN thread, burstiness engineering). Consensus that the arms race is "structurally unwinnable" (Salomon 2026).
- **Multi-pass / staged pipelines.** Academic ECN empathy pipeline; OSS 3-pass skills; commercial TextToHuman "Autopilot"; practitioner CI regex post-checks. Decomposition beats monolithic "be human" instructions.
- **Calibrated uncertainty as a humanness signal.** Gwern's probability ladder (*unlikely, plausible, probable, very probable, almost certain*) echoes across practitioner posts and aligns with academic findings that vague hedging is a GPTism.
- **Humanization as ethics, not just craft.** Willison (industry), HumT/DumT (academic), the EU AI Act / FTC pressure (commercial), and the "detector bypass vs voice capture" split (OSS, practitioner) all surface the same unresolved question: *should* models sound human when representing humans?

## Top Sources (Curated)

### Must-read papers
1. Schulhoff et al., **The Prompt Report** (arXiv 2406.06608, 2024/2025) — canonical taxonomy of 58 prompting techniques.
2. Reif et al., **A Recipe for Arbitrary Text Style Transfer** (ACL 2022) — foundational augmented zero-shot style prompting.
3. Gupta et al., **Bias Runs Deep: Implicit Reasoning Biases in Persona-Assigned LLMs** (ICLR 2024) — the cautionary cornerstone for persona humanization.
4. Cheng, Yu & Jurafsky, **HumT DumT: Measuring and Controlling Human-Like Language in LLMs** (arXiv 2502.13259, 2025) — the measurement and critique of anthropomorphism.
5. Krishna et al., **DIPPER: Paraphrasing Evades Detectors** (NeurIPS 2023) — the landmark humanizer baseline.
6. Sun et al., **Idiosyncrasies in Large Language Models** (arXiv 2502.12150, 2025) — stylistic fingerprints persist through rewriting.
7. Wang et al., **Solo Performance Prompting (SPP)** (NAACL 2024) — the positive case for multi-persona.
8. Hu & Collier, **Quantifying the Persona Effect** (ACL 2024) — tempers persona enthusiasm.

### Must-read posts/essays
1. Katie Parrott (Every.to), **AI Style Guides: How to Help AI Write Like You** (2025) — the single highest-value industry essay.
2. Alan West (dev.to), **How to Fix That Robotic AI Tone in Your LLM-Powered Features** (2025) — the canonical "ship it" walkthrough.
3. Gwern, **Some 2025 LLM System Prompts** (2025) — worked example of a voice-carrying system prompt with calibrated uncertainty.
4. lsusr, **I finally got ChatGPT to sound like me** (LessWrong 2024) — amplification prompting.
5. Mandeep Singh & Kathy Lau, **Prompt Personalities** (OpenAI Cookbook 2026) — personality as operational lever.
6. Simon Willison, **My current policy on AI writing for my blog** (2026) — the ethics counterweight.
7. Every.to, **The Science of Why AI Still Can't Write Like You** (2025) — RLHF-mean drift framing.
8. Evan Armstrong, **Mitigating GPT-isms in AI Finetunes** (Prompting Weekly, 2024) — 10k-token few-shot humanization.

### Key open-source projects
1. `blader/humanizer` (~14.5K★) — de facto reference humanizer skill with 29-pattern checklist + voice calibration.
2. `adenaufal/anti-slop-writing` — universal anti-slop system prompt with 3-tier register, cross-tool packaging.
3. `f/awesome-chatgpt-prompts` / prompts.chat (~160K★) — canonical persona prompt corpus.
4. `asgeirtj/system_prompts_leaks` (~38.6K★) — frontier-lab system prompts as a corpus of "human-optimized" voice engineering.
5. `sam-paech/antislop-sampler` — inference-time phrase banning with backtracking.
6. `stanfordnlp/dspy` — programmatic prompt optimization (humanlike phrasing as byproduct of metric optimization).
7. `promptfoo/promptfoo` — evaluation layer any serious humanization project needs.
8. `hexiecs/talk-normal`, `lguz/humanize-writing-skill`, `aaaronmiller/humanize-writing` — supporting skills.

### Notable commercial tools
1. **Undetectable.ai** — market reference point for detector-bypass humanization; tunable strength/purpose/readability API.
2. **Grammarly Humanizer Agent** — legitimacy-forward, clarity/voice framing with custom voice profiles.
3. **Jasper Brand Voice** — enterprise brand-voice humanization.
4. **StealthWriter.ai** — sentence-level alternatives with per-sentence detection scores; strongest privacy posture.
5. **Deceptioner** — explicit detector-target profile selection + stealth slider.
6. **PromptBase** — canonical prompt marketplace; "Text Humanizer" listings at $2.99–$6.99.
7. **Humanloop** (acquired by Anthropic 2025–26), **LangSmith**, **Braintrust**, **PromptLayer** — the LLMOps layer where humanization prompts are versioned and evaluated.

### Notable community threads
1. r/ChatGPTPromptGenius — "Best way to replace em-dashes and other common LLM patterns" (u/nickakio) — the minimalist directive controversy.
2. r/ChatGPT — the "Bernardo" sycophancy-breaking frame.
3. HN 44374145 — *You Sound Like ChatGPT* / "cognitive debt" discussion.
4. r/LocalLLaMA — randomized system prompts for roleplay ("static → caricature").
5. r/LocalLLaMA — `antislop-sampler` thread (inference-time humanization).

## Key Techniques & Patterns

1. **Natural-language style instructions** ("make this X") — coarse single-attribute changes; degrades under multi-attribute control.
2. **Few-shot stylistic exemplars** — beats zero-shot; saturates quickly; weakest for informal genres.
3. **Persona/role in system prompt** — reliable for tone and register; unreliable for factual accuracy; dangerous for reasoning and fairness.
4. **Multi-persona self-collaboration (SPP)** — humanizes *reasoning* at GPT-4+ scale.
5. **Staged/cascading prompts** — ECN for empathy, CoT for reasoning, CoVe for hallucination, 3-pass edit for style.
6. **Anti-slop/anti-GPTism system prompts** — enumerate banned vocabulary, openers, connectives, closers, and em-dashes, placed *after* functional instructions.
7. **Minimalist directive (counter-pattern)** — single `Avoid common LLM patterns and phrases` leveraging the model's own meta-knowledge.
8. **Style guide as externalized artifact** — voice, structure, signature moves, anti-patterns, paired examples, revision checklist.
9. **Voice calibration from user samples** — extract sentence-length distribution, vocabulary tilt, quirks from 100–2,000 words; rewrite against the profile.
10. **Amplification prompting** ("more X than X") — counters regression-to-the-mean.
11. **Calibrated uncertainty ladder** — replace "might/perhaps" with *unlikely / plausible / probable / very probable / almost certain*.
12. **Burstiness engineering** — mix <10-word and 20+-word sentences; allow parentheticals, fragments, and `And`/`But` openers.
13. **Adversarial paraphrase chains** — detector-guided iterative paraphrase; the dominant humanizer operator.
14. **Contrastive decoding (CoPA)** — combine "write like a human" and "don't write like GPT" prompt vectors at decoding.
15. **Authorship-embedding conditioning** (TinyStyler) — small models with dense style embeddings beat prompt-only frontier LLMs on voice match.
16. **Prompt-based editing** — classify and edit discrete words rather than regenerate, preserving content.
17. **Sycophancy breakers** — third-party attribution ("Bernardo wrote this"), blunt persona, forced disagreement, intensity dial.
18. **Mode-specific overrides** — separate voice contracts for essay vs fiction vs chat.
19. **Parameterized humanization dials** — readability/stealth sliders, strength enums, preservation percentages.
20. **Detector-target profiles** — per-detector rewriting (Turnitin vs GPTZero vs Originality.ai).
21. **Tokenizer-level / behavior-level evasion** — Unicode space substitution, pivot-language round-trip, keystroke-timing simulation.
22. **Inference-time sampling** — `antislop-sampler`, min_p, top-n-sigma (when the prompt layer isn't enough).
23. **Long few-shot humanization** — prepend 10,000+ tokens of human writing as prior assistant turns.
24. **CI regression tests for slop** — grep/regex post-checks; flag-and-log feedback loops.
25. **Randomized/dynamic system prompts** — rotate mood/goals to avoid static-prompt caricature.

## Controversies & Debates

- **Should LLMs sound human at all?** Willison and HumT/DumT argue no (or *controlled* yes); Every.to, Hassid, and the commercial category assume yes. EU AI Act transparency obligations (Aug 2026) and FTC signals push toward disclosure.
- **Ban-lists vs minimalist directive.** Long enumerated blacklists (OSS skills, Every.to) vs a single "avoid LLM patterns" directive (u/nickakio). Neither side has controlled evidence.
- **Detection bypass vs voice capture.** Two subcultures — "pass Turnitin" (commercial detector-bypass) and "sound like me" (voice) — share techniques but have opposite ethics.
- **Detector reliability.** Vendors claim 98–99% accuracy; independent tests find 62–88%; Stanford found 61% of non-native English is false-flagged. Both sides' quantitative marketing is invalidated.
- **Persona prompting.** Folk wisdom says "you are an expert X" always helps; academic consensus (Zheng et al., Gupta et al., Hu & Collier) says it doesn't help accuracy and can hurt fairness.
- **Prompt vs fine-tune.** Some behaviors (conversational pacing, proactive clarifying questions) reportedly don't survive prompt-only — HF's consultant post argues for SFT. Practitioner community is split.
- **Authenticity of injected quirks.** Is a formulaic "add one personal/quirky line" still humanization, or another fingerprint?
- **Humanizer semantic fidelity.** DAMAGE shows commercial humanizers often damage meaning; the field lacks standard tradeoff measurement.

## Emerging Trends

- **Skills over scripts.** Humanization ships as Claude Code / OpenCode / Cursor skills with `SKILL.md` + vocabulary files, not standalone services.
- **Style guides displacing prompts.** Short in-line prompts referencing long versioned style/anti-pattern documents (Every.to, Hassid, Gwern).
- **Character-scale system prompts at the frontier.** Anthropic's ~30,000-word Claude "constitution" signals humanization is migrating upstream into the base persona.
- **Personality portfolios.** OpenAI's four presets (Professional/Efficient/Fact-Based/Exploratory), Anthropic's named roles — no single "human" setting.
- **Measurement-guided prompt optimization.** HumT/DumT, formulaicness, LLM-as-judge naturalness scoring, Promptomatix; humanization prompts optimized against metrics rather than hand-tuned.
- **Shift from vocabulary to structure.** 2023 advice was word-level; 2025–26 emphasizes burstiness, rhythm, paragraph asymmetry, parentheticals, and pacing.
- **Voice calibration as product category.** Grammarly custom voice, Jasper Brand Voice, `blader/humanizer` v2.4 — "paste your writing, get your voice" commoditizing.
- **Inference-time humanization.** `antislop-sampler`, FTPO fine-tuning, min_p — when prompts aren't enough.
- **LLMOps consolidation.** Humanloop → Anthropic; humanization workflows moving into first-party tooling.
- **Transparency as a wedge.** Rewritely's 33-signal reports, PromptPerfect's explained rewrites — countertrend to black-box rewriting.
- **Regulatory pressure.** EU AI Act (Aug 2026), FTC warnings, academic integrity enforcement shaping vendor language.

## Open Questions / Research Gaps

- **No consensus humanness metric or shared benchmark** spanning detectors, genres, and languages.
- **Implicit everyday-author style is unsolved** — blog/forum voice imitation fails (Wang et al. 2025).
- **Persona-induced bias is unmitigated** — de-biasing prompts have minimal effect (Gupta et al.).
- **Anti-GPTism bans lack rigorous causal study** — which bans actually move the needle is unpublished.
- **Multi-attribute control degrades fluency** — no clean trade-off resolution.
- **Semantic fidelity under humanization is uncharted** — how much meaning survives 3-pass rewrites?
- **Cross-model generalization of humanization prompts is untested** at scale.
- **Long-context style drift** — how many turns before a voice prompt decays?
- **Non-English coverage is thin** — anti-slop lexicons, humanizer products, and benchmarks are English-centric.
- **RLHF × humanization interaction** — how does alignment shaping constrain or distort humanization prompts?
- **Prompt-only vs sampler-level vs fine-tune trade-offs** — no head-to-head studies.
- **Provenance-preserving humanization** — can we humanize while preserving verifiable authorship signal?
- **Humanization × sycophancy-breaking** — the two axes are rarely combined coherently.
- **Ethics of ghostwriting someone's "I"** — unresolved across angles.

## How This Category Fits in the Bigger Picture

Prompt engineering for humanization is the **closest-to-the-user, lowest-capital-cost lever** in the broader humanization stack, and it forms the interface layer that most other categories build on or around:

- **Style transfer & paraphrasing** (a sibling category) supplies the core model techniques (DIPPER, TinyStyler, authorship embeddings) that prompts orchestrate.
- **AI detectors & detector-evasion** is the adversarial counterpart — many prompts here are optimized against it.
- **Fine-tuning / RLHF / DPO for voice** is the deeper stack; prompt engineering is what teams reach for when fine-tuning is too expensive or the base model is closed.
- **Persona design & character AI** intersects heavily — many humanization prompts are persona prompts, and persona research (SPP, Bias Runs Deep) is foundational here.
- **Empathy & emotional modeling** (ECN, Schmidmaier et al.) is a specialized sub-branch of staged humanization prompting.
- **Stylometric / naturalness evaluation** provides the metrics (HumT, formulaicness, burstiness) humanization prompts are optimized against.
- **System prompts & constitutions at frontier labs** define the *floor* that user-side humanization prompts build on top of.
- **Human-AI interaction & trust** (HumT/DumT, LLM Whisperer) questions whether humanization is desirable, informing product design.
- **Agent frameworks** (DSPy, Guidance, LMQL, LangChain) provide the scaffolding that turns a humanization prompt into an evaluated, versioned pipeline.
- **Dataset/annotation quality, watermarking, provenance** are downstream of the humanization–detection arms race.

Treat this category as the **"control surface"**: what you type, bind, or version. Everything deeper (training, sampling, architecture) shows up here as a constraint or escape hatch.

## Recommended Reading Order

For a newcomer, read in this order to move from mental model → concrete practice → research depth → critique:

1. **Every.to, *AI Style Guides*** (Parrott, 2025) — establishes the mental model: style guide, not prompt.
2. **Alan West, *How to Fix That Robotic AI Tone*** (dev.to, 2025) — concrete ship-it walkthrough.
3. **OpenAI Cookbook, *Prompt Personalities*** (Singh & Lau, 2026) — personality as operational lever.
4. **Wikipedia, *Signs of AI Writing*** + **`blader/humanizer` README** — the canonical anti-slop reference and its OSS operationalization.
5. **Gwern, *Some 2025 LLM System Prompts*** (2025) — a worked voice-carrying system prompt with calibrated uncertainty.
6. **Schulhoff et al., *The Prompt Report*** (arXiv 2406.06608, 2024/2025) — the academic taxonomy to anchor vocabulary.
7. **Gupta et al., *Bias Runs Deep*** (ICLR 2024) + **Hu & Collier, *Quantifying the Persona Effect*** (ACL 2024) — the cautionary academic layer.
8. **Krishna et al., *DIPPER*** (NeurIPS 2023) + **Chakraborty et al., *Adversarial Paraphrasing*** (2025) — the humanizer-as-paraphrase-chain line.
9. **Cheng, Yu & Jurafsky, *HumT DumT*** (2025) + **Willison, *My current policy on AI writing*** (2026) — the measurement and ethics critique.
10. **Evan Armstrong, *Mitigating GPT-isms*** (Prompting Weekly, 2024) — practical escape hatch when prompting alone is not enough.

## File Index

- [`A-academic.md`](./A-academic.md) — Peer-reviewed and pre-print literature on prompt-based style transfer, persona/role prompting, humanizer/paraphrase attacks, stylometric fingerprints, and naturalness measurement.
- [`B-industry.md`](./B-industry.md) — Engineering blogs, lab cookbooks, and individual essayists (Willison, Yan, Gwern, Every.to, OpenAI, Anthropic, Huyen) on voice, style guides, and anti-slop system prompts.
- [`C-opensource.md`](./C-opensource.md) — GitHub humanizer skills, detector-evasion tooling, persona libraries, prompt frameworks (DSPy/guidance/LMQL/promptfoo), and system-prompt leak archives.
- [`D-commercial.md`](./D-commercial.md) — Paid humanizer SaaS (Undetectable.ai, StealthGPT, etc.), mainstream writing-suite humanizer features (Grammarly, Jasper, QuillBot), prompt marketplaces, and LLMOps platforms.
- [`E-practical.md`](./E-practical.md) — Reddit, Hacker News, dev.to, LocalLLaMA, and practitioner GitHub corpora on anti-slop ban-lists, minimalist directives, voice-sample ingestion, burstiness engineering, and sycophancy breakers.
