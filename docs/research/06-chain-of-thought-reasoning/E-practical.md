# 06-Chain-of-Thought & Reasoning — Angle E: Practical How-Tos & Forums

**Project:** Humanizing AI output and thinking
**Angle:** Reddit / HN / Twitter-X / YouTube / Discord — practical CoT prompts, test-time compute, reasoning-model tips
**Date compiled:** 2026-04-19

---

## Summary

**Research value: high** — Community discussion on CoT has matured into two opposing camps: (1) the "magic phrase" tradition ("let's think step by step", "take a deep breath", "show your work") still widely taught in r/ChatGPTPromptGenius, r/PromptEngineering, and YouTube, and (2) a growing backlash from r/LocalLLaMA, HN, and the OpenAI Developer Forum arguing that explicit CoT is counterproductive on modern reasoning models (o1/o3/R1/Gemini Deep Think) and that the visible "thinking" is *not* faithful to the model's actual computation. For a humanization project, the key tension is that visible reasoning traces are often stylized performances ("fanfic", "confidence theater") rather than authentic thought — which is both a *risk* (fake introspection reads as robotic) and an *opportunity* (deliberately styling the trace to sound human-like is tractable as a prompt pattern).

---

## High-signal posts

### 1. "Reasoning should be thought of as a drawback, not a feature"
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1o7bve2/reasoning_should_be_thought_of_as_a_drawback_not/
- **Source:** r/LocalLLaMA (2025)
- **Gist:** Contrarian post arguing that visible CoT is a UX liability — adds latency, produces text users don't want, and the presence of reasoning itself shouldn't be taken as valuable. Top comments separate "reasoning as computational technique" (good) from "reasoning as a surface artifact" (bad). Recommends hiding traces by default and expanding only on demand.
- **Humanization takeaway:** Humans don't narrate every thought. Collapse-by-default reasoning UX matches how humans communicate deliberation ("let me think… okay, here's my answer") rather than a 600-token scratchpad.

### 2. "Which models have transparent chains of thought?"
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1p630rj/which_models_have_transparent_chains_of_thought/
- **Source:** r/LocalLLaMA
- **Gist:** Catalog of models with inspectable CoT: DeepSeek, Kimi K2 Thinking, Qwen3.5, Olmo3-Think. Thread emphasizes that "transparent" traces are shaped by RL, not SFT, and are *summaries* of reasoning rather than raw internal computation.
- **Humanization takeaway:** Confirms visible CoT is already a *rendered* artifact — so styling it to sound human is legitimate rather than deceptive.

### 3. "Qwen3.5-397B-A17B thought chains look very similar to Gemini 3's"
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1r6taah/qwen35397ba17b_thought_chains_look_very_similar/
- **Source:** r/LocalLLaMA
- **Gist:** Observation that frontier reasoning models have converged on a common "voice" for CoT — short second-person monologue with "Wait…", "Let me check…", "Actually…", "Hmm…" tokens. Comments trace this to shared distillation lineage from R1.
- **Humanization takeaway:** The "Wait-Let me-Actually-Hmm" pattern is already strongly human-sounding. It's a reusable stylistic template for making non-reasoning models sound deliberative.

### 4. "I told ChatGPT 'you're overthinking this' and it gave me the simplest, most elegant solution"
- **URL:** https://www.reddit.com/r/ChatGPTPromptGenius/comments/1r33iz0/i_told_chatgpt_youre_overthinking_this_and_it/
- **Source:** r/ChatGPTPromptGenius
- **Gist:** Counter-prompt that redirects the model out of "show-off mode". Community confirmed variants: "Simpler", "That's too clever", "What's the boring solution?", "Occam's razor this."
- **Example prompt:**
  ```
  You're overthinking this. What's the boring, Occam's-razor solution?
  ```
- **Humanization takeaway:** Humans signal cognitive effort calibration ("don't overthink it"). Borrowing this register — and having the model *respond* in kind with a short, unshowy answer — is a direct humanization lever.

