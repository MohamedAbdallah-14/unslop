# 08 · Conversational & Dialogue Systems — Angle A: Academic

**Project:** Humanizing AI output and thinking
**Category:** Conversational & Dialogue Systems
**Angle:** A — Academic & scholarly (arXiv, ACL, EMNLP, NeurIPS, ICLR, PNAS, Language, theses)
**Scope:** Foundational conversation-analysis theory → modern neural dialogue systems → full-duplex voice LLMs, with a humanization lens (naturalness, grounding, repair, turn-taking, backchanneling, discourse coherence, persona).

---

## Why this angle matters for "humanizing AI"

Dialogue is where AI output stops being a document and starts being *interaction*. The gap between "correct response" and "natural response" is almost entirely governed by mechanisms that classical LLM training ignores: how humans build common ground turn by turn, who speaks when, how they recover from misunderstandings, and how listeners signal engagement without taking the floor. The academic literature on this spans 50+ years — from Sacks/Schegloff/Jefferson's conversation analysis (CA) in the 1970s to 2024–2026 full-duplex speech LLMs like Moshi and GPT-4o Voice. Humanizing AI dialogue means porting CA's empirical findings into neural architectures, not just scaling turn-based chatbots.

---

## Papers (18)

Each entry: title, authors, venue/year, URL, core contribution, humanization relevance.

### Foundational theory (pre-neural)

1. **A Simplest Systematics for the Organization of Turn-Taking for Conversation**
   - Sacks, H., Schegloff, E., & Jefferson, G.
   - *Language*, 50(4), 696–735, **1974**.
   - https://doi.org/10.2307/412243
   - Founding paper of conversation analysis. Proposes turn-taking as locally managed, party-administered, interactionally controlled, and sensitive to recipient design; introduces transition-relevance places (TRPs) and the rules governing next-speaker selection. Still the most cited article in *Language*.
   - **Humanization relevance:** Any dialogue agent that assumes fixed turn boundaries (silence → "your turn") is already inhuman. Modern VAP/Moshi architectures are essentially empirical reimplementations of Sacks et al.'s rules.

2. **The Preference for Self-Correction in the Organization of Repair in Conversation**
   - Schegloff, E. A., Jefferson, G., & Sacks, H.
   - *Language*, 53(2), 361–382, **1977**.
   - https://www.jstor.org/stable/413107
   - Establishes the four-cell typology of repair (self-/other-initiated × self-/other-completed) and demonstrates a strong structural preference for self-initiated self-repair. Codifies the three-turn NTRI (next-turn-repair-initiation) sequence.
   - **Humanization relevance:** LLMs today mostly perform *other-completed* repair ("Let me correct that…") in response to explicit user challenges. Human-like dialogue requires self-initiated mid-turn repair, repair-initiating tokens ("huh?", "y'mean X?"), and graceful recovery without full restart.

3. **Grounding in Communication**
   - Clark, H. H., & Brennan, S. E.
   - In *Perspectives on Socially Shared Cognition* (Resnick, Levine, Teasley, eds.), APA, 1991.
   - https://web.stanford.edu/~clark/1990s/Clark,%20H.H.%20_%20Brennan,%20S.A.%20Grounding%20in%20communication.pdf
   - Formalizes common ground as *mutual knowledge + mutual belief + mutual assumption*, built via a presentation/acceptance phase. Distinguishes evidence of understanding (acknowledgements, relevant next turn, continued attention) and the *least collaborative effort* principle.
   - **Humanization relevance:** The single most important theoretical frame for why LLM chat "feels off" — LLMs skip the acceptance phase, over-claim understanding, and ignore the collaborative cost users pay to keep repairing.

4. **On Getting a Word in Edgewise**
   - Yngve, V.
   - Papers from the 6th Regional Meeting, Chicago Linguistic Society, 567–578, **1970**.
   - Coins the term "back channel" for short listener responses ("yes", "uh-huh") that acknowledge a speaker without claiming the turn. Also independently introduces "turn-taking" as a linguistic term.
   - **Humanization relevance:** Backchanneling is the dominant listener behavior in human dialogue and is completely absent from standard turn-based chat UX. A humanized voice agent must *produce* backchannels while the user speaks and *tolerate* them without interpreting them as turn grabs.

