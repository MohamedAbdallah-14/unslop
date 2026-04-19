# Creative Writing & Storytelling — Academic

**Research value: high** — The academic corpus on LLM creative writing is dense and convergent: a canonical set of co-writing interfaces (Wordcraft, CoAuthor, Dramatron, TaleBrush), a well-mapped story-generation pipeline lineage (Fan→Re3→DOC→CritiCS→Weaver), a coherent set of evaluation frameworks adapted from creativity psychology (TTCW, CAT, AUT), and a growing, empirically-robust literature on *collective* homogenization that directly constrains what "humanizing" AI output can mean at scale.

## Executive Summary

Academic work on AI-assisted creative writing clusters into five tightly connected lines:

1. **Human–AI co-writing interfaces and interaction datasets** — Wordcraft, CoAuthor, Dramatron, TaleBrush, Storium — establish the interaction patterns (continue / infill / rewrite, outline-to-scene hierarchical generation, fortune-sketching) and release keystroke-level data that the rest of the field evaluates against.
2. **Long-form story generation pipelines** — Hierarchical Neural Story Generation → Re3 → DOC → Weaver → CritiCS / DOME — progressively move from left-to-right decoding to plan-draft-revise-critique loops, treating "write a novella" as a compositional pipeline rather than a single prompt.
3. **Creativity-psychology-derived evaluation** — Torrance Tests of Creative Writing (TTCW), Consensual Assessment Technique (CAT), Alternative Uses Test (AUT), Creative Problem Solving (CPS) rubrics — these are the principal frameworks researchers adapt because n-gram metrics (BLEU, ROUGE) are demonstrably inadequate for creative text.
4. **LLM-specific benchmarks for long-form and personalized creative writing** — BooookScore, LongLaMP, Suri, NoveltyBench, EQ-Bench Creative Writing, Confederacy of Models, Judgemark — formalize what "good long creative text" means at scale and operationalize LLM-as-judge with bias-mitigation.
5. **Homogenization, style, and naturalness** — Doshi & Hauser (*Science Advances* 2024), Anderson et al. (2025), Reinhart et al. (*PNAS* 2025), and stylometric detection work establish that even "good-enough" LLM fiction is (a) statistically distinguishable from human writing at machine level despite fooling human readers, and (b) collectively *homogenizing* the creative output of its users — reframing the humanization problem from "sound human" to "preserve inter-author diversity."

The central academic finding, which cuts across all five clusters, is that LLMs are plausible *sentence-local* stylists but persistently weak at **originality, long-range coherence, stylistic variation, and surprise**. Chakrabarty et al.'s TTCW work — the field's most-cited scalable creativity evaluation — found that LLM stories pass **3–10× fewer creativity tests than professional human stories**, and that none of the evaluated LLMs positively correlated with expert creativity judgments. This result has not been meaningfully overturned by subsequent work.

---

## Papers (26)

### Co-writing interfaces and interaction datasets

**1. CoAuthor: Designing a Human-AI Collaborative Writing Dataset for Exploring Language Model Capabilities**
- Authors: Mina Lee, Percy Liang, Qian Yang · Stanford
- Venue: CHI 2022 · arXiv:2201.06796
- Summary: Keystroke-level dataset of 1,445 writing sessions (830 creative stories, 615 argumentative essays) from 63 writers collaborating with four GPT-3 instances. 72.3% suggestion acceptance; 72.6% of final text human-written. Public dataset + replay interface at coauthor.stanford.edu.
- Humanization relevance: The canonical empirical substrate for studying *what humans actually accept* from LLM suggestions during creative writing.

**2. Wordcraft: A Human-AI Collaborative Editor for Story Writing**
- Authors: Andy Coenen, Daphne Ippolito, Ann Yuan, Emily Reif, Luke Davis · Google PAIR
- Venue: arXiv 2021 · arXiv:2107.07430
- Summary: Few-shot-prompted single-model editor supporting continuation, infill, and rewrite as conversational affordances. Seeded the Wordcraft Writers Workshop (13 professional writers).
- Humanization relevance: Established the core interaction grammar (`continue`, `infill`, `rewrite`, `elaborate`) reused by almost every subsequent AI-writing interface.

