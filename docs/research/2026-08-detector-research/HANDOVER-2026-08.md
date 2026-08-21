# HANDOVER — August 2026 Detector Research & SSOT Integration

**Prepared:** 2026-08-20 (updated 2026-08-21 post-merge)  
**Session:** Cursor agent + 3 parallel subagents (git state, 100-agent corpus map, review consolidation)  
**Audience:** Next maintainer, reviewer, or agent picking up unslop detector/evasion work  
**Status:** Research **complete**; SSOT/code fixes **merged** via PR #19 (commit `76f387d`, sync `b5270b9`)

---

## 0. Read this first (60 seconds)

| Question | Answer |
|----------|--------|
| What was built? | **100-agent research program** in `docs/research/2026-08-detector-research/` (80 topic memos + 16 syntheses + 4 plans) |
| What ships next? | **Phase 2** from `PLAN-98-PHASE-2.md` — surprisal dynamics (Phase 1 merged) |
| What's merged? | **PR #19** → `76f387d` on main; sync commit `b5270b9`; **635 passed, 3 skipped** |
| Tests? | **635 passed, 3 skipped** — use `/opt/homebrew/bin/python3 -m pytest tests/unslop/` |
| Biggest lie to kill? | Booth tested **StealthGPT only** — not Turnitin, not twelve humanizers |
| Biggest remaining gap? | Phase 2 surprisal dynamics (TSD, SurpMark lite, multi-objective stop) |
| Start file | [`PLAN-100-MASTER-PRIORITIES.md`](./PLAN-100-MASTER-PRIORITIES.md) |

---

## 1. Mission & product truth

**unslop** subtracts AI-isms and preserves technical substance. It is a **polish layer**, not a detector-defeat tool.

August 2026 research converges on:

1. **Lexical scrub works** (~88–92% AI-ism reduction on fixtures).
2. **Deterministic passes move TMR ~0.0–0.2 pp** — expected; detectors read distributional fingerprints, not vocabulary lists.
3. **2026 detectors use five largely independent signals:** lexical AI-isms, burstiness (σ), DivEye surprisal variance, TSD late-stage volatility, GPTZero v6 predictability cones. unslop covers #1–2 well, measures #3 without fully closing the loop, has **zero code** for #4–5.
4. **TMR is a maintainer diagnostic**, not a user pass certificate. Never claim GPTZero/Turnitin bypass from TMR alone.
5. **Anti-detector mode** = ESL false-positive defense and voice restoration — **not** academic misconduct, watermark stripping, or bypass marketing.

**Strategic posture:** Ship honesty and wiring first (Phase 1), then surprisal dynamics (Phase 2), then optional LLM pipeline (Phase 3).

---

## 2. The 100-agent program (complete)

**Location:** `docs/research/2026-08-detector-research/`  
**Manifest:** [`AGENT-MANIFEST-100.md`](./AGENT-MANIFEST-100.md) — full index of all 100 outputs  
**Method:** Each of agents #1–80 = one topic, real web sweep (papers, GitHub, commercial, debate, unslop integration). #81–96 = category synthesis. #97–100 = phased implementation plans.

### 2.1 Agents 1–80 by domain

