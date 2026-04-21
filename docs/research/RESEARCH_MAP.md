# Research Corpus — Cross-Reference Map

*Cross-reference tables for 20 per-folder SYNTHESIS.md files. April 2026.*

---

## Categories at a Glance

| # | Category | Primary lens | Key stat |
|---|----------|-------------|----------|
| 01 | Prompt Engineering & Humanization | Techniques | DIPPER drops DetectGPT 70.3% → 4.6%; antislop ~90% slop reduction |
| 02 | RLHF and Alignment | Root causes | Singhal et al.: length explains most RLHF gains; LIMA 1,000 examples ≈ GPT-4 in 43% of comparisons |
| 03 | Persona and Character Design | Voice stability | Drift within ~8 turns; CoSER-70B 75.80% InCharacter; Character.AI 20M users $9.99/mo |
| 04 | Natural Language Quality | Generation quality | Human sentence-length stdev ~8.2 vs GPT-4o ~4.1; min-p (ICLR 2025 Oral) |
| 05 | AI Text Detection and Evasion | Arms race | StealthRL 97.6% ASR; mean AUROC 0.79 → 0.43; Liang et al. >50% TOEFL misclassified |
| 06 | Chain-of-Thought Reasoning | Reasoning traces | DeepSeek-R1-Zero AIME 71.0%; PaLM-540B 58.1% GSM8K; CoT + reasoning-trace risks |
| 07 | Emotional Intelligence & Empathy | Affect calibration | ChatGPT 9.8× more empathetic (JAMA 2023); Oxford 2025: 8–13% error rate with warmth |
| 08 | Conversational Dialogue Systems | Latency + turn-taking | ~200ms inter-turn target (Stivers et al. 2009); 39% multi-turn performance drop |
| 09 | Bias, Fairness, Ethics | Regulation | EU AI Act Art. 50 Aug 2026; €15M/3% penalties; Italy €5M fine on Luka |
| 10 | Style Transfer and Voice | Voice cloning | TinyStyler ~800M beats GPT-4; rejection profiles > preference profiles |
| 11 | Theory of Mind | Social cognition | GPT-4o FANToM All* 0.8% (humans 87.5%); SimpleToM 49.5% → 93.5% with scaffolding |
| 12 | Cognitive Architectures | Agent memory + reflection | Reflexion 91% HumanEval vs GPT-4 80%; 1,052-agent study 85% test-retest; CoALA |
| 13 | Anthropomorphism and User Perception | User-side effects | HumT/DumT: users prefer less human-like in task contexts; ElevenLabs $11B; Soul Machines bankruptcy |
| 14 | Creative Writing and Storytelling | Structural tells | LLM stories 3–10× lower creativity; instruction-tuning as bottleneck; stdev gap |
| 15 | Academic Papers — LLM Humanization | Benchmarks + audits | Adversarial Paraphrasing 98.96% TPR drop; DAMAGE L1/L2/L3 taxonomy; Oxford warmth paper |
| 16 | GitHub Tools and Libraries | OSS tooling | blader/humanizer ~14.5k stars; GradEscape 139M params > DIPPER 11B; StealthRL GRPO Qwen3-4B |
| 17 | Industry Blogs and Case Studies | Deployment outcomes | Klarna reversal; Brynjolfsson +34% novice; no deployed system publishes perceived-humanness score |
| 18 | Commercial Humanizer Tools | Product landscape | ~150 products ~$500M+ revenue ~34M visits; DAMAGE audit; WriteHuman 1.98% vs QuillBot 93.56% |
| 19 | Agentic Autonomous Thinking | Cognitive humanness | Project Vend identity crisis; HumanLLM cognitive > behavioral; no reasoning-trajectory benchmark |
| 20 | Memory and Personalization | Continuity | LongMemEval 30–60% accuracy drop; PReF 67% win rate 30× fewer signals; no "feels human" metric |

---

## Theme → Category Index

### Subtraction-first humanization

The highest-leverage humanization is removal, not addition. Adding warmth adds sycophancy.

