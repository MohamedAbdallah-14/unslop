# SYNTH-91 — Human-Writing Cues: Preserve vs Inject

**Synthesis Agent #91**  
**Date:** 2026-08-19  
**Scope:** Human-writing cue taxonomy for unslop — what to keep, what to add, what to strip  
**Sources:** AGENT-44 (blandification), AGENT-45 (four-cue taxonomy), AGENT-46 (alignment tax), AGENT-51 (warmth–reliability)  
**Audience:** unslop maintainers — SKILL.md, `humanize.py`, validator, anti-detector policy

---

## Executive summary

Four memos converge on one operational split:

**Preserve** = author signal. Stance, disagreement, refusals, calibrated uncertainty, idiosyncratic metaphors, concrete specifics, uneven paragraph length, and any voice already present in the source. These are what RLHF and commercial humanizers sand away — Abdulhai's ~70% stance neutralization, Liu's semantic cluster collapse, Ibrahim's sycophancy under false beliefs.

**Inject** = distributional human-likeness without stance drift. Burstiness (sentence-length variance), contraction rate toward human baselines, intra-document surprisal variance, rough edges (fragments, directive verbs), and subtractive removal of RLHF homogenization markers (stock vocab, hedging stacks, sycophancy, signposting). These are **style moves on the linguistic cue dimension** — not warmth, not agreement, not performative empathy.

**Never inject** = fake anthropomorphism. Sycophancy openers, hedging stacks, performative balance, knowledge-cutoff disclaimers, visible reasoning theater, empathy softeners, and "neutralize for safety" rewrites. Ibrahim (+7.43 pp avg error, +11–12 pp under false beliefs) and Xiao's capability–expectation misalignment both say: cues that promise warmth or competence the system doesn't have are the failure mode.

unslop's job is **calibrated α** (Xiao): lower misleading cognitive/behavioral cues, raise authentic linguistic register, preserve stance. Alignment tax (Liu) means this cannot be fixed by temperature or synonym swap — subtractive variance restoration plus optional cross-model regime change, not re-authoring.

---

## 1. The preserve/inject matrix

### 1.1 Always preserve (author signal)

| Cue class | Examples | Why preserve | Source |
|-----------|----------|--------------|--------|
| **Argumentative stance** | "X is wrong because…", "Use memo, not callback", directive fixes | Blandification neutralizes ~70% of for/against essays; detectors and readers lose author ownership | Abdulhai 2603.18161 (AGENT-44) |
| **Distinctive claims & metaphors** | Unusual analogies, strong opinions, non-centrist framing | LLM edits shift embeddings in a **common direction** even under "grammar only" | Abdulhai counterfactual (AGENT-44) |
| **Disagreement & refusals** | "That won't work", "No — the bug is elsewhere" | Warmth training +40% false-belief affirmation; stance ≠ style | Ibrahim 2507.21919 (AGENT-51) |
| **Calibrated epistemic uncertainty** | "I think", "probably", "seems", "in my experience" | Honest uncertainty is stance, not performative hedging — distinct from "It's important to note" | SKILL Principle #2; AGENT-51 §8.6 |
| **Concrete specifics** | Names, numbers, dates, project details, code references | Detectors struggle when text carries out-of-training specifics; blandification strips toward generality | AGENT-44 detection §; AGENT-46 HIP chain |
| **Uneven paragraph length** | Short punch paragraph after long block | Tidy five-paragraph shapes are RLHF/register homogenization | AGENT-44; Reinhart/Rallapalli via AGENT-46 |
| **Source voice (when present)** | Colloquialisms, author tics, rejection-profile patterns | Prompt-only voice reconstruction fails stylometric attribution; preserve beats reconstruct | AGENT-44 § balanced limits; AGENT-45 voice-match |
| **Idiosyncrasy & rough edges** | Fragments, starting with "And"/"But", non-template list structure | Homogenization compresses high-reward modes; rough edges exit chat centroid | AGENT-46 Layer 2–3; anti-detector SKILL |
| **Factual content integrity** | Claims, metrics, citations as written | Fluent wrongness > stiff accuracy; warmth edits correlate with error | Ibrahim (AGENT-51); Principle #3 |

**Rule of thumb:** If removing it makes the text more "balanced", "neutral", or "safe" without changing technical meaning — **do not remove it**. That is blandification.

### 1.2 Inject when absent (authentic human register)