**3. Creative Writing with an AI-Powered Writing Assistant: Perspectives from Professional Writers**
- Authors: Daphne Ippolito, Ann Yuan, Andy Coenen, Sehmon Burnam · Google Research
- Venue: arXiv 2022 · arXiv:2211.05030
- Summary: Qualitative study with 13 commissioned professional writers using Wordcraft. Found LLMs useful for brainstorming, world-building, research — but struggle to preserve authorial voice, "rehash tired tropes," and require heavy human curation.
- Humanization relevance: First rigorous evidence that *amateur* benchmarks overstate how well LLMs serve writers with an established voice.

**4. Dramatron: Co-Writing Screenplays and Theatre Scripts with Language Models — An Evaluation by Industry Professionals**
- Authors: Piotr Mirowski, Kory W. Mathewson, Jaylen Pittman, Richard Evans · DeepMind
- Venue: CHI 2023 · arXiv:2209.14958
- Summary: Hierarchical prompt-chaining from log-line → title → characters → plot → scene descriptions → dialogue, circumventing long-context coherence failures. Evaluated with 15 theatre/film professionals; four co-written scripts staged publicly as *Plays by Bots*.
- Humanization relevance: The reference design for decomposition-based long-form generation; established "world-building assistant, not autonomous author" as the acceptable co-creative frame.

**5. STORIUM: A Dataset and Evaluation Platform for Machine-in-the-Loop Story Generation**
- Authors: Nader Akoury, Shufan Wang, Josh Whiting, Stephen Hood, Nanyun Peng, Mohit Iyyer
- Venue: EMNLP 2020
- Summary: 6K author-generated stories (125M tokens) with fine-grained in-situ annotations (character goals/attributes). Fine-tuned models deployed inside the live Storium community; evaluation uses real authors' edits to model suggestions, and those automatic edit-based metrics correlate with user ratings.
- Humanization relevance: Pioneered evaluation-in-the-wild — the rare benchmark where the evaluation surface is real creative use, not crowdsourced ratings.

**6. TaleBrush: Sketching Stories with Generative Pretrained Language Models**
- Authors: John Joon Young Chung et al. · Naver AI
- Venue: CHI 2022 (Extended Abstracts)
- Summary: Visual story-sketching interface where users draw the protagonist's fortune arc as an x/y line that controls a GPT-Neo backbone. User study (n=14) showed reliable control plus retained novelty.
- Humanization relevance: Demonstrates that *non-linguistic control surfaces* can dictate narrative shape without the user ceding voice to a language prompt.

### Long-form story generation pipelines

**7. Hierarchical Neural Story Generation**
- Authors: Angela Fan, Mike Lewis, Yann Dauphin · Facebook AI
- Venue: ACL 2018 · arXiv:1805.04833
- Summary: 300K WritingPrompts dataset; two-stage generate-premise-then-passage architecture with gated multi-scale self-attention and model fusion. Humans prefer hierarchical vs flat 2:1. ~1,750 citations — the foundational hierarchical-story-gen paper.

**8. Re3: Generating Longer Stories with Recursive Reprompting and Revision**
- Authors: Kevin Yang, Yuandong Tian, Nanyun Peng, Dan Klein · UC Berkeley
- Venue: EMNLP 2022 · arXiv:2210.06774
- Summary: Four-stage Plan → Draft → Rewrite → Edit loop on GPT-3, producing >2,000-word stories with +14pp plot coherence and +20pp premise relevance vs flat baselines.

**9. DOC: Improving Long Story Coherence With Detailed Outline Control**
- Authors: Kevin Yang, Dan Klein, Nanyun Peng, Yuandong Tian
- Venue: ACL 2023 · arXiv:2212.10077
- Summary: Refines Re3 by generating a *detailed* hierarchical outline first, then enforcing it during drafting via a Detailed Controller. +22.5pp plot coherence, +28.2pp outline relevance, +20.7pp interestingness over Re3.

