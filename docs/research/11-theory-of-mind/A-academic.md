# Theory of Mind in LLMs — Angle A (Academic)

**Category:** 11 — Theory of Mind in AI
**Angle:** A — Academic & scholarly (arXiv, ACL/EMNLP/NAACL/EACL, NeurIPS, ICML, Nature journals)
**Project:** Humanizing AI output and thinking
**Research value:** **high** — A large, rapidly maturing academic literature with clear anchor papers, named benchmarks, active controversies, and well-documented failure modes directly relevant to humanizing AI behavior.

---

## 1. Scope & Framing

Theory of Mind (ToM) — the capacity to attribute beliefs, desires, intentions, knowledge, and emotions to self and others and use those attributions to predict behavior — is a central construct in developmental and cognitive psychology (Premack & Woodruff 1978; Wimmer & Perner 1983 Sally–Anne test). Since late 2022, it has become a flashpoint in LLM evaluation: do frontier models actually model other minds, or do they pattern-match on psychological test surface structure?

For a humanization project, ToM matters because most behaviors that feel "human" in dialogue (tact, inference about what the user already knows, avoiding over-explaining, irony, indirect requests, faux pas avoidance, persona consistency with beliefs about the interlocutor) are downstream of some form of mental-state tracking — however implemented.

This digest covers the principal academic claims (2018–2025), the primary benchmarks, the methodological critiques, and the emerging interpretability work.

---

## 2. Annotated Paper List (18 papers)

Fields per entry: **Citation · Venue · Contribution · Method · Key finding · Relevance to humanization**

### Foundational / pre-LLM

1. **Rabinowitz, Perbet, Song, Zhang, Eslami, Botvinick (2018). "Machine Theory of Mind."** ICML 2018. arXiv:1802.07740.
   - Introduces **ToMnet**, a meta-learning neural net that builds models of other agents from behavioral observations and passes a Sally–Anne-style false-belief test.
   - Pre-LLM anchor. Establishes the framing that ToM can be posed as meta-learning over agent behavior — relevant for agent-based humanization (modeling the *user* as an agent).

2. **Le, Boureau, Nickel (2019). "Revisiting the Evaluation of Theory of Mind through Question Answering" (ToMi).** EMNLP 2019.
   - Canonical **ToMi** benchmark: procedurally generated stories with true-belief, first-order false-belief, and second-order false-belief items plus memory/reality controls.
   - Showed prior memory-augmented models were exploiting dataset biases. Still the default unit test used by nearly every 2022–2025 follow-up.

3. **Sap, Rashkin, Chen, Le Bras, Choi (2019). "Social IQa: Commonsense Reasoning about Social Interactions."** EMNLP-IJCNLP 2019.
   - **SocialIQA**: 38K multiple-choice items on motivations, reactions, next actions in social scenarios, with an adversarial answer-collection protocol that mitigates stylistic artifacts.
   - Long-standing reference point for social commonsense; humans ~88%, pre-GPT-4 models ~55–65%. Transfer-learning value for downstream commonsense tasks.

### The 2023 emergence-vs-fragility debate

4. **Kosinski (2023/2024). "Theory of Mind May Have Spontaneously Emerged in Large Language Models" → "Evaluating Large Language Models in Theory of Mind Tasks."** arXiv:2302.02083; PNAS 2024.
   - 40 classic false-belief tasks across GPT-3 through GPT-4. Reports a scaling progression: davinci-001 ≈ 3.5-yr-old (40%) → GPT-3.5 ≈ 7-yr-old (90%) → GPT-4 95%. PNAS 2024 version tightens criteria (all eight variants per task) and reports GPT-4 at ~75%, ≈6-yr-old level.
   - **The claim that ignited the field.** Read the PNAS version, not the working paper — the stricter protocol is more defensible.

5. **Ullman (2023). "Large Language Models Fail on Trivial Alterations to Theory-of-Mind Tasks."** arXiv:2302.08399.
   - Direct adversarial reply to Kosinski. Shows that minor, ToM-preserving perturbations (e.g., transparent containers, perception changes) flip model answers. Argues failure outliers should outweigh aggregate success.
   - Establishes the **"zero hypothesis"**: default to skepticism about intuitive-psychology benchmarks; reporting should emphasize failure-mode robustness.

