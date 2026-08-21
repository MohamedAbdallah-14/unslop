# Agent #44 — Blandification / Neutralization of AI Text Style

**Topic:** Stance flattening, voice erosion, and semantic drift in LLM-assisted writing  
**Prepared:** 2026-08-19  
**Status:** Complete research memo for unslop detection-landscape update

---

## Executive summary

**Blandification** is the practitioner label for a measured academic effect: LLM-assisted writing converges toward argumentative neutrality, formal detachment, and a shared "house voice" that overwrites author idiolect. The strongest quantification comes from Abdulhai et al. (arXiv 2603.18161, March 2026): heavy LLM use produced a **68.9% increase** in essays that stayed neutral on a for/against prompt, plus self-reported loss of creativity and voice. The effect is not cosmetic. Even "grammar only" edits shift semantic embeddings in a **common direction across models**, toward a region of embedding space no human essay occupied.

**Neutralization** is the mechanism: RLHF-aligned models optimize for broadly acceptable, premise-matching, low-conflict prose. Rallapalli et al. (arXiv 2604.14111, April 2026) show instruction-tuned chat models cluster in stylometric space regardless of base architecture — homogenization is a post-training artifact, not a GPT-vs-Claude quirk. Xu & Zubiaga (arXiv 2503.17965) add that RLHF **increases detectability** by narrowing output diversity toward stereotyped syntactic and lexical patterns detectors already hunt.

**Detection implication:** Blandified text is *easier* to flag as AI-generated, not harder. Uniform stance, low burstiness, zero contractions, and analytical LIWC scores are exactly the features DivEye-style surprisal-variance detectors and stylometric classifiers exploit. Humanizers that "neutralize" further amplify the homogenization signal. Commercial tools marketing "neutralize every detector" conflate evasion with voice destruction — and Turnitin's August 2025 anti-humanizer update specifically targets uniform-structure humanizer outputs.

**unslop balanced mode** sits deliberately between subtractive cleanup and full rewrite. It cuts stock AI vocabulary and hedging stacks, engineers burstiness, and allows opinions and fragments — but its LLM path carries an explicit **ANTI-BLANDIFICATION** block citing the 70% figure, instructing the model to preserve strong stances, unusual metaphors, and distinctive claims. Deterministic mode is subtractive by construction (regex removal only). Balanced is the default because it removes slop without the stance-flattening risk of aggressive humanizers or the insufficient coverage of subtle mode on sycophancy and hedging.

---

## What blandification is (and is not)

### Definition

**Blandification** names the convergence of LLM-assisted text toward:
1. **Argumentative neutrality** — for/against essays become "on the one hand… on the other hand" non-committal summaries.
2. **Voice flattening** — colloquialisms, anecdotes, and idiosyncratic metaphors get replaced by generic analytical framing.
3. **Semantic drift** — intended meaning shifts even when the user asked for surface edits only.

Psychology Today popularized the term in March 2026, covering Abdulhai et al.: https://www.psychologytoday.com/us/blog/emotional-behavior-behavioral-emotions/202603/llms-and-the-blandification-of-writing

**Neutralization** is the underlying process: the model sandpapers distinctive stance, emotion, and lexical fingerprint toward RLHF's preferred register — helpful, balanced, non-inflammatory, analytically structured.

These are **not** the same as removing AI-isms (`delve`, `tapestry`, tricolon padding). Stripping stock vocabulary can *reduce* one homogenization channel while accidentally *increasing* another if the rewriter also softens claims. A humanizer that deletes slop but preserves "I think X is wrong because…" is anti-blandification. One that rewrites that sentence as "There are several perspectives to consider regarding X" is blandification with extra steps.

### Distinction from related concepts

| Concept | What it captures | Key source |
|---------|------------------|------------|
| **Blandification / neutralization** | Stance + voice + meaning drift toward safe centrism | arXiv 2603.18161 |
| **Stylistic homogenization** | Cross-model convergence in Biber/LIWC feature space | arXiv 2604.14111 |
| **Alignment tax / response homogenization** | DPO/RLHF collapses output diversity; sampling uncertainty dies | arXiv 2603.24124 |
| **Stylistic collapse** | Entropy redistribution in instruction-tuned models | arXiv 2605.28826 |
| **Population homogenization** | AI lifts individual quality but clusters collective output | Doshi & Hauser, *Science Advances* 2024 |