**10. Weaver: Foundation Models for Creative Writing**
- Authors: Tiannan Wang et al. · Aiwaves
- Venue: arXiv 2024 · arXiv:2401.17268
- Summary: Four-size (1.8B/6B/14B/34B) model family pre-trained on writing-curated corpora, aligned to professional-writer preferences via novel instruction-synthesis methods; natively supports RAG and tool use. Weaver Ultra reported to beat GPT-4 on writing-specific benchmarks.
- Humanization relevance: One of the first serious attempts at a *writing-specialist* base model — evidence that humanization can be baked into pre-training, not just prompting.

**11. Collective Critics for Creative Story Generation (CritiCS)**
- Authors: Minwook Bae, Hyounghun Kim
- Venue: EMNLP 2024 · arXiv:2410.02428
- Summary: Two-stage multi-critic framework (CrPlan for plan refinement, CrText for generation) where a council of LLM critics plus a leader iteratively revise drafts. Human eval shows significant gains on creativity and engagement while holding coherence.
- Humanization relevance: Generalizes agentic revision loops to creativity; complementary to Re3/DOC which target coherence.

### Evaluation frameworks and benchmarks

**12. Art or Artifice? Large Language Models and the False Promise of Creativity (TTCW)**
- Authors: Tuhin Chakrabarty, Philippe Laban, Divyansh Agarwal, Smaranda Muresan, Chien-Sheng Wu · Columbia + Salesforce AI
- Venue: CHI 2024 · arXiv:2309.14556
- Summary: Introduces the Torrance Test of Creative Writing (TTCW), 14 binary tests across Fluency, Flexibility, Originality, Elaboration. 10 creative-writing experts rated 48 stories (pro + LLM). **LLM stories pass 3–10× fewer tests than professional stories; no LLM-as-judge positively correlates with expert judgments.**
- Humanization relevance: The most cited negative result in the field — every subsequent humanization claim must explain how it moves this baseline.

**13. Creativity Support in the Age of Large Language Models: An Empirical Study Involving Emerging Writers**
- Authors: Tuhin Chakrabarty, Vishakh Padmakumar, He He, Nanyun Peng · Columbia / NYU / UCLA
- Venue: ACM Creativity & Cognition 2024 · arXiv:2309.12570
- Summary: n=30 emerging writers use an LLM-assisted interface grounded in the Flower & Hayes cognitive writing model (plan / translate / review). Writers find LLMs most helpful for *translation* and *reviewing*, least helpful for planning.
- Humanization relevance: Localizes where in the cognitive writing process LLMs add vs subtract value — useful input for designing human-AI collaboration.

**14. BooookScore: A Systematic Exploration of Book-Length Summarization in the Era of LLMs**
- Authors: Yapei Chang, Kyle Lo, Tanya Goyal, Mohit Iyyer · UMass / AI2
- Venue: ICLR 2024 (oral) · arXiv:2310.00785
- Summary: 1,193 human annotations on GPT-4 book summaries define 8 coherence error types; BooookScore = fraction of error-free sentences. Saves ~$15K and ~500 hours vs manual eval; high agreement with humans.
- Humanization relevance: Goes beyond sentence-level fluency to measure *book-scale* narrative coherence — necessary for any long-form humanization claim.

**15. LongLaMP: A Benchmark for Personalized Long-form Text Generation**
- Authors: Ishita Kumar, Snigdha Viswanathan, Sushrita Yerra, Alireza Salemi, Ryan A. Rossi, et al.
- Venue: arXiv 2024 · arXiv:2407.11016
- Summary: Benchmark for personalized long-form generation (reviews, emails, abstracts) using per-user history; zero-shot and fine-tuned baselines; HF dataset + code released.
- Humanization relevance: Formalizes *personalization to a specific human's past writing* — a direct operationalization of "humanize to this user's voice."

**16. Suri: Multi-Constraint Instruction Following for Long-form Text Generation**
- Authors: Chau M. Pham, Simeng Sun, Mohit Iyyer
- Venue: Findings of EMNLP 2024 · arXiv:2406.19371
- Summary: 20K long human-written texts paired with synthesized instructions containing ~10 semantic/stylistic constraints each. Introduces Instructional ORPO (I-ORPO) trained against corrupted-instruction negatives (preference collection on 5K-token outputs being infeasible).
- Humanization relevance: Supplies training data + preference signal for long-form, constraint-heavy creative generation.

