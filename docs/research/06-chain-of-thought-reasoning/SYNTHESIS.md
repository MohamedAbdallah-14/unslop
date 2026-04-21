# Category 06 — Chain of Thought Reasoning

## Scope

This category covers the full lifecycle of how LLMs reason out loud — from the 2022 academic papers that established the basic patterns (CoT, zero-shot CoT, self-consistency, Tree of Thoughts, ReAct, Reflexion) through the 2024–2026 shift to RL-trained reasoning models (o1, DeepSeek-R1, Kimi k1.5, Gemini Deep Think) and the commercial, open-source, and practitioner layers built on top of them. The focal question for the Unslop project is narrow: reasoning traces are now a first-class product surface, they frequently read like machine output rather than human thought, and the industry has acknowledged this problem without publishing a clean solution.

---

## Executive Summary

- The 2022–2023 era established that showing intermediate steps ("chain of thought") unlocks reasoning in large models without fine-tuning — PaLM-540B with 8 CoT exemplars hit 58.1% on GSM8K (A), and simply prepending "Let's think step by step" moved MultiArith accuracy from 17.7% to 78.7% (A). These results seeded the entire downstream humanization thesis: reasoning made visible reads as human deliberation. **Note (2025): explicit CoT prompting is now empirically shown to be ineffective or counterproductive on reasoning-tier models (Wharton GAIL, Jun 2025). The "think step by step" era is over for frontier models.**

- By 2025 the prompting era had been overtaken by training-time approaches. DeepSeek-R1-Zero showed that pure RL with rule-based rewards causes long CoT, self-verification, and "aha moments" to emerge in a 671B model without any SFT cold-start — AIME 2024 pass@1 reached 71.0% (86.7% with majority voting), matching OpenAI-o1-0912 (A). TinyZero reproduced the core behavior in a 3B model for under $30 (C), confirming this is not a scale-only artifact. DeepSeek-R1 was subsequently published in *Nature* (2025), formalizing it as a landmark result.

- Visible CoT is demonstrably unfaithful to internal computation. Turpin et al. 2023 found reordering MCQ options shifted predictions by up to 36% on BIG-Bench Hard while the CoT never mentioned the bias (A). Anthropic's 2025 study found Claude 3.7 Sonnet mentioned embedded hints only 25% of the time and R1 only 39%, even when answers demonstrably relied on the hints — and unfaithful CoTs were longer, not shorter (B). Empirical unfaithfulness rates across models (arXiv 2503.08679, discussed on HN) ranged from 13% (GPT-4o-mini) down to 0.04% (Sonnet 3.7 thinking) (E).

- Two transparency postures have hardened at the product layer. OpenAI hides raw CoT and ships a summarized surface — **GPT-5 (Aug 2025) merges the o-series reasoning with the chat product, routing internally between fast and extended-thinking modes, removing the explicit mode selection developers relied on.** Anthropic ships a visible `thinking` block, now with **adaptive thinking** (Claude 4 series) where the model decides reasoning depth rather than the developer setting `budget_tokens`. DeepSeek ships fully visible `reasoning_content`. Each implies a different humanization strategy (D, B).

- A canonical "reason privately, humanize publicly" pattern has emerged. DeepSeek-R1-Zero's RL-only training produced strong reasoning but unreadable, language-mixed output. A downstream readability/character SFT pass fixed it (B, C). OpenAI similarly summarizes before surfacing. This two-pass structure is structurally identical to what Unslop does.

- Legible human-voiced CoT trades off against raw capability. R1's language-mixing fix demonstrably degraded final-answer quality on some tasks (E). Raschka flags "over-thinking" as a real failure mode (B). SimpleRL-Zoo found that response length does not correlate with self-verification or reflection (C). Humanized reasoning is not free.

- Humanization of reasoning traces is an open white space. Labs optimize CoT for math, code, and science — not for tone, register, empathy, or conversational naturalness. There is no published pipeline that jointly trains reasoning ability and a consistent persona voice (B, C). No major product post-processes CoT into human-grade explanation (D). The community has no standard prompt pattern for "humanized-but-faithful" reasoning (E).

- Karpathy's IQ-vs-EQ split is underappreciated but load-bearing for this project. RL/test-time compute helps IQ tasks (math, code). Pretraining-scale-derived "vibes" drive EQ gains (word choice, humor, calibration). Humanization lives in the EQ layer, not the IQ layer — and the two are not the same axis (E).

---

## Cross-Angle Themes

**Thought structure has generalized in a clear arc.** CoT (linear narration, Wei 2022) gave way to Self-Consistency (multi-sample marginalizing, Wang 2022) to Tree of Thoughts (BFS/DFS with backtracking, Yao 2023) to Graph of Thoughts (DAG with merge/refine, Besta 2023) to multi-agent debate (Grok 4.20's four-persona architecture, Gemini Deep Think's parallel hypotheses, Meta Collaborative Reasoner). Each step represents a more humanlike mode of deliberation — narration, then exploration, then synthesis. Sources: A (papers), B (Gemini Deep Think, Meta posts), C (ToT, GoT, ReAct repos), D (Grok, Gemini products).

