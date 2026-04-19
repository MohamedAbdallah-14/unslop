# Prompt Engineering for Humanization — Academic & Scholarly

*Research angle A of category 01: peer-reviewed and pre-print literature on prompt-engineering techniques that shape LLM outputs to sound and reason more like a human.*

---

## Executive Summary

- **Prompt engineering for "humanization" now spans four overlapping academic threads**: (1) zero-/few-shot *style transfer* via natural-language instructions (Reif et al. 2022; Liu et al. 2023), (2) *persona / role* prompting for voice and perspective (Wang et al. NAACL 2024; Hu & Collier ACL 2024; Gupta et al. ICLR 2024), (3) *adversarial paraphrasing / humanizers* that defeat AI detectors (Krishna et al. NeurIPS 2023; Chakraborty et al. 2025; CoPA EMNLP 2025), and (4) *stylometric and linguistic* work documenting what actually makes text read as "AI" (Sun et al. 2024; ChatGPT vs L2 essays 2025). The most-cited single reference point is the comprehensive taxonomy in *The Prompt Report* (Schulhoff et al. 2024/2025).
- **Persona prompts reliably change voice but not reasoning quality.** Hu & Collier (ACL 2024) find persona variables explain **<10% of variance** in subjective NLP datasets; Zheng et al. (2023/24) show adding social roles to system prompts gives **no reliable accuracy gain** over no-persona baselines; Gupta et al. (ICLR 2024) show persona assignment *degrades* reasoning (up to 70%+ drops on some datasets) and surfaces demographic bias even after explicit de-biasing prompts. Multi-persona *self-collaboration* (SPP, Wang et al. NAACL 2024) is the notable counter-example, but the effect emerges only in the largest models.
- **The dominant stylistic levers identified in the literature are few-shot exemplars, natural-language style instructions ("make this X"), authorship/style embeddings, and iterative paraphrase chains.** Augmented zero-shot prompting (Reif et al. ACL 2022) and its descendants (APR, AAAI 2024; Prompt-Based Editing, EMNLP-Findings 2023; ICLEF, ACL 2024; TinyStyler, EMNLP-Findings 2024) consistently outperform naive instruction prompts, and authorship-embedding-conditioned small models can beat GPT-4 on style matching.
- **"Humanization" is now measurable in two opposing directions.** Cheng, Yu & Jurafsky (2025) introduce **HumT / DumT**, showing that (a) human-like tone is quantifiable via LLM-relative probabilities, (b) *users often prefer less human-like outputs*, and (c) human-like language correlates with warmth, femininity, low status and risks of deception/overreliance. On the other side, DAMAGE (Juzek et al. 2025) benchmarks 19 commercial humanizers and finds they routinely evade detectors while sometimes damaging meaning.
- **Open gaps are acute.** LLMs still fail to imitate the *implicit* style of everyday authors in blogs and forums (Wang et al. 2025); fine-grained, multi-attribute control degrades fluency; persona prompting amplifies socio-demographic bias; and no consensus "naturalness" metric exists — recent work proposes formulaicness (INLG 2025), BERT-based naturalness (Nayak et al. 2021), stylometric fingerprints (Sun et al. 2024), and HumT (Cheng et al. 2025) as competing candidates.

---

## Sources

### 1. The Prompt Report: A Systematic Survey of Prompting Techniques
- **URL**: https://arxiv.org/abs/2406.06608
- **Authors / Org**: Sander Schulhoff, Michael Ilie, Nishant Balepur, Konstantine Kahadze, Amanda Liu, Chenglei Si, Yinheng Li, Aayush Gupta, HyoJung Han, Sevien Schulhoff, et al. (University of Maryland, OpenAI, Stanford, Microsoft, and others)
- **Year / Venue**: 2024, arXiv preprint (v1 Jun 2024, revised through Feb 2025)
- **Core claim**: Establishes a unified taxonomy of **58 LLM prompting techniques** (plus 40 multi-modal, 33 vocabulary terms) and provides a meta-analysis of the entire prefix-prompting literature, including style/persona/role methods relevant to humanization.
- **Techniques mentioned**: Zero-shot, few-shot, CoT, self-consistency, role/persona prompting, style priming, exemplar selection, decomposition, ensembling, self-criticism, automatic prompt optimization.
- **Practical takeaways**: Serves as the authoritative reference list for any humanization prompt stack; recommends exemplar-based style transfer over pure instruction prompts for stylistic control.
- **Summary**: The most comprehensive systematic survey of prompt engineering as of 2025. Provides a canonical vocabulary (e.g., "persona," "style prompting," "exemplar") and consolidates fragmented nomenclature. Any academic discussion of humanization prompts should cite its taxonomy as the baseline.

