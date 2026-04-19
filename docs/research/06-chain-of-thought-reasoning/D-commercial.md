# Chain-of-Thought & Reasoning — Angle D: Commercial Products

**Research value: high** — Mature and rapidly moving product category with named patterns ("thinking budgets", "private CoT", "visible extended thinking"), concrete pricing signals, and directly relevant humanization tensions for the Humazier project.

**Scope:** Commercial products that sell reasoning or chain-of-thought as a first-class feature. Three tiers are treated together because they buy/build against the same underlying CoT primitives:
1. **Reasoning-native APIs** (model layer): OpenAI o1/o3, Anthropic Extended Thinking, Google Gemini Deep Think, DeepSeek Reasoner, xAI Grok Reasoning.
2. **Reasoning-optimized end-user platforms** (retrieval + reasoning): Perplexity Pro, You.com Advanced Research, Phind Expert Mode, Consensus.app.
3. **Agent-reasoning platforms** (reasoning + tool use + long-horizon execution): Adept, Reflection AI (Asimov), Cognition Devin, Lindy, Relevance AI.

Pricing and positioning figures below were surfaced in April 2026 and are volatile — treat any specific number as a point-in-time snapshot, not a contract.

---

## Standard-field product catalog

For each product: **vendor · category · pricing · reasoning mechanic · how "thinking" is surfaced to the user · positioning quote · notable gap**.

### Reasoning-native APIs

**1. OpenAI o1**
- Vendor: OpenAI. Category: reasoning-native API.
- Pricing: ~$15 / 1M input, ~$60 / 1M output; 200K context, 100K max output; Batch API 50% off.
- Reasoning mechanic: RL-trained private chain-of-thought; reasoning tokens counted and billed but not exposed raw.
- Surfacing: summarized reasoning only; internal CoT withheld for "safety".
- Positioning: the first mainstream "think before you answer" frontier model.
- Gap: opacity — users see a summary, not the actual thought process; hard to debug or trust.

**2. OpenAI o3 / o3-mini / o3-pro**
- Vendor: OpenAI. Category: reasoning-native API.
- Pricing: o3 $2 in / $8 out per 1M; o3-mini $1.10 / $4.40; o3-pro $20 / $80. Prompt caching discounts available.
- Reasoning mechanic: same private-CoT family as o1, tuned for tool use, multimodal input, and higher compute-per-answer regimes.
- Surfacing: still summarized; February 2025 update added more visible reasoning on o3-mini in response to DeepSeek R1 transparency pressure.
- Positioning: "reasoning that also uses tools" — the practical production tier.
- Gap: reasoning text is curated for safety; raw CoT remains sealed.

**3. Anthropic Claude Extended Thinking (Sonnet 4.6 / Haiku 4.5)**
- Vendor: Anthropic. Category: reasoning-native API.
- Pricing: Sonnet 4.6 $3 in / $15 out per 1M; Haiku 4.5 $1 / $5. Thinking tokens billed separately at a higher rate; caching up to 90% off, Batch 50% off.
- Reasoning mechanic: returns a distinct `thinking` block *and* a `text` block; developer sets `budget_tokens` (min 1,500) to cap CoT length.
- Surfacing: **visible by design**. App layer chooses whether to show the raw thinking stream. Anthropic explicitly calls it "visible extended thinking" and caveats that the prose is unpolished and may not be fully "faithful" to internal computation.
- Positioning: "Keep thinking" — 2025/26 brand campaign framing Claude as a thinking *partner*, not a shortcut.
- Gap: "faithfulness" — Anthropic's own research acknowledges the visible CoT is not guaranteed to match the true internal computation; risk of performative reasoning.

**4. Google Gemini 3 Deep Think**
- Vendor: Google / DeepMind. Category: reasoning-native API + consumer tier.
- Pricing: gated behind **Gemini Ultra at ~$24.99/mo** for consumer; early API access for developers.
- Reasoning mechanic: "advanced parallel reasoning" — explores multiple hypotheses simultaneously rather than a single sequential CoT; multimodal (text, image, code, data).
- Surfacing: visible reasoning across modalities; markedly slower responses traded for thoroughness.
- Positioning: the premium tier for "complex math, science, and logic problems."
- Gap: cloud-locked, US-jurisdiction; closed weights; parallel-reasoning UX is novel and hard to render cleanly.