**Faithfulness is the category's central unresolved tension.** Academic papers (Turpin A), Anthropic research (B), and empirical surveys discussed on HN (E) all converge on the same finding: CoT explanations often do not reflect the model's actual computation, larger models tend to be less faithful, and outcome-based RL improves faithfulness only up to a plateau around 28%. The humanization-relevant twist from angle E: humans also post-hoc rationalize (Nisbett & Wilson, Kahneman), so a fluent-but-slightly-unfaithful trace may read more human than a perfectly faithful but robotic one.

**Dual-process framing is the shared vocabulary.** Kahneman's System 1/System 2 shows up in Li et al.'s survey (A), Weng's "Why We Think" (B), Lambert's compute-allocation reframe (B), Amodei's "continuous spectrum" framing (B), and the r/LocalLLaMA threads that treat reasoning as a cognitive mode to switch on or off (E). It is load-bearing for researcher intuitions and product marketing alike.

**"Reason privately, humanize publicly" has become the canonical two-pass pattern.** Angle B documents it in multiple labs' public writing; angle C shows it in the DeepSeek-R1 and Open-R1 codebases; angle D shows it in OpenAI's hidden-CoT-plus-summary and Anthropic's un-character-trained thinking block; angle E shows practitioners discovering it from the bottom up ("don't CoT a reasoning model; shape the output").

**Open-weights reasoning is now the default assumption.** DeepSeek-R1 (MIT, 671B + 6 distilled sizes, ~92k+ GitHub stars), Open-R1 (~26k stars, Mixture-of-Thoughts 350K traces), Open-Reasoner-Zero, SimpleRL-Zoo, TinyZero, **Kimi K2 Thinking (Nov 2025, 1T-param MoE, Modified MIT, 256K context, tool-fused reasoning)**, and **Qwen3 (235B-A22B and 30B-A3B MoE, Apr–mid 2025)** — by 2026, licensing is not the constraint for humanization research (C). The commodity pricing gap is also real: DeepSeek R1 at $0.27–$0.55 per million tokens vs. earlier o1 at $15/$60; GPT-5 Thinking is priced as a premium tier within the unified product (B, D).

**Thinking budget is diverging into two patterns.** Anthropic's Claude 4 has replaced `budget_tokens` with **adaptive thinking** — the model decides reasoning depth per request. GPT-5's internal router makes the same decision without developer access. Meanwhile, You.com's effort dial, Gemini Deep Think vs. standard mode, and llama.cpp's `--reasoning-budget` with a natural-language cutoff message remain explicit. The s1 paper (Jan 2025) formalized **budget forcing** — appending "Wait" tokens to extend thinking, or truncating to shorten — as a reproducible inference-time technique. The form of the stop signal matters: a natural-language cutoff ("time to commit to an answer") recovers quality from 78% to 89% vs. hard truncation's drop from 94% (E, D, C). The trend is toward model-decided budgets, which removes a direct humanization control surface.

**Persona-first agent design has arrived but not yet merged with reasoning-RL.** CrewAI's `role/goal/backstory` pattern (~48k stars, ~5.4M PyPI downloads/month) makes voice a first-class attribute alongside capability (C). DSPy makes reasoning traces optimizable artifacts (C). But no public pipeline jointly trains reasoning ability and a consistent persona. They are parallel tracks (B gap, C gap).

---

## Top Sources

### Must-read papers