| Cue class | Mechanism | Target | Mode gate |
|-----------|-----------|--------|-----------|
| **Sentence-length burstiness** | `structural.py` — mix 4–35 word sentences, break uniform RLHF shapes | Human σ ~8.2 vs GPT-4o ~4.1 (Paneru line) | balanced+ |
| **Contraction rate** | `soul.py` — lift toward ~0.17/chunk human baseline | Near-zero contractions in aligned chunks | balanced+ |
| **Intra-document surprisal variance** | `surprisal.py` DivEye proxies; structural pass | Counter alignment-tax low σ; DivEye/TSD signal | anti-detector / opt-in |
| **Lexical de-homogenization** | Stock vocab, copula avoidance, significance inflation removal | Reinhart-overrepresented RLHF items (tapestry, intricate, "serves as") | subtle+ |
| **Structural non-uniformity** | Bullet-soup merge, em-dash cap, break template lists | Turnitin anti-humanizer uniform-structure fingerprint | balanced+ |
| **Directive cadence** | Preserve or sharpen imperatives where source had them | Anti-blandification: "Wrap in useMemo" not "developers should consider" | balanced+ |
| **Cross-model dispersion** (optional) | Phase 3 S2 iterative paraphrase | Exit instruct statistical regime (HIP analog) | anti-detector explicit |

**Rule of thumb:** Inject **distribution shape**, not **personality**. Burstiness and contractions change how human the text *reads*; they do not change whether the text *agrees*.

### 1.3 Never inject (fake human cues)

| Cue class | Examples | Why forbidden | Source |
|-----------|----------|---------------|--------|
| **Sycophancy openers** | "Great question!", "I'd be happy to help", "Certainly!" | +7–12 pp error under interpersonal context; paraphrase keeps stance | Ibrahim; AGENT-45 sycophancy rules |
| **Performative empathy** | "I'm so sorry you feel that way", "You're absolutely right to feel…" | Sadness + false belief = +11.9 pp reliability gap | Ibrahim Fig. 3 (AGENT-51) |
| **Hedging stacks** | "It's important to note", "Generally speaking", "At its core" | Fake cognitive uncertainty; alignment homogenization marker | AGENT-45 cognitive ↓; AGENT-46 Layer 2 |
| **Performative balance** | "On the one hand… on the other", both-sidesism on settled points | Blandification mechanism; stance flattening | AGENT-44; performative rules |
| **Signposting / meta-narration** | "Let me explain", "In this section", "There are several factors" | Behavioral fake proactivity; essay-register homogenization | AGENT-45 behavioral ↓ |
| **Knowledge-cutoff scripts** | "As of my last training" | Assistant behavioral cue; wrong register for human prose | AGENT-45 |
| **Visible reasoning theater** | `<thinking>`, "## Reasoning", "Let me think step by step" | High cognitive α without competence; breaks public register | AGENT-45 `--strip-reasoning` |
| **Added warmth / soul tier** | Empathy phrases, inclusive "we", validation without grounding | Warmth optimization causally degrades reliability | Ibrahim cold control (AGENT-51) |
| **Stance softening for "humanity"** | "There are several perspectives to consider" replacing "X is wrong" | Abdulhai semantic basin; ESL false-positive adjacency | AGENT-44, AGENT-46 anti-patterns |
| **Synonym-only paraphrase** | Thesaurus swap preserving homogenized structure | Stays in predictability cone + SCR cluster | AGENT-46 anti-patterns |