**5. DeepSeek Reasoner (V3.2)**
- Vendor: DeepSeek. Category: reasoning-native API + open-weight.
- Pricing: steeply undercuts Western incumbents; also deployable locally via Ollama at zero cloud cost.
- Reasoning mechanic: `model="deepseek-reasoner"` or `thinking={"type":"enabled"}` on `deepseek-chat`; returns `reasoning_content` separate from final `content`.
- Surfacing: fully visible `reasoning_content` field — arguably the most transparent of the frontier-adjacent options.
- Positioning: open reasoning at commodity cost; data-sovereignty alternative.
- Gap: safety tuning and brand trust are weaker than US incumbents; fewer enterprise guarantees.

**6. xAI Grok 4.20 Reasoning (and 4.1 Fast Reasoning)**
- Vendor: xAI. Category: reasoning-native API.
- Pricing: Grok 4.20 $2 in / $6 out per 1M (cached input $0.20); Grok 4.1 Fast $0.20 / $0.50. 2M context window. Reasoning tokens billed at standard rates.
- Reasoning mechanic: **multi-agent "debate" architecture** — four named internal agents (Grok coordinator, Harper fact-checking, Benjamin logic/math, Lucas creative) negotiate before a final synthesis.
- Surfacing: "think before responding" mode; multi-agent internals partially visible.
- Positioning: frontier reasoning with a distinctive multi-persona internal process.
- Gap: closed model, cloud-locked, subscription-gated; the persona metaphor is a marketing skin over standard ensemble/CoT mechanics.

### Reasoning-optimized end-user platforms

**7. Perplexity Pro / Max + Sonar Reasoning Pro**
- Vendor: Perplexity. Category: reasoning-optimized answer engine.
- Pricing: Free / Pro $20 per mo / **Max $200 per mo** (adds o3-pro, GPT-5 Thinking, Claude Opus 4.5) / Enterprise custom. Sonar Reasoning Pro API: $2 in / $8 out per 1M, 128K context.
- Reasoning mechanic: Pro Search runs multi-step CoT with automated tool / web-search invocation; Sonar Reasoning Pro is their in-house CoT model.
- Surfacing: shows a step list ("searching X", "reading Y") and a final cited answer; intermediate reasoning is partially exposed.
- Positioning: "answer engine" — reasoning in service of grounded answers with citations.
- Gap: reasoning is retrieval-biased; weak for abstract problems without a web source to anchor on.

**8. You.com Advanced Research & Reasoning (Smart Mode)**
- Vendor: You.com. Category: reasoning-optimized research agent.
- Pricing: Smart Mode free/unlimited; research tiers via subscription and API.
- Reasoning mechanic: agentic multi-step research — breaks query into components, builds a plan, selects tools, and synthesizes. At high effort a single query can exceed **1,000 reasoning turns** across **~10M tokens** and **200+ sources**.
- Surfacing: visible research plan and progress; explicit "effort" dial.
- Positioning: "PhD-level research" for depth-first questions.
- Gap: latency and cost scale dramatically with effort; the 1000-turn upper bound is rarely justified for typical queries.

**9. Phind (Pro + Expert Mode)**
- Vendor: Phind. Category: reasoning-optimized developer search.
- Pricing: free tier + Pro ~$15–$20/mo; VS Code extension included.
- Reasoning mechanic: "Expert" mode feeds relevant docs and sites into a reasoning model and returns step-by-step guides with citations; slower than default.
- Surfacing: cited stepwise answers; lightweight visibility into retrieved sources.
- Positioning: fewer hallucinations on technical questions via grounded reasoning.
- Gap: narrow domain (code / dev); Expert mode is a retrieval wrapper more than a novel reasoning primitive.

