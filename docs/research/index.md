# Research Corpus — Navigation Index

This corpus spans 20 research categories covering AI text humanization: the techniques, the detectors, the tools, the cognitive architectures, and the social and ethical context around all of it. Together the categories amount to several hundred papers, 30+ GitHub repos, dozens of commercial products, and practitioner cases from 2021 through early 2026.

**Three companion files:**
- This file (`index.md`) — navigation guide
- [`SYNTHESIS.md`](./SYNTHESIS.md) — cross-category analysis: themes, tensions, gaps, practical playbook
- [`RESEARCH_MAP.md`](./RESEARCH_MAP.md) — cross-reference tables: theme-to-category index, dependency graph, entry points by question

---

## All 20 Categories

| # | Folder | One-line summary |
|---|--------|-----------------|
| 01 | [`01-prompt-engineering-humanization`](./01-prompt-engineering-humanization/SYNTHESIS.md) | Subtraction-first prompting (blacklists, anti-slop system prompts) beats "write like a human" instructions; DIPPER drops DetectGPT accuracy 70%→5% |
| 02 | [`02-rlhf-and-alignment`](./02-rlhf-and-alignment/SYNTHESIS.md) | RLHF creates the "AI voice" as a post-training artifact; sycophancy and length-padding are structural reward-model failures, not model personality |
| 03 | [`03-persona-and-character-design`](./03-persona-and-character-design/SYNTHESIS.md) | Persona is source code, not a prompt string; drift begins within ~8 turns; versioned persona artifacts beat ad-hoc character prompts |
| 04 | [`04-natural-language-quality`](./04-natural-language-quality/SYNTHESIS.md) | Sampler choices (min-p + DRY + temperature) produce measurable naturalness gains; structural tells (uniform sentence length) outweigh vocabulary tells |
| 05 | [`05-ai-text-detection-and-evasion`](./05-ai-text-detection-and-evasion/SYNTHESIS.md) | Arms race on a monthly cadence; SynthID-Text validated at scale; StealthRL achieves 97.6% attack success; Liang et al. found >50% TOEFL essays falsely flagged |
| 06 | [`06-chain-of-thought-reasoning`](./06-chain-of-thought-reasoning/SYNTHESIS.md) | Visible reasoning traces humanize output but also rationalize harm fluently; "reason privately, humanize publicly" is the emerging two-pass pattern |
| 07 | [`07-emotional-intelligence-empathy`](./07-emotional-intelligence-empathy/SYNTHESIS.md) | ChatGPT rated 9.8× more empathetic than physicians in JAMA 2023; warm training increases error rates 8–13% (Oxford Internet Institute 2025) |
| 08 | [`08-conversational-dialogue-systems`](./08-conversational-dialogue-systems/SYNTHESIS.md) | ~200ms inter-turn latency target; 39% multi-turn performance drop documented; latency matters more for "feels human" than word choice |
| 09 | [`09-bias-fairness-ethics`](./09-bias-fairness-ethics/SYNTHESIS.md) | EU AI Act Art. 50 enforcement August 2026; detector bias hits non-native speakers hardest; the Klarna reversal and Character.AI/Google settlement as 2026 case studies |
| 10 | [`10-style-transfer-voice`](./10-style-transfer-voice/SYNTHESIS.md) | TinyStyler (~800M params) beats GPT-4 on authorship transfer; rejection profiles outperform preference profiles; two-stage extract-then-apply architecture wins |
| 11 | [`11-theory-of-mind`](./11-theory-of-mind/SYNTHESIS.md) | Explicit ToM ≠ applied ToM; GPT-4o FANToM All* score 0.8% vs humans at 87.5%; scaffolding rescues SimpleToM from 49.5% to 93.5% |
| 12 | [`12-cognitive-architectures`](./12-cognitive-architectures/SYNTHESIS.md) | CoALA framework as shared vocabulary; Park et al. 1,052-agent study achieves 85% test-retest reliability from interview data; Reflexion hits 91% HumanEval |
| 13 | [`13-anthropomorphism-user-perception`](./13-anthropomorphism-user-perception/SYNTHESIS.md) | HumT/DumT: users often prefer less human-like LLM output; anthropomorphism backfires with angry users; ElevenLabs at $11B vs Soul Machines bankruptcy |
| 14 | [`14-creative-writing-storytelling`](./14-creative-writing-storytelling/SYNTHESIS.md) | LLM stories score 3–10× lower on creativity tests; instruction-tuning is the bottleneck; human sentence-length stdev ~8.2 vs GPT-4o ~4.1 |
| 15 | [`15-academic-papers-llm-humanization`](./15-academic-papers-llm-humanization/SYNTHESIS.md) | Most rigorous academic benchmarks; DAMAGE taxonomy; Adversarial Paraphrasing drops TPR 98.96%; Oxford warmth paper documents 10–30pp error rate increase |
| 16 | [`16-github-tools-libraries`](./16-github-tools-libraries/SYNTHESIS.md) | blader/humanizer ~14.5k stars; antislop-sampler ~340 stars ~90% slop reduction; GradEscape 139M params beats DIPPER 11B; StealthRL via GRPO on Qwen3-4B |
| 17 | [`17-industry-blogs-case-studies`](./17-industry-blogs-case-studies/SYNTHESIS.md) | Klarna's AI-assistant reversal as the defining cautionary tale; novice-bias (+34% for low performers, ~0% for top); no deployed system publishes a perceived-humanness score |
| 18 | [`18-commercial-humanizer-tools`](./18-commercial-humanizer-tools/SYNTHESIS.md) | ~150 products, ~$500M+ revenue, ~34M monthly visits; DAMAGE audit; WriteHuman 1.98% vs QuillBot 93.56% detection rate; research humanizers 20–30 ASR points ahead of commercial tier-1 |
| 19 | [`19-agentic-autonomous-thinking`](./19-agentic-autonomous-thinking/SYNTHESIS.md) | Cognitive architecture (memory, reflection, planning) determines humanness of agent output more than vocabulary; no benchmark measures human-likeness of reasoning trajectory |
| 20 | [`20-memory-personalization`](./20-memory-personalization/SYNTHESIS.md) | Tiered memory is the universal architecture; PReF achieves 67% win rate over GPT-4o with 30× fewer user signals; "feels human" is the shared blind spot across all memory benchmarks |

