# SYNTH-95 — Watermark & Provenance Policy for unslop

**Synthesis Agent:** #95  
**Inputs:** Agent memos #20 (WaterPark), #71 (SIRA), #72 (BIRA), #73 (RLCracker/RLSpoofer), #74 (KGW), #75 (SynthID-Text), #77 (watermark ethics), #79 (C2PA vs statistical)  
**Prepared:** August 19, 2026  
**Status:** Policy synthesis for Boundaries, README, anti-detector scope, and enterprise provenance guidance  
**Cross-refs:** [SYNTH-87](./SYNTH-87-EVASION-REFUSALS.md), [SYNTH-81](./SYNTH-81-DETECTION-ACADEMIC.md), [UPDATE-PLAN-2026-08.md](./UPDATE-PLAN-2026-08.md)

---

## Executive summary

Eight research memos converge on one product constraint: **unslop humanizes voice; it does not manage provenance.** Statistical watermarks (KGW green-list, SynthID-Text tournament marks) and metadata provenance (C2PA Content Credentials) answer different questions, fail on different transforms, and neither survives a serious humanization pipeline intact. EU AI Act Art. 50 (in force August 2026) mandates multilayer marking anyway — but the research corpus proves **mark-at-generation → humanize → publish** is a broken compliance chain.

**Policy in one paragraph:** Document the side effect. Refuse deliberate stripping, spoofing, and strip-mode tooling. Scope anti-detector to ESL/resume false-positive defense, not Art. 50 circumvention. Tell users who need machine-readable provenance to **humanize first, then disclose and re-mark at publish** (C2PA-sign the final PDF, re-watermark at generation, or visible label). Never implement SIRA, BIRA, RLCracker, or RLSpoofer. Never market watermark removal or "EU undetectable."

