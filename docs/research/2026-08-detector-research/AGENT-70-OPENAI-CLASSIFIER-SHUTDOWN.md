# Agent #70 — OpenAI AI Classifier Shutdown

**Topic:** Why OpenAI shut down its public AI text classifier, full timeline, community reaction, and implications for the 2026 detection landscape  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detector refresh

---

## Executive summary

OpenAI ran **two separate text-detection programs**. Only one was shut down.

1. **Public AI Text Classifier (Jan–Jul 2023)** — a free web tool for detecting *any* AI-generated English prose. OpenAI discontinued it **July 20, 2023** with a one-line note on the launch blog: *"low rate of accuracy."* On OpenAI's own challenge set it caught **26%** of AI text (true positives) while falsely flagging **9%** of human text. The UI returned 404; no press release.

2. **Internal ChatGPT text watermark (2022–present, unreleased)** — a token-selection watermark Aaronson/Kirchner built, reported **99.9% effective** on sufficient ChatGPT output in internal docs ([WSJ Aug 4, 2024](https://www.wsj.com/tech/ai/openai-tool-chatgpt-cheating-writing-135b755a)). OpenAI confirmed it in an Aug 4, 2024 blog update but **still has not shipped it** as of August 2026. Reasons: trivial bypass via cross-model rewrite/translation, ESL stigma fears, and ~**30%** of surveyed users saying they'd use ChatGPT less if outputs were traceable.

**What did *not* shut down:** the **2019 GPT-2 RoBERTa detectors** (`openai-community/roberta-base-openai-detector`, `roberta-large-openai-detector`) remain on Hugging Face. Liang et al. (2023) and StealthRL still treat them as baselines. They are GPT-2-era models; OpenAI's model card warns against using them for ChatGPT misconduct allegations.

**Why it mattered:** The company that launched ChatGPT publicly admitted it could not reliably classify post-hoc AI text — **one day before** signing White House voluntary commitments that scoped watermarking to **audio and visual** content only ([White House PDF](https://whitehouse.gov/wp-content/uploads/2023/07/Ensuring-Safe-Secure-and-Trustworthy-AI.pdf)). HN (503 points, 283 comments) and academia treated the shutdown as validation that detector-gated enforcement was broken. Third-party vendors (GPTZero, Turnitin, Originality) filled the vacuum and kept iterating; OpenAI pivoted to **C2PA metadata + SynthID** for images/audio and left text provenance to competitors.

**unslop verdict:** The shutdown is the canonical **vendor exit precedent** — when a frontier lab won't stand behind post-hoc text classification, unslop should never imply "OpenAI-grade detection" exists for users. Cite it in Boundaries and anti-detector docs: **post-hoc classifiers are commercially abandoned by the generator; process provenance (Authorship, Replay) and third-party ensembles are the institutional substitute.** unslop's defensive ESL/resume positioning aligns with OpenAI's stated reason for withholding watermarking (stigma of AI-assisted writing for non-native speakers).

---

## Primary sources (URLs)

| Resource | URL | Note |
|----------|-----|------|
| **OpenAI launch + shutdown notice (canonical)** | https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/ | Jan 31, 2023 launch; Jul 20, 2023 shutdown note at top |
| **OpenAI provenance blog (watermark update)** | https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/ | May 2024 original; Aug 4, 2024 text-watermark confirmation |
| **WSJ — unreleased watermark** | https://www.wsj.com/tech/ai/openai-tool-chatgpt-cheating-writing-135b755a | Aug 4, 2024; internal 99.9% claim |
| **White House voluntary commitments (PDF)** | https://whitehouse.gov/wp-content/uploads/2023/07/Ensuring-Safe-Secure-and-Trustworthy-AI.pdf | Jul 21, 2023; commitment #5 = audio/visual only |
| **White House fact sheet** | https://www.presidency.ucsb.edu/documents/fact-sheet-biden-harris-administration-secures-voluntary-commitments-from-leading | Same commitments, public summary |
| **Decrypt — first shutdown report** | https://decrypt.co/149826/openai-quietly-shutters-its-ai-detection-tool | Jul 25, 2023 |
| **Ars Technica shutdown analysis** | https://arstechnica.com/information-technology/2023/07/openai-discontinues-its-ai-writing-detector-due-to-low-rate-of-accuracy/ | "Performative Band-Aid" framing |
| **The Verge shutdown** | https://www.theverge.com/2023/7/25/23807487/openai-ai-generated-low-accuracy | Jul 25, 2023 |
| **The Verge watermark non-release** | https://www.theverge.com/2024/8/4/24213268/openai-chatgpt-text-watermark-cheat-detection-tool | Aug 4, 2024 |
| **TechCrunch launch** | https://techcrunch.com/2023/01/31/openai-releases-tool-to-detect-ai-generated-text-including-from-chatgpt/ | Jan 31, 2023 |
| **Axios launch (Jan Leike quote)** | https://www.axios.com/2023/01/31/openai-chatgpt-detector-tool-machine-written-text | "False positives and false negatives" |
| **HN discussion** | https://news.ycombinator.com/item?id=36862850 | 503 pts, Jul 25, 2023 |
| **OpenAI Developer Community launch thread** | https://community.openai.com/t/new-ai-classifier-for-indicating-ai-written-text/46514 | No API planned; evasion concern noted |
| **RoBERTa base detector (still live)** | https://huggingface.co/openai-community/roberta-base-openai-detector | 2019 GPT-2 era; ~95% on 1.5B GPT-2 |
| **RoBERTa large detector** | https://huggingface.co/openai-community/roberta-large-openai-detector | Used in StealthRL, Liang eval |
| **GPT-2 detector paper (GPT-2 Report)** | https://d4mucfpksywv.cloudfront.net/papers/GPT_2_Report.pdf | Original ~95% accuracy claim |
| **Liang ESL false-positive study** | https://arxiv.org/abs/2304.02819 | OpenAI RoBERTa in 7-detector panel |
| **Sadasivan impossibility** | https://arxiv.org/abs/2305.12001 | Cited in repo AGENT-17; post-shutdown policy shift |
| **Kirchenbauer watermark (related lineage)** | https://arxiv.org/abs/2301.10226 | Statistical watermarking; Aaronson/OpenAI adjacent |
| **Ars — White House watermark pledge** | https://arstechnica.com/ai/2023/07/openai-google-will-watermark-ai-generated-content-to-hinder-deepfakes-misinfo/ | Jul 21, 2023; text not in scope |
| **Silicon Republic (Toby Walsh reaction)** | https://www.siliconrepublic.com/machines/openai-classifier-tool-detect-ai-written-text-distinguish-humans | "No hope for outsiders like Turnitin" |

---

## Timeline: three detection eras at OpenAI

### Era 0 — GPT-2 RoBERTa detector (2019, still on Hugging Face)

| Date | Event |
|------|-------|
| **Feb 2019** | OpenAI releases GPT-2 1.5B weights + RoBERTa sequence classifier trained on GPT-2 vs WebText outputs |
| **2019–2022** | Detector hosted as web demo; weights mirrored to Hugging Face |
| **2023+** | Web UI deprecated; HF checkpoints remain. Model card: **~95% accuracy on 1.5B GPT-2** with nucleus sampling; **not** validated for ChatGPT |

This is the **"previously released classifier"** the January 2023 tool claimed to improve upon.

### Era 1 — Public AI Text Classifier (Jan–Jul 2023)

| Date | Event | Source |
|------|-------|--------|
| **Nov 2022** | ChatGPT launch; educator panic over essay cheating begins | — |
| **Jan 31, 2023** | OpenAI launches **AI Text Classifier** — free web UI, ≥1,000 characters, English-only, five ordinal labels ("very unlikely" → "likely AI") | [OpenAI blog](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/) |
| **Jan 31, 2023** | OpenAI publishes headline stats: **26% TPR**, **9% FPR** on English "challenge set"; warns evasion via editing, short text, non-English, code | Same |
| **Jan 31, 2023** | Jan Leike (alignment lead): *"It has both false positives and false negatives"* — not for sole authorship decisions | [Axios](https://www.axios.com/2023/01/31/openai-chatgpt-detector-tool-machine-written-text) |
| **Mar 2023** | Liang et al. benchmarks **OpenAI RoBERTa** (HF) among seven detectors; TOEFL FPR crisis begins | [arXiv:2304.02819](https://arxiv.org/abs/2304.02819) |
| **Apr 2023** | OpenAI surveys ChatGPT users on watermarking: **69%** fear false accusations; **~30%** would use ChatGPT less if watermarked | [WSJ Aug 2024](https://www.wsj.com/tech/ai/openai-tool-chatgpt-cheating-writing-135b755a) |
| **May 2023** | GPTZero seed funding; Turnitin AI detector in development | AGENT-57, Turnitin blogs |
| **Jul 20, 2023** | **Shutdown:** blog post updated — classifier *"no longer available due to its low rate of accuracy"*; research pivot to *"more effective provenance techniques for text"* + commitment to audio/visual marking | [OpenAI blog](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/) |
| **Jul 20, 2023** | Classifier URL returns 404 / "Page Not Found" | [Decrypt](https://decrypt.co/149826/openai-quietly-shutters-its-ai-detection-tool) |
| **Jul 21, 2023** | White House voluntary AI commitments signed (OpenAI, Google, Meta, Microsoft, Amazon, Anthropic, Inflection). **Commitment #5:** watermark/provenance for **AI-generated audio or visual content** — text not mentioned | [White House PDF](https://whitehouse.gov/wp-content/uploads/2023/07/Ensuring-Safe-Secure-and-Trustworthy-AI.pdf) |
| **Jul 25, 2023** | Decrypt breaks story; Ars, Verge, Search Engine Land follow; **HN 503 points** | [HN](https://news.ycombinator.com/item?id=36862850) |
| **Aug 2023** | Vanderbilt disables Turnitin AI detection citing unreliable detection + equity | AGENT-17 |

**Lifespan:** ~**5.5 months** (Search Engine Land: *"R.I.P. Text Classifier, 2023–2023"*).

### Era 2 — Unreleased watermark + provenance pivot (2022–2026)

| Date | Event | Source |
|------|-------|--------|
| **Nov 2022** | Scott Aaronson describes token-probability watermarking approach (UT Austin lecture) | WSJ, Aaronson blog references |
| **2022–2023** | Hendrik Kirchner builds working prototype; internal docs claim **99.9%** detection on sufficient ChatGPT output | [WSJ](https://www.wsj.com/tech/ai/openai-tool-chatgpt-cheating-writing-135b755a) |
| **Jul 2023** | Public classifier killed; watermark stays internal | This memo |
| **May 2024** | OpenAI publishes *"Understanding the source of what we see and hear online"* — C2PA, SynthID for audio/images; text classifiers/watermarks mentioned generically | [OpenAI blog](https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/) |
| **Aug 4, 2024** | WSJ: watermark *"ready about a year"* — *"just a matter of pressing a button"* | WSJ |
| **Aug 4, 2024** | OpenAI blog **update** confirms text watermarking method: accurate vs **localized** tampering (paraphrase), weak vs **globalized** tampering (translation, cross-model rewrite, character-insertion tricks) | Same blog |
| **Aug 4, 2024** | OpenAI cites ESL stigma: watermark could *"disproportionately impact"* non-native speakers using AI as writing aid | Same |
| **2024–2026** | No ChatGPT text watermark shipped. Competitors move: Google **SynthID text** (Gemini, May 2024+); Anthropic **Claude text watermark** default (Aug 2026) | Inc42, Google DeepMind |
| **Aug 2026** | OpenAI still on **C2PA + SynthID for AV**; text provenance remains research-only | OpenAI blog state |

---

## Why OpenAI shut down the public classifier

### Stated reason (official)

Single sentence on the launch blog: **low rate of accuracy.** No separate post-mortem, no replacement product announcement.

### Disclosed limitations (known at launch — shutdown vindicated them)

From the January 2023 blog and press:

| Limitation | Detail |
|------------|--------|
| **Low recall** | 26% of AI text labeled "likely AI-written" on challenge set |
| **Non-trivial FPR** | 9% of human text falsely flagged |
| **Length floor** | Unreliable below **1,000 characters** (~150–250 words) |
| **Language** | English-only; worse on other languages |
| **Code** | Unreliable on code |
| **Evasion** | *"AI-written text can be edited to evade the classifier"* — OpenAI explicitly doubted long-term detection advantage |
| **Calibration** | Neural classifiers *"poorly calibrated outside of their training data"* |
| **No API / no weights** | Web UI only — adversaries could probe and optimize against labels |
| **Human–AI collaboration** | *"Not thoroughly assessed"* for mixed authorship |

### Structural interpretation (industry + academic)

1. **Distribution shift:** Classifier trained on early InstructGPT/GPT-3 outputs; ChatGPT-3.5/4 writing style drifted faster than retraining cycles.

2. **Adversarial surface:** Any public scorer becomes an optimization target (HN: plug classifier into generative loop and backprop). OpenAI refused to release weights partly for this reason ([Developer Community thread](https://community.openai.com/t/new-ai-classifier-for-indicating-ai-written-text/46514)).

3. **Liability asymmetry:** 9% FPR × millions of student essays = mass false accusations. OpenAI warned against *"primary decision-making tool"* use; educators ignored the warning ([Ars Technica](https://arstechnica.com/information-technology/2023/07/openai-discontinues-its-ai-writing-detector-due-to-low-rate-of-accuracy/)).

4. **Business incentive:** A working detector undermines ChatGPT's core use case (writing assistance). Shutting the **general** classifier while hoarding a **ChatGPT-specific** watermark is consistent with protecting product usage — especially given the 30% churn survey ([Verge Aug 2024](https://www.theverge.com/2024/8/4/24213268/openai-chatgpt-text-watermark-cheat-detection-tool)).

5. **Strategic pivot to provenance:** Post-shutdown, OpenAI consistently frames the problem as **marking at generation time** (watermark, C2PA metadata) rather than **classifying after the fact** — aligned with Sadasivan-style impossibility arguments for robust post-hoc detection under paraphrase ([AGENT-17-SADASIVAN-IMPOSSIBILITY.md](./AGENT-17-SADASIVAN-IMPOSSIBILITY.md)).

### Quiet shutdown as signal

- No dedicated announcement — only a blog edit and 404.
- Decrypt (*"quietly unplugged"*) noted the contrast with January's fanfare.
- Timing: **one day before** White House commitments that omitted text watermarking — suggests deliberate narrative control: *we're responsible about AV deepfakes; we're not claiming we can detect text.*

---

## Community reaction (Jul–Aug 2023)

### Hacker News (503 points, 283 comments)

Dominant themes from [HN thread](https://news.ycombinator.com/item?id=36862850):

| Theme | Representative sentiment |
|-------|-------------------------|
| **Shutdown was correct** | Glad it's gone; should have been announced properly |
| **Detection impossible at short length** | *"Impossible they could guarantee that"* for few sentences |
| **Adversarial arms race** | Classifier + generator = doomed unless weights secret; even then incentive to leak |
| **False accusations in academia** | *"Tons of false accusations"* — PhD students, K-12 Reddit stories |
| **Snake-oil market** | *"Hundred different AI detectors… basically snake oil"* but admins keep buying |
| **Quality over authorship** | Better to automate *quality* assessment than human vs AI binary |
| **Google won't do it either** | Same reasons OpenAI cancelled — typing-pattern detection unlikely from docs vendors |

Technically literate commenters treated OpenAI's published 26%/9% numbers as **honest** — better than random on recall while FPR stayed the binding constraint for high-stakes use.

### Press and expert quotes

| Source | Quote / framing |
|--------|-----------------|
| **Ars Technica** | *"Performative Band-Aid"*; Daniel Jeffries: *"AI detection tools are snake oil… Don't trust them"* |
| **Toby Walsh (UNSW)** | If OpenAI with inside access gives up, *"there's probably no hope for outsiders like Turnitin"* ([Silicon Republic](https://www.siliconrepublic.com/machines/openai-classifier-tool-detect-ai-written-text-distinguish-humans)) |
| **The Verge** | *"Not even the company that helped kickstart the generative AI craze… has answers"* |
| **Search Engine Land** | Reminder to marketers/SEOs: detectors *"fail at their only job"* |

### Educator ecosystem

- January launch was explicitly framed for **academic dishonesty** and misinformation ([OpenAI blog](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/)).
- Shutdown left educators with **third-party tools** (GPTZero launched Jan 2, 2023 — 29 days *before* OpenAI's classifier) and Turnitin (shipped Apr 2023).
- Institutional retreat accelerated: Vanderbilt (Aug 2023), later CASRAI/USD guidance treating scores as inquiry prompts not proof (AGENT-17 §7.2).

### Supporter / skeptic split

| Camp | Position |
|------|----------|
| **Skeptics (majority)** | Shutdown proves post-hoc detection isn't deployable; validates Liang ESL concerns and Sadasivan bounds |
| **Pragmatists (minority)** | 26% recall + low FPR threshold still better than nothing for *screening* if humans review — but OpenAI wouldn't maintain it |
| **Vendor optimists** | GPTZero, Turnitin, Originality cited OpenAI's exit as market opportunity, not technical impossibility — and invested in deep-learning + adversarial retraining (AGENT-57, AGENT-56) |

---

## What survived vs what died

| Artifact | Status Aug 2026 | Notes |
|----------|-----------------|-------|
| **AI Text Classifier web UI** | **Dead** (Jul 20, 2023) | 404 |
| **Launch blog post** | **Living tombstone** | Shutdown note preserved at top |
| **RoBERTa GPT-2 detectors (HF)** | **Alive** | Still used as research baseline; not ChatGPT-calibrated |
| **Internal ChatGPT watermark** | **Unreleased** | 99.9% internal claim; commercial/ESL/bypass concerns |
| **C2PA / SynthID (images, audio)** | **Shipped** | OpenAI's actual provenance bet |
| **Text watermark in ChatGPT output** | **Not shipped** | Anthropic/Google moved first on text marking |

**Important correction for literature reviews:** "OpenAI shut down its detector" usually means the **2023 classifier**, not the **2019 RoBERTa weights**. Liang (2023) tested the HF RoBERTa model, which outlived the web tool.

---

## Implications for the 2026 detection landscape

### 1. Generator–detector separation is permanent

OpenAI will generate text; it will not publicly score text it didn't watermark at source. Detection market belongs to **third parties** (GPTZero/Superhuman, Turnitin, Originality, Copyleaks, Pangram) and **open methods** (DetectGPT lineage, Binoculars, DivEye, Ghostbuster).

### 2. Provenance beats classification — but text provenance stalled at OpenAI

Policy tailwinds (EU AI Act Art. 50, White House commitments) push **marking at generation**. OpenAI's own trajectory:

- **Jul 2023:** Kill post-hoc classifier → promise AV watermarking  
- **Aug 2024:** Admit text watermark works internally → don't ship  
- **2026:** Competitors watermark text; OpenAI still doesn't  

unslop's WaterPark / SIRA research (AGENT-20, AGENT-71) documents that even shipped watermarks face paraphrase stripping — OpenAI's bypass list (translation, cross-model rewrite) matches WaterPark/DIPPER findings.

### 3. Commercial detectors filled the vacuum — with contested accuracy

GPTZero went from perplexity demo (Jan 2023) to deep-learning + adversarial training + Superhuman acquisition (Jun 2026). Turnitin held LMS channel. None have OpenAI's generator access — they compensate with **versioned retraining** and **process tools** (Replay, Authorship).

OpenAI's exit did **not** kill the detector industry; it **delegitimized sole reliance on any single vendor** while legitimizing skepticism.

### 4. False-positive equity became mainstream

OpenAI's Aug 2024 watermark rationale explicitly cited **non-native English speakers** — the same population Liang showed detectors over-flag. Institutional policy now converges on: detectors as **one signal**, never sole evidence (AGENT-17 §7.4). unslop's ESL false-positive defense is aligned with the **generator's own stated ethics**, not a loophole narrative.

### 5. Arms-race framing hardened

Shutdown + Sadasivan (May 2023) + OpenAI watermark non-release (Aug 2024) form a **triad** cited in:

- Academic integrity guides (Weber-Wulff, CASRAI)  
- Adversarial paraphrase papers (AGENT-25, AGENT-39)  
- Humanizer benchmark literature (DAMAGE, MGTBench)  

Message: **post-hoc detection is a narrowing window**; humanization that changes token-level statistics without semantic drift remains the evasion primitive.

### 6. Benchmark baselines frozen in time

Papers through 2025 still cite **OpenAI RoBERTa** and **"OpenAI classifier (withdrawn)"** as era markers. DIPPER evals (AGENT-31) used the 2023 classifier before shutdown. Modern evals should **not** treat OpenAI as an active commercial detector — use GPTZero version strings, Turnitin API, or open methods instead.

---

## Comparison: public classifier vs unreleased watermark

| Dimension | AI Text Classifier (2023) | Internal watermark (unreleased) |
|-----------|---------------------------|-----------------------------------|
| **Target** | Any AI-generated English prose | ChatGPT output only |
| **Mechanism** | Supervised LM classifier | Token-selection bias pattern |
| **Claimed accuracy** | 26% TPR / 9% FPR (public) | 99.9% on sufficient ChatGPT text (internal) |
| **Paraphrase resistance** | Poor (disclosed at launch) | Good vs *localized*; poor vs *globalized* (Aug 2024 blog) |
| **False positives** | 9% on human text | Low per-doc; volume scaling still problematic |
| **Deployment** | Public 5.5 months | Never public |
| **Kill / hold reason** | Too inaccurate to maintain | Too accurate — user churn, ESL stigma, trivial bypass |

The juxtaposition defines OpenAI's detection philosophy: **don't ship bad post-hoc tools; don't ship good watermarking that hurts usage.**

---

## unslop integration implications

| Shutdown lesson | unslop relevance | Action |
|-----------------|------------------|--------|
| Frontier lab abandoned post-hoc text UI | Never claim parity with "OpenAI detection" | README / SKILL.md landscape: cite Jul 2023 exit |
| 9% FPR at best published rate | ESL/resume users face real false-positive risk | Keep Boundaries: defensive use only |
| Watermark withheld for ESL stigma | unslop anti-detector ≠ misconduct; aligns with OpenAI's own equity argument | Cross-link AGENT-18 in help text |
| RoBERTa still in HF | `detector.py` / benchmarks may reference stale baseline | Prefer GPTZero version-pin or DivEye; note RoBERTa is GPT-2-era |
| Provenance > classification | Authorship/Replay are institutional endgame | Document in education-facing copy (AGENT-57) |
| Public classifier lasted 5.5 months | Vendor detector versioning matters | Log detector version in benchmarks |
| Quiet shutdown | Users may not know OpenAI exited | FAQ: "Does OpenAI detect AI text?" → No public tool since Jul 2023 |

### Suggested copy snippets (internal / Boundaries)

- *"OpenAI discontinued its public AI text classifier in July 2023 (26% detection rate, 9% false positives on its own benchmarks). The company has not shipped text watermarking in ChatGPT despite internal tools reported at 99.9% accuracy."*
- *"unslop is not a Turnitin bypasser. It exists partly because post-hoc detectors falsely flag constrained registers — the same equity concern OpenAI cited when withholding watermarking."*

### Benchmark hygiene

When running `benchmarks/` or `detector.py` feedback loops:

1. Do **not** treat `openai-community/roberta-*-openai-detector` as a 2026 commercial proxy.  
2. If comparing to historical papers (Liang, DIPPER), label RoBERTa as **"OpenAI GPT-2 baseline (2019)"**.  
3. Primary commercial targets: GPTZero (`predicted_class`, version string), Turnitin, Originality — per AGENT-57 / AGENT-62.

---

## Bottom line

OpenAI's classifier shutdown was not a technical footnote — it was the **generator officially walking away from post-hoc text scoring** after publishing numbers too weak for education and too honest to walk back. The company then **refused to deploy** a far more accurate watermark for commercial, equity, and bypass reasons, while signing government commitments limited to **audio/visual** marking. Third-party detectors prospered in the gap; institutions slowly moved toward **process provenance** and **multi-signal review**. For unslop, the lesson is narrow and durable: **no first-party OpenAI text detector exists; third-party and open-method skepticism is warranted; defensive humanization for ESL/resume users sits on the same equity grounds OpenAI itself invoked.**

---

## Cross-references in this research batch

- [AGENT-17-SADASIVAN-IMPOSSIBILITY.md](./AGENT-17-SADASIVAN-IMPOSSIBILITY.md) — policy retreat after shutdown  
- [AGENT-18-LIANG-ESL-BIAS.md](./AGENT-18-LIANG-ESL-BIAS.md) — OpenAI RoBERTa in 7-detector panel  
- [AGENT-39-ADVERSARIAL-PARAPHRASING-GITHUB.md](./AGENT-39-ADVERSARIAL-PARAPHRASING-GITHUB.md) — shutdown as vendor-exit precedent  
- [AGENT-57-GPTZERO-EVOLUTION.md](./AGENT-57-GPTZERO-EVOLUTION.md) — who filled the vacuum  
- [AGENT-31-DIPPER.md](./AGENT-31-DIPPER.md) — pre-shutdown OpenAI classifier evasion numbers  
- [AGENT-20-WATERPARK-BENCHMARK.md](./AGENT-20-WATERPARK-BENCHMARK.md) — watermark vs paraphrase