**17. A Confederacy of Models: a Comprehensive Evaluation of LLMs on Creative Writing**
- Authors: Carlos Gómez-Rodríguez, Paul Williams
- Venue: Findings of EMNLP 2023
- Summary: Human evaluation of ~12 LLMs on creative writing across fluency, coherence, originality, humor, style. Quantifies how far models were from each other and from humans on open-ended creative prompts.

**18. NoveltyBench: Evaluating Creativity and Diversity in Language Models**
- Authors: (team, 2025) · arXiv:2504.05228
- Summary: Prompts designed to elicit *multiple distinct* high-quality answers; scores diversity over quality-gated outputs. Finding: SOTA models produce significantly less diversity than humans; larger models often less diverse than smaller ones.
- Humanization relevance: Directly quantifies the homogenization failure mode at the model-output level.

**19. Sonnet or Not, Bot? Poetry Evaluation for Large Models and Datasets**
- Authors: Melanie Walsh et al.
- Venue: Findings of EMNLP 2024
- Summary: 4.1K expert-annotated poems across English poetic forms (sonnet, sestina, pantoum, etc.); LLMs achieve surprisingly high form-recognition but struggle on unfixed forms.
- Humanization relevance: One of few benchmarks where literary form — not just sentiment or coherence — is the target of evaluation.

**20. Evaluating Diversity in Automatic Poetry Generation**
- Authors: (team)
- Venue: EMNLP 2024
- Summary: Measures structural, lexical, semantic, stylistic diversity vs human distributions; finds LLMs systematically underperform on rhyme sufficiency, semantic range, and length distribution, but that style-conditioning + char-level modeling close much of the gap.

### Style, naturalness, and detection

**21. MERMAID: Metaphor Generation with Symbolism and Discriminative Decoding**
- Authors: Tuhin Chakrabarty, Xurui Zhang, Smaranda Muresan, Nanyun Peng
- Venue: NAACL 2021
- Summary: Parallel metaphor/literal corpus from Gutenberg Poetry + MLM/commonsense inference; metaphor-discriminator-guided decoding. Preferred 66% vs baselines; metaphor-enhanced poems preferred 68% vs originals.
- Humanization relevance: Early demonstration that *figurative* language — a classic humanness signal — can be learned as a controllable lever.

**22. Do LLMs Write Like Humans? Variation in Grammatical and Rhetorical Styles**
- Authors: Alex Reinhart, David West Brown, Ben Markey et al. · CMU
- Venue: PNAS 2025, 122(8)
- Summary: Biber-framework comparison of GPT-4o / GPT-4o Mini / Llama 3 vs humans. Instruction-tuned LLMs use present participial clauses 2–5× human rate, nominalizations 1.5–2×, passive voice ~0.5×; overuse "camaraderie," "tapestry," "palpable," "intricate." Differences *larger* for instruction-tuned models than base models.
- Humanization relevance: RLHF-ish post-training is a major cause of measurable un-humanness; this paper is the current citation for "why instruction-tuned models sound like ChatGPT."

**23. Stylometric Comparisons of Human versus AI-Generated Creative Writing**
- Authors: (team, 2025) · *Humanities and Social Sciences Communications* (Nature)
- Summary: Machine classifiers discriminate human vs LLM creative writing at 93–98% accuracy while humans perform near chance. LLM outputs cluster tightly by model; human texts form broader clusters. GPT-4 more internally consistent than GPT-3.5; Llama-70B similar to GPT-4.
- Humanization relevance: Establishes the "statistical fingerprint" ceiling — even polished LLM fiction is trivially detectable at machine level.

### Homogenization and the collective-creativity frame

**24. Generative AI Enhances Individual Creativity but Reduces the Collective Diversity of Novel Content**
- Authors: Anil R. Doshi, Oliver P. Hauser
- Venue: *Science Advances* 2024 (doi: 10.1126/sciadv.adn5290)
- Summary: ~300-writer experiment across three conditions (no AI / 1 AI idea / 5 AI ideas). AI assistance lifts individual creativity (10–11%) and readability (22–26%), especially for less-creative writers — but AI-assisted stories cluster significantly more than unassisted stories. Framed as a social dilemma: individual rationality → collective homogenization.
- Humanization relevance: Redefines the humanization problem at population scale — "humanize this output" must not become "homogenize all outputs."