- Cat. 01 — prompt-level blacklists, anti-slop system prompts
- Cat. 02 — sycophancy as reward-model artifact
- Cat. 04 — sampler-level slop reduction (antislop-sampler)
- Cat. 16 — OSS implementations (antislop-sampler, blader/humanizer, avoid-ai-writing)
- Cat. 17 — "humanization via subtraction" pattern across 24 deployed products

### Structural tells (lexical vs. burstiness)

Sentence-length uniformity and paragraph rhythm are stronger signals than vocabulary.

- Cat. 04 — sentence-length stdev, min-p sampler, MAUVE
- Cat. 05 — detector evolution toward burstiness/entropy features
- Cat. 14 — human stdev ~8.2 vs GPT-4o ~4.1; instruction-tuning as structural bottleneck
- Cat. 15 — DAMAGE L1/L2/L3 tiers; Adversarial Paraphrasing burstiness
- Cat. 18 — Tier 1/2/3 humanizer taxonomy; statistical fingerprint layer

### RLHF and sycophancy

The AI voice as a post-training artifact; sycophancy as structural reward failure.

- Cat. 02 — Singhal et al.; LIMA; DPO; SimPO; Surge AI annotator economics
- Cat. 07 — warmth training → error rate increase (Oxford Internet Institute 2025)
- Cat. 15 — Oxford warmth finding +10–30pp error rates
- Cat. 17 — Anthropic anti-sycophancy as explicit product engineering

### Detection and evasion

The monthly-cadence arms race between humanizers and detectors.

- Cat. 05 — SynthID-Text; RAID benchmark; StealthRL; detector stealing
- Cat. 15 — Adversarial Paraphrasing; AuthorMist; MASH; HUMPA; SIRA
- Cat. 16 — StealthRL; GradEscape; antislop-sampler; DIPPER
- Cat. 18 — DAMAGE audit; commercial humanizer landscape; Turnitin AI-bypasser detection
- Cat. 09 — regulatory inflection (EU AI Act); FTC framing; false-positive harm (Liang et al.)

### Style transfer and voice calibration

Sounding like a specific person or brand, not just "not-AI."

- Cat. 10 — TinyStyler; STEER; hyperbolic trick; rejection profiles; extract-then-apply
- Cat. 12 — Park et al. 1,052-agent interview-conditioned simulation; 85% test-retest
- Cat. 03 — persona as versioned artifact; Character.AI four-layer model; drift within ~8 turns
- Cat. 20 — style memory as missing primitive; Lex Style Guides as closest commercial analog

### Cognitive architecture and agent humanness

Memory, reflection, planning — the structural determinants of whether an agent's *thinking* feels human.

- Cat. 12 — CoALA; Reflexion; Self-Refine; Park et al. Generative Agents
- Cat. 19 — four-module stack; Project Vend; HumanLLM; Thoughtful Agents; "agent = model + harness"
- Cat. 20 — tiered memory; PReF; LongMemEval; style memory gap
- Cat. 06 — chain-of-thought; "reason privately, humanize publicly"
- Cat. 11 — Theory of Mind gaps; explicit ToM ≠ applied ToM

### Memory and continuity

Persistent memory as the substrate for humanization techniques.

- Cat. 20 — tiered memory architecture; PReF; LongMemEval; Zep temporal KG; Letta
- Cat. 12 — CoALA working/episodic/semantic/procedural taxonomy
- Cat. 19 — relationship-continuity memory as missing primitive; Letta; MemGPT
- Cat. 03 — persona drift without persistent memory

### User perception and anthropomorphism

How users actually respond to humanized AI, including when it backfires.

- Cat. 13 — HumT/DumT; Crolic et al.; ElevenLabs vs Soul Machines; anthropomorphism backfire
- Cat. 07 — JAMA empathy finding; warmth-reliability tradeoff
- Cat. 17 — Klarna arc; novice-bias; no perceived-humanness metric; latency as humanness proxy
- Cat. 08 — latency targets; multi-turn performance drop

### Ethics, fairness, and regulation

Who gets harmed, who is responsible, and what is coming legally.

