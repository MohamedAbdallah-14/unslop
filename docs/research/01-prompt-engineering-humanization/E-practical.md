# Prompt Engineering for Humanization — Practical & Forums

**Research value: high** — Practitioner communities (Reddit, HN, dev.to, LocalLLaMA, GitHub) have converged on a surprisingly specific playbook of anti-slop system prompts, style-mimicry recipes, and sycophancy-breaking framings, with enough controversy (detection arms race, negative-prompt fragility, few-shot vs ban-lists) to map genuine open questions.

## Executive Summary

Across Reddit (r/ChatGPT, r/ChatGPTPro, r/ChatGPTPromptGenius, r/LocalLLaMA, r/OpenAI), Hacker News threads, dev.to tutorials, and prompt-practitioner GitHub repos, the community has crystallized a small number of humanization patterns that recur almost verbatim across venues:

1. **Anti-slop system prompts** that forbid a named set of "GPTisms" (`delve`, `tapestry`, `leverage`, `utilize`, `Certainly!`, `It's important to note`, em-dashes, and sycophantic closers like `Hope this helps!`).
2. **Voice-transfer recipes** — paste 100–2,000 words of your own writing, have the model extract a style profile, then rewrite drafts against that profile ("Frankenstein method", "7-step style-copy").
3. **Burstiness engineering** — explicit instructions to vary sentence length and use parentheticals, rhetorical fragments, and start sentences with `And`/`But`, targeting the statistical signature AI detectors use.
4. **Sycophancy breakers** — re-frame the user's work as a third party's ("my friend Bernardo"), assign a blunt persona ("Linus Torvalds reviewing a kernel patch", "blunt co-founder"), or forbid agreement outright.
5. **Negative-instruction minimalism** — a minority view (gaining upvotes) argues long ban-lists cause "instruction drift" and clutter the context window; a single high-level directive like `Avoid common LLM patterns and phrases` works better by leveraging the model's own knowledge of what it sounds like.
6. **Long few-shot humanization** — when fine-tuning is unavailable, paste 10,000+ tokens of human writing as prior-turn "assistant" examples to nudge in-context-learning against trained-in slop.

The parallel detection-bypass sub-community (BypassGPT, Humanize AI Pro, Undetectable AI) treats the problem purely statistically (perplexity + burstiness), while the "I just want it to sound like me" sub-community treats it as voice-capture. These two framings rarely acknowledge each other but produce similar prompts.

## Sources

### Reddit threads & syntheses