**25. We're Different, We're the Same: Creative Homogeneity Across LLMs**
- Authors: Emily Anderson et al.
- Venue: arXiv 2025 · arXiv:2501.19361
- Summary: Shows LLM creative outputs are more similar to *other LLM outputs* than human outputs are to each other, controlling for structure. Effect persists across models → points at architecture-/training-data-level convergence, not a single-model quirk.

### HCI design and agency

**26. A Design Space for Intelligent and Interactive Writing Assistants**
- Authors: Mina Lee, Katy Ilonka Gero, John Joon Young Chung, Hua Shen, et al. (40+ co-authors)
- Venue: CHI 2024
- Summary: Systematic review of 115 writing-assistant papers across NLP / HCI / CSS, synthesized into a 5-axis design space (Task / User / Technology / Interaction / Ecosystem). Writing-assistant.github.io hosts the interactive taxonomy.

**27. Where Do I 'Add the Egg'? Exploring Agency and Ownership in AI Creative Co-Writing Systems**
- Authors: Jeb Thomas-Mitchell et al.
- Venue: arXiv 2025 · arXiv:2509.15440
- Summary: n=18 professional + non-professional writers try three functionally identical co-writing systems differing only in interface metaphor (agentic / tool-like / magical). Metaphors shape *where users feel control* and *whether they feel like authors*, not just system usability.

---

## Key Techniques & Patterns

- **Hierarchical decomposition** (Dramatron, Re3, DOC, DOME, CritiCS). Treat "write a story" as plan → draft → revise → edit, with LLM calls at each level. Standard mitigation for long-range coherence failures.
- **TTCW-style binary rubrics for creativity.** 14 yes/no criteria (Fluency, Flexibility, Originality, Elaboration) with expert raters replace Likert vagueness; the field's most-reused creativity protocol.
- **LLM-as-judge with bias mitigation** (EQ-Bench v3, Judgemark, BooookScore). Pairwise Elo + rubric scoring; explicit controls for length bias, position bias, verbosity, poetic incoherence; ensemble judging.
- **Interaction-dataset evaluation** (CoAuthor, Storium). Evaluate model behavior from *edits real users make to suggestions*, not from post-hoc ratings.
- **Adapted psychology instruments.** TTCT, Torrance Test of Creative Writing, AUT, CAT, CPS rubrics — all imported directly from creativity psychology, with modifications for LLM-scale sampling.
- **Instruction-backtranslation + I-ORPO for long-form.** Suri: synthesize instructions from real long human texts; use corrupted-instruction negatives instead of preference pairs (infeasible at 5K-token scale).
- **Multi-constraint outputs.** 8–10 semantic/stylistic constraints per instruction is now the de-facto long-form difficulty target (Suri, LongLaMP).
- **Homogenization as first-class metric.** NoveltyBench, "We're Different, We're the Same," Doshi & Hauser — diversity-across-outputs is promoted from post-hoc observation to evaluation axis.
- **Metaphor / figurative language as controllable lever.** MERMAID shows figurative-ness can be discriminatively decoded at inference time — an inference-time humanization knob.

## Trends

- **Creativity psychology is becoming the lingua franca of evaluation.** Since ~2023 almost every serious creative-writing evaluation paper either (a) re-uses TTCW, (b) re-uses CAT with LLM judges, or (c) builds on AUT. N-gram-only creative-writing evaluations are increasingly rejected at top venues.
- **The long-form story pipeline is stabilizing.** Plan → detailed outline → draft → multi-critic revision is now the dominant architecture (DOC, CritiCS, DOME, SWAG). Debate is over critic composition and memory, not the overall shape.
- **Instruction-tuning is the current humanness bottleneck.** Reinhart et al. (PNAS 2025), stylometry papers, and homogenization studies converge: post-training pushes models toward a shared "ChatGPT voice" that base models don't have. Humanization research is shifting from prompts to post-training recipes.
- **Specialist writing models.** Weaver 2024 is the first of a likely wave — curated pre-training + writer-preference alignment + native RAG/tools. Generalist models may lose creative-writing SOTA to domain specialists.
- **From individual to collective evaluation.** Doshi & Hauser's *Science Advances* paper moved the conversation from "is this story good?" to "what happens to literature if everyone uses this tool?" Follow-up work (Anderson 2025, NoveltyBench) treats collective homogenization as a primary failure mode.
- **HCI-side focus on metaphor and agency.** "Where Do I Add the Egg?" signals that *interface framing* (agentic vs tool-like vs magical) now receives the same empirical attention as prompts or models.