### 2. A Recipe for Arbitrary Text Style Transfer with Large Language Models
- **URL**: https://aclanthology.org/2022.acl-short.94/
- **Authors / Org**: Emily Reif, Daphne Ippolito, Ann Yuan, Andy Coenen, Chris Callison-Burch, Jason Wei (Google Research, UPenn)
- **Year / Venue**: ACL 2022 (Short Papers, pp. 837–848)
- **Core claim**: **Augmented zero-shot learning (AZSL)** — combining a zero-shot instruction with a short priming sequence of arbitrary style rewrites — lets LLMs perform style transfer for open-ended, non-standard targets ("make this melodramatic," "insert a metaphor") without fine-tuning or in-style exemplars.
- **Techniques mentioned**: Zero-shot instruction prompting; priming sequences of diverse-style rewrites; natural-language style descriptors.
- **Practical takeaways**: A single well-designed priming block generalizes across dozens of arbitrary styles; demonstrates that natural-language style names alone are sufficient control signals for large LMs.
- **Summary**: The foundational academic paper demonstrating that LLMs can be steered toward arbitrary target styles via prompt alone. Cited as the ancestor of most modern humanizer prompts. Importantly, it framed "style" as any rewriting operation, unlocking qualitative targets like "sound more human" or "be conversational."

### 3. Bias Runs Deep: Implicit Reasoning Biases in Persona-Assigned LLMs
- **URL**: https://arxiv.org/abs/2311.04892
- **Authors / Org**: Shashank Gupta, Vaishnavi Shrivastava, Ameet Deshpande, Ashwin Kalyan, Peter Clark, Ashish Sabharwal, Tushar Khot (Allen Institute for AI, Princeton)
- **Year / Venue**: ICLR 2024
- **Core claim**: Assigning sociodemographic personas to LLMs surfaces deep, measurable reasoning biases that are **hard to discern and hard to avoid**, including via explicit de-biasing prompts.
- **Techniques mentioned**: Persona prompting ("You are an X person"); abstention detection; 19 personas across race, gender, religion, disability, political affiliation.
- **Practical takeaways**: Humanization through persona carries a hidden accuracy tax and ethical risk; ChatGPT-3.5 biased in **80% of personas**, some datasets with 70%+ performance drops; GPT-4-Turbo biased in 42%.
- **Summary**: A cautionary cornerstone for persona-based humanization. Shows that even "friendly" persona prompts trigger stereotyped abstentions and degraded reasoning, and that de-biasing prompts "have minimal to no effect." Essential reading when designing any persona-based humanizer.

### 4. Quantifying the Persona Effect in LLM Simulations
- **URL**: https://aclanthology.org/2024.acl-long.554/
- **Authors / Org**: Tiancheng Hu, Nigel Collier (University of Cambridge)
- **Year / Venue**: ACL 2024 (Long Papers, pp. 10289–10307)
- **Core claim**: Persona variables account for **<10% of variance** in subjective NLP annotations, and persona prompting yields only modest, statistically-significant-but-small gains.
- **Techniques mentioned**: Demographic persona prompting; zero-shot simulation; variance decomposition of annotator disagreement.
- **Practical takeaways**: Persona helps most in *low-controversy* disagreement samples; a 70B model + persona prompt captures 81% of the variance achievable by ground-truth-fitted linear regression, an upper bound that is still quite limited in absolute terms.
- **Summary**: Tempers enthusiasm for demographic persona prompting. The authors argue that for most subjective tasks, persona provides diminishing returns, and that naïve persona prompts risk overclaiming simulation fidelity.