**10. Consensus.app (Scholar Agent)**
- Vendor: Consensus. Category: reasoning-optimized academic research.
- Pricing: consumer + institutional tiers; MCP integration with Claude/ChatGPT for embedded research.
- Reasoning mechanic: multi-agent pipeline (Planning → Search → Reading → Analysis) on top of GPT-5 Responses API across 250M+ peer-reviewed papers.
- Surfacing: "Consensus Meter" visually shows agreement/disagreement across evidence; cites each claim to papers.
- Positioning: automates literature review — days of work in minutes; evidence-first, not opinion-first.
- Gap: domain-locked to academic corpora; Consensus Meter is a strong visual but flattens nuanced disagreement into yes/no.

### Agent-reasoning platforms

**11. Adept AI (ACT-1 + agentic platform)**
- Vendor: Adept. Category: agent-reasoning platform (web/UI actions).
- Pricing: enterprise; no public self-serve pricing.
- Reasoning mechanic: Action Transformer translates natural-language goals to browser/tool actions; proprietary models trained on web UIs and software usage; web-VQA and end-to-end workflow planning.
- Surfacing: action traces (clicks, types) visible to operators; reasoning sits behind the action log.
- Positioning: "AI that powers the workforce" — automates desk work inside existing enterprise apps.
- Gap: strategic uncertainty post co-founder departures; reasoning is instrumental to actions, not a primary product surface.

**12. Reflection AI — Asimov**
- Vendor: Reflection AI (ex-DeepMind; $2B raise Oct 2025 at $8B valuation, Nvidia-led).
- Pricing: free tier + custom enterprise quotes; deploys inside customer VPC.
- Reasoning mechanic: **comprehension-first** agent — indexes codebase, docs, GitHub threads, Slack/chat into a persistent understanding store before taking action; positions itself against "code generation" agents.
- Surfacing: explanatory answers about existing systems; reasoning is the deliverable, not an afterthought.
- Positioning: "70% of developer time is spent understanding existing systems" — so that's the product.
- Gap: new, small deployment footprint; published benchmarks still thin; pricing opaque.

**13. Cognition — Devin**
- Vendor: Cognition. Category: autonomous-coding agent.
- Pricing (April 2026 restructure): Free / **Pro $20/mo** / **Max $200/mo** / Teams usage-based with $80/mo minimum / Enterprise custom. Old Core/Team ($500/mo) tiers retiring.
- Reasoning mechanic: long-horizon plan → execute → test → debug → PR loop inside a sandbox with shell, editor, and browser. **Agent Compute Units (ACU)** ≈ 15 minutes of active Devin work.
- Surfacing: visible plan timeline, step execution log, PR artifacts; user can intervene.
- Positioning: "autonomous AI software engineer."
- Gap: documented to struggle with ambiguous specs and large codebases; best on small, well-scoped tasks — the gap between marketing and capability is the most-cited critique.

**14. Lindy**
- Vendor: Lindy. Category: business-workflow agent platform.
- Pricing: Plus $49.99 / Pro $99.99 / Max $199.99 / Enterprise. Credits (1–3 on cheap models, ~10 on large models) that **don't roll over**.
- Reasoning mechanic: trigger → conditions → actions → AI steps → message; agents learn user tone from observed email/calendar behavior and require approval before sending.
- Surfacing: workflow builder exposes decision nodes; reasoning per step is implicit.
- Positioning: personal AI employees; voice-matching assistant.
- Gap: credit model's opacity (1 vs 10 credits per task) makes cost-prediction hard; reasoning is behind a form-like workflow rather than surfaced.

**15. Relevance AI**
- Vendor: Relevance AI. Category: agent workforce platform.
- Pricing (Sept 2025 model): usage-based with **Actions + Vendor Credits** (exact-cost passthrough). Free 200 actions/mo; Pro $19/mo (30K actions/yr); Team $234/mo (84K actions/yr); Enterprise custom. Overages: $80/1K actions, $20/10K vendor credits. BYO API keys allowed on paid plans.
- Reasoning mechanic: multi-agent "workforce" orchestration; smart escalations, scheduled tasks, A/B testing of agent variants.
- Surfacing: action/credit meter; agents have task histories (30 or 90 days by tier).
- Positioning: build your AI workforce without markup on model costs.
- Gap: no markup on vendor credits is rare and attractive but pushes complexity onto the buyer; reasoning is embedded in tool use, not a distinct primitive.

---

## Marketing quotes and positioning language

