# Production Refresh 0.7.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the August 2026 research archive, modernize supported runtimes and automation, add a distributable Cursor plugin, and prepare unslop 0.7.0 without adding Phase 2 or Phase 3 detector-evasion features.

**Architecture:** Work from synced `origin/main` in Cursor's isolated worktree. Import only the research and policy artifacts from `chore/repo-refresh-2026-08`; keep runtime behavior at the merged Phase 1 surface. SSOT files remain authoritative, generated mirrors are validated locally but left for the post-merge sync workflow.

**Tech Stack:** Python 3.10–3.14, Node.js 24 LTS, GitHub Actions, Docker, Markdown/JSON plugin manifests, pytest, Ruff, mypy, Cursor Plugins.

**Spec:** `docs/research/2026-08-detector-research/HANDOVER-2026-08.md`

## Global Constraints

- Keep Python support at `>=3.10`; Python 3.14 is a required CI row.
- Edit `skills/unslop/SKILL.md`, `rules/unslop-activate.md`, and `unslop/` only as SSOT; do not commit generated mirrors.
- Do not add TSD, SurpMark, predictability-cone, watermark-removal, score-targeting, or multi-stage evasion code.
- Public detector claims must name the detector/version, evaluation arm, metric, and evidence tier.
- Liang ESL is arXiv:2304.02819; Booth tested StealthGPT only; Jemama owns the 23.5× few-shot result.
- Version every public distribution surface as `0.7.0` and use tag `unslop-v0.7.0`.
- Use official registries or upstream release pages for version claims.

---

### Task 1: Import and correct the August research archive

**Files:**
- Create: `docs/research/2026-08-detector-research/**`
- Modify: `.gitignore`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `docs/research/index.md`
- Modify: `docs/research/research-updating.md`
- Modify: `docs/research/IMPLEMENTATION_TRACE.md`
- Modify: `docs/RESEARCH_AND_TECH.md`

**Interfaces:**
- Consumes: the preserved `chore/repo-refresh-2026-08` branch and merged PR #19 state.
- Produces: a tracked research snapshot and citation rules used by the rest of the release docs.

- [x] **Step 1: Import only research-owned paths from the preserved branch**

Run:

```bash
git restore --source=chore/repo-refresh-2026-08 -- \
  .gitignore AGENTS.md CLAUDE.md docs/research/index.md \
  docs/research/2026-08-detector-research
```

Do not restore benchmark result timestamps, generated mirrors, runtime code, or tests from that branch.

- [x] **Step 2: Rename the Paneru memo and update references**

Rename `AGENT-41-KALEMAJ-CONTRACTION-STYLOMETRY.md` to `AGENT-41-PANERU-CONTRACTION-STYLOMETRY.md`. Replace author-name errors while preserving any historical note explaining the earlier misattribution.

- [x] **Step 3: Update the handover from pre-merge state to production history**

Record PR #19, merge commit `76f387d`, sync commit `b5270b9`, 635 passed/3 skipped, the completed Phase 1 items, and the remaining Phase 2/3 roadmap. Remove claims that the work is uncommitted or that baseline/CLI sentinel fixes are open.

- [x] **Step 4: Run citation-hygiene scans and fix every hit**

Run:

```bash
rg -n 'Liang.{0,80}2306\.04723|2306\.04723.{0,80}Liang' docs AGENTS.md CLAUDE.md
rg -n 'Booth.{0,120}(Turnitin|twelve humanizers)|Jabarian.{0,120}Turnitin' docs
rg -n 'Catch Me.{0,120}23\.5|23\.5.{0,120}Catch Me' docs
rg -n 'Kalemaj.{0,120}2604\.11687|2604\.11687.{0,120}Kalemaj' docs
```

Expected: zero unsupported attribution hits. References that explain a past error must state the correction in the same sentence.

- [x] **Step 5: Validate research identifiers and links**

Extract unique arXiv IDs, DOI links, and GitHub repository links from the new archive. Check arXiv/DOI resolution and GitHub repository existence using primary endpoints. Save no credentials or transient response files in the repo.

- [x] **Step 6: Commit the research snapshot**

```bash
git add .gitignore AGENTS.md CLAUDE.md docs/RESEARCH_AND_TECH.md docs/research
git commit -m "docs(research): publish August detector audit"
```

---

### Task 2: Modernize CI, runtimes, and dependency pins

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `.github/workflows/sync.yml`
- Modify: `.github/workflows/publish.yml`
- Modify: `.github/workflows/weekly-detector-bench.yml`
- Modify: `Dockerfile`
- Modify: `unslop/pyproject.toml`

**Interfaces:**
- Consumes: official GitHub Action releases, PyPI JSON metadata, Node release index, and Docker Hub tag metadata checked on 2026-08-21.
- Produces: a required Python 3.10–3.14 matrix and current automation/runtime pins.

- [x] **Step 1: Update official Actions majors**