---

## How to Navigate

**New reader — get the full picture first:**
Start with [`SYNTHESIS.md`](./SYNTHESIS.md) § Master Executive Summary (the 12 bullets), then read the Mega-Themes section. That gives you the cross-cutting story in ~30 minutes. Come back to individual category SYNTHESIS.md files as you encounter specific questions.

**Practitioner building a humanization pipeline:**
Go to [`SYNTHESIS.md`](./SYNTHESIS.md) § Practical Playbook, then dig into categories 01, 04, 10, 16 for technique details. Category 05 for detection awareness. Category 18 for the commercial tool landscape.

**Researcher investigating a specific topic:**
Use [`RESEARCH_MAP.md`](./RESEARCH_MAP.md) — the Theme → Category Index gets you to relevant categories fast. The Entry Points by Question section maps "what do I want to know?" to "which categories to read."

**Agent/architecture builder:**
Categories 12, 19, and 20 are the load-bearing ones. Category 11 (Theory of Mind) and category 03 (Persona Design) are supporting. Read [`SYNTHESIS.md`](./SYNTHESIS.md) § The Humanization Stack for how the layers compose.

**Ethics and policy researcher:**
Categories 05, 09, 13, and 18 cover the detection arms race, regulatory inflection, anthropomorphism risks, and commercial tool accountability. Category 17 grounds the ethical debates in real deployment outcomes.