---

## Academic evidence

### Primary measurement: Abdulhai et al. (2026)

**Paper:** *How LLMs Distort Our Written Language*  
**URL:** https://arxiv.org/abs/2603.18161  
**Code:** https://github.com/abdulhaim/llm_writing_distortion  
**Project page:** https://sites.google.com/view/llmwritingdistortion/home

Three empirical legs:

**1. Randomized controlled trial (N=100).** Participants wrote an argumentative essay ("Does money lead to happiness?") with or without embedded gpt-4o-mini. Heavy LLM users (generating >40% of text via model) reported essays were significantly less creative (p=0.039) and **not in their voice** (p<0.001) — yet reported similar satisfaction. Paradox: users like the output while losing ownership.

**2. Counterfactual edit analysis (ArgRewrite-v2, 86 pre-ChatGPT essays).** Human edits produce small, multidirectional semantic shifts in embedding space. LLM edits (gpt-5-mini, gemini-2.5-flash, claude-haiku) produce **large, aligned shifts** in a common direction — including under "minimal edits" and "grammar only" prompts. LLMs roughly **double** positive and negative sentiment markers while increasing analytical LIWC scores. Lexical divergence (JSD) for gpt-5-mini edits approaches **triple** the human baseline.

**3. ICLR 2026 peer reviews in the wild.** 21%+ LLM-generated (Pangram classifier); 39% additional LLM-edited traces. LLM reviews weight reproducibility/scalability over clarity/impact; average scores ~1 point higher. Institutional criteria shift, not just prose polish.

The 68.9% neutral-stance increase is the headline number practitioners cite as "~70% blandification."

### Structural cause: RLHF and instruction tuning

**Rallapalli et al. — *Interpretable Stylistic Variation in Human and LLM Writing***  
**URL:** https://arxiv.org/abs/2604.14111

Large-scale Biber-feature analysis across 11 LLMs, 8 genres, 4 decoding strategies. Finding: **genre > model > decoding** for stylistic variation, but instruction-tuned chat variants of different model families **cluster together** in stylometric space. RLHF/instruction tuning is the proximate homogenizer — explaining why "the AI voice" persists across vendors.

**Xu & Zubiaga — *Understanding the Effects of RLHF on the Quality and Detectability of LLM-Generated Texts***  
**URL:** https://arxiv.org/abs/2503.17965

SFT and RLHF iterations make LLM outputs **more detectable**, not less. Hypothesis: alignment internalizes stereotyped fluency patterns that detectors already recognize. Direct link between homogenization and detection ease.

**Alignment tax paper (2026)**  
**URL:** https://arxiv.org/html/2603.24124

DPO drives **single-cluster response homogenization** on TruthfulQA (40–79% of questions produce one semantic answer across 10 samples). Base model: 1.0% single-cluster rate; instruct Qwen3-14B: 28.5%. Uncertainty methods break when alignment collapses diversity.

**Stylistic collapse (2026)**  
**URL:** https://doi.org/10.48550/arxiv.2605.28826

Instruction-tuned systems show extreme entropy redistribution on discourse/structural probes (mean amplification 1,949–16,853%). Weak entropy regularization **worsens** collapse; strong regularization (λ=5.0) recovers diversity. Implication: blandification is a training-pipeline property, not fixable by prompt alone at scale.

**Trends in Cognitive Sciences review (2026)**  
**URL:** https://www.rivista.ai/wp-content/uploads/2026/03/1-s2.0-S1364661326000033-main.pdf

Synthesizes homogenization across expression, perspective, and reasoning. RLHF amplifies frequent, generalizable patterns; synthetic training data and reward optimization further narrow stylistic range.

### Population-level and cultural dimensions