1. Wei et al. 2022 — Chain-of-Thought Prompting — [arXiv:2201.11903](https://arxiv.org/abs/2201.11903). Foundational. PaLM-540B + 8 exemplars, 58.1% GSM8K. *(Historical baseline; explicit CoT prompting now deprecated for reasoning-tier models.)*
2. Kojima et al. 2022 — Large Language Models are Zero-Shot Reasoners — [arXiv:2205.11916](https://arxiv.org/abs/2205.11916). "Let's think step by step." MultiArith 17.7% → 78.7%. *(Valid for non-reasoning models; superceded for reasoning-tier by Wharton 2025.)*
3. Wang et al. 2022 — Self-Consistency — [arXiv:2203.11171](https://arxiv.org/abs/2203.11171). +17.9 pts GSM8K over vanilla CoT.
4. Yao et al. 2023 — Tree of Thoughts — [arXiv:2305.10601](https://arxiv.org/abs/2305.10601). Game of 24: 4% (GPT-4 CoT) → 74% (ToT).
5. Besta et al. 2023 — Graph of Thoughts — [arXiv:2308.09687](https://arxiv.org/abs/2308.09687). +62% quality over ToT on sorting at >31% lower cost.
6. Yao et al. 2022 — ReAct — [arXiv:2210.03629](https://arxiv.org/abs/2210.03629). +34% absolute on ALFWorld vs. baselines; the proto-pattern for agents.
7. Shinn et al. 2023 — Reflexion — [arXiv:2303.11366](https://arxiv.org/abs/2303.11366). 91% pass@1 on HumanEval; verbal self-critique as reinforcement.
8. Madaan et al. 2023 — Self-Refine — [arXiv:2303.17651](https://arxiv.org/abs/2303.17651). ~20% absolute preference gain across 7 tasks with no training.
9. Turpin et al. 2023 — Language Models Don't Always Say What They Think — [arXiv:2305.04388](https://arxiv.org/abs/2305.04388). The faithfulness problem, formalized. Biasing features shift predictions up to 36% while CoTs stay silent about it.
10. Lightman et al. 2023 — Let's Verify Step by Step — [arXiv:2305.20050](https://arxiv.org/abs/2305.20050) · [PRM800K](https://github.com/openai/prm800k). 78% on representative MATH subset; 800K step-level labels.
11. DeepSeek-AI 2025 — DeepSeek-R1 — [arXiv:2501.12948](https://arxiv.org/abs/2501.12948). AIME 2024 15.6% → 71.0%; emergent "aha moment" from pure RL. Published in *Nature* 2025.
12. Kimi Team 2025 — Kimi k1.5 — [arXiv:2501.12599](https://arxiv.org/abs/2501.12599). 77.5 AIME, 96.2 MATH-500; long-context RL without MCTS or PRMs.
13. Li et al. 2025 — From System 1 to System 2: A Survey — [arXiv:2502.17419](https://arxiv.org/abs/2502.17419). The single best landscape map of the reasoning-LLM field.
14. Zelikman et al. 2022 — STaR — [arXiv:2203.14465](https://arxiv.org/abs/2203.14465). Ancestor of R1-Zero-style self-generated reasoning data.
15. OpenAI 2024 — o1 System Card — [PDF](https://cdn.openai.com/o1-system-card-20241205.pdf). Industrial reference for long-CoT + deliberative alignment.
16. Muennighoff et al. 2025 — s1: Simple Test-Time Scaling — [arXiv:2501.19393](https://arxiv.org/abs/2501.19393). Budget forcing with "Wait" tokens; 1K training samples beat o1-preview by 27% on AIME. *(New, Jan 2025.)*
17. Korbak et al. 2025 — Chain of Thought Monitorability — [arXiv:2507.11473](https://arxiv.org/abs/2507.11473). CoT as a fragile safety surface; 41 authors across DeepMind/OpenAI/Anthropic. *(New, Jul 2025.)*
18. Chen et al. 2024/2025 — Coconut: Reasoning in a Continuous Latent Space — [arXiv:2412.06769](https://arxiv.org/abs/2412.06769). ICLR 2025. Latent-space BFS; no surface CoT tokens needed. *(New, ICLR 2025.)*
19. arXiv 2503.08679 (2025) — CoT Reasoning In The Wild Is Not Always Faithful. Production model faithfulness rates: GPT-4o-mini 13%, Sonnet 3.7 thinking 0.04%. *(New, Mar 2025.)*
20. Meincke, Mollick et al. 2025 — The Decreasing Value of CoT in Prompting — [Wharton GAIL](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/). Empirical tombstone for explicit CoT on reasoning-tier models. *(New, Jun 2025.)*

### Key essays and posts

1. OpenAI — "Learning to Reason with LLMs" (Sep 2024) — <https://openai.com/index/learning-to-reason-with-llms/>. The "think before you speak" frame; rationale for hidden CoT; o1 hits 83% AIME vs. GPT-4o's 13%.
2. Anthropic — "Claude's extended thinking" (Feb 2025) — <https://www.anthropic.com/research/visible-extended-thinking>. Visible, un-character-trained CoT as a deliberate design choice; 84.8% GPQA with parallel test-time compute.
3. Anthropic — "Reasoning models don't always say what they think" (Apr 2025) — <https://www.anthropic.com/research/reasoning-models-dont-say-think>. Claude 3.7 Sonnet hint-mention rate 25%, R1 39%; unfaithful CoTs longer, not shorter.
4. Lilian Weng — "Why We Think" (May 2025) — <https://lilianweng.github.io/posts/2025-05-01-thinking/>. Dual-process + latent-variable framings; sequential revision can degrade correct answers without external feedback.
5. Nathan Lambert — "Why reasoning models will generalize" (Jan 2025) — <https://www.interconnects.ai/p/why-reasoning-models-will-generalize>. Reasoning as compute-allocation; R1's strong creative-writing leaderboard results.
6. Sebastian Raschka — "Understanding Reasoning LLMs" (Feb 2025) — <https://sebastianraschka.com/blog/2025/understanding-reasoning-llms.html>. Four-path taxonomy (inference-time scaling, pure RL, SFT+RL, distillation); the over-thinking warning.
7. Jay Alammar — "The Illustrated DeepSeek-R1" (Jan 2025) — <https://newsletter.languagemodels.co/p/the-illustrated-deepseek-r1>. Automatic verifiability as the key ingredient; the readability-SFT pattern.
8. Simon Willison — Notes on o1 and DeepSeek-R1 — <https://simonwillison.net/2024/Sep/12/openai-o1> · <https://simonwillison.net/2025/Jan/20/deepseek-r1/>. Practitioner critique of hidden CoT; the "Wait, but" thinking-extension hack.
9. Karpathy on GPT-4.5 (Feb 2025) — <https://threadreaderapp.com/thread/1895213020982472863.html>. The IQ-vs-EQ split — reasoning and humanness are orthogonal axes.
10. Google DeepMind — "Gemini Deep Think" (Feb 2026) — <https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/>. Parallel thinking, Aletheia agent, balanced prompting, IMO Gold 2025.
11. OpenAI — "Introducing o3 and o4-mini" (Apr 2025) — <https://openai.com/index/introducing-o3-and-o4-mini/>. AIME 2025 saturation (99.5% with tools); o4-mini as first model to "think with images"; last standalone o-series.
12. OpenAI — "Introducing GPT-5" (Aug 2025) — <https://openai.com/index/introducing-gpt-5/>. Unified reasoning + chat via internal routing; GPT-5 Thinking 50–80% fewer tokens than o3. Marks end of separate reasoning-model tier.
13. Anthropic — "Introducing Claude 4" (2025) — <https://www.anthropic.com/news/claude-4>. Opus 4, Sonnet 4 with adaptive thinking; interleaved thinking + tool use; Opus 4.6 SWE-bench 72.5%.
14. Meincke, Mollick et al. — "The Decreasing Value of CoT in Prompting" (Jun 2025) — <https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/>. The definitive empirical study showing CoT prompts add no meaningful benefit on reasoning-tier models.

### Key open-source projects

- [deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1) — open-weights long-CoT reasoning model (MIT, 671B + 6 distilled sizes 1.5B–70B), ~92k+ stars. Also published in *Nature* 2025.
- [huggingface/open-r1](https://github.com/huggingface/open-r1) — fully open reproduction pipeline + Mixture-of-Thoughts (350K traces) + OpenR1-Distill-7B, ~26k stars.
- [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) — `ChainOfThought`, `ReAct` as optimizable modules; MIPROv2 / GEPA optimizers learn better prompts from data.
- [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) — stateful agent graphs with durable execution and human-in-the-loop interrupts, ~28.7k+ stars.
- [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) — role/goal/backstory agent crews; persona-first reasoning, ~48k+ stars, ~5.4M PyPI downloads/month.
- [openai/prm800k](https://github.com/openai/prm800k) — 800K step-level correctness labels; companion to Lightman et al. 2023.
- [PRIME-RL/PRIME](https://github.com/PRIME-RL/PRIME) — implicit process rewards from outcome models, no human step annotation needed.
- [princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm) — canonical ToT reference, ~5.9k stars.
- [noahshinn/reflexion](https://github.com/noahshinn/reflexion) — verbal self-critique with configurable Actor/Evaluator/Self-Reflection modules, ~3.1k stars.
- [hkust-nlp/simpleRL-reason](https://github.com/hkust-nlp/simpleRL-reason) — aha moment reproduced across 10 base model families, ~3.8k stars.
- [simplescaling/s1](https://github.com/simplescaling/s1) — budget forcing with "Wait" tokens; 1K training samples; EMNLP 2025. *(New, 2025.)*
- [MoonshotAI/Kimi-K2-Thinking](https://huggingface.co/moonshotai/Kimi-K2-Thinking) — 1-trillion-parameter MoE reasoning model, 32B active, 256K context, tool-fused CoT, Modified MIT. *(New, Nov 2025.)*
- [facebookresearch/coconut](https://github.com/facebookresearch/coconut) — latent continuous reasoning, ICLR 2025; no surface CoT tokens; BFS in hidden space. *(New, 2025.)*

### Notable commercial tools

**Reasoning-native APIs:** OpenAI o1 ($15/$60 per M tokens, hidden CoT; *historical* — mostly superseded by GPT-5) · o3/o4-mini ($2/$8, $1.10/$4.40; last standalone o-series, Apr 2025) · **OpenAI GPT-5 / GPT-5.2 / GPT-5.4** — unified routing between fast and GPT-5 Thinking modes; opaque; current flagship (Aug 2025 onward) · Anthropic Claude Extended / Adaptive Thinking — visible `thinking` block; `budget_tokens` superseded by adaptive thinking on Claude 4 series; "Keep thinking" brand campaign · Google Gemini 3 Deep Think — parallel reasoning, ~$24.99/mo consumer · DeepSeek Reasoner (R1-0528) — `reasoning_content` field, open weights, commodity pricing ($0.27–$0.55/M) · xAI Grok 4.20 Reasoning — four-persona "debate" (Grok/Harper/Benjamin/Lucas), $2/$6 per M tokens.

**Reasoning-optimized platforms:** Perplexity Pro/Max (Sonar Reasoning Pro API $2/$8 per M tokens) · You.com Advanced Research (up to 1,000 reasoning turns, ~10M tokens, 200+ sources per query) · Consensus.app Scholar Agent (250M+ papers, Consensus Meter).

**Agent-reasoning systems:** Cognition Devin (Pro $20/Max $200/mo; ACUs ≈ 15 min of work) · Reflection AI Asimov (comprehension-first, $2B raise Oct 2025 at $8B valuation) · Lindy · Relevance AI.

### Notable community threads and practitioner reports

- [r/LocalLLaMA — "Reasoning should be thought of as a drawback, not a feature"](https://www.reddit.com/r/LocalLLaMA/comments/1o7bve2/) — the collapse-by-default UX argument.
- [r/LocalLLaMA — "Qwen3.5-397B thought chains look very similar to Gemini 3's"](https://www.reddit.com/r/LocalLLaMA/comments/1r6taah/) — convergent "Wait… Let me… Actually… Hmm" voice across R1-distilled models.
- [r/ChatGPT — "AI internal monologues"](https://www.reddit.com/r/ChatGPT/comments/1qze1p7/) — the `<inner-monologue>` tag pattern; inner voice should be first-person, hesitant, referencing prior turns.
- [r/ChatGPTPromptGenius — "Cognitive Mesh Protocol"](https://www.reddit.com/r/ChatGPTPromptGenius/comments/1qak6um/) — expansion/compression "breathing" system prompt.
- [OpenAI Developer Forum — "O1 Tips & Tricks"](https://community.openai.com/t/o1-tips-tricks-share-your-best-practices-here/937923) — canonical "don't CoT a reasoning model; specify the output" thread.
- [HN — arXiv 2503.08679 discussion](https://news.ycombinator.com/item?id=44900340) — empirical unfaithfulness rates per model.
- [r/LocalLLaMA — "Llama.cpp with a true reasoning budget"](https://www.reddit.com/r/LocalLLaMA/comments/1rr6wqb/) — natural-language cutoff message recovers 89% quality vs. 78% on hard truncation.
- Wharton GAIL Technical Report (Jun 2025) — [The Decreasing Value of Chain of Thought in Prompting](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/) — the empirical practitioner close to the "should I add CoT prompts?" debate. Answer: no, for reasoning-tier models.

---

## Key Techniques & Patterns

### Prompting-layer patterns

1. **Zero-shot CoT** — "Let's think step by step" / "Take a deep breath and work through this" — still the most reused cue for non-reasoning models; measurable accuracy gains on PaLM-2/early GPT-4 era models (E).
2. **Few-shot CoT exemplars** — show the desired reasoning shape, not just the answer (Wei 2022, A).
3. **Self-consistency** — sample N reasoning paths, take the majority-voted answer; +17.9 pts on GSM8K over vanilla CoT (A).
4. **Tree/Graph search over thoughts** — propose thoughts, self-evaluate, backtrack, merge partial solutions; Game of 24 from 4% to 74% (ToT, A/C).
5. **ReAct loops** — `Thought → Action → Observation`, the backbone of every modern agent framework (A/C).
6. **Self-critique and self-refine** — Actor + Evaluator + Reflector (Reflexion); `<inner-monologue>` tags; Cognitive Mesh expansion/compression cycles (A/C/E).
7. **Program-aided reasoning (PAL, PoT)** — narrate in natural language, offload arithmetic to an interpreter; +15 pts on GSM8K over PaLM-540B + CoT (A).
8. **Least-to-most prompting** — decompose then solve in sequence; code-davinci-002 hits ≥99% on SCAN with 14 exemplars vs. 16% with CoT (A).
9. **Balanced prompting** — ask for proof and refutation simultaneously to prevent confirmation bias; used in Gemini Deep Think's Aletheia agent (B).
10. **"Overthinking" counter-prompts** — "What's the boring solution?", "Occam's-razor this" — calibrate effort down when models over-elaborate (E).
11. **`<think>` manipulation** — intercept `</think>` and replace with "Wait, but" or "So" to force deeper reasoning on demand (B/E).
12. **Thinking-budget cutoff messages** — natural-language stop signal ("time to commit to an answer") preserves quality where hard truncation degrades it (E/D).
13. **Structural separation: inner voice and final answer** — both OpenAI's guide and community prompts converge on keeping deliberation in a dedicated block separate from the terminal response (E/B).

### Training-layer patterns

14. **STaR / rationalization loop** — sample rationales, condition on correct answer for wrong ones, fine-tune on successful rationales, repeat (Zelikman 2022, A).
15. **Process reward models** — reward each step, not just the outcome; 78% on MATH test subset with PRM800K (Lightman 2023, A/C).
16. **Implicit process rewards (PRIME)** — derive step rewards from an outcome model; removes the human-annotation bottleneck (C).
17. **Pure-RL reasoning** — rule-based rewards + GRPO/PPO on a base model; reflection, self-verification, and aha moments emerge without SFT (DeepSeek-R1-Zero, TinyZero, SimpleRL-Zoo, Open-Reasoner-Zero, A/C).
18. **Cold-start SFT → reasoning RL → rejection sampling → mixed RL** — the canonical four-stage DeepSeek-R1 recipe (A/B/C).
19. **Long-context RL (Kimi k1.5)** — 128K context + partial rollouts + online mirror descent; no MCTS or PRM required (A).
20. **Readability/character SFT after reasoning RL** — the fix for R1-Zero's language mixing; the "reason privately, humanize publicly" two-pass structure (A/B/C/D).

### UX and product patterns

21. **Collapsed-by-default thinking blocks** — brief summary visible, full trace expandable on demand; matches how humans surface deliberation (E/D).
22. **Step trays with meaningful labels** — "Searching 12 papers" beats "Processing…" for trust and time-setting (D).
23. **Thinking budget as a user-visible dial** — Anthropic `budget_tokens`, You.com effort slider, Gemini Deep Think toggle (D).
24. **Multi-agent debate/panels** — Grok's four named personas, Consensus's Scholar Agent stages, Gemini Deep Think's parallel hypotheses (B/D).
25. **Reasoning-as-time pricing** — Devin's ACUs (≈15 min of work), Lindy's credits, Relevance's Actions; abstracts away tokens for end buyers (D).

---

## Controversies & Debates

**Is visible CoT faithful to the model's real computation?**
Turpin 2023, Anthropic 2023, Anthropic 2025, and arXiv 2503.08679 all say: often not. Larger, more capable models produce *less* faithful traces. Outcome-based RL improves faithfulness but plateaus around 28%. The uncomfortable corollary (E): humans also post-hoc rationalize, so a fluent-but-slightly-unfaithful trace may read more human than a perfectly faithful but robotic one. Both communities and alignment researchers treat this as unresolved.

**Should raw CoT be hidden or visible?**
OpenAI hides it (alignment monitoring, UX, competitive moat) and ships a summary. Anthropic ships visible `thinking` blocks, explicitly un-character-trained, with a faithfulness disclaimer. DeepSeek ships fully visible `<think>` tags, directly editable via the "Wait, but" trick. Consumer Gemini lands in the middle. This is a product decision, not a technical inevitability (B/D/E). OpenAI's February 2025 o3-mini transparency patch came in direct response to DeepSeek R1's competitive pressure, suggesting the visible camp is gaining ground.

**Does "Let's think step by step" still help?**
Beginner tutorial content (YouTube, DataCamp, IBM) says yes, universally. Cognition Labs, the OpenAI Developer Forum o1 thread, and HN/r/LocalLLaMA say no for modern reasoning models — and possibly counterproductive, because they already reason internally (E). A practitioner HN thread found "think carefully" added to Claude Sonnet often matched DeepSeek-R1 accuracy at a fraction of the cost, cutting both ways (E).

**Is reasoning a new capability or just more compute allocated at test time?**
Lambert, Raschka, and Weng frame it as "learning to allocate more test-time compute to harder problems" — a general skill, not a distinct capacity. OpenAI's product framing (o1 is a separate tier) pushes the other way. Anthropic's "continuous spectrum" language sides with the compute-allocation camp (B). This debate has practical stakes: if reasoning is just compute allocation, humanization needs its own policy for when to think versus when to just answer.

**PRM vs. outcome-only rewards.**
PRM800K / Lightman 2023 argue step-level supervision produces reasoning that is correct for correct reasons (A). DeepSeek-R1-Zero and Open-Reasoner-Zero argue you don't need PRMs at all — rule-based outcome rewards plus scale is enough (A/C). PRIME finds a middle path with implicit process rewards from outcome models (C). Ongoing; no consensus.

**Length does not equal quality.**
SimpleRL-Zoo explicitly found that response length does not correlate with self-verification or reflection (C). QwQ-32B famously enters recursive reasoning loops (A). llama.cpp users and r/LocalLLaMA catalog "thinking loops" ("Wait the source is… New plan… Wait let me check again…") as a real failure mode requiring temperature increases or budget cutoffs (E). Longer CoT is not better CoT.

**Emergent reasoning: real or a metric artifact?**
Wei et al. 2022 (Emergent Abilities) framed CoT as a discontinuous emergent capability above scale thresholds (A). Schaeffer et al. 2023 argued this is partly a metric artifact. arXiv 2508.01191 (Aug 2025) adds a data-distribution lens: CoT may be strong pattern-matching on training distributions rather than transferable reasoning. Angle A explicitly flags this as an unresolved caveat. The debate matters for humanization claims about what models "really" do at scale — and, counterintuitively, the "mirage" framing supports humanization: if CoT is already a trained-in performance rather than genuine cognition, styling it for human readers is legitimate rather than deceptive.

**Sycophancy and reasoning interact in complex ways.**
OpenAI's April 2025 GPT-4o sycophancy postmortem — rolling back an update that made the model "overly flattering and agreeable" — is not reconciled with their reasoning work. Independent research shows CoT can both reduce and mask sycophancy: models construct plausible-sounding rationales for agreeing with a wrong user. Humanization layers that make reasoning traces more fluent risk compounding this (B).

**Safety of surfaced reasoning.**
H-CoT (arXiv 2502.12893) showed that allowing users to see or write the reasoning trace creates an attack surface: refusal rates drop from ~98% to <2% when the trace is manipulated. OpenAI's deliberative alignment approach trains models to reason over the safety spec before answering. Any humanization that makes the reasoning trace more readable and accessible needs to decouple "sounds human" from "is a direct dump of safety-relevant computation" (E).

---

## Emerging Trends

- **From "elicit reasoning" to "shape reasoning."** Community attention has shifted from "how do I get the model to think?" to "the model already thinks — how do I make the thinking shorter, more human-voiced, more committed?" (E). This is the practical frontier for the Unslop project.

- **Transparency as competitive differentiation.** Anthropic's "Keep thinking" brand campaign (Sep 2025, Netflix/Hulu/NYT/WSJ), DeepSeek's open `reasoning_content`, and OpenAI's reactive o3-mini transparency patch all push the same direction: letting users see the reasoning builds trust (B/D).

- **Reasoning distillation down-market.** DeepSeek-R1-Distill-Qwen-1.5B/7B, OpenR1-Distill-7B, and TinyZero's "aha moment for <$30" bring humanlike CoT to consumer- and edge-scale models. The reasoning substrate is becoming a commodity (A/B/C).

- **Parallel and multi-agent thinking replacing single-stream CoT.** Gemini Deep Think (parallel hypotheses simultaneously), Grok 4.20 (four named internal agents debating), You.com's 1,000-turn agentic loop, Meta Collaborative Reasoner — single-thread CoT is being displaced by orchestrated multi-stream reasoning (B/D).

- **Convergent "voice" across frontier reasoning models.** The "Wait… Hmm… Actually… Let me check…" first-person register is now shared by R1, Qwen3.5, Kimi K2, QwQ, and Gemini 3 — traceable to shared distillation lineage from DeepSeek-R1 (E).

- **Latent and continuous reasoning as the next frontier.** Recurrent-depth papers, Coconut-style continuous thought tokens, and Meta's Large Concept Models (operating on sentence-level SONAR embeddings rather than tokens) argue that token-level CoT is sub-human — humans plan at the level of concepts and sentences (B). Capability win, interpretability loss.

- **Natural-language budget and commit signals standardizing — then bifurcating.** llama.cpp `--reasoning-budget-message` and the s1 "Wait" budget-forcing technique formalize natural-language stop/extend signals as first-class inference primitives. At the same time, GPT-5's opaque routing and Claude 4's adaptive thinking move budget decisions *away from developers* and into the model. The industry is splitting: explicit-budget APIs (You.com effort dial, Gemini Deep Think toggle) versus adaptive-budget models (GPT-5, Claude 4 adaptive). Both have humanization implications — explicit lets you control depth, adaptive removes that lever but simplifies the interface (E/D).

- **Tool use fused into the reasoning trace.** Kimi K2 Thinking (Nov 2025) and Claude 4's interleaved thinking both merge tool invocations into the CoT pass rather than deferring them to after the thinking block closes. This produces reasoning traces where the model interrupts its deliberation to search or execute code — closely matching how human researchers actually work. This is the next frontier for humanized CoT: not just how it sounds, but whether it *interacts with reality mid-thought* (C/D).

- **Explicit CoT prompting empirically deprecated for reasoning-tier models.** The Wharton GAIL report (Jun 2025) is the first rigorous empirical study to show that CoT prompts add no meaningful benefit and increase variance on reasoning-tier models (o3, Claude 4, etc.). This closes the debate that had been running since 2023 in practitioner communities. "Think step by step" is now a beginner mistake on modern reasoning models (E/A).

- **Latent and continuous reasoning as the next frontier.** Coconut (ICLR 2025), Heima (single-token CoT compression), and the Latent CoT Survey (arXiv 2505.16782, May 2025) show that token-level CoT is sub-optimal and that reasoning can happen entirely in hidden states. Capability win, interpretability loss. If this trajectory continues, there will be no surface trace to humanize — the entire humanization pass becomes synthetic rather than styled (A/B).

- **Agent framework re-consolidation.** AutoGen is in maintenance mode (→ Microsoft Agent Framework). The category is compressing around stateful graphs + tools + MCP/A2A interop (C/D).

---

## Open Questions & Research Gaps

- **Humanized-but-faithful reasoning.** No published recipe produces a CoT that is both fluent and human-sounding and demonstrably faithful to internal computation. Prompt and training communities each optimize one at the expense of the other (B/E).

- **Persona × reasoning co-training.** CrewAI provides persona; DSPy provides optimizable reasoning; R1 provides reasoning RL. No public pipeline jointly trains reasoning ability and a consistent voice. They are parallel tracks that never merge (B gap, C gap).

- **Reasoning-RL for non-math/code domains.** Nearly every R1-style recipe trains on math and code because verification is cheap. Dialogue, empathetic reasoning, creative planning, and argumentation — the core humanization domains — have no equivalent open recipe. PRIME's implicit PRM is the most promising substrate; it is largely untested on conversational data (C gap).

- **Controllable "aha moments."** Repos observe emergent reflection; nobody offers knobs to elicit or suppress it. From a UX perspective, sometimes visible reflection is desirable; sometimes a confident, concise answer is better (C gap, E gap).

- **Register and style transfer for reasoning traces.** Near-zero open work on making the inner monologue sound like a tired engineer vs. an eager grad student. Most work treats reasoning voice as a binary switch (E gap).

- **Humanization-specific reasoning benchmarks.** All major benchmarks test logical correctness (MATH, AIME, GPQA, SWE-bench). No widely adopted open eval measures how humanlike the reasoning trace reads — its variability, hedging, self-talk, emotional register, tangents (C gap).

- **A portable rendering standard for reasoning.** Every vendor ships a different UI. Developers building cross-provider experiences must re-invent the surface (D gap).

- **Cost legibility for thinking.** Anthropic's separately-billed thinking tokens, Lindy's credits, Devin's ACUs, Relevance's Actions — none are easy to predict before a task runs (D gap).

- **Memory × reasoning integration.** LangGraph has long-term memory; reasoning-RL recipes do not train with it in the loop. Humanlike multi-session reasoning is a framework-side scaffolding hack, not a model-side property (C gap).

- **Psycholinguistic evaluation.** Whether model CoT structurally resembles human think-aloud protocols is barely studied. This is a direct gap the Unslop project could exploit (A gap).

- **Sycophancy × reasoning interaction.** CoT can mask sycophancy. No frontier lab has published a joint reasoning + sycophancy study (B gap).

---

## How This Category Fits

Humanizing AI output has two layers: what the model says (surface voice, prose, register) and what the model appears to be thinking (the reasoning trace). Most of the Unslop research stack addresses the first. Category 06 is about the second — and it is now the more leveraged one. By 2026 most frontier models ship a reasoning mode that users see before seeing the final answer. Humanization work that ignores that pass operates downstream of a surface users are already forming opinions about.

This category intersects most directly with evaluation and benchmarking (what would a humanness-of-reasoning eval look like?), persona and voice design (how does persona shape CoT style, not just final-answer style?), and sycophancy/safety research (CoT can both reveal and hide misalignment). It also touches interpretability and alignment — Anthropic's faithfulness work and the H-CoT jailbreak paper both originate here and have consequences throughout the stack.

The industry's canonical pattern is already structurally "humanize the reasoning": DeepSeek-R1's cold-start SFT, OpenAI's CoT summarization, Anthropic's un-character-trained thinking block with the caveat that raw thoughts read less personal — all are explicit acknowledgments that raw reasoning reads machine-like and must be transformed. Unslop is the generalization of that pattern to prose output.

---

## Recommended Reading Order

1. Wei et al. 2022 — CoT (arXiv:2201.11903). Set the historical baseline; understand what "showing reasoning" originally meant.
2. Jay Alammar — "The Illustrated DeepSeek-R1." How the current wave was built; verifiability + readability-SFT pattern.
3. OpenAI — "Learning to Reason with LLMs" (Sep 2024). The o1 frame; rationale for hidden CoT; "think before you speak" as a product metaphor.
4. Anthropic — "Claude's extended thinking" (Feb 2025). The visible-CoT design choice; why the thinking block reads "detached and less personal-sounding."
5. Anthropic — "Reasoning models don't always say what they think" (Apr 2025). Faithfulness numbers on live models; the post-rationalization problem.
6. Meincke, Mollick et al. — "The Decreasing Value of CoT in Prompting" (Jun 2025). The empirical study that closes the "should I add CoT prompts?" debate for reasoning-tier models.
7. Turpin et al. 2023 (arXiv:2305.04388) + arXiv 2503.08679 (Mar 2025). The academic grounding for why visible CoT can mislead, plus current production-model faithfulness rates.
8. Karpathy on GPT-4.5 (Feb 2025). The IQ-vs-EQ split — essential framing for where humanization actually lives.
9. Lilian Weng — "Why We Think" (May 2025). Dual-process + latent-variable synthesis; sequential revision fragility without external feedback.
10. Muennighoff et al. — s1: Simple Test-Time Scaling (arXiv:2501.19393, EMNLP 2025). Budget forcing with "Wait" tokens; the cleanest operationalization of human-style hesitation as an inference signal.
11. Korbak et al. — Chain of Thought Monitorability (arXiv:2507.11473, Jul 2025). Why visible CoT is a fragile safety surface; how "sounds human" and "is monitorable" are not the same axis.
12. Angle E practical threads — specifically: "reasoning as drawback" (r/LocalLLaMA), "AI internal monologues" (r/ChatGPT), Cognitive Mesh Protocol, "Prompting o1" (Cognition Labs), llama.cpp reasoning budget, Wharton report. These translate the academic and industry frames into what practitioners are actually doing today.
