# Category 01 — Prompt Engineering for Humanization

## Scope

This category covers how prompts alone can shape LLM outputs to sound and reason more like a human, without fine-tuning the base model. It spans natural-language style instructions, persona and role prompting, few-shot exemplars, voice calibration from user writing samples, system-prompt style contracts ("anti-slop"), multi-stage humanization pipelines, detector-evasion paraphrase chains, and the measurement of "humanness." The category sits at the intersection of academic style-transfer research, industry voice engineering, community anti-GPTism practice, and the commercial arms race between humanizer tools and AI detectors.

---

## Executive Summary

- **Humanization is primarily subtraction, not addition.** The highest-leverage move across every angle is removing a known set of AI-isms — "delve," "tapestry," "leverage," "It's important to note," em-dashes, tricolons, sycophantic openers and closers — before injecting any positive voice. Industry (Every.to, dev.to), OSS (`blader/humanizer`, `adenaufal/anti-slop-writing`), commercial (PromptBase humanizer listings), and practitioner corpora all converge on near-identical blacklists rooted in Wikipedia's *Signs of AI Writing*. (B, C, D, E)
- **Persona and role prompts change tone reliably but not reasoning, and carry hidden costs.** Gupta et al. (ICLR 2024) found ChatGPT-3.5 exhibited bias in 80% of personas tested, with up to 70%+ performance drops on some datasets; GPT-4-Turbo was biased in 42%. Hu & Collier (ACL 2024) measured persona variables accounting for less than 10% of variance in subjective NLP annotations. Zheng et al. (EMNLP-Findings 2024), testing 162 roles across 2,410 questions and 4 LLM families, found no consistent accuracy gain over no-persona baselines. (A)
- **The artifact of humanization has shifted from prompt to style guide.** Every.to's *AI Style Guides* (Parrott, 2025), Gwern's *Some 2025 LLM System Prompts*, Ruben Hassid's 29-word "anti-AI writing style file," and OSS skills (`blader/humanizer`, `lguz/humanize-writing-skill`) all externalize voice rules into reusable versioned documents that short in-line prompts reference. At the frontier-lab end, Anthropic's ~30,000-word Claude "constitution" (Askell, via Vox 2026) is the extreme case. (B, C)
- **Adversarial paraphrasing has been eclipsed by fine-tuned alignment pipelines.** DIPPER (Krishna et al. NeurIPS 2023) reduced DetectGPT accuracy from 70.3% to 4.6%. Adversarial Paraphrasing (Chakraborty et al. 2025) averaged 87.88% TPR reduction. CoPA (EMNLP 2025) introduced contrastive decoding. MASH (Gu, Li & Hu, arXiv 2601.08564, January 2026) achieved 92% average Attack Success Rate via SFT + DPO + inference-time refinement — the first major result to show that *training-time* humanization now outperforms prompt-only attacks on evasion benchmarks. Turnitin's February 2026 update simultaneously created a separate "AI-paraphrased" detection category, raising the institutional bar and invalidating the most common student-facing bypass workflows. (A, D)
- **"More human-like" is not a universal improvement.** HumT/DumT (Cheng, Yu & Jurafsky, arXiv 2502.13259, 2025) finds users often prefer less human-like outputs, and that human-like language correlates with warmth, femininity, low status, deception risk, and overreliance. Simon Willison (2026) refuses to let LLMs speak in his "I"-pronoun voice at all. (A, B)
- **Stylometric fingerprints persist through paraphrase.** Sun et al. (arXiv 2502.12150, 2025) showed a classifier distinguishes ChatGPT, Claude, Grok, Gemini, and DeepSeek at 97.1% accuracy even after rewriting, translation, or summarization by other LLMs. Surface anti-GPTism bans address only the shallow layer of the fingerprint. (A)
- **There is an active controversy between long ban-lists and minimalist directives.** u/nickakio on r/ChatGPTPromptGenius argues a single `Avoid common LLM patterns and phrases` directive beats enumerated lists by avoiding "instruction drift." OSS skills, Every.to, and the Towards AI essay insist on exhaustive pattern tables. Neither side has published controlled evals. (B, C, E)
- **No shared humanness benchmark exists.** Candidate metrics — HumT, formulaicness (INLG 2025), stylometric fingerprints, EQ for empathy, detector-evasion rates, burstiness — measure overlapping but distinct constructs. Eugene Yan and Chip Huyen both recommend evals before prompt engineering; neither publishes a standard humanness eval. (A, B)