5. **Universals and Cultural Variation in Turn-Taking in Conversation**
   - Stivers, T., Enfield, N. J., Brown, P., Englert, C., Hayashi, M., Heritage, J., Levinson, S. C., et al.
   - *PNAS*, 106(26), 10587–10592, **2009**.
   - https://www.pnas.org/doi/10.1073/pnas.0903616106
   - 10-language corpus study showing gap-between-turns is universally ~200 ms, varying only ±250 ms across cultures. Establishes turn-taking as a human universal with ethological roots.
   - **Humanization relevance:** Sets the empirical latency target. GPT-4o Voice's 232–320 ms response is not a product decision — it's the only number that reads as human. Anything > ~700 ms reads as "thinking" or "robotic".

6. **When 'Others' Initiate Repair**
   - Schegloff, E. A.
   - *Applied Linguistics*, 21(2), 205–243, **2000**.
   - Extends the 1977 repair framework with a detailed taxonomy of other-initiation formats (open-class "huh?", restricted "who?", category-specific "y'mean X?", candidate understandings) and their differential deployment.
   - **Humanization relevance:** Gives a concrete inventory of repair-initiating moves a dialogue agent should recognize in input and produce in output when it detects an own-speech trouble source.

### Dataset and task frameworks (neural era)

7. **Wizard of Wikipedia: Knowledge-Powered Conversational Agents**
   - Dinan, E., Roller, S., Shuster, K., Fan, A., Auli, M., & Weston, J.
   - *ICLR*, **2019**. arXiv:1811.01241.
   - https://arxiv.org/abs/1811.01241
   - Large knowledge-grounded dialogue dataset where one speaker ("wizard") retrieves Wikipedia passages before speaking. Introduces retrieval-then-generate Transformer Memory Networks.
   - **Humanization relevance:** Operationalizes Clark-style factual grounding: a response isn't just fluent, it's *tied to evidence the listener can verify*. Precursor to RAG-style dialogue agents.

8. **Personalizing Dialogue Agents: I Have a Dog, Do You Have Pets Too?** (Persona-Chat)
   - Zhang, S., Dinan, E., Urbanek, J., Szlam, A., Kiela, D., & Weston, J.
   - *ACL*, **2018**. arXiv:1801.07243.
   - https://arxiv.org/abs/1801.07243
   - 162k-utterance crowd-collected dataset where each worker is given a 4–6 sentence persona. Directly targets the "no personality / generic 'I don't know'" failure mode of chit-chat models.
   - **Humanization relevance:** The canonical resource for injecting consistent identity into dialogue systems — a foundational building block for any "humanizer" that must maintain a stable voice across turns.

### Open-domain neural chatbots (2019–2022)

9. **DialoGPT: Large-Scale Generative Pre-training for Conversational Response Generation**
   - Zhang, Y., Sun, S., Galley, M., Chen, Y.-C., Brockett, C., Gao, X., Gao, J., Liu, J., & Dolan, B.
   - *ACL demo*, **2020**. arXiv:1911.00536.
   - https://arxiv.org/abs/1911.00536
   - GPT-2 architecture pretrained on 147M Reddit comment chains (2005–2017). 117M / 345M / 762M parameter sizes. First open model demonstrating near-human single-turn response quality.
   - **Humanization relevance:** Benchmarks the ceiling of pure *scale + conversational pretraining* — already fluent at token level, already generic at interaction level. Shows scale alone does not give grounding or repair.