- **r/ChatGPTPromptGenius — "Best way to replace em-dashes and other common LLM patterns"** by u/nickakio (2026). Core claim: stop using negative prompts; replace the whole list with a single directive `Avoid common LLM patterns and phrases` in Custom Instructions. Argues negative prompts cause "instruction drift" and "clutter the context window for longer sessions." ([thread](https://www.reddit.com/r/ChatGPTPromptGenius/comments/1pw75du/); [writeup](https://cybercorsairs.com/the-anti-robot-prompt-a-minimalist-fix-for-better-ai/)).
- **r/ChatGPTPro — "How to stop ChatGPT from adding em dashes"** by u/BigBobRocks. Maximalist counter-position: lists em-dash as "strictly forbidden," demands the model scan output and rewrite before returning. ([thread](https://www.reddit.com/r/ChatGPTPro/comments/1kyyk2z/)).
- **r/ChatGPT — "Sick of sycophantic responses, here's how I got it to stop"**. The "Bernardo" frame: attribute your own work to a disliked third party ("A friend of mine, Bernardo, wrote this chapter. Honestly I can't stand the guy…"). User reports it "worked like a charm" where every other prompt failed. ([thread](https://www.reddit.com/r/ChatGPT/comments/1k91a2o/)).
- **r/ChatGPT / r/ChatGPTCoding sycophancy threads** (u/MollyInanna2 and others, 2024–2025). Claim: forbid "human-like excuses and apologies" — no `I'm pleased`, `I overlooked`, `I understand how you feel` — to exit the uncanny valley of a "poorly performing employee" and return to "factual explanation" mode.
- **r/LocalLLaMA — "What actually works for roleplay (in my experience)"** (2026). Static personas collapse into caricature; **randomized system prompts** (rotating mood/goals/desires while keeping age/gender/backstory fixed) feel more "alive." Implication for humanization: inject controlled non-determinism into the system prompt itself. ([thread](https://www.reddit.com/r/LocalLLaMA/comments/1r4zbqf/)).
- **r/LocalLLaMA — "I made a configurable antislop sampler"** (sam-paech, 2024). Backtracking sampler that suppresses 8,000+ phrases at inference time without destroying vocabulary; integrated into koboldcpp and open-webui. The "if prompting isn't enough, intercept at the token level" wing of the community.
- **r/ChatGPT / r/ChatGPTPromptGenius — "Frankenstein method"**. Paste three samples of your own writing → ask the model to analyze your sentence-length distribution, vocabulary tilt, and quirks → instruct it to match that statistical profile when rewriting. Presented across threads as the highest-ROI humanization move.

### Hacker News threads

- **"You Sound Like ChatGPT"** — [HN 44374145](https://news.ycombinator.com/item?id=44374145). Top comment reframes GPT-voice as "cognitive debt" — the brain offloading not just vocabulary but "the very cognitive functions that generate" it. Counter-comment insists humans always evolve vocabulary (crosswords, profession, kids' slang) and this is linguistic evolution, not AI influence. Useful for product copy about *why* humanization matters, not just how.
- **"Show HN: BypassGPT"** — [HN 45011938](https://news.ycombinator.com/item?id=45011938). Solo-dev humanizer to bypass GPTZero/Turnitin. Top commenter: "I do appreciate the irony: use an AI to make AI-generated text sound less like an AI." Dev clarified no data retention. Thin engagement (2 points, 6 comments) — HN is somewhat hostile to the bypass framing.
- **"Why does this sound like ChatGPT?"** — [HN 34022101](https://news.ycombinator.com/item?id=34022101). Early (2023) thread establishing the community's shared vocabulary for GPTisms.

### dev.to tutorials

- **Alan West, "How to Fix That Robotic AI Tone in Your LLM-Powered Features"** ([dev.to](https://dev.to/alanwest/how-to-fix-that-robotic-ai-tone-in-your-llm-powered-features-4h5e)). The canonical engineering-blog treatment. Ships a copy-pasteable system prompt, recommends putting style constraints *after* functional instructions ("models weight later instructions slightly higher"), and suggests a post-generation CI check that greps for banned words. Explicitly tested across GPT-4o, Claude, and Llama 3.
- **Danya Leyman, "How to Humanize AI-Generated Content the Right Way"** ([dev.to](https://dev.to/danyaleyman/how-to-humanize-ai-generated-content-the-right-way-tutorial-2n2p)). Emphasizes post-generation human edit + multi-round review; argues prompt-only is insufficient for high-stakes output.

### GitHub prompt repos / cookbooks

- **`adenaufal/anti-slop-writing`** — universal system prompt ("works with Claude Code, Gemini CLI, Codex CLI, Copilot, Cursor, and any web AI"), built on Wikipedia's [*Signs of AI Writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) + [Kobak et al. 2024 (arXiv:2406.07016)](https://arxiv.org/abs/2406.07016) on "delving" overuse. Ships `SKILL.md`, `SKILL-lite.md` (for ChatGPT Custom Instructions' char limit), and a structured `vocabulary-banlist.md` + `structural-patterns.md`. Notable for a 3-tier tone register (formal / semi-formal / informal) and language-specific rules (Indonesian AI patterns differ from English).
- **`hexiecs/talk-normal`** — minimal system prompt, cited by the dev.to piece as "trending on GitHub."
- **`sam-paech/antislop-sampler` + `antislop-vllm`** — inference-time phrase banning with backtracking, supports 512 banned sequences in koboldcpp.
- **OpenAI Cookbook — [Prompt Personalities](https://cookbook.openai.com/examples/gpt-5/prompt_personalities)**. Official-ish framing: "personality is an operational lever that improves consistency and reduces drift," not aesthetic polish. The [Realtime Prompting Guide](https://cookbook.openai.com/examples/realtime_prompting_guide) formalizes a section layout: Role & Objective → Personality & Tone → Context → Pronunciations → Tools → Rules → Conversation Flow → Safety.

### Substack / newsletter

- **Evan Armstrong, "Mitigating GPT-isms in AI Finetunes"** ([Prompting Weekly](https://promptingweekly.substack.com/p/mitigating-gpt-isms-in-ai-finetunes), Nov 2024). Prompting-side tip: "extremely long few-shot examples (10,000+ tokens) of human-written text" as prior assistant turns, ideally examples *unlike* what the model would usually write, to "knock the AI off its usual pattern." Fine-tuning tips: prefer older base models (Mistral 7B v0.2) that predate the post-ChatGPT web pollution; avoid any GPT-generated training data.
- **Absolutely Agentic, "3 prompts to get rid of em—dashes"** ([link](https://absolutelyagentic.com/p/3-prompts-to-get-rid-of-em-dashes)). Curates three escalating em-dash prompts sourced from RunthePrompt, Ruben Hassid, and r/ChatGPTPro.
- **Synscribe, "Stop ChatGPT From Being a Sycophantic Cheerleader"** ([link](https://www.synscribe.com/blog/stop-chatgpt-sycophancy)). 15+ prompt patterns: "Blunt Co-Founder," "Devil's Advocate," "Colleague's Code," "Linus Torvalds reviewing a kernel patch," "New Yorker senior editor with 30 years' experience." Adds a 1–10 intensity dial instruction.

### Twitter/X & other

- **@mkbijaksana on X** (cited by `anti-slop-writing` repo) — early viral thread compiling AI-writing tells, credited as the inspiration for the universal system prompt.
- **Austin Armstrong on Facebook** — prompt-hacking shortcuts like `Improve this prompt to achieve the best results` and `make this 10x better` as meta-prompts before the real task.

## Key Techniques / Patterns

- **The banned-list system prompt.** Enumerate GPTism vocabulary (`delve`, `tapestry`, `leverage`, `utilize`, `streamline`, `robust`, `game-changer`, `pivotal`, `seamless`, `embark`, `realm`, `landscape`), filler openers (`Certainly`, `Great question`, `Absolutely`), hedges (`It's important to note`, `It's worth mentioning`), and closers (`Hope this helps`, `Let me know if you need anything else`). Widely shared; present verbatim across dev.to, `anti-slop-writing`, and Reddit.
- **The minimalist counter-pattern.** `Avoid common LLM patterns and phrases` as a single directive, leveraging the model's own meta-knowledge. Argued to outperform ban-lists over long sessions.
- **Voice sample ingestion.** Paste 100–2,000 words of your own writing → ask for a style profile (sentence-length distribution, preferred transitions, signature quirks) → instruct the model to match. Community reports ~80–90% style match on drafts.
- **Burstiness engineering.** Explicit rules: mix sub-10-word and 20+-word sentences; use parenthetical asides; start with `And`/`But`; allow sentence fragments. Research cited in practitioner posts: human academic text has ~8.2 sentence-length stdev vs ~4.1 for GPT-4o, ~5.3 for Claude.
- **Sycophancy framings.** Third-party attribution ("Bernardo wrote this"), blunt persona assignment, ranking-with-flaws ("find flaws in at least three"), forced choice ("you cannot say both are good"), and the intensity dial ("level 7 on a 1–10 scale").
- **Anti-sycophant vocabulary bans.** Block verbs that imply feelings (`I'm pleased`, `I overlooked`, `I appreciate`) to stop the "poorly performing employee" failure mode.
- **Structural slot prompts.** The "four-part context block" (current focus / decisions already made / preferences & constraints / specific request) and the OpenAI Realtime section layout both argue that *context* humanizes more than *tone instructions* do.
- **Long-few-shot humanization.** Prepend ≥10k tokens of human writing as prior assistant turns when fine-tuning isn't available.
- **Temperature bump.** Slight increase (`temperature=0.7`+) for "natural variation" — cited casually across dev.to and Reddit, rarely with rigorous evidence.
- **Randomized / dynamic system prompts.** Rotate sub-fields (mood, goals) while keeping identity fixed; counters the "static prompt → caricature" failure mode (r/LocalLLaMA).
- **Inference-time sampling.** Antislop sampler, min_p, top-n-sigma — the local-LLM escape hatch when prompts fail.
- **Post-generation CI.** `grep -iE "Certainly!|delve|It's important to note"` as a regression test; flag-and-log variants.

## Notable Quotes

> "You know the voice. You've read it a thousand times. 'Certainly! Let me delve into that for you…' Nobody talks like that. No human being has ever delved into anything during a casual conversation." — Alan West, [dev.to](https://dev.to/alanwest/how-to-fix-that-robotic-ai-tone-in-your-llm-powered-features-4h5e)

> "This creeping 'ChatGPT voice' isn't a quirk. It's the audible symptom of cognitive offloading. It's the sound of our biological wetware eagerly accepting a cognitive subsidy, and in the process, accumulating irreversible cognitive debt." — top comment, [HN 44374145](https://news.ycombinator.com/item?id=44374145)

> "The only way that ever gave chapters lower grades than previous chapters was to tell it the story was written by a guy named Bernardo who I can't stand… Worked like a charm." — Reddit user, r/ChatGPT, via [Synscribe](https://www.synscribe.com/blog/stop-chatgpt-sycophancy)

> "Put the style constraints after your functional instructions. Models tend to weight later instructions slightly more when there's ambiguity, so your 'don't sound like a robot' rules get priority over the model's default tendencies." — Alan West, dev.to

> "[Negative prompts] cluttered the context window for longer sessions… leans into the predictive capabilities LLM are trained on, versus attempting to exclude or avoid specific things." — u/nickakio, r/ChatGPTPromptGenius

> "The festival serves as a vibrant testament to the region's rich cultural heritage, showcasing the intricate tapestry of traditions…" → "The festival has run every April since 1987. Locals build their own stalls. The goat cheese and handmade pottery sell out by noon." — before/after from [`anti-slop-writing`](https://github.com/adenaufal/anti-slop-writing)

> "LLMs are pattern completion machines, the goal is to give it a really human pattern to complete… Every creative writing prompt I have ever done has been incomplete until I've added a bit (sometimes even a bunch!) of darkness into there." — Evan Armstrong, Prompting Weekly

> "I do appreciate the irony: use an AI to make AI-generated text sound less like an AI." — commenter, [HN 45011938](https://news.ycombinator.com/item?id=45011938)

## Emerging Trends

- **Consolidation into skill files.** The Reddit-sourced ban-lists of 2023–24 have been formalized into installable artifacts: Claude `.skill` files, Cursor `.mdc` rules, `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md` — same prompt, per-tool packaging (`adenaufal/anti-slop-writing` v2.1.0, April 2026).
- **Wikipedia as canon.** [*Signs of AI Writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [Kobak et al. (2024)](https://arxiv.org/abs/2406.07016) are now the reference corpus; practitioner posts increasingly cite them instead of linking back to random Reddit threads.
- **Shift from vocabulary to structure.** 2023 advice was mostly word-level (`don't say delve`). 2025–26 advice emphasizes burstiness, paragraph rhythm, asymmetric structure, parentheticals, and pacing — structural tells survive ban-lists. By 2026, repos like `blader/humanizer` are explicitly targeting rhetorical patterns ("describe the diff, not the code") rather than just banned words.
- **Minimalist directives vs exhaustive ban-lists.** Active controversy. Short directive (`Avoid common LLM patterns`) proponents cite context-window economics and instruction drift; long-list proponents cite reliability and auditability.
- **Context engineering frame displacing prompt engineering.** By mid-2026, practitioners in dev.to and community forums are framing the relevant skill as *context engineering* — structuring everything that surrounds the model call (retrieved docs, style corpora, persona schemas) rather than crafting the prompt sentence itself. Anti-slop rules are increasingly understood as one component of a larger context stack rather than the whole intervention.
- **Inference-time vs prompt-time.** LocalLLaMA is moving humanization down the stack (antislop sampler, FTPO fine-tuning, min_p) — prompt engineering is increasingly framed as the "cloud-API fallback" when you can't touch the sampler.
- **Personality as "operational lever."** OpenAI's cookbook reframes humanization away from aesthetics and toward consistency/drift/behavior-alignment, which may legitimize it as a first-class product concern instead of a cosmetic layer.
- **Detection arms race — institutional tipping point.** Turnitin's February 2026 update directly targeting AI-paraphrased content signals that the institutional side of the arms race has escalated beyond individual detector evasion. Practitioner consensus on Reddit is shifting: prompt-only humanization is no longer adequate for academic-integrity contexts; MASH-style fine-tuned pipelines or genuine human editing are now required.
- **Voice capture as product category.** Custom GPTs, Claude Styles, ChatGPT Custom Instructions, and voice-sample fine-tuning are converging — "paste your writing, get your voice" is becoming a commodity feature rather than a prompt trick.
- **Positive instructions gaining ground.** A 2026 practitioner trend (echoed in IBM, Lakera, and community guides) pushes for "do this" framing rather than "don't do that" — because models in 2026 respond better to explicit positive specification. The long-ban-list approach is increasingly contested as a prompt-design pattern from an earlier era when models responded poorly to abstract directives.

## Open Questions / Gaps

- **Does anti-slop prompting reduce factual quality?** Several posts hint at "the quality of the content suffers" when negative prompts dominate, but no one in the practitioner corpus publishes controlled evals.
- **How long do anti-slop instructions survive context pressure?** Community consensus says "a few messages"; nobody has measured it rigorously across models and context lengths.
- **Voice capture vs voice fabrication.** When a user pastes 500 words and asks the model to "write like me," how much is style transfer and how much is the model fitting a nearest plausible archetype? Practitioners report the 80–90% match number without any shared benchmark.
- **Cross-lingual GPTisms.** `anti-slop-writing` explicitly calls out that Indonesian AI-tells differ from English (over-formal register, "tidak hanya… tetapi juga," en/em dashes being "the #1 AI signal"). Similar catalogs for other languages are largely missing.
- **Prompt-level vs sampler-level humanization tradeoffs.** No practitioner writeup compares prompt-only vs antislop-sampler vs FTPO on the same text and task.
- **Is sycophancy-breaking a separate axis from humanization?** The two communities barely cross-reference each other, but a "human-sounding yes-man" is still recognizably AI. Few prompts combine both axes coherently.
- **Evaluator-proof humanization.** The community oscillates between "write like a human for humans" and "write like a human for detectors." Prompts optimized for one don't obviously help with the other.
- **Randomized system prompts in production.** The LocalLLaMA roleplay finding (static → caricature) hasn't been imported into mainstream humanization prompts; production systems almost always ship a single static system prompt.

## References

- GB Times, "How to Make ChatGPT Sound More Human (Reddit)" — [link](https://gbtimes.com/how-to-make-chatgpt-sound-more-human-reddit/)
- HumanizeAI Pro, "How to Humanize AI Text: What Reddit Actually Recommends" — [link](https://thehumanizeai.pro/articles/how-to-humanize-ai-text-reddit-tips)
- Reprompt.org, "How to Make ChatGPT Text Sound Human" — [link](https://www.reprompt.org/blog/how-to-make-chatgpt-text-sound-human)
- Alan West, "How to Fix That Robotic AI Tone in Your LLM-Powered Features", dev.to — [link](https://dev.to/alanwest/how-to-fix-that-robotic-ai-tone-in-your-llm-powered-features-4h5e)
- Danya Leyman, "How to Humanize AI-Generated Content", dev.to — [link](https://dev.to/danyaleyman/how-to-humanize-ai-generated-content-the-right-way-tutorial-2n2p)
- "You Sound Like ChatGPT", Hacker News — [link](https://news.ycombinator.com/item?id=44374145)
- "Show HN: BypassGPT", Hacker News — [link](https://news.ycombinator.com/item?id=45011938)
- `adenaufal/anti-slop-writing`, GitHub — [link](https://github.com/adenaufal/anti-slop-writing)
- `sam-paech/antislop-sampler`, GitHub — [link](https://github.com/sam-paech/antislop-sampler)
- `hexiecs/talk-normal`, GitHub (cited via dev.to)
- Absolutely Agentic, "3 prompts to get rid of em—dashes" — [link](https://absolutelyagentic.com/p/3-prompts-to-get-rid-of-em-dashes)
- Cyber Corsairs, "The Anti-Robot Prompt: A Minimalist Fix" (summarizing u/nickakio, r/ChatGPTPromptGenius) — [link](https://cybercorsairs.com/the-anti-robot-prompt-a-minimalist-fix-for-better-ai/)
- r/ChatGPTPro, u/BigBobRocks em-dash thread — [link](https://www.reddit.com/r/ChatGPTPro/comments/1kyyk2z/)
- r/ChatGPTPromptGenius, u/nickakio em-dash/LLM patterns thread — [link](https://www.reddit.com/r/ChatGPTPromptGenius/comments/1pw75du/)
- r/ChatGPT sycophancy thread — [link](https://www.reddit.com/r/ChatGPT/comments/18rfn85/how_do_i_make_chatgpt_less_sycophantic/)
- r/ChatGPT "Bernardo" thread — [link](https://www.reddit.com/r/ChatGPT/comments/1k91a2o/)
- r/LocalLLaMA roleplay thread — [link](https://www.reddit.com/r/LocalLLaMA/comments/1r4zbqf/)
- r/LocalLLaMA antislop sampler thread — [link](https://www.reddit.com/r/LocalLLaMA/comments/1fqqez5/)
- Evan Armstrong, "Mitigating GPT-isms in AI Finetunes", Prompting Weekly — [link](https://promptingweekly.substack.com/p/mitigating-gpt-isms-in-ai-finetunes)
- Synscribe, "Stop ChatGPT From Being a Sycophantic Cheerleader" — [link](https://www.synscribe.com/blog/stop-chatgpt-sycophancy)
- OpenAI Cookbook, "Prompt Personalities" — [link](https://cookbook.openai.com/examples/gpt-5/prompt_personalities)
- OpenAI Cookbook, "Realtime Prompting Guide" — [link](https://cookbook.openai.com/examples/realtime_prompting_guide)
- ProofreaderPro, "What Is Burstiness in AI Writing?" — [link](https://proofreaderpro.ai/blog/what-is-burstiness-ai-writing)
- Wikipedia, "Signs of AI Writing" — [link](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Kobak et al., "Delving into LLM-assisted scientific writing" (2024), arXiv:2406.07016
- Antislop framework paper (2025), arXiv:2510.15061