6. **Sap, LeBras, Fried, Choi (2022). "Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs."** EMNLP 2022. arXiv:2210.13312.
   - Pre-dated Kosinski. Evaluated GPT-3 on SocialIQA (55%) and ToMi (60%), argued limitations come from training data, architecture, and paradigm — not just scale.
   - Important precursor that framed the **scale-is-not-enough** thesis later vindicated by benchmark-specific failures.

7. **Shapira, Levy, Alavi, Zhou, Choi, Goldberg, Sap, Shwartz (2024). "Clever Hans or Neural Theory of Mind? Stress Testing Social Reasoning in Large Language Models."** EACL 2024. arXiv:2305.14763.
   - Stress-tests 6 ToM-related tasks with adversarial perturbations inspired by Ullman. Finds consistent degradation; models rely on **shallow heuristics**.
   - Best single citation for the "LLMs have inconsistent, non-robust ToM" position.

### Second-generation benchmarks (2023–2024)

8. **Gandhi, Fränken, Gerstenberg, Goodman (2023). "Understanding Social Reasoning in Language Models with Language Models" (BigToM).** NeurIPS 2023 Datasets & Benchmarks. arXiv:2306.15448.
   - **BigToM**: 25 controls + 5,000 model-generated items built by populating formal **causal templates** (context, desire, percept, causal event, action). Human raters judged BigToM higher quality than ToMi/SocialIQA, on par with expert-written items.
   - First benchmark designed around a causal-graph theory of ToM rather than narrative templates. GPT-4 near-ceiling on forward belief; smaller models show strong belief-attribution biases.

9. **Kim, Sclar, Zhou, Bras, Liu, Choi, Sap (2023). "FANToM: A Benchmark for Stress-testing Machine Theory of Mind in Interactions."** EMNLP 2023. arXiv:2310.15421.
   - **FANToM**: 10K questions over 256 multi-party conversations with characters entering/leaving — natural information asymmetry. Interlocking question types (belief / answerability / info-accessibility, choice vs list vs free-response).
   - Introduces the concept of **"illusory ToM"**: models look fine on single easy question types, but when scored on *all* interlocking questions for the same scene, performance collapses. This is the best single benchmark for testing ToM *in dialogue* — directly relevant to humanization.

10. **Wu, He, Jia, Mihalcea, Chen, Deng (2023). "Hi-ToM: A Benchmark for Evaluating Higher-Order Theory of Mind Reasoning in Large Language Models."** Findings of EMNLP 2023. arXiv:2310.16755.
    - **Hi-ToM**: 1.2K QA pairs probing orders 1–4 ("A thinks that B thinks that C thinks …"). Monotonic accuracy decay as order increases across all tested LLMs.
    - Strongest evidence that apparent first-order success does not generalize to the recursive belief nesting humans handle routinely.

11. **Xu, Zhao, Zhang, Mihalcea, Wang (2024). "OpenToM: A Comprehensive Benchmark for Evaluating Theory-of-Mind Reasoning Capabilities of Large Language Models."** ACL 2024. arXiv:2402.06044.
    - **OpenToM**: 696 longer narratives (avg 194/491 words) with explicit personality traits, intention-driven actions, and three question families (location, multi-hop, attitude). 16K total questions.
    - Separates **physical-state** mental modeling (where LLMs do relatively well) from **psychological-state** modeling (where they struggle) — a distinction useful for humanization, which mostly needs the latter.

12. **Chen, Wu, He, Liu, Bai, Han, Yang, Xu, Yin, Long, Zhou, Mi, Xu, Yan, Huang (2024). "ToMBench: Benchmarking Theory of Mind in Large Language Models."** ACL 2024. arXiv:2402.15052.
    - **ToMBench**: 2,860 bilingual (EN/ZH) items across **8 classic psychological tasks** (Unexpected Outcome, Scalar Implicature, Persuasion Story, False Belief, Ambiguous Story, Hinting, Strange Stories, Faux-pas) × 6 abilities (Emotion/Desire/Belief/Intention/Knowledge/Action). Multiple-choice with controlled distractors, built from scratch to resist contamination.
    - Even GPT-4 lags humans by >10 pp. Most *systematic* benchmark to date; cite when making the "no LLM has reached human ToM" claim.

