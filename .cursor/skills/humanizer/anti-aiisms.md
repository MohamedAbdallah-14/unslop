# Canonical AI-ism Ban List

Distilled from Category 01 (`blader/humanizer`, `adenaufal/anti-slop-writing`, Every.to *AI Style Guides*), Category 04 (`antislop-sampler` corpora, AlpinDale rentry), Category 05 (adversarial-paraphrase target phrases), Category 16 (OSS humanizer skill-packs), and Wikipedia's *Signs of AI Writing*. Use as a reference block inside system prompts or as input to `scripts/scan.py`.

Three severity tiers. High = almost always a tell. Medium = a tell in combination. Low = only when over-used.

## HIGH severity — single occurrence is enough to flag

### Signature vocabulary
- delve, delves, delving
- tapestry
- testament (as in "a testament to")
- bustling
- vibrant
- realm (outside fantasy)
- navigate (as metaphor)
- harness (as verb)
- leverage (as verb)
- multifaceted
- underscores (as verb)
- underscore the importance of
- paradigm shift
- treasure trove
- labyrinth / labyrinthine
- myriad (of)
- plethora
- ever-evolving
- ever-changing
- game-changing / game-changer
- crucial / crucially
- pivotal
- robust (outside engineering context)
- whimsical
- meticulous / meticulously
- seamless / seamlessly
- unparalleled
- cutting-edge (when the subject is not cutting-edge)
- state-of-the-art (same)

### Signature phrases and connectives
- It's important to note
- It's worth noting
- It's worth mentioning
- It's crucial to
- It's essential to
- In conclusion,
- In summary,
- To summarize,
- To conclude,
- Overall,
- Ultimately, (as a paragraph opener)
- Furthermore,
- Moreover,
- Additionally, (as a paragraph opener)
- In today's fast-paced world
- In the ever-evolving landscape of
- In the world of
- When it comes to
- Dive into / Let's dive in
- Unlock the power of
- Unleash the potential of
- At the heart of
- The rise of
- A deep dive into

### Sycophantic openers and closers
- Great question!
- That's an excellent question
- What a thoughtful question
- I hope this helps!
- I hope this answers your question!
- Feel free to ask if you have any more questions
- Let me know if you need any further clarification
- Certainly! / Of course! / Absolutely! (as standalone openers)

### Structural tells
- Tricolons: any "X, Y, and Z" where all three are single adjectives or near-synonyms (rhetorical triples). Flag ≥2 per 200 words.
- "It's not just X, it's Y" (and "It's not X — it's Y").
- "Whether you're X, Y, or Z, …" (parallel-case opener).
- Five-paragraph shape: intro + exactly three body paragraphs + neat conclusion.
- Every paragraph starts with a subject noun phrase or transitional adverb.
- Bullet lists where every bullet starts with the same word or grammatical form.
- Em-dash pairs (`— … —`) more than once per 200 words, or any appearance in casual registers.

## MEDIUM severity — tell only in combination

### Hedging and uncertainty filler
- might
- perhaps
- possibly
- arguably
- could be seen as
- some would argue
- it could be argued
- in many ways
- to some extent
- relatively (as in "relatively common")

Replace with the calibrated-uncertainty ladder: `unlikely / plausible / probable / very probable / almost certain` (Gwern 2025). If a hedge is genuinely warranted, keep it; if it's reflexive padding, cut.

### Warmth / empathy filler
- I understand how you feel
- That must be difficult
- I'm here for you
- Remember, you're not alone
- It's completely understandable
- Please know that

Flag when the register is analytical or when the user did not ask for support.

### Marketing-slop verbs
- foster, fosters, fostering
- facilitate, facilitates
- enable (when "let" would do)
- optimize (outside technical context)
- streamline
- revolutionize
- empower
- elevate (metaphorical)
- transform (metaphorical)
- curate, curated (outside museums)

### Abstract-noun pileups
Any sentence with ≥3 of: *insights, solutions, strategies, opportunities, capabilities, experiences, journeys, perspectives, considerations, implications*.

## LOW severity — fine in moderation, flag only on repetition

### Adverb-ly openers
- Importantly,
- Interestingly,
- Notably,
- Remarkably,
- Essentially,
- Fundamentally,
- Ultimately,
- Significantly,

Acceptable ≤ 1 per 500 words. Flag on repetition.

### Vague intensifiers
- very
- really
- quite
- rather
- truly
- incredibly

Flag when >3 per 200 words.

### Structural filler
- "As we can see,"
- "Let's take a closer look at"
- "One thing to keep in mind"
- "That being said,"
- "With that said,"

## Punctuation tells

- **Em-dash (`—`) overuse**: >1 per 200 words in casual registers, or >2 per 500 words in formal registers.
- **Oxford comma present in a tricolon of AI-ism words**: double-flag.
- **Curly quotes in plain-text output** (when the model was asked for ASCII): model tell.
- **Smart-apostrophe inconsistency within one document**: model tell.
- **Unicode thin-space / zero-width chars**: some humanizer tools insert these; detectors and forensic tools catch them. Never use.

## Non-native English writer note

Several items on this list (formal connectives, Latinate vocabulary, hedging patterns) overlap with non-native English writing patterns. When humanizing for a non-native author, preserve authentic quirks (small article errors, Germanic-via-L1 word choices) rather than sanding them flat toward "AI-smooth neutral." Source: `docs/research/05-ai-text-detection-and-evasion/INDEX.md` (detector bias finding, Liang et al. 2023).

## Extending the list

Project- or user-specific bans go in a companion file `anti-aiisms.local.md` (git-ignore if private). Load both in order when the user runs a personalized humanization job.
