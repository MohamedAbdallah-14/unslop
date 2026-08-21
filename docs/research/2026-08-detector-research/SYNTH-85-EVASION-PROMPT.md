# SYNTH-85 — Prompt/Rule-Based Evasion Strategies for unslop

**Synthesis agent:** #85  
**Date:** 2026-08-19  
**Inputs:** Agent memos #21–40, #33 (ANTISLOP), #37 (peakoss)  
**Scope:** Strategies unslop can adopt **without fine-tuning, RL, gradient evaders, or logit access** — deterministic rules, skill prompts, and optional multi-call LLM pipelines only  
**Out of scope:** MASH Style-SFT/DPO, HIP LoRA, StealthRL/AuthorMist GRPO, GradEscape pseudo-embeddings, CoPA contrastive decoding, TempParaphraser 1B weights, StyleShield embedding flow, ToBlend token ensemble

---

## Executive summary

The evasion literature (MASH, HIP, TempParaphraser, Adversarial Paraphrasing, CoPA, GradEscape, StealthRL, AuthorMist, DIPPER, ToBlend) converges on one operational fact: **detectors read distributional geometry**, not vocabulary alone. Trained humanizers win by optimizing against detector scores. unslop cannot ship that stack.

What unslop *can* ship is the **decomposition** those papers imply — mapped to prompts and rules:

| Layer | Mechanism | Literature source | unslop home |
|-------|-----------|-------------------|-------------|
| **L0** | Lexical + pattern subtraction | ANTISLOP, blader/humanizer, AdvPara (negative lesson) | `humanize.py`, SKILL.md |
| **L1** | Structural burstiness + register | AdvPara, GradEscape style-disparity, StyleShield PPL | `structural.py`, `soul.py` |
| **L2** | Surprisal / dynamics targets | StyleShield, DivEye, TSD gap | `surprisal.py`, Phase 2 |
| **L3** | Multi-call alignment | MASH S1 (draft→critique→fix) | `llm_pipeline.py` S1 |
| **L4** | Cross-model iterative paraphrase | HIP, DIPPER, ToBlend (capstone), Agent #35 | S2 + S5 |
| **L5** | Multi-sample sentence pick | TempParaphraser | S3 |
| **L6** | Detector-guided span rewrite | Adversarial Paraphrasing (document analog) | S4 + `detector.py` |

**Headline constraint from AdvPara:** lexical-only rewrite can **raise** detector TPR (+8.57% RADAR, +15.03% Fast-DetectGPT). Rule-based evasion must always run **structural before or with** lexical LLM passes. `subtle` is slop removal, not anti-detector.

**Headline constraint from StyleShield/RateAudit:** document-level percentages are **gameable** — unslop must never optimize toward a target detector score. TMR is diagnostic; preservation contract is hard stop.

**Honest ceiling:** StealthRL/AuthorMist (T3 trained adversaries) collapse Fast-DetectGPT/Binoculars to ~0% TPR@1%FPR. unslop deterministic moves TMR ~0.0–0.2 pp. Phase 3 LLM pipeline target: **≥5 pp TMR improvement on ≥3 fixtures** — not MASH's 92% ASR or TempParaphraser's 82.5 pp accuracy drop.

---

## 1. Threat-model placement

| Tier | Actor | unslop coverage |
|------|-------|-----------------|
| **T0** | Raw AI output | N/A |
| **T1** | Deterministic unslop (regex, structural, soul) | **Shipped** — slop + light distributional nudge |
| **T2** | Prompted LLM pipeline + cross-model manual pass | **Phase 3** — primary product path for anti-detector |
| **T3** | StealthRL / AuthorMist / MASH weights | **Refuse** — cite as upper bound only |

unslop anti-detector mode = **T1→T2** for ESL false-positive defense and resume polish. Boundaries unchanged.

---

## 2. Five-signal targeting matrix

2026 detectors fuse largely independent signals. Prompt/rule strategies must name which signal they move.