10. **Towards a Human-like Open-Domain Chatbot** (Meena)
    - Adiwardana, D., Luong, M.-T., So, D. R., Hall, J., Fiedel, N., Thoppilan, R., Yang, Z., Kulshreshtha, A., Nemade, G., Lu, Y., & Le, Q. V.
    - Google Research, **2020**. arXiv:2001.09977.
    - https://arxiv.org/abs/2001.09977
    - 2.6B-parameter Evolved Transformer seq2seq trained on 341 GB of filtered social-media dialogue. Introduces **SSA (Sensibleness and Specificity Average)** as a human-like proxy metric; reports R² = 0.93 between perplexity and SSA.
    - **Humanization relevance:** SSA is still the most widely cited humanness proxy for open-domain dialogue. The perplexity↔SSA correlation is the core justification for "just keep training the LM."

11. **Recipes for Building an Open-Domain Chatbot** (BlenderBot 1)
    - Roller, S., Dinan, E., Goyal, N., Ju, D., Williamson, M., Liu, Y., Xu, J., Ott, M., Shuster, K., Smith, E. M., Boureau, Y.-L., & Weston, J.
    - *EACL*, **2021**. arXiv:2004.13637.
    - https://arxiv.org/abs/2004.13637
    - Argues scale is necessary but insufficient. Combines personality (Persona-Chat), empathy (ED), and knowledge (WoW) into *Blended Skill Talk* fine-tuning. 90M / 2.7B / 9.4B sizes. Human evals show preference over Meena on engagingness and humanness.
    - **Humanization relevance:** Explicit multi-skill recipe — the direct intellectual ancestor of modern "humanizer" prompt stacks that juggle persona, empathy, and factuality as separate dials.

12. **LaMDA: Language Models for Dialog Applications**
    - Thoppilan, R., De Freitas, D., Hall, J., Shazeer, N., Kulshreshtha, A., Cheng, H.-T., Jin, A., et al.
    - Google, **2022**. arXiv:2201.08239.
    - https://arxiv.org/abs/2201.08239
    - 137B-parameter dialog-specialized Transformer; 1.56T tokens of dialogue + web. Introduces a factuality pipeline with external tool calls (search, calculator, translator) and a safety classifier fine-tuned on crowd-labeled violations.
    - **Humanization relevance:** First large model to separate *quality* (SSI — sensibleness, specificity, interestingness) from *safety* and *groundedness* as orthogonal fine-tuning targets. The tri-axis evaluation frame is now standard.

13. **Improving Alignment of Dialogue Agents via Targeted Human Judgements** (Sparrow)
    - Glaese, A., McAleese, N., Trębacz, M., Aslanides, J., Firoiu, V., Ewalds, T., Rauh, M., et al.
    - DeepMind, **2022**. arXiv:2209.14375.
    - https://arxiv.org/abs/2209.14375
    - Decomposes "be helpful, correct, harmless" into ~23 natural-language rules, collects per-rule preference data, trains rule-specific reward models. Adds inline evidence citations with 78% plausibility.
    - **Humanization relevance:** Operationalizes fine-grained dialogue norms as separable reward dimensions — the academic version of "don't claim to be a person" rules in commercial system prompts.

### Turn-taking, backchanneling, incremental processing

14. **A General, Abstract Model of Incremental Dialogue Processing**
    - Schlangen, D., & Skantze, G.
    - *EACL*, **2009**; extended version in *Dialogue & Discourse*, 2(1), 83–111, 2011.
    - https://aclanthology.org/E09-1081/
    - Defines dialogue modules by network topology, information flow, incremental unit (IU) granularity, and processing (start-before-input-complete). Supports anything from non-incremental pipelines to fully asynchronous predictive systems.
    - **Humanization relevance:** The canonical reference for why *"wait for silence, then ASR, then LLM, then TTS"* pipelines can never be human-like — natural dialogue requires incremental commitment, revision, and anticipation at sub-utterance granularity.

15. **Towards a General, Continuous Model of Turn-Taking in Spoken Dialogue Using LSTM Recurrent Neural Networks**
    - Skantze, G.
    - *SIGDIAL*, **2017**.
    - https://aclanthology.org/W17-5527/
    - Replaces silence-threshold VAD with an LSTM that continuously predicts future voice activity, generalizing zero-shot to turn-shift prediction, backchannel-vs-utterance classification, and HRI turn control. Outperforms human observers on turn-shift prediction in pauses.
    - **Humanization relevance:** The architectural blueprint that later becomes Voice Activity Projection (VAP), and ultimately the full-duplex architectures of Moshi and dGSLM.

