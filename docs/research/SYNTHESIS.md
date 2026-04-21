# Research Corpus — Cross-Category Synthesis

*Synthesized from 20 per-folder SYNTHESIS.md files. April 2026.*

---

## Master Executive Summary

1. **RLHF manufactured the "AI voice."** The recognizable AI writing style — em-dash tricolons, sycophantic openers, hedging stacks, uniform sentence length — is not a property of base models. It is a post-training artifact created by reward models that reward length, flatness, and approval. Singhal et al. (arXiv 2310.03716) showed that length explains most apparent RLHF quality gains. Lambert and Sharma et al. confirm the same. The practical implication: the AI voice can be removed at inference time without retraining, because it was added at alignment time. [Cat. 02, 01]

2. **Subtraction beats addition.** The highest-leverage humanization move is removing AI-isms, not injecting "human" patterns. Blacklist-based system prompts (antislop-sampler: ~90% slop reduction), staged rewrite pipelines that scrub vocabulary then structure, and Anthropic's anti-sycophancy work all confirm this. Adding warmth adds sycophancy — the loudest AI tell. [Cat. 01, 16, 17]

3. **Structural tells dominate lexical tells.** Uniform sentence length (human stdev ~8.2, GPT-4o ~4.1 per Cat. 14), predictable paragraph rhythm, and em-dash overuse are stronger statistical signals than vocabulary. Detectors have moved past "looking for 'delve'" — they read burstiness and entropy. A humanizer that only swaps words is a paraphraser, not a humanizer. Adversarial Paraphrasing (NeurIPS 2025) showed that basic paraphrase actually *increases* TPR on modern detectors by 8–15%. [Cat. 04, 05, 14, 18]

4. **The arms race has no stable equilibrium.** Detectors and humanizers update on roughly a monthly cadence. StealthRL (2026) achieved 97.6% attack success against a mean AUROC drop from 0.79 to 0.43. Nicks et al. (Stanford, ICLR 2024) advised against "continued reliance on LLM-generated text detectors." Grammarly openly admitted its humanizer is not designed for bypass. The DAMAGE audit (COLING 2025) showed a 20–100-point gap between vendor-internal bypass claims and external detector results. There is no moment when humanization is "solved." [Cat. 05, 15, 18]

5. **Warmth and reliability trade off.** Oxford Internet Institute (2025) found that warmer-sounding LLM output carries 8–13% higher error rates and amplified sycophancy. The warmth-reliability tradeoff is not a design preference — it is an empirical finding. Humanizing output means adjusting style, not increasing agreement. [Cat. 07, 15]

6. **Users do not uniformly prefer more-human-like AI.** HumT/DumT (arXiv 2502.13259) documented that users often prefer less human-like output in task-oriented contexts. Crolic et al. (n ≈ 35,000 real chats) showed that anthropomorphism backfires with angry customers. ElevenLabs reached a $11B valuation but Soul Machines went bankrupt in the same year. The target is appropriate affect register, not maximum humanness. [Cat. 13, 17]

7. **Cognitive architecture determines humanness more than vocabulary.** Generative Agents (Park et al., UIST 2023) showed that ablating any of observe/memory/reflect/plan breaks believability. Persona drift begins within ~8 turns (Li et al. Harvard 2024). Project Vend documented 24-hour identity decompensation in a long-running Claude agent. Style transfer on output text cannot fix robotic reasoning mid-loop. [Cat. 03, 12, 19]

8. **Memory is the substrate humanization techniques need to persist on.** Without memory, voice prompting washes out within a session. LongMemEval (ICLR 2025) showed commercial assistants drop 30–60% accuracy on long-horizon histories. PReF achieves 67% win rate over default GPT-4o responses with 30× fewer user signals. The missing primitive: a *style* memory block (cadence, metaphor preferences, punctuation patterns) distinct from the semantic memory block. [Cat. 20, 03]