Use `actions/checkout@v7`, `actions/setup-python@v7`, `actions/setup-node@v7`, `actions/cache@v6`, `actions/upload-artifact@v7`, `codecov/codecov-action@v7`, and `dependabot/fetch-metadata@v3`. Keep `pypa/gh-action-pypi-publish@release/v1` because upstream's current stable release is still v1.

- [x] **Step 2: Expand supported runtimes**

Add Python `3.14` to the required CI matrix, change hook tests to Node `24`, add the Python 3.14 classifier, and set Docker's default `PYTHON_VERSION` to `3.14`. Keep the GPU/model weekly workflow on Python 3.12 until its heavy optional stack is separately certified.

- [x] **Step 3: Pin current development/build tooling compatible with Python 3.10**

Set build floors to `setuptools>=84` and `wheel>=0.48`. Pin dev tools to `pytest==9.1.1`, `pytest-cov==7.1.0`, `ruff==0.16.4`, and `mypy==2.3.1`. Raise the Anthropic optional floor to `anthropic>=1.0,<2`; leave heavy scientific dependencies resolver-compatible across Python 3.10–3.14.

- [x] **Step 4: Pin release tooling in the publish workflow**

Install `build==1.5.0` and `twine==7.0.0`, then retain Trusted Publishing and the existing tag/version check.

- [x] **Step 5: Verify tooling locally**

```bash
/opt/homebrew/bin/python3 -m pytest tests/unslop/
/private/tmp/unslop-ruff-0164/bin/ruff check --config unslop/pyproject.toml unslop/scripts benchmarks
/opt/homebrew/bin/python3 -m mypy --config-file unslop/pyproject.toml unslop/scripts
node --version
docker build --build-arg PYTHON_VERSION=3.14 -t unslop:0.7.0-test .
```

Expected: tests, lint, and types pass; Node reports v24 in CI; the Docker image builds and `unslop --version` works.

- [x] **Step 6: Commit automation updates**

```bash
git add .github/workflows Dockerfile unslop/pyproject.toml
git commit -m "ci: update runtimes and actions"
```

---

### Task 3: Add and validate the Cursor Plugin package

**Files:**
- Create: `.cursor-plugin/plugin.json`
- Modify: `tests/verify_repo.py`
- Modify: `README.md`
- Modify: `GETTING_STARTED.md`

**Interfaces:**
- Consumes: root `skills/`, `.cursor/rules/`, and existing SVG assets.
- Produces: a single-repository Cursor Plugin ready for local loading and marketplace review.

- [x] **Step 1: Add a failing verifier test**

Require `.cursor-plugin/plugin.json`, parse it, check version alignment, and confirm its `skills`, `rules`, and `logo` paths exist. Do not include `commands/*.toml`: Cursor's plugin reference accepts Markdown/text command files, not this repo's Claude TOML commands.

- [x] **Step 2: Run the verifier and confirm the missing-manifest failure**

```bash
/opt/homebrew/bin/python3 tests/verify_repo.py
```

Expected: failure naming `.cursor-plugin/plugin.json`.

- [x] **Step 3: Create the manifest**

Use required `name: unslop`, version `0.7.0`, author, homepage, repository, MIT license, keywords, a committed SVG logo, `skills: ./skills/`, and `rules: ./.cursor/rules/`. Use only fields supported by Cursor's official plugin reference.

- [x] **Step 4: Re-run verification**

```bash
/opt/homebrew/bin/python3 tests/verify_repo.py
node -e "JSON.parse(require('fs').readFileSync('.cursor-plugin/plugin.json'))"
```

Expected: both commands exit 0.

- [x] **Step 5: Document current Cursor installation paths**

State that cloned repositories still auto-load project rules. For installed plugins, direct users to Cursor Customize after marketplace approval. Document local development loading via `~/.cursor/plugins/local/unslop` without claiming the listing is live.

- [x] **Step 6: Commit the Cursor package**

```bash
git add .cursor-plugin tests/verify_repo.py README.md GETTING_STARTED.md
git commit -m "feat(cursor): add marketplace plugin manifest"
```

---

### Task 4: Align every 0.7.0 distribution signal

**Files:**
- Modify: `unslop/scripts/__init__.py`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `.codex/hooks.json`
- Modify: `gemini-extension.json`
- Modify: `plugins/unslop/.codex-plugin/plugin.json`
- Modify: `.cursor-plugin/plugin.json`
- Modify: `tests/verify_repo.py`

**Interfaces:**
- Consumes: version `0.7.0` and tag format `unslop-v0.7.0`.
- Produces: one release version across Python, Claude, Agents, Codex, Cursor, and Gemini surfaces.

- [x] **Step 1: Extend version verification**

Add `.codex/hooks.json` and `.cursor-plugin/plugin.json` to `verify_version_alignment()`.

- [x] **Step 2: Bump authoritative version files**

Change every listed public version signal to `0.7.0`. Rename the local Agents marketplace plugin from `unslop-repo` to `unslop` so its install name matches other hosts.

- [x] **Step 3: Verify no stale public versions remain**

```bash
rg -n '"version"\s*:\s*"(0\.3\.0|0\.6\.2)"' --glob '*.json'
/opt/homebrew/bin/python3 tests/verify_repo.py
```