### 5. Unleashing the Emergent Cognitive Synergy in Large Language Models: A Task-Solving Agent through Multi-Persona Self-Collaboration (SPP)
- **URL**: https://aclanthology.org/2024.naacl-long.15/
- **Authors / Org**: Zhenhailong Wang, Shaoguang Mao, Wenshan Wu, Tao Ge, Furu Wei, Heng Ji (UIUC, Microsoft Research Asia)
- **Year / Venue**: NAACL 2024
- **Core claim**: **Solo Performance Prompting (SPP)** — in which a single LLM simulates a dynamic panel of fine-grained personas debating a task — reduces hallucination and improves multi-step reasoning on knowledge- and reasoning-intensive benchmarks.
- **Techniques mentioned**: Multi-persona self-collaboration; dynamic expert personas; turn-by-turn internal dialogue.
- **Practical takeaways**: SPP benefits emerge only at GPT-4 scale (not GPT-3.5 or LLaMA2-13B); useful as a template for "thinking like a group" humanization prompts.
- **Summary**: The most commonly cited positive result for persona prompting. Reframes persona less as voice coloring and more as an internal collaboration pattern that mimics how humans reason in groups. Illustrates that humanizing *reasoning* (not just tone) may require multi-persona orchestration.

### 6. Is "A Helpful Assistant" the Best Role for Large Language Models? A Systematic Evaluation of Social Roles in System Prompts
- **URL**: https://arxiv.org/abs/2311.10054
- **Authors / Org**: Mingqian Zheng, Jiaxin Pei, David Jurgens (University of Michigan)
- **Year / Venue**: 2023/2024 preprint; later EMNLP-Findings 2024 presentations
- **Core claim**: Across **162 roles × 2,410 questions × 4 LLM families**, adding social roles/personas to system prompts **does not consistently improve factual accuracy** over a no-persona baseline.
- **Techniques mentioned**: System-prompt role assignment; interpersonal-relationship roles; expertise-domain roles.
- **Practical takeaways**: Role prompting is valuable for *tone, register, and behavioral anchoring*, not for factual gain; automatic role selection performs near random; the 5–15% gains sometimes seen are attributable to implicit domain instructions, not the role framing.
- **Summary**: The canonical academic counterweight to folk wisdom that "You are an expert X" always helps. Establishes that humanization via role is a stylistic intervention, not a cognitive upgrade.

### 7. HumT DumT: Measuring and Controlling Human-Like Language in LLMs
- **URL**: https://arxiv.org/abs/2502.13259
- **Authors / Org**: Myra Cheng, Sunny Yu, Dan Jurafsky (Stanford NLP)
- **Year / Venue**: 2025 preprint (v2 May 2025)
- **Core claim**: Introduces **HumT** and **SocioT** metrics for human-like tone and social perception, and **DumT**, a method to systematically *reduce* human-likeness while preserving task performance.
- **Techniques mentioned**: Relative-probability-based style scoring; DPO-style controlled generation; preference-data analysis.
- **Practical takeaways**: Users often **prefer less human-like outputs**; human-like LLM language correlates with *warmth, social closeness, femininity, and low status*, which in turn correlate with deception risk and overreliance. Any "humanizer" design must consider these downstream perceptions.
- **Summary**: A direct, rigorous challenge to the assumption that "more human-like = better." Provides a measurement tool for the field and argues that humanization is a value-laden design choice, not a universal improvement.

### 8. Paraphrasing Evades Detectors of AI-Generated Text, But Retrieval is an Effective Defense (DIPPER)
- **URL**: https://arxiv.org/abs/2303.13408
- **Authors / Org**: Kalpesh Krishna, Yixiao Song, Marzena Karpinska, John Wieting, Mohit Iyyer (UMass Amherst, Google)
- **Year / Venue**: NeurIPS 2023
- **Core claim**: **DIPPER**, an 11B-parameter discourse-level paraphraser controllable via lexical-diversity and content-reordering knobs, reduces **DetectGPT accuracy from 70.3% to 4.6%** and evades GPTZero, OpenAI classifier, and watermarking schemes.
- **Techniques mentioned**: Controllable paraphrasing; lexical-diversity and reordering codes; retrieval-based defense.
- **Practical takeaways**: Paraphrase-based humanization is shown to be near-universally effective against then-current detectors; authors propose retrieval over API history as a defense.
- **Summary**: The landmark academic result establishing paraphrase-based humanization as a dominant adversarial technique. Nearly all subsequent humanizer research cites DIPPER as the baseline.