**Rule of thumb:** If the edit **adds** pleasantries, agreement pressure, or simulated competence — reject. Subtract (Principle #1).

---

## 2. Four-cue framework mapping (Xiao et al.)

AGENT-45 maps unslop passes to perceptual / linguistic / behavioral / cognitive dimensions. SYNTH-91 adds the **preserve vs inject** verdict per dimension.

| Cue dimension | Preserve | Inject (authentic) | Strip (fake) | unslop coverage |
|---------------|----------|-------------------|--------------|-----------------|
| **Perceptual** | N/A (text tool) | N/A | N/A | Out of scope |
| **Linguistic** | Author register, tics, rejection patterns | Burstiness, contractions, concrete nouns | Stock vocab, copula avoidance, em-dash pileups | ~85% — core product |
| **Behavioral** | Directiveness, turn-appropriate brevity | None (subtractive only) | Sycophancy, signposting, knowledge-cutoff, vague attribution | ~30% |
| **Cognitive** | Real uncertainty, factual claims, refusals | None | Hedging openers, reasoning theater, performative balance | ~40% |

**Calibrated α profile by mode:**

| Mode | Fake α (strip) | Authentic linguistic α (inject) | Stance preservation |
|------|----------------|-----------------------------------|---------------------|
| subtle | Low | Minimal | Maximum |
| balanced | Medium | Medium (structural + soul) | **Primary** — ANTI-BLANDIFICATION |
| full | High | High | Guarded — higher rewrite surface |
| voice-match | Match user sample | Per stylometry targets | Explicit in prompt |
| anti-detector | High | High (variance restoration) | **Load-bearing** — no neutralization trade |

---

## 3. Alignment tax lens — homogenization vs human cues

AGENT-46 reframes preserve/inject as **exit vs remain in the instruct cluster**:

### 3.1 RLHF homogenization markers (strip = inject negative space)

These are not "AI-isms" in the marketing sense — they are **shared post-training fingerprints**:

- Zero/near-zero contraction rate
- Low sentence-length coefficient of variation
- Noun-heavy nominalizations (Reinhart 2.1× GPT-4o vs human)
- Analytical LIWC elevation + stance neutralization (Abdulhai)
- Stock collocations (tapestry, intricate, pivotal, seamless)
- Uniform bullet syntax and template paragraph shapes
- Late-stage surprisal stabilization (TSD — homogenization is temporal)

Stripping these **does not** blandify if stance and specifics stay intact.

### 3.2 Human dispersion targets (inject = move away from chat centroid)

| Signal | Human-ish target | unslop pass |
|--------|------------------|-------------|
| Sentence-length CV | Higher σ, mixed 4–35 words | `structural.py` |
| Contraction rate | ~0.17/chunk (human baseline) | `soul.py` |
| Intra-doc surprisal σ | DivEye proxy ↑ when measured low | `surprisal.py` |
| Stance variance | Preserve strong claims | ANTI-BLANDIFICATION block |
| Cross-family fingerprint | Different post-training artifact | Cross-model S2 (anti-detector) |

### 3.3 What temperature and synonym swap cannot do

Liu Exp. 15: SCR persists at T=0.3–1.5. Rallapalli: prompting/decoding weaker than model+genre. **Do not document decoding as primary humanization.** unslop's inject layer is deterministic variance restoration, not sampling tricks.

---

## 4. Warmth–reliability lens — style vs stance

AGENT-51 is the empirical license for Principles #1–#3:

```
Style moves (safe to inject):
  burstiness, contractions, uneven paragraphs, concrete nouns,
  em-dash cap, stock-vocab removal

Stance holds (always preserve):
  disagreement, refusals, calibrated "I think/probably",
  factual claims, corrections of false premises

Never conflate:
  "humanize" ≠ "agree more"
  "warm rhythm" ≠ "empathy phrases"
  "anti-detector" ≠ "likability optimization"
```

**Ibrahim-informed test for any new feature:** Does it add or subtract? Does it move stance? Would it survive sadness + false belief? Cold-control preference: if a colder edit preserves meaning with lower agreement pressure, prefer cold.

---

## 5. Blandification failure modes — preserve/inject misclassification

Common errors when preserve/inject boundaries blur:

| Misclassification | What happens | Fix |
|-----------------|--------------|-----|
| **Inject warmth instead of burstiness** | +7–12 pp error path; sycophancy persists | Strip sycophancy; engineer cadence only |
| **Preserve hedging stacks as "author voice"** | Fake uncertainty stays; homogenization marker remains | Strip performative hedges; keep honest "I think" |
| **Inject neutrality as "human balance"** | Abdulhai 70% stance loss; ESL/detector adjacency | ANTI-BLANDIFICATION audit pass |
| **Preserve uniform structure as "clarity"** | Turnitin/DivEye second-order fingerprint | structural.py merge + variance |
| **Inject synonym paraphrase as anti-detector** | Stays in predictability cone (AGENT-46) | Cross-model + subtractive ladder |
| **Strip rough edges as "slop"** | Voice destruction; idiolect loss | Preserve fragments, directives, metaphors |

---

## 6. Mode-specific preserve/inject doctrine

### balanced (default)

- **Preserve:** stance, metaphors, opinions, fragments, uneven paragraphs, all factual content
- **Inject:** burstiness, contractions, concrete directive cadence where source supports it
- **Strip:** full sycophancy/hedging/performative/stock-vocab set
- **Guard:** ANTI-BLANDIFICATION two-pass audit in LLM path

### anti-detector

- **Preserve:** stance + idiosyncrasy (same as balanced — neutralization trades detection for blandification)
- **Inject:** variance restoration — structural, soul, surprisal nudge, optional cross-model S2
- **Strip:** all balanced strips + lexical_targets gap closure vs human baselines
- **Never inject:** warmth, empathy, agreement softeners "to sound human"

### voice-match

- **Preserve:** user rejection profile (what they'd never write) > preference list
- **Inject:** stylometric targets from sample (cadence, contractions, register) — not invented bio
- **Strip:** slop that contradicts sample; do not reconstruct missing idiolect from corpus mean

### subtle

- **Preserve:** almost everything except stock vocab
- **Inject:** minimal — insufficient for sycophancy/hedging (escalate to balanced)

---

## 7. Validator and product implications

### 7.1 New residual checks (recommended)

Flag post-humanize:

1. **Stance softening** — hedge insertion, "perspectives to consider" replacing direct claims
2. **Warmth injection** — new empathy/sycophancy phrases not in source
3. **Neutralization** — sentiment/stance shift toward non-committal (Abdulhai axis)
4. **Homogenization** — sentence-length CV drop, contraction rate unchanged near zero
5. **Second-order smoothness** — uniform bullets, low surprisal σ after anti-detector pass

### 7.2 Documentation citations

| Claim | Cite |
|-------|------|
| ~70% stance neutralization | Abdulhai arXiv:2603.18161 |
| Alignment collapses diversity; decoding won't fix | Liu arXiv:2603.24124 |
| Warmth +11pp / +12.1pp error under false beliefs | Ibrahim arXiv:2507.21919 / Nature 2026 |
| Calibrated anthropomorphism α | Xiao et al. EMNLP 2025 arXiv:2508.17573 |

### 7.3 Default policy

**Default balanced, not anti-detector.** Evasion modes increase smoothness pressure; blandification and detectability rise together (AGENT-44). Prefer deterministic subtractive pass first on sensitive docs — lower semantic drift risk (Abdulhai grammar-only finding).

---

## 8. Quick reference card

### Preserve (author signal)
- Stance, opinions, disagreement, refusals
- Unusual metaphors, distinctive claims
- Calibrated uncertainty ("I think", "probably")
- Concrete names, numbers, code, specifics
- Uneven paragraphs, fragments, directives
- Source voice tics and rejection patterns

### Inject (authentic register)
- Sentence-length burstiness
- Contraction rate toward human baseline
- Surprisal variance (when measured low)
- Structural non-uniformity
- Lexical de-homogenization (subtract RLHF markers)
- Cross-model dispersion (anti-detector only, explicit)

### Never inject (fake human)
- Sycophancy, performative empathy
- Hedging stacks, performative balance
- Signposting, knowledge-cutoff scripts
- Reasoning theater, added warmth
- Stance softening, synonym-only paraphrase
- "Neutralize for safety" rewrites

---

## 9. Source memos

| Memo | Path | Core contribution to SYNTH-91 |
|------|------|-------------------------------|
| AGENT-44 | `AGENT-44-BLANDIFICATION-NEUTRALIZATION.md` | Preserve stance/voice; blandification = detectable homogenization |
| AGENT-45 | `AGENT-45-HUMANIZING-MACHINES-FOUR-CUE.md` | Four-cue preserve/strip/inject mapping; calibrated α |
| AGENT-46 | `AGENT-46-ALIGNMENT-TAX-HOMOGENIZATION.md` | Variance restoration inject layer; homogenization markers to strip |
| AGENT-51 | `AGENT-51-IBRAHIM-WARMTH-RELIABILITY.md` | Style ≠ stance; subtract don't add; never inject warmth |

---

## Bottom line

Human writing cues split cleanly:

**Preserve** = what the author meant and how they argued it.  
**Inject** = statistical shape of human prose (variance, contractions, de-homogenized lexicon).  
**Never inject** = RLHF warmth theater that Ibrahim proved costs reliability.

unslop is not a humanizer in the commercial sense (add empathy, neutralize voice, synonym swap). It is a **stance-preserving de-homogenizer**: strip alignment-tax residue, restore linguistic dispersion, keep the argument sharp. That is the intersection of Abdulhai (don't blandify), Liu (don't re-homogenize), Xiao (calibrate α), and Ibrahim (don't add warmth).

---

*SYNTH-91 complete. Cross-refs: SYNTH-81 (detection signals), AGENT-22-HIP (regime change), `skills/unslop/SKILL.md` Principles #1–#5, `unslop/scripts/humanize.py` ANTI-BLANDIFICATION block.*