**Doshi & Hauser — *Generative AI enhances individual creativity but reduces collective diversity***  
**URL:** https://www.science.org/doi/10.1126/sciadv.adn1265

AI assistance improves individual story creativity ~10–11% and readability ~22–26%, but **clusters** assisted stories significantly vs. unassisted. Individual gain, collective sameness — the social-dilemma framing for humanizers.

**CHI 2025 — AI suggestions homogenize toward Western styles**  
**URL:** https://arxiv.org/abs/2409.11360

Non-Western writers pushed toward Western stylistic norms via AI suggestions. Blandification has a cultural vector, not just a formality vector.

**EMNLP 2025 — "Catch Me If You Can?" personal-style imitation**  
**URL:** https://arxiv.org/abs/2509.14543

Six frontier models fail at implicit everyday-author style imitation. Catch Me reports ~2–3× few-shot gain over zero-shot but still insufficient; Jemama reports up to 23.5× with few-shot prompting on a separate academic-essay corpus. Prompt-only "preserve my voice" remains domain-sensitive — relevant because blandification is the default when voice preservation fails.

---

## Practitioner sources

### Naming and awareness

- **Psychology Today "Blandification"** (March 2026): https://www.psychologytoday.com/us/blog/emotional-behavior-behavioral-emotions/202603/llms-and-the-blandification-of-writing — mainstream vocabulary for the 70% figure.
- **Practitioner voice guides** (Cat 10 synthesis): converged 5-step recipe (collect samples → extract style → inject → few-shot → iterate) at https://github.com/TamSiuhin/P2P and commercial tools (VoiceDNA, My Writing Twin). Recurring insight: **rejection profiles** (what you'd never write) outperform preference lists — because LLMs default to corpus-mean "safe" prose unless actively constrained.

### Humanizer market conflation

Commercial humanizers often brand **neutralization** as a feature, not a bug:

- **HumanifyLab:** "Neutralize Every Detector in Seconds" — https://humanifylab.com/ (tagline documented in Cat 18 commercial synthesis)
- **Walter Writes:** surged 517% YoY in early 2026; Turnitin August 2025 update partially recovered detection (now ~38% flagged per internal research notes)

The market sells **detector evasion via further homogenization** — shorter sentences, synonym swaps, uniform structure — which is precisely what post-2025 detectors (Turnitin anti-humanizer, DivEye surprisal-variance) target. Blandification-as-service creates a detectable secondary fingerprint.

### Practitioner failure modes

From HN/Reddit synthesis (Cat 10 E-practical):

1. **"Grammar check" prompts** that silently rewrite argument structure — matches Abdulhai et al.'s grammar-only finding.
2. **Custom Instructions decay** after ~10 turns — model regresses to RLHF mean; voice files need per-session reinjection.
3. **Hyperbolic trick** (lsusr): models regress to mean, so practitioners amplify style past target then trim — implicit acknowledgment that neutralization is the default gradient.
4. **Skeptic counter-current:** laundering AI output through voice tools without disclosure — frames blandification as an integrity problem, not just quality.

---

## Detection implications

Blandification interacts with detection in counterintuitive ways.

### Bland text is more detectable, not less

Homogenized outputs share:
- **Low burstiness** — sentence-length σ ~4.1 for GPT-4o vs ~8.2 human (Paneru 2026, cited in unslop anti-detector spec)
- **Zero or near-zero contraction rate** in AI chunks
- **High analytical LIWC, low authenticity scores** — exactly what Abdulhai et al. measure post-LLM-edit
- **Aligned semantic embeddings** — multiple essays occupy the same cluster; classifiers exploit cross-document similarity

Xu & Zubiaga (2503.17965) confirm RLHF makes text **easier** for training-based and zero-shot detectors. Neutralization does not erase the machine fingerprint — it **concentrates** it.

### Humanizers that blandify create a second-order signal

