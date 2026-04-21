# Category 14 — Creative Writing and Storytelling

**Last updated: April 2026.** Major additions since prior version: StoryWriter (CIKM 2025), DOME (NAACL 2025), HAMLET (ICLR 2026), Rethinking Creativity Evaluation (EACL 2026), CHI 2025 cultural homogenization study, PNAS "Echoes in AI", diverse-personas mitigation (2026), lechmazur/writing V4 benchmark, NovelAI Xialong (GLM-4.6), Sao10K Euryale v2.3 (Llama 3.3), SillyTavern 1.15.0, Sudowrite Story Engine 3.0 / pricing update, Character.AI PipSqueak 2 / DeepSqueak 2 roadmap, EQ-Bench Creative Writing v3 standings, Kimi K2 cost profile.

## Scope

This category covers humanization research as it applies to fiction, long-form narrative, and character-driven creative writing. It spans five angles: academic research on co-writing interfaces, story-generation pipelines, and evaluation frameworks; industry essays and vendor blogs; open-source fiction frontends and community models; commercial voice-preservation products; and practitioner forums and Substack writing communities. Out of scope: SEO/marketing copy and academic prose (other categories). Adjacent to style transfer (06), persona/roleplay (15+), and detector-evasion as a commercial vertical (01–02).

---

## Executive Summary

- **LLMs are plausible sentence-local stylists but structurally weak on originality, long-range coherence, and surprise.** Chakrabarty et al.'s TTCW (CHI 2024) — the most cited scalable creativity evaluation — found LLM stories pass 3–10× fewer creativity tests than professional human stories, and no LLM-as-judge positively correlates with expert creativity judgments. This baseline has not been overturned. (A)
- **Instruction-tuning is the current humanness bottleneck, not scale.** Reinhart et al. (*PNAS* 2025) show instruction-tuned models use present-participial clauses 2–5× the human rate, nominalizations 1.5–2×, passive voice ~0.5×, and overuse *camaraderie, tapestry, palpable, intricate*. Differences are larger for instruction-tuned models than base models. (A) Robin Sloan, Nathan Lambert, and the *Claude5.com* 4.6 writing-controversy review independently report that RLHF/reasoning gains regress prose quality. (B)
- **At population scale the problem flips from "sound human" to "preserve inter-author diversity."** Doshi & Hauser (*Science Advances* 2024) found AI assistance lifts individual creativity 10–11% and readability 22–26% but clusters assisted stories significantly more than unassisted ones. Anderson et al. (2025) and NoveltyBench (2025) confirm homogenization is architectural, not a single-model quirk: SOTA models produce significantly less diversity than humans, and larger models are often less diverse than smaller ones. CHI 2025 adds a cultural dimension: AI suggestions actively push non-Western writers toward Western styles. PNAS 2025 ("Echoes in AI") extends this to plot structure — LLMs repeatedly reuse the same combinations of plot elements. The first empirical mitigation (diverse AI personas, 2026 ScienceDirect) shows persona rotation can restore diversity to human-baseline levels. (A)
- **The commercial and open-source worlds have converged on the same five-piece voice-preservation stack**: fiction-tuned base model + Story Bible/Codex/Lorebook (application-layer RAG) + voice calibration from user samples + creativity/temperature dial + persistent character memory. Sudowrite, NovelCrafter, AI Dungeon, Character.AI, NovelAI, DoppelWriter, KoboldAI, and SillyTavern all ship this architecture under different names. (B, C, D)
- **Long-form generation is a pipeline problem, not a model problem.** Dramatron → Re3 → DOC → CritiCS → autonovel → StoryDaemon → StoryWriter → DOME converge on plan → detailed outline → draft → multi-critic revision → edit pass. Re3 achieved +14pp plot coherence and +20pp premise relevance over flat baselines; DOC achieved +22.5pp plot coherence, +28.2pp outline relevance, and +20.7pp interestingness over Re3. 2025 additions: StoryWriter (CIKM 2025) adds event-relationship graphs and a 6,000-story open training set; DOME (NAACL 2025) introduces KG-based memory that lets the outline adapt to narrative uncertainty mid-generation. Raw sampling past ~4k tokens still collapses regardless of base model. (A, C)
- **Humanization has crossed from aesthetic opinion to a measurable objective.** Sam Paech's `slop-score` scores overused vocabulary (60%), "not X, but Y" constructions (25%), and slop trigrams (15%). EQ-Bench creative-writing-v3 explicitly penalizes "poetic incoherence." Gryphe's MythoMist 7B merged against slop vocabulary (*anticipation, ministrations, shivers*) as an optimization target. (C)
- **Practitioner consensus has moved from vocabulary to structure.** The most-cited 2026 r/WritingWithAI thesis is that "robotic writing" comes from uniform sentence lengths, smooth transitions, and paragraphs that resolve too cleanly — not from the word *delve*. The dominant voice-capture method in Q1 2026 Substack writing is interview-the-writer → save a `voice.md` (Hassid, Pajonas, Toncheva), explicitly replacing the failed "paste 5 samples" approach; core insight: taste is defined by what you reject. (E)
- **Fiction-specific fine-tuned models reliably out-voice frontier RLHF'd chat models.** Sudowrite Muse 1.5, Character.AI PipSqueak 2 (SFT + DPO + RL + QAT), NovelAI Kayra/Erato/Xialong, AI Dungeon Dragon, and the community Mytho/Midnight-Miqu/Sao10K catalog all explicitly market against safety-tuned general models on the premise that RLHF flattens stylistic range — a premise Reinhart et al. now supports empirically. (A, B, C, D)
- **Sampler choice moves voice more than model choice at the margin.** The text-generation-webui Preset Arena ground-truth shows the winning sampler recipe is **high min-p + moderate temperature + DRY** to suppress clichés, not high temperature alone. KoboldCpp's context-shifting is the cheapest known way to pin opening voice on long outputs. Midnight-Miqu ships sampler preset JSON alongside weights; weights alone underspecify voice. (C, E)