The verbatim language these vendors ship with is itself a signal — "thinking" has become the dominant commercial metaphor of 2025–26.

- **Anthropic — "Keep thinking."** First brand campaign (Sep 2025, multi-million, Netflix/Hulu/NYT/WSJ): Claude as "a thinking partner to take on their most meaningful challenges," explicitly **not a shortcut**.
- **Google — "Deep Think."** Sub-brand of Gemini 3 for "complex math, science, and logic problems" via "advanced parallel reasoning."
- **OpenAI — "private chain of thought."** Vendor-chosen phrase that both names the feature and defends the opacity ("for safety reasons").
- **Perplexity — "the answer engine"** + Pro Search as "multi-step reasoning with automated tool use."
- **You.com — "PhD-level research methodologies,"** "200 sources per query," "1,000 reasoning turns."
- **Consensus — "turn days of literature review into minutes"** + Consensus Meter.
- **Reflection AI — "Frontier Open Intelligence, accessible to all"** + Asimov's framing: "understand before you change."
- **Cognition — "autonomous AI software engineer"** + the ACU ("≈ 15 minutes of active Devin work") as a unit of agent thought-time.
- **xAI — "Grok thinks before responding,"** dramatized with four named internal agents debating.
- **DeepSeek — "reasoning in the open"** (implicit positioning as the transparent, sovereign alternative).

Notice the linguistic split: API vendors sell *reasoning as a capability* ("extended thinking", "deep think", "reasoning tokens"); end-user platforms sell *reasoning as a workflow* ("research plan", "Consensus Meter", "ACU"); agent platforms sell *reasoning as time* (ACUs, minutes of autonomous work, workforce hours).

---

## Patterns

**P1. "Thinking budget" has emerged as a near-standard primitive.** Anthropic `budget_tokens`, OpenAI reasoning-effort levels, You.com "effort" dial, Gemini Deep Think vs standard, Grok 4.20 vs 4.1 Fast-reasoning. Users and developers can now *buy more thought per query*. This is both a pricing lever and a UX affordance.

**P2. Reasoning tokens are separately billed — often at a premium.** Anthropic thinking tokens cost more than standard output tokens. OpenAI counts reasoning tokens into billed output. This creates direct commercial pressure to *look like you are thinking* even when you aren't.

