# Category 14 — Creative Writing & Storytelling

## Angle D: Commercial Products & Services

**Research value: high** — The fiction/storytelling AI market is one of the most mature "humanization-adjacent" verticals; vendors have converged on a clear set of voice-preservation techniques (style examples, codex/story bibles, fine-tuned fiction models) and explicitly sell against "generic AI prose."

**Project context:** Humanizing AI output and thinking. This vertical is the single richest commercial source of voice-preservation and anti-slop techniques outside the humanizer-tool category itself. Unlike general humanizers, fiction tools must preserve *two* voices simultaneously (the narrator's and each character's) across 80k–120k words, which forces deeper architectural answers than text-swap humanizers.

**Last updated: April 2026.**

---

## Product Landscape (17 products)

### 1. Sudowrite

- **Vendor / URL:** Sudowrite, Inc. — sudowrite.com
- **Positioning:** "The AI writing tool with unparalleled story smarts" — fiction-only co-writer.
- **Core tech:** Proprietary **Muse 1.5** model (entered public availability mid-2025 after months in private beta), "built just for fiction" and trained on published novels and short stories to "remove clichés and match writer voice." In blind tests, Muse 1.5 was preferred 2× over Claude 3.7 Sonnet for fiction prose. Platform also offers access to Gemini 3.1 Pro, Claude Sonnet 4.6, and GPT 5.4 for users who prefer frontier models.
- **Voice-preservation mechanics:**
  - **Style Examples** — user pastes writing samples; Muse mimics cadence, vocabulary, rhythm.
  - **Story Bible** — centralized characters/worldbuilding/synopsis threaded into every generation to hold consistency across 100k+ words.
  - **Story Engine 3.0** (2026) — flagship full-novel feature: input Braindump + Genre + Style + Character List → generates chapter beats → expands each beat into full chapters.
  - **Canvas 2.0** — spatial brainstorming board for non-linear story planning (upgraded in 2026).
  - **Write / Guided Write / Auto Write** — 300–500 word continuations "in your voice."
  - **Rewrite** tool specifically trained for show-don't-tell transformations.
  - Integration with Zapier and Make.com for workflow automation.
- **Pricing:** Hobby $10/mo (annual) / $19/mo (monthly); Professional $22/$29; Max $44/$59. Unused credits expire monthly except on Max (12-month rollover). 10,000 free credits trial.
- **Marketing quotes:**
  - "It's scary good." — Hugh Howey (author of *Silo*)
  - "Sudowrite may well be a salvation." — Stephen Marche, *The New York Times*
  - "…convinced journalism legend Gay Talese it could imitate him." — Steven Zeitchik
  - "AI is a phenomenal collaborator, not a destroyer of worlds."
- **Signal for Unslop:** Best-in-class example of *training data provenance as marketing* ("trained on published fiction to remove clichés"). Style Examples is the clearest commercial pattern for single-author voice cloning. Story Engine 3.0 is the clearest example of an end-to-end hierarchical pipeline as a user-facing product.

### 2. NovelCrafter

- **Vendor / URL:** Independent — novelcrafter.com
- **Positioning:** "The Master Blueprint" — planner's tool with BYOK AI layer. 157k+ authors (figure as of early 2025; likely higher by April 2026).
- **Core tech:** **BYOK (bring-your-own-key)** — connects to OpenAI GPT-5/5.1/5.4, Anthropic Claude Sonnet 4.6, Gemini, Llama, Mistral, OpenRouter (300+ models), LM Studio, Ollama (local). NovelCrafter's own testing found GPT-5 "excels at style mimicry and dialogue but tends to veer off-plot" — useful calibration data for model choice within the platform.
- **Voice-preservation mechanics:**
  - **Codex** — wiki that auto-links characters, places, lore; AI is forced to consult it during generation.
  - Customizable prompt system so writers can hand-tune voice preservation per-scene.
  - Local-model support → genuine privacy/voice-fidelity story.
- **Pricing:** From **$4/mo**; user pays model costs separately.
- **Marketing quotes:**
  - "Built by writers, for writers. No venture funding, no corporate agenda — just writers helping writers."
  - "The Chat is similar to brainstorming with a writer buddy, only difference is this writer buddy is available 24/7 and remembers everything." — Lia Mack
  - "The AI pulls details from the codex!" — Bianca
- **Signal for Unslop:** Proof that serious creatives demand *model choice + local inference* for humanization workflows; a single hosted model isn't enough.

### 3. NovelAI (Anlatan)