- Cat. 09 — EU AI Act; DarkBench; MASK; Character.AI/Google settlement; TOEFL bias
- Cat. 05 — Liang et al. false-positive finding (>50% TOEFL essays); defensive use case
- Cat. 18 — commercial humanizer ToS vs marketing gap; Turnitin bypasser detection; Brittany Carr case
- Cat. 17 — HN backlash; deception vs transparency debate

---

## Source Type → Category Index

### Peer-reviewed papers with key results

| Paper | Key result | Category |
|-------|-----------|---------|
| Singhal et al. arXiv 2310.03716 | Length explains most RLHF gains | 02 |
| LIMA (Zhou et al.) | 1,000 examples ≈ GPT-4 in 43% comparisons | 02 |
| DPO arXiv 2305.18290 | Preference alignment without AI-ism injection | 02 |
| DIPPER (Krishna et al., NeurIPS 2023) | DetectGPT 70.3% → 4.6%; SSTH 66.5% → 1.5% | 01, 05, 16 |
| HumT/DumT arXiv 2502.13259 | Users often prefer less human-like output | 01, 13 |
| Adversarial Paraphrasing (NeurIPS 2025) | 98.96% TPR drop on Fast-DetectGPT; basic paraphrase +8–15% TPR | 05, 15, 18 |
| StealthRL (2026) | 97.6% ASR, AUROC 0.79 → 0.43 | 05, 16 |
| Liang et al. *Patterns* 2023 | >50% TOEFL essays falsely flagged as AI | 05, 09, 18 |
| DAMAGE (COLING 2025) | 19 commercial humanizers audited; L1/L2/L3 taxonomy | 15, 18 |
| TinyStyler (EMNLP 2024) | ~800M beats GPT-4 on authorship transfer | 10, 16 |
| Ayers et al. JAMA 2023 | ChatGPT preferred 78.6%; 9.8× more empathetic | 07, 17 |
| Oxford Internet Institute 2025 | Warm training +8–13% error rate, +40% sycophantic false belief | 07, 15 |
| Park et al. arXiv 2411.10109 (1,052 agents) | 85% test-retest reliability from interview data | 03, 12, 19 |
| Reflexion (NeurIPS 2023) | 91% HumanEval vs GPT-4 80% | 12, 19 |
| LongMemEval (ICLR 2025) | Commercial assistants drop 30–60% on long-horizon histories | 20 |
| PReF arXiv 2503.06358 | 67% win rate over GPT-4o defaults with 30× fewer signals | 20 |
| Brynjolfsson et al. (NBER WP 31161) | +34% novice agents; ~0% top performers | 17 |
| Crolic et al. *Journal of Marketing* 2022 | Anthropomorphism backfires with angry customers (n ≈ 35,000) | 13, 17 |
| Dell'Acqua et al. HBS WP 24-013 | –19% correct-solution rate outside GPT-4's competence boundary | 17 |
| min-p arXiv 2407.01082 (ICLR 2025 Oral) | Naturalness gains without quality loss | 04 |
| CoALA arXiv 2309.02427 | Working/episodic/semantic/procedural taxonomy | 12, 20 |
| Nicks et al. (Stanford, ICLR 2024) | DPO humanizer drops AUROC from 0.84 to 0.63 in under a day | 05, 15, 18 |
| HumanLLM arXiv 2601.10198 | Cognitive modeling beats behavioral mimicry | 19 |
| Zep arXiv 2501.13956 | 94.8% DMR; bi-temporal validity | 20 |

### High-star OSS projects

| Repo | Stars | Category |
|------|-------|----------|
| All-Hands-AI/OpenHands | ~71k | 19 |
| FoundationAgents/MetaGPT | ~67k | 19 |
| mem0ai/mem0 | ~53.5k | 20 |
| blader/humanizer | ~14.5k | 16 |
| letta-ai/letta | ~22k | 19, 20 |
| getzep/graphiti | ~25.1k | 20 |
| humanlayer/12-factor-agents | ~19k | 19 |
| antislop-sampler | ~340 | 04, 16 |
| conorbronsdon/avoid-ai-writing | ~1.1k | 17 |
| dontriskit/awesome-ai-system-prompts | ~5.7k | 17 |

