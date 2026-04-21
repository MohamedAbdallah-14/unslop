# Creative Writing & Storytelling — Practical How-Tos & Forums

**Research value: high** — The AI-writing practitioner forums (r/WritingWithAI, r/NovelAi, r/SillyTavernAI, r/CharacterAI, r/KoboldAI, r/WritingPrompts), Hacker News creative-writing debates, and Substack "voice" essayists have converged on a narrower, more fiction-specific playbook than the general-purpose prompt communities — one centered on **structure over vocabulary**, **interview-driven voice capture**, and **character-card craft** — with a clear split between "AI as drafter" (Sudowrite/NovelCrafter/NovelAI) and "AI as final editor only" (the Substack purist wing).

**Last updated: April 2026.**

## Executive Summary

The creative-writing sub-communities are past the em-dash wars of the general-prompt subs and have moved on to more craft-specific problems. Five recurring patterns:

1. **Structure beats vocabulary.** The most-upvoted r/WritingWithAI posts of the last year argue that "robotic writing" is about uniform sentence lengths, clean transitions, and chapters that resolve too tidily — not about the word `delve`. Fixing burstiness (sentence-length variance) and leaving conflicts *unresolved* at scene breaks are the high-ROI moves.
2. **Interview-the-writer beats show-the-writer.** The 2026 Substack consensus (Steph Pajonas, Ruben Hassid, Ina Toncheva, "The AI Girl") is that pasting 5 samples of your writing produces generic Claude-mimicry; letting Claude *interview you* for 30–50 minutes and saving a "Voice DNA" `.md` file produces voice that survives across tools. Core insight: **taste is defined by what you reject**, not what you like.
3. **Character-card craft is a genre of its own.** r/SillyTavernAI / r/CharacterAI have developed surprisingly literary conventions: dump adjective lists → replace with behavioral clauses ("She deflects emotional moments with cutting jokes — not because she doesn't care, but because sincerity makes her uncomfortable"). Example-dialogue fields are treated as few-shot voice training.
4. **Platform fragmentation matters.** NovelAI (Kayra/Erato) has its own vocabulary: ATTG metadata (`[Author; Title; Tags; Genre]`), Memory vs Author's Note position weighting, `[S:X]` quality tags, curly-brace instructions. Sudowrite Muse ships a "Creativity Dial" and cliché-reduction training. SillyTavern uses regex post-processors. Humanization advice is increasingly **tool-specific**.
5. **r/WritingPrompts banned it outright.** The purist end of the spectrum: "You are not allowed to use AI in this subreddit, you will be banned." Meanwhile r/NoSleep went from 4.2% AI in 2020 to 41% in 2024. The subreddits are now sorting themselves into pro-AI craft communities and AI-forbidden pure-human communities, with different humanization stakes in each.

The Hacker News thread is dominated by an older debate: *whether* AI can write good fiction at all, not *how* to humanize it. The practitioner view ("months of supervision can produce New Yorker-quality work") coexists uneasily with the detector view ("it's upbeat, cheery, consistent metaphors, flowery — it hides incompetence with fluency").

## Sources

### Reddit — r/WritingWithAI (~25k members, pro-AI craft community)