- **Vendor / URL:** Anlatan Inc. — novelai.net
- **Positioning:** Creative freedom + fine-tuned storytelling models; "uncensored" prose.
- **Core tech:** Own fine-tuned LLMs: Kayra (13B), Clio-Pro, Erato (Llama 3 70B base, released Sep 23 2024), and Opus-tier **Xialong** (GLM-4.6 base, 2026 — "our most high-performance text generation model"). Xialong represents a significant departure: the first major commercial fiction LLM based on Zhipu AI's GLM-4.6 architecture rather than the Llama family. RL-trained to avoid repetition, eliminating the need for repeat-penalty presets. Supports ATTG metadata tags, Memory, Lorebook, and en-space quoting. Up to **128k context**, lorebook, granular sampler controls.
- **Voice-preservation mechanics:**
  - Fiction-fine-tuned base models (vs. RLHF'd general models that flatten voice).
  - Lorebook + metadata tags for continuity.
  - Exposed decoding parameters — users tune "burstiness" directly.
  - Xialong: RL-based repetition avoidance preserves creative variation without manual repeat-penalty tuning.
- **Pricing:** **$10 / $15 / $25** per month (Tablet / Scroll / Opus). Xialong available Opus tier only.
- **Marketing quotes:**
  - "Unleash the power of AI… to easily bring your imagination to life without limits."
- **Signal for Unslop:** Demonstrates the market appetite for *exposed sampling controls* as a humanization lever — something RLHF'd chat models hide. Xialong's shift to GLM-4.6 base is a signal that the fiction-model space is no longer Llama-family-only.

### 4. AI Dungeon (Latitude)

- **Vendor / URL:** Latitude — aidungeon.com
- **Positioning:** Interactive text-adventure / improv storytelling (launched 2019; genre-defining).
- **Core tech:** Multi-model marketplace — proprietary Pegasus/Griffin/Wyvern/Dragon + Claude 3.5 Sonnet + GPT-4o + Mistral. Lorebooks, Author's Note, memory slots.
- **Voice-preservation mechanics:** Author's Note (persistent style steering injected every turn) is the canonical "persistent voice directive" pattern later copied by most tools.
- **Pricing:** Free (Wanderer) → **$9.99 / $14.99 / $29.99 / $49.99** per month (Adventure → Mythic). Credit-based generation with escalating context windows (2k → 32k).
- **Marketing quotes:** Positioned around "unlimited imagination" and player agency; tooling for branching choose-your-own-adventure play.
- **Signal for Unslop:** "Author's Note" = mini-system-prompt for style. Persistent style injection is cheap and effective; Unslop should adopt a similar lightweight mechanism.

### 5. Campfire Writing

- **Vendor / URL:** Campfire Technology — campfirewriting.com
- **Positioning:** All-in-one story planning (timelines, calendars, maps, character sheets, encyclopedia).
- **Core tech:** Traditional (non-generative) planning software; AI integration is minimal/ambient; positioned as a **bible-first** tool that other AI writers can plug into.
- **Pricing:** Modular, from **$2/mo per module**; free tier.
- **Marketing quotes:** "Where Stories Come to Life." Publishing royalties advertised at 80%.
- **Signal for Unslop:** Shows that "structure first, generation second" is a viable stance — users distrust pure-generation tools for long work.

### 6. Squibler

- **Vendor / URL:** Squibler — squibler.io
- **Positioning:** "AI Book and Novel Writer" — chat-to-book, full-length generation. 20k+ writers.
- **Core tech:** Generates complete books/screenplays organized into chapters+scenes; **Smart Elements Board** (characters/locations/traits) fed back into AI for consistency; AI Smart Writer for iterative revision; built-in image/video generation.
- **Pricing:** Free (6k words/mo) → **$16/mo** (Plus, discounted from $29) → **$49/mo** (Pro, from $89).
- **Marketing quotes:**
  - "Turn Your Idea into a Story… Say goodbye to writer's block."
  - "Squibler knew where my story was going even when I didn't." — Tim Boyle
  - "I finished my first draft in just a few days!" — Isla Ravenswood
- **Signal for Unslop:** Aggressive full-book automation is selling; signal that many buyers *don't* care about voice at all, which sharpens the differentiation opportunity for voice-first humanization.

### 7. Plottr (+ AI)

- **Vendor / URL:** Plottr — plottr.com
- **Positioning:** Visual plotting software that added *opt-in* AI brainstorming.
- **Core tech:** AI features are **off by default**, marked with purple sparkle buttons; routes prompts through ChatGPT API; data not used for training; "AI-assisted" not "AI-generated" for Amazon KDP disclosure purposes.
- **Pricing:** ~$25/yr base; Pro tier cloud-stored.
- **Marketing quotes / framing:**
  - "AI in Plottr Gives You Control."
  - "We're not transforming into an AI company."
  - "No prompt engineering, model selection, or hyperparameter tweaking" required.
- **Signal for Unslop:** The explicit *opt-in sparkle button* UX is a strong pattern for humanization tools — positions AI as a seasoning, not a replacement, which aligns with voice-preservation value props.

### 8. AutoCrit

- **Vendor / URL:** AutoCrit — autocrit.com
- **Positioning:** AI-powered fiction **editing** (not generation) with genre-specific benchmarks.
- **Core tech:** 20+ reports (pacing, dialogue, repetition, passive voice, adverbs, clichés, filler, POV); **Voice Reader** (TTS for prose audit); **100+ bestselling-author genre comparisons** (Stephen King, Danielle Steel, Lee Child…).
- **Pricing:** Free tier + **$30/mo** Pro.
- **Marketing quotes:** Frames itself around "data-backed feedback" and writing "comparable to bestsellers."
- **Signal for Unslop:** The "compare to 100 bestselling authors" hook is an implicit *humanness benchmark* — humanization could be marketed the same way ("sound like a published author, not an AI").

### 9. Laika (Write with LAIKA)

- **Vendor / URL:** Writewithlaika.com — **SHUT DOWN 2024–2025**
- **Positioning (historical):** Custom-trained-on-your-writing fiction co-writer; "approximately 10–20% AI and 80–90% your own work."
- **Core tech (historical):** Personalized model fine-tuning on user samples; 100+ author style profiles.
- **Status:** Team moved on to game development. Domain has been repurposed for an unrelated generic AI writer.
- **Signal for Unslop:** A **cautionary data point**: a pure, serious voice-preservation fiction tool failed to sustain commercially despite strong product reviews. Likely causes are cost of fine-tuning, API price compression, and generic tools catching up. Humanization-as-feature may beat humanization-as-product.

### 10. Reedsy Studio

- **Vendor / URL:** Reedsy — reedsy.com/studio
- **Positioning:** Free cloud writing/editing/formatting platform tied to Reedsy's freelance-editor marketplace.
- **Core tech:** Clean editor, boards, collaboration, EPUB/PDF export. AI role is explicitly **minimal** (Reedsy's blog editorializes about AI writing tools rather than ships its own flagship).
- **Pricing:** Free; **$4.99/mo** Studio Essential.
- **Marketing quotes:** "All-in-one writing platform." Leans on trust in human editors.
- **Signal for Unslop:** The "human-editor marketplace" adjacency is how Reedsy hedges against AI slop; a humanization service could partner with editorial marketplaces rather than compete.

### 11. Scrivener (Literature & Latte)

- **Vendor / URL:** Literature & Latte — literatureandlatte.com
- **Positioning:** The incumbent professional writing app — **no native AI**.
- **Core tech:** Data stays local; AI prompts users see on macOS 15+ are Apple Intelligence, *not Scrivener*; no integration plans surfaced.
- **Pricing:** ~$60 one-time.
- **Marketing quotes / framing:** "Scrivener does not send your text to external servers or participate in data scraping."
- **Signal for Unslop:** Large, loyal pro segment that explicitly opts out of cloud AI — a target persona for an **on-device** humanizer.

### 12. ShortlyAI (now Jasper)

- **Vendor / URL:** Acquired by Jasper — shortlyai.com → jasper.ai
- **Positioning (historical):** Minimalist long-form creative writer; "/instruct" and "/expand" commands.
- **Status:** Folded into Jasper; accessed through Jasper's Boss Mode / Creator plan ($59+/mo).
- **Signal for Unslop:** Indicative of consolidation — standalone "creative-mode" tools get absorbed into horizontal marketing-first platforms.

### 13. Rytr

- **Vendor / URL:** Rytr — rytr.me
- **Positioning:** Broad short-form AI writer; fiction is one of 40+ use cases.
- **Voice features:** **Tone matching** (20+ presets + custom tone, "ensures generated content sounds like your unique voice"), 30+ languages.
- **Pricing:** Free → **$9/mo** Unlimited → **$29/mo** Premium.
- **Marketing quotes:** "AI Story Generator… captivating story plots and engaging narratives."
- **Signal for Unslop:** "Tone matching" as a consumer-grade humanization primitive — proves price sensitivity at <$10/mo for simple voice work.

### 14. Jasper (creative modes)

- **Vendor / URL:** Jasper — jasper.ai
- **Positioning:** Enterprise marketing AI; creative/story modes are a side surface.
- **Core tech:** Proprietary "writing algorithm" layered over frontier models; AI Story Generator tool; houses ShortlyAI's legacy features.
- **Pricing:** From **$39/mo** Creator to Enterprise.
- **Signal for Unslop:** Enterprise brand-voice cloning (Jasper's core business) is structurally the same problem as fiction author-voice cloning — the B2B humanization story is proven.

### 15. DoppelWriter

- **Vendor / URL:** doppelwriter.com
- **Positioning:** "AI Writing That Sounds Like You." Explicit voice-cloning tool for fiction.
- **Core tech:** Clones a voice from writing samples; **140+ pre-built iconic-author profiles** (Hemingway, McCarthy, Le Guin…); per-character voice profiles maintained across 80k+ words; analyzes "sentence length, vocabulary preferences, punctuation patterns, tone."
- **Pricing:** Free (5 uses/mo) → **$15/mo**.
- **Marketing quotes:**
  - "Your villain shouldn't sound like your narrator."
  - "Keeps every character's voice distinct — across chapters, drafts, and 80,000 words."
  - One user testimonial: "actually sounded like her — sharp, clipped, cynical. Not generic AI fluff."
  - On process: captures "rhythm, dynamics, the spaces between notes."
- **Signal for Unslop:** **The single most aligned product** with Unslop's thesis. Their voice-profile feature set (sentence length + vocab + punctuation + tone signatures) is a workable feature spec for any humanizer.

### 16. LivingWriter

- **Vendor / URL:** livingwriter.com
- **Positioning:** Scrivener-style manuscript app + optional AI (AI Outlines, Element Generation, Rewrite, Chat, Analysis, Summarize, Screenplays, Book Covers).
- **Voice-preservation framing:** "Data is never stored or used to train AI; all AI features are optional."
- **Signal for Unslop:** Privacy-first framing is a mainstream selling point, not a fringe one.

### 17. StoryWeaver / Dreamweaver.ink

- **Vendor / URL:** dreamweaver.ink
- **Positioning:** Interactive / branching-fiction platform with reader analytics.
- **AI role:** Continuity checking and dead-end detection rather than prose generation — a **defensive** AI role vs. offensive generation.
- **Signal for Unslop:** Example of AI used to *audit* human writing for inconsistencies rather than generate; a complementary mode to humanization.

### Honorable mentions (adjacent, worth tracking)

- **Cordecho** — "Voice-Aware Generation"; explicitly markets "Your voice, amplified" / "AI-powered novel writing that respects your voice."
- **StorySmith** — Custom models maintaining character voice and plot across full novels.
- **Manuscripts.ai Humanizer** — Frames itself as preserving "character's subtext, chapter's tension, and the voice that makes your story yours."
- **VSProse** — "AI Novel Editing Software That Preserves Your Voice… editors never take the pen from your hand."
- **Novarrium, SidekickWriter, Inkfluence AI** — 2025–2026 entrants explicitly benchmarked on the 25-chapter-consistency test. Novarrium's 25-chapter stress test remains one of the few available long-form consistency evaluations even though it is not public.
- **Kimi K2** (Moonshot AI) — Emerging as a cost-competitive option for creative writing. EQ-Bench Creative score ~1700 (vs Claude Sonnet 4.6 at 1936) at $0.60 input / $2.50 output per 1M tokens (~5× cheaper). Positioned as the best performance-per-dollar for writing in early 2026 aggregated leaderboards.

---

## Patterns & Trends

1. **Voice preservation has become the central marketing axis.** Every serious fiction tool now competes on *how* it preserves voice (Style Examples, voice profiles, author comparisons, style tags), not on raw output quality. Generic AI prose is universally cast as the enemy ("AI fluff," "flat," "robotic," "formulaic," "uncanny valley prose").
2. **Convergence on three voice-preservation primitives.** Across Sudowrite, NovelCrafter, DoppelWriter, Cordecho, Laika (historical), and Jasper: (a) **style-sample fine-tuning / few-shot**, (b) **persistent codex / story bible injection**, and (c) **per-character sub-voices** tracked across the manuscript.
3. **Author's-Note pattern is table stakes.** Pioneered by AI Dungeon, every tool now has some equivalent persistent style directive injected on each generation. This is the cheapest, most replicable humanization primitive.
4. **Fiction-tuned base models beat RLHF'd chat models for voice.** NovelAI, Sudowrite (Muse 1.5), and AI Dungeon's own models all explicitly market *against* safety-tuned chat models, on the premise that RLHF flattens stylistic range. This is directly relevant to humanization — RLHF is the root cause of "AI voice."
5. **BYOK and local-model support are appearing as premium features.** NovelCrafter, LM Studio/Ollama integrations — serious creatives want model choice, in part for privacy, in part because no single model has the right voice for everything.
6. **Opt-in sparkle-button UX.** Plottr's "AI is off by default, click a clearly marked button" model is being copied by LivingWriter, Campfire, and Scrivener-adjacent tools. The market reads "AI-first" as a negative signal for serious writers.
7. **Pricing has bifurcated.** A flat-rate prosumer tier at **$9–$16/mo** (Rytr, NovelCrafter, DoppelWriter, Squibler Plus, Sudowrite, NovelAI Tablet) and a power-user tier at **$25–$50/mo** (AutoCrit, NovelAI Opus, AI Dungeon Mythic, Squibler Pro).
8. **"As seen in NYT" and bestselling-author endorsements are the dominant trust proof.** Sudowrite leans hard on Hugh Howey and NYT coverage. The humanization category is adopting the same pattern — bestselling-author voice comparisons (AutoCrit, DoppelWriter's 140+ author profiles) are the equivalent of "trusted by Fortune 500" for creative work.
9. **Consolidation and failure are shaping the map.** ShortlyAI → Jasper. Laika shut down. Pure-play voice tools face compression from (a) horizontal platforms (Jasper), (b) frontier model price drops making fine-tuning less defensible, and (c) the incumbent authoring apps (Scrivener, Plottr, Reedsy) gradually adding AI as a feature, not a product.
10. **Character-voice differentiation is the *next* frontier.** DoppelWriter, StorySmith, and Cordecho are competing on *multi-voice* fidelity — "your villain shouldn't sound like your narrator." This is a harder technical problem than single-voice humanization and remains open.

## Gaps & Opportunities for Unslop

1. **Long-horizon consistency is broadly unsolved.** Every major review (Novarrium 25-chapter test, sidekickwriter comparisons, Inkfluence AI) concludes that all current tools drift beyond ~chapter 10. Even 128k–1M context windows don't fix it. This is an open engineering problem with a willing, paying audience.
2. **No serious tool ships on-device / air-gapped by default.** Scrivener users are an obvious underserved persona — professional writers who refuse cloud AI. An on-device humanizer (local LLM + voice profile) has essentially zero direct competition.
3. **Voice drift across revisions is under-served.** Tools preserve voice in generation but not across edit passes — a user's own edits, plus AI rewrites, plus editor suggestions erode voice over 3–5 drafts. A "voice-diff" / voice-regression-test feature is absent from the market.
4. **The B2B brand-voice story is thin outside Jasper.** Most fiction tools explicitly disclaim non-fiction. A humanizer that treats author-voice and brand-voice as the same technical problem has a cleaner B2B story than any fiction-only player.
5. **Transparency about *how* voice is preserved is marketing, not product.** Vendors describe "analyzes rhythm, punctuation, sentence length" but don't expose the model to the user. A humanization tool that shows the voice profile (so the user can edit / lock / version it) would be structurally novel.
6. **Cliché-removal is undertreated.** Sudowrite's Muse claims "trained on published fiction to remove clichés," but no tool offers a *cliché and AI-ism detector* as a first-class feature. Given that detector-dodging is a known adjacent use case (Manuscripts.ai, WriteHuman), a detector-inverted tool ("find your AI tells") has market fit.
7. **Failed-products pattern suggests humanization-as-feature > humanization-as-product.** Laika's shutdown argues that Unslop may be better positioned as an **SDK/API and platform integration** (Scrivener plugin, NovelCrafter prompt pack, Plottr add-on, Jasper custom brand-voice module) than as a standalone consumer app.

---

## Sources

- [Sudowrite homepage](https://www.sudowrite.com/) — positioning, Muse 1.5, Story Bible, testimonials.
- [Sudowrite Review 2026 (Scribehow)](https://scribehow.com/page/Sudowrite_Review_2026_I_Tested_It_on_5_Fiction_Genres__Heres_What_Actually_Works__mUBpPMiIQuqw8tm0wDgq9Q) — genre-by-genre test and rating.
- [Sudowrite vs NovelCrafter (Sudowrite blog)](https://sudowrite.com/blog/sudowrite-vs-novelcrafter-the-ultimate-ai-showdown-for-novelists/) — "Magic Wand vs Master Blueprint" framing.
- [Novarrium 25-chapter stress test](https://novarrium.com/blog/best-ai-writing-tool-novels-2026) — long-horizon consistency failures.
- [NovelAI homepage](https://novelai.net/) — Xialong/Kayra/Clio models, Tablet/Scroll/Opus pricing.
- [NovelCrafter homepage](https://novelcrafter.com/) — BYOK model list, Codex, testimonials, "no venture funding" positioning.
- [Techlasi: NovelAI vs AI Dungeon](https://techlasi.com/savvy/novelai-vs-ai-dungeon-a-detailed-comarison/) — coherence and training-data comparison.
- [Squibler homepage](https://squibler.io/) — full-book generation, Smart Elements Board, tiered pricing.
- [Campfire Writing plans / features](https://www.campfirewriting.com/pricing) — modular pricing, planning-first stance.
- [Plottr: AI in Plottr / AI and Your Data](https://plottr.com/ai-in-plottr-workflow/) — opt-in sparkle-button UX, KDP disclosure framing.
- [AutoCrit review (Fictionary)](https://fictionary.co/journal/autocrit-review) — 20+ reports, 100+ author comparisons.
- [DoppelWriter for Fiction Writers](https://doppelwriter.com/for/fiction-writers) — per-character voice profiles, 140+ author presets.
- [Write with LAIKA (repurposed domain)](https://www.writewithlaika.com/) — confirms Laika shutdown 2024–2025.
- [Reedsy Studio](https://reedsy.com/studio/) — free platform + human-editor marketplace.
- [Literature & Latte: Scrivener and AI](https://www.literatureandlatte.com/blog/scrivener-and-ai-why-do-i-see-ai-prompts-in-my-scrivener-projects-on-mac) — no native AI; privacy posture.
- [Rytr AI Story Generator](https://rytr.me/use-cases/story-plot) — tone matching + pricing.
- [Jasper AI Story Generator](https://jasper.ai/tools/ai-story-generator) — creative surface of the enterprise marketing platform; ShortlyAI absorption.
- [Latitude / AI Dungeon plans](https://latitude.io/blog/new-ai-dungeon-membership-plans-are-now-available-to-all-players/) — Wanderer → Mythic pricing and context-window tiers.
- [LivingWriter AI Features](https://livingwriter.com/en/ai-features) — optional AI, "never stored or used to train."
- [Smallhandsbigideas: 2026 landscape](https://smallhandsbigideas.com/the-ai-storytelling-tools-landscape-in-early-2026-how-novelai-sudowrite-and-sillytavern-serve-different-writer-archetypes/) — archetype framing for the three-horse market.
- [Cordecho](https://cordecho.com/) — "voice-aware generation" marketing language.
- [Sudowrite Story Engine 3.0 changelog](https://feedback.sudowrite.com/changelog) — 2026 flagship feature.
- [Sudowrite Pricing 2026 (CheckThat.ai)](https://checkthat.ai/brands/sudowrite/pricing) — updated plan structure.
- [NovelAI Xialong model announcement](https://blog.novelai.net/novelai%E6%9C%80%E6%96%B0%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E7%94%9F%E6%88%90%E3%83%A2%E3%83%87%E3%83%AB-xialong-%E3%81%8C%E7%99%BB%E5%A0%B4-8a4ec11895ea) — GLM-4.6 based, 2026.
- [NovelCrafter blog: Is GPT-5 any good for writing fiction?](https://www.novelcrafter.com/blog/is-gpt-5-any-good-for-writing-fiction) — GPT-5 evaluation.
- [Character.AI April 2026 CEO update / PipSqueak 2](https://blog.character.ai/pipsqueak2-and-more/) — PSQ2 rollout, DeepSqueak 2 roadmap.
- [EQ-Bench Creative Writing v3 Leaderboard](https://eqbench.com/creative_writing.html) — Claude Sonnet 4.6 Elo 1936, Claude Opus 4.6 Elo 1932, as of March 2026.
- [Best AI for Creative Writing April 2026 (buildmvpfast.com)](https://www.buildmvpfast.com/articles/best-llms-2026-guide/creative-writing-ai) — aggregated leaderboard with Kimi K2 cost analysis.