### Commercial tools with verified data

| Tool | Key verified claim | Category |
|------|-------------------|---------|
| Undetectable.ai | 72–89% independent bypass (15M+ users) | 18 |
| Intercom Fin | 66% avg resolution, 40M conversations, five tone presets | 17 |
| Klarna AI Assistant | 2.3M conv/month, ~700 FTE equiv, $40M; reversed 2026 | 17 |
| GPTZero | ~$20M ARR; TPR 99.73% → 60.04% after humanization (DAMAGE) | 05, 18 |
| ElevenLabs | $11B valuation Feb 2026 | 13 |
| SynthID-Text | Validated ~20M Gemini responses; DIPPER drops it to 1.5% TPR | 05 |
| Grammarly AI Humanizer | Only major vendor stating "not intended for bypass" | 18 |

---

## Cross-Category Dependencies

These pairs have strong bidirectional dependencies — findings in one category directly affect how you should interpret findings in the other.

**Cat. 02 → Cat. 01.** RLHF is *why* blacklist-based subtraction works. The AI-isms being scraped are reward-model artifacts, not model personality. Understanding Cat. 02 makes Cat. 01's techniques theoretically grounded rather than empirical hacks.

**Cat. 04 ↔ Cat. 05.** Sampler choices (Cat. 04) affect the statistical fingerprint detectors read (Cat. 05). You cannot evaluate whether your generation strategy works without understanding what detectors are measuring. Antislop-sampler reduces slop at generation time; detectors have evolved to measure burstiness, not vocabulary.

**Cat. 05 ↔ Cat. 18.** Detection research (Cat. 05) is the theoretical backbone; commercial humanizer products (Cat. 18) are the productization lagging by one to two technique generations. Research frontier is 20–30 ASR points ahead of commercial tier-1.

**Cat. 10 ↔ Cat. 03.** Style transfer (Cat. 10) is the technique layer; persona design (Cat. 03) is the application layer. Style transfer produces the right output registers; persona design maintains them across a session. Neither works without the other for long-horizon use cases.

**Cat. 12 → Cat. 19.** Cognitive architectures (Cat. 12) provides the framework vocabulary (CoALA, Reflexion, Generative Agents). Agentic autonomous thinking (Cat. 19) is where those frameworks play out in production. Read Cat. 12 first to understand why the patterns in Cat. 19 exist.

**Cat. 19 ↔ Cat. 20.** Memory (Cat. 20) is the substrate that agent humanness (Cat. 19) runs on. Reflection without persistent memory degrades every session. Persistent memory without reflection triggers produces static facts, not evolving understanding. The "relationship-continuity memory" gap is named in both categories.

**Cat. 07 ↔ Cat. 02.** The warmth-reliability tradeoff (Cat. 07) is the consequence of the RLHF mechanism (Cat. 02). Warmer training is more RLHF-aligned; that alignment is what introduces error rates. These two categories together make the case for subtraction-first humanization more strongly than either alone.

**Cat. 09 ↔ Cat. 05 ↔ Cat. 18.** Regulatory risk (Cat. 09) directly affects the commercial humanizer market (Cat. 18) and the detection-evasion arms race (Cat. 05). EU AI Act enforcement in August 2026, Turnitin AI-bypasser detection, and FTC framing all cross these three categories simultaneously.

---

## Entry Points by Question

**"Why does AI text sound like AI?"**
→ Cat. 02 (RLHF mechanism), then Cat. 14 (structural tells), then Cat. 04 (sampler contribution)

**"What's the fastest way to reduce AI-isms in output?"**
→ Cat. 01 (prompt techniques), Cat. 04 (antislop-sampler), Cat. 16 (OSS tools). Start with antislop-sampler + blacklist; then staged rewrite pipeline.

**"What do AI text detectors actually measure?"**
→ Cat. 05 (detector landscape), Cat. 15 (academic audits), Cat. 04 (burstiness/entropy metrics)