16. **Real-Time and Continuous Turn-Taking Prediction Using Voice Activity Projection** / **"Yeah, Un, Oh": Continuous Real-Time Backchannel Prediction with VAP Fine-Tuning**
    - Inoue, K., Jiang, B., Ekstedt, E., Kawahara, T., & Skantze, G.
    - arXiv:2401.04868 (**2024**) and arXiv:2410.15929 / NAACL 2025.
    - https://arxiv.org/abs/2401.04868 · https://arxiv.org/abs/2410.15929
    - VAP directly maps stereo dialogue audio to future voice activity probabilities via contrastive predictive coding + self-attention; fine-tuning variant predicts *type* of backchannel frame-by-frame on unbalanced real-world data.
    - **Humanization relevance:** State-of-the-art continuous turn/backchannel prediction suitable for shipping in voice agents. Operationalizes Yngve (1970) and Sacks et al. (1974) as a real-time neural module.

### Full-duplex spoken LLMs (2022–2026)

17. **Generative Spoken Dialogue Language Modeling** (dGSLM)
    - Nguyen, T. A., Kharitonov, E., Copet, J., Adi, Y., Hsu, W.-N., Elkahky, A., Tomasello, P., Algayres, R., Sagot, B., Mohamed, A., & Dupoux, E.
    - *TACL*, **2023**. arXiv:2203.16502.
    - https://arxiv.org/abs/2203.16502
    - First textless full-duplex spoken dialogue model. Trained on 2000 h of stereo Fisher telephone audio without transcripts; dual-tower Transformer with cross-attention produces parallel discrete-unit streams that reproduce natural turn-taking, overlaps, and laughter.
    - **Humanization relevance:** Demonstrates that paralinguistics (laughter, breaths, simultaneous-talk) are learnable without text — a direct challenge to text-centric humanization pipelines that strip exactly these signals.

18. **Moshi: A Speech-Text Foundation Model for Real-Time Dialogue**
    - Défossez, A., Mazaré, L., Orsini, M., Royer, A., Pérez, P., Jégou, H., Grave, E., & Kyutai team.
    - Kyutai tech report, **2024**. arXiv:2410.00037.
    - https://arxiv.org/abs/2410.00037
    - 7B Temporal Transformer + Depth Transformer over the Mimi neural audio codec (24 kHz at 1.1 kbps). Two parallel audio streams (user + system) remove explicit turn structure; *Inner Monologue* conditions audio generation on time-aligned text. 160 ms theoretical / 200 ms practical latency. Open-source.
    - **Humanization relevance:** The current reference architecture for human-like voice AI. The "two streams + inner monologue" design is the first neural system that is architecturally incapable of treating dialogue as turn-based — and therefore the first that can genuinely implement Sacks-style overlapping talk, interruptions, and continuous backchanneling.

### Evaluation and naturalness benchmarks

19. **USR: An Unsupervised and Reference-Free Evaluation Metric for Dialog Generation**
    - Mehri, S., & Eskenazi, M.
    - *ACL*, **2020**. arXiv:2005.00456.
    - https://arxiv.org/abs/2005.00456
    - Composite of interpretable sub-metrics (understandable, natural, maintains context, interesting, uses knowledge) trained unsupervised on MLM + retrieval objectives. Turn-level correlation 0.42 (Topical-Chat) / 0.48 (PersonaChat); system-level correlation 1.0.
    - **Humanization relevance:** Decomposes "naturalness" into operational sub-qualities that map cleanly onto humanization axes — the template most later dialogue-evaluation metrics follow.

20. **ACUTE-EVAL: Improved Dialogue Evaluation with Optimized Questions and Multi-Turn Comparisons**
    - Li, M., Weston, J., & Roller, S.
    - NeurIPS CAI workshop, **2019**. arXiv:1909.03087.
    - https://arxiv.org/abs/1909.03087
    - Side-by-side multi-turn pairwise human evaluation with empirically optimized question wording; robust across annotators, supports self-chat. ParlAI open source.
    - **Humanization relevance:** The standard protocol for claiming "more human-like than baseline." Self-chat variant is particularly useful because humanization work rarely has paired human conversations.