**P3. Two divergent transparency postures.**
 - **Visible CoT camp:** Anthropic (explicit visible thinking block), DeepSeek (`reasoning_content` field), You.com (plan + step stream), Consensus (Scholar Agent stages), Devin (plan timeline).
 - **Private CoT camp:** OpenAI o1/o3 (summarized only), most consumer-facing Gemini, agent platforms where reasoning is collapsed into "what I did."
 The visible camp is growing under competitive pressure (OpenAI's Feb 2025 o3-mini transparency patch came in direct response to DeepSeek R1).

**P4. Multi-agent "debate" is the new CoT wrapper.** Grok 4.20's four-persona architecture, Consensus's Scholar Agent (Planning/Search/Reading/Analysis), Gemini Deep Think's parallel hypotheses, You.com's 1000-turn agentic loop. The market is moving from single-stream CoT to orchestrated multi-stream reasoning — and marketing is leaning hard on *personas* and *panels* to make that legible.

**P5. UX converging on a "stepper" for reasoning.** Visible pipeline steps with meaningful labels ("Querying vendor history," "Searching 12 papers") consistently improve trust and set time expectations; generic "Processing..." is being retired. Collapsible-by-default thinking blocks are becoming the default pattern.

**P6. Pricing convergence on a $20 / $200 staircase.** Perplexity Pro / Max, Devin Pro / Max, ChatGPT-analog tiers — the industry has settled on $20 as the consumer reasoning tier and $200 as the "unlocked frontier" tier. Enterprise is always "contact us."

**P7. Reasoning-as-time is replacing reasoning-as-tokens at the agent tier.** Devin sells ACUs (≈15 min of work); Lindy sells credits tied to task complexity; Relevance sells Actions + Vendor Credits. End buyers increasingly don't care about tokens — they care about outcomes and wall-clock autonomy.

---

## Trends

**T1. Transparency is becoming a competitive moat.** Anthropic's "Keep thinking" campaign, DeepSeek's open `reasoning_content`, and OpenAI's reactive transparency patch all point the same direction: **the product that lets you see the reasoning wins trust**, even if faithfulness caveats remain.

**T2. Reasoning is being unbundled from chat.** Standalone reasoning models (o1/o3, Deep Think, Grok Reasoning) are sold distinct from general chat. This lets vendors charge a premium for "thinking mode" — and lets buyers opt in to cost only when warranted.

**T3. Agents are absorbing reasoning as a commodity input.** Devin, Lindy, Relevance, Reflection AI all treat CoT as a *dependency* rather than a feature. Their product surface is plans, actions, and outcomes — not reasoning traces.

**T4. Research-style reasoning is eating knowledge-work search.** Perplexity Max, You.com Advanced Research, Consensus Scholar Agent, and enterprise deep-research products are converging on: plan → fan-out search → read → synthesize → cite. This is rapidly commoditizing a surface that used to be humans + Google Scholar.

**T5. "Thinking out loud" is becoming a UX primitive, not just an API feature.** Slack has a native "thinking steps" API; many chat UIs stream reasoning by default. Showing work is moving from developer-only to end-user-expected.

**T6. Cost-inverted transparency.** Hidden reasoning used to be cheaper to produce (summarized). Now visible reasoning is the premium offering — users pay more to *see* the thought, not less.

---

## Gaps (directly relevant to a "humanize AI output and thinking" project)

**G1. The "faithfulness gap."** Anthropic itself flags that the visible thinking stream may not represent the model's true internal computation. **Nobody is selling a product that makes the visible CoT demonstrably faithful** — this is an open product and research gap. A humanizer that clearly distinguishes *performed reasoning* from *real reasoning* has room to exist.

**G2. Reasoning prose is unpolished on purpose.** Anthropic explicitly notes the thinking block "lacks the polished tone of standard outputs." OpenAI summarizes rather than exposing raw CoT partly because raw CoT reads like machine internals. **No major product post-processes the CoT into human-grade explanation.** A humanization layer that rewrites CoT into genuinely readable natural-language reasoning — without losing structure — is a white space.

**G3. No shared rendering standard for reasoning.** Every vendor ships a different UI (steppers, collapsible blocks, Consensus Meter, ACU timelines, multi-agent debate panels). Developers building on top must re-invent the surface. A *portable humanized reasoning view* across providers is missing.

**G4. Persona theater vs. real reasoning.** Grok's four named agents and similar multi-persona framings are mostly marketing skins over standard ensemble mechanics. Users can't easily tell when personas carry real orthogonal signal vs. when they're a UI trick. A humanizer that collapses or expands persona framing honestly — or flags when it's theatrical — would add trust.

**G5. Cost legibility for thinking.** Lindy's credits, Devin's ACUs, Relevance's Actions-plus-credits, Anthropic's separately-billed thinking tokens — **none of these are easy to predict before a task runs**. "Show me what this thought will cost" is a missing product affordance across the category.

**G6. Reasoning localization / register.** CoT output is overwhelmingly English, terse, and technical — even on consumer products. No major vendor re-registers the thinking stream to match user literacy, domain, or emotional context. Humanizing reasoning for a non-expert audience is open ground.

**G7. Non-code agent reasoning is thin.** The strongest agent-reasoning products (Devin, Reflection AI) are in code. Lindy and Relevance are workflow-centric. There is room for a reasoning agent specialized in *humanized writing and argumentation* — which aligns directly with the Humazier brief.

**G8. The transparency ↔ safety tradeoff is under-explored in product.** OpenAI uses safety to justify opacity; Anthropic uses safety to argue *for* visibility. No product currently lets end-users configure this tradeoff per task ("show me everything on this math problem; summarize on this medical question"). A per-task transparency dial is a plausible humanization primitive.

---

## Cross-domain analogies (that hold up)

- **Courtroom "show your reasoning" vs. jury deliberation privacy.** The visible-CoT vs. private-CoT split maps cleanly: judges write opinions (visible reasoning, post-hoc, may not be fully faithful to deliberation); juries deliberate in private. Both are legitimate, and the legal system has spent centuries tuning which is appropriate when. Product analog: task-type-dependent transparency.
- **Scientific lab notebook vs. published paper.** Raw CoT is the lab notebook — messy, exploratory, honest. Final answer is the paper — polished, defensible, compressed. Current products ship one or the other; almost none ship both and let users toggle. Humanization = the peer-review pass between them.
- **Chess engine PV (principal variation) display.** Strong chess engines expose the top line of their search as "what I think the game will go." Users don't see the full tree, but they see the *committed line of reasoning*. This is a robust UX for "here's my thinking without flooding you," and it has not yet been ported well to LLM reasoning UIs.

---

## Sources

- OpenAI pricing and o1/o3 model docs — https://platform.openai.com/docs/pricing ; https://developers.openai.com/docs/models/o1 ; https://openai.com/blog/introducing-o3-and-o4-mini
- OpenAI o3 reasoning transparency context — https://en.wikipedia.org/wiki/OpenAI_o3 ; https://reezo.ai/blog/openai-reasoning-models-transparency
- Anthropic extended thinking — https://www.anthropic.com/research/visible-extended-thinking ; https://platform.claude.com/docs/en/docs/about-claude/models/overview ; https://claudelab.net/en/articles/claude-ai/claude-extended-thinking-showcase
- Anthropic "Keep thinking" brand campaign — https://www.axios.com/2025/09/18/anthropic-brand-campaign-claude ; https://greynblack.com/creative/anthropics-keep-thinking-campaign-elevating-claude-as-the-ai-partner-for-problem-solvers/
- Gemini 3 Deep Think — https://winsomemarketing.com/ai-in-marketing/gemini-3-deep-think-googles-premium-reasoning-model-arrives ; https://vucense.com/ai-intelligence/industry-business/gemini-3-deep-think-vs-grok-4-20-two-approaches-to-frontier-reasoning-in-2026/
- DeepSeek Reasoner — https://chat-deep.ai/docs/deepseek-thinking-mode/ ; https://deepseekagi.org/deepseek-vs-gemini/
- xAI Grok Reasoning — https://docs.x.ai/developers/models ; https://docs.x.ai/developers/models/grok-4.20-0309-reasoning ; https://aicostcheck.com/blog/xai-grok-pricing-guide-2026
- Perplexity — https://docs.perplexity.ai/pricing ; https://docs.perplexity.ai/docs/sonar/models/sonar-reasoning-pro ; https://aumiqx.com/ai-tools/perplexity-pricing-pro-plans-compared-2026/
- You.com — https://you.com/articles/the-first-advanced-research-reasoning-capability-for-llms ; https://docs.you.com/research/overview.mdx
- Phind — https://ai-coding-flow.com/blog/phind-review-2026/ ; https://shipsquad.ai/pricing/phind
- Consensus.app — https://consensus.app/ ; https://openai.com/index/consensus/ ; https://consensus.app/home/blog/consensus-outperforms-google-scholar-for-academic-search-retrieval/
- Adept AI / ACT-1 — https://www.adept.ai/ ; https://www.adept.ai/act ; https://www.adept.ai/blog/act-1/
- Reflection AI / Asimov — https://docs.reflection.ai/ ; https://reflection.ai/blog/frontier-open-intelligence/ ; https://aifundingtracker.com/reflection-ai-2b-funding-autonomous-coding-agents/
- Cognition / Devin — https://devin.ai/pricing/ ; https://cognition.ai/blog/new-self-serve-plans-for-devin ; https://www.eesel.ai/en/blog/cognition-ai-pricing
- Lindy — https://lindy.ai/pricing ; https://docs.lindy.ai/llms-full.txt ; https://get-alfred.ai/blog/lindy-pricing
- Relevance AI — https://relevance.ai/pricing ; https://relevanceai.com/docs/admin/subscriptions/plans ; https://agentsindex.ai/pricing/relevance-ai
- Reasoning UX patterns — https://dev.to/snehapriyar556/how-we-designed-a-visible-ai-pipeline-and-why-it-made-the-agent-feel-more-trustworthy-m67 ; https://slack.dev/slack-thinking-steps-ai-agents/ ; https://docs.langchain.com/oss/javascript/langchain/frontend/reasoning-tokens