## Gaps / Open Questions

- **No consensus humanness metric.** TTCW measures creativity; BooookScore measures coherence; NoveltyBench measures diversity; stylometry measures distinguishability; CAT measures expert preference. No unified scalar or vector reliably captures "sounds human, reads as authored."
- **Professional-writer evaluations are sparse and small.** Ippolito et al. used 13; Chakrabarty used 10 raters / 30 emerging writers. Replication power is limited, and results may not generalize to amateur use, which is where most LLM-assisted writing actually happens.
- **The voice-preservation problem is unsolved.** Every professional-writer study reports the same complaint: LLMs cannot hold the author's voice across a long draft. Style-transfer work (STYLL, author-style steering vectors) is promising but not integrated into long-form pipelines.
- **Collective homogenization mitigation is early.** Doshi/Hauser's result is widely cited but interventions (diverse personas, sampler-level diversity promotion, persona rotation) are only beginning to be empirically tested.
- **LLM-as-judge reliability is domain-specific.** Rethinking Creativity Evaluation (EACL 2026) shows metrics that separate creative writing fail on problem-solving and vice versa. Cross-domain creativity evaluation remains unsolved.
- **Evaluation-leakage risk.** Most creative benchmarks use public web-sourced reference stories; newer LLMs likely saw them in pre-training, inflating scores without corresponding creativity.
- **Multilingual and non-English creative writing is drastically under-represented.** Almost all major benchmarks (CoAuthor, TTCW, BooookScore, LongLaMP) are English-only; non-English literary naturalness is largely unstudied.
- **Detection vs authorial voice are conflated.** Stylometric work shows 93–98% classifier accuracy, but that is a statistical-tell question, not a literary-quality question. Humanization research often slides between the two.

## Sources