Turnitin's August 2025 update explicitly targets humanizer-tool outputs (updated February 2026, FP <1% claimed). Anti-humanizer detection looks for:
- Uniform bullet syntax across a document
- Surprisingly low intra-document surprisal variance (DivEye, TMLR 2026 — https://arxiv.org/abs/2501.03406)
- Stereotyped rewrite patterns from commercial tools

A rewrite that removes `delve` but also removes stance creates **double homogenization**: RLHF base + humanizer smoothing. Detectors trained on humanizer outputs flag this harder than raw GPT prose in some benchmarks (Chicago Booth 2026 reference in unslop SKILL).

### False-positive intersection

Liang et al. (*Patterns* 2023): https://doi.org/10.1016/j.patter.2023.100779 — detectors misclassify >50% of TOEFL essays as AI. Formal, neutral, non-native academic prose **resembles** blandified LLM output. ESL writers and LLM-humanizers converge on the same detectable register: grammatically clean, low idiolect, hedged claims. Anti-blandification (preserving author stance and rough edges) helps **defensive** humanization for false-positive victims — but only if the preserved voice is genuinely theirs, not invented.

### What detectors cannot see

Detectors struggle when:
- User supplied concrete specifics (names, numbers, project details) absent from training data
- Cross-model second pass breaks single-family stylometric fingerprint (TempParaphraser, EMNLP 2025)
- Author's original voice was strong and preserved through subtractive edit

Balanced-mode unslop targets the first and third; anti-detector mode adds burstiness/contraction engineering and recommends cross-model pass for the second.

---

## unslop balanced mode: design against blandification

### Mode ladder (relevant slice)

From `skills/unslop/SKILL.md` (SSOT):

| Mode | Blandification risk | Coverage |
|------|---------------------|----------|
| **subtle** | Lowest rewrite risk; **insufficient** for sycophancy/hedging | Stock vocab trim only; structure unchanged |
| **balanced** | **Default.** Explicit anti-blandification in LLM path | Cut slop + vary rhythm + preserve opinions/fragments |
| **full** | Higher rewrite surface area — more stance drift risk if unchecked | Strong restructure; needs ANTI-BLANDIFICATION guard |
| **anti-detector** | Can over-smooth for detector evasion | Burstiness/contraction engineering; not stance preservation primary |

Balanced is the default because it matches the Abdulhai finding: responsible editing (not wholesale generation) still blandifies unless actively counter-instructed.

### Operational rules (balanced)

Balanced mode applies the full Rules block:
- Drop sycophancy, stock vocab, hedging stacks, performative balance, tidy essay shapes
- **Keep:** technical terms, real uncertainty, uneven paragraph length
- Engineer burstiness — mix 4–35 word sentences
- Allow short fragments and opinions

Principle #1 from SKILL: **"Subtract, don't add."** Warmth via added filler is sycophancy. Blandification via added hedging is the same failure mode from the opposite direction.

### ANTI-BLANDIFICATION block (LLM mode)

In `unslop/scripts/humanize.py` LLM prompt:

```
ANTI-BLANDIFICATION (critical):
- Do NOT neutralize distinctive claims, opinions, or stylistic choices from the original.
  LLM-assisted rewrites neutralize ~70% of author voice on average (arXiv 2603.18161).
- If the original has a strong stance, keep it. If it has an unusual metaphor, keep it.
  Strip the slop; preserve the signal.
```

Plus a **two-pass self-audit**: "Did I accidentally neutralize the original's voice or opinions?" Deterministic regex mode avoids LLM stance drift entirely — it only removes pattern-matched AI-isms inside `_protect()` placeholders.

### Worked example (balanced vs blandified failure)

Prompt: "Why is React re-rendering on every state update?"

- **Raw LLM slop:** "Great question! React re-renders child components when parent state changes. It's important to note that inline object props create new references. However, there are several approaches to consider…"
- **Blandified humanizer failure:** "React re-rendering occurs when parent components update. Inline object props may contribute to unnecessary re-renders. Developers should consider various optimization strategies including memoization."
- **unslop balanced:** "Parent re-renders → child re-renders. Inline object props create a fresh reference each render, so the child sees 'new' props even when the value is the same. Wrap the object in `useMemo`, or memoize the child with `React.memo`."

The balanced version keeps directive stance (`Wrap…`) and concrete fix; the blandified failure hedges into generality.

### What balanced mode cannot do

Per "Catch Me If You Can?" (2509.14543), prompt-based voice preservation fails stylometric attribution against the real author. Balanced preserves **explicit** stance and metaphors present in the input; it does not reconstruct idiolect absent from the source. For that, voice-match mode extracts stylometric signals (`stylometry.py`) — still prompt-limited — or fine-tuning (TinyStyler, Profile-to-PEFT).

---

## Recommendations for unslop product

1. **Treat blandification as a first-class failure mode** in validator output — flag hedging insertion and stance softening, not just residual `delve`.
2. **Default to balanced, not anti-detector** — evasion modes increase smoothness pressure; blandification and detectability rise together.
3. **Prefer deterministic pass first** on sensitive docs (subtractive = lower semantic drift risk per Abdulhai counterfactual).
4. **Cite 2603.18161 in user-facing docs** — the 70% figure is the strongest external justification for ANTI-BLANDIFICATION.
5. **Do not conflate "neutralize detectors" with "neutralize voice"** — opposite effects on detection after Turnitin 2025.

---

## Primary sources (full URLs)

| Resource | URL |
|----------|-----|
| **Abdulhai et al. — How LLMs Distort Our Written Language (2026)** | https://arxiv.org/abs/2603.18161 |
| **Project page + reproduction code** | https://sites.google.com/view/llmwritingdistortion/home |
| **GitHub reproduction** | https://github.com/abdulhaim/llm_writing_distortion |
| **Psychology Today — "Blandification" popularization** | https://www.psychologytoday.com/us/blog/emotional-behavior-behavioral-emotions/202603/llms-and-the-blandification-of-writing |
| **Rallapalli et al. — RLHF stylistic homogenization (2026)** | https://arxiv.org/abs/2604.14111 |
| **Xu & Zubiaga — RLHF increases detectability (2025)** | https://arxiv.org/abs/2503.17965 |
| **Alignment tax / response homogenization (2026)** | https://arxiv.org/html/2603.24124 |
| **Stylistic collapse / entropy redistribution (2026)** | https://doi.org/10.48550/arxiv.2605.28826 |
| **Trends in Cognitive Sciences homogenization review (2026)** | https://www.rivista.ai/wp-content/uploads/2026/03/1-s2.0-S1364661326000033-main.pdf |
| **Wang et al. — Catch Me If You Can? EMNLP 2025** | https://arxiv.org/abs/2509.14543 |
| **Doshi & Hauser — collective diversity loss** | https://www.science.org/doi/10.1126/sciadv.adn1265 |
| **CHI 2025 — Western style homogenization** | https://arxiv.org/abs/2409.11360 |
| **Liang et al. — detector ESL bias** | https://doi.org/10.1016/j.patter.2023.100779 |
| **DivEye surprisal-variance detection (2026)** | https://arxiv.org/abs/2501.03406 |
| **ArgRewrite-v2 dataset (pre-ChatGPT edits)** | https://arxiv.org/abs/2202.09694 |
| **unslop SSOT skill (balanced mode spec)** | `skills/unslop/SKILL.md` |
| **ANTI-BLANDIFICATION implementation** | `unslop/scripts/humanize.py` |

---

## unslop verdict

Blandification is the measured inverse of what unslop sells. Users ask for "sound human"; models deliver "sound safely inoffensive." The 70% neutral-stance figure is not a rounding error — it is the quantitative case for stance-preserving rewrite rules. **Balanced mode** is the product answer: aggressive enough to kill slop, constrained enough to keep the author's argument, with ANTI-BLANDIFICATION as explicit guardrail in LLM path. Detection-wise, blandification helps classifiers and hurts authors; anti-blandification is both a quality stance and a false-positive-defense strategy for writers whose natural register is already formal. Commercial humanizers that promise to "neutralize detectors" often neutralize voice instead — and post-2025 detectors hunt exactly that secondary uniformity.