### 5. "Add 'show your work' to any prompt and ChatGPT actually thinks through the problem"
- **URL:** https://www.reddit.com/r/PromptEngineering/comments/1rr6xi5/add_show_your_work_to_any_prompt_and_chatgpt/
- **Source:** r/PromptEngineering
- **Gist:** "Show your work" appended to any prompt triggers line-by-line reasoning and self-correction mid-explanation. Reports include the model catching its own mistakes — a behavior that reads as humanly honest.
- **Example prompt:**
  ```
  [your question]
  Show your work. If you notice you made an error partway through, correct it out loud and keep going.
  ```
- **Humanization takeaway:** Explicit permission to self-correct mid-trace produces the uniquely human artifact "actually wait, I was wrong about X — let me redo that."

### 6. "Simple AI prompt tricks that make it think like a human"
- **URL:** https://www.reddit.com/r/ChatGPTPromptGenius/comments/1m43b3s/simple_ai_prompt_tricks_that_make_it_think_like_a/
- **Source:** r/ChatGPTPromptGenius
- **Gist:** Collected set of short humanization triggers: "Walk me through your reasoning", "Challenge my assumption that…", "Give me the contrarian view", "What questions should I be asking instead?"
- **Example prompts:**
  ```
  Challenge my assumption that [X]. Steelman the opposite.

  What questions should I be asking instead of the one I just asked?
  ```
- **Humanization takeaway:** Curious counter-questioning and devil's-advocate reframing are human conversational moves that reasoning-tuned models will perform on request but rarely by default.

### 7. "Cognitive Mesh Protocol: A System Prompt for Enhanced AI Reasoning"
- **URL:** https://www.reddit.com/r/ChatGPTPromptGenius/comments/1qak6um/cognitive_mesh_protocol_a_system_prompt_for/
- **Source:** r/ChatGPTPromptGenius
- **Gist:** Community-built system prompt that makes the model track four self-monitoring variables — Coherence, Entropy, Temperature, Grounding — and alternate between "expansion" (5-6 exploratory steps) and "compression" (1-2 synthesis steps). Explicitly flags failure states: Fossil (repetition), Chaos (disconnection), Hallucination risk.
- **Example prompt (excerpted):**
  ```
  Reason in breathing cycles:
  - Expansion (5-6 steps): generate possibilities, explore alternatives
  - Compression (1-2 steps): synthesize and commit
  If you notice repetition, force 3 unexplored alternatives.
  If coherence drops below 0.65, compress to the most important thread.
  If grounding is weak, pause and flag the uncertainty in plain language.
  ```
- **Humanization takeaway:** Explicit "breathing" rhythm (expand → compress) mimics how humans oscillate between divergent and convergent thinking. Naming failure modes in plain language is also a human metacognitive move.

### 8. "AI internal monologues"
- **URL:** https://www.reddit.com/r/ChatGPT/comments/1qze1p7/ai_internal_monologues/
- **Source:** r/ChatGPT
- **Gist:** Discussion of prompting models to emit `<inner-monologue>…</inner-monologue>` tags before answering. OpenAI's own prompt guide endorses the pattern. Community argues the interior voice should be first-person, hesitant, and reference prior turns — not bullet points.
- **Example prompt:**
  ```
  Before answering, write an <inner-monologue> section in first person where
  you think aloud like a person would — hesitations, reconsiderations, and
  references to what was said earlier. Then give the final answer.
  ```
- **Humanization takeaway:** Structural separation between inner voice and final answer is one of the strongest single levers for human-sounding reasoning output.

### 9. "O1 Tips & Tricks: Share Your Best Practices" (OpenAI Developer Forum)
- **URL:** https://community.openai.com/t/o1-tips-tricks-share-your-best-practices-here/937923
- **Source:** OpenAI Developer Community
- **Gist:** Canonical thread with Cognition Labs' observation that "asking o1 to only give the final answer often performs better, since it will think before answering regardless." Community consensus: reasoning models need *dense* context and hate redundant "think step by step" instructions.
- **Example prompt pattern for reasoning models:**
  ```
  [full problem statement, all facts, constraints, and desired output format]
  Give only the final answer in the specified format.
  ```