| Signal | What detectors read | Prompt/rule levers | Trained-only (refuse) |
|--------|---------------------|--------------------|-----------------------|
| **S1 Lexical AI-isms** | Stock vocab, hedging, tricolons | L0 regex, blader patterns, CoPA anti-machine negative spec | — |
| **S2 Sentence-length σ** | Uniform rhythm, bullet soup | L1 `structural.py`, MASH critique list | — |
| **S3 Surprisal variance** | Low-entropy regularity (DivEye) | L2 `--surprisal-variance` targets; StyleShield PPL injection *concept* | StyleShield γ embedding flow |
| **S4 Late-stage stability (TSD)** | Position-aware volatility | L2 Phase 2 rules (not yet shipped) | — |
| **S5 Cross-model fingerprint** | Instruction-tuning artifacts (HIP) | L4 cross-family rewrite, plain HIP tags | HIP LoRA, ToBlend token splice |
| **S6 Detector boundary** | Target-specific decision surface | L6 span loop with TMR; **not** score targeting | MASH DPO, GradEscape, AuthorMist GRPO |

**Gap honesty:** MASH, HIP, StealthRL never evaluated DivEye/TSD/GPTZero v6 cones. No prompt-only stack is sufficient against the full 2026 commercial panel without empirical bench.

---

## 3. Recommended pipeline architecture

Gate entire stack behind `--intensity anti-detector` and `--llm-pipeline balanced|max`.

```
Input text
  → L0  deterministic lexical (humanize.py) — never alone for anti-detector
  → L1  structural + soul (+ voice-match profile if set)
  → L2  surprisal/dynamics measurement (optional stop if variance flat)
  → L3  S1 MASH-style: draft → detector-critique → constrained fix
  → L4  S2 HIP: 1–4 cross-model plain paraphrase rounds
  → L5  S3 TempParaphraser: N candidates × hot sentences, pick lowest TMR
  → L6  S4 AdvPara analog: top-K flat spans, rewrite, accept if TMR ↓
  → L4  S5 cross-model capstone (different provider than author)
  → validate.py preservation + AI_ISMS residual
  → detector.feedback_loop (diagnostic; escalate ladder incl. anti-detector)
```

**Stop rules (all stages):**

1. `validate.py` byte contract fails → reject output, do not escalate aggression.
2. Semantic preservation ≥0.92 (embedding or judge) on LLM stages.
3. TMR improves or holds — never greedy minimize to a **target** (RateAudit forbidden).
4. HIP rounds cap at 4; meaning drift dominates beyond that.
5. Single well-designed pass beats naive multi-pass (CoPA, MASH ablation).

---

## 4. Strategy catalog — deterministic rules (L0–L2)

### 4.1 Lexical subtraction (L0) — ANTISLOP + blader + AdvPara lesson

**Sources:** Agent #33, #32, #25  
**Mechanism:** Remove statistically over-represented AI patterns without injecting fake warmth.

| Rule family | Examples | unslop artifact |
|-------------|----------|-----------------|
| Stock vocab | delve, tapestry, leverage (filler), seamless, holistic | `STOCK_VOCAB` |
| Sycophancy | "Great question", "I'd be happy to" | `SYCOPHANCY` |
| Hedging stacks | "It's important to note that" | `HEDGING_OPENERS` |
| Transition tics | Furthermore, Moreover, In conclusion | `TRANSITION_TICS` |
| Performative balance | "Not X, but Y" tricolons | `PERFORMATIVE` + structural |
| blader #34–35 | Fake objection answers, rejected alternatives | **Add to SKILL.md** (Agent #32 P0) |

**AdvPara rule:** Do not market `subtle` or lexical-only LLM as anti-detector. Document +8–15% TPR regression on naive paraphrase.

**blader imports (prompt-side, no code):**

- Two-question self-audit before final output (Q1: what still sounds AI? Q2: any fact drift?)
- False-positive guard: don't strip deliberate em dashes, salutations, quoted third-party slop
- Three output modes: pasted / file / embedded (reduce token waste)

### 4.2 Structural burstiness (L1) — AdvPara + GradEscape + StyleShield

**Sources:** Agent #25, #29, #23  
**Mechanism:** Detectors exploit **style disparity** — uniform sentence length, parallel bullets, flat paragraphs. GradEscape's active-paraphrase *defense* and unslop's evasion pass share the same insight: normalize expression *shape* toward human variance.

| Target | Human-ish band | Rule |
|--------|----------------|------|
| Sentence-length σ | ~8.2 (human) vs ~4.1 (GPT-4o) | Split long sentences; merge bullet soup |
| Contraction rate | Human floor per genre | `soul.py` |
| Paragraph shape | Avoid 5-sentence symmetric blocks | `structural.py` flat-paragraph detection |
| Em-dash cap | ≤2 per paragraph (list carve-out) | `_cap_em_dashes_per_paragraph` |