13. **Strachan, Albergo, Borghini, Pansardi, Scaliti, Gupta, Saxena, Rufo, Panzeri, Manzi, Graziano, Becchio (2024). "Testing theory of mind in large language models and humans."** *Nature Human Behaviour* 8, May 2024. DOI:10.1038/s41562-024-01882-z.
    - Direct head-to-head: two GPT models and Llama-2 family vs **1,907 humans** across false belief, indirect requests, irony, and faux pas.
    - GPT-4 at or above human level on indirect requests, false beliefs, and misdirection; **struggles on faux pas** — but the authors show this is a conservative-responding artifact, not an inference failure. Llama-2 "wins" faux pas only via an ignorance-attribution bias.
    - The highest-visibility peer-reviewed result; gold standard citation for "*behavior* consistent with mentalistic inference" with careful hedging.

14. **Jin, Kim, Kim, Hwang, Welleck, Bisk, Choi (2024). "MMToM-QA: Multimodal Theory of Mind Question Answering."** ACL 2024 **Outstanding Paper**. arXiv:2401.08743.
    - First **multimodal ToM** benchmark (text + household video). 600 questions (300 belief, 300 goal inference). Introduces **BIP-ALM** (Bayesian Inverse Planning accelerated by LMs) as a neuro-symbolic baseline that outperforms GPT-4 on multimodal items.
    - Supports the recurring finding that **pure LLMs struggle when grounding is required**; a probabilistic planning core + LM helps.

15. **Gu, Sclar, Kim, Choi, Sap, West (2024). "SimpleToM: Exposing the Gap between Explicit ToM Inference and Implicit ToM Application in LLMs."** arXiv:2410.13648 (OpenReview 2025).
    - **SimpleToM**: concise real-world stories (supermarkets, hospitals, offices), each with three layered questions: mental-state inference → behavior prediction → behavior judgment.
    - SOTA models infer mental states reliably but fail at **applying** that inference to predict or judge behavior. GPT-4o action-prediction accuracy 49.5% → 93.5% only with strong scaffolding prompts.
    - Most important result for humanization: *knowing* what a user believes ≠ *acting* differently because of it.

### Mitigations, representations, and mechanism

16. **Sclar, Kumar, West, Suhr, Choi, Tsvetkov (2023). "Minding Language Models' (Lack of) Theory of Mind: A Plug-and-Play Multi-Character Belief Tracker" (SymbolicToM).** ACL 2023 **Outstanding Paper**. arXiv:2306.00924.
    - **SymbolicToM**: decoding-time algorithm that maintains a per-character graphical belief state, higher-order nested. Zero-shot, no fine-tuning.
    - Dramatic ToMi improvements plus strong OOD robustness. Articulates the **symbolic-augmentation thesis**: scale alone will not deliver ToM because the phenomenon is inherently symbolic and implicit.

17. **Zhu, Zhang, Wang (2024). "Language Models Represent Beliefs of Self and Others."** ICML 2024. arXiv:2402.18496.
    - Probes LLM activations and shows belief states of protagonist and oracle are **linearly decodable** from attention-head activations. More heads encode oracle beliefs than protagonist beliefs.
    - Causal intervention: manipulating these directions dramatically changes ToM performance; random directions do nothing. First strong **interpretability-level** evidence that LLMs carry belief-like structure internally.

18. **Li, Chi, Chawla, Griffiths, Hawkins (2023). "Theory of Mind for Multi-Agent Collaboration via Large Language Models."** arXiv:2310.10701 (EMNLP 2023).
    - LLM-based agents in multi-agent cooperative tasks show emergent collaboration and higher-order ToM-like behavior, but systematic failures at long-horizon context and hallucinated task states.
    - Recommends explicit belief-state representations and BDI-style scaffolds. Bridge between ToM evaluation and *applied* agentic systems.

### Meta-critique (2025)

19. **Soubki & Rambow (2025). "Machine Theory of Mind Needs Machine Validation."** Findings of ACL 2025.
    - Meta-analysis of 16 ToM-in-LLM studies. Almost all perform **human validation** (human raters checking items); fewer than half perform **machine validation** (checking for patterns that simple models can exploit). Among studies that *do* run machine validation, **none** find LMs exceeding humans.
    - Best single citation for the structural-skepticism position in 2025.