---

## Cross-Angle Themes

### Themes present in 3 or more angles

**Story-Bible-as-RAG is table stakes.** Sudowrite Story Bible, NovelCrafter Codex, Character.AI Lorebook, AI Dungeon World Info, NovelAI Lorebook, and KoboldAI's Memory/Author's Note/World Info triad all converge on a structured, user-maintained knowledge store containing typed entities (Character, Place, Object, Lore, Timeline) plus dialogue samples retrieved at generation time. This is the application-layer answer to context windows not being enough for novel-length voice consistency. (B, C, D, E)

**Fiction-tuned base models beat RLHF'd chat models for prose.** Academic stylometry (Reinhart, PNAS 2025), industry vendors (Sudowrite Muse, NovelAI, Character.AI PipSqueak 2), open-source community merges (MythoMist, Goliath, Sao10K Euryale), and practitioner forums (r/SillyTavernAI purple-prose threads) all converge on the same diagnosis: RLHF/safety-tuning flattens voice range; smaller, narrower fiction-tuned models beat general frontier models on prose quality. (A, B, C, D, E)

**Author's Note as the cheapest humanization primitive.** A persistent style directive injected N tokens before the latest output reduces voice drift on long outputs. Originating in AI Dungeon, this pattern was copied by KoboldAI, NovelAI, and now appears as "current-state prefix blocks" in Sudowrite and Claude fiction prompts described by Balthrop. (B, C, D, E)

**Long-form is a pipeline, not a prompt.** Plan → detailed outline → draft → critic-revision → edit pass is now the dominant architecture across Dramatron, Re3, DOC, CritiCS, autonovel, and StoryDaemon. The debate is about outline rigidity and critic composition, not the overall shape. (A, C, D)

**Voice calibration from user samples.** Sudowrite Style Examples (≤1,000 words), Replika positive-statement backstory, NovelCrafter character cards with dialogue samples, DoppelWriter sentence-length + vocab + punctuation signatures, and the interview-method `voice.md` all do the same thing: ingest 500–2,000 words of concrete reference prose/dialogue as an in-context few-shot anchor. (B, D, E)

**Homogenization is a first-class metric.** NoveltyBench, Anderson et al. "We're Different, We're the Same," and Doshi & Hauser all promote diversity-across-outputs from post-hoc observation to evaluation axis. For a humanization product this reframes the goal from "sound human" to "preserve inter-author diversity at scale." (A, B, E)

### Themes present in exactly two angles

**Sampler stacks are underused humanization levers.** The Preset Arena (C) and practitioner forums (E) converge on min-p + DRY + XTC + quadratic as superior to temperature-only — a lever that commercial tools rarely expose clearly.

**Per-character sub-voices as an open frontier.** DoppelWriter and StorySmith (D) and r/SillyTavernAI behavioral-clause character cards (E) both identify keeping distinct character voices across 80k+ words as harder than narrator humanization and structurally under-served.

**Interface framing matters as much as model or prompt.** Thomas-Mitchell's "Where Do I 'Add the Egg'?" academic study (A) and Plottr's opt-in sparkle-button UX and Scrivener's no-AI stance (D) show that how AI presence is framed shapes felt ownership and writer identity — not just usability.