Expected: the grep is empty and verification reports `0.7.0`.

- [x] **Step 4: Commit version alignment**

```bash
git add unslop/scripts/__init__.py .claude-plugin/marketplace.json \
  .agents/plugins/marketplace.json .codex/hooks.json gemini-extension.json \
  plugins/unslop/.codex-plugin/plugin.json .cursor-plugin/plugin.json tests/verify_repo.py
git commit -m "chore(release): align 0.7.0 versions"
```

---

### Task 5: Refresh release notes, guides, and install copy

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `GETTING_STARTED.md`
- Modify: `CONTRIBUTING.md`
- Create: `docs/RELEASING.md`

**Interfaces:**
- Consumes: completed tasks 1–4 and their exact user-visible behavior.
- Produces: release copy and a reproducible maintainer release path.

- [x] **Step 1: Cut the 0.7.0 changelog section**

Leave a new empty `[Unreleased]` section, then date `[0.7.0] — 2026-08-21`. Cover detector feedback Phase 1, the research archive, current CI/runtime support, Cursor packaging, citation corrections, and dependency updates. Edit only root `CHANGELOG.md`; `unslop/CHANGELOG.md` is generated.

- [ ] **Step 2: Audit install and product claims**

Verify every Claude, Cursor, Windsurf, Gemini, Codex, pip, and Docker command against actual files or current first-party docs. Remove stale model labels and future-tense EU AI Act wording. Do not change benchmark numbers without a matching committed result.

- [ ] **Step 3: Add a release runbook**

Document: clean main, version check, tests, mirror sync dry run, build, `twine check`, tag, GitHub workflow, PyPI verification, GitHub release, Cursor submission/refresh, and dependent marketplace checks. Mark Cursor submission as manual because Cursor reviews plugins through its publisher form.

- [ ] **Step 4: Commit release documentation**

```bash
git add CHANGELOG.md README.md GETTING_STARTED.md CONTRIBUTING.md docs/RELEASING.md
git commit -m "docs: update release and install guides"
```

---

### Task 6: Run release verification without committing mirrors

**Files:**
- Generated locally then restored: `.cursor/`, `.windsurf/`, `plugins/unslop/skills/`, `skills/unslop-file/`, `unslop/CHANGELOG.md`

**Interfaces:**
- Consumes: the full maintenance branch.
- Produces: reproducible evidence for the PR and release tag.

- [ ] **Step 1: Run the deterministic gates**

```bash
/opt/homebrew/bin/python3 -m pytest tests/unslop/
/opt/homebrew/bin/python3 -m mypy --config-file unslop/pyproject.toml unslop/scripts
/private/tmp/unslop-ruff-0164/bin/ruff check --config unslop/pyproject.toml unslop/scripts benchmarks
/opt/homebrew/bin/python3 benchmarks/run.py --strict
/opt/homebrew/bin/python3 benchmarks/run.py --all-intensities --strict
/opt/homebrew/bin/python3 benchmarks/detector_feedback_bench.py
```

- [ ] **Step 2: Run repository and package gates**

```bash
/opt/homebrew/bin/python3 tests/verify_repo.py
/opt/homebrew/bin/python3 -m build unslop
/opt/homebrew/bin/python3 -m twine check unslop/dist/*
```

- [ ] **Step 3: Prove mirrors are CI-owned**

After verification, restore generated mirror paths to `origin/main`. Confirm the PR diff contains SSOT changes but no generated mirrors.

- [ ] **Step 4: Run an independent Cursor Opus production review**

Review `origin/main...HEAD` in read-only mode. Fix all verified P0–P2 findings, repeat affected tests, and record any declined false positive with evidence.

---

### Task 7: Open, review, merge, and release

**Files:**
- No new implementation files unless review finds a verified defect.

**Interfaces:**
- Consumes: green Task 6 evidence.
- Produces: merged maintenance PR, successful post-merge workflows, release tag, and a manual-action report.

- [ ] **Step 1: Push and open the PR from MohamedAbdallah-14**

Use branch `repo-refresh-2026-08`; verify `gh pr view` reports author `MohamedAbdallah-14`.

- [ ] **Step 2: Wait for all checks and reviews**

Address every verified inline finding, resolve threads only after the fix is pushed, and rerun local gates for Python changes.

- [ ] **Step 3: Merge with the repository's merge-commit convention**

Monitor Tests, Sync SSOT Mirrors, Pages, and any sync-generated follow-up SHA until the final state is green.

- [ ] **Step 4: Tag and verify PyPI**

Create and push `unslop-v0.7.0` only after synced `main` is green. Watch `Publish to PyPI`, then verify PyPI reports 0.7.0 and a clean install returns `unslop 0.7.0`.

- [ ] **Step 5: Report manual distribution actions**

Report Cursor Marketplace publisher-form submission or refresh as manual. Report whether Claude, Codex, Gemini, Agents, npm, or any other registry needs action; do not invent a registry where the repo ships only source files.