20. **Nguyen (2025). "A Survey of Theory of Mind in Large Language Models: Evaluations, Representations, and Safety Risks."** arXiv:2502.06470. (See also: Sarıtaş et al., "A Systematic Review on the Evaluation of Large Language Models in Theory of Mind Tasks," arXiv:2502.08796; and ACL 2025 survey "Theory of Mind in Large Language Models: Assessment and Enhancement," 2025.acl-long.1522.)
    - Three independent 2025 surveys converge on: (a) GPT-4-class models match or exceed humans on a narrow slice of classical tasks; (b) all models fail LLM-hardened benchmarks (BigToM, FANToM, OpenToM, Hi-ToM, ToMBench); (c) internal belief representations exist but remain non-robust; (d) advanced ToM in LLMs introduces safety risks (manipulation, privacy, collective misalignment).

### Additional relevant entries (for a fuller reading list)

21. **Jung, Kim, Sclar, Kim, Sap, Choi (2024). "Perceptions to Beliefs: Exploring Precursory Inferences for Theory of Mind in Large Language Models" (PercepToM).** EMNLP 2024. arXiv:2407.06004.
    - Separates **perception inference** (who saw/heard what — LLMs do well) from **perception→belief inference** (LLMs do poorly, lack inhibitory control). Offers a scaffold that combines the two. Releases Percept-ToMi and Percept-FANToM annotations.

22. **Pi, Rebain, Zhang, Shwartz (2024). "Dissecting the Ullman Variations with a SCALPEL: Why do LLMs fail at Trivial Alterations to the False Belief Task?"** arXiv:2406.14737.
    - Builds **SCALPEL**, an incremental-perturbation tool to isolate *why* LLMs fail Ullman's transparent-access variant. Finds failures stem from missing commonsense inference (transparent container → contents known), not from pure ToM failure.

---

## 3. Patterns, Trends, Gaps

### Patterns

- **Benchmark treadmill.** Each generation of benchmarks (ToMi → BigToM / FANToM / Hi-ToM → OpenToM / ToMBench / SimpleToM / MMToM-QA) has been explicitly designed to break the previous generation. The same models that "pass" ToMi often score near random on ToMBench faux-pas or SimpleToM applied-ToM.
- **First-order vs higher-order divergence.** First-order false belief is now largely solved by GPT-4-class models; second-order is shaky; Hi-ToM shows monotonic decay past that. Humanizing long-range dialogue (where 3rd/4th-order nesting naturally appears — "she thinks I think she forgot…") remains brittle.
- **Explicit ≠ applied (SimpleToM gap).** Models correctly infer the mental state when directly asked, then fail to condition subsequent behavior predictions on it. This is arguably the most practically damaging gap for humanization.
- **Representations exist (Zhu 2024) but are non-robust (Shapira, Ullman, Pi).** Linear probes recover belief-like structure; adversarial perturbations still flip answers. LLMs appear to have *unreliable access* to their own belief representations.
- **Psychology vs physics split (OpenToM).** Models track physical-world facts (where the object is) better than psychological-world facts (what the character *feels* about it).
- **Outstanding paper cluster.** SymbolicToM (ACL 2023), MMToM-QA (ACL 2024), and the wider prominence of Strachan (Nature HB 2024) indicate the field is taken seriously by top venues — useful signal for citation weight.

### Trends (2024–2025)

- **From behavior to mechanism.** 2023 was about *whether* LLMs have ToM; 2024–2025 is about *how* — probing, causal interventions, symbolic scaffolds.
- **From narrative to interactive.** FANToM, SimpleToM, and MMToM-QA move evaluation into dialogue and embodied scenarios, which is closer to production humanization use cases than Sally–Anne vignettes.
- **Machine-validation discipline.** The Soubki & Rambow 2025 meta-analysis is likely to set a new methodological bar: any new ToM dataset without machine-validation checks will be discounted.
- **Agentic ToM.** Multi-agent LLM work (Hypothetical Minds, "Theory of Mind for Multi-Agent Collaboration," BDI scaffolds) is pushing ToM from a benchmark score into a design primitive for agent loops.

### Gaps relevant to humanization