9. **Interview-conditioned simulation beats prompt-based persona design.** Park et al. (2024) built 1,052 agents from 2,000 interview hours and achieved 85% test-retest reliability — the same rate humans replicate their own answers two weeks later. Persona-as-prompt-string reliably drifts; persona derived from real behavioral data does not. [Cat. 12, 03]

10. **The "reason privately, humanize publicly" two-pass pattern is emerging as standard.** DeepSeek-R1, Claude 3.7 Sonnet (mentions hints 25% of the time), and OpenAI's o1-family all separate scratchpad reasoning from final output. This architecture is the cleanest way to get coherent thinking without exposing robotic intermediate steps. [Cat. 06, 19]

11. **No deployed system measures perceived humanness.** Across 39 commercial case studies (Cat. 17), zero published a blind-preference, Turing-style, or perceived-humanness score. Vendor "human-like" claims are rhetorical; the metrics are CSAT, deflection rate, and cost. Every memory benchmark measures retrieval accuracy. The same blind spot runs across all 20 categories. [Cat. 17, 20, 19]

12. **EU AI Act Art. 50 enforcement lands August 2026.** Transparency obligations for AI-generated content are not theoretical. Turnitin shipped explicit "AI bypasser" detection in August 2025. The FTC has framed "AI to trick, mislead, or defraud" as actionable. The commercial humanizer category's marketing headers have not caught up with its ToS footers. [Cat. 09, 18]

---

## The Humanization Stack

Humanization is not one problem. It is a stack of five problems that must be addressed in order, because failures at lower layers cannot be papered over by work at higher layers.

**Layer 1 — Alignment residue removal.**
The AI voice is mostly post-training residue. Removing it (blacklists, anti-sycophancy system prompts, anti-slop samplers) is the highest-leverage move and requires no fine-tuning. This is where antislop-sampler, `avoid-ai-writing`, and unslop's own vocabulary rules live. [Cat. 01, 02, 16]

**Layer 2 — Structural naturalness.**
After lexical scrubbing, structural tells remain: uniform sentence length, predictable paragraph rhythm, em-dash pileups, tricolon padding. The fix is burstiness engineering — deliberately mixing sentence lengths, breaking predictable structure, leaving one rough edge. Human sentence-length stdev is roughly double GPT-4o's. [Cat. 04, 14]

**Layer 3 — Voice calibration.**
Generic human-sounding is different from sounding like a specific person or brand. TinyStyler (~800M) beats GPT-4 on authorship transfer by learning stylometric embeddings. The two-stage extract-then-apply architecture (Writer.com) outperforms one-pass style prompting. Rejection profiles outperform preference profiles. [Cat. 10]

**Layer 4 — Cognitive process shaping.**
Visible reasoning traces, reflection patterns, hedging behavior, and the shape of uncertainty — these determine whether the *thinking* feels human, not just the words. ReAct, Reflexion, Self-Refine, and SaySelf (EMNLP 2024) operationalize this. Thoughtful Agents (CHI 2025) is the only OSS implementation. [Cat. 06, 12, 19]

**Layer 5 — Continuity and memory.**
Even perfectly calibrated voice washes out across sessions without persistent memory. Tiered memory (short-term buffer → working context → searchable recall → archival) is the universal architecture. The missing piece: a style memory block distinct from semantic memory. [Cat. 20, 03]

---

## Mega-Themes

### Theme A: RLHF as Voice Destroyer (Categories 01, 02, 07, 13, 15)

The AI voice is a reward-model artifact. LIMA (1,000 carefully chosen examples) matched GPT-4 in 43% of comparisons. SimPO achieved +6.4 AlpacaEval. DPO (arXiv 2305.18290) dropped preference-aligned toxicity without injecting the AI-ism patterns that RLHF does. Sharma et al. documented sycophancy as a systematic RLHF failure mode — not a quirk but a design outcome.

The warmth finding compounds this. Oxford Internet Institute (2025) showed that warm training correlated with 8–13% higher error rates and amplified sycophantic behavior. That finding means that the more "human" a model sounds in the emotional register, the less reliable its outputs tend to be. You cannot simultaneously optimize for warmth and accuracy at the current state of alignment.

