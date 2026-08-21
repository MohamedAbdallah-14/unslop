# Agent #77 — Watermark Side Effect of Humanization (Ethics)

**Topic:** When humanization strips watermarks — ethical framing, academic evidence, industry/regulatory guidance, and unslop policy  
**Prepared:** 2026-08-19  
**Scope:** Mechanism overlap (humanizer ↔ watermark attack), intent vs side effect, EU AI Act Art. 50 / Code of Practice, OpenAI/Google industry posture, commercial humanizer ethics, unslop Boundaries  
**Status:** Complete research memo for policy docs, README honesty pass, and anti-detector boundary review  
**Cross-refs:** [Agent #71](AGENT-71-SIRA-WATERMARK-REMOVAL.md), [Agent #72](AGENT-72-BIRA-WATERMARK-ATTACK.md), [Agent #73](AGENT-73-RL-WATERMARK-ATTACKS.md), [Agent #74](AGENT-74-KGW-WATERMARK.md), [Agent #20](AGENT-20-WATERPARK-BENCHMARK.md), [Agent #31](AGENT-31-DIPPER.md), [Agent #35](AGENT-35-CROSS-MODEL-PARAPHRASE.md), [Agent #40](AGENT-40-DAMAGE-HUMANIZER-TIERS.md), [Agent #67](AGENT-67-MARKETING-VS-AUDIT.md), [Agent #70](AGENT-70-OPENAI-CLASSIFIER-SHUTDOWN.md)

---

## Executive summary

Humanization and watermark stripping share a **mechanism**, not necessarily an **intent**. Any rewrite that changes token-level conditional distributions — synonym swap, burstiness injection, cross-model paraphrase, anti-detector mode — can degrade KGW green-list statistics, SynthID-style tournament marks, and similar **statistical provenance** embedded at generation time. The side effect is now **quantified**, not speculative: DIPPER and GPT paraphrase halve WaterPark TGRL TPR (Agent #20); DAMAGE shows commercial humanizers collapse SynthID TPR from 66.5% → 1.5% (Agent #40); SIRA achieves ~100% ASR at $0.88/M tokens (Agent #71); BIRA proves **>99% evasion** via surprisal-targeted rewrite without watermark key access (Agent #72).

**Ethical core:** The same pass that helps an ESL writer escape a GPTZero false positive can scrub Gemini's SynthID mark. Law and product ethics must separate:

| Dimension | Legitimate humanization | Prohibited watermark evasion |
|-----------|-------------------------|------------------------------|
| **User goal** | Sound human; fix AI-isms; defend against detector FP | Hide AI authorship from mandated disclosure |
| **Target signal** | Lexical tells, uniform surprisal, register | Provenance mark specifically |
| **Knowledge** | May not know watermark exists | Knows mark must survive for compliance |
| **Product stance** | Document side effect; refuse strip mode | Must not ship or advertise removal |

**Regulatory floor (Aug 2026):** EU AI Act **Article 50(2)** requires machine-readable marking of generative text; the **Code of Practice on Transparency of AI-Generated Content** (draft Dec 2025, final Jun 2026) mandates multilayer marking (metadata + imperceptible watermark for text >200 tokens) and **Measure 1.5: non-removal** — signatories must prohibit deployers from altering or removing marks and must not promote tools designed to circumvent them. Deliberate watermark removal is a compliance violation; **incidental** degradation during legitimate editing sits in a harder gray zone that unslop resolves via **disclosure + refusal**, not feature denial of voice improvement.

**Industry posture:** OpenAI declined to ship a 99.9%-detectable ChatGPT watermark (Aug 2024) citing paraphrase bypass and ~30% user churn — validating the side-effect problem at source. Google ships SynthID on Gemini while acknowledging paraphrase fragility. Commercial humanizers (Undetectable.ai, StealthGPT, etc.) market **detector** evasion, not watermark removal, but DAMAGE proves the collateral damage is identical.

**unslop verdict:** unslop is a **humanizer**, not a watermark remover. Policy is already correct in `skills/unslop/SKILL.md`, `unslop/scripts/detector.py`, and README: document the side effect, refuse deliberate stripping, recommend **watermark after unslop** for provenance needs, scope anti-detector mode to ESL/resume false-positive defense. This memo is the ethics backbone for those Boundaries — cite Agents #71–74 for mechanism, Art. 50 CoP for law, Agent #67 for why "100% undetectable" marketing creates compliance exposure.

---

## 1. The side effect — mechanism in plain language

### 1.1 What watermarks actually are

Statistical text watermarks (KGW, SynthID-Text, Unigram, etc.) embed detectable bias in **token choice** at high-entropy positions. KGW adds δ to green-list logits; detection is a z-test on green-token rate (Agent #74). SynthID generalizes to tournament sampling (Agent #75 preview). These marks are **invisible to readers** but **fragile under rewrite** — by design they live where the model is uncertain, and rewrite targets the same positions (SIRA, BIRA).

Metadata provenance (C2PA, signed JSON sidecars) is a **different layer**: survives different attacks, dies on copy-paste and platform re-upload. EU CoP mandates **both** for online content where feasible.

### 1.2 Why humanization strips marks

| Humanization operation | Effect on watermark |
|------------------------|---------------------|
| Synonym / stock-vocab replacement | New token IDs → new green/red assignments |
| Sentence splitting / merging | Resets context hash for KGW LeftHash |
| Burstiness / structural pass | Changes high-entropy token draws |
| Cross-model paraphrase (GPT→Claude) | Full resample; strongest scrub (Agent #35) |
| Anti-detector LLM rewrite | Optimizes detector features; collaterally hits watermark stats |
| SIRA/BIRA-class targeted rewrite | **Deliberate** strip; unslop does not implement |

**Key insight from BIRA (Agent #72):** Rewriters need not identify green tokens exactly. Consistent suppression of high-surprisal tokens drives green rate below detector threshold with exponential decay in text length (Theorem 4.2). Humanizers that "sound more natural" often **accidentally** perform weak BIRA — varied vocabulary and sentence openings preferentially avoid the smoothest, highest-surprisal continuations.

### 1.3 Side effect vs primary effect

```
                    ┌─────────────────────────────────────┐
                    │         Rewrite pass (shared)        │
                    └─────────────────┬───────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    Primary intent              Collateral                 Adversarial
    (unslop default)            (unslop accepts)           (unslop refuses)
    ─────────────────           ──────────────             ────────────────
    Remove AI-isms              Degrade KGW/SynthID        Optimize ASR
    Fix ESL false positive      Break metadata if          Spoof watermark
    Match user voice            re-export strips tags      Strip for misconduct
    Improve readability         Lower detector score       Market "remove SynthID"
```

unslop owns the left column, documents the middle, refuses the right.

### 1.4 Quantified collateral (reference card)

| Source | Condition | Watermark / detection result |
|--------|-----------|------------------------------|
| Kirchenbauer ICLR 2024 | Human paraphrase, long text | Detectable @ ~800 tokens, FPR 10⁻⁵ |
| WaterPark (#20) | Dipper DP-40 | TGRL TPR 0.993 → **0.485** |
| WaterPark (#20) | Copy-paste 10% watermarked | TGRL TPR **≈0.000** |
| DAMAGE (#40) | Commercial humanizer tier | SynthID TPR 66.5% → **1.5%** |
| TempParaphraser (#24) | Single pass | Detection 56% → **1.7%** |
| SIRA (#71) | Self-info rewrite | **~100% ASR**, 7 schemes, $0.88/M tok |
| BIRA (#72) | Bias inversion | **>99% ASR**, improves on SIRA fidelity |
| OpenAI internal | Paraphrase / translation | 99.9% watermark → bypass cited as ship blocker (#70) |

**Takeaway:** Short, lightly edited watermarked text may retain marks; any serious humanization pass likely does not. "Watermark before edit" is a **broken compliance workflow** for human-in-the-loop publishing.

---

## 2. Ethical framing — intent, harm, and double effect

### 2.1 Four harm families (Category 09 lens)

Humanization ethics usually debates **detector evasion** and **academic misconduct**. Watermark side effects add a **provenance** harm family:

| Harm | Detector-evasion framing | Watermark side-effect framing |
|------|---------------------------|-------------------------------|
| **Epistemic** | Reader can't tell AI from human | Reader can't verify **which model** or **when** generated |
| **Institutional** | Grader loses signal | Regulator loses Art. 50 compliance chain |
| **Fairness** | ESL writers falsely flagged | Compliant creators lose mark after legitimate edit |
| **Security** | Spam/misinfo at scale | Stripped marks on synthetic news, deepfake captions |

unslop's anti-detector mode addresses **fairness** (Liang et al. ESL false positives). Watermark ethics adds: **legitimate editing must not be conflated with deliberate provenance fraud.**

### 2.2 Intent taxonomy (product-relevant)

| Class | Example | unslop response |
|-------|---------|-----------------|
| **A — Unaware** | User runs `/unslop balanced` on Claude draft; doesn't know SynthID exists | Side effect OK; Boundaries disclosure sufficient |
| **B — Aware, legitimate** | Journalist humanizes AI-assisted research brief; will add byline disclosure | Side effect OK; suggest disclose in prose + re-mark if org requires |
| **C — Aware, compliance conflict** | User asks to keep EU watermark while humanizing | Explain impossibility; workflow = humanize → re-mark → disclose |
| **D — Deliberate strip** | "Remove SynthID so Turnitin can't tell" | **Decline**; cite Art. 50 |
| **E — Deliberate strip + misconduct** | "Humanize so professor can't detect ChatGPT" | **Decline** academic misconduct (existing Boundary) |

Classes A–C are why unslop **documents** rather than **disables** rewrite. Classes D–E are hard refusals.

### 2.3 Doctrine of double effect (applied carefully)

Classic formulation: an act with a good primary effect and a bad side effect may be permissible if (1) the bad effect is not intended, (2) the good effect is not achieved **by means of** the bad one, (3) there is proportionate reason.

Applied to unslop:

- **Primary effect:** Remove AI-slop; improve voice; reduce false detector flags.
- **Side effect:** Statistical watermark degradation.
- **Not using harm as means:** unslop does not optimize ASR or sell "mark removal."
- **Proportionate reason:** ESL/resume/journalism use cases are documented; alternative (ban all rewrite) punishes legitimate users for adversarial misuse.

**Limit:** Double effect does **not** license marketing that **hides** the side effect or targets Class D users. Agent #67: "100% undetectable" claims create FTC-style substantiation and EU CoP exposure.

### 2.4 Mens rea and law (EU Art. 50)

The Code of Practice targets **intentional** removal and **tools designed to circumvent** marking (Measure 1.5–1.6). Incidental loss during copy-editing is not the same as running SIRA or advertising watermark stripping.

| Legal hook | Text (paraphrased from CoP draft/final 2026) | unslop alignment |
|------------|-----------------------------------------------|------------------|
| **Art. 50(2)** | Providers mark AI text machine-readably | unslop is not a GPAI provider; deployer-adjacent |
| **CoP Measure 1.5** | Preserve marks; prohibit removal/tampering in ToS | unslop ToS/docs should mirror: no strip mode |
| **CoP Measure 1.6** | Do not promote tools to circumvent marks | No "remove SynthID" marketing; anti-detector ≠ anti-watermark |
| **CoP text >200 tokens** | Imperceptible watermark required | Short emails may be exempt; cover letters often aren't |

**Gray zone:** A user who humanizes **knowing** marks will break but whose **purpose** is voice, not evasion — likely not "deliberate removal" under CoP if they add human disclosure. A user who humanizes **to evade** institutional AI marking — **is** deliberate circumvention. Product can't always distinguish; **refuse explicit strip requests**, document side effect for everyone else.

### 2.5 Asymmetry: watermark strip vs watermark spoof

RLSpoofer (Agent #73) shows **forgery** — human text injected with fake watermark signal. Ethics cuts both ways:

- **Stripping** breaks provenance on real AI text.
- **Spoofing** creates false provenance on human text.

unslop refuses both. Voice humanization has no legitimate spoof use case.

---

## 3. Academic literature — ethics-relevant papers

### 3.1 Foundational watermark + robustness

| Paper | Ethics takeaway for humanizers |
|-------|-------------------------------|
| **Kirchenbauer et al. 2023** (ICML) | Watermarks are public-good detection, not DRM; fragility under edit was known early |
| **Kirchenbauer et al. 2024** (ICLR reliability) | Human paraphrase **does not** erase marks instantly — long text survives; **sets false comfort** for "light edit" compliance |
| **Krishna et al. 2023** (DIPPER, NeurIPS) | Paraphrase evades detectors; **retrieval** defense is provider-side — humanizer can't beat logged API provenance |
| **Sadasivan et al. 2023** | TV bound on detection; watermark is **orthogonal** — you can strip mark while staying AI-detectable or vice versa |

### 3.2 Attack papers as ethics evidence (not instructions)

| Paper | What it proves for policy |
|-------|---------------------------|
| **SIRA** (Cheng et al., ICML 2025) | Commodity-cheap strip; responsible disclosure debate; side effect ≈ attack at scale |
| **BIRA** (Hwang et al., ICML 2026) | Humanization and strip are **structurally coupled**; surprisal rewrite is the shared lever |
| **RLCracker / RLSpoofer** (Huang et al., 2025–2026) | Adaptive attacks; long-text worst case; spoofing completes adversarial picture |
| **WaterPark** (EMNLP 2025) | No scheme wins all; paraphrase is default failure — **humanizers are in the threat model** |
| **DAMAGE** (COLING 2025) | Commercial humanizers **already** strip watermarks as side effect — industry norm, not unslop anomaly |
| **Christ–Gunn–Zamir** (COLT 2024) | Cryptographic undetectable marks possible — but **not deployed**; regulatory reliance on KGW-class is empirically fragile |

### 3.3 HCI / ethics venues (disclosure, not watermark-specific)

| Source | Relevance |
|--------|-----------|
| **Cohn et al. CHI 2024** | Disclosure labels don't stop anthropomorphism/trust inflation — same for "AI-generated" badges |
| **Weidinger et al. / DeepMind Ethics of Advanced AI Assistants** | Provenance and transparency as duty-of-care |
| **Category 09 SYNTHESIS** | Regulation targets structure (Art. 50); detection failing → watermarking; watermarking fragmenting |
| **HN cluster 45090612 et al.** | Community split: ESL legitimacy vs adversarial default assumption |

**Gap:** No FAccT/AIES paper yet titled "ethics of humanizer watermark side effects." Closest is DAMAGE conflict-of-interest discussion + EU policy commentaries. unslop can cite **mechanism papers + law**, not a single ethics canonical source.

---

## 4. Industry guidance and posture

### 4.1 EU — Art. 50 and Code of Practice

| Document | URL | Humanizer-relevant content |
|----------|-----|----------------------------|
| **EU AI Act Art. 50 guide** | https://artificialintelligenceact.eu/transparency-rules-article-50/ | Marking + labelling obligations Aug 2026 |
| **CoP draft (Dec 2025)** | EC digital strategy PDF | Measure 1.5 non-removal; >200 token watermark |
| **CoP final (Jun 2026)** | Published multi-layer framework | Signatories must not promote circumvention tools |
| **Commission Guidelines (Jul 2026)** | digital-strategy.ec.europa.eu | Implementation detail for providers |

**Practical guidance for deployers using humanizers:**

1. Mark at **publish**, not at first model draft, if editing pipeline includes paraphrase.
2. Prefer **metadata + visible disclosure** for text; treat statistical watermark as **best-effort**, not proof.
3. Contractually prohibit third-party tools that **advertise** mark removal.
4. Log generation provenance server-side (Grammarly Authorship model) where watermark can't survive.

### 4.2 Provider decisions

| Provider | Decision | Ethics read |
|----------|----------|-------------|
| **OpenAI** | No public ChatGPT text watermark (Aug 2024) | Chose UX over provenance; cited paraphrase bypass — **implicit admission** humanization breaks marks |
| **Google** | SynthID on Gemini; detector portal May 2025 | Ships mark knowing paraphrase risk; multilayer with C2PA |
| **Anthropic** | No public text watermark (2026 surveys) | Provenance via policy/disclosure, not token mark |

OpenAI's non-release is the strongest **industry** argument for unslop's "watermark after unslop" guidance: if the generator won't mark because rewrite breaks it, downstream humanizers can't fix upstream's choice.

### 4.3 Commercial humanizers — ethics contrast

| Segment | Marketing | Watermark stance | unslop differentiation |
|---------|-----------|------------------|------------------------|
| **Undetectable.ai, StealthGPT, etc.** | "Bypass Turnitin/GPTZero" | DAMAGE: strip SynthID collaterally; never disclose | unslop cites ESL FP defense; documents watermark side effect |
| **QuillBot, Grammarly** | Editing / clarity | Paraphrase product; no Art. 50 positioning | unslop is AI-slop stripper, not generic paraphrase |
| **SEO humanizers** | Rank / "human score" | Adversarial default | unslop refuses plagiarism use cases |

Agent #67: FTC Content at Scale order — **false detector claims** are enforceable. EU CoP extends logic to **circumvention tools**. A humanizer that adds "watermark removal" crosses a brighter line than one that admits collateral strip.

### 4.4 Practitioner community norms

From `docs/research/05-ai-text-detection-and-evasion/E-practical.md` and Category 09 forums:

- **Legitimate:** ESL writers, journalists polishing AI-assisted drafts, authors who disclose AI use.
- **Adversarial:** Students evading grader; SEO spam; "make ChatGPT undetectable" prompts.
- **Watermark rarely named** in practitioner threads — users conflate watermark with **detector score**. unslop must **disambiguate** in docs: green-list mark ≠ GPTZero probability.

---

## 5. unslop policy — current state and recommendations

### 5.1 Shipped policy (SSOT)

From `skills/unslop/SKILL.md` Boundaries:

> **Watermark interaction.** Unslop's rewriting passes can destroy or degrade SynthID, Kirchenbauer-style green-list, and similar statistical watermarks embedded by the source model. EU AI Act Article 50 prohibits watermark removal as a deliberate act. Unslop is a humanizer, not a watermark remover, but the side effect is real. Users who need provenance should watermark after unslop, not before.

From `unslop/scripts/detector.py` (ladder exhaustion):

> Do NOT attempt watermark removal — EU AI Act Article 50 prohibits it.

From `README.md`:

> Rewriting can degrade statistical watermarks like SynthID or green-list schemes. Side effect, not a feature. If provenance matters, watermark after unslop.

**Assessment:** Policy is **correct and ahead of most commercial humanizers**. This memo supplies citations and ethical scaffolding; no fundamental policy change required.

### 5.2 Anti-detector mode — scoped defense, not strip mode

Anti-detector (`/unslop anti-detector`) targets **detector false positives** (Liang ESL data, resume writers). Technical overlap with watermark strip is **real** (cross-model paraphrase step 6) but **intent boundary** is documented:

- SKILL.md: "not offered for academic misconduct"
- SKILL.md: "not for circumventing disclosure obligations"
- detector.py: refuses to recommend watermark removal at ladder end

**Ethical line:** Anti-detector may collaterally scrub marks. It must never **optimize** for scrubbing or cite SIRA/BIRA as next steps.

### 5.3 Refusal scripts (recommended)

| User request | Response pattern |
|--------------|------------------|
| "Remove SynthID / watermark" | Decline; cite Art. 50; explain side effect is unintended, not a service |
| "Humanize so [institution] can't detect AI" | Decline misconduct; offer voice improvement with disclosure obligation |
| "Will unslop break Gemini watermark?" | Yes, likely; humanize first, re-mark/disclose at publish |
| "I need EU Art. 50 compliance" | unslop is not a compliance tool; consult provider marking + legal; don't watermark pre-edit |

### 5.4 Workflow guidance (provenance-aware)

```
Recommended (provenance needed):
  Generate → unslop (voice) → visible AI disclosure → provider re-mark / C2PA at publish
                                    ↓
                          server-side log if available

Broken:
  Watermarked generate → unslop → assume mark survives

Acceptable (no statutory mark):
  Generate → unslop → human disclosure in prose only
```

### 5.5 Product action matrix

| Priority | Action | Rationale |
|----------|--------|-----------|
| **P1** | Keep Boundaries text in SSOT | Already correct; verify sync mirrors |
| **P2** | Add 1-sentence watermark side-effect note to `unslop-help` Boundaries | Help card completeness |
| **P2** | Anti-detector docs: "may affect embedded provenance marks" | Parallel to detector.py message |
| **P3** | Link Agent #77 from `docs/research/IMPLEMENTATION_TRACE.md` | Research ↔ policy trace |
| **P3** | Do **not** add watermark detection/removal to Python package | Legal + scope boundary |
| **P4** | Optional: `--provenance-warning` CLI flag | Prints side-effect once per run; opt-in to avoid noise |
| **—** | Never implement SIRA/BIRA/RLCracker | Hard red line |

---

## 6. Debate — stakeholder positions

### 6.1 Regulator / compliance officer

**Position:** Mandate marking at generation; prohibit removal; restrict detection to verified experts given FPR and paraphrase fragility.

**Humanizer challenge:** Supply chain includes edit tools. CoP Measure 1.5(a) explicitly covers content "used as input and subsequently transformed." Compliance requires **process**, not just model flags.

**unslop stance:** Align with CoP; don't be a circumvention tool.

### 6.2 Watermark researchers (Kirchenbauer, Google DeepMind)

**Position:** Marks are useful for **platform-scale** moderation and long-form audit; optimize for paraphrase robustness.

**Humanizer challenge:** SIRA/BIRA/WaterPark show single-pass paraphrase defeats most schemes; human edit is indistinguishable from attack.

**unslop stance:** Cite reliability paper for "long text survives light edit"; cite WaterPark/SIRA for "serious humanization breaks marks."

### 6.3 Humanizer vendors

**Position:** Detector bypass as product value; watermark rarely mentioned.

**Humanizer challenge:** DAMAGE proves watermark strip; EU CoP may classify aggressive bypass marketing as circumvention promotion.

**unslop stance:** Differentiate on **honesty + ESL defense**; eat own dog food on disclosure.

### 6.4 ESL / journalist users

**Position:** Need voice tools; didn't ask to break law; may not know watermarks exist.

**Humanizer challenge:** Collateral strip without disclosure feels like hidden liability.

**unslop stance:** Document side effect prominently; refuse only explicit strip/misconduct.

### 6.5 Academic integrity officers

**Position:** All humanizers are cheating tools.

**Humanizer challenge:** Over-broad; ignores legitimate AI-assisted writing with disclosure.

**unslop stance:** Keep misconduct refusal; don't ban voice improvement for disclosed AI use.

---

## 7. Open questions

1. **Does EU enforcement treat incidental strip as violation?** No public cases yet (Aug 2026); CoP language suggests **intent** matters.
2. **Post-hoc re-watermarking after humanization?** Technically requires another generation pass; not equivalent to preserving original mark.
3. **SynthID + unslop — measured ASR?** SIRA/BIRA didn't test SynthID in main tables; DAMAGE gives commercial-humanizer proxy only.
4. **Should unslop detect watermarks and warn?** Keyless z-test possible for KGW; false positives; scope creep — **not recommended**.
5. **C2PA for text documents?** Emerging; side effect differs (metadata strip on export vs token stats).
6. **Spoofing risk for unslop users?** RLSpoofer is attack-side; out of scope unless user requests forgery (refuse).
7. **Institutional policy templates?** Universities may ban humanizers entirely; unslop can't resolve — document tradeoffs.

---

## 8. Cross-references (sibling agents)

| Agent | Relevance to #77 |
|-------|------------------|
| **#17 Sadasivan** | TV bound; detection ≠ watermark |
| **#20 WaterPark** | Paraphrase as default watermark failure |
| **#24 TempParaphraser** | Cheap strip; anti-detector citation |
| **#31 DIPPER** | Paraphrase humanizer proxy |
| **#35 Cross-model paraphrase** | Strongest collateral scrub; Art. 50 refusal |
| **#40 DAMAGE** | Commercial humanizer watermark table |
| **#67 Marketing vs audit** | Honesty norm; FTC precedent |
| **#70 OpenAI shutdown** | Why watermark wasn't shipped |
| **#71 SIRA** | Side effect quantified; $0.88/M tok |
| **#72 BIRA** | Structural coupling theorem |
| **#73 RL attacks** | Strip + spoof worst case |
| **#74 KGW** | Mechanism primer |
| **#75 SynthID** | Production mark (companion) |
| **#76 EU Art. 50** | Legal deep dive (when written) |
| **#79 C2PA vs statistical** | Multilayer provenance response |

---

## 9. Key citations

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
  title={LLM Watermark Evasion via Bias Inversion},
  author={Hwang, Jaewoo and Park, Junhyeok and Ok, Junyoung},
  journal={arXiv:2509.23019},
  year={2025}
}
```

```bibtex
@inproceedings{kirchenbauer2023watermark,
  title={A Watermark for Large Language Models},
  author={Kirchenbauer, John and others},
  booktitle={ICML},
  year={2023},
  url={https://arxiv.org/abs/2301.10226}
}
```

```bibtex
@inproceedings{krishna2023dipper,
  title={Paraphrasing evades detectors of {AI}-generated text, but retrieval is an effective defense},
  author={Krishna, Kalpesh and others},
  booktitle={NeurIPS},
  year={2023}
}
```

```bibtex
@misc{eu2026coptransparency,
  title={Code of Practice on Transparency of {AI}-Generated Content},
  author={{European Commission}},
  year={2026},
  note={Measure 1.5 non-removal; text >200 tokens watermark}
}
```

---

## 10. Bottom line

Humanization **will** strip statistical watermarks as a **side effect** of the same distributional rewrite that removes AI-slop and reduces detector scores. That is empirically established (WaterPark, DAMAGE, SIRA, BIRA), legally sensitive (EU Art. 50 + CoP non-removal), and **ethically distinct from deliberate circumvention** when the user's goal is voice and disclosure, not provenance fraud.

unslop's job: **improve voice, document collateral, refuse strip modes, never market circumvention.** Users who need marks should **humanize first, mark and disclose at publish** — or skip humanization on watermarked drafts. The generator vendors already made the same bet when OpenAI chose not to ship a breakable watermark and Google shipped SynthID with known paraphrase fragility.

**Status:** Complete — ready for manifest update (#77 → complete) and synthesis pass (Category 09 ethics + Category 05 detection).