- **Humanization takeaway:** For models that already reason internally, the humanizing move is to *remove* visible chain-of-thought scaffolding and let the terminal answer carry the deliberation — closer to how experts actually communicate.

### 10. "Prompting o1 & Reasoning Models — Key Tips"
- **URL:** https://o1-prompt-guide.replit.app/
- **Source:** Community-maintained guide (HN-surfaced)
- **Gist:** Codifies the "don't CoT a reasoning model" rule: focus on *output specification*, not methodology. Avoid few-shot examples. Treat o1/o3 as "report generators" not chat partners. Front-load all context.
- **Humanization takeaway:** Decouple "reasoning" from "persona". A reasoning model does its thinking silently; humanization work moves to the *surface style* of the final answer.

### 11. "Has anyone benchmarked reasoning models vs. simply prompting with 'think carefully'?" (HN)
- **URL:** https://news.ycombinator.com/item?id=42829870
- **Source:** Hacker News
- **Gist:** HN debate: adding "think carefully" to Claude Sonnet often matches DeepSeek-R1's accuracy at a fraction of the cost. Skeptics argue reasoning models are "throwing arbitrary compute at a benchmark number" rather than qualitatively reasoning better.
- **Humanization takeaway:** For humanization projects on non-reasoning models, a lightweight "think carefully" prefix plus structured output remains cost-effective — you don't need a reasoning-tier model to get deliberate-sounding output.

### 12. "Scaling up test-time compute with latent reasoning" (HN)
- **URL:** https://news.ycombinator.com/item?id=43004416
- **Source:** Hacker News
- **Gist:** Extended thread on latent vs. token-level reasoning. Key community insight: R1's language-mixing fix (forcing readable English CoT) *degraded* final-answer quality, demonstrating that legible reasoning trades off against raw capability. The "bitter lesson" rephrased: if you ask for X to get Y, you do worse than asking for Y directly.
- **Humanization takeaway:** Readable, human-sounding CoT is already a tax on capability. A humanization project should accept this tradeoff consciously and tune for the right balance, not pretend humanized reasoning is free.