**StyleShield γ analog → intensity tiers:**

| γ (StyleShield) | unslop mode | Budget |
|-----------------|-------------|--------|
| 5.0–5.5 mild | `subtle` / `balanced` | Regex + stock vocab only |
| 6.0–6.5 moderate | `full` | + structural + soul + optional LLM |
| 7.0 strong | `anti-detector` | Max deterministic + LLM pipeline |

Document the trade-off explicitly — discrete steps, not continuous embedding perturbation.

### 4.3 Surprisal / dynamics (L2) — StyleShield PPL + DivEye

**Sources:** Agent #23, #34 (via landscape)  
**Mechanism:** StyleShield shows output PPL **21.2** vs human **16.5** vs AI **10.7** — detectors exploit low-entropy regularity. unslop cannot inject embedding noise; it **measures** and nudges:

- Wire `surprisal.py` stdev into feedback loop when TMR plateaus (Phase 1).
- Phase 2: TSD second-half volatility target, SurpMark transition recovery — rule thresholds on measured dynamics.
- Stop if semantic validator fails — StyleShield A5 lesson (no conditioning → evasion via destruction).

---

## 5. Strategy catalog — prompt-based LLM stages (L3–L6)

### 5.1 S1 — MASH align + refine (3-call chain)

**Source:** Agent #21  
**Maps:** Style-SFT → DPO hard negatives → Stage 4 polish — **without training**.

| Call | MASH analog | Prompt intent |
|------|-------------|---------------|
| **S1a Draft** | Style-SFT | Rewrite toward natural human register; apply unslop anti-slop rules; preserve meaning |
| **S1b Critique** | DPO implicit reward | List remaining machine tells **as a detector would**: uniform rhythm, hedging, safe parallelism, low-variance sentences — cite phrases |
| **S1c Fix** | Hard-negative rejection | Revise **only** flagged spans; do not reintroduce S1b patterns; strict preservation |

**Optional S1d (Stage 4 analog):**

1. Rank sentences by proxy fluency (local PPL if `--surprisal-variance`; else length/variance heuristic).
2. Polish top-K "flat" sentences.
3. Accept only if TMR improves or holds.

**Conditioning block:** Inject `stylometry.py` / `style_memory.py` voice profile into S1a as numeric targets (partial MASH style embedding analog).

**Env surface (proposed):**

```bash
UNSLOP_LLM_PIPELINE=balanced
UNSLOP_MASH_S1=1
UNSLOP_MASH_REFINE=1
UNSLOP_MASH_REFINE_TOPK=5
```

### 5.2 S2 — HIP iterative cross-model paraphrase

**Source:** Agent #22, #35, #31  
**Mechanism:** Commercial detectors flag **instruction-tuning artifacts**; different model family = different conditional distribution. Approximate HIP Stage 3 without LoRA.

| Rule | Detail |
|------|--------|
| **Cross-model** | If text from Claude, paraphrase via GPT or Gemini (and vice versa) |
| **Plain format** | No assistant persona; HIP tags or minimal rewrite instruction |
| **Rounds** | 1–4 (not 10); stop on preservation failure or TMR plateau |
| **Prompt skeleton** | See below |

```
Rewrite the text inside <source> toward natural human prose.
Preserve every fact, number, name, and citation exactly.
Vary sentence length. No hedging openers. No stock AI vocabulary.

<source>
{TEXT}
</source>

<target>
```

**DIPPER analog within rules:** Discourse-aware rewrite (full paragraph context in prompt), not sentence-at-a-time unless S3. Encourage light reordering where meaning allows (O-diversity concept).

### 5.3 S3 — TempParaphraser multi-sample selection

**Source:** Agent #24, #38  
**Mechanism:** N independent paraphrases at normal temperature → pick lowest detector score. Jensen's inequality: ensemble entropy widens without raw high-T quality collapse.

**API port (no fine-tuned 1B model):**

```
For each flagged sentence (high TMR chunk, low surprisal variance, or flat σ):
  1. Generate N=2–3 paraphrases via Model B (batched)
  2. Score each with detector.py (TMR) on merged document
  3. Keep lowest p_ai candidate passing validate.py
  4. Reassemble
```