- **Dynamic ToM over long dialogues.** Benchmarks are mostly single-scene. Production humanizers need belief tracking across hours- to weeks-long interactions; recency-bias results suggest this is genuinely unsolved.
- **ToM under persona constraints.** No benchmark (as of 2025) isolates whether a model can simultaneously maintain a persona *and* track the user's beliefs; persona-conditioning may degrade ToM.
- **Affective ToM.** Most benchmarks focus on epistemic states (beliefs, knowledge). Desire/emotion attribution is underrepresented outside ToMBench's ability axis.
- **Production-style output effects.** No work rigorously connects measured ToM capability to downstream *human-judgment* outcomes like perceived warmth, tact, or "naturalness" — this is the white-space for the Humanizer project.
- **Non-English ToM.** ToMBench is bilingual (EN/ZH); almost everything else is English-only. Cross-linguistic pragmatic inference (irony, indirect speech) is a large gap.
- **Safety coupling.** Surveys flag that better ToM ≠ safer models (easier manipulation, privacy inference). Humanization work needs to track this co-movement explicitly.

### Open controversies to flag when citing

- Kosinski's "emergence" framing is still cited widely but has been substantially narrowed: cite the **PNAS 2024** version and co-cite Ullman, Shapira, or Soubki & Rambow to avoid overclaiming.
- "GPT-4 matches humans" (Strachan, Nature HB 2024) is true **on that specific battery**; do not generalize to BigToM/FANToM/ToMBench without qualification.
- Linear probes finding belief directions (Zhu 2024) do **not** settle the "genuine ToM" debate — they show structure, not grounded mental-state attribution.

---

## 4. Sources (used in synthesis)

- arXiv:2302.02083 — Kosinski, "Theory of Mind May Have Spontaneously Emerged in LLMs" (→ PNAS 2024).
- arXiv:2302.08399 — Ullman, "LLMs Fail on Trivial Alterations to ToM Tasks."
- arXiv:2210.13312 — Sap et al., "Neural Theory-of-Mind?" EMNLP 2022.
- arXiv:2305.14763 — Shapira et al., "Clever Hans or Neural Theory of Mind?" EACL 2024.
- arXiv:2306.15448 — Gandhi et al., "BigToM," NeurIPS 2023.
- arXiv:2310.15421 — Kim et al., "FANToM," EMNLP 2023.
- arXiv:2310.16755 — Wu et al., "Hi-ToM," Findings of EMNLP 2023.
- arXiv:2402.06044 — Xu et al., "OpenToM," ACL 2024.
- arXiv:2402.15052 — Chen et al., "ToMBench," ACL 2024.
- Nature Human Behaviour 8 (2024), DOI 10.1038/s41562-024-01882-z — Strachan et al.
- arXiv:2401.08743 — Jin et al., "MMToM-QA," ACL 2024 (Outstanding Paper).
- arXiv:2410.13648 — Gu et al., "SimpleToM."
- arXiv:2306.00924 — Sclar et al., "SymbolicToM," ACL 2023 (Outstanding Paper).
- arXiv:2402.18496 — Zhu et al., "Language Models Represent Beliefs of Self and Others," ICML 2024.
- arXiv:2310.10701 — Li et al., "Theory of Mind for Multi-Agent Collaboration via LLMs."
- ACL Anthology 2025.findings-acl.951 — Soubki & Rambow, "Machine Theory of Mind Needs Machine Validation."
- arXiv:2502.06470 — Nguyen, "A Survey of Theory of Mind in LLMs."
- arXiv:2502.08796 — Sarıtaş et al., "A Systematic Review on the Evaluation of LLMs in ToM Tasks."
- arXiv:2407.06004 — Jung et al., "PercepToM," EMNLP 2024.
- arXiv:2406.14737 — Pi et al., "Dissecting the Ullman Variations with a SCALPEL."
- Le, Boureau, Nickel, "Revisiting the Evaluation of Theory of Mind through Question Answering" (ToMi), EMNLP 2019 — ACL Anthology D19-1598.
- arXiv:1904.09728 — Sap et al., "SocialIQA," EMNLP-IJCNLP 2019.
- PMLR v80, Rabinowitz et al., "Machine Theory of Mind," ICML 2018 — arXiv:1802.07740.