**The "ghost/quiet/hum/echo/liminal" failure mode is now named.** Kriss/Read/Sloan essay cluster (B) and r/SillyTavernAI anti-slop system prompts (E) both catalog this vocabulary cluster explicitly, alongside the broader word-level ban-list tradition (Min Choi's ~30-word list in E).

---

## Top Sources

### Must-read papers

- Chakrabarty, Laban, Agarwal, Muresan, Wu — *Art or Artifice? LLMs and the False Promise of Creativity* (TTCW). CHI 2024. [arXiv:2309.14556](https://arxiv.org/abs/2309.14556). The most cited negative result; LLM stories pass 3–10× fewer creativity tests than professional stories; no LLM-as-judge positively correlates with experts.
- Doshi & Hauser — *Generative AI Enhances Individual Creativity but Reduces the Collective Diversity of Novel Content*. *Science Advances* 2024. [doi:10.1126/sciadv.adn5290](https://www.science.org/doi/10.1126/sciadv.adn5290). The population-scale reframe: +10–11% individual creativity, significant clustering.
- Reinhart, Brown, Markey et al. — *Do LLMs Write Like Humans? Variation in Grammatical and Rhetorical Styles*. *PNAS* 122(8), 2025. [link](https://www.pnas.org/doi/10.1073/pnas.2422455122). Biber-framework stylometry; instruction-tuning as bottleneck.
- Lee, Liang, Yang — *CoAuthor*. CHI 2022. [arXiv:2201.06796](https://arxiv.org/abs/2201.06796). 1,445 keystroke-level co-writing sessions; 72.3% suggestion acceptance; 72.6% human-written.
- Mirowski, Mathewson, Pittman, Evans — *Dramatron*. CHI 2023. [arXiv:2209.14958](https://arxiv.org/abs/2209.14958). Hierarchical log-line → dialogue, validated by 15 professionals; *Plays by Bots* staged publicly.
- Yang, Klein, Peng, Tian — *DOC: Improving Long Story Coherence With Detailed Outline Control*. ACL 2023. [arXiv:2212.10077](https://arxiv.org/abs/2212.10077). +22.5pp coherence, +28.2pp outline relevance over Re3.
- Anderson et al. — *We're Different, We're the Same: Creative Homogeneity Across LLMs*. 2025. [arXiv:2501.19361](https://arxiv.org/abs/2501.19361). Homogenization is architectural, not a single-model quirk.
- *NoveltyBench: Evaluating Creativity and Diversity in Language Models*. 2025. [arXiv:2504.05228](https://arxiv.org/abs/2504.05228). Larger models often less diverse than smaller; SOTA less diverse than humans.
- *AI Suggestions Homogenize Writing Toward Western Styles and Diminish Cultural Nuances*. CHI 2025. [arXiv:2409.11360](https://arxiv.org/abs/2409.11360). Extends homogenization to cultural register; non-Western writers pushed toward Western norms.
- *Echoes in AI: Quantifying Lack of Plot Diversity in LLM Outputs*. PNAS 2025. [doi:10.1073/pnas.2504966122](https://www.pnas.org/doi/10.1073/pnas.2504966122). Plot-level homogenization; Semantic Space Collapse framing; introduces automatic plot-diversity metric.
- *Rethinking Creativity Evaluation: A Critical Analysis of Existing Creativity Evaluations*. EACL 2026. [arXiv:2508.05470](https://arxiv.org/abs/2508.05470). No single existing creativity metric generalizes across domains. Directly invalidates single-metric evaluation gates for humanization pipelines.
- *StoryWriter: A Multi-Agent Framework for Long Story Generation*. CIKM 2025. [arXiv:2506.16445](https://arxiv.org/abs/2506.16445). Event-relationship graph outlines + dynamic history compression; LongStory dataset (6,000 stories, avg 8,000 words) released open.
- *DOME: Generating Long-form Story Using Dynamic Hierarchical Outlining with Memory-Enhancement*. NAACL 2025. [arXiv:2412.13575](https://arxiv.org/abs/2412.13575). KG memory makes outlines adaptive mid-generation; addresses the "rigid outline = mechanical prose" failure mode.

### Key essays and posts

- Max Read — *Will A.I. writing ever be good?* Dec 2025. [maxread.substack.com](https://maxread.substack.com/p/will-ai-writing-ever-be-good). Coins "F.O.B. voice"; synthesizes Kriss and Lambert.
- Sam Kriss — *What Does A.I. Actually Sound Like?* NYT Magazine, Dec 3 2025. Catalogs the ghost/quiet/hum/echo/liminal tic (7 instances in GPT-5's 1,100-word demo story).
- Robin Sloan — *Secondhand embarrassment*. Oct 12 2025. [robinsloan.com](https://robinsloan.com/lab/secondhand-embarrassment/). Best single essay on writing-regression-with-reasoning-gains.
- Ruben Hassid — *I am just a text file*. [ruben.substack.com](https://ruben.substack.com/p/i-am-just-a-text-file). Viral origin of the `voice.md` pattern; "taste is defined by what you reject."
- Nick Quick / Daniel Nest — *AI Writing Without the Slop*. Apr 2026. [cozora.substack.com](https://cozora.substack.com/p/ai-writing-without-the-slop). Introduces the VAST framework: Vocabulary / Architecture / Stance / Tempo.
- Inworld — *Beyond Quality: Emotionality and Expressiveness*. Mar 2026. [inworld.ai](https://inworld.ai/blog/beyond-quality-emotionality-and-expressiveness). Proprietary arousal and expressivity metrics used as RL reward signals — the most precise industry operationalization of voice humanness.
- Steph Pajonas — *The Interview Is the Secret*. Mar 2026. [spajonas.substack.com](https://spajonas.substack.com/p/the-interview-is-the-secret-how-i). Four-step interview voice-capture; personal AI-ism blocklist including `"It's not X. It's Y."`.
- RP|Fiend — *How To Write a SillyTavern Character Card That Actually Has Soul*. [rpfiend.com](https://rpfiend.com/how-to-write-a-sillytavern-character-card/). Canonical behavioral-clause over adjective-dump guide; the actor test.

### Key open-source projects

- [sam-paech/slop-score](https://github.com/sam-paech/slop-score) — scalar "how LLM does this sound" metric; 60% slop words + 25% "not X, but Y" + 15% slop trigrams. The most on-thesis tool in the category.
- [EQ-Bench creative-writing-bench](https://github.com/EQ-bench/creative-writing-bench) + [longform-writing-bench](https://github.com/EQ-bench/longform-writing-bench) + [Judgemark-v2](https://github.com/EQ-bench/Judgemark-v2) (Sam Paech) — de-facto open creative-writing leaderboard with explicit bias mitigation for length, position, verbosity, and poetic incoherence.
- [KoboldAI (henk717/united)](https://github.com/henk717/KoboldAI) (~3,880 stars) + [KoboldCpp](https://github.com/LostRuins/koboldcpp) (~9,900 stars) — the founding fiction frontend; Memory/Author's Note/World Info triad; context-shifting for long outputs.
- [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui) (~46,400 stars) — Preset Arena ground-truth data on human-preferred sampler stacks; winning recipe: high min-p + moderate temperature + DRY. SillyTavern 1.15.0 (Dec 28 2025) is now the dominant creative-writing frontend for power users; oobabooga remains the sampler-research reference.
- [google-deepmind/dramatron](https://github.com/google-deepmind/dramatron) (~1,075 stars), [yangkevin2/doc-story-generation](https://github.com/yangkevin2/doc-story-generation) (~162 stars), [NousResearch/autonovel](https://github.com/NousResearch/autonovel), [EdwardAThomson/StoryDaemon](https://github.com/EdwardAThomson/StoryDaemon), [StoryWriter (CIKM 2025)](https://arxiv.org/abs/2506.16445), [DOME (NAACL 2025)](https://aclanthology.org/2025.naacl-long.63.pdf) — the long-form pipeline reference implementations, in historical order.
- [CoAuthor interface](https://github.com/minalee-research/coauthor-interface) + [dataset](https://coauthor.stanford.edu/) — the only public dataset capturing keystroke-level human edits of AI suggestions.
- [GPT-WritingPrompts](https://github.com/KristinHuangg/gpt-writing-prompts) — parallel human and LLM-generated stories on matched prompts; ready-made training/eval set for humanization classifiers.
- [Gryphe/MythoMist-7b](https://huggingface.co/Gryphe/MythoMist-7b) — existence proof that anti-slop vocabulary suppression is optimizable at merge time. [Sao10K/L3.3-70B-Euryale-v2.3](https://huggingface.co/Sao10K/L3.3-70B-Euryale-v2.3) — the current open frontier for Llama-family creative writing (Dec 2024, 131K context, no LoRA). Qwen3-235B-A22B and DeepSeek-V3 are now cited as top performers in 2026 aggregated writing benchmarks, competing with the Llama-family dominance.
- [lechmazur/writing](https://github.com/lechmazur/writing) — V4 (Nov 2025) pairwise Thurstone evaluation across 29+ models; companion [lechmazur/writing_styles](https://github.com/lechmazur/writing_styles) documents per-model stylistic fingerprints. The best open creative-writing evaluation with contamination-resistant constrained prompts.
- [yingpengma/Awesome-Story-Generation](https://github.com/yingpengma/Awesome-Story-Generation) — the most actively maintained index of LLM story generation papers (2025–2026); supersedes Picrew/awesome-llm-story-generation.

### Notable commercial tools

- [Sudowrite](https://www.sudowrite.com/) (Hobby $10/mo annual, Professional $22/mo, Max $44/mo) — proprietary Muse 1.5 (2× preferred over Claude 3.7 Sonnet in blind tests); Story Engine 3.0 (2026 flagship: full-novel generation from Braindump + Genre + Style); Canvas 2.0; Style Examples; Story Bible; Creativity Dial 1–11; also offers Gemini 3.1 Pro, Claude Sonnet 4.6, GPT 5.4. Vendor claim: 40% fewer revision passes vs general AI. Endorsed by Hugh Howey and the NYT.
- [NovelCrafter](https://novelcrafter.com/) (from $4/mo + BYOK) — Codex as auto-linking worldbuilding RAG; 300+ models including local Ollama/LM Studio; "smart highlighting" flags AI-generated patterns. Own testing: GPT-5 "excels at style mimicry and dialogue but tends to veer off-plot."
- [DoppelWriter](https://doppelwriter.com/) (free → $15/mo) — voice cloning from samples; 140+ iconic-author profiles; per-character voice profiles tracking sentence length, vocab, punctuation, tone across 80k+ words. The most aligned commercial product with the humanization thesis.
- [AutoCrit](https://autocrit.com/) ($30/mo Pro) — 20+ editor reports; 100+ bestselling-author comparisons (Stephen King, Danielle Steel, Lee Child). Editing-not-generation; implicit humanness benchmark.
- [NovelAI (Anlatan)](https://novelai.net/) ($10/$15/$25/mo) — fiction-fine-tuned Kayra/Clio/Erato; **Xialong** (GLM-4.6 base, Opus tier, 2026) — RL-trained for repetition avoidance, eliminates repeat-penalty presets. First major commercial fiction LLM outside the Llama family.
- [Character.AI](https://character.ai/) — PipSqueak 2 (April 2026): less drift, more expressive dialogue, expanded memory categories (hairstyle, eye color, quirks). DeepSqueak 2 in training as of April 2026 (Spring 2026 target). Free users now access PSQ2.
- [Scrivener](https://literatureandlatte.com/) (~$60 one-time) — no native AI; explicit "your text is not sent to external servers." Cleanest target persona for an on-device humanizer.
- [Laika (shut down 2024–2025)](https://www.writewithlaika.com/) — cautionary data point: pure-play voice-cloning fiction tool with strong reviews killed by API price compression and horizontal competition. Humanization-as-feature may beat humanization-as-product.
- **Kimi K2** (Moonshot AI, 2026) — EQ-Bench Creative Writing score ~1700 at $0.60/$2.50 per 1M tokens (input/output). ~87% of Claude Sonnet 4.6 quality at ~5× lower cost. Emerging as the cost-competitive creative-writing choice for budget-conscious tools.

### Notable community threads

- r/WritingWithAI — [*"I realized most 'robotic' writing isn't about vocabulary"*](https://www.reddit.com/r/WritingWithAI/comments/1r9r6gk/) — the most-cited 2026 structural reframing; cites ~8.2 vs ~4.1 sentence-length stdev gap between humans and GPT-4o.
- r/SillyTavernAI — [anti-slop system prompt thread](https://www.reddit.com/r/SillyTavernAI/comments/1rbbsfk/) — widely forked; bans purple prose, archaic phrasing, excessive metaphors; enforces subtext dialogue and per-character vocab.
- Hacker News — [*"Ask HN: How would you describe the way AI writes versus a human?"*](https://news.ycombinator.com/item?id=43523658) — clean enumeration of AI-voice tells: upbeat/cheery, unusually consistent metaphors, overly flowery, hides incompetence with fluency.
- Hacker News — [*"When GPT-4.5 came out, I used it to write novels for my son"*](https://news.ycombinator.com/item?id=47304600) — honest ceiling data: "better than the median novel aimed at my son's age group… not good enough that he would recommend them or re-read them."

---

## Key Techniques & Patterns

1. **Hierarchical decomposition.** Treat "write a story" as plan → detailed outline → draft → multi-critic revision → edit pass (Dramatron, Re3, DOC, CritiCS, autonovel). Now the default long-form architecture; raw sampling past ~4k tokens collapses regardless of base model.

2. **Story-Bible-as-RAG.** Typed entities (Character / Place / Object / Lore / Timeline) plus dialogue samples and voice notes, retrieved at generation time. Ships as Story Bible (Sudowrite), Codex (NovelCrafter), Lorebook (Character.AI, NovelAI, AI Dungeon), World Info (KoboldAI).

3. **Author's Note / persistent style directive.** Inject a style anchor N tokens before the latest output. The cheapest known way to reduce voice drift; originating in AI Dungeon, now standard across every fiction tool.

4. **Interview-the-writer voice capture.** 30–50 min Q&A session → `voice.md` file → reusable across tools. Replaces the failed "paste 5 samples" approach. Core insight: taste is defined by what you reject, not what you like (Hassid, Pajonas, Toncheva).

5. **VAST framework.** Vocabulary / Architecture / Stance / Tempo — four voice axes encoded in a system prompt before drafting (Nick Quick / Cozora, Apr 2026).

6. **Behavioral-clause character cards.** Replace adjective dumps ("cold, reserved, fierce") with behavior-plus-cause: "She doesn't flinch. Not at threats, not at raised voices..." Actor test: "If an actor received this card as their only direction, could they perform it consistently?" (RP|Fiend, r/SillyTavernAI).

7. **Per-character sub-voices.** Track per-character speech patterns, vocab ranges, emotional registers, and dialogue samples so narrator and villain don't converge. DoppelWriter, StorySmith, NovelCrafter Character Progressions, Sudowrite Characters.

8. **TTCW-style binary rubrics.** 14 yes/no criteria across Fluency, Flexibility, Originality, Elaboration with expert raters. The most reused creativity evaluation protocol since CHI 2024.

9. **LLM-as-judge with bias mitigation.** EQ-Bench Glicko-2 pairwise Elo + rubric scoring with explicit controls for length bias, position bias, verbosity, and poetic incoherence. Judgemark-v2 evaluates the judges; Prometheus 2 is the open-weights default.

10. **Slop-score as a training/gating signal.** Curated slop-word list (60%) + "not X, but Y" detection (25%) + slop trigrams (15%). Directly turnable into a reward, a CI gate, or a decoder-time penalty.

11. **Merge-time anti-slop optimization.** MythoMist merges 12 constituent models layer-by-layer with inline benchmarking, explicitly targeting suppression of GPT vocabulary (*anticipation, ministrations, shivers*). Anti-slop is optimizable at merge time, not only at sampler time.

12. **Sampler-level humanization.** min-p + DRY (Don't Repeat Yourself) + XTC (eXclude Top Choices) + quadratic/smoothing, with moderate temperature. Consistently beats high-temp defaults on human preference (Preset Arena winners: Midnight Enigma, Yara, Shortwave).

13. **Context-shifting for long outputs.** KoboldCpp pins the opening prompt/style anchor while evicting old turns; the inference-layer answer to "the story forgot its opening voice."

14. **Structure-first humanization.** Sentence-length variance (mix sub-10-word and 20+-word sentences), em-dash / semicolon stitching, scenes ending on unresolved beats, subtext dialogue, paragraph-rhythm irregularity. This layer moves humanness more than word-ban lists at current tooling skill levels.

15. **Current-state prefix block.** "Here's what has already happened / where we are / whose POV" prefix before each chapter — fixes Claude's default of treating all narrative info as equally current (Balthrop).

16. **Bundle releases.** Ship weights + sampler preset + prompt template as a single unit. Midnight-Miqu, MythoMax, Sao10K Euryale all use this pattern. Weights alone underspecify voice.

17. **Write-rewrite-then-AI-polish.** Human draft → human rewrite → AI polish. Inverts the typical AI-first order; produces a visibly different voice profile (Martinez, Pajonas).

18. **Regex post-processors.** SillyTavern PR #3581 strips recurring AI phrases after generation; pairs with system-prompt bans as belt-and-braces.

19. **Multiverse UI.** Generate N variants with reasoned diffs rather than a single-output replace; aligned with Sudowrite's multiple-rewrites feature and Webb's "LLMs as multiverse generators" framing.

20. **Memory-reinforcement mid-session.** Periodically reinject a 2-sentence voice anchor to counter drift in long drafts or long roleplay sessions (r/CharacterAI, SillyTavern community practice).

---

## Controversies & Debates

**AI-draft-then-edit vs human-draft-then-AI-polish.** Substack purists (Martinez, Pajonas step 4, Sloan) insist the human must produce the first sentences; Sudowrite / NovelCrafter / Nerdy Novelist camp is comfortable with AI-first as long as the voice system is right. Neither camp has conceded; both have credible evidence. (B, E)

**Ban-lists summon what they forbid.** The dominant humanize-prompt bans ~30 specific words (Min Choi) and fiction-specific phrases (`A beat.`, `A pause.`, "It's not X — it's Y"). A minority view on HN and r/SillyTavernAI holds that naming the phrases makes the model start producing them. No controlled test has resolved this. (C, E)

**Outline-first (Dramatron, DOC) vs emergent structure (StoryDaemon).** Detailed-outline systems achieve measurable coherence gains; StoryDaemon argues no-outline produces more human prose at the cost of plot consistency. Both have human-preference evidence. (A, C)

**Serve-the-reader vs bypass-detection.** r/WritingWithAI, Joanna Penn, Robin Sloan, and Creativindie explicitly reject the bypass framing; detector-dodging tools (Humanize AI Pro, Undetectable AI) treat it as pure statistics. Most practitioners borrow from both without reconciling. (D, E)

**"LLM voice" is bad vs "LLM voice" is competent public communication.** HN minority position and Lambert's economic framing: the recognizable LLM signature resembles effective magazine writing, and pushing writers to avoid it may produce deliberately worse prose. (B, E)

**Detection vs literary quality are conflated.** Stylometric work shows 93–98% machine-classifier accuracy on human-vs-AI creative writing, while human readers perform near chance. That is a statistical-tell question, not a literary-quality question — but humanization literature routinely slides between the two. (A, E)

**Reasoning gains regress prose quality.** Sloan's anecdotal claim, the Claude5.com 4.6 writing-controversy review, and Reinhart et al. all point at this; no lab has published a controlled ablation. A high-leverage small research contribution waiting to be made. (A, B)

**Individual vs collective creativity.** Doshi & Hauser recast AI humanization as a social dilemma: individually rational AI use produces collectively homogenized literature. A product that helps one user may damage the broader literary ecosystem. (A, B)

---

## Emerging Trends

- **Instruction-tuning as the named bottleneck.** Reinhart (2025), stylometry work, and homogenization studies have moved the conversation from "LLMs can't write" to "post-training is the culprit." Humanization research is shifting from prompts toward post-training recipes.
- **Writing-specialist base models expanding beyond Llama.** Weaver (2024), Sudowrite Muse 1.5, Character.AI PipSqueak 2 (DeepSqueak 2 in training), Inworld TTS 1.5, **NovelAI Xialong (GLM-4.6 base, 2026)**. The shift to GLM-4.6 signals that fiction-specialist models are no longer constrained to the Llama family.
- **Structure overtaking vocabulary (2023 → 2026).** Burstiness, scene-break deferral, subtext dialogue, metaphor families, and tempo have overtaken word-level ban lists as the primary humanization lever in practitioner communities. PNAS 2025 "Echoes in AI" provides academic confirmation: LLM homogenization operates at the plot-structure level, not primarily the lexical level.
- **Interview-method as the dominant voice-capture pattern.** Hassid, Pajonas, and Toncheva converge independently on interview → `voice.md` as the 2026 replacement for sample-paste.
- **Homogenization expanding beyond vocabulary to culture and plot structure.** NoveltyBench, Anderson 2025, Doshi & Hauser at the vocabulary/semantic level; CHI 2025 at the cultural level (Western-style bias); PNAS 2025 at the plot structure level. First empirical mitigation: diverse AI personas (2026 ScienceDirect).
- **Writing-specific benchmarks fragmenting and questioning themselves.** EQ-Bench creative-writing-v3 (Claude Sonnet 4.6 #1, Elo 1936 as of March 2026), longform-writing-bench, Judgemark-v2, WritingBench, LongGenBench, BiGGen, lechmazur/writing V4 (Thurstone pairwise, 29+ models, Nov 2025). EACL 2026 "Rethinking Creativity Evaluation" warns that no single metric generalizes across domains.
- **Slop-vocabulary suppression migrating from prompt to weights.** MythoMist (2023) as curiosity → now standard at merge and fine-tune time. An adversarial arms race between slop detectors and slop-avoiders is beginning.
- **Small judges beating GPT-4-as-judge on prose rubrics.** WritingBench's 7B critic, Prometheus 2, and CharacterRM all hit human-level agreement on narrow prose rubrics at lower cost.
- **Community LLM ecosystem fragmenting beyond Llama.** Mytho family (Llama 2) legacy; Miqu-based drift-limited; Sao10K L3.3-70B-Euryale-v2.3 (Dec 2024) is the Llama-family frontier. Qwen3-235B-A22B and DeepSeek-V3 now cited as top performers in 2026 aggregated writing leaderboards. Fiction-model space is no longer Llama-only.
- **Character-voice distinctiveness as the next product frontier.** DoppelWriter, StorySmith, and Cordecho are competing on multi-voice fidelity across 80k+ words — a harder problem than narrator humanization and still structurally open.
- **Platform sorting of writing communities accelerating.** Pro-AI craft (r/WritingWithAI, r/SillyTavernAI) vs AI-banned (r/WritingPrompts). Cornell Chronicle (Oct 2025) identified AI as a "triple threat" to moderators; r/NoSleep reached 41% AI content by 2024.
- **On-device humanization growing.** Scrivener holdouts, LivingWriter privacy framing, NovelCrafter local-model BYOK. SillyTavern 1.15.0 + KoboldCpp/Ollama + Euryale-70B or Qwen3 is now the standard local stack.
- **Cost-competitive open models entering the creative-writing conversation.** Kimi K2 (~87% of Claude Sonnet 4.6 at 5× lower cost on EQ-Bench). GPT-5 ranked outside the top 8 for creative writing in 2026 aggregated leaderboards despite being a flagship model.

---

## Open Questions & Research Gaps

- **No consensus humanness metric.** TTCW (creativity), BooookScore (coherence), NoveltyBench (diversity), stylometry (distinguishability), CAT (expert preference), slop-score (slop vocabulary), and lechmazur/writing V4 (constrained element incorporation, pairwise) each measure a different proxy. EACL 2026 "Rethinking Creativity Evaluation" confirmed that no single existing metric generalizes across creative domains. No unified scalar or vector reliably captures "sounds human, reads as authored."
- **No public benchmark for long-form voice consistency.** Character.AI cites internal EQ benchmarks; Sudowrite cites a proprietary 40% revision-pass figure; Novarrium uses a 25-chapter stress test. None is public or reproducible. EQ-Bench longform gets close but is multi-chapter, not novel-length.
- **Voice preservation across revisions is under-served.** Tools preserve voice in generation but not across edit passes — user edits + AI rewrites + editor suggestions erode voice over 3–5 drafts. No "voice-diff" or voice-regression-test feature exists in any tool.
- **Collective homogenization mitigation is beginning but thin.** Doshi & Hauser widely cited; diverse AI personas (2026 ScienceDirect) is the first empirically tested intervention. Sampler-level diversity promotion, culturally-diverse fine-tuning, and persona rotation schedules remain minimally tested.
- **Cultural homogenization is an underexplored humanization dimension.** CHI 2025 established that AI suggestions push non-Western writers toward Western styles. Humanization research has not addressed *which* human's norms are the reference for "sounds human."
- **Evaluation-leakage risk.** Most creative benchmarks reuse public web-sourced reference stories. Newer LLMs likely saw them in pre-training, inflating scores. The lechmazur/writing constrained-element design partially mitigates this.
- **Multilingual creative writing is drastically under-represented.** CoAuthor, TTCW, BooookScore, LongLaMP, and EQ-Bench are all English-only. Almost all forum advice is English-first. Non-English literary naturalness is largely unstudied.
- **No open dataset of revisions at scale.** CoAuthor's 1,445 sessions is the gold standard; nothing at millions-of-sessions scale exists publicly. StoryWriter released a 6,000-story open training set (LongStory), but it is generated-story, not revision-session data.
- **Affect and emotional-trajectory evaluation is subjective.** EQ-Bench rubrics request "emotional engagement" with no principled arc-level metric; no public benchmark captures "does this story *feel* real" independent of a proprietary judge.
- **Sampler/preset discovery is manual.** The Preset Arena is blind-voting at human scale; no public automated search against creative-writing benchmarks exists.
- **No open end-to-end system combines the best pieces.** The stack Euryale-70B + slop-score inner-loop reward + DOME outline controller + EQ-Bench rubric gate + voice.md interview does not exist as a single repo.
- **Human-AI revision interfaces are stagnant.** CoAuthor's tab-to-suggest is still the reference UI from CHI 2022; SillyTavern 1.15.0 added Macros 2.0 but nothing has materially improved the underlying feedback model.
- **Reader-side perception is unstudied.** Near-zero forum or academic discussion of what actually makes a reader identify AI fiction, as opposed to what detectors flag or what writers self-flag.
- **Character-voice distinctiveness across a full novel.** Keeping two characters' voices genuinely distinct over 80k+ words is open; only DoppelWriter, StorySmith, and Cordecho are attempting it commercially.
- **Professional-writer evaluations are sparse.** Ippolito et al. used 13 writers; Chakrabarty used 10 raters and 30 emerging writers. Replication power is limited and results may not generalize to amateur use, where most LLM-assisted writing actually happens.
- **Early vs late AI use in ideation is underspecified.** CHI 2025 found AI introduced early in the creative process is most harmful to diversity, but no study has mapped optimal AI-intervention timing across the full plan → outline → draft → revise pipeline.

---

## How This Category Fits

Creative writing is where the humanization project meets its hardest technical constraint and its clearest market proof. Other categories ask "does this sound reasonable?" or "does this pass a detector?" Creative writing asks "does this sound like *this specific author*, consistently, across 80,000 words, with multiple distinct character voices, on a timeline I control?" That bar raises the engineering requirements from prompt trick to pipeline + specialized model + retrieval + sampler + evaluator.

Three specific connections to the broader project. First, creative writing is the canary for voice preservation: if a technique (style-example fine-tuning, voice DNA interview, per-character sub-voice) works on fiction — where voice is visible at every sentence — it transfers to every vertical where voice matters: B2B brand voice, personal email style, ghostwriting, political speechwriting. The Sudowrite/DoppelWriter pattern is structurally identical to Jasper's brand-voice-cloning pattern. Second, creative writing is the canary for homogenization: Doshi & Hauser's finding that AI lifts individual creativity but clusters assisted output transfers directly to every text-generation category. Any humanization strategy that ignores diversity preservation is buying individual quality at collective cost. Third, creative writing is where RLHF's fingerprints are loudest: the F.O.B. voice, the ghost/quiet/hum/echo tic, the not-X-but-Y construction. Fixes discovered here generalize to easier verticals.

The category also establishes the commercial viability of humanization as a product feature. Sudowrite, NovelAI, NovelCrafter, AI Dungeon, Character.AI, DoppelWriter, and Inworld all charge voice-preservation premiums; the Laika shutdown shows pure-play humanization products are fragile but humanization as a feature inside a larger writing environment is robust. The practitioner community (r/WritingWithAI, Substack voice essayists, The Nerdy Novelist, Joanna Penn) is pre-educated on the problem and willing to pay.

Where this category does not map cleanly to the wider project: the anti-detector framing. The pro-writer wing — r/WritingWithAI, Joanna Penn, Creativindie, Robin Sloan — is openly hostile to "bypass detection" positioning and prefers "serve the reader / preserve the voice." A humanization strategy leading with detector-dodging will alienate this audience; one leading with voice fidelity and structural quality will not.

Sibling categories this intersects: persona/roleplay (character-card craft, per-character voice distinctiveness), style transfer (06), long-form coherence and memory as a general problem, and the detector-evasion commercial vertical (01–02).

---

## Recommended Reading Order

1. **Start with the diagnosis.** Max Read, *Will A.I. writing ever be good?* (F.O.B. voice, Dec 2025) → Sam Kriss, *What Does A.I. Actually Sound Like?* (NYT Magazine, Dec 3 2025) → Robin Sloan, *Secondhand embarrassment* (Oct 12 2025). ~60 minutes. You now know what the problem sounds like.

2. **Ground the diagnosis in stylometry.** Reinhart et al. (*PNAS* 2025, *Do LLMs Write Like Humans?*) + the *Humanities and Social Sciences Communications* stylometric comparisons paper (Nature 2025). Instruction-tuning as the named bottleneck; 93–98% classifier accuracy as the detection ceiling.

3. **Read the creativity baseline.** Chakrabarty et al. (TTCW, CHI 2024). 3–10× gap on creativity tests; no LLM-as-judge positively correlates with experts. Every humanization claim must address this starting point.

4. **Read the long-form pipeline arc.** Fan (ACL 2018) → Dramatron (CHI 2023) → Re3 (EMNLP 2022) → DOC (ACL 2023) → CritiCS (EMNLP 2024). The architectural consensus in one sitting.

5. **Read the homogenization line.** Doshi & Hauser (*Science Advances* 2024) → NoveltyBench (2025) → Anderson et al. *We're Different, We're the Same* (2025). The population-scale reframe.

6. **Open the practitioner playbook.** r/WritingWithAI *"robotic writing isn't vocabulary"* thread → Ruben Hassid *I am just a text file* → Steph Pajonas *The Interview Is the Secret* → Nick Quick *AI Writing Without the Slop* (VAST) → Kelly Balthrop *Writing Fiction with Claude* → RP|Fiend character-card guide. ~3–4 hours. You now know how working writers actually operate.

7. **Scan the commercial stack.** Sudowrite Story Engine 3.0 changelog → NovelCrafter blog (GPT-5 evaluation, Codex) → Character.AI PipSqueak 2 / DeepSqueak 2 April 2026 post → Inworld *Beyond Quality: Emotionality and Expressiveness* → DoppelWriter fiction page → NovelAI Xialong announcement. ~90 minutes. You now know the product vocabulary the paying audience uses and which models matter in 2026.

8. **Run the open-source evaluators.** Install KoboldCpp + SillyTavern 1.15.0; run `slop-score` on your own outputs; skim [yingpengma/Awesome-Story-Generation](https://github.com/yingpengma/Awesome-Story-Generation); run EQ-Bench creative-writing-v3 against one model; check lechmazur/writing for the pairwise creative element benchmark. A weekend. You now have both the tools and a baseline score.

Optional depth: Lee et al.'s CHI 2024 *Design Space for Intelligent and Interactive Writing Assistants* (115-paper review) for the full HCI landscape. Vauhini Vara's *Ghosts* (The Believer 2021) and *Searches* (2024) for the literary and ethical process-over-product frame. BooookScore, LongLaMP, Suri, and BiGGen Bench for the full benchmark ecology.