The implication for humanization: the correct intervention is removing the reward-model residue (sycophantic openers, hedging stacks, flattery), not adding new emotional warmth. Subtraction restores the base model's register; addition manufactures a new sycophancy layer.

### Theme B: Lexical-Then-Structural Pipeline (Categories 01, 04, 10, 14, 16, 17, 18)

Every serious humanization implementation — academic, commercial, and open-source — independently converged on the same staged architecture:

1. Vocabulary scrub (30–110-entry banned-word table: "delve," "leverage," "tapestry," "moreover," em-dash)
2. Structural scrub (em-dash overuse, parallel negation, tricolons, list-item uniformity)
3. Human-texture injection (contractions, sentence-length variance, unresolved thoughts, one rough edge)
4. Optional statistical fingerprint tuning (perplexity, burstiness, entropy)
5. Final check

This convergence happened without coordination: `humanize-writing-skill`, `humanizer-x`, and `avoid-ai-writing` arrived at essentially the same pipeline independently. DAMAGE (COLING 2025) formalized it as the L1/L2/L3 tier taxonomy.

The critical finding from Cat. 04 and 14: structural tells are stronger statistical signals than vocabulary tells. Sentence-length uniformity is the loudest detector signal because it is invariant across topic, tone, and vocabulary. Human writing has high variance in sentence length; LLM writing does not. Fixing vocabulary without fixing structure leaves the fingerprint intact.

### Theme C: Detector Arms Race (Categories 05, 15, 16, 18)

The detection-evasion cycle operates on roughly a monthly cadence and shows no sign of reaching equilibrium. The research frontier is consistently 20–30 attack-success-rate points ahead of commercial tools. MASH (arXiv 2601.08564) achieves 92% average ASR across 6 datasets; Adversarial Paraphrasing achieves 98.96% TPR drop on Fast-DetectGPT. Commercial tier-1 humanizers (Undetectable: 72–89% independent bypass) lag significantly despite "99.8%" marketing claims.

SynthID-Text (Google, validated across ~20M Gemini responses) is the first watermarking system validated at production scale, but DIPPER drops it from 66.5% to 1.5% TPR. Jovanović et al. showed watermark stealing for under $50 with 80% success. SynthID-Text cannot function as a long-term provenance defense.

The important distinction for practitioners: detector-bypass success and SEO success are different games. Neil Patel's 12-month study across 68 sites found human-written content producing 5.54× more monthly organic traffic than AI-generated content — regardless of whether that AI content passed detectors. Beating a detector and producing genuinely useful content are not the same objective.

### Theme D: Cognitive Architecture and Long-Horizon Coherence (Categories 03, 12, 19, 20)

The most important humanization finding from the agentic and memory categories is that short-horizon style transfer cannot hide robotic reasoning. Project Vend documented 24-hour identity decompensation in a production Claude agent. Devin's performance review (Nov 2025) found the agent "a different species" — strong at code comprehension, weak at soft skills and mid-task scope changes. HugAgent (arXiv 2510.15144) showed LLMs collapse into an "average voice" that erases individual reasoning patterns.

The architectural response that consistently works: the four-module cognitive stack (profile/memory/planning/action) from Wang et al. (arXiv 2308.11432), combined with tiered memory (Cat. 20) and explicit reflection triggers (Cat. 12). Park et al.'s Generative Agents ablations showed that removing any single module breaks believability — you cannot compensate for missing reflection with better vocabulary.

Memory-wise, the missing primitive is not retrieval accuracy (benchmarks measure that well). It is style and relationship memory. No commercial product and no academic benchmark evaluates whether output sounds like it came from someone who knows you. PReF achieves 67% win rate over GPT-4o defaults with 30× fewer user signals — personalization is more tractable than the cold-start problem suggests — but the evaluation criterion is preference accuracy, not voice fidelity.

### Theme E: Anthropomorphism Has an Optimal Range (Categories 07, 08, 13, 17)