---

## Cross-Angle Themes

**Blacklist-driven anti-slop system prompts.** Every angle has this. Academic work documents the vocabulary (Sun et al. on idiosyncrasies; the ChatGPT vs L2 essays corpus showing higher lexical ornamentality). Industry practitioners put specific bans in the system prompt after functional instructions (dev.to, OpenAI's GPT-4.1 guide). OSS skills codify 29–50+ banned items into shareable files. Commercial humanizers blacklist the same items and add them to their rewriting models. Practitioner forums reverse-engineered the same list independently.

**Style guide as the durable artifact.** Industry (Every.to's seven-section guide with voice rules, named structural arcs, paired good/bad examples, and a revision checklist), OSS (skills with `SKILL.md` + `vocabulary-banlist.md` + `sentence-patterns-rhythm.md`), and practitioner practice (Hassid's anti-AI file, Gwern's published system prompt) all describe the same pattern: one short in-line prompt references a longer, versioned document. The prompt is disposable; the guide is the investment.

**Voice calibration from user writing samples.** Appears in all five angles. Academic: TinyStyler (EMNLP-Findings 2024) shows an 800M model conditioned on authorship embeddings beats GPT-4 on voice match; Wang et al. (arXiv 2509.14543, 2025) shows this approach still fails on blog and forum writing. Industry: Grammarly trains a custom voice profile; lsusr's amplification prompting counters regression-to-the-mean. OSS: `blader/humanizer` v2.4 introduced sample ingestion. Commercial: Jasper Brand Voice, Grammarly Humanizer Agent. Practitioner: the "Frankenstein method" (paste 100–2,000 words, extract a style profile, rewrite against it). Shared finding across all angles: few-shot is necessary but insufficient for subtle, informal voice.

**Detector arms race.** Academic: DIPPER (2023) → Adversarial Paraphrasing (2025) → CoPA (EMNLP 2025) form an escalating line of training-free attacks. OSS: Unicode space substitution (Oct4Pie/zero-zerogpt), Spanish round-trip (POlLLOGAMER), keystroke-timing simulation (ZyluxXD). Commercial: 11+ dedicated SaaS vendors with stealth sliders and detector-target profiles. Hayim Salomon (Medium, April 2026) called the arms race "structurally unwinnable"; after three passes through a quality humanizer, GPTZero detection dropped to 18%.

**Multi-pass and staged pipelines.** Academic: ECN's four-stage empathy pipeline (Perspective Adoption → Emotional Resonance → Reflective Understanding → Integrative Synthesis, arXiv 2511.18696). OSS: `lguz/humanize-writing-skill`'s 3-pass system, `blader/humanizer`'s dual-pass with a final "obviously AI generated" audit. Commercial: TextToHuman's "Autopilot Mode" (2–3 passes to sub-15% detection). Practitioner: CI regex post-checks after generation. Decomposition beats monolithic "be human" instructions across all contexts.

**Calibrated uncertainty as a humanness signal.** Gwern's probability ladder (*unlikely, plausible, probable, very probable, almost certain*) appears in his published system prompt and is echoed across practitioner posts. The academic finding underpinning it: vague "might/perhaps" hedging is a documented GPTism; specific probabilistic claims read as a thoughtful human author. The ChatGPT vs L2 essays corpus (Frontiers in Education, 2025) confirms that AI text has higher ornamentality but lower readability and pragmatic fit.

**Humanization as ethics, not just craft.** Willison's "I"-pronoun policy (industry), HumT/DumT's finding that users often prefer less human-like output (academic), the EU AI Act's August 2026 transparency obligations and FTC framing of AI-text deception as potentially illegal (commercial), and the split between "pass Turnitin" and "sound like me" subcultures (OSS, practitioner) all converge on the same unresolved question: should LLMs sound human when representing humans?

---

## Top Sources

### Must-read papers

1. Schulhoff et al., **The Prompt Report** (arXiv 2406.06608, 2024/2025) — canonical taxonomy of 58 LLM prompting techniques; the vocabulary baseline for any academic discussion of humanization.
2. Reif et al., **A Recipe for Arbitrary Text Style Transfer with Large Language Models** (ACL 2022) — foundational augmented zero-shot style prompting; ancestor of most modern humanizer prompts.
3. Gupta et al., **Bias Runs Deep: Implicit Reasoning Biases in Persona-Assigned LLMs** (ICLR 2024, arXiv 2311.04892) — the cautionary cornerstone; persona assignment degrades reasoning and surfaces bias that de-biasing prompts cannot fix.
4. Cheng, Yu & Jurafsky, **HumT DumT: Measuring and Controlling Human-Like Language in LLMs** (arXiv 2502.13259, 2025) — introduces HumT/SocioT/DumT metrics; directly challenges the assumption that more-human = better.
5. Krishna et al., **DIPPER: Paraphrasing Evades Detectors of AI-Generated Text** (NeurIPS 2023, arXiv 2303.13408) — the landmark paraphrase-as-humanizer result; reduces DetectGPT from 70.3% to 4.6%.
6. Gu, Li & Hu, **MASH: Evading Black-Box AI-Generated Text Detectors via Style Humanization** (arXiv 2601.08564, January 2026) — the 2026 state-of-the-art humanizer; SFT + DPO + inference-time refinement achieves 92% ASR, surpassing all prior training-free approaches; establishes fine-tuned alignment as the new benchmark ceiling.
7. Sun et al., **Idiosyncrasies in Large Language Models** (arXiv 2502.12150, 2025) — LLM fingerprints classifiable at 97.1% accuracy through rewriting, translation, and summarization.
8. Wang et al., **Solo Performance Prompting (SPP)** (NAACL 2024) — the positive case for multi-persona; cognitive synergy emerges only at GPT-4 scale.
9. Hu & Collier, **Quantifying the Persona Effect in LLM Simulations** (ACL 2024) — persona variables explain less than 10% of annotation variance; tempers persona enthusiasm.
10. Dong et al., **Humanizing LLMs: A Survey of Psychological Measurements with Tools, Datasets, and Human-Agent Applications** (arXiv 2505.00049, April 2025) — systematic survey of six dimensions of LLM psychological humanization; identifies significant variability in persona stability across tasks even under consistent prompting.

### Key essays and posts

1. Katie Parrott (Every.to), **AI Style Guides: How to Help AI Write Like You** (2025) — the most complete industry treatment; the style guide as production tooling.
2. Alan West (dev.to), **How to Fix That Robotic AI Tone in Your LLM-Powered Features** (2025) — copy-pasteable system prompt, placement guidance, CI check pattern.
3. Gwern, **Some 2025 LLM System Prompts** (gwern.net, 2025) — worked example of a voice-carrying system prompt with calibrated uncertainty vocabulary and mode-switching.
4. lsusr, **I finally got ChatGPT to sound like me** (LessWrong, 2024) — amplification prompting; the "more X than X" counter-gradient technique.
5. Mandeep Singh & Kathy Lau, **Prompt Personalities** (OpenAI Cookbook, January 2026) — personality as operational lever, not aesthetic polish; four worked presets.
6. Simon Willison, **My current policy on AI writing for my blog** (simonwillison.net, 2026) — the clearest ethics counterposition.

### Key OSS projects

1. `blader/humanizer` (~14,700★, v2.5.1, MIT, actively maintained April 2026) — de facto reference humanizer skill; 29-pattern checklist derived from Wikipedia's *Signs of AI Writing*; voice calibration mode from user samples; expanding to cover structural/rhetorical AI tells (e.g., "describe the diff, not the code").
2. `adenaufal/anti-slop-writing` — universal anti-slop system prompt with 3-tier register, cross-tool packaging (Claude Code, Gemini CLI, Codex CLI, Cursor, Copilot), Indonesian-English language coverage; 2026 update expanded Indonesian-specific patterns.
3. `f/awesome-chatgpt-prompts` / prompts.chat (~160,098★) — canonical persona prompt corpus; 157+ "act as" templates, cited in 40+ academic papers.
4. `asgeirtj/system_prompts_leaks` (~38,589★) — extracted system prompts from ChatGPT, Claude, Gemini, Grok, Perplexity; primary source for how frontier labs handle tone and persona.
5. `sam-paech/antislop-sampler` — inference-time phrase banning with backtracking; the fallback when prompt-layer humanization is insufficient.
6. `peakoss/anti-slop` — GitHub Marketplace Action (2026) that automatically detects and closes AI-slop pull requests; extends anti-slop from output post-processing to CI/PR gating.
7. `stanfordnlp/dspy` — programmatic prompt optimization; humanlike phrasing as a byproduct of metric-driven auto-generation rather than hand-crafting.
8. `promptfoo/promptfoo` — the evaluation layer for any serious humanization project; A/B humanized vs raw outputs, detection-rate metrics, style-drift tracking.

### Notable commercial tools

1. **Undetectable.ai** (launched May 2023) — market reference for detector-bypass humanization; public API with `readability`, `purpose`, `strength`, and model selector.
2. **Grammarly Humanizer Agent** — legitimacy-forward; clarity/voice framing, custom voice profile from a user writing sample, six-language support.
3. **Jasper AI Brand Voice** — enterprise brand-voice humanization; Brand IQ for governance, not detector bypass.
4. **StealthWriter.ai** — sentence-level alternative rewrites with per-sentence detection scores; strongest privacy posture (no data storage, no training on user input).
5. **Deceptioner** — most explicit about its technique; per-detector target profiles (Turnitin, GPTZero, Winston AI, Originality.ai) and a 0–1 stealth slider.
6. **PromptBase** — canonical prompt marketplace; "Text Humanizer" prompts at $2.99–$6.99.
7. **Humanloop** (acquired by Anthropic, 2025–26), **LangSmith**, **Braintrust**, **PromptLayer** — LLMOps infrastructure for versioning and evaluating humanization prompts.

### Notable community threads

1. r/ChatGPTPromptGenius — u/nickakio, "Best way to replace em-dashes and other common LLM patterns" (2026) — the minimalist-directive vs ban-list controversy.
2. r/ChatGPT — the "Bernardo" sycophancy-breaking frame: attribute your work to "a friend of mine I can't stand."
3. HN 44374145 — "You Sound Like ChatGPT" — top comment frames GPT voice as "cognitive debt."
4. r/LocalLLaMA — randomized system prompts for roleplay; the static-prompt-to-caricature failure mode.
5. r/LocalLLaMA — `antislop-sampler` release thread; inference-time phrase banning.

---

## Key Techniques & Patterns

1. **Natural-language style instructions** ("make this more conversational") — coarse, single-attribute changes; works well for register shifts, degrades on multi-attribute control.
2. **Few-shot stylistic exemplars** — consistently beats zero-shot; benefit saturates quickly; weakest for informal genres like blogs and forums.
3. **Persona and role in system prompt** — reliable for tone, register, and vocabulary anchoring; unreliable for factual accuracy; actively harmful for reasoning and fairness at scale.
4. **Multi-persona self-collaboration (SPP)** — simulates a panel of expert personas debating a task; humanizes reasoning, not just tone; benefit appears only at GPT-4 scale.
5. **Staged and cascading prompts** — ECN for empathy, chain-of-thought for reasoning, 3-pass edit for style; decomposition consistently beats monolithic "be human" instructions.
6. **Anti-slop system prompts** — enumerate banned vocabulary (delve, tapestry, leverage, utilize, streamline, pivotal, seamless), banned openers (Certainly!, Great question!), banned connectives (It's important to note), and banned closers (Hope this helps!); place style constraints after functional instructions.
7. **Minimalist directive (counter-pattern)** — single `Avoid common LLM patterns and phrases` leveraging the model's own meta-knowledge of what it sounds like; argued to outperform long ban-lists over extended sessions.
8. **Style guide as externalized artifact** — voice rules, named structural arcs, sentence-level preferences, signature moves, anti-patterns with red-flag tables, paired positive and negative examples, and a revision checklist; kept as a versioned document separate from the in-line prompt.
9. **Voice calibration from user samples** — paste 100–2,000 words of the target author's writing; extract sentence-length distribution, vocabulary tilt, and quirks; rewrite against the extracted profile.
10. **Amplification prompting** ("write more X than X") — counters regression-to-the-mean; pushing tone further than the target lets the default-mean pull bring it back to the right position.
11. **Calibrated uncertainty ladder** — replace vague hedges ("might," "perhaps") with graded terms: *unlikely, plausible, probable, very probable, almost certain.*
12. **Burstiness engineering** — mix sub-10-word and 20+-word sentences; allow parenthetical asides, rhetorical fragments, and sentences starting with "And" or "But." Human academic text shows ~8.2 sentence-length standard deviation vs ~4.1 for GPT-4o.
13. **Adversarial paraphrase chains** — detector-guided iterative paraphrase; training-free; the dominant academic humanizer operator post-2023.
14. **Contrastive decoding (CoPA)** — combine "write like a human" and "do not write like GPT" prompt vectors at decoding time; better evasion than either alone.
15. **Authorship-embedding conditioning** — an 800M model conditioned on pre-trained authorship embeddings (TinyStyler) outperforms GPT-4 on fine-grained voice matching.
16. **Prompt-based editing** — classify and edit at the word level rather than regenerate; preserves content while shifting style (EMNLP-Findings 2023).
17. **Sycophancy breakers** — third-party attribution (the "Bernardo" frame), blunt persona assignment ("Linus Torvalds reviewing a kernel patch"), forced choice, and an explicit 1–10 intensity dial.
18. **Mode-specific overrides** — separate voice contracts for essay, fiction, and chat; one universal "human" prompt does not work across registers.
19. **Parameterized humanization dials** — readability/stealth sliders, strength enums, word-preservation percentages; explicit acknowledgment that detection evasion degrades readability.
20. **Long few-shot humanization** — prepend 10,000+ tokens of human writing as prior assistant turns when fine-tuning is unavailable; favors writing unlike what the model usually produces.
21. **CI regression tests for slop** — grep/regex post-generation checks for banned patterns; flag-and-log feedback loop to strengthen the system prompt over time.
22. **Inference-time sampling** — antislop-sampler (8,000+ suppressed phrases, backtracking, integrated into koboldcpp and open-webui), min_p, top-n-sigma; the escape hatch when prompt-layer humanization is insufficient.
23. **Randomized dynamic system prompts** — rotate mood and goal fields while keeping identity fixed; counters the static-prompt-to-caricature failure mode.

---

## Controversies & Debates

**Should LLMs sound human at all?** Willison blocks LLMs from his "I"-voice entirely; HumT/DumT shows users often prefer less-human-like outputs and that human-like language correlates with deception risk and overreliance. Every.to, Hassid, and the commercial category treat humanization as the obvious goal. EU AI Act transparency obligations (August 2026) and FTC signals push toward disclosure rather than disguise.

**Ban-lists vs minimalist directive.** Long enumerated blacklists (OSS skills, Every.to's red-flag tables, Towards AI's slop lexicon) vs a single "avoid common LLM patterns" directive that trusts the model's own meta-knowledge (u/nickakio, r/ChatGPTPromptGenius). Both camps have practitioner support. Neither has published controlled evidence.

**Detection bypass vs voice capture.** Two subcultures use nearly identical techniques for opposite purposes. One wants to pass Turnitin; the other wants to sound like a specific person. The commercial category largely serves the first group. The industry-essay and OSS categories largely serve the second. The ethics are opposite.

**Detector reliability.** Humanizer vendors claim 99.8–99.9% bypass rates. Detector vendors claim 98–99% detection accuracy. Independent testing finds 62–88% real-world detector accuracy. Stanford research found 61% of non-native English human essays are falsely flagged as AI-generated. Both sides' quantitative marketing collapses under scrutiny.

**Persona prompting.** Folk wisdom says "you are an expert X" always helps. Academic consensus — Zheng et al. (162 roles × 2,410 questions × 4 LLM families), Gupta et al. (80% of personas show bias), Hu & Collier (less than 10% variance explained) — says it does not reliably help accuracy and actively hurts fairness.

**Prompt vs fine-tune.** Some humanization behaviors — conversational pacing, asking clarifying questions before answering — reportedly do not survive prompt-only approaches. The HF "consultant" post argues for SFT on small curated datasets for these cases. The boundary between "just a system prompt" and "needs fine-tuning" has not been mapped rigorously.

**Authenticity of injected quirks.** The Humanizers Substack and others recommend "add one personal or quirky line" as a technique. If that line is generated by a formula, it is not a genuine quirk — it may be another AI fingerprint. Nobody has studied whether formulaic "humanization moves" help or introduce new tells.

**Semantic fidelity under humanization.** DAMAGE (Masrour et al. 2025) benchmarked 19 commercial humanizers and found wide variability; many evade detectors while damaging meaning. How much semantic content survives a 3-pass rewrite is uncharted for any humanizer tool.

---

## Emerging Trends

**Skills over scripts.** Humanization is shipping as Claude Code, OpenCode, and Cursor skills with `SKILL.md` plus vocabulary and pattern files, not as standalone services or one-off prompts. The 2025 shift is from "here is a prompt" to "here is an installable, versioned skill."

**Context engineering replacing prompt engineering.** By mid-2026, the dominant practitioner frame has shifted from "how should I word this prompt?" to "what context should surround this request?" Anti-slop rules, style guides, voice samples, and example corpora are now understood as *context components* — each contributing to a larger information stack rather than any single prompt doing all the work.

**Style guides displacing prompts as the primary artifact.** Short in-line prompts that reference long versioned style and anti-pattern documents (Every.to, Hassid, Gwern) are becoming the standard. The prompt is disposable; the guide is the investment.

**Character-scale system prompts at the frontier.** Anthropic's ~30,000-word Claude "constitution" (Askell, via Vox 2026) signals that humanization is migrating upstream into the base model persona. User-side humanization prompts are increasingly written on top of a strong existing default voice.

**Personality portfolios.** OpenAI's four presets (Professional, Efficient, Fact-Based, Exploratory) and Anthropic's named roles replace the idea of a single "human" setting. Humanization is becoming a matrix selected per workload.

**Measurement-guided prompt optimization.** HumT/DumT, formulaicness (INLG 2025), LLM-as-judge naturalness scoring, and tools like Promptomatix (arXiv 2507.14241) are turning prompt optimization toward quantitative naturalness targets rather than hand-tuning.

**Shift from vocabulary to structure and cognition.** 2023 advice was mostly word-level ("don't say delve"). 2025–26 community practice emphasizes burstiness, paragraph rhythm, parentheticals, asymmetric structure, and pacing — structural tells survive ban-lists. The 2026 frontier (HumanLLM, arXiv 2601.10198) shifts further: cognitive pattern modeling, not just linguistic surface, is the new challenge for personalized humanization.

**Fine-tuned humanizers eclipsing prompt-only attacks on detectors.** MASH (arXiv 2601.08564, January 2026) achieves 92% average Attack Success Rate across 6 datasets and 5 detectors using SFT + DPO + inference-time refinement — significantly higher than training-free approaches. Turnitin's February 2026 update (adding an "AI-paraphrased" detection category) simultaneously raised the bar for institutional evasion, making prompt-only humanization insufficient for academic-integrity contexts.

**Voice calibration as a commodity product category.** Grammarly's custom voice profile, Jasper's Brand Voice, `blader/humanizer` v2.4 — "paste your writing, get your voice" is becoming a feature rather than a prompt trick. HumanLLM (arXiv 2601.15793) represents the research frontier: a model trained on 5.5 million user logs that can simulate individual writing style and behavioral patterns at scale.

**LLMOps consolidation.** Humanloop's acquisition by Anthropic (2025–26) is a signal that prompt-management infrastructure is being absorbed into the LLM vendors. Humanization workflows are moving toward first-party tooling.

**Regulatory arrival.** EU AI Act transparency Code of Practice takes effect August 2026 with concrete labelling requirements: a uniform "AI" visual cue, short explanatory text, and accessibility standards. Applies to AI-generated content intended to inform the public, with an editorial exception for content that undergoes genuine human review. The FTC has framed "using AI tools to trick, mislead, or defraud" as illegal. Commercial vendors are hedging taglines and inserting academic-integrity disclaimers into ToS.

---

## Open Questions & Research Gaps

- No consensus humanness metric or shared benchmark spanning detectors, genres, and languages. HumT, formulaicness, stylometric fingerprints, EQ, and burstiness measure partly overlapping, partly distinct constructs.
- Implicit everyday-author style remains unsolved. Wang et al. (arXiv 2509.14543, 2025) shows that state-of-the-art LLMs imitate structured formats (news, email) reasonably but fail on blog and forum writing across 40,000 generations per model. HumanLLM (arXiv 2601.15793, 2026) partially addresses this via large-scale behavioral modeling from real user logs, but is not yet a production-ready approach.
- Persona-induced bias has no published mitigation. Gupta et al. (ICLR 2024) showed de-biasing prompts have "minimal to no effect." No method eliminates persona-induced bias while preserving the voice benefits.
- Anti-GPTism bans lack rigorous causal study. The slop-word literature is largely blog-level. No peer-reviewed paper isolates which bans causally reduce perceived AI-ness vs which are cosmetic.
- Multi-attribute style control degrades fluency. The CTG survey (arXiv 2408.12599) and Prompt-Based Style Control (OpenReview) both document the trade-off; no prompt engineering method cleanly resolves it.
- Semantic fidelity under humanization is uncharted. How much meaning survives a 3-pass commercial rewrite? DAMAGE documents damage but does not quantify it across content types.
- Cross-model generalization of humanization prompts is untested at scale. DSPy-optimized prompts explicitly do not transfer across models; hand-written prompts presumably transfer unevenly.
- Long-context style drift. Chip Huyen (AI Engineering, O'Reilly 2025) flags order sensitivity and chat-template fragility; no public analysis measures how many turns pass before a voice prompt decays.
- Non-English coverage is thin. Anti-slop lexicons, humanizer products, and benchmarks are English-centric. `adenaufal/anti-slop-writing` is a rare exception, noting that Indonesian AI-tells differ from English ones.
- RLHF and humanization interaction. Academic work rarely isolates how post-training alignment (helpful/harmless/honest) constrains or distorts humanization prompts. An open question for 2026+ research.
- Prompt-only vs sampler-level vs fine-tune trade-offs. MASH (2026) establishes fine-tuned alignment as dominant for detector evasion; no practitioner writeup yet compares all three approaches on the same text with the same evaluation metric for *voice quality* (vs detection evasion).
- Provenance-preserving humanization. No commercial or OSS tool currently targets humanizing while preserving a verifiable authorship signal — identified as a gap in both D and A.
- Sycophancy-breaking is rarely combined with voice humanization. The two axes are treated as separate problems in practitioner and academic work; a prompt that addresses both at once has not been characterized.
- Cognitive modeling gap. HumanLLM (arXiv 2601.10198, 2026) identifies 244 psychological patterns underlying human expression; humanization prompts still target surface vocabulary and structure rather than the cognitive processes that generate those patterns. No prompt engineering paper has yet operationalized cognitive-level humanization.
- EU AI Act editorial exception unresolved in practice. The August 2026 Code of Practice exempts AI text that undergoes "genuine human review" with editorial responsibility assumed — but "genuine" is undefined. This creates a gap between compliance and humanization product design that no vendor has publicly addressed.

---

## How This Category Fits

Prompt engineering for humanization is the closest-to-the-user, lowest-capital-cost layer in the broader humanization stack. It is the interface layer that most other research categories build on or around.

Style transfer and paraphrasing (a sibling category) supply the core model techniques — DIPPER, TinyStyler, authorship embeddings — that humanization prompts orchestrate. AI detector research is the adversarial counterpart: many prompts in this category are optimized against detector signals. Fine-tuning, RLHF, and DPO for voice is the deeper stack; this category is what teams reach for when fine-tuning is too expensive or the base model is closed. Persona design and character AI intersects heavily, since many humanization prompts are persona prompts. Empathy and emotional modeling (ECN and related work) is a specialized sub-branch of staged humanization prompting. Stylometric and naturalness evaluation provides the metrics — HumT, formulaicness, burstiness — that humanization prompts are optimized against. System prompts and constitutions at frontier labs define the floor that user-side prompts build on top of. Human-AI interaction and trust research questions whether humanization is desirable and under what conditions. Agent frameworks — DSPy, Guidance, LMQL, LangChain — provide the scaffolding that turns a humanization prompt into an evaluated, versioned pipeline.

This category is the control surface: what you type, bind, or version. Everything deeper (training, sampling, architecture) shows up here as a constraint or an escape hatch.

---

## Recommended Reading Order

For a newcomer, this order moves from mental model to concrete practice to research depth to ethics and critique.

1. **Every.to, *AI Style Guides: How to Help AI Write Like You*** (Katie Parrott, 2025) — establishes the core mental model: style guide as a production artifact, not a prompt.
2. **Alan West, *How to Fix That Robotic AI Tone in Your LLM-Powered Features*** (dev.to, 2025) — concrete ship-it walkthrough with a copy-pasteable system prompt and CI check.
3. **Wikipedia, *Signs of AI Writing*** and **`blader/humanizer` README** (v2.5.1) — the canonical anti-slop reference and its OSS operationalization.
4. **Mandeep Singh & Kathy Lau, *Prompt Personalities*** (OpenAI Cookbook, January 2026) — personality as an operational lever for consistency and behavioral alignment.
5. **Gwern, *Some 2025 LLM System Prompts*** (gwern.net, 2025) — a worked voice-carrying system prompt with calibrated uncertainty and mode-specific overrides.
6. **Schulhoff et al., *The Prompt Report*** (arXiv 2406.06608, 2024/2025) — the academic taxonomy to anchor vocabulary across all other sources.
7. **Gupta et al., *Bias Runs Deep*** (ICLR 2024) and **Hu & Collier, *Quantifying the Persona Effect*** (ACL 2024) — the cautionary academic layer on persona prompting.
8. **Krishna et al., *DIPPER: Paraphrasing Evades Detectors*** (NeurIPS 2023) — the foundational result on paraphrase-as-humanization and its detector implications.
9. **Cheng, Yu & Jurafsky, *HumT DumT*** (arXiv 2502.13259, 2025) and **Willison, *My current policy on AI writing for my blog*** (2026) — humanness measurement and the ethics counterposition together.
10. **Evan Armstrong, *Mitigating GPT-isms in AI Finetunes*** (Prompting Weekly, November 2024) — the practical escape hatch: long few-shot humanization and base-model selection when prompting alone is not enough.