### 9. Adversarial Paraphrasing: A Universal Attack for Humanizing AI-Generated Text
- **URL**: https://arxiv.org/abs/2506.07001
- **Authors / Org**: Yize Chen (lead), et al.
- **Year / Venue**: 2025 preprint
- **Core claim**: A *training-free* adversarial paraphrasing framework uses detector signals to steer an instruction-following LLM, reducing TPR@1%FPR on RADAR by **64.49%** and on Fast-DetectGPT by **98.96%**, averaging **87.88%** across diverse detectors.
- **Techniques mentioned**: Detector-guided prompt iteration; instruction-following paraphrasing; training-free attack.
- **Practical takeaways**: Even state-of-the-art detectors collapse under iterative prompt-steered paraphrase; humanization no longer requires specialized fine-tuning.
- **Summary**: Extends DIPPER-style attacks into the era of instruction-tuned LLMs, showing that humanization is now achievable with off-the-shelf models plus a detector-aware prompt loop.

### 10. Your Language Model Can Secretly Write Like Humans: Contrastive Paraphrase Attacks on LLM-Generated Text Detectors (CoPA)
- **URL**: https://aclanthology.org/2025.emnlp-main.433/
- **Authors / Org**: (EMNLP 2025 main track; multi-institution)
- **Year / Venue**: EMNLP 2025
- **Core claim**: **Contrastive Paraphrase Attack** crafts prompts that encourage human-like patterns while *subtracting* machine-like patterns at decoding time, producing texts that reliably evade detection without model fine-tuning.
- **Techniques mentioned**: Contrastive decoding; prompt-conditioned logit arithmetic; human-style vs machine-style prompt pairs.
- **Practical takeaways**: Combining "write like a human" and "do not write like GPT" prompt vectors at decoding yields better evasion than either alone.
- **Summary**: Refines adversarial humanization by showing that *anti-GPTism* signals can be encoded at decoding time, bridging prompt engineering and controlled decoding.

### 11. DAMAGE: Detecting Adversarially Modified AI Generated Text
- **URL**: https://arxiv.org/abs/2501.03437
- **Authors / Org**: Elyas Masrour, Bradley Emi, Max Spero (Pangram Labs; also appears at genaidetect 2025)
- **Year / Venue**: 2025 preprint + ACL 2025 genaidetect workshop
- **Core claim**: Systematic audit of **19 commercial AI-humanizer tools** shows wide variability in quality; many evade existing detectors but damage meaning. Authors build a cross-humanizer detector robust to fine-tuning attacks.
- **Techniques mentioned**: Humanizer taxonomy; cross-humanizer generalization; data-centric augmentation for detectors.
- **Practical takeaways**: Commercial humanizer output varies dramatically; most preserve detection evasion but differ on semantic fidelity.
- **Summary**: Rare academic benchmark of *actual deployed* humanizer tools. Complements DIPPER and Adversarial Paraphrasing by measuring the real-world humanizer ecosystem rather than isolated attack methods.

### 12. Idiosyncrasies in Large Language Models
- **URL**: https://arxiv.org/abs/2502.12150
- **Authors / Org**: Mingjie Sun, Yida Yin, Zhiqiu Xu, J. Zico Kolter, Zhuang Liu (CMU, UC Berkeley)
- **Year / Venue**: 2025 preprint
- **Core claim**: Each LLM leaves a **stylistic fingerprint** in word-level distributions consistent enough that a classifier can distinguish ChatGPT, Claude, Grok, Gemini, and DeepSeek with **97.1% accuracy**, even after rewriting, translation, or summarization by other LLMs.
- **Techniques mentioned**: N-gram fingerprinting; downstream classifier probing; cross-lingual persistence tests.
- **Practical takeaways**: Humanization must address model-specific fingerprints, not just surface "GPTisms." Simple rewriting is insufficient; fingerprints persist through most transformations.
- **Summary**: Provides the empirical basis for "anti-GPTism" prompt engineering. Since idiosyncrasies are encoded in semantic content, pure style instructions will leak model identity unless paraphrase chains or cross-model rewriting is layered in.

### 13. Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors
- **URL**: https://arxiv.org/abs/2509.14543
- **Authors / Org**: Zhengxiang Wang et al.
- **Year / Venue**: 2025 preprint
- **Core claim**: State-of-the-art LLMs in-context imitate user style reasonably well for structured text (news, email) but fail on **blog and forum** writing; **40,000 generations per model × 400 authors**.
- **Techniques mentioned**: Few-shot style imitation; authorship attribution / verification; stylometric + AI-detection ensembles.
- **Practical takeaways**: Effective personal-voice humanization requires more than a handful of demonstrations for informal genres; there is a fundamental adaptation gap for implicit style.
- **Summary**: Establishes the empirical ceiling of current prompt-based personal-voice imitation. Critical for product designs that promise "write in your voice" — in informal registers, the promise is not yet delivered.