21. **LLMs Get Lost in Multi-Turn Conversation**
    - Laban, P., Hilleli, B., Kamoi, R., Wang, Y., Rosé, C. P., Shwartz, V., et al. (Microsoft Research + collaborators)
    - **2025**. arXiv:2505.06120.
    - https://www.microsoft.com/en-us/research/publication/llms-get-lost-in-multi-turn-conversation/
    - Across 200k+ simulated multi-turn conversations and 15+ frontier LLMs, reports a mean **39% performance drop** from single-turn to "sharded" multi-turn tasks. Decomposes the gap into small aptitude loss + large *unreliability* gain: models commit early, can't recover, and contaminate context with their own earlier wrong moves.
    - **Humanization relevance:** Strongest recent empirical evidence that coherent multi-turn dialogue is a distinct, under-solved capability — humanization work that stops at "make the tone warmer" is optimizing the wrong surface.

---

## Cross-cutting patterns and trends

### Convergence (high signal — multiple independent sources agree)

- **Classical CA predicts the frontier.** Moshi's two-stream architecture, VAP's continuous turn prediction, and dGSLM's overlap modeling are, respectively, neural implementations of Sacks et al. (1974), Yngve (1970), and the "simultaneous both-speakers" observation Yngve used to justify the backchannel term. Twenty-first-century speech AI is converging on a mid-twentieth-century descriptive model.
- **Latency is the non-negotiable humanness bit.** Stivers et al. (2009) put inter-turn gaps at ~200 ms universally. GPT-4o (232–320 ms), Moshi (160–200 ms), and the 2025 full-duplex systems all target this window. Text chat humanization ignores this; voice humanization cannot.
- **Scale → fluency, not grounding.** Meena, DialoGPT, and LaMDA all report that scaling improves token-level perplexity and SSA-style scores while leaving factual grounding, safety, and *coherent multi-turn intent* roughly untouched. LLMs-Get-Lost (2025) is the most recent restatement.
- **Humanness is decomposable.** From USR (2020) to LaMDA's SSI/Safety/Groundedness axes to Sparrow's 23 rules to DialogBench's 12 tasks, every successful evaluation reframes "natural" as a bundle of ~5–25 interpretable sub-qualities. Humanizer systems that optimize a single "human-like" score drift toward generic sycophancy.

### Trends (2022 → 2026)

- **Turn-based → full-duplex.** The center of gravity has moved from text chatbots (BlenderBot-era) to speech-to-speech models (Moshi, GPT-4o Voice, FLM-Audio, TurnGuide). Half-duplex "push to talk" is now a legacy pattern.
- **Text-only → paralinguistic.** dGSLM and Moshi demonstrate learning laughter, breaths, and interruption-recovery directly from audio. The "transcribe → LLM → TTS" pipeline is losing ground because it strips exactly the signals that make speech sound alive.
- **Coarse to fine repair.** Early neural systems had zero repair machinery. Recent work (VAP backchannel types, FLEXI benchmark, NC-Bench) is explicitly grounded in CA categories — open-class vs restricted repair, next-turn vs fourth-position.
- **Static benchmarks → simulated dialogue.** MT-Bench-101, LLMs-Get-Lost "sharded" conversations, and CoReflect all move toward *simulation-based* evaluation where a judge LLM plays a user across many turns. Static single-turn benchmarks are quietly being deprecated for dialogue claims.

### Gaps and unsolved problems