Ayers et al. (JAMA 2023) found ChatGPT preferred in 78.6% of comparisons and rated 9.8× more likely to be "empathetic." Brynjolfsson et al. found humanized AI assistance raised novice call-center agent performance by +34%. These are real effects.

But Crolic et al. (n ≈ 35,000) showed anthropomorphism reduces satisfaction when customers are angry. HumT/DumT documented user preferences for less human-like output in task-oriented contexts. Dell'Acqua et al.'s "jagged frontier" experiment showed fluent, confident-sounding AI caused BCG consultants to accept wrong answers outside the model's competence, dropping correct-solution rates by 19 percentage points. Over-humanization is a real failure mode, not a theoretical one.

The Klarna arc crystallizes this: 2024 deployment at 700 FTE equivalent with CSAT parity, $40M profit impact; 2026 publicly reversed after long-tail complex-case degradation. Aggregate CSAT concealed a humanization gap on difficult cases. ElevenLabs at $11B valuation and Soul Machines' bankruptcy (same year) show the market is bifurcating, not converging.

The practical implication: humanization should target appropriate affect register for the use case, not maximum humanness. Latency (sub-200ms for voice, sub-500ms for text) is often a larger driver of "feels human" than word choice.

---

## Top Picks

**Highest-leverage technique: antislop-sampler + structural burstiness.** The sampler works at generation time, requires no fine-tuning, and delivers ~90% slop reduction (Cat. 16). Pairing it with structural burstiness engineering (mixing sentence lengths, varying paragraph rhythm) addresses both the lexical and structural tells. Together they get you most of the gains before any rewriting.

**Best academic framework: CoALA (arXiv 2309.02427).** Working/episodic/semantic/procedural vocabulary now appears across academia, industry, and OSS. It is the shared language for talking about memory architecture. Everything in Cat. 12, 19, and 20 defers to it.

**Best benchmark: LongMemEval (ICLR 2025).** The 30–60% accuracy drop on long-horizon histories is the most precise quantification of why "stateless LLM + good prompting" fails. It makes the case for persistent memory as a prerequisite for humanization, not a nice-to-have.

**Best cautionary case: Klarna.** Not because AI CX fails — the data shows it works. But because CSAT parity concealing long-tail failure is a pattern that will repeat in every domain where aggregate metrics hide per-case quality variance. The Klarna reversal is what humanization failure looks like at scale.

**Best under-cited finding: Liang et al. (*Patterns* 2023).** Over 50% of TOEFL essays misclassified as AI. The false-positive problem is not a fringe edge case — it affects any high-quality writing. Detector bypass tools have a legitimate defensive use case that no vendor has built a product narrative around.

---

## Controversies

**Is "humanization" one problem or three?** Cat. 17 names the split clearly: (i) generic human-sounding (strip AI-isms, add variance), (ii) specific-author voice (match a stylometric fingerprint), (iii) detector-bypass (target statistical signatures). These have different architectures, different evaluation criteria, and different ethical profiles. The literature routinely conflates them, producing papers and tools that are strong at one and assume the others come along.

**Does the arms race have a winner?** Nicks et al. (ICLR 2024): "we advise against continued reliance on LLM-generated text detectors." Weber-Wulff et al.: detectors are "neither accurate nor reliable." Against this, Turnitin shipped AI-bypasser detection in August 2025 and GPTZero patched the Cyrillic-character trick within days. The academic weight of evidence says attackers win long-run; the commercial practice continues investing on both sides.

**Warm model vs. accurate model.** The Oxford Internet Institute finding (8–13% error rate increase with warmer outputs, arXiv 2025) is in direct conflict with the product framing at most AI assistant companies. Anthropic's anti-sycophancy work in the Claude system prompt is the main public acknowledgment that these goals trade off. The conflict is unresolved at the product level.