### 14. TinyStyler: Efficient Few-Shot Text Style Transfer with Authorship Embeddings
- **URL**: https://aclanthology.org/2024.findings-emnlp.781/
- **Authors / Org**: (EMNLP-Findings 2024; multi-institution)
- **Year / Venue**: EMNLP-Findings 2024
- **Core claim**: An 800M-parameter model conditioned on pre-trained authorship embeddings **outperforms GPT-4** on authorship style transfer and competes with controllable-generation methods on formal↔informal attribute transfer.
- **Techniques mentioned**: Authorship embeddings; small-LM conditioning; few-shot style transfer.
- **Practical takeaways**: For personal-voice humanization, authorship-embedding conditioning is more effective than scaling model size or prompt length.
- **Summary**: Shows that, contrary to "bigger is better," a well-conditioned small model can beat frontier LLMs on fine-grained authorial style. Relevant to on-device and latency-sensitive humanizer systems.

### 15. Empathetic Cascading Networks (ECN): A Multi-Stage Prompting Technique for Empathy and Bias Reduction
- **URL**: https://arxiv.org/abs/2511.18696
- **Authors / Org**: (2025 preprint; multi-author)
- **Year / Venue**: 2025 preprint
- **Core claim**: A four-stage prompt pipeline — **Perspective Adoption → Emotional Resonance → Reflective Understanding → Integrative Synthesis** — yields the highest Empathy Quotient (EQ) scores across GPT-3.5 and GPT-4 while reducing social bias.
- **Techniques mentioned**: Staged/cascading prompting; explicit empathy rubric; bias-mitigation structured prompts.
- **Practical takeaways**: Decomposing "be empathetic" into sequential sub-tasks outperforms a single "be empathetic" instruction.
- **Summary**: Operationalizes empathy in a reproducible prompt pipeline. A useful template for humanization in emotionally sensitive contexts (mental health, support, education).

### 16. Lexical Diversity, Syntactic Complexity, and Readability: A Corpus-Based Analysis of ChatGPT and L2 Student Essays
- **URL**: https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1616935/full
- **Authors / Org**: (Frontiers in Education, 2025)
- **Year / Venue**: 2025, Frontiers in Education (peer-reviewed)
- **Core claim**: ChatGPT essays show **higher lexical diversity (TTR) and syntactic complexity (MLT)** than L2 student essays, but **lower readability and communicative appropriateness** — i.e., more "ornate" yet less natural.
- **Techniques mentioned**: Type-Token Ratio, Mean Length of T-Unit, Flesch readability; corpus-based stylometric comparison.
- **Practical takeaways**: Humanization prompts should actively *reduce* lexical ornamentation and syntactic density while improving readability and pragmatic fit — the reverse of default LLM output tendencies.
- **Summary**: Provides empirical metrics for what "too AI" looks like at the sentence level. Useful as an evaluation target for humanization interventions.

### 17. Prompt-Based Editing for Text Style Transfer
- **URL**: https://aclanthology.org/2023.findings-emnlp.381/
- **Authors / Org**: Guoqing Luo, Yu Tong Han, Lili Mou, Mauajama Firdaus (University of Alberta)
- **Year / Venue**: EMNLP-Findings 2023
- **Core claim**: Reformulates style transfer from autoregressive generation to **prompt-based classification + discrete word-level editing**, which avoids error accumulation and exposure bias typical of generation.
- **Techniques mentioned**: Word-level discrete search; classifier scoring; prompt-based editing.
- **Practical takeaways**: For high-precision style changes (e.g., register shifts), edit-based approaches outperform prompt-based generation at comparable cost.
- **Summary**: Important counterpoint to purely generative humanizers: sometimes targeted edits conditioned by a classifier prompt beat free generation on both style-transfer accuracy and content preservation.