- **Self-initiated repair in text LLMs.** Vast literature on *other*-completed repair (user complains → model apologizes). Almost no work on the Schegloff 1977 preference: mid-turn self-correction without a user prompt. This is where "AI-sounding" text most obviously diverges from human writing.
- **Grounding beyond citation.** Wizard of Wikipedia / RAG-style citation is *evidential* grounding (Clark's mutual belief about facts). **Procedural** grounding — "do you want me to elaborate?" / "so to confirm, X?" — is largely missing from academic benchmarks and is the dominant source of LLM dialogue awkwardness in practice.
- **Backchanneling in text.** Entirely unaddressed. Chat UIs have no channel for listener signals; models cannot receive "uh-huh" mid-reasoning or emit "wait, let me think" mid-generation. This is an *interface* gap as much as a model gap and suggests an underexplored humanization axis.
- **Long-horizon persona maintenance.** Persona-Chat (4–6 sentences) and Character.ai-style cards both underspecify stable identity. No academic benchmark I found tests identity *stability under adversarial or emotional pressure over 100+ turns*, which is exactly where humanized agents break.
- **Cross-cultural turn-taking.** Stivers (2009) demonstrates ±250 ms variation is real. All major full-duplex systems optimize for a single (English-monolingual) latency profile. A Japanese-calibrated Moshi-equivalent (7 ms gaps, heavy overlap tolerance) does not exist in the literature.
- **Multi-turn reliability.** The 39% single→multi-turn performance drop in LLMs-Get-Lost is not being seriously attacked — most alignment and humanization work still optimizes single-turn SFT/RLHF signals.

### Cross-domain analogies worth porting

- **Music ensemble entrainment.** Jazz combos solve turn-taking, backchanneling, and overlap continuously without explicit turn structure. The entrainment literature (Keller, Repp) has mathematical models of mutual predictive adaptation that map cleanly onto VAP-style prediction — richer than silence-threshold borrowings.
- **Collaborative whiteboarding / mixed-initiative planning.** HCI's mixed-initiative tradition (Horvitz 1999) predates LaMDA's "helpful assistant" framing by two decades and has thought more carefully about when the system *shouldn't* speak — an underused source for humanization defaults.
- **Sign-language interaction.** Deaf conversation has different floor-management norms (gaze, space) but the same CA repair structure. Work on sign-language dialogue systems offers a useful control: which turn-taking phenomena survive the loss of acoustic signal?

---

## Sources (for verification)

- arXiv:1801.07243 — Zhang et al., Persona-Chat (2018)
- arXiv:1811.01241 — Dinan et al., Wizard of Wikipedia (2019)
- arXiv:1909.03087 — Li, Weston, Roller, ACUTE-Eval (2019)
- arXiv:1911.00536 — Zhang et al., DialoGPT (2019)
- arXiv:2001.09977 — Adiwardana et al., Meena (2020)
- arXiv:2004.13637 — Roller et al., BlenderBot 1 (2020)
- arXiv:2005.00456 — Mehri & Eskenazi, USR (2020)
- arXiv:2201.08239 — Thoppilan et al., LaMDA (2022)
- arXiv:2203.16502 — Nguyen et al., dGSLM (2022/2023 TACL)
- arXiv:2209.14375 — Glaese et al., Sparrow (2022)
- arXiv:2401.04868 — Inoue et al., VAP real-time turn-taking (2024)
- arXiv:2410.00037 — Défossez et al., Moshi (2024)
- arXiv:2410.15929 — Inoue et al., VAP backchannel fine-tuning (2024, NAACL 2025)
- arXiv:2505.06120 — Laban et al., LLMs Get Lost in Multi-Turn Conversation (2025)
- ACL Anthology E09-1081 — Schlangen & Skantze, Incremental Dialogue Processing (2009)
- ACL Anthology W17-5527 — Skantze, LSTM turn-taking (SIGDIAL 2017)
- *Language* 50(4), 1974 — Sacks, Schegloff & Jefferson, Turn-Taking
- *Language* 53(2), 1977 — Schegloff, Jefferson & Sacks, Repair
- *PNAS* 106(26), 2009 — Stivers et al., Turn-taking universals
- Clark & Brennan, 1991 — *Grounding in Communication* (APA book chapter)
- Yngve, 1970 — *On Getting a Word in Edgewise* (CLS proceedings)
- *Applied Linguistics* 21(2), 2000 — Schegloff, Other-initiated repair