- Lee, Liang, Yang. *CoAuthor: Designing a Human-AI Collaborative Writing Dataset*. CHI 2022. [arXiv:2201.06796](https://arxiv.org/abs/2201.06796). [coauthor.stanford.edu](https://coauthor.stanford.edu/)
- Coenen, Yuan, Reif, Ippolito, Davis. *Wordcraft: A Human-AI Collaborative Editor*. 2021. [arXiv:2107.07430](https://arxiv.org/abs/2107.07430)
- Ippolito, Yuan, Coenen, Burnam. *Creative Writing with an AI-Powered Writing Assistant: Perspectives from Professional Writers*. 2022. [arXiv:2211.05030](https://arxiv.org/abs/2211.05030)
- Mirowski, Mathewson, Pittman, Evans. *Co-Writing Screenplays and Theatre Scripts (Dramatron)*. CHI 2023. [arXiv:2209.14958](https://arxiv.org/abs/2209.14958). [DeepMind](https://deepmind.google/research/publications/13609/)
- Akoury et al. *STORIUM: Machine-in-the-Loop Story Generation*. EMNLP 2020. [ACL](https://aclanthology.org/2020.emnlp-main.525/)
- Chung et al. *TaleBrush: Sketching Stories with Generative Pretrained Language Models*. CHI 2022 EA. [project site](https://johnr0.github.io/publications/TaleBrush_CHI2022/)
- Fan, Lewis, Dauphin. *Hierarchical Neural Story Generation*. ACL 2018. [arXiv:1805.04833](https://arxiv.org/abs/1805.04833)
- Yang, Tian, Peng, Klein. *Re3: Generating Longer Stories with Recursive Reprompting and Revision*. EMNLP 2022. [arXiv:2210.06774](https://arxiv.org/abs/2210.06774)
- Yang, Klein, Peng, Tian. *DOC: Improving Long Story Coherence With Detailed Outline Control*. ACL 2023. [arXiv:2212.10077](https://arxiv.org/abs/2212.10077)
- Wang et al. *Weaver: Foundation Models for Creative Writing*. 2024. [arXiv:2401.17268](https://arxiv.org/abs/2401.17268)
- Bae, Kim. *Collective Critics for Creative Story Generation (CritiCS)*. EMNLP 2024. [arXiv:2410.02428](https://arxiv.org/abs/2410.02428)
- Chakrabarty, Laban, Agarwal, Muresan, Wu. *Art or Artifice? LLMs and the False Promise of Creativity* (TTCW). CHI 2024. [arXiv:2309.14556](https://arxiv.org/abs/2309.14556)
- Chakrabarty, Padmakumar, He, Peng. *Creativity Support in the Age of Large Language Models*. C&C 2024. [arXiv:2309.12570](https://arxiv.org/abs/2309.12570)
- Chang, Lo, Goyal, Iyyer. *BooookScore*. ICLR 2024 (oral). [arXiv:2310.00785](https://arxiv.org/abs/2310.00785)
- Kumar et al. *LongLaMP: Benchmark for Personalized Long-form Text Generation*. 2024. [arXiv:2407.11016](https://arxiv.org/abs/2407.11016). [project](https://longlamp-benchmark.github.io/)
- Pham, Sun, Iyyer. *Suri: Multi-constraint Instruction Following for Long-form Text Generation*. Findings of EMNLP 2024. [arXiv:2406.19371](https://arxiv.org/abs/2406.19371)
- Gómez-Rodríguez, Williams. *A Confederacy of Models: Comprehensive Evaluation of LLMs on Creative Writing*. Findings of EMNLP 2023. [ACL](https://aclanthology.org/2023.findings-emnlp.966/)
- *NoveltyBench: Evaluating Creativity and Diversity in Language Models*. 2025. [arXiv:2504.05228](https://arxiv.org/abs/2504.05228)
- Walsh et al. *Sonnet or Not, Bot? Poetry Evaluation for Large Models and Datasets*. Findings of EMNLP 2024. [ACL](https://aclanthology.org/2024.findings-emnlp.914)
- *Evaluating Diversity in Automatic Poetry Generation*. EMNLP 2024. [ACL](https://aclanthology.org/2024.emnlp-main.1097/)
- Chakrabarty, Zhang, Muresan, Peng. *MERMAID: Metaphor Generation with Symbolism and Discriminative Decoding*. NAACL 2021. [ACL](https://aclanthology.org/2021.naacl-main.336/)
- Reinhart, Markey, Laudenbach, Pantusen, Yurko, Weinberg, Brown. *Do LLMs Write Like Humans? Variation in Grammatical and Rhetorical Styles*. PNAS 122(8), 2025. [PNAS](https://www.pnas.org/doi/10.1073/pnas.2422455122)
- *Stylometric comparisons of human versus AI-generated creative writing*. Humanities and Social Sciences Communications (Nature) 2025. [link](https://www.nature.com/articles/s41599-025-05986-3)
- Doshi, Hauser. *Generative AI Enhances Individual Creativity but Reduces the Collective Diversity of Novel Content*. Science Advances 2024. [doi](https://www.science.org/doi/10.1126/sciadv.adn5290)
- Anderson et al. *We're Different, We're the Same: Creative Homogeneity Across LLMs*. 2025. [arXiv:2501.19361](https://arxiv.org/abs/2501.19361)
- Lee, Shen, Gero, Chung, Young et al. *A Design Space for Intelligent and Interactive Writing Assistants*. CHI 2024. [ACM](https://dl.acm.org/doi/10.1145/3613904.3642697) · [project](https://writing-assistant.github.io/)
- Thomas-Mitchell et al. *Where Do I 'Add the Egg'? Exploring Agency and Ownership in AI Creative Co-Writing Systems*. 2025. [arXiv:2509.15440](https://arxiv.org/abs/2509.15440)
- *Rethinking Creativity Evaluation: A Critical Analysis of Existing Creativity Evaluations*. EACL 2026. [ACL](https://aclanthology.org/2026.eacl-long.297/)
- EQ-Bench Creative Writing Benchmark v3 / Longform / Judgemark-v2 (Sam Paech). [eqbench.com](https://eqbench.com/creative_writing_v2.html)