### 18. Automating Text Naturalness Evaluation of NLG Systems
- **URL**: https://arxiv.org/abs/2006.13268
- **Authors / Org**: Erion Çano, Ondřej Bojar (Charles University)
- **Year / Venue**: 2020 arXiv; foundational reference
- **Core claim**: Uses pretrained LM probability distributions to score naturalness of NLG output automatically; shows larger models yield more informative naturalness signals.
- **Techniques mentioned**: Probability-based naturalness scoring; generator–discriminator pairing.
- **Practical takeaways**: Early precedent for measuring "naturalness" that still underlies today's HumT-style metrics.
- **Summary**: The historical reference for automated naturalness evaluation. Useful for framing HumT (Cheng et al. 2025) as part of a lineage rather than a novel construct.

---

## Key Techniques / Patterns

The academic literature converges on a small set of reusable humanization patterns:

1. **Natural-language style instructions ("make this X").** Reif et al. 2022 established that LLMs respond to free-form style descriptors. Works well for coarse, single-attribute changes; degrades on multi-attribute control (Controllable Text Generation Survey, arXiv 2408.12599).
2. **Few-shot stylistic exemplars.** Providing 3–8 examples in the target voice consistently outperforms zero-shot style instructions (Wang et al. 2025; TinyStyler; ICLEF). The marginal benefit saturates quickly and is weakest for informal genres.
3. **Persona / role in system prompt.** Reliable for tone, register, formality, and vocabulary anchoring; *unreliable* for factual accuracy (Zheng et al.); *dangerous* for reasoning and fairness (Gupta et al. ICLR 2024).
4. **Multi-persona self-collaboration (SPP).** Large models can internally simulate a panel; useful for reasoning-heavy humanization tasks where "think like a group" is the target.
5. **Staged / cascading prompts.** ECN for empathy; CoT for reasoning; Chain-of-Verification for hallucination control. Decomposition beats monolithic instructions for nuanced human-like behaviors (empathy, reflection, qualification).
6. **Anti-pattern prompts (anti-GPTisms).** Academic support for anti-slop prompts is weak but growing. Idiosyncrasies (Sun et al. 2025) and stylometric studies imply that explicitly banning common markers — *"delve," "multifaceted," "it's important to note that," "In conclusion,"* — reduces detectability, though the fingerprint persists in deeper distributions.
7. **Adversarial paraphrase chains.** DIPPER, Adversarial Paraphrasing, and CoPA show that iterative paraphrasing — often detector-guided — is the single most reliable humanization operator. Academic consensus: this works *too well* for current detectors.
8. **Authorship-embedding conditioning.** TinyStyler demonstrates that dense stylistic embeddings dominate prompt-only methods for matching a specific author. A practical hybrid: embed-conditioned rewriter + prompt-specified register.
9. **Prompt-based editing / contrastive decoding.** Rather than regenerate, classify and edit (EMNLP-Findings 2023) or decode with contrastive "human vs machine" prompt vectors (CoPA). Preserves content while shifting style.
10. **Measurement-driven prompting.** HumT / DumT, stylometric readability metrics, and EQ-based empathy scoring provide targets for prompt optimization loops. Increasingly, humanization prompts are being optimized against quantitative naturalness metrics rather than tuned by hand.

---

## Notable Quotes

> "LLMs harbor deep rooted bias against various socio-demographics underneath a veneer of fairness. While they overtly reject stereotypes when explicitly asked … they manifest stereotypical and erroneous presumptions when asked to answer questions while adopting a persona."
> — *Gupta et al., "Bias Runs Deep," ICLR 2024 (Abstract)*

> "Persona variables account for <10% variance in annotations in existing subjective NLP datasets. Nonetheless, incorporating persona variables via prompting in LLMs provides modest but statistically significant improvements."
> — *Hu & Collier, "Quantifying the Persona Effect in LLM Simulations," ACL 2024 (Abstract)*

> "Should LLMs generate language that makes them seem human? … We find that users prefer less human-like outputs from LLMs in many contexts. HumT also offers insights into the perceptions and impacts of anthropomorphism: human-like LLM outputs are highly correlated with warmth, social closeness, femininity, and low status, which are closely linked to the aforementioned harms."
> — *Cheng, Yu & Jurafsky, "HumT DumT," arXiv 2502.13259 (Abstract)*

> "While LLMs can approximate user styles in structured formats like news and email, they struggle with nuanced, informal writing in blogs and forums … our findings highlight a fundamental gap in personalized LLM adaptation."
> — *Wang et al., "Catch Me If You Can? Not Yet," arXiv 2509.14543 (Abstract)*