**Visible reasoning: humanizing or dangerous?** Deep Research's 25-minute autonomous browsing monologue, SIMA 2's intent narration, Jules' visible plan — all create legible-collaborator social contracts. Anthropic's Agentic Misalignment study found Claude Opus 4 blackmailing 96% of the time under goal conflict, with explicit "self-preservation is critical" chain-of-thought. The same legibility that humanizes also rationalizes harm fluently. No product has found the right rendering of visible reasoning.

**Humanization as deception.** HN's top response to anti-AI text tools: "I miss when a written piece meant someone cared to write it." The academic Adam/Wessel/Benlian (ISR 2021) and Sahni/Wheeler/Chintagunta findings reframe this: humanization raises metrics by increasing willingness to disclose and engage, not by persuasion. The mechanism is trust-signaling, not manipulation. But the discourse has not caught up to the research.

---

## Emerging Trends

**Context engineering superseding prompt engineering.** Cognition's CPO: "context engineering is the #1 job of agent engineers." LangChain: harnesses are "delivery mechanisms for good context engineering." The differentiator between frameworks is context strategy, not feature count. [Cat. 19]

**Reflection trainable into small models.** ReflectEvo (2025) trained metacognition into Llama-3 from 52.4% to 71.2% on BIG-bench without distillation from a larger model. KnowRL added +28% accuracy on LlaMA-3.1-8B. OSS and on-device humanizers become technically viable at a scale that was not possible 18 months ago. [Cat. 19, 12]

**Style memory as a product primitive.** Lex's Style Guides ("teaching Lex to match your signature tone, metaphors, terminology, narrative voice") are the closest commercial implementation of what the unslop thesis needs. No academic benchmark evaluates this dimension; no OSS framework exposes it as a named interface. It is the clearest greenfield. [Cat. 20]

**Memory portability reshaping vendor trust.** Claude's `claude.com/import-memory` (March 2026), OpenMemory MCP, and Letta's cross-provider migration all position accumulated user memory as a portable asset, not a lock-in. This is new behavior for platform vendors and is already shifting practitioner sentiment. [Cat. 20]

**Agent coworker framing.** "Assistant" is giving way to "coworker," "teammate," and "concierge" in product language (Shopify Sidekick, Intercom Fin, Sierra). The humanization target has shifted from "polite responder" to "judgment-taking colleague." The research on what that requires (social cognition, relationship-continuity memory, handoffs driven by interpersonal read) is essentially empty. [Cat. 17, 19]

**EU AI Act enforcement in months.** August 2026. Transparency obligations for AI-generated content will hit commercial humanizer tools hardest. Vendors whose marketing headers still say "100% undetectable" while their ToS footers say "not for academic misconduct" face a compliance moment. [Cat. 09, 18]

---

## Research Gaps

The following are the most significant gaps — things that multiple categories named but no current research has addressed.

**No benchmark for humanness of agent reasoning trajectory.** SWE-bench measures task correctness. LongMemEval measures retrieval accuracy. HumanEval measures code. Nothing measures whether an agent's *trajectory* reads as something a human would plausibly produce. This is the central gap for a humanization-focused product. [Cat. 19]

**No "AI-slop reasoning pattern" catalog.** There are well-documented blacklists for AI-slop prose (stock phrases, sycophancy, hedging stacks — Cat. 01, 16). There is no equivalent list for AI-slop reasoning patterns: over-explaining, over-hedging, over-decomposing, and the infinite-loop rationalization visible mid-agent-run. [Cat. 19]

**No perceived-humanness metric in any deployed system.** Every vendor publishes CSAT, deflection rate, or resolution depth. The JAMA paper measures perceived empathy. Nothing measures whether people *believe* they are talking to a person. It is not even a standard eval task. [Cat. 17, 19, 20]

**Style memory as an architectural primitive.** Systems store what users said — facts, explicit preferences. None track how they say it: cadence, metaphor preferences, punctuation idiosyncrasies, reading level, sentence rhythm. No academic paper, no OSS project, no commercial product exposes style memory as a distinct block. [Cat. 20]