- **"I realized most 'robotic' writing isn't about vocabulary"** ([r/WritingWithAI, 1r9r6gk](https://www.reddit.com/r/WritingWithAI/comments/1r9r6gk/i_realized_most_robotic_writing_isnt_about/)). The most-cited 2026 reframing. OP argues the robotic feel comes from uniform sentence lengths, perfectly smooth transitions, and paragraphs that resolve too cleanly — not from individual words. Research-adjacent claim reproduced in downstream posts: human academic text has ~8.2 sentence-length stdev, GPT-4o ~4.1. Fix: mix sub-10-word and 20+-word sentences, use em-dashes/semicolons to stitch short sentences, let paragraphs end mid-thought. This finding is now independently corroborated by the PNAS "Echoes in AI" paper (2025), which documents that LLM plot diversity collapse operates at the structural, not lexical, level.
- **Chet Day, "Why r/WritingWithAI Is Different: A 77-Year-Old AI Author's Take"** ([chetday.com](https://chetday.com/r-writingwithai-review-ai-author/)). Ethnographic snapshot: "Instead of 'You're cheating,' I got 'Have you tried experimenting with different temperature settings for historical accuracy?'" Community norms: share prompts, share failures, disclose your AI involvement, ask targeted questions ("How do you maintain character voice consistency across chapters?") not philosophical ones.
- **"I like using AI to discuss ideas and to generate outlines but I do not want it to write the draft"** ([1r2d63h](https://www.reddit.com/r/WritingWithAI/comments/1r2d63h/)). Representative of the "scaffold-only" wing: AI for brainstorming, outline-generation, and research; human writes every sentence. The counter-wing ("let AI draft, I revise") is equally visible but produces different humanization advice.

### Reddit — r/NovelAi (Kayra/Erato, prose-first)

- **"Resubbed after a few months, better but struggling with coherence"** ([qzje9m](https://www.reddit.com/r/NovelAi/comments/qzje9m/resubbed_after_a_few_months_better_but_struggling/)). Canonical "your input IS the style" thread. Core claim: NovelAI mimics your prose more directly than other tools, so sloppy input = sloppy output. Start with no modules, use Fresh Coffee/Green Tea presets, accept purple prose is a Kayra/older-model problem and switch to Claude Opus for revision.
- **"Pretty new to this… how do I give short instructions and get a scene?"** ([1i9pwvi](https://www.reddit.com/r/NovelAi/comments/1i9pwvi/)). Teaches the community's two standard inline instruction formats: `***` (dinkus) followed by a scene summary, and bracketed direction `[ Next: X happens ]`.
- **"Accidentally generated but don't know the prompt(s)"** ([y18dcz](https://www.reddit.com/r/NovelAi/comments/y18dcz/)). Community reverse-engineers style from an output — surfaces the ATTG metadata recipe (`[ Author: X; Title: Y; Tags: Z; Genre: W ]`) and style tags (`[ S: 4 ]`, `[ Style: verbose ]`).
- **[NovelAI docs on Memory vs Author's Note](https://docs.novelai.net/en/text/specialsymbols/)** ([context explainer](https://tapwavezodiac.github.io/novelaiUKB/Context.html)). The position-weighting rule practitioners teach newcomers: Memory goes at the top (weakest influence, holds metadata), Author's Note is inserted 3 paragraphs before the last token (strongest influence, holds POV/date/style overrides). "Text closer to the bottom of context has stronger influence than text at the top" — applied to any long-context LLM, not just NovelAI.

### Reddit — r/SillyTavernAI (roleplay, natural dialogue)

- **"What do you guys think of the instruction?"** ([1rbbsfk](https://www.reddit.com/r/SillyTavernAI/comments/1rbbsfk/what_do_you_guys_think_of_the_instruction/)). Widely forked anti-slop system prompt. Forbids "Purple prose, Archaic phrasings, Excessive metaphors, Sensory overload disguised as depth." Hard rules: characters can't read the user's internal thoughts; dialogue must have hesitations/interruptions; characters keep their own vocabulary patterns; "meaningful small details (a twitch, a glance, voice catching)" replace generic sensory dumps.
- **"How do you guys combat purple prose?"** ([1fx8fck](https://www.redditmedia.com/r/SillyTavernAI/comments/1fx8fck/how_do_you_guys_combat_purple_prose/)). Community answer is tiered: (1) upgrade model — Claude Opus+ has less purple prose; (2) regex post-processors in SillyTavern ([PR #3581](https://github.com/SillyTavern/SillyTavern/pull/3581)) to strip recurring phrases; (3) inject explicit bans in the author's-note slot.
- **"GLM 5: Great dialogue, but how to get longer, more descriptive narration?"** ([1r5drao](https://www.reddit.com/r/SillyTavernAI/comments/1r5drao/)). Source of the rejected-minimalist-fragments advice: block `A beat.`, `A pause.`, `A breath.` — AI fills these in for free but they read as filler. Force 500-word minimum, require beats to be "integrated into developed prose."
- **"SillyTavern Character Generator v2 - does it all"** ([1r8go10](https://www.reddit.com/r/SillyTavernAI/comments/1r8go10/)). Token budgets for character cards: Description 250–400 tokens (1–2 physical features, 2–3 core traits max), Personality 30–80 tokens, Example Dialogue 2–3 exchanges only (more hurts). "Details at the start of your persona are remembered better, so lead with facts."
- **RP|Fiend, ["How To Write a SillyTavern Character Card That Actually Has Soul"](https://rpfiend.com/how-to-write-a-sillytavern-character-card/)**. The canonical reference. Before/after example: `cold, reserved, fierce` → `She doesn't flinch. Not at threats, not at raised voices, not at the kind of silence that makes other people nervous. She's spent enough years in rooms where the wrong reaction gets you killed that stillness became a survival mechanism.` Test: "If an actor received this card as their only direction, could they perform it consistently?"

### Reddit — r/CharacterAI, r/KoboldAI, r/WritingPrompts

- **r/CharacterAI prompt community** ([guide roundups](https://characterai.it.com/advanced-character-ai-prompt-engineering-2026-guide/), [personas testing](https://aitipsters.com/testing-character-ai-personas/)). Dominant patterns: structured label-value personas (`Name | Role | Fear | Voice`) outperform narrative blurbs; layer emotional context over role ("weary king who recently survived betrayal"); memory-reinforcement mid-chat ("You're [X] — dry wit, hates small talk. Let's pick back up from that energy") to counter drift.
- **r/KoboldAI — [Settings wiki](https://github.com/KoboldAI/KoboldAI-Client/wiki/Settings) / [community-recommended sampler order](https://koboldai.com/KoboldAILite/)**. Creative-writing defaults: Top-P 0.92, Temperature 0.7, Rep Penalty 1.1, sampler order `[6,0,1,3,4,2,5]`. Min_P is the newer community darling (not covered in the official wiki but dominant in 2026 LocalLLaMA posts) — intuition: discard improbable tokens relative to the *top* token, which preserves creativity under higher temperatures better than Top-P.
- **r/WritingPrompts anti-AI stance** ([user_guide wiki](https://old.reddit.com/r/WritingPrompts/wiki/user_guide); [Cornell summary of mod concerns](https://news.cornell.edu/stories/2025/10/ai-generated-content-triple-threat.html)). Explicit ban, bannable offense: "you are not allowed to use AI in this subreddit, you will be banned." Mods report AI responses "often contain glaring errors in both style and content." Useful counterweight: these are the readers your "humanized" output is being judged against.
- **Context — [174% rise in AI content across writing subreddits, Originality.ai](https://originality.ai/blog/ai-in-writing-subreddits)**. r/NoSleep went from 4.2% (2020) to 41.39% (2024) AI. r/Fantasy from 1.1% (2023) to 10.9% (2024). The enforcement asymmetry (r/WritingPrompts zero-tolerance vs r/NoSleep half-AI) is already splitting the creative-writing corpus. Cornell Chronicle's Oct 2025 study identifies AI-generated content as a "triple threat" to Reddit moderators: volume, detection difficulty, and social-trust erosion.

### Hacker News creative-writing debates

- **"Ok, AI Can Write Pretty Good Fiction Now"** ([HN 44455193](https://news.ycombinator.com/item?id=44455193)). Top commenter disagrees with a blog-post critic who wanted the line `She could tell from the particular way he moved around the counter, post-endorphins quiet` cut: "I found it to be thoughtful and the most human line of the story / the one that best mimicked real prose." Useful for distinguishing *AI slop* from *AI-voicing real interior observation*. Also: name ambiguity ("Sam") as a "trickery very common in real prose."
- **"When GPT-4.5 came out, I used it to write a couple of novels for my son"** ([HN 47304600](https://news.ycombinator.com/item?id=47304600)). Agent-of-specialists pattern: separate SKILL.md files for `planner / author / editor / lore keeper / plot consistency checker`. Produced "better than the median novel aimed at my son's age group," but: "good enough that he finished reading them once, but not good enough that he would recommend them or re-read them." Honest data point on the current ceiling.
- **"I let Claude Code write an entire book"** ([HN 44134677](https://news.ycombinator.com/item?id=44134677)). 83 comments. Notable framing: "human hallucinations are fundamentally social" (social validation at gatherings) vs AI hallucinations occurring in isolation — read as a literary-voice commentary, human voice is partly a record of *being corrected by other humans*, AI voice isn't.
- **"My experience trying to write human-sounding articles using Claude AI"** ([HN 38382067](https://news.ycombinator.com/item?id=38382067)). Foundational 2023 thread. Core grievance: RLHF / safety tuning produces "censored" prose that can't commit to a voice. Claude-specific: overhedging, multiple-perspectives-offered, reflexive disclaimers.
- **"Ask HN: How would you describe the way AI writes versus a human?"** ([HN 43523658](https://news.ycombinator.com/item?id=43523658)). Clean enumeration of tells: "upbeat and cheery," "won't complain about things," "unusually consistent metaphors," "overly flowery language," "hides lack of competence through fluency."
- **"Warranty Void If Regenerated"** ([HN 47431237](https://brianlovin.com/hn/47431237)). Author spent months polishing Claude-drafted fiction; readers didn't realize it was AI until the comments. Counter-framing: "months of supervision, guidance, and human intent" — "AI-generated" is the wrong unit; the unit is author-AI collaboration time.
- **"Ok, AI Can Write Pretty Good Fiction Now"** ([HN 44455193](https://news.ycombinator.com/item?id=44455193)). Top commenter defends the line "She could tell from the particular way he moved around the counter, post-endorphins quiet" as the most human line in the story, against a critic who wanted it cut. Also surfaces name ambiguity ("Sam") as a "trickery very common in real prose" — a structural humanness signal that most ban-lists miss.
- **"LLM voice" comment thread** ([HN 47571783](https://news.ycombinator.com/item?id=47571783)). Dissenting argument the humanization community should engage: the recognizable "LLM voice" resembles *effective public-communication prose*, and dismissing it risks pushing writers to deliberately write worse to avoid the signature.

### Substack — voice, interview method, anti-slop

- **Steph Pajonas, "The Interview Is the Secret"** ([spajonas.substack.com](https://spajonas.substack.com/p/the-interview-is-the-secret-how-i), Mar 2026). Four-step process: (1) bring a topic + gut-feel brief, (2) let AI interview you while you *talk-to-text and rant into your phone*, (3) AI drafts from your answers + style guide, (4) hand-edit every line. Personal AI-ism blocklist: "`It's not X. It's Y.`", "`Here's what I learned:`", any mid-article summarization.
- **Ruben Hassid, "I am just a text file"** ([ruben.substack.com](https://ruben.substack.com/p/i-am-just-a-text-file)) + [X thread](https://substack.com/@ruben/note/c-205779383). Viral origin of the "Voice DNA" `.md` pattern: Claude interviews you for 30–50 min → save answers as `voice.md` → upload to any AI going forward. Core claim: "taste is defined by what you *reject*, not what you like."
- **Ina Toncheva, "How to Make Claude Write Like You: The Interview Method"** ([inatoncheva.substack.com](https://inatoncheva.substack.com/p/how-to-make-claude-write-like-you-the-interview-method)). Extends the method with a specific failure analysis of the naive "give 5 samples" approach: most writers don't have clean samples, their writing is inconsistent, contaminated by prior AI edits, or they can't explain what makes their writing good.
- **Paulina Martinez, "No AI Slop: Writing With AI Without Losing Your Voice"** ([wespeakhuman.substack.com](https://wespeakhuman.substack.com/p/no-ai-slop-writing-with-ai-without), Feb 2026). Purist wing: "I write the text, I rewrite it, and *then, and only then*, do I bring in the AI for a final revision. No Prompt and Publish." Also documents "model decay": LLMs "get dumb" mid-workflow, forgetting context — switch models when you notice it.
- **Cozora / Nick Quick + Daniel Nest, "AI Writing Without the Slop"** ([cozora.substack.com](https://cozora.substack.com/p/ai-writing-without-the-slop), Apr 2026). Introduces the **VAST framework**: Vocabulary, Architecture, Stance, Tempo — four dimensions of voice that must be encoded before the AI touches the draft. Headline insight: "The writers beating AI slop aren't using better prompts — they're using better systems. The tools are commodities. The voice isn't."
- **Kelly Balthrop, "Writing Fiction with Claude"** ([wbalthrop.substack.com](https://wbalthrop.substack.com/p/writing-fiction-with-claude)). Fiction-specific Claude failure modes + fixes: (1) **timeline confusion** — Claude treats all narrative info as equally current, needs a "Mental Framework Prompt" distinguishing past/future events; (2) **current-state summary block** prefixed to each new chapter; (3) detailed voice instructions to avoid generic-language default.
- **Rebecca Dugas, "Stop Your Writing from Sounding Like AI"** ([youraicopyeditor.substack.com](https://youraicopyeditor.substack.com/p/stop-your-writing-from-sounding-like)). Copyeditor's field taxonomy of AI-isms: overly flowery language, the `"It's not X — it's Y"` structure ("Chat loooooves it"), colon-separated two-part titles, vague platitude closers, filler conversational phrases when "make it conversational" is requested.
- **Nick Garnett, "How I Overcame Producing AI Slop"** ([nickgarnett.substack.com](https://nickgarnett.substack.com/p/how-i-overcame-producing-ai-slop)). Five tactics: specify length/angle/audience/tone explicitly; do your own research first; give instructions rather than asking questions; use a system prompt to set rules upfront; rewrite before publishing.
- **Ligma Blog, "The Way of the Voice in AI Prompts — A Field Guide"** ([ligma.blog/post4](https://ligma.blog/post4/)). Decomposition of "voice" into addressable axes: punctuation habits, sentence-length rhythm, word choice register, tone, metaphor density. Recommends placing instructions at both top and bottom of long prompts, and using Claude Projects / ChatGPT Custom Instructions for persistent voice rather than ad-hoc prompting.

### YouTube — author tutorials

- **The Nerdy Novelist (YouTube channel).** Canonical author-creator on AI fiction. Recommends Claude over ChatGPT for creative writing ("the best LLM family for creative writing"). Signature techniques: create a style-guide prompt with sample chapters as context (works especially well on Claude 3+); add the author as a Codex character in NovelCrafter to inject author perspective; use Global Entries as persistent voice anchors. Exemplar video: ["Every Author Should Use this ChatGPT Prompt (Insane Story Bibles)"](https://www.youtube.com/watch?v=6_ZqwscNZGk).
- **Joanna Penn / The Creative Penn.** "AI-Assisted Artisan Author" framing ([Author Media interview](https://www.authormedia.com/the-authors-guide-to-ai-with-joanna-penn/); [YouTube](https://www.youtube.com/watch?v=cYqaTuXaJ6A)). Core advice: "double down on being human" — write only books you can write, with personal elements only you can provide. On character voice: "Metaphor Families" that anchor each character's dialogue ([The Creative Penn, Mar 2026](https://www.thecreativepenn.com/2026/03/16/writing-characters-15-actionable-tips-for-writing-deep-character/)).
- **Sudowrite 101 tutorial channel** ([Sudowrite 101 tutorial](https://www.youtube.com/watch?v=DJVg09qsHeM)). Teaches the "super prompt" Story Engine pattern: upload Story Bible + Style Examples (up to 1,000 words) → use Creativity Dial around 3 for continuity chapters, 8–9 for brainstorming. Pricing gates model choice (Claude 3, GPT-4, or Sudowrite's own fiction-trained Muse model).

### Sudowrite / NovelCrafter / NovelAI product patterns (practitioner-facing)

- **Sudowrite Muse** ([product page](https://sudowrite.com/muse); [deep dive](https://sudowrite.com/blog/what-is-sudowrite-muse-a-deep-dive-into-sudowrites-custom-ai-model/)). Notable for *what gets shipped as a feature*: systematic cliché reduction during training, Creativity Dial 1–10, Style Examples (1,000-word style sample slot), "unfiltered" adult-content default. Vendor claim: 40% fewer revision passes for voice consistency vs general-purpose AI.
- **Sudowrite's "Show Don't Tell"** ([blog](https://sudowrite.com/blog/show-dont-tell-how-sudowrites-describe-feature-makes-your-prose-come-alive/)). The Describe feature generates sensory details broken out by five senses + metaphors. Vendor stat worth scrutinizing: show-don't-tell passages receive "3x more Kindle highlights" than summary passages on the same content.
- **NovelCrafter "Codex"** ([Nerdy Novelist vs Sudowrite comparison](https://sudowrite.com/blog/sudowrite-vs-novelcrafter-the-ultimate-ai-showdown-for-novelists/)). Structured database for character/location/lore that the LLM references before drafting. BYOK (Bring Your Own Key) — route to Claude/GPT/Gemini. The "master blueprint" end of the planner spectrum; Sudowrite is the "discovery writer" end.

### Twitter/X + viral prompts

- **Min Choi (@minchoi) — "Humanize AI Content" prompt** ([PromptPal vault drop #04](https://promptpal.substack.com/p/community-vault-drop-04-popular-reddit)). Went viral in 2024 and is still the baseline humanize prompt across Reddit. Bans ~30 words (`delve`, `craft`, `realm`, `revolutionize`, `harness`, `tapestry`, `unlock`, `transformative`, `beacon`, `embark`, `landscape`, `navigating`, `moreover`…); mandates short sentences, active voice, direct "you" address, data-backed claims.

## Key Techniques / Patterns

- **Structure-first humanization.** Target uniform sentence lengths, clean transitions, tidy scene resolutions. Fixes: explicit mix of short/long sentences, em-dash/semicolon stitching, scenes ending on unresolved beats. ([r/WritingWithAI 1r9r6gk](https://www.reddit.com/r/WritingWithAI/comments/1r9r6gk/), [Creativindie](https://www.creativindie.com/how-to-humanize-chatgpt-written-content-for-better-fiction-and-to-pass-ai-detection/))
- **Interview-the-writer voice capture.** Live Q&A session (30–50 min) → `voice.md` file → upload to any AI → reusable across tools. Replaces the failed "paste 5 writing samples" method. (Hassid, Pajonas, Toncheva, The AI Girl)
- **VAST voice encoding.** Vocabulary / Architecture / Stance / Tempo — explicit per-dimension constraints in a system prompt before drafting. (Nick Quick)
- **Behavioral-clause character cards.** Replace adjective dumps (`cold, reserved, fierce`) with behaviors-with-cause ("She deflects emotional moments with cutting jokes — not because she doesn't care, but because sincerity makes her uncomfortable"). The actor test: "If an actor received this card as their only direction, could they perform it consistently?" (r/SillyTavernAI, RP|Fiend)
- **Position-weighted context.** Text nearer the bottom of context weights higher. Put style instructions last, durable worldbuilding first. (NovelAI Memory vs Author's Note; OpenAI cookbook's confirmation that style constraints belong after functional instructions)
- **Scene-break unresolved tension.** Instruct explicitly: do not resolve the scene, end on a question/reaction/interruption. AI defaults to clean closure; human fiction usually doesn't. (Murphy/Creativindie; Nerdy Novelist)
- **Subtext dialogue rule.** Replace "I'm feeling very vulnerable" with "Don't look at me like that." Force dialogue to imply emotion rather than name it. (The AI Writer Hub, Sudowrite)
- **Memory-reinforcement mid-session.** For long roleplay / long drafts, periodically reinject a 2-sentence personality/voice anchor to prevent drift. (r/CharacterAI, bswen voice-consistency doc)
- **Randomized character/mood slots.** Static system prompts → caricature. Rotate mood/goals/desires while keeping identity fixed. (r/LocalLLaMA crossover pattern now adopted in SillyTavern)
- **Talk-to-text for voice priming.** Rant into your phone to produce unfiltered input, then let AI draft from the transcript — prevents the user's own writing from being pre-corrected into genericity. (Pajonas)
- **Regex post-processors.** SillyTavern's regex feature strips recurring AI phrases after generation; pairs with system-prompt bans as a belt-and-braces approach. (r/SillyTavernAI, [ST PR #3581](https://github.com/SillyTavern/SillyTavern/pull/3581))
- **Sampler-level humanization.** Min_P (or min_p + temperature bump) in KoboldAI/text-generation-webui for creative-writing — local-model escape hatch when prompts aren't enough.
- **Tool-specific metadata.** NovelAI's `[ Author; Title; Tags; Genre ]` ATTG, `[ S: 3 ]` quality tag, `{ curly-brace }` instructions — the dialect of Kayra/Erato humanization doesn't transfer to Claude/GPT.
- **Current-state summary block.** Prefix each chapter prompt with "Here's what's already happened / where we are / whose POV" — fixes Claude's "treats all narrative info as equally current" failure mode. (Balthrop)
- **Write-rewrite-revise-with-AI (not AI-then-edit).** The Substack purist workflow: human draft → human rewrite → AI polish. Inverts the typical "AI draft → human edit" order and produces visibly different voice profiles. (Martinez, Pajonas)

## Notable Quotes

> "The robotic feel doesn't come from the vocabulary. Every sentence is the same length. The transitions are perfectly smooth. Paragraphs resolve too cleanly. Human writing has uneven pacing — it speeds up and slows down." — [r/WritingWithAI, 1r9r6gk](https://www.reddit.com/r/WritingWithAI/comments/1r9r6gk/)

> "Let's be absolutely clear: you are not allowed to use AI in this subreddit, you will be banned." — r/WritingPrompts moderator, via [Cornell Chronicle](https://news.cornell.edu/stories/2025/10/ai-generated-content-triple-threat-reddit-moderators)

> "If an actor received this card as their only direction, could they perform it consistently? Could they nail the voice in 10 different scenes? If the answer is no, the card probably needs more work." — [RP|Fiend, SillyTavern character-card guide](https://rpfiend.com/how-to-write-a-sillytavern-character-card/)

> "She deflects emotional moments with cutting jokes. Not because she doesn't care, but because sincerity makes her uncomfortable." — standard Personality-field rewrite, widely shared on r/SillyTavernAI

> "Taste is defined by what you reject, not what you like. Most of a strong voice profile comes from articulating what you'd never do — specific words to avoid, sentence structures you refuse, tones you reject." — Ruben Hassid / [The AI Girl](https://theaigirl.substack.com/p/voice)

> "I write the text, I rewrite it, and *then, and only then*, do I bring in the AI for a final revision. No Prompt and Publish. When an LLM 'writes' on its own, it sounds nothing like me." — Paulina Martinez, [We Speak Human](https://wespeakhuman.substack.com/p/no-ai-slop-writing-with-ai-without)

> "AI is extraordinarily good at mimicking. If you give it your voice — your actual opinions, your rhythm, the way you're declarative when you mean business — it has real material to work with. My mom has read all my books. When she told me she couldn't tell my Substack articles were written with AI, I knew I was doing something right." — Steph Pajonas, [The Interview Is the Secret](https://spajonas.substack.com/p/the-interview-is-the-secret-how-i)

> "The writers beating AI slop aren't using better prompts — they're using better systems. The tools are commodities. The voice isn't." — Nick Quick, [Cozora](https://cozora.substack.com/p/ai-writing-without-the-slop)

> "`It's not X. It's Y.` — This construction is everywhere in AI writing. It sounds clever in a way that I don't actually sound clever. Out." — Steph Pajonas

> "She could tell from the particular way he moved around the counter, post-endorphins quiet. Blog asks for this line to be cut. I found it to be thoughtful and the most human line of the story." — [HN 44455193](https://news.ycombinator.com/item?id=44455193), on "Ok, AI Can Write Pretty Good Fiction Now"

> "It worked well enough that the novels were better than the median novel aimed at my son's age group… good enough that he finished reading them once, but not good enough that he would recommend them or re-read them." — [HN 47304600](https://news.ycombinator.com/item?id=47304600)

> "Don't just dump adjectives in the personality field. That gives too much room for interpretation." — [RP|Fiend](https://rpfiend.com/how-to-write-a-sillytavern-character-card/)

> "Instead of 'You're cheating,' I got 'Have you tried experimenting with different temperature settings for historical accuracy?'" — Chet Day, 77, on joining [r/WritingWithAI](https://chetday.com/r-writingwithai-review-ai-author/)

## Example Prompts / Prompt Snippets

**SillyTavern anti-slop system prompt (condensed from [1rbbsfk](https://www.reddit.com/r/SillyTavernAI/comments/1rbbsfk/))**

```text
Voice & Style:
- Casual, modern language written like describing a scene to a friend.
- Avoid purple prose, archaic phrasing, excessive metaphors, sensory overload.
Dialogue:
- Characters cannot read {{user}}'s internal thoughts or narration.
- Natural hesitations, interruptions, imperfections. No exposition dumps.
- Each character keeps their own vocabulary pattern.
Scene beats:
- Use meaningful small details (a twitch, a glance, voice catching),
  not piles of sensory description.
Forbidden filler: "A beat.", "A pause.", "A breath."
  Integrate beats into developed prose instead.
```

**Character-card Personality-field rewrite pattern ([RP|Fiend](https://rpfiend.com/how-to-write-a-sillytavern-character-card/))**

```text
Before: "cold, reserved, fierce"
After:  "She doesn't flinch. Not at threats, not at raised voices,
         not at the kind of silence that makes other people nervous.
         She's spent enough years in rooms where the wrong reaction
         gets you killed that stillness became a survival mechanism —
         and now it's just who she is."
```

**NovelAI ATTG + style tag (from community threads)**

```text
[ Author: George R.R. Martin; Title: A Song of Ice and Fire;
  Tags: dragons, politics, dynasty; Genre: fantasy ]
[ S: 4 ]   # quality tier (1–5; 2–4 most effective on Erato)
[ Style: verbose ]

*** The scene opens on the eve of the harvest.
```

**Interview-method opener ([Pajonas](https://spajonas.substack.com/p/the-interview-is-the-secret-how-i), [Hassid](https://ruben.substack.com/p/i-am-just-a-text-file))**

```text
Before I draft anything, interview me. Ask one question at a time.
I want you to learn:
- my beliefs and worldview on [topic]
- what makes me cringe / words and phrases I'd never use
- my actual thinking process (contradictions welcome)
- my sentence patterns, formatting habits, opening/closing moves
- the positions I'd never take

When you have 5–10 substantive answers, output a "Voice DNA" .md file
I can reuse. Lead with what I REJECT, not what I like —
taste is defined by what we won't do.
```

**Claude fiction "Mental Framework" prefix ([Balthrop](https://wbalthrop.substack.com/p/writing-fiction-with-claude))**

```text
CURRENT STATE (as of Chapter 7):
- Already happened: Sam lost her job (Ch1), met Jordan (Ch3),
  confronted her sister (Ch5).
- Not yet: the funeral (Ch9), the confession (Ch11).
Treat past events as done. Do NOT reference future plot points
as if they've occurred. POV this chapter: Sam, close third.
```

**Humanize-pass rewrite prompt (Min Choi pattern, adapted for fiction)**

```text
Rewrite the following passage to read like human fiction:
- Vary sentence length sharply (mix sub-10-word sentences with 20+).
- Use em-dashes and semicolons, allow fragments.
- Delete: delve, tapestry, crucial, navigating, landscape, moreover,
  realm, embark, unlock, transformative, beacon.
- End the scene on an unresolved beat (question, reaction, interruption)
  — not a tidy summary.
- Show emotion via action or subtext. No "she felt X".
```

## Patterns, Trends, and Gaps

### Trends

- **From vocabulary to architecture (2023 → 2026).** 2023 advice was word-level (don't say `delve`). 2025–26 advice is structural: sentence-length variance, scene-break resolution, subtext, metaphor families, tempo. Forums now openly cite "burstiness" research. The PNAS 2025 "Echoes in AI" paper (plot diversity collapse) is beginning to appear in practitioner discussions, validating the forum consensus.
- **Interview-method ascent.** The dominant voice-capture approach in Q1 2026 Substack writing is interview-based, explicitly framed as a replacement for the failed "paste samples" method. Multiple independent writers converge on the same insight that rejection is more voice-bearing than preference.
- **Character-card craft is its own discipline.** r/SillyTavernAI and r/CharacterAI have developed a literary-grade craft taxonomy (Description / Personality / First Message / Example Dialogue as separate few-shot slots with token budgets). This is the closest any AI-writing community gets to textbook creative-writing advice.
- **Tool-native humanization.** Sudowrite Muse ships cliché-suppression as a training objective; NovelCrafter ships a Codex as an anti-drift structure; SillyTavern 1.15.0 ships Macros 2.0 and regex post-processors. Humanization is migrating from prompt-layer to product-layer.
- **Author pros reframing the debate.** Joanna Penn's "AI-Assisted Artisan Author" and Chet Day's "curiosity about new tools" frame AI as *amplifying author voice* rather than *passing detection*, explicitly repositioning humanization away from anti-detector framing. The CHI 2025 finding on cultural homogenization is beginning to reach practitioner discourse — non-Western writers are noting that AI "sounds American."
- **Platform sorting accelerating.** Writing subreddits are bifurcating — pro-AI craft communities (r/WritingWithAI, r/SillyTavernAI) vs AI-banned-on-sight communities (r/WritingPrompts). Cornell Chronicle Oct 2025 identified AI as a "triple threat" to moderators. The humanization stakes differ: in the pro-AI communities, "sounds like me" is the goal; in the anti-AI communities, "undetected" is the goal.
- **SillyTavern 1.15.0 (Dec 28 2025) as the current power-user reference.** Macros 2.0, new backends (Ollama, KoboldCpp, LM Studio, cloud APIs all natively supported), and expanded regex post-processing capabilities. The practitioner stack has consolidated around SillyTavern + KoboldCpp/Ollama + Euryale-70B or Qwen3 for local use.

### Active controversies

- **AI draft → human edit vs Human draft → AI polish.** The Substack purist camp (Martinez, Pajonas step 4) insists the human must produce the first sentences. The Sudowrite/NovelCrafter/Nerdy Novelist camp is comfortable with AI-first drafts as long as the voice system is right. Neither camp has conceded.
- **Long ban-lists vs model-knows-best.** Same split visible in general-prompt communities, now specialized: fiction-specific bans (`A beat.`, `A pause.`, "It's not X — it's Y") are widely shared, but there's a minority view that listing slop phrases summons them (Claude starts using them *because* you named them).
- **Bypass detection vs serve the reader.** Creativindie / Derek Murphy explicitly argues detectors don't work and humanization is for reader quality. The bypass-tool wing (Humanize AI Pro, Undetectable AI) treats it purely statistically. Practitioners borrow from both without reconciling.
- **"LLM voice" is bad vs "LLM voice" is effective prose.** Hacker News minority position: the recognizable LLM voice resembles competent public communication, and we may be training a generation of writers to write deliberately worse to avoid it.

### Gaps

- **Longform consistency is underspecified.** Everyone acknowledges voice drift over 50k+ words, but the concrete solutions (Codex, Lorebook, continuous context feeding, chapter-prefix state blocks) are in their first generation. No consensus best practice.
- **Dialogue differentiation per character is hard.** Most "humanize" prompts act on the narrator voice. Keeping two characters' voices *distinct* over a whole novel is a rarer topic and the existing advice (Metaphor Families, Vocabulary Gap, Emotional Shield) is craft-flavored rather than systematized.
- **Non-English is undertreated.** Almost all the forum advice is English-first. The `anti-slop-writing` repo's note that Indonesian AI patterns differ from English is a rare exception.
- **Reader-side perception.** Near-zero forum discussion of what actually makes a *reader* identify AI fiction (vs what detectors flag, vs what writers self-flag). Worth a dedicated research pass.
- **POV discipline.** Claude and GPT both default to author-intrusion / omniscient slippage in close third; the fiction-writing forums mention it often but haven't converged on a fix beyond "remind the model every chapter."
- **Interactive fiction / CYOA.** r/SillyTavernAI has deep craft knowledge on responsive fiction but it almost never gets translated back into static-text novel workflows.

## Implications for "Humanizing AI Output"

1. **Target structure, not vocabulary.** A product that measures and enforces sentence-length variance, scene-resolution deferral, paragraph-rhythm irregularity, and subtext-vs-telling would hit patterns that ban-lists miss. The practitioner consensus has moved there; tooling hasn't caught up.
2. **Interview-based voice capture as a feature, not a prompt.** The recurring Substack pattern — run a 30–50 min voice interview, save a reusable `voice.md` — is under-tooled. Most products still rely on style samples or tone dropdowns.
3. **Character voice distinctiveness is an unsolved vertical.** Narrator humanization is saturated; per-character voice consistency across a long work is open. Metaphor Families / Vocabulary Gap / Emotional Shield are craft vocabularies waiting to become product primitives.
4. **Position the tool on the right side of the detector debate.** Practitioner-author communities (Penn, Day, r/WritingWithAI) are openly hostile to the "bypass detection" framing. A humanizer aimed at *writers* should sell reader quality and voice fidelity; aiming at *students* should sell detector evasion. The two audiences don't overlap well.
5. **Respect platform-native idioms.** NovelAI users think in ATTG + Author's Note slots; SillyTavern users think in Description/Personality/Example-Dialogue fields; Sudowrite users think in Story Bible + Style Examples. A cross-tool humanizer that ignores these conventions will be rejected by every native community.
6. **The "write-rewrite-then-polish" workflow is a viable product opposition.** Most humanizers assume AI-first output. A tool that frames itself as "paste your draft, I'll only polish" would differentiate strongly in the Substack purist segment.