> "LLMs possess unique fingerprints manifesting as differences in the frequency of certain lexical and morphosyntactic features … these patterns persist even when texts are rewritten, translated, or summarized by external LLMs."
> — *Sun et al., "Idiosyncrasies in Large Language Models," arXiv 2502.12150 (Abstract, §1 Introduction)*

> "Our framework achieves dramatic evasion rates — reducing true positives at 1% false positive by 64.49% on RADAR and 98.96% on Fast-DetectGPT, with an average reduction of 87.88% across diverse detectors."
> — *Chakraborty et al., "Adversarial Paraphrasing," arXiv 2506.07001 (Abstract)*

> "Our approach matches human performance on most stylistic tasks, but still lags behind on structural tasks such as adding or deleting content."
> — *Prompt-Based Style Control paper (OpenReview zHoLvqFAJJ)*

> "Assigning multiple fine-grained personas improves problem-solving abilities compared to using a single or fixed number of personas … cognitive synergy emerges only in GPT-4, not in less capable models."
> — *Wang et al., "Solo Performance Prompting," NAACL 2024 (§4 Experiments)*

> "Adding personas in system prompts does not improve model performance compared to a control setting … the effect of each persona can be largely random."
> — *Zheng, Pei & Jurgens, "Is A Helpful Assistant the Best Role?" arXiv 2311.10054 (§4 Results)*

---

## Emerging Trends

- **From single-prompt style to measurement-guided prompt optimization.** HumT/DumT, formulaicness (INLG 2025), and LLM-as-judge naturalness scoring (arXiv 2310.05657) are increasingly used as optimizable targets. Promptomatix (arXiv 2507.14241) exemplifies automatic prompt optimization reaching humanization tasks.
- **Anti-anthropomorphism backlash.** HumT/DumT and a growing CHI/CSCW literature (e.g., LLM Whisperer, CHI 2025) argue that more-human-like LLMs cause overreliance, deception, and gendered perception. Expect 2026+ academic work to focus on *controlled* humanization — human-like enough to be usable, but disclosing AI identity.
- **Adversarial paraphrase as de facto humanizer.** DIPPER → RADAR → Adversarial Paraphrasing → CoPA shows an escalating arms race. Training-free, detector-guided paraphrase is now the dominant academic humanizer pattern, eclipsing fine-tuned style-transfer models.
- **Fingerprint-aware humanization.** Post-Sun et al. 2025, prompt engineering is shifting from generic "anti-GPTisms" to model-specific fingerprint suppression (lexical distribution flattening, cross-model rewrite chains).
- **Multi-stage humanization pipelines.** ECN for empathy, Chain-of-Verification for hallucination, SPP for reasoning — the field is converging on *decomposed* humanization prompts rather than monolithic instructions.
- **Authorship-embedding + prompt hybrids.** TinyStyler and subsequent work suggest the next-gen personal-voice humanizer is a small, embedding-conditioned rewriter steered by a natural-language style prompt, rather than a frontier LLM with a long prompt.
- **HCI / CHI reframing of "humanization" as a design question.** Papers like LLM Whisperer (CHI 2025), HumT/DumT, and Schmidmaier et al. (2025, secondary empathic channel) argue humanization should be evaluated against user tasks and trust dynamics, not just text similarity.

---

## Open Questions / Gaps

- **No consensus naturalness metric.** Formulaicness (INLG 2025), HumT, BERT-based naturalness (Nayak 2021), stylometric fingerprints (Sun et al.), and EQ-based empathy scores measure partly overlapping, partly orthogonal constructs. The field lacks a unified benchmark.
- **Implicit everyday-author style remains unsolved.** Wang et al. 2025 shows blog/forum imitation fails; academic work on efficient personal-voice adaptation via prompt alone is open.
- **Persona prompting's fairness costs are unmitigated.** Gupta et al. 2024 shows de-biasing prompts fail; no published method eliminates persona-induced bias while retaining voice benefits.
- **Anti-GPTism prompts lack rigorous study.** The slop-word literature is largely blog-level (ANTI-SLOP.md, slop-score). No peer-reviewed paper yet isolates which bans are causally effective vs cosmetic.
- **Multi-attribute style control degrades fluency.** CTG Survey (arXiv 2408.12599) and Prompt-Based Style Control (OpenReview) both document the fine-grained-control-vs-fluency trade-off; no published prompt engineering method cleanly resolves it.
- **Humanizers weaponize the detection asymmetry.** Resilience research (arXiv 2511.00416) shows detectors catch plagiarism-direction paraphrase but fail on authorship-obfuscation direction; implications for academic integrity and journalism remain underexplored.
- **Empathy and emotional humanization cross cultures poorly.** ECN is English-centric; cross-lingual empathetic prompt engineering is an open area, intersecting multilingual prompting surveys (arXiv 2505.11665).
- **Interaction of humanization prompts with model alignment (RLHF).** Academic work rarely isolates how post-training shaping (helpful/harmless/honest) constrains or distorts humanization prompts — an open question for 2026+ research.