| Range | Domain | Count | Example memos |
|-------|--------|-------|----------------|
| 1–20 | Academic detection + benchmarks | 20 | DivEye (#1), TSD (#2), SurpMark (#3), RAID (#15), Liang ESL (#18), WaterPark (#20) |
| 21–40 | Evasion / humanization | 20 | MASH (#21), HIP (#22), TempParaphraser (#24), Adversarial Paraphrasing (#25), DIPPER (#31), CoPA (#28) |
| 41–55 | Stylometry / voice | 15 | Paneru contractions (#41), Catch Me (#43), Jemama (#50), Biber (#53), sentence-length (#54) |
| 56–70 | Commercial + policy | 15 | Turnitin (#56), GPTZero (#57), Booth (#62), Turnitin bypasser (#66), institutional retreat (#69) |
| 71–80 | Watermark + code gap | 10 | SIRA (#71), EU Art. 50 (#76), C2PA (#79), **`detector.py` gap audit (#80)** |

### 2.2 Agents 81–96 (synthesis)

| # | File | Scope |
|---|------|-------|
| 81–84 | `SYNTH-81` … `SYNTH-84` | Detection: academic, commercial, code gap, benchmarks |
| 85–88 | `SYNTH-85` … `SYNTH-88` | Evasion: prompt, LLM pipeline, refusals, tools |
| 89–92 | `SYNTH-89` … `SYNTH-92` | Stylometry: signals, voice-match, human cues, integration |
| 93–96 | `SYNTH-93` … `SYNTH-96` | Landscape: commercial, regulatory, watermark, user segments |

### 2.3 Agents 97–100 (implementation plans)

| # | File | Scope |
|---|------|-------|
| 97 | `PLAN-97-PHASE-0-1.md` | Docs refresh + Phase 1 quick wins (ladder, baseline, surprisal telemetry, bench) |
| 98 | `PLAN-98-PHASE-2.md` | TSD, SurpMark lite, cone proxy, multi-objective stop |
| 99 | `PLAN-99-PHASE-3.md` | LLM pipeline S1–S5 (MASH → HIP → TempParaphraser → AdvPara → cross-model) |
| 100 | `PLAN-100-MASTER-PRIORITIES.md` | **Master ranked list**, timeline, risks, non-goals |

### 2.4 Supporting artifacts

| File | Purpose |
|------|---------|
| `UPDATE-PLAN-2026-08.md` | Full integration plan + acceptance criteria per phase |
| `DEEP-RESEARCH-EXEC-SUMMARY.md` | Parallel-cli exec summary |
| `ai-detection-landscape-aug2026.json` | Structured landscape metadata |
| `drafts/2026-05-detector-test/` | May 2026 commercial detector bench protocol + partial results |

---

## 3. What this session accomplished

### 3.1 Research (prior sessions + corpus)

- All **100 agent outputs** written and indexed in manifest (status ✅ COMPLETE 2026-08-19).
- DivEye benchmark run: `benchmarks/results/diveye_comparison.json` — unslop proxies match IBM on GPT-2.
- Stylometric baseline generated: `benchmarks/results/stylometric_baseline.json` (untracked).

### 3.2 SSOT + code (merged in PR #19, commit `76f387d`)

**Docs (SSOT and research shards):**

- `skills/unslop/SKILL.md` — Liang 2304.02819; Catch Me vs Jemama split; Booth/StealthGPT-only; August 2026 five-signal landscape; Paneru contraction cite
- `README.md` — anti-detector honest framing; 4/6-step ladder; Booth/Jabarian attribution; Liang link
- `AGENTS.md` — citation hygiene block (accidental mem-palace dump removed)
- `docs/RESEARCH_AND_TECH.md`, `IMPLEMENTATION_TRACE.md`, `research-updating.md`, `D-commercial.md`, `A-academic.md` — aligned citations

**Code:**

- `unslop/scripts/detector.py` — `DEFAULT_LADDER` 4 steps (ends `anti-detector`); `LADDER_AGGRESSIVE` 6 steps; defaults 4/6; honest TMR docstring
- `unslop/scripts/cli.py` — default `--detector-max-iterations` 4; `_detector_feedback_max_iterations()`; `_surprisal_stdev_for_feedback()` wired
- `tests/unslop/test_detector.py` — ladder tests updated

### 3.3 Production review record

| Tool | Result |
|------|--------|
| GitHub Actions | Python 3.10–3.13, Codecov, mirror sync, and Pages passed |
| CodeRabbit | Initial findings fixed; zero unresolved review threads before merge |
| Codex | Focused review findings fixed and reverified |
| Cursor CLI | `claude-4.6-opus-max-thinking` found no blocking P0/P1 issue in the final production diff |

---

## 4. Citation ground truth (non-negotiable)

Verify against memos before any public cite. **`AGENTS.md`** and **`PLAN-97`** are the enforcement list.

| Wrong | Correct | Agent memo |
|-------|---------|------------|
| Liang ESL = `arXiv:2306.04723` | **Liang 2023 — [2304.02819](https://arxiv.org/abs/2304.02819)** | #18 |
| 2306.04723 for Liang | That's **Tulchinskii PHD** (intrinsic dimension) | #9 |
| "Booth tested 12 humanizers" / Turnitin at Booth | **Jabarian & Imas 2025 (BFI WP 2025-116) tested StealthGPT only** | #62 |
| Turnitin 54–85% bypass | Cite **Blommerde / MPG ONE tier tests**, not Booth | #56, #66 |
| Catch Me 23.5× few-shot | Catch Me ~**2–3×** few-shot; Blog AV ~17–21% | #43 |
| 23.5× from Catch Me | **Jemama (2509.24930)** — few-shot prompting versus zero-shot on its academic-essay corpus | #50 |
| "Kalemaj" + 2604.11687 | **Paneru et al. 2026 — [2604.11687](https://arxiv.org/abs/2604.11687)** | #41 |
| "~6 pp median" in Jabarian & Imas | **Not in that paper** — cite HumanizerBench/DAMAGE with date if used | #62, #67 |
| TMR 99.28% RAID as product score | Model-card fact for **TMR checkpoint only** | #15, #80 |
| "HIP-powered product" | **"Prompt analog of published stages"** | #22, SYNTH-86 |

**Adjudicated 2026-08-21:** arXiv:2509.24930 explicitly attributes the 23.5× gain to **few-shot prompting**, not fine-tuning.

---

## 5. Merge record

### 5.1 PR #19 → main

- **PR:** #19
- **Merge commit:** `76f387d`
- **Post-merge sync:** `b5270b9`
- **CI result:** 635 passed, 3 skipped
- **Phase 1 items shipped:** citation fixes, 4-step detector ladder, anti-detector mode, baseline JSON path, CLI sentinel fix, SSOT skill refresh

### 5.2 Mirrors (synced by CI)

Post-merge sync workflow (`b5270b9`) updated all generated mirrors:

- `plugins/unslop/skills/unslop/SKILL.md`
- `.cursor/skills/unslop/SKILL.md`, `.windsurf/skills/unslop/SKILL.md`
- `skills/unslop-file/scripts/cli.py`, `detector.py`

**Rule:** Edit only SSOT per `CLAUDE.md`. Mirrors are generated.

### 5.3 Detector ladder (merged code)

**Default (`DEFAULT_LADDER`) — 4 steps:**

1. `("balanced", False, False)`
2. `("full", False, False)`
3. `("full", True, True)` — structural + soul
4. `("anti-detector", True, True)` — lexical_targets (needs baseline JSON)

**Aggressive (`LADDER_AGGRESSIVE`) — 6 steps:** subtle → balanced → balanced+structural → full+structural → full+structural+soul → anti-detector

**CLI defaults:** an omitted `--detector-max-iterations` maps to **4** for the default ladder or **6** for the aggressive ladder. An explicit value, including `4`, is preserved.

---

## 6. Consolidated review findings (resolved in PR #19)

Sources: `.tmp-codex-review.md`, Gemini context, subagent consolidation. All P0 and P1 items below were resolved before merge.

### P0 — resolved

| ID | Location | Issue | Resolution |
|----|----------|-------|------------|
| P0-1 | `RESEARCH_AND_TECH.md:51`, `SKILL.md:82`, `A-academic.md:212`, `IMPLEMENTATION_TRACE.md:38`, `research-updating.md:287` | **Jemama 23.5× mechanism** | Verified and aligned across all files |

### P1 — resolved

| ID | Location | Issue | Resolution |
|----|----------|-------|------------|
| P1-1 | `cli.py:451` | Explicit `--detector-max-iterations 4` silently becomes 6 in aggressive mode | Fixed: sentinel logic corrected |
| P1-2 | `detector.py:278–282` | Baseline required but no CLI validation | Fixed: baseline path wired and validated |
| P1-3 | `research-updating.md:129,143` | "Chicago Booth 2026" | Fixed: Jabarian & Imas 2025 / StealthGPT-only |
| P1-4 | `D-commercial.md:35` | Stanford HAI 32% vs Liang >50% TOEFL mixed | Fixed: claims separated and cited properly |
| P1-5 | `README.md:392` vs `:597,:643,:671` | TMR `< 0.5 pp` vs `0.0–0.2 pp` | Fixed: consistent measured band |

### P2 — resolved or deferred

| ID | Location | Issue | Status |
|----|----------|-------|--------|
| P2-1 | `AGENTS.md:33` vs `CLAUDE.md` | Citation hygiene not mirrored | Resolved |
| P2-2 | `SKILL.md:88` | "Detectors stack DivEye/TSD/SurpMark" | Softened |
| P2-3 | `detector.py:27` vs `:32` | "release gate" vs "not a gate" | Resolved |
| P2-4 | `cli.py:444` | `except Exception` + unused import | Resolved |
| P2-5 | `IMPLEMENTATION_TRACE.md` | Stale line refs; Kalemaj → Paneru | Resolved |
| P2-6 | `IMPLEMENTATION_TRACE.md:43` | "Single most reliable" superlative | Resolved |
| P2-7 | `README.md:610` | Weak comparator cite | Resolved |
| P2-8 | Mirrors | Run `sync-mirrors.sh` | Handled by CI sync (`b5270b9`) |

---

## 7. Implementation roadmap (from PLAN-100)

### Phase 0 — Docs + honesty (complete)

- [x] Liang, Booth, Catch Me/Jemama in SSOT
- [x] August 2026 block in `docs/research/research-updating.md`
- [x] Four-question gate + refusal scripts in `SKILL.md` (SYNTH-87)
- [x] Five-signal table in `SKILL.md` (SYNTH-81)
- [x] Wave A: refresh `docs/research/` cat 05, 15, 16 (+ 09, 18)
- [x] Mirror sync + `CLAUDE.md` citation block

**Gate:** No commercial cite without `[detector] [version] [arm] [metric] [tier I–V]`.

### Phase 1 — Quick wins (complete, merged PR #19)

| Rank | Action | Status |
|------|--------|--------|
| 1 | Anti-detector in feedback ladder | **Merged** |
| 2 | Ship `stylometric_baseline.json` | **Merged** |
| 3 | Fix SSOT citations | **Merged** |
| 4 | Surprisal/TSD in `--detector-feedback` JSON | **Merged** |
| 5 | SKILL August landscape | **Merged** |
| 6 | `shield_metrics.py` | **Merged** |
| 7 | `detector_bench.py` upgrades | **Merged** |
| 8 | May detector-test CSV | **Merged** — protocol + run |
| 14 | CoPA-style anti-detector prompt | **Merged** |

**Phase 1 exit criteria met:** pytest green (635/3); ladder step 4+ is anti-detector; `load_baselines()` non-empty; feedback JSON includes full surprisal vector; no Booth/Turnitin misattribution.

### Phase 2 — Surprisal dynamics (weeks 4–8)

- `compute_tsd_reading()` in `surprisal.py`
- SurpMark lite, cone-width proxy
- Multi-objective stop (TMR + dynamics band)
- StylometryContext: measure → edit → re-measure

### Phase 3 — LLM pipeline (weeks 9–16, optional)

- `llm_pipeline.py`: MASH → HIP → TempParaphraser → AdvPara → cross-model capstone
- Budget caps; semantic ≥0.92 gate; no ASR marketing

### Explicit non-goals (never ship)

- Watermark strip modes / SIRA integration
- Score-targeting schedulers (RateAudit pattern)
- "Beat Turnitin" / "100% undetectable" marketing
- Commercial humanizer API wrappers in core package
- Trained adversary weights in pip wheel

---

## 8. Commands cheat sheet

| Task | Command |
|------|---------|
| Tests | `/opt/homebrew/bin/python3 -m pytest tests/unslop/` |
| Mirror sync | `bash scripts/sync-mirrors.sh` |
| Stylometric baseline regen | `python3 benchmarks/stylometric_baseline.py --out benchmarks/results/stylometric_baseline.json` |
| DivEye comparison | See `benchmarks/results/diveye_comparison.md` |
| Detector feedback (local) | `unslop --detector-feedback file.md` (needs TMR weights: `python3 -m unslop.scripts.fetch_detectors`) |
| Hook verify | `bash hooks/install.sh` then `/unslop full` and `stop unslop` |
| SSOT skill | Edit `skills/unslop/SKILL.md` only |
| Commit scope suggestion | 12 tracked SSOT/code files + optionally `benchmarks/results/stylometric_baseline.json`; separate PR for full `drafts/` if desired |

**Python pitfall:** PlatformIO venv's `python3` lacks pytest — use Homebrew Python.

---

## 9. Key file map

| Purpose | Path |
|---------|------|
| **Start here** | `docs/research/2026-08-detector-research/PLAN-100-MASTER-PRIORITIES.md` |
| Phase 0–1 tasks | `docs/research/2026-08-detector-research/PLAN-97-PHASE-0-1.md` |
| 100-agent index | `docs/research/2026-08-detector-research/AGENT-MANIFEST-100.md` |
| Code gap audit | `docs/research/2026-08-detector-research/AGENT-80-DETECTOR-PY-GAP-AUDIT.md` |
| DivEye memo | `docs/research/2026-08-detector-research/AGENT-01-DIVEYE.md` |
| Booth / StealthGPT | `docs/research/2026-08-detector-research/AGENT-62-CHICAGO-BOOTH-2026.md` |
| Liang ESL | `docs/research/2026-08-detector-research/AGENT-18-LIANG-ESL-BIAS.md` |
| Catch Me / Jemama | `AGENT-43-*`, `AGENT-50-*`, `SYNTH-90-*` |
| This handover | `docs/research/2026-08-detector-research/HANDOVER-2026-08.md` |
| SSOT skill | `skills/unslop/SKILL.md` |
| Detector loop | `unslop/scripts/detector.py` |
| CLI | `unslop/scripts/cli.py` |
| Maintainer guide | `CLAUDE.md` |
| Agent instructions | `AGENTS.md` |
| Codex review | `.tmp-codex-review.md` (repo root, untracked) |
| Review prompt template | `.tmp-review-prompt.md` |

---

## 10. Next owner checklist

### Day 1 (2–4 hours)

1. Read §0 and §4 of this doc + `PLAN-100` executive summary.
2. Run Claude Opus review (if quota available); merge with `.tmp-codex-review.md`.
3. Fix **P0-1** (Jemama mechanism — verify paper first).
4. Fix **P1-1** (CLI sentinel), **P1-3** (Booth 2026), **P1-5** (TMR pp).
5. `bash scripts/sync-mirrors.sh` + pytest.
6. Decide commit scope: code/docs only vs include `drafts/` + benchmarks.

### Week 1

7. Complete Phase 0 doc items (August block, four-question gate, five-signal table).
8. Commit `stylometric_baseline.json` + prove anti-detector step 4 end-to-end (**P1-2**).
9. Add `--detector-surprisal` flag + full `SurprisalReading` in feedback JSON (PLAN-97).
10. Open PR with Conventional Commit; run `unslop-commit` style.

### Weeks 2–3 (Phase 1 exit)

11. `shield_metrics.py` + detector bench upgrades.
12. May detector-test bench run → `scores.csv`.
13. CoPA anti-detector prompt block in `humanize.py`.

---

## 11. Risks & known blockers

| Risk | Mitigation |
|------|------------|
| Cursor Task ignores `model` param | Use Codex CLI or direct API for specified models |
| Claude CLI session limits | Schedule reviews; use API key path if available |
| Mirror drift | Always sync after SSOT edit; CI handles post-merge |
| Overclaim regression | Enforce citation hygiene in PR review |
| Phase 2 complexity (TSD, SurpMark) | Keep scope bounded per PLAN-98 |

---

## 12. Subagent audit trail (handover compilation)

This document was assembled using **3 parallel subagents** (not 100 — the **100-agent research corpus** is the subject, not the handover runner count):

| Subagent | ID | Output used in |
|----------|-----|----------------|
| Shell / git state | `c59de703-4d34-426f-ac30-be18ded35844` | §5, §8 |
| 100-agent corpus map | `2f5f73a6-8e0e-420d-8825-6cfca85e2e0a` | §2, §7, §4 |
| Review consolidation | `abfb11e4-78a2-480f-ad27-d8a42c502fc3` | §6, §3.3 |

Prior session subagents (Opus/Gemini review via Task) **mis-routed to Composer** — findings discarded except Gemini cross-doc flags folded into §6.

---

## 13. One-line handoff

**Phase 1 shipped (PR #19, `76f387d`).** Research archive published. Next: Phase 2 surprisal dynamics per `PLAN-98-PHASE-2.md` — TSD readings, SurpMark lite, multi-objective stop.

---

*End of handover. Update this file when Phase 2 gates close or when significant architectural decisions are made.*
