<!--
Read this template top to bottom. PRs that leave required sections blank,
bundle unrelated changes, or skip the SSOT/mirror rule will be closed
without review.

For voice: write the PR description in the same plain-spoken style we ask
the model to use. No "comprehensive solution", no "robust implementation",
no "Great question!" openers. See skills/unslop-commit/SKILL.md.
-->

## What problem does this solve?

<!-- Describe the specific problem. If a behavior surprised you, name what
     you expected vs what you got. "Improve X" is not a problem statement. -->

## What does this PR change?

<!-- 1–3 sentences. The "what". The "why" goes above. -->

## Type of change

<!-- Mark ALL that apply with [x]. -->

- [ ] New AI-ism pattern (regex added to `unslop/scripts/humanize.py`)
- [ ] Validator change (`unslop/scripts/validate.py` `AI_ISMS`)
- [ ] CLI / package behavior (`unslop/scripts/cli.py` or sibling)
- [ ] Skill / rule content (`skills/`, `rules/`, hook prompts)
- [ ] Hook code (`hooks/*.{js,sh,ps1}`)
- [ ] Sync / CI / release workflow
- [ ] Documentation only
- [ ] Bug fix
- [ ] Refactor (no behavior change)
- [ ] Other: <!-- describe -->

## SSOT / mirrors

<!-- See CLAUDE.md "Source of Truth" section. The sync workflow overwrites
     mirrors on every push to main. Editing a mirror by hand is wasted work. -->

- [ ] I edited the SSOT file, not a mirrored copy
- [ ] If I added a new mirror target, I updated `scripts/sync-mirrors.sh`
      AND `.github/workflows/sync.yml` trigger paths
- [ ] N/A — this PR does not touch SSOT'd files

## If this PR adds an AI-ism

<!-- The repo's contract: every new AI-ism is added in 4 places. -->

- [ ] Regex added to the right list in `unslop/scripts/humanize.py`
      (`STOCK_VOCAB` / `HEDGING_OPENERS` / `SYCOPHANCY` / `PERFORMATIVE` /
      `TRANSITION_TICS` / `AUTHORITY_TROPES` / `SIGNPOSTING` /
      `FILLER_PHRASES` / `NEGATIVE_PARALLELISM`)
- [ ] Mirror pattern added to `AI_ISMS` in `unslop/scripts/validate.py`
- [ ] Test added in `tests/unslop/test_humanize.py` covering both the
      replacement and the preservation contract (no code/URL/heading mutation)
- [ ] Phrase added to the "Drop" lists in `skills/unslop/SKILL.md` and
      `rules/unslop-activate.md`
- [ ] N/A

## Tests

<!-- Required for any code or pattern change. -->

- [ ] `python3 -m pytest tests/unslop/` passes locally
- [ ] `ruff check unslop/scripts benchmarks` clean
- [ ] `mypy unslop/scripts` clean (strict mode)
- [ ] `python3 tests/verify_repo.py` passes
- [ ] `python3 benchmarks/run.py --all-intensities --strict` passes
      (monotonicity gate `subtle ≤ balanced ≤ full`)
- [ ] N/A — docs / non-code change

## Changelog

- [ ] Added a bullet under `## [Unreleased]` in `CHANGELOG.md`
- [ ] N/A — internal-only or trivial doc fix

## Breaking changes

<!-- Mark "None" if there are none. Otherwise list what callers/users must
     change and link to the migration note in CHANGELOG.md. -->

None.

## Bundled changes

<!-- If this PR contains multiple unrelated changes, stop and split it.
     If they're related, explain the dependency. -->

- [ ] Single concern. No drive-by changes mixed in.

## Security / privacy

- [ ] No secrets, API keys, or `.env*` content in the diff
- [ ] If the change reads or writes files, it routes through
      `is_sensitive_path()` (see `unslop/scripts/detect.py`)
- [ ] If the change writes to flag files or hook state, it routes through
      `safeWriteFlag()` (see `hooks/unslop-config.js`)
- [ ] N/A

## Human review

- [ ] A human read the entire diff before submission, not just the summary