### 13. "qwen3.5:9b thinking loop" + related DeepSeek loop issues
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1rvlu4t/qwen359b_thinking_loop/ (+ https://github.com/deepseek-ai/DeepSeek-V3.2-Exp/issues/46)
- **Source:** r/LocalLLaMA + GitHub
- **Gist:** Reasoning models get stuck in "Wait the source is… New plan… Wait let me check again…" loops. Cause: inductive bias toward temporally correlated errors plus risk aversion from training. Workaround: raise temperature, add a reasoning-budget cutoff message.
- **Humanization takeaway:** Looping is the *opposite* of human reasoning, which naturally de-escalates and commits. Budgeting the trace and forcing a "commit now" move is a humanization-by-subtraction pattern.

### 14. "Llama.cpp now with a true reasoning budget"
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1rr6wqb/llamacpp_now_with_a_true_reasoning_budget/
- **Source:** r/LocalLLaMA
- **Gist:** `--reasoning-budget` + `--reasoning-budget-message` flags in llama.cpp. Without a cutoff message, performance collapses (94% → 78%); with a polite budget message, it recovers to 89%.
- **Example budget message:**
  ```
  … reasoning budget exceeded. Time to commit to an answer.
  ```
- **Humanization takeaway:** Telling a model "time to commit" in natural language is itself a human metacognitive cue. The *form* of the cutoff matters, not just the token count.

### 15. "Can 'thinking' be regulated on Qwen3.5 and other newer LLMs?"
- **URL:** https://www.reddit.com/r/LocalLLaMA/comments/1rpwu3h/can_thinking_be_regulated_on_qwen35_and_other/
- **Source:** r/LocalLLaMA
- **Gist:** Practical tips for toggling reasoning mode via `chat_template_kwargs` (`enable_thinking: false`). Users report StepFun 3.5 and other heavily reasoning-tuned models misbehave when thinking is forced to zero — they try to re-open a second reasoning block.
- **Humanization takeaway:** Reasoning behavior is deeply baked in for some models; humanization by simply turning it off is unreliable. Better to shape the trace than suppress it.

### 16. Andrej Karpathy's GPT-4.5 thread (Feb 27, 2025)
- **URL:** https://threadreaderapp.com/thread/1895213020982472863.html (mirror of x.com/karpathy/status/1895213020982472863)
- **Source:** X / Twitter
- **Gist:** Karpathy frames a useful split for humanization work: **IQ tasks** (math, code, reasoning) benefit from RL/test-time compute. **EQ tasks** (creativity, analogy, humor, world-knowledge nuance) benefit from raw pretraining scale. Pretraining scale-ups (GPT-4→4.5) produce diffuse "everything slightly better" gains — subtler word choice, better humor, fewer hallucinations — which is precisely where humanization wins live.
- **Humanization takeaway:** Humanization ≠ reasoning. They're orthogonal axes. The project should probably not lean on reasoning-tuned models for its EQ layer; it should target models (or modes) whose pretraining-derived "vibes" are strongest.

### 17. H-CoT: Hijacking Chain-of-Thought Safety Reasoning (arXiv + r/singularity surfacing)
- **URL:** https://arxiv.org/html/2502.12893v1
- **Source:** arXiv, discussed on r/singularity and HN
- **Gist:** Exposing or writing the CoT to the user creates an attack surface — refusal rates drop from ~98% to <2% when the reasoning trace is manipulated. OpenAI's "deliberative alignment" response trains models to reason *about* safety specs before answering.
- **Humanization takeaway:** There's a real safety cost to surfacing thought-like text. Any humanization of the visible trace needs to decouple "sounds human" from "is a verbatim dump of the safety-relevant reasoning."

### 18. "Chain-of-Thought Reasoning in the Wild Is Not Always Faithful" (HN discussion)
- **URL:** https://news.ycombinator.com/item?id=44900340 (arXiv 2503.08679)
- **Source:** Hacker News + arXiv
- **Gist:** Empirical unfaithfulness rates across models: GPT-4o-mini 13%, Haiku 3.5 7%, Gemini 2.5 Flash 2.17%, DeepSeek R1 0.37%, Sonnet 3.7 thinking 0.04%. Visible CoT can be post-hoc rationalization rather than the real cause of the answer.
- **Humanization takeaway:** A key *humanization* insight: humans also post-hoc rationalize (see Kahneman, Nisbett & Wilson). A model whose CoT is *slightly* unfaithful but reads as honest-human-reasoning may be more human-like than a perfectly faithful but robotic trace. Fidelity and humanness trade off.

### 19. "The 'Take a Deep Breath' Prompt"
- **URL:** https://guaeca.com/en/blog/take-a-deep-breath-prompt/ (widely reshared on r/ChatGPT and X)
- **Source:** Viral across Reddit/X
- **Gist:** Appending "take a deep breath and think carefully" produced measurable accuracy gains on PaLM-2/early GPT-4 era models (DeepMind "Large Language Models as Optimizers" paper discovered it via automated prompt search). Community has generalized it into a family: "let's reason this out", "let's slow down", "let me think about this for a moment."
- **Example prompt:**
  ```
  Take a deep breath and work through this step by step.
  ```
- **Humanization takeaway:** Emotional/embodied metaphors ("breathe", "slow down") work because they shift register away from crisp-answer mode. Humanization benefits double: better reasoning *and* more human voice.

### 20. "Cognition Labs: Prompting o1" (referenced throughout forums)
- **URL:** https://www.cognition.ai/blog/prompting-o1 (resurfaced in OpenAI forum #937923 and HN)
- **Source:** Engineering blog, recirculated in community threads
- **Gist:** Three canonical rules from a frontier agent company: (1) don't tell o1 to think out loud, (2) front-load dense context, (3) specify desired output precisely. Widely repeated community shorthand for "how to prompt reasoning models."
- **Humanization takeaway:** Reinforces the divide between *reasoning elicitation* (dead on modern reasoning models) and *output styling* (where humanization work must shift).

### 21. Wharton GAIL Report — "The Decreasing Value of Chain of Thought" (Jun 2025)
- **URL:** https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/
- **Source:** Wharton Generative AI Labs (Meincke, Mollick, Mollick, Shapiro)
- **Date:** June 8, 2025
- **Gist:** Empirical study across reasoning and non-reasoning model tiers. Non-reasoning models: modest gains (Gemini Flash 2.0 +13.5%, Sonnet 3.5 +11.7%, GPT-4o-mini +4.4% not significant) but increased variance — CoT can cause errors on easy questions the model would otherwise answer correctly. Reasoning-tier models: **negligible CoT gain** at 20–80% additional time cost (35–600% more seconds). Conclusion: for reasoning models, explicit CoT prompting is not worth the cost.
- **Example finding:** CoT requests took 5–15 seconds longer. For models that already reason internally, adding "let's think step by step" is noise.
- **Humanization takeaway:** The strongest empirical confirmation that explicit CoT prompting is now a beginner mistake on reasoning-tier models. Humanization work should operate at the output-style layer, not the reasoning-elicitation layer. This also validates the "overthinking counter-prompt" (#4) and Cognition Labs guidance (#20) as the correct practitioner posture.

### 22. arXiv 2508.01191 — "Is Chain-of-Thought Reasoning a Mirage?" (Aug 2025)
- **URL:** https://arxiv.org/abs/2508.01191
- **Source:** arXiv preprint
- **Gist:** Analysis framed through a data distribution lens: CoT reasoning is brittle when pushed beyond training distributions. Models exploit statistical regularities in training data rather than performing genuine multi-step reasoning. The "mirage" claim: apparent CoT capability may be pattern matching on training distribution, not transferable reasoning skill.
- **Humanization takeaway:** If CoT is partly an artifact of training distribution, then "making CoT sound human" is styling a performance, not a cognition — which is precisely the Unslop framing. The paper actually supports the case for post-processing the trace: if the trace isn't genuine reasoning, it can be shaped freely without fidelity concerns.

### 23. LightChen233/Awesome-Long-Chain-of-Thought-Reasoning (GitHub, ongoing)
- **URL:** https://github.com/LightChen233/Awesome-Long-Chain-of-Thought-Reasoning
- **Source:** GitHub (community-maintained research list)
- **Gist:** Continuously updated paper tracker for long-CoT and reasoning-model research. Currently the most complete catalog of the 2025 reasoning paper wave — covering latent CoT, budget forcing, overthinking studies, faithfulness audits, and instruction-following in reasoning models.
- **Humanization takeaway:** A live resource for tracking what's been established vs. still open in the reasoning trace space. Useful for auditing whether any "new" humanization technique is actually already covered by a 2025 paper.

---

## Patterns, trends, and gaps

### Patterns
- **Two-camp split on "Let's think step by step":** Still universally taught in YouTube/beginner content (IBM, DataCamp, DEV Community, PE Collective), but now **empirically deprecated** by the Wharton GAIL report (#21, Jun 2025) for reasoning-tier models. The practitioner consensus has hardened: explicit CoT prompts add latency and variance on o3/GPT-5/Claude 4, with negligible accuracy gain.
- **Magic phrases cluster:** "Take a deep breath", "show your work", "you're overthinking this", "what's the boring solution?", "walk me through your reasoning", "challenge my assumption". All are short, emotionally/cognitively loaded, and re-usable as humanization levers — valid on non-reasoning models, but increasingly misapplied to reasoning ones.
- **Convergent reasoning voice:** R1-distilled models (Qwen3, DeepSeek, Kimi K2) share a recognizable "Wait… Hmm… Actually… Let me check…" first-person register. This is the de facto template for human-sounding internal monologue and is now confirmed across the open-weights class.
- **Structural separation between inner and outer:** Both OpenAI's official guide and community-built prompts (Cognitive Mesh, `<inner-monologue>` tags) converge on keeping deliberation separate from the final answer.
- **Budgeted reasoning with natural cutoffs:** llama.cpp's experience (and s1's budget forcing formalization) shows that a natural-language "time to commit" message preserves quality; abrupt truncation degrades it. The *form* of the stop signal matters. "Wait" as an extension token is now a published technique.

### Trends
- **From "elicit reasoning" to "shape reasoning":** The community frontier is moving from "how do I get the model to think?" to "the model already thinks — how do I make the thinking shorter, more grounded, more human-voiced, more committed?"
- **Faithfulness anxiety deepening:** The Wharton empirical study (#21) and arXiv 2503.08679 (#18) together make the practitioner case that visible CoT is often a performance. Teams are designing *around* unfaithfulness rather than trusting the trace. The "CoT is a mirage" framing (#22) adds a data-distribution critique.
- **CoT prompting officially declared declining value:** The Wharton June 2025 report is the first peer-reviewed empirical study to systematically show that CoT prompts have marginal or no benefit on reasoning-tier models. This closes a debate that had been running since 2023.
- **Latent / hidden reasoning rising:** Multiple HN threads highlight latent-space reasoning (Coconut, Heima) as a capability win but an interpretability loss. The concern is growing that future models will not *produce* a CoT trace to style.
- **EQ ≠ IQ axis (Karpathy):** Growing consensus that humanization lives in pretraining vibes, not RL-reasoning. This is an under-discussed strategic cut for the project.
- **GPT-5 routing opaqueness creating practitioner friction:** HN and r/LocalLLaMA threads (mid-2025 forward) document confusion about when GPT-5 engages deep reasoning — the shift from explicit `model="o3"` to implicit routing removes a control surface practitioners relied on. Workarounds include phrasing queries as hard problems and frontloading complexity signals.

### Gaps (open research space for the Humanizer project)
- **No community prompt pattern for humanized-but-faithful reasoning.** Everyone optimizes for one or the other.
- **No public-domain "voice transfer" for CoT traces.** There's huge work on style transfer for final output, near-zero on style transfer for the reasoning trace itself (e.g., make the monologue sound like a tired engineer vs. an eager grad student).
- **Limited discussion of register modulation in CoT.** Most community work treats "think step by step" as a binary switch; almost nobody talks about *who* is thinking aloud (age, mood, expertise, tiredness). Rich humanization opportunity.
- **No established UX pattern for "show/hide/collapse-with-summary"** matching how humans naturally surface a short justification rather than a full transcript. The r/LocalLLaMA "reasoning is a drawback" thread is hitting this wall but has no solution.
- **Discord content is largely ephemeral and undersurfaced.** Cursor, Anthropic, and OpenAI Discords contain high-signal reasoning-prompt tips not indexed by Google; this angle is under-mined.

---

## Sources used

- r/LocalLLaMA: transparent CoT catalog, reasoning-as-drawback post, Qwen3.5/Gemini CoT convergence, thinking-loop reports, llama.cpp reasoning budget, Qwen thinking toggle
- r/ChatGPT, r/ChatGPTPromptGenius, r/PromptEngineering: "overthinking" trick, "show your work", internal-monologue thread, Cognitive Mesh Protocol, human-think prompt tricks
- Hacker News: test-time compute + latent reasoning, reasoning-vs-simple-prompting benchmark debate, unfaithful CoT paper discussion
- OpenAI Developer Community: o1 tips & tricks canonical thread
- X / Twitter: Andrej Karpathy GPT-4.5 IQ-vs-EQ thread
- Rephrase-it blog (2026): "Chain-of-Thought Prompting in 2026" — well-cited practitioner synthesis of community consensus
- YouTube/tutorial corpus: DataCamp, IBM, DEV Community, PE Collective, AppliedAI — canonical "think step by step" teaching
- H-CoT jailbreak paper (arXiv 2502.12893), CoT faithfulness paper (arXiv 2503.08679) — academic findings that are actively driving the forum backlash
- Cognition Labs blog ("Prompting o1") — engineering-side rule set the community keeps quoting
- Wharton GAIL Technical Report — "The Decreasing Value of Chain of Thought in Prompting" (Jun 2025) — https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/
- arXiv 2508.01191 — "Is Chain-of-Thought Reasoning a Mirage?" (Aug 2025) — https://arxiv.org/abs/2508.01191
- GitHub: LightChen233/Awesome-Long-Chain-of-Thought-Reasoning — https://github.com/LightChen233/Awesome-Long-Chain-of-Thought-Reasoning