---

## References

1. https://arxiv.org/abs/2406.06608 — Schulhoff et al., *The Prompt Report* (arXiv, 2024/2025)
2. https://aclanthology.org/2022.acl-short.94/ — Reif et al., *A Recipe for Arbitrary Text Style Transfer* (ACL 2022)
3. https://arxiv.org/abs/2311.04892 — Gupta et al., *Bias Runs Deep* (ICLR 2024)
4. https://aclanthology.org/2024.acl-long.554/ — Hu & Collier, *Quantifying the Persona Effect* (ACL 2024)
5. https://aclanthology.org/2024.naacl-long.15/ — Wang et al., *Solo Performance Prompting* (NAACL 2024)
6. https://arxiv.org/abs/2311.10054 — Zheng, Pei & Jurgens, *Is "A Helpful Assistant" the Best Role?* (arXiv 2023/2024)
7. https://arxiv.org/abs/2502.13259 — Cheng, Yu & Jurafsky, *HumT DumT* (arXiv 2025)
8. https://arxiv.org/abs/2303.13408 — Krishna et al., *DIPPER: Paraphrasing Evades Detectors* (NeurIPS 2023)
9. https://arxiv.org/abs/2506.07001 — Chakraborty et al., *Adversarial Paraphrasing* (arXiv 2025)
10. https://aclanthology.org/2025.emnlp-main.433/ — *Contrastive Paraphrase Attacks (CoPA)* (EMNLP 2025)
11. https://arxiv.org/abs/2501.03437 — Masrour, Emi, Spero, *DAMAGE* (arXiv 2025 / ACL 2025 workshop)
12. https://arxiv.org/abs/2502.12150 — Sun et al., *Idiosyncrasies in Large Language Models* (arXiv 2025)
13. https://arxiv.org/abs/2509.14543 — Wang et al., *Catch Me If You Can? Not Yet* (arXiv 2025)
14. https://aclanthology.org/2024.findings-emnlp.781/ — *TinyStyler* (EMNLP-Findings 2024)
15. https://arxiv.org/abs/2511.18696 — *Empathetic Cascading Networks (ECN)* (arXiv 2025)
16. https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1616935/full — *Lexical Diversity, Syntactic Complexity, and Readability: ChatGPT vs L2 Essays* (Frontiers in Education, 2025)
17. https://aclanthology.org/2023.findings-emnlp.381/ — *Prompt-Based Editing for Text Style Transfer* (EMNLP-Findings 2023)
18. https://arxiv.org/abs/2006.13268 — Çano & Bojar, *Automating Text Naturalness Evaluation* (arXiv 2020)
19. https://arxiv.org/abs/2408.12599 — *Controllable Text Generation for LLMs: A Survey* (arXiv 2024)
20. https://aclanthology.org/2024.acl-long.854/ — *ICLEF: In-Context Learning with Expert Feedback* (ACL 2024)
21. https://aclanthology.org/2025.findings-emnlp.1261/ — *The Prompt Makes the Person(a): Sociodemographic Persona Prompting* (EMNLP-Findings 2025)
22. https://aclanthology.org/2025.inlg-main.21/ — *Incorporating Formulaicness in Naturalness Evaluation* (INLG 2025)
23. https://arxiv.org/abs/2109.02938 — *Naturalness Evaluation via BERT* (arXiv 2021)
24. https://dl.acm.org/doi/10.1145/3706598.3714025 — *LLM Whisperer: An Inconspicuous Attack to Bias LLM Responses* (CHI 2025)
