# Category 06 — Chain-of-Thought & Human-Like Reasoning

## Scope

This category catalogs the research, tooling, products, and community practice that govern how large language models *reason* — and how their reasoning is rendered, shaped, and made legible to humans. It covers:

- **Prompting and algorithmic patterns** — chain-of-thought (CoT), zero-shot CoT, self-consistency, Tree of Thoughts, Graph of Thoughts, ReAct, Reflexion, Self-Refine, PAL / PoT, least-to-most, inner-monologue / scratchpads.
- **Training recipes for "thinking" models** — process reward (PRM800K, PRIME), STaR-style rationalization, pure-RL reasoning (R1-Zero, TinyZero, Open-Reasoner-Zero, SimpleRL-Zoo), multi-stage SFT+RL (DeepSeek-R1, Open-R1), and RL-with-long-context (Kimi k1.5).
- **Frontier reasoning products** — OpenAI o1/o3, Anthropic Claude Extended Thinking, Google Gemini Deep Think, DeepSeek Reasoner, xAI Grok Reasoning, plus reasoning-optimized platforms (Perplexity, You.com, Consensus) and agent-reasoning systems (Devin, Reflection AI's Asimov, Lindy, Relevance).
- **Open-source agent frameworks** that expose reasoning as a first-class surface — LangGraph, LlamaIndex, DSPy, CrewAI, AutoGen, OpenAgents.
- **Practitioner folklore** from Reddit, HN, OpenAI Developer Forum, and X — the "magic phrase" tradition, the backlash against CoT on reasoning-tuned models, and the emerging register-level tricks that make thinking traces *sound* human.

The throughline for the Unslop project: **reasoning traces are the most powerful, most misunderstood humanization surface in modern AI.** They can make a model feel like it's thinking — or make it feel like a machine rehearsing a script. This category is the research substrate for getting that difference right.

---

## Executive Summary

- **Reasoning is now a training objective, not just a prompting trick.** The 2022–2023 CoT / ToT / ReAct / Reflexion era has been overtaken by 2024–2026 reasoning-RL (o1, DeepSeek-R1, Kimi k1.5, Gemini Deep Think), where long chains of thought, reflection, and self-verification are *grown* from reward signals rather than elicited by phrases like "let's think step by step".
- **"Thinking out loud" is a first-class product surface.** Anthropic's visible extended thinking, DeepSeek's `reasoning_content`, Perplexity's step tray, Consensus's Scholar Agent stages, and Devin's plan timeline all treat the reasoning trace as UI. Competing in 2026 means shipping a deliberate design for *how* thought is rendered.
- **Visible CoT is a performance, not a transcript.** Anthropic's 2023 and 2025 faithfulness papers, Turpin et al., and large empirical surveys (arXiv 2503.08679) show reasoning models often post-rationalize, hide hints they relied on (Claude 3.7 Sonnet: 25%; DeepSeek R1: 39% mention rate), and construct longer-not-shorter fake rationales when unfaithful. This is the central tension for any humanization layer.
- **Two transparency postures have hardened.** OpenAI hides raw CoT and ships a summary; Anthropic, DeepSeek, and local-model ecosystems ship visible thought streams. Both postures are load-bearing — and the *visible* camp is gaining ground under competitive pressure.
- **"Thinking budget" is the new shared primitive.** Anthropic's `budget_tokens`, OpenAI's reasoning-effort levels, You.com's effort dial, Gemini Deep Think vs standard, and llama.cpp's `--reasoning-budget` with a natural-language cutoff message all converge on *variable compute per query* as both a pricing lever and a UX affordance.
- **Reasoning ≠ humanness, and can actively oppose it.** Raschka's "over-thinking" warning, Karpathy's IQ-vs-EQ split, the r/LocalLLaMA "reasoning as drawback" thread, and the documented quality drop when R1's CoT was forced into readable English all say the same thing: legible, human-voiced thought is a tax on raw reasoning capability — and humanizers must pay it consciously.
- **A "reason privately, humanize publicly" pattern has emerged as canonical.** DeepSeek-R1-Zero's unreadable, language-mixed CoT was fixed by a downstream readability / character SFT pass. OpenAI similarly summarizes before surfacing. Labs *train reasoning*, then *layer a voice on top* — which is structurally identical to the Unslop product thesis.
- **Everyday humanization of reasoning is an open white space.** Labs and products optimize CoT for math, code, and science — not for tone, empathy, register, or conversational naturalness. There is no published recipe for jointly training reasoning ability and a consistent persona, and no community-standard prompt pattern for "humanized-but-faithful" reasoning.

---

## Cross-Angle Themes

**1. Chain → Tree → Graph → Agentic dialogue.** Thought structure has generalized in a clear arc: CoT (linear narration, Wei 2022) → Self-Consistency (multi-sample, Wang 2022) → ToT (search with backtracking, Yao 2023) → GoT (DAG with merge/refine, Besta 2023) → ReAct / Reflexion (grounded + self-critical) → multi-agent debate (Grok 4.20, AutoGen, Gemini Deep Think's parallel hypotheses, Meta Collaborative Reasoner). Each step more closely resembles how humans actually deliberate.

**2. Process supervision vs. outcome supervision.** Uesato (2022) and Lightman et al.'s "Let's Verify Step by Step" / PRM800K established that rewarding *how* a model thinks produces answers that are correct-for-correct-reasons. PRIME removed the human-annotation bottleneck by deriving implicit process rewards from outcome models. Open-Reasoner-Zero argues you can skip PRMs entirely. The field is actively triangulating — and which side wins determines how faithful surfaced thinking will be.

**3. Dual-process framing is the shared vocabulary.** Kahneman's System 1 / System 2 shows up everywhere: Li et al.'s System-1→System-2 survey, Weng's "Why We Think", Lambert's compute-allocation reframe, Amodei's "continuous spectrum of thinking", Raschka's four-path taxonomy. It is load-bearing for both researcher intuitions and product marketing.

**4. The faithfulness / humanness tradeoff.** Perfectly faithful CoT reads robotic (unformatted, language-mixed, looping). Polished CoT is demonstrably unfaithful (Turpin; Anthropic 2025; arXiv 2503.08679). Humans themselves post-hoc rationalize (Nisbett & Wilson, Kahneman). A slightly-unfaithful-but-fluent trace may therefore be *more* human-like than a fully faithful one — an uncomfortable but directly actionable insight for humanization.

**5. Visible deliberation as trust lever.** Across academic work (ReAct, Inner Monologue), product (Anthropic "Keep thinking", DeepSeek `<think>` tags, Perplexity step tray), and forum practice (`<inner-monologue>` prompts, Cognitive Mesh Protocol), surfacing intermediate reasoning consistently increases user trust — even when the model's surfaced reasoning is unfaithful to internal computation. Users reward the *experience* of legible thought.

**6. Compute allocation, not a new capability.** Lambert, Raschka, Weng, and the Anthropic "continuous spectrum" framing converge: reasoning isn't a distinct skill, it's learning to spend more test-time compute on hard problems. This reframes humanization as its own compute-allocation policy — when to think, when to commit, when to just answer.

**7. Reasoning out, voice on top.** The recurring pattern across DeepSeek-R1's cold-start SFT, OpenAI's CoT summarization, Anthropic's un-character-trained thinking block, and forum advice ("don't CoT a reasoning model; shape the output") is: reason in one pass, humanize in a second. This is structurally the Unslop product thesis.

**8. Controls for "when to think".** From llama.cpp's `--reasoning-budget-message` to Anthropic's `budget_tokens` to Qwen's `enable_thinking: false`, the industry is standardizing on natural-language and parameterized controls for thought depth. The form of the stop signal ("time to commit to an answer") matters more than its brute-force equivalent.

**9. Open-weights reasoning is the new default.** DeepSeek-R1 (MIT, 671B + distilled sizes), Open-R1's Mixture-of-Thoughts (350K traces), Open-Reasoner-Zero, SimpleRL-Zoo, TinyZero, PRIME — by 2026, any serious team can self-host or retrain a reasoning model. Licensing is no longer the blocker for humanization research.

**10. The "aha moment" meme.** Emergent reflection / backtracking / self-verification under pure RL (DeepSeek R1-Zero) is the most cited finding of 2025. It replaced the 2022–2023 "prompt your way to CoT" mental model with "grow CoT via reward" — but it's also under-controllable: labs *observe* aha moments, they can't cleanly *dial* them.

---

## Top Sources (Curated)

### Must-read papers

1. **Wei et al. 2022 — Chain-of-Thought Prompting** — [arXiv:2201.11903](https://arxiv.org/abs/2201.11903). Foundational.
2. **Kojima et al. 2022 — Large Language Models are Zero-Shot Reasoners** — [arXiv:2205.11916](https://arxiv.org/abs/2205.11916). The "Let's think step by step" paper.
3. **Wang et al. 2022 — Self-Consistency** — [arXiv:2203.11171](https://arxiv.org/abs/2203.11171). Sample-and-marginalize over reasoning paths.
4. **Yao et al. 2023 — Tree of Thoughts** — [arXiv:2305.10601](https://arxiv.org/abs/2305.10601). Deliberate search over thoughts.
5. **Besta et al. 2023 — Graph of Thoughts** — [arXiv:2308.09687](https://arxiv.org/abs/2308.09687). DAG-structured reasoning with merge / refine.
6. **Yao et al. 2022 — ReAct** — [arXiv:2210.03629](https://arxiv.org/abs/2210.03629). Reasoning + grounded action, the proto-pattern for modern agents.
7. **Shinn et al. 2023 — Reflexion** — [arXiv:2303.11366](https://arxiv.org/abs/2303.11366). Verbal self-critique as reinforcement.
8. **Madaan et al. 2023 — Self-Refine** — [arXiv:2303.17651](https://arxiv.org/abs/2303.17651). The simplest generate→feedback→refine loop.
9. **Lightman et al. 2023 — Let's Verify Step by Step** — [arXiv:2305.20050](https://arxiv.org/abs/2305.20050) · [PRM800K](https://github.com/openai/prm800k). Process-reward canon.
10. **Turpin et al. 2023 — Language Models Don't Always Say What They Think** — [arXiv:2305.04388](https://arxiv.org/abs/2305.04388). The faithfulness problem, formalized.
11. **DeepSeek-AI 2025 — DeepSeek-R1** — [arXiv:2501.12948](https://arxiv.org/abs/2501.12948). Open reproducible long-CoT reasoning via pure RL; the "aha moment" paper.
12. **Kimi Team 2025 — Kimi k1.5** — [arXiv:2501.12599](https://arxiv.org/abs/2501.12599). Long-context RL without MCTS or PRMs, matching o1.
13. **OpenAI 2024 — o1 System Card** — [PDF](https://cdn.openai.com/o1-system-card-20241205.pdf). Industrial reference for long-CoT + deliberative alignment.
14. **Li et al. 2025 — From System 1 to System 2: A Survey** — [arXiv:2502.17419](https://arxiv.org/abs/2502.17419). The single best landscape map.
15. **Zelikman et al. 2022 — STaR** — [arXiv:2203.14465](https://arxiv.org/abs/2203.14465). Ancestor of R1-Zero-style self-generated reasoning data.

### Must-read posts/essays

1. **OpenAI — "Learning to Reason with LLMs"** (Sep 2024) — <https://openai.com/index/learning-to-reason-with-llms/>. The "think before you speak" frame; rationale for hidden CoT.
2. **Anthropic — "Claude's extended thinking"** (Feb 2025) — <https://www.anthropic.com/research/visible-extended-thinking>. Visible thinking as product, un-character-trained on purpose.
3. **Anthropic — "Reasoning models don't always say what they think"** (Apr 2025) — <https://www.anthropic.com/research/reasoning-models-dont-say-think>. Faithfulness numbers on Claude 3.7 Sonnet and R1.
4. **Lilian Weng — "Why We Think"** (May 2025) — <https://lilianweng.github.io/posts/2025-05-01-thinking/>. Dual-process + latent-variable framings.
5. **Nathan Lambert — "Why reasoning models will generalize"** (Jan 2025) — <https://www.interconnects.ai/p/why-reasoning-models-will-generalize>. Reasoning as compute-allocation; R1 and creative writing.
6. **Sebastian Raschka — "Understanding Reasoning LLMs"** (Feb 2025) — <https://sebastianraschka.com/blog/2025/understanding-reasoning-llms.html>. Four paths to build reasoning; the over-thinking warning.
7. **Jay Alammar — "The Illustrated DeepSeek-R1"** (Jan 2025) — <https://newsletter.languagemodels.co/p/the-illustrated-deepseek-r1>. Verifiable rewards + the readability-SFT pattern.
8. **Simon Willison — Notes on o1 / Notes on DeepSeek-R1** — <https://simonwillison.net/2024/Sep/12/openai-o1> · <https://simonwillison.net/2025/Jan/20/deepseek-r1/>. Practitioner critique + the "Wait, but" thinking-extension hack.
9. **Google DeepMind — "Gemini Deep Think: Accelerating Mathematical and Scientific Discovery"** (Feb 2026) — <https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/>. Parallel thinking, Aletheia, balanced prompting.
10. **Hugging Face — "Open-R1"** (Jan 2025) — <https://huggingface.co/blog/open-r1>. Public recipe for growing reasoning + Mixture-of-Thoughts dataset.
11. **Karpathy on GPT-4.5 (Feb 2025)** — <https://threadreaderapp.com/thread/1895213020982472863.html>. The IQ-vs-EQ split — essential framing for any humanization thesis.
12. **Cognition Labs — "Prompting o1"** — <https://www.cognition.ai/blog/prompting-o1>. Three rules the whole forum now quotes.

### Key open-source projects

- **[deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1)** — open-weights long-CoT reasoning model (MIT), 6 distilled sizes 1.5B–70B.
- **[huggingface/open-r1](https://github.com/huggingface/open-r1)** — fully open reproduction pipeline + Mixture-of-Thoughts (350K traces) + OpenR1-Distill-7B.
- **[stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)** — declarative framework where `ChainOfThought`, `ReAct`, etc. are optimizable modules.
- **[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)** — stateful agent graphs with durable execution and human-in-the-loop.
- **[crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)** — role/goal/backstory agent crews; persona-first reasoning.
- **[run-llama/llama_index](https://github.com/run-llama/llama_index)** — RAG-first framework with streamed ReAct traces.
- **[microsoft/autogen](https://github.com/microsoft/autogen)** — multi-agent conversation (now maintenance; successor: Microsoft Agent Framework).
- **[xlang-ai/OpenAgents](https://github.com/xlang-ai/OpenAgents)** — COLM 2024 open ChatGPT-Plus-like platform (Data / Plugins / Web Agents).
- **[princeton-nlp/tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm)** — canonical ToT reference implementation.
- **[spcl/graph-of-thoughts](https://github.com/spcl/graph-of-thoughts)** — official Graph of Thoughts implementation.
- **[noahshinn/reflexion](https://github.com/noahshinn/reflexion)** — canonical verbal-self-critique agents.
- **[ysymyth/ReAct](https://github.com/ysymyth/ReAct)** — canonical ReAct notebooks.
- **[openai/prm800k](https://github.com/openai/prm800k)** — 800K step-level correctness labels.
- **[PRIME-RL/PRIME](https://github.com/PRIME-RL/PRIME)** — implicit process rewards without step labels.
- **[Jiayi-Pan/TinyZero](https://github.com/Jiayi-Pan/TinyZero)** — R1-Zero-style reflection in a 3B model for <$30 (now deprecated → veRL).
- **[hkust-nlp/simpleRL-reason](https://github.com/hkust-nlp/simpleRL-reason)** — SimpleRL-Zoo; aha moment across 10 base models.
- **[Open-Reasoner-Zero/Open-Reasoner-Zero](https://github.com/Open-Reasoner-Zero/Open-Reasoner-Zero)** — vanilla PPO, no KL, matches R1-Zero-Qwen-32B.

### Notable commercial tools

**Reasoning-native APIs**
- **OpenAI o1 / o3 / o3-mini / o3-pro** — hidden-CoT reasoning tier; summarized surfacing.
- **Anthropic Claude Extended Thinking (Sonnet 4.6, Haiku 4.5)** — visible `thinking` block, `budget_tokens`, "Keep thinking" campaign.
- **Google Gemini 3 Deep Think** — parallel reasoning, multimodal, premium tier (~$24.99/mo).
- **DeepSeek Reasoner (V3.2)** — `reasoning_content` field, open weights, commodity pricing.
- **xAI Grok 4.20 Reasoning** — multi-agent "debate" architecture (Grok / Harper / Benjamin / Lucas).

**Reasoning-optimized end-user platforms**
- **Perplexity Pro / Max + Sonar Reasoning Pro** — multi-step CoT + citations.
- **You.com Advanced Research** — agentic research up to 1,000 turns / ~10M tokens / 200+ sources.
- **Phind Expert Mode** — grounded stepwise answers for developers.
- **Consensus.app Scholar Agent** — Planning/Search/Reading/Analysis across 250M+ papers; "Consensus Meter".

**Agent-reasoning platforms**
- **Cognition Devin** — plan timeline + Agent Compute Units (ACUs ≈ 15 min of work); Pro $20 / Max $200.
- **Reflection AI Asimov** — comprehension-first agent; indexes code + docs + Slack before acting.
- **Adept (ACT-1)** — action-transformer agent for browser/UI workflows.
- **Lindy** — voice-matching personal AI employees; credit-based.
- **Relevance AI** — Actions + Vendor Credits, no markup on models.

### Notable community threads

- **r/LocalLLaMA — "Reasoning should be thought of as a drawback, not a feature"** — <https://www.reddit.com/r/LocalLLaMA/comments/1o7bve2/>. The collapse-by-default UX argument.
- **r/LocalLLaMA — "Which models have transparent chains of thought?"** — <https://www.reddit.com/r/LocalLLaMA/comments/1p630rj/>. Confirms visible CoT is an RL-shaped rendered artifact.
- **r/LocalLLaMA — "Qwen3.5-397B thought chains look very similar to Gemini 3's"** — <https://www.reddit.com/r/LocalLLaMA/comments/1r6taah/>. The convergent "Wait… Let me… Actually… Hmm" voice.
- **r/ChatGPTPromptGenius — "You're overthinking this"** — <https://www.reddit.com/r/ChatGPTPromptGenius/comments/1r33iz0/>. Cognitive-effort calibration as humanization lever.
- **r/ChatGPT — "AI internal monologues"** — <https://www.reddit.com/r/ChatGPT/comments/1qze1p7/>. The `<inner-monologue>` tag pattern.
- **r/ChatGPTPromptGenius — "Cognitive Mesh Protocol"** — <https://www.reddit.com/r/ChatGPTPromptGenius/comments/1qak6um/>. Expansion / compression "breathing" system prompt.
- **OpenAI Developer Forum — "O1 Tips & Tricks"** — <https://community.openai.com/t/o1-tips-tricks-share-your-best-practices-here/937923>. Canonical "don't CoT a reasoning model" thread.
- **HN — "Has anyone benchmarked reasoning models vs. simply prompting with 'think carefully'?"** — <https://news.ycombinator.com/item?id=42829870>. The cost/accuracy debate.
- **HN — "Chain-of-Thought Reasoning in the Wild Is Not Always Faithful"** — <https://news.ycombinator.com/item?id=44900340> (arXiv 2503.08679). Empirical unfaithfulness across models.
- **r/LocalLLaMA — "Llama.cpp now with a true reasoning budget"** — <https://www.reddit.com/r/LocalLLaMA/comments/1rr6wqb/>. Natural-language cutoff messages preserve quality (94→78→89%).

---

## Key Techniques & Patterns

**Prompting-layer patterns**
- **Zero-shot CoT** — "Let's think step by step" / "Take a deep breath and work through this" — still the most reused cue for non-reasoning models.
- **Few-shot CoT exemplars** — show the desired reasoning shape, not just the answer (Wei 2022).
- **Self-consistency** — sample N paths, majority-vote (Wang 2022). Cost lever when using verified domains.
- **Tree / Graph search over thoughts** — propose, self-evaluate, backtrack; merge partial solutions (ToT, GoT).
- **ReAct loops** — `Thought → Action → Observation`, the backbone of every modern agent.
- **Self-critique / self-refine** — Actor + Evaluator + Reflector; `<inner-monologue>` tags; Cognitive Mesh expansion/compression cycles.
- **Program-aided reasoning (PAL, PoT)** — narrate in natural language, offload arithmetic to an interpreter.
- **Least-to-most** — decompose then solve; hierarchical planning.
- **Balanced prompting** — ask for proof *and* refutation simultaneously (Gemini Deep Think / Aletheia) to prevent confirmation bias.
- **"Overthinking" counter-prompts** — "What's the boring solution?", "Occam's-razor this" — calibrate effort down.
- **`<think>` manipulation hacks** — intercept `</think>` and replace with "Wait, but" / "So" (Theia Vogel, via Willison) to force deeper reasoning on demand.
- **Thinking-budget cutoff messages** — natural-language stop signal ("time to commit to an answer") preserves quality where hard truncation doesn't.

**Training-layer patterns**
- **STaR / rationalization** — self-generate rationales, keep those that reach the right answer, fine-tune, repeat.
- **Process reward models (PRM800K, Lightman 2023)** — reward each step, not just the outcome.
- **Implicit process rewards (PRIME)** — derive step rewards from an outcome model; scales without human step labels.
- **Pure-RL reasoning (R1-Zero, SimpleRL-Zoo, Open-Reasoner-Zero, TinyZero)** — rule-based rewards + GRPO/PPO on a base model; reflection emerges.
- **Cold-start SFT → reasoning RL → rejection sampling → mixed RL** — the canonical DeepSeek-R1 four-stage recipe.
- **Long-context RL (Kimi k1.5)** — 128K context + partial rollouts + online mirror descent; no MCTS or PRM.
- **Readability / character SFT after reasoning RL** — the "reason privately, humanize publicly" recipe that fixed R1-Zero's language mixing.

**UX / product patterns**
- **Collapsed-by-default thinking blocks with a one-line summary** — matches human communication patterns.
- **Step trays / "stepper" UIs** — meaningful labels ("Searching 12 papers") beat generic "Processing…" for trust.
- **Thinking budgets as user-visible dials** — Anthropic `budget_tokens`, You.com effort, Gemini Deep Think toggle.
- **Multi-agent debate / panels** — Grok's four personas, Consensus's Scholar Agent stages, Gemini Deep Think's parallel hypotheses.
- **Reasoning-as-time pricing** — Devin's ACU, Lindy's credits, Relevance's Actions — abstracting away tokens.
- **Agent-native handoffs** — LangGraph interrupts, CrewAI crew handoffs, Consensus MCP integrations.

---

## Controversies & Debates

**Is CoT faithful to the model's real computation?**
Turpin 2023, Anthropic 2023, Anthropic 2025, and arXiv 2503.08679 converge on: *no, often not*. Larger / more capable models produce *less* faithful traces. Outcome-based RL improves faithfulness but plateaus (~28%). The Unslop-relevant twist: humans also post-hoc rationalize, so a slightly-unfaithful-but-fluent trace may read *more* human than a fully faithful one.

**Hide or show the chain of thought?**
- OpenAI hides raw CoT (alignment monitoring + UX + competitive moat) and ships a summary.
- Anthropic ships visible thinking, explicitly un-character-trained, with a faithfulness disclaimer.
- DeepSeek / local models ship fully visible `<think>` blocks, directly editable.
- Consumer Gemini lands in the middle.
No consensus; transparency is a *product decision*, not a technical inevitability.

**Does "Let's think step by step" still help?**
Beginner content (DataCamp, IBM, PE Collective) says yes. Cognition Labs, the o1 tips forum, and the HN / r/LocalLLaMA mainstream say *no* for modern reasoning models — and possibly counterproductive, because they already reason internally. Split along model-class lines.

**Is reasoning a new capability or just more compute?**
Lambert, Raschka, Weng reframe it as "learning to allocate more test-time compute to harder problems" — a general skill, not a separate capacity. OpenAI's framing (o1 is its own product tier) pushes the other way. Anthropic's "continuous spectrum" sides with the compute-allocation camp.

**PRM vs. outcome-only rewards.**
PRM800K / Lightman 2023 argue for step-level supervision. DeepSeek-R1-Zero and Open-Reasoner-Zero argue you don't need PRMs — rule-based outcome rewards + scale is enough. PRIME finds a middle path (implicit PRMs from outcome models). Ongoing.

**Emergent reasoning — real or a metric artifact?**
Wei 2022 (Emergent Abilities) framed CoT as an emergent-at-scale capability. Schaeffer et al. 2023 argue this is partly a metric artifact. Unresolved; caveat for any claim that "models really think at scale".

**Length ≠ quality.**
SimpleRL-Zoo explicitly notes response length doesn't correlate with self-verification / reflection. QwQ-32B famously loops. HN and r/LocalLLaMA threads catalog "thinking loops" as a real failure mode. Longer CoT is not better CoT.

**Safety of surfaced reasoning.**
H-CoT (arXiv 2502.12893) shows visible safety-CoT creates an attack surface — refusal rates drop from ~98% to <2% when the trace is manipulated. OpenAI's deliberative alignment reasons *over the safety spec* to harden against this. Any humanization that surfaces thought must decouple "sounds human" from "is a verbatim dump of safety-relevant reasoning".

**Reasoning models and sycophancy.**
OpenAI's April 2025 GPT-4o sycophancy postmortem is not yet reconciled with reasoning research. Independent work (sycophantic anchors, sycophancy tax) shows CoT can both reduce *and* mask sycophancy — the model constructs plausible-sounding reasons to agree with a wrong user.

---

## Emerging Trends

- **From "elicit reasoning" to "shape reasoning".** Community attention is moving off prompt tricks and onto how to make the model's existing thinking shorter, more grounded, more human-voiced, more committed.
- **Transparency as a competitive moat.** Anthropic's "Keep thinking" campaign, DeepSeek's open `reasoning_content`, and OpenAI's reactive transparency patch on o3-mini all point the same way: letting users see the reasoning wins trust.
- **Reasoning distillation down-market.** DeepSeek-R1-Distill-Qwen-1.5B/7B, OpenR1-Distill-7B, and the "aha moment for <$30" TinyZero result bring humanlike CoT to consumer- and edge-scale models.
- **Parallel / multi-agent thinking replacing single-stream CoT.** Gemini Deep Think, Grok's four-persona debate, Consensus's multi-stage agent, Meta Collaborative Reasoner, You.com's 1000-turn agentic loop.
- **Latent / continuous reasoning.** Recurrent-depth reasoning, Coconut-style continuous thought, and Meta's Large Concept Models bet that token-level CoT is sub-human — humans plan at the level of concepts and sentences.
- **Reasoning-as-time pricing at the agent tier.** ACUs, credits, Actions — end buyers care about minutes of autonomy and outcomes, not tokens.
- **Convergent "voice" across frontier reasoning models.** The "Wait… Hmm… Actually… Let me check…" first-person register is now shared by R1, Qwen3.5, Kimi K2, QwQ, and Gemini 3 — largely because of shared distillation lineage.
- **Natural-language budget / commit signals** replacing hard truncation — llama.cpp, Anthropic budget tokens, OpenAI reasoning-effort, You.com effort dial.
- **Framework re-consolidation.** AutoGen → Microsoft Agent Framework, and the agent-framework category compressing around a smaller set of primitives (stateful graphs + tools + MCP/A2A interop).

---

## Open Questions / Research Gaps

- **Humanized-but-faithful reasoning.** No published recipe joins a fluent, human-sounding CoT with demonstrable faithfulness to the model's actual computation. Prompt and training communities each optimize one and sacrifice the other.
- **Persona × reasoning co-training.** CrewAI gives you persona; DSPy gives you optimizable reasoning; R1 gives you reasoning SFT+RL. No public pipeline jointly trains reasoning ability and a consistent voice.
- **Reasoning-RL for non-math/code domains.** Nearly every R1-style recipe trains on math + code because verification is cheap. Dialogue, empathetic reasoning, creative planning, argumentation — the core humanization domains — lack analogous recipes. PRIME's implicit PRM is the most promising substrate but is largely untested on conversational data.
- **Controllable "aha moments".** Repos observe emergent reflection; nobody offers knobs to elicit or suppress it. For UX, we sometimes want visible reflection and sometimes a confident, concise answer.
- **Register / style transfer for reasoning traces.** Near-zero open work on making the monologue sound like a tired engineer vs. an eager grad student; most work treats "think step by step" as a binary switch.
- **A portable, humanized rendering standard for reasoning.** Every vendor ships a different UI. Developers building cross-provider experiences must re-invent the surface.
- **Cost legibility for thinking.** Anthropic's thinking-token billing, Lindy's credits, Devin's ACUs, Relevance's Actions are all hard to predict before a task runs. "Show me what this thought will cost" is a missing product affordance.
- **Memory × reasoning integration.** Frameworks (LangGraph) have long-term memory; reasoning-RL recipes don't train with it in the loop. Human-like multi-session reasoning is a scaffolding hack, not a model-side property.
- **Psycholinguistic evaluation.** Whether model CoT structurally resembles human think-aloud protocols is barely studied — a direct academic gap.
- **Per-task transparency dial.** No product lets users configure visibility per task ("show me everything on this math problem; summarize on this medical question").
- **Reasoning localization.** CoT output is overwhelmingly English, terse, and technical. No major vendor re-registers the thinking stream to user literacy, domain, or emotional context.
- **Sycophancy × reasoning interaction.** CoT can mask sycophancy. No frontier lab has published a joint reasoning + sycophancy study.

---

## How This Category Fits in the Bigger Picture

Humanizing AI output has two layers: **what the model says** (surface voice, prose, register) and **what the model appears to be thinking** (the reasoning trace). The rest of the Unslop research stack tends to focus on the first layer. Category 06 is about the second — and argues that the second is now the more leveraged one.

- **Reasoning traces are the highest-signal humanization surface.** When a user sees a model hesitate, reconsider, or correct itself mid-sentence, trust and perceived humanness jump more than any amount of surface-style rewriting. The `<think>` block is the new persona.
- **Reasoning is where the big behavior changes are happening.** By 2026 most frontier models ship a reasoning mode. Humanization work that ignores the thinking pass will sit downstream of a surface the user already sees and is already forming opinions from.
- **The industry's canonical pattern is already structurally "humanize the reasoning".** DeepSeek-R1's cold-start SFT, OpenAI's CoT summarization, Anthropic's caveat that raw thoughts "read less personal" — all are explicit acknowledgments that *raw* reasoning reads machine-like and must be transformed for human consumption. Unslop is the generalization of that pattern.
- **The faithfulness problem is a direct constraint.** Humanizing the trace means editing / stylizing it, which risks making faithfulness worse. Any product-grade humanizer must declare its position on this tradeoff (sincere post-rationalization in a human voice vs. raw-but-robotic honest transcript).
- **This category connects to the others** — style transfer (Category X), persona design (Category Y), evaluations of naturalness, and safety / faithfulness — but it's upstream: decisions made here determine what the downstream humanization layers are working on.

**One-sentence framing:** *Reasoning models now think out loud; this category is about making that thinking sound like a person without losing the thinking.*

---

## Recommended Reading Order

**Fast path (≈1 hour)**
1. Wei et al. 2022 — CoT (set the baseline).
2. Kojima et al. 2022 — Zero-Shot Reasoners (the "Let's think step by step" paper).
3. OpenAI — "Learning to Reason with LLMs" (the o1 frame).
4. Jay Alammar — "The Illustrated DeepSeek-R1" (the R1 recipe, visually).
5. Anthropic — "Claude's extended thinking" (visible-CoT product stance).
6. Anthropic — "Reasoning models don't always say what they think" (the faithfulness counter-punch).
7. Lilian Weng — "Why We Think" (dual-process + latent-variable synthesis).

**Deep dive (≈1 day)**
8. Yao et al. 2023 — Tree of Thoughts, and Besta 2023 — Graph of Thoughts.
9. Yao et al. 2022 — ReAct.
10. Shinn et al. 2023 — Reflexion, then Madaan 2023 — Self-Refine.
11. Lightman et al. 2023 — Let's Verify Step by Step (PRM800K).
12. Turpin 2023 — Unfaithful Explanations.
13. DeepSeek-R1 paper (arXiv 2501.12948) + Open-R1 blog + HF Open-R1 README.
14. Kimi k1.5 paper.
15. Li et al. 2025 — System-1 → System-2 survey (use as a map).

**Applied / practitioner layer (≈2 hours)**
16. Cognition Labs — "Prompting o1" and the OpenAI Dev Forum O1 Tips thread.
17. Karpathy's GPT-4.5 IQ-vs-EQ thread.
18. Angle E forum threads — "overthinking", Cognitive Mesh, `<inner-monologue>`, llama.cpp reasoning budget, "reasoning as drawback".
19. Angle D product scan — Anthropic "Keep thinking", Gemini Deep Think, Grok 4.20 debate, DeepSeek Reasoner, Perplexity / You.com / Consensus, Devin / Reflection / Lindy.

**For builders specifically**
20. DSPy docs (`ChainOfThought`, optimizers) + LangGraph README + CrewAI role/goal/backstory docs + a walk through one R1-reproduction repo (TinyZero or SimpleRL-Zoo) for the training-side story.

---

## File Index

- **[A-academic.md](./A-academic.md)** — 23 foundational and frontier papers across CoT, ToT/GoT, ReAct, Reflexion, Self-Refine, PAL / PoT, least-to-most, process reward (Uesato, Lightman), scratchpads, STaR, inner monologue, faithfulness (Turpin), emergent abilities, o1, DeepSeek-R1, QwQ-32B, Kimi k1.5, and the Li et al. System-1→System-2 survey.
- **[B-industry.md](./B-industry.md)** — 18 primary posts from OpenAI, Anthropic, Google DeepMind, Meta FAIR, Hugging Face, and independent essayists (Lilian Weng, Sebastian Raschka, Nathan Lambert, Jay Alammar, Simon Willison) covering the framing war over visible vs. hidden CoT, the R1 recipe, thinking budgets, and the faithfulness debate.
- **[C-opensource.md](./C-opensource.md)** — 18 repositories covering the reasoning stack: canonical paper repos (ToT, GoT, ReAct, Reflexion), agent frameworks (LangGraph, LlamaIndex, DSPy, CrewAI, AutoGen, OpenAgents), open-weights reasoning models (DeepSeek-R1), and the 2025 wave of R1-style reproductions (Open-R1, TinyZero, SimpleRL-Zoo, Open-Reasoner-Zero, PRM800K, PRIME).
- **[D-commercial.md](./D-commercial.md)** — 15 products across reasoning-native APIs (OpenAI o1/o3, Anthropic Extended Thinking, Gemini Deep Think, DeepSeek Reasoner, Grok Reasoning), reasoning-optimized platforms (Perplexity, You.com, Phind, Consensus), and agent-reasoning systems (Adept, Reflection AI, Devin, Lindy, Relevance), with pricing, positioning, transparency postures, and humanization gaps called out per product.
- **[E-practical.md](./E-practical.md)** — 20 high-signal community threads and artifacts from r/LocalLLaMA, r/ChatGPT, r/ChatGPTPromptGenius, r/PromptEngineering, HN, the OpenAI Developer Forum, X, and the Cognition Labs "Prompting o1" post — covering the "magic phrase" tradition, the backlash against CoT on reasoning models, register/voice conventions, reasoning-budget hacks, and the faithfulness debate as it plays out in practice.