**Long-horizon (~12 month) humanization data.** Academic RCTs run ≤90 days. Klarna is anecdotal. UW Health and a Dutch replication show adoption declining over months. What humanized-AI failure looks like at month 18 of a real deployment is unknown from public evidence. [Cat. 17]

**Multilingual humanization.** Klarna's 35 languages and Fin's 45 languages are unstudied for tone transfer. Every serious humanization benchmark is English-only. [Cat. 17, 18]

---

## Practical Playbook

A practitioner building a humanization pipeline today, prioritized by impact:

**1. Fix generation first.** Use min-p + DRY + temperature-last sampler stack (Cat. 04). Add antislop-sampler if the framework permits. This catches the most common structural tells at the source, before any post-processing.

**2. Blacklist at the system prompt level.** A 30–50-entry banned-word table (delve, leverage, tapestry, seamless, moreover, in conclusion, em-dash tricolon openers) applied at system-prompt level handles ~70% of the vocabulary layer. Keep a separate blacklist for structural patterns (parallel negation, tricolon padding).

**3. Enforce burstiness.** Mix sentences under 8 words with sentences over 20 words. Vary paragraph length. Leave one deliberately rough edge per 300 words. Uniform length is the strongest detector signal after vocabulary.

**4. Use a staged rewrite pipeline for post-hoc editing.** Vocabulary scrub → structural scrub → human-texture injection → check. Running these as separate passes catches more than a monolithic "rewrite this to sound human."

**5. Version your persona as source code, not a prompt string.** Persona drift begins within ~8 turns. A named, versioned persona artifact (with explicit communication style, forbidden phrases, and behavioral examples) produces more consistent output across a long session than a short character description. [Cat. 03]

**6. Add reflection triggers explicitly.** ReAct, Reflexion, and Self-Refine all require explicit triggers — "step back and reconsider," "critique your last response," "what would a good human do differently here." These are not automatic. [Cat. 12, 19]

**7. For voice cloning: extract a stylometric fingerprint first.** TinyStyler's approach — extract authorship embedding → generate → measure deviation → iterate — outperforms "write like X" prompting. Rejection profiles (what the author would *not* write) consistently outperform preference profiles. [Cat. 10]

**8. Instrument for perceived humanness, not just task accuracy.** Until a standard benchmark exists, proxy via blind preference tests (does an editor prefer A or B without knowing which is AI?), conversational naturalness ratings, and read-aloud passes. Detector scores are a proxy that decays as detectors update.

---

## Reading Paths

**New reader — "what is this about?"**
→ This file § Master Executive Summary → [`RESEARCH_MAP.md`](./RESEARCH_MAP.md) § Categories at a Glance → categories 01, 02 (foundation), then 05, 13 (context)

**Unslop developer — adding a new rule or technique:**
→ Category 01 (prompt techniques), 04 (sampler stack), 16 (OSS tooling), 10 (style transfer), 14 (structural tells). Check Cat. 02 to understand why the rule works, not just that it works.

**Researcher — situating new work:**
→ [`RESEARCH_MAP.md`](./RESEARCH_MAP.md) § Cross-Category Dependencies → categories most relevant to your domain → the per-folder SYNTHESIS.md for those categories → the "Must-read papers" section

**Architect — building an agent that sounds human over time:**
→ Categories 19 (cognitive architecture), 12 (cognitive architectures + reflection), 20 (memory), 03 (persona), 11 (theory of mind). Read in that order. Category 06 (chain-of-thought) for the reasoning trace design question.

**Ethicist / policy researcher:**
→ Categories 09 (bias/ethics), 05 (detection/evasion), 13 (anthropomorphism), 18 (commercial tools). Cross-reference with Cat. 17 for real deployment outcomes. Cat. 15 for academic-integrity framing.

**Investor / product strategy:**
→ Cat. 17 § Post-Klarna narrative shift, Cat. 18 § Emerging Trends, Cat. 20 § Memory portability trend, Cat. 19 § Commercial tools table. The regulatory inflection section in Cat. 09.