**"Can I detect AI text reliably?"**
→ Cat. 05 (current detector state), Cat. 15 (DAMAGE, Adversarial Paraphrasing), Cat. 18 (commercial tool audits). Short answer: no stable answer.

**"How do I make an agent maintain consistent voice across a long session?"**
→ Cat. 03 (persona design), Cat. 12 (reflection + memory architecture), Cat. 19 (long-horizon coherence), Cat. 20 (persistent memory)

**"What does research say about users' reaction to human-like AI?"**
→ Cat. 13 (anthropomorphism), Cat. 07 (empathy/warmth), Cat. 17 (deployment outcomes). Also: Cat. 08 for latency findings.

**"What is the regulatory landscape for AI-generated text?"**
→ Cat. 09 (primary), Cat. 18 (commercial tool compliance gap), Cat. 05 (watermarking)

**"How do I clone a specific person's writing style?"**
→ Cat. 10 (style transfer), Cat. 12 (interview-conditioned simulation), Cat. 03 (persona versioning), Cat. 20 (style memory)

**"What memory architecture should an LLM assistant use?"**
→ Cat. 20 (primary), Cat. 12 (CoALA taxonomy), Cat. 19 (production agent patterns)

**"What has actually worked in production humanization deployments?"**
→ Cat. 17 (only category covering real deployment outcomes), then Cat. 08 (latency data)

**"What are the ethical risks of humanizing AI text?"**
→ Cat. 09 (regulatory/bias), Cat. 13 (anthropomorphism harm), Cat. 18 (commercial tool practices), Cat. 17 (deception debate)

**"What's the state of commercial humanizer tools?"**
→ Cat. 18 (primary), Cat. 05 (arms race context), Cat. 16 (OSS alternative landscape)

**"What is context engineering and why does it matter for humanization?"**
→ Cat. 19 (primary), Cat. 12 (CoALA), Cat. 20 (memory as context). "Humanization is downstream of what the agent remembers, forgets, and surfaces at each step."

---

## What's Not Covered

The following are relevant to humanization but fall outside the 20 categories or appear only as references without dedicated coverage.

**Multimodal humanization.** Voice disfluency patterns, visual turn-taking, avatar expression. `humanizer-x` is the only OSS project shipping SSML disfluency injection for voice. ElevenLabs gets brief coverage in Cat. 13 but voice humanization has no dedicated category. Identified in Cat. 17, 19 as the biggest open frontier with the thinnest evidence base.

**Hardware and inference economics.** Character.AI serves 20k QPS with 95% KV-cache hit rate and 33× cost reduction since 2022. Mem0 reports −91% p95 latency. These numbers appear in Cat. 20 and Cat. 17 respectively, but there is no dedicated cost-of-humanization category.

**Non-English humanization.** Every serious humanization benchmark is English-only. Klarna deployed across 35 languages; Fin across 45. No category covers cross-lingual humanization explicitly, though Cat. 09 covers the Liang et al. ESL bias finding and Cat. 18 flags the multilingual gap.

**Human-in-the-loop annotation economics.** Surge AI ($1.4B 2025 revenue, 121 employees) represents a shift in who bears the cost of alignment. Cat. 02 covers this briefly but it is not systematically analyzed.

**Long-form creative narrative.** Cat. 14 covers LLM story evaluation at the paragraph level but not book-length narrative coherence. DOC +22.5pp coherence is the closest benchmark, but 80k-word structural humanization is unaddressed.

**Memory-security interaction.** Rehberger's indirect prompt injection via malicious documents that write persistent false memories (Cat. 20) has no canonical defense. Cat. 09 covers the bias and fairness angle but not memory as an attack surface.

**Enterprise brand-voice at editorial scale.** Cat. 17 notes this is almost certainly under NDA. Cat. 10 covers the style-transfer techniques. The deployment-scale implementation — applying brand-voice humanization to 10,000 articles/month — has no public coverage.

**AI-slop reasoning patterns.** Cat. 19 names this gap explicitly: there are blacklists for AI-slop prose but no equivalent catalog for AI-slop reasoning patterns (over-explaining, over-hedging, over-decomposing, infinite-loop rationalization). No category fills it.