| Paper default | unslop pragmatic |
|---------------|------------------|
| N=7, fine-tuned 1B | N=2–3, API model |
| Period sentence split | Upgrade to BlingFire optional |
| HC3 selector | TMR local scorer |

**Fix doc bug:** TempParaphraser requires LLM inference; only the *recommendation* after deterministic exhaust is LLM-optional.

### 5.4 S4 — Adversarial Paraphrasing span loop (document analog)

**Source:** Agent #25, #39  
**Mechanism:** Token-level detector argmin is not portable on API models. Document-level analog:

```
1. Score full text with TMR
2. Identify top-K sentences/spans with highest local AI signal (chunk mean or heuristic)
3. LLM rewrite span only: "Rephrase for human rhythm; preserve meaning"
4. Accept merge only if document TMR improves
5. Max 3 iterations; then recommend S5 cross-model
```

**CoPA dual-prompt inside span rewrite (Agent #28):**

```text
Rewrite in a casual human voice (like a text to a friend — no greeting, no emoji).

While rewriting, actively REMOVE patterns associated with AI assistant output:
- even sentence rhythm and parallel structure
- hedging openers ("It's important to note", "In today's world")
- stock transitions (Furthermore, Moreover, In conclusion)
- overly safe, symmetrical paragraphs

Keep meaning exact. Keep code, URLs, headings, and quoted material unchanged.
```

This is the **prompt analog** of CoPA's human logit minus machine logit — without logit access.

**Do not:** subprocess `chengez/Adversarial-Paraphrasing` in default pip wheel (CUDA, cluster paths). Optional `--adv-paraphrase /path` for research users only.

### 5.5 S5 — Cross-model capstone (ToBlend/HIP practitioner technique)

**Source:** Agent #30, #35  
**Mechanism:** ToBlend breaks detectors by **mixing generator manifolds** at token level — unslop approximates at **document level** via family swap.

**Protocol (user- or pipeline-orchestrated):**

1. Run L0–L6 on Model A's output locally.
2. Final pass through Model B from different family with light prompt: *"Rewrite for clarity. Preserve all facts verbatim. Vary syntax."*
3. Manual fact restore (numbers, dates, citations).
4. Re-score with target detector if needed.

**ToBlend QPA insight:** If multiple capstone candidates, pick **quality-ranked** merge (readability + preservation), not random — random token blend destroys semantics; unslop preserves contract.

**Already shipped:** `detector.py` ladder-exhaustion message cites TempParaphraser + AdvPara; keep SSOT sync.

---

## 6. Detector feedback loop — rule refinements

**Sources:** Agent #23, #25, #27, #35

| Rule | Rationale |
|------|-----------|
| Add `anti-detector` to ladder (Phase 1 P0) | Loop currently stops at `full+structural+soul` |
| TMR is **diagnostic**, not optimization target | RateAudit: aggregate % is schedulable |
| Run distribution shaping (S2–S5) **before** feedback loop | Sadasivan: paraphrase first, then residual cleanup |
| On exhaust: print cross-model recommendation | Strongest honest product lever (Agent #35) |
| Never recommend watermark removal | EU AI Act Art. 50 |
| Do not ship RateAudit-style greedy chunk scheduling | UPDATE-PLAN explicit refusal |

**AuthorMist analog (8-candidate rerank):** `--detector-feedback` 3–5 step ladder ≈ single-pass rerank, not GRPO policy. Do not bundle `authormist-originality` weights.

---

## 7. Mode interactions and conflicts

### 7.1 voice-match vs anti-detector

**Source:** Agent #27, #52 (cross-ref)

| Mode | Optimizes |
|------|-----------|
| voice-match | `StyleProfile(output) ≈ StyleProfile(sample)` |
| anti-detector | Leave low-σ, low-contraction ESL basin if sample is formal |

**Rule:** Do not merge modes without explicit floors:

```
voice-match first (slop removal)
→ anti-detector only if user opts in
→ floors: max(sample_σ, 6), max(sample_contractions, human_floor)
```

AuthorMist is **not** a voice-match backend — no authorship embedding.

### 7.2 HumanLLM (Agent #36) — orthogonal axis

HumanLLM scores **cognitive pattern fidelity** (IPE/MPD), not detector evasion. Optional eval slice for dialogue/scenario prose; not a substitute for TMR bench.

### 7.3 peakoss / ANTISLOP (Agent #33, #37) — stack, not competition

```
Vendor Custom Styles (generation)
  → ANTISLOP sampler/FTPO (self-hosted only)
  → unslop hooks/CLI (post-generation)     ← this synthesis
  → peakoss/anti-slop (maintainer PR gate, optional)
```

**Partnership preset (docs only):** Export high-precision `blocked-terms` for agent footers (`Generated with Claude Code`, honeypot STRAWBERRY pattern). Do **not** dump full `STOCK_VOCAB` into peakoss — case-sensitive substring false positives.

---

## 8. Explicit refusals (trained / infrastructure)

| Method | Why refuse | What to steal |
|--------|------------|---------------|
| MASH Style-SFT + DPO | Requires BART training + detector oracle | Stage decomposition → S1 prompts |
| HIP LoRA | Requires base model + vLLM | Iteration + plain tags → S2 |
| StealthRL / AuthorMist GRPO | T3 adversary; quality tax | Threat-model tier citation |
| GradEscape | 139M gradient evader + Zenodo training | Style-disparity diagnosis |
| CoPA logit contrast | Needs 2× forward pass per token | Dual-prompt block → S4 |
| TempParaphraser weights | Academic-only license; LLaMA-Factory stack | N-candidate selection → S3 |
| StyleShield flow matching | 128×A800, Chinese vocab | γ tiers + RateAudit **critique** |
| ToBlend token ensemble | 80 GB, ROUGE ~0.26 | Cross-model capstone → S5 |
| RateAudit score targeting | Integrity gaming | Document trust crisis only |
| Commercial L1 humanizers | Cloud paste-box; DAMAGE 20–100 pp marketing gap | Honesty in README |

---

## 9. Implementation priority

| Priority | Action | Effort | Source agents |
|----------|--------|--------|---------------|
| **P0** | Wire `anti-detector` on detector feedback ladder | S | #25, #35, UPDATE-PLAN |
| **P0** | CoPA dual-prompt + anti-machine negative in `_INTENSITY_PROMPT_GUIDANCE["anti-detector"]` | S | #28 |
| **P0** | Document `subtle` ≠ anti-detector; cite AdvPara +8–15% | S | #25 |
| **P0** | Fix TempParaphraser "no LLM" comment in `detector.py` | S | #24, #38 |
| **P1** | Implement `llm_pipeline.py` S1 (MASH 3-call) | M | #21 |
| **P1** | S2 HIP rounds + `--hip-rounds` env | M | #22 |
| **P1** | S4 span loop with TMR gate | M | #25 |
| **P1** | blader patterns #34–35 + false-positive guard in SKILL.md | S | #32 |
| **P1** | Surprisal stdev in feedback stop policy | M | #23, SYNTH-83 |
| **P2** | S3 TempParaphraser batched N-candidate | M | #24, #38 |
| **P2** | S5 cross-model prompt templates | S | #30, #35 |
| **P2** | S1d PPL-ranked polish | M | #21 |
| **P2** | `examples/ci/anti-slop-blocked-terms.txt` preset | S | #37 |
| **P3** | Bench pipeline vs May detector-test panel | L | #40, drafts/2026-05 |
| **—** | Do not ship DPO/GRPO/GradEscape/StealthRL weights | — | #26, #27, #29 |

**Acceptance (Phase 3):**

- Pipeline beats legacy `humanize_llm()` by **≥5 pp TMR** on ≥3 fixtures
- Semantic preservation **≥0.92**
- `TestPreservation` **100%**
- No "92% ASR" / "82.5% undetectable" marketing — benchmark snapshots only

---

## 10. Honesty constraints (DAMAGE + StealthRL)

**Source:** Agent #40, #26

| Claim | Allowed | Forbidden |
|-------|---------|-----------|
| Removes AI-isms, improves voice | ✅ | — |
| Moves TMR ~0.0–0.2 pp deterministic | ✅ with bench cite | — |
| ESL false-positive mitigation | ✅ | — |
| Beats Turnitin/GPTZero/Pangram | ❌ | Without fixture-specific re-run |
| "HIP-powered" / "MASH-powered" | ❌ | Implies trained weights |
| Target detector score X% | ❌ | RateAudit gaming |
| Same tier as Undetectable.ai | ❌ | L1 SaaS = cloud evasion product |

**Threat-model sentence for README (optional):**

> Open research (StealthRL, Feb 2026) shows a fine-tuned 4B paraphrase model can collapse Fast-DetectGPT and Binoculars to near-zero TPR@1%FPR. unslop is T1–T2 polish, not T3.

---

## 11. Prompt template quick reference

### Anti-detector intensity (CoPA + unslop rules)

```text
Rewrite for a human reader. Preserve all facts, code, URLs, headings, and quotes exactly.

REMOVE AI-assistant patterns:
- uniform sentence length and parallel structure
- hedging stacks and sycophancy openers
- stock transitions (Furthermore, Moreover, In conclusion)
- significance inflation and performative balance
- em-dash pileups (max two per paragraph)

ADD human rhythm:
- mix short and long sentences deliberately
- use contractions where natural
- allow one rough edge or direct fragment if honest

Do not invent facts. Do not soften refusals or disagreement.
```

### MASH S1b critique (detector-eye)

```text
You are simulating a 2026 AI-text detector. List specific phrases in the INPUT
that would raise AI score: rhythm uniformity, low perplexity bands, hedging,
safe parallelism, template transitions. Quote each phrase. Do not rewrite yet.
```

### HIP round (cross-model)

```text
<source>{TEXT}</source>
Rewrite everything inside source as natural human prose. Same meaning.
No assistant voice. Vary sentence length. Output only the rewritten text.
```

### TempParaphraser pick (per sentence)

```text
Provide {N} alternative phrasings of this sentence. Same meaning.
Each on its own line numbered 1–{N}. No other commentary.
```

---

## 12. Cross-reference index

| Agent | Topic | Prompt/rule takeaway |
|-------|-------|---------------------|
| #21 MASH | Style humanization | S1 3-call + S1d polish |
| #22 HIP | Iterative paraphrase | S2 cross-model, 1–4 rounds |
| #23 StyleShield | Embedding evasion | γ tiers; refuse RateAudit |
| #24 TempParaphraser | Multi-sample | S3 N-candidate argmin |
| #25 AdvPara | Token search | Structural mandatory; S4 span analog |
| #26 StealthRL | RL evasion | T3 upper bound only |
| #27 AuthorMist | API-reward RL | voice-match conflict |
| #28 CoPA | Contrastive decode | Dual-prompt block |
| #29 GradEscape | Gradient evader | Style-disparity insight |
| #30 ToBlend | Token ensemble | S5 cross-model only |
| #31 DIPPER | Discourse paraphrase | L/O via structure + cross-model |
| #32 blader | Prompt humanizer | Pattern taxonomy + audit |
| #33 ANTISLOP | Slop subtraction | L0 philosophy alignment |
| #35 Cross-model | Practitioner #1 | Capstone + ladder message |
| #36 HumanLLM | Anthropomorphism | Orthogonal eval |
| #37 peakoss | CI gate | Maintainer layer; blocked-terms preset |
| #40 DAMAGE | Commercial tiers | Honesty; no bypass marketing |

---

## Bottom line

Trained evaders (MASH, HIP, StealthRL, AuthorMist, GradEscape) share a shape: **separate style alignment from boundary crossing from gated polish**. unslop can adopt that **architecture** as a prompt pipeline on top of deterministic L0–L2 rules — without claiming their ASR numbers.

The rule-based non-negotiables:

1. **Never lexical-only** for anti-detector (AdvPara regression).
2. **Always structural + soul** before LLM evasion passes.
3. **Cross-model family swap** is the strongest practitioner lever unslop can document and partially automate (S2/S5).
4. **Multi-sample sentence pick** is the TempParaphraser port (S3).
5. **Detector-guided spans**, not score targeting (S4 + TMR diagnostic).
6. **Preserve byte-exact** code/URLs/headings — the semantic anchor StyleShield's Qwen conditioning approximates.

Ship T1→T2 honestly. Measure on unslop fixtures. Cite StealthRL as the ceiling, DAMAGE as the marketing gap, RateAudit as the reason aggregate detector percentages are not evidence.

---

*SYNTH-85 complete. Feeds UPDATE-PLAN Phase 3 `llm_pipeline.py` spec and anti-detector SKILL.md refresh.*