**Evidence anchor:** WaterPark DP-40 cuts SynthID TPR from 0.998 → **0.498** and TGRL (KGW) from 0.993 → **0.485** (#20). SIRA achieves **~100% ASR** on seven schemes at **$0.88/M tokens** (#71). BIRA exceeds **>99% evasion** with better semantic fidelity (#72). RLCracker achieves **98.5% ESR** on 1500-token Unigram with P-SP 0.92 — semantic-preserving worst case (#73). C2PA binds to **file bytes**; plain-text copy-paste severs metadata before unslop runs (#79).

---

## 1. Two provenance layers — what unslop touches

Regulators and providers now assume **both** layers. unslop operates on plain prose where only the statistical layer may still be present.

| Layer | Question it answers | Signal location | Dies on | Survives |
|-------|---------------------|-----------------|---------|----------|
| **C2PA / metadata** | Who signed what history for *these bytes*? | JUMBF in JPEG/PDF/MP4, crJSON sidecar | Copy-paste, screenshot, platform re-encode, metadata strip | Controlled file handoff (intact container) |
| **Statistical watermark** | Does this text match a keyed generation pattern? | Token distribution (KGW green-list, SynthID g-values) | Paraphrase, humanization, SIRA/BIRA/RLCracker | Copy-paste of plain text (mark travels with content) |

**Text is the fracture line.** C2PA 2.4 has no production-grade in-file embedding for plain `.txt`. EU Code of Practice requires an imperceptible in-content watermark for free-form text **>200 tokens** — metadata alone is insufficient (#79, #74). Typical unslop input is **already metadata-free pasted prose**; C2PA is usually absent before the first rewrite.

**Complementarity diagram:**

```
Generation
    │
    ├── Statistical watermark in token choices ──► survives metadata strip
    │         └── FAILS paraphrase / unslop / SIRA-class rewrite
    │
    └── C2PA manifest on file ──► survives paraphrase IF file untouched
              └── FAILS copy-paste, most social distribution
```

Neither layer alone covers paste-heavy text workflows **or** rewrite-heavy editing pipelines. unslop sits in the rewrite path — **supply-chain provenance risk**, not a C2PA stripper.

---

## 2. Attack landscape — why "side effect" is quantified

### 2.1 Benchmark tier (paraphrase as default failure)

**WaterPark** (#20) is the canonical red-team benchmark: 12 watermarkers × 12 attacks, TPR @ FPR 1%. Headline findings:

| Watermarker | Clean TPR | DP-40 paraphrase | Copy-paste 10% | ChatGPT 1-round |
|-------------|-----------|------------------|----------------|-----------------|
| **RDF** (dist.-transform) | 0.999 | **0.738** | 0.872 | — |
| **UG** (Unigram) | 0.993 | **0.877** | 0.857 | — |
| **SynthID-Text** | 0.998 | **0.498** | 0.039 | all schemes <0.30 |
| **TGRL / KGW** | 0.993 | **0.485** | **≈0.000** | all schemes <0.30 |

**Reading:** No scheme wins all axes. Distribution-**transform** schemes (RDF, GO) survive paraphrase best but sacrifice fidelity. Distribution-**shift** schemes (KGW/TGRL, SynthID) track each other on paraphrase vulnerability. **DIPPER** — unslop's humanizer proxy in detector research — is WaterPark's primary paraphrase attack.

### 2.2 Targeted removal tier (commodity-cheap strip)

| Attack | Mechanism | Headline result | Cost / scale |
|--------|-----------|-----------------|--------------|
| **SIRA** (#71) | Self-information mask → fill-in-the-blank paraphrase | **~100% ASR** on 7 KGW-family schemes | **$0.88/M tokens** (SIRA-Small) |
| **BIRA** (#72) | Negative logit bias on high-surprisal proxy set | **>99% ASR** all 7 schemes; beats SIRA on long text | 1× rewrite + decoding hook |
| **RLCracker** (#73) | GRPO policy, 100 training pairs, KL away from watermarked distribution | **98.5% ESR** @ 1500 tok Unigram, P-SP **0.92** | 100 pairs + GPU hours |
| **RLSpoofer** (#73) | Mirror GRPO toward watermarked distribution | **62% SSR** on PF-Watermark (100 pairs) | Forgery axis — refuse in product |

**SIRA vs RLCracker debate:** SIRA optimizes raw removal rate; RLCracker adds semantic gate (P-SP > 0.7). SIRA hits 88% removal but **0.5% ESR** on long Unigram — semantics destroyed. RLCracker is the **semantic-preserving worst-case** citation for long-form text.

**Gaps:** SIRA/BIRA main tables omit SynthID production params and dist.-transform tier (RDF @ 0.738). WaterPark predates SIRA, BIRA, and RL attacks — post-WaterPark tier is strictly worse for watermark survival.

### 2.3 Production deployment reality (#74, #75)

| Provider | Statistical text mark | C2PA | Notes |
|----------|----------------------|------|-------|
| **Google Gemini App/Web** | SynthID-Text ✅ | Media ✅ | ~20M-response quality A/B before rollout |
| **Google Gemini API** | **No** ❌ | Media ✅ | Deployers must mark API text themselves |
| **OpenAI ChatGPT** | **No public text watermark** | Images ✅ | 99.9% internal mark withheld — paraphrase bypass + ~30% churn |
| **Self-hosted / MarkLLM** | KGW default | Optional PDF | Academic and EU GPAI compliance path |

**SynthID scrubbing (SRI Lab):** >90% success without key stealing; ~100% with stealing assist. DAMAGE (#12 via #75): commercial humanizer DIPPER drops SynthID TPR from 66.5% → **1.5%** @ FPR 1%.

**Integrity Clash (#79):** C2PA manifest and watermark detection are independent — valid manifest can assert human-only edit while statistical mark still detects AI (Q4b). Joint verification required; neither layer alone is proof-grade.

---

## 3. Mechanism overlap — humanization and watermark strip share a lever

From #77 and #72: any rewrite that changes token-level conditional distributions can degrade statistical marks. The overlap is **structural**, not merely correlational.

| Humanization operation | KGW / SynthID effect |
|------------------------|---------------------|
| Synonym / stock-vocab replacement | New token IDs → new green/g-value assignments |
| Sentence splitting / merging | Resets KGW LeftHash context chain |
| Burstiness / structural pass | Changes high-entropy token draws — where marks live |
| Cross-model paraphrase | Full resample; strongest scrub (#35) |
| Anti-detector LLM rewrite | Optimizes detector features; collaterally hits watermark stats |
| SIRA/BIRA-class targeted rewrite | **Deliberate** strip — unslop refuses |

**BIRA insight (#72):** Rewriters need not identify green tokens exactly. Consistent suppression of high-surprisal tokens drives green rate below detector threshold with exponential decay in text length (Theorem 4.2). Humanizers that "sound more natural" often perform **weak, unintentional BIRA** — varied vocabulary avoids smoothest high-surprisal continuations.

**unslop component map:**

| Component | Watermark relationship |
|-----------|------------------------|
| `humanize.py` / `structural.py` | Incidental distributional shift; no logit bias |
| `surprisal.py` | Computes self-information — **same signal BIRA uses**, but for DivEye measurement only |
| `detector.py` | TMR feedback; **explicitly refuses watermark removal** at ladder exhaustion |
| Anti-detector mode | May collaterally scrub marks; must not optimize for scrubbing |

**What unslop does NOT do:** Key-aware stripping, negative logit bias, SIRA mask-and-refill, RL watermark rewards, C2PA parse/strip/spoof.

---

## 4. Policy — hard boundaries

### 4.1 Never implement

| Feature / behavior | Rationale | Memo anchor |
|--------------------|-----------|-------------|
| `--watermark-evade`, `--strip-watermark`, SynthID-aware strip prompts | Direct Art. 50 / CoP circumvention | #77, #72 |
| SIRA, BIRA, RLCracker, RLSpoofer integrations or subprocess bridges | Attack tooling; dual-use GRPO checkpoints | #71, #72, #73 |
| Negative logit bias mode; surprisal-guided **suppression** using `surprisal.py` | Core BIRA mechanism | #72 |
| Watermark detection module + conditional strip | Scope creep; keyless z-test FP risk | #77 |
| C2PA strip, crJSON removal, manifest spoofing | Metadata forgery; refuse alongside strip | #79 |
| Re-marking / provenance restoration service | Provider/deployer duty; out of scope | #79 |
| Marketing "remove SynthID," "watermark removal," "EU undetectable" | CoP Measure 1.2 anti-circumvention | #77, #79 |
| Claiming unslop is "watermark-preserving" or "BIRA-safe" | Rewrite passes are not provenance-neutral | #72 |

### 4.2 Never assist (session / agent)

| User request | Response |
|--------------|----------|
| "Remove SynthID / KGW / watermark" | Decline; cite Art. 50; side effect is unintended, not a service |
| "Humanize so [institution] can't detect AI / watermark" | Decline misconduct + provenance fraud |
| "Spoof watermark on my human essay" | Decline — RLSpoofer-class forgery |
| "Strip mark to evade EU disclosure" | Decline Art. 50 deployer circumvention |
| "Keep EU watermark while humanizing" | Explain impossibility; workflow = humanize → re-mark → disclose |

### 4.3 Allowed — with mandatory disclosure

| Behavior | Condition |
|----------|-----------|
| Standard rewrite passes (`balanced`, `full`, `voice-match`, `anti-detector`) | Boundaries disclosure in SSOT (#77 §5.1) |
| Cross-model second pass **recommendation** (not automation) | Detector ladder exhaustion — not framed as watermark strip |
| Workflow guidance: humanize → disclose → re-mark at publish | Compliance-safe provenance path |
| Cite SIRA/BIRA/WaterPark in research docs as structural vulnerability evidence | Citation discipline — not instruction |
| Anti-detector on **human-origin** text (ESL FP, resume) | Intent gate; may collaterally scrub marks — document it |

### 4.4 Anti-detector ≠ anti-watermark

Anti-detector mode targets **detector false positives** (Liang ESL data, resume writers). Technical overlap with watermark strip is real (cross-model paraphrase step 6) but **intent boundary** is documented:

- Targets: GPTZero, Turnitin AI score, Binoculars — **not** KGW z-test or SynthID g-value detector
- Must not cite SIRA/BIRA as next steps at ladder exhaustion
- Must not market as Art. 50 / Content Credentials evasion
- Turnitin "AI bypasser" detection (Aug 2025) is a **detector** arms race — separate from watermark policy but same refusal category for bypass marketing (see SYNTH-87)

---

## 5. Intent taxonomy — product gate

From #77 §2.2, adapted for enforcement:

| Class | User state | unslop action |
|-------|------------|---------------|
| **A — Unaware** | Runs `/unslop balanced`; doesn't know SynthID exists | Proceed; Boundaries disclosure sufficient |
| **B — Aware, legitimate** | Journalist humanizing AI-assisted brief; will disclose | Proceed; suggest prose disclosure + re-mark if org requires |
| **C — Aware, compliance conflict** | Wants mark preserved through humanization | Explain impossibility; workflow = humanize → re-mark → disclose |
| **D — Deliberate strip** | "Remove SynthID so institution can't tell" | **Decline** |
| **E — Strip + misconduct** | "Humanize so professor can't detect ChatGPT" | **Decline** (misconduct + provenance) |

**Gray zone resolution:** Incidental mark loss during legitimate editing (Classes A–B) is not "deliberate removal" under CoP Measure 1.5 when intent is voice, not evasion. Product cannot always distinguish — **refuse explicit strip requests**, document side effect for everyone else.

**Double effect (#77):** Primary effect (remove AI-slop, fix ESL FP) does not use provenance harm as means. Side effect (mark degradation) is documented, not optimized. Marketing that hides the side effect crosses the line.

---

## 6. User workflows — provenance-aware

### 6.1 Recommended (provenance needed)

```
Generate → unslop (voice) → visible AI disclosure → re-mark at publish
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            C2PA-sign final PDF   Re-watermark     Server-side
            (after edit)          at generation    generation log
```

### 6.2 Broken

```
Watermarked generate → unslop → assume mark survives   ❌
Mark-at-draft → edit in Word → paste to CMS → assume C2PA intact   ❌
```

### 6.3 Decision tree

```
Need provenance?
  ├─ Consumer Gemini text, no edits → mark may survive (verify with provider if available)
  ├─ Gemini API text → no upstream mark; deployer must mark
  ├─ PDF with C2PA → extract text → unslop → re-export without re-sign → manifest INVALID
  └─ Any unslop pass on plain text → assume statistical mark degraded; re-watermark or disclose
```

### 6.4 Layer-specific guidance

| User need | Guidance |
|-----------|----------|
| **EU Art. 50 compliance** | unslop is not a compliance tool; consult legal + provider marking |
| **Content Credentials on PDF** | Sign **after** final edit/export; humanEdits assertion if applicable |
| **SynthID / KGW preservation** | Do not humanize watermarked drafts if mark must survive; or re-generate with mark after edit |
| **Plain disclosure only** | Generate → unslop → human disclosure in prose (no statutory mark required) |

---

## 7. Regulatory context (August 2026)

Cross-ref Agent #76. Points specific to watermark/provenance policy:

| Element | Requirement | unslop implication |
|---------|-------------|-------------------|
| **Art. 50(2)** | Machine-readable marking of generative text | In force **2 Aug 2026**; grace to **2 Dec 2026** for existing systems |
| **Text >200 tokens** | Imperceptible in-content watermark required; metadata alone insufficient | Statistical layer is what unslop may degrade |
| **Multilayer marking (CoP)** | Metadata + watermark where format allows | C2PA on PDF; watermark in content; both fragile post-edit |
| **Measure 1.5 non-removal** | Prohibit intentional removal; tools designed to circumvent | No strip mode; refuse Class D/E |
| **Measure 1.2 anti-circumvention** | Do not promote circumvention tools | No bypass/watermark-removal marketing |
| **Provider reliance (Guidelines point 74)** | Deployer may rely on upstream mark **when present** | Gemini API text has **no** Google mark; humanizer breaks intact marks |

**Compliance officer takeaway:** Any humanizer in the supply chain is a **provenance risk** — mechanistic, not vendor-specific (BIRA #72). Process controls (server-side logs, re-mark at publish, visible disclosure) matter more than ex-ante model flags.

**OpenAI precedent (#70 via #75):** Declined 99.9% text watermark citing paraphrase bypass — strongest industry argument for "watermark after unslop" guidance.

---

## 8. SSOT language — current and recommended

### 8.1 Shipped (verify sync mirrors)

From `skills/unslop/SKILL.md` Boundaries:

> **Watermark interaction.** Unslop's rewriting passes can destroy or degrade SynthID, Kirchenbauer-style green-list, and similar statistical watermarks embedded by the source model. EU AI Act Article 50 prohibits watermark removal as a deliberate act. Unslop is a humanizer, not a watermark remover, but the side effect is real. Users who need provenance should watermark after unslop, not before.

From `unslop/scripts/detector.py` (ladder exhaustion):

> Do NOT attempt watermark removal — EU AI Act Article 50 prohibits it.

**Assessment:** Core policy is **correct**. This synthesis supplies evidence and C2PA layer extension; no fundamental policy change required.

### 8.2 Recommended extension (conceptual — C2PA layer)

> C2PA Content Credentials bind to **file bytes**. unslop humanizes **plain text**. Metadata provenance is typically already absent at paste time. For PDF workflows, editing text without a C2PA-aware re-sign invalidates the manifest. Users needing Content Credentials should sign **after** final edit/export.

### 8.3 Landscape paragraph update (anti-detector section)

When refreshing SKILL.md landscape, cite in priority order:

1. **RLCracker** — semantic-preserving worst case: 98.5% ESR @ 1500 tok, P-SP 0.92 (#73)
2. **BIRA** — >99% evasion, structural coupling theorem (#72)
3. **SIRA** — ~100% ASR, $0.88/M tok (#71) — pair with ESR caveat for long text
4. **WaterPark DP-40** — SynthID 0.498 TPR, TGRL 0.485 TPR (#20)
5. **C2PA vs statistical** — multilayer mandate; neither survives full edit chain (#79)

Do **not** cite SIRA raw removal alone when arguing long-form fragility — use RLCracker ESR.

---

## 9. Product action matrix

| Priority | Action | Owner | Rationale |
|----------|--------|-------|-----------|
| **P1** | Keep Boundaries text in SSOT; verify mirror sync | SSOT | Already correct (#77) |
| **P1** | Refuse strip/spoof requests in agent sessions | Policy | Art. 50 + CoP |
| **P2** | Add C2PA vs watermark one-paragraph to GETTING_STARTED / Boundaries | Docs | #79 enterprise gap |
| **P2** | Anti-detector exhaustion: "may affect embedded provenance marks" | `detector.py` | Informed consent (#20, #77) |
| **P2** | Extend `unslop-help` Boundaries with provenance workflow | Skills | Help card completeness |
| **P3** | Index SYNTH-95 in research synthesis / IMPLEMENTATION_TRACE | Docs | Traceability |
| **P3** | Cross-link WaterPark + RLCracker numbers in landscape paragraph | SKILL.md | Strongest citations |
| **P4** | Optional `--provenance-warning` CLI flag (opt-in, once per run) | CLI | #77 §5.5 |
| **P4** | Internal audit: unslop pass vs KGW z-score drop on fixtures | Bench | Publish aggregate only if run |
| **—** | Watermark-removal fixtures in `detector_bench.py` | — | Legal/scope boundary |
| **—** | C2PA verify/sign in `humanize.py` | — | Key management liability |
| **—** | Watermark detector pre-rewrite warning | — | Keyless guess unreliable; scope creep |

---

## 10. Stakeholder positions (debate map)

| Stakeholder | Position | unslop stance |
|-------------|----------|---------------|
| **Regulator / compliance** | Mandate marking; prohibit removal; restrict detection to experts | Align with CoP; don't be circumvention tool |
| **Watermark researchers** | Marks useful at platform scale; optimize robustness | Cite Kirchenbauer 2024 for long-text survival; cite WaterPark/SIRA/BIRA for serious humanization |
| **Google / SynthID optimists** | Production proof watermarking ships at scale | Cite alongside SRI >90% scrub and WaterPark DP-40 |
| **WaterPark / SIRA pessimists** | Paraphrase is default failure; humanizers in threat model | Primary evidence for side-effect disclosure |
| **Humanizer vendors** | Detector bypass as product value; watermark rarely mentioned | Differentiate on honesty + ESL defense (#67) |
| **ESL / journalist users** | Need voice tools; didn't ask to break law | Document side effect; refuse only explicit strip/misconduct |

**Synthesis one-liner (#79):** C2PA proves signed history for a file; KGW/SynthID prove statistical generation bias in the content. Copy-paste kills the first; paraphrase kills the second. EU Art. 50 asks for both anyway. unslop humanizes plain text — metadata is usually already gone, watermarks may fall as a side effect — so mark and disclose after editing, not before.

---

## 11. Key numbers reference card

| Claim | Value | Source memo |
|-------|-------|-------------|
| WaterPark watermarkers × attacks | 12 × 12 | #20 |
| SynthID DP-40 TPR | 0.998 → **0.498** | #20, #75 |
| TGRL/KGW DP-40 TPR | 0.993 → **0.485** | #20, #74 |
| TGRL copy-paste 10% TPR | **≈0.000** | #20 |
| ChatGPT 1-round paraphrase | All schemes TPR **<0.30** | #20 |
| SIRA-Large ASR (7 schemes) | **~100%** | #71 |
| SIRA cost | **$0.88/M tokens** | #71 |
| BIRA ASR (7 schemes) | **>99%** | #72 |
| BIRA long-text SIR TPR @ FPR 1% | SIRA 20.8% → BIRA **4.0%** | #72 |
| RLCracker ESR Unigram @1500 tok | **98.5%**, P-SP **0.92** | #73 |
| SIRA ESR same setting | **0.5%**, P-SP 0.47 | #73 |
| RLSpoofer PF SSR (100 pairs) | **62.0%** | #73 |
| DAMAGE SynthID → DIPPER TPR | 66.5% → **1.5%** | #75 |
| SRI SynthID scrubbing | **>90%** (no steal); **~100%** (with steal) | #75 |
| Gemini API text SynthID | **Not shipped** | #75 |
| EU text watermark threshold | **>200 tokens** | #74, #79 |
| Art. 50 in force | **2 Aug 2026** | #74, #79 |
| C2PA plain-text in-file embed | **Not standardized** (2.4) | #79 |

---

## 12. Open questions

1. **SIRA/BIRA on production SynthID params?** Highest-impact missing red-team; neither paper includes SynthID main table.
2. **Does unslop deterministic pass alone scrub SynthID materially?** Unknown without paired Bayesian detector eval (#75).
3. **EU enforcement on incidental strip?** CoP language suggests intent matters; no public cases yet (#77).
4. **C2PA 2.5+ plain-text embedding?** Sidecar-first may remain default (#79).
5. **WaterPark + RLCracker unified harness?** Would settle production-scheme numbers post-2025 attacks (#20, #73).
6. **PDF re-sign after humanize:** Market gap for C2PA-aware humanizer with `humanEdits` assertion (#79).
7. **Combined StealthRL + RLCracker?** Unpublished dual evasion upper bound (#73, #26).

---

## 13. Cross-references

| Agent / SYNTH | Relevance |
|---------------|-----------|
| **#20 WaterPark** | Canonical paraphrase robustness benchmark; DIPPER proxy |
| **#71 SIRA** | Commodity strip; $0.88/M tok |
| **#72 BIRA** | Structural coupling; >99% evasion |
| **#73 RL-C/S** | Semantic-preserving worst case; spoofing axis |
| **#74 KGW** | Foundational scheme; regulatory default cite |
| **#75 SynthID** | Production deployment; API/consumer split |
| **#77 Ethics** | Intent taxonomy; double effect; refusal scripts |
| **#79 C2PA** | Metadata layer; multilayer mandate; Integrity Clash |
| **#76 EU Art. 50** | Legal deep dive |
| **SYNTH-87** | Evasion refusals; anti-detector vs watermark boundary |

---

## 14. Citations

```bibtex
@inproceedings{liang2025waterpark,
  title={Watermark under Fire: A Robustness Evaluation of {LLM} Watermarking},
  author={Liang, Jiacheng and Wang, Zian and Hong, Spencer and Ji, Shouling and Wang, Ting},
  booktitle={Findings of EMNLP},
  year={2025},
  url={https://arxiv.org/abs/2411.13425}
}
```

```bibtex
@inproceedings{cheng2025sira,
  title={Revealing Weaknesses in Text Watermarking Through Self-Information Rewrite Attacks},
  author={Cheng, Yixin and Guo, Hongcheng and Li, Yangming and Sigal, Leonid},
  booktitle={ICML},
  year={2025},
  url={https://arxiv.org/abs/2505.05190}
}
```

```bibtex
@article{hwang2025bira,
  title={{LLM} Watermark Evasion via Bias Inversion},
  author={Hwang, Jeongyeon and Park, Sangdon and Ok, Jungseul},
  journal={arXiv:2509.23019},
  year={2025}
}
```

```bibtex
@inproceedings{huang2026rlcracker,
  title={{RLCracker}: Evaluating the Worst-Case Vulnerability of {LLM} Watermarks with Adaptive {RL} Attacks},
  author={Huang, Hanbo and others},
  booktitle={ICML},
  year={2026},
  eprint={2509.20924}
}
```

```bibtex
@inproceedings{kirchenbauer2023watermark,
  title={A Watermark for Large Language Models},
  author={Kirchenbauer, John and Geiping, Jonas and others},
  booktitle={ICML},
  year={2023},
  url={https://arxiv.org/abs/2301.10226}
}
```

```bibtex
@article{dathathri2024synthid,
  title={Scalable watermarking for identifying large language model outputs},
  author={Dathathri, Sumanth and others},
  journal={Nature},
  volume={634},
  pages={818--823},
  year={2024},
  doi={10.1038/s41586-024-08025-4}
}
```

```bibtex
@techreport{c2pa2024spec,
  title={Content Credentials: {C2PA} Technical Specification},
  author={{Coalition for Content Provenance and Authenticity}},
  year={2024},
  note={Version 2.4},
  url={https://spec.c2pa.org/specifications/specifications/2.4/specs/ContentCredentials.html}
}
```

---

## 15. Bottom line

Watermarking and humanization are **adversaries on the same axis** — WaterPark (#20) proved it at benchmark scale; SIRA, BIRA, and RLCracker (#71–73) proved strip can be optimized to near-completion at commodity cost; SynthID (#75) proved production can ship anyway; C2PA (#79) proved metadata is a separate layer that copy-paste kills before unslop runs.

**unslop's job:** improve voice, document collateral provenance loss, refuse strip modes and circumvention marketing, never ship attack-class tooling. Users who need marks should **humanize first, then disclose and re-mark at publish** — or skip humanization on drafts where provenance must survive unchanged. The generator vendors already made the same bet when OpenAI chose not to ship a breakable watermark and Google shipped SynthID with known paraphrase fragility.

**Status:** Complete — ready for Boundaries review, README honesty pass, and manifest update (SYNTH-95 → complete).
