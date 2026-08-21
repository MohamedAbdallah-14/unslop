# Releasing unslop

This is the maintainer path from a reviewed branch to PyPI and the host packages. Run it from a disposable worktree, not a checkout with unrelated changes.

## Before the PR

Confirm the release identity and base:

```bash
gh api user --jq .login
git fetch origin
git status --short --branch
git merge-base --is-ancestor origin/main HEAD
```

The GitHub login must be the intended maintainer account. The worktree must be clean before verification.

Update the version in every public source:

- `unslop/scripts/__init__.py`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `.codex/hooks.json`
- `.cursor-plugin/plugin.json`
- `gemini-extension.json`
- `plugins/unslop/.codex-plugin/plugin.json`
- root `CHANGELOG.md`

Leave an empty `[Unreleased]` section above the dated release. Edit root `CHANGELOG.md` only; `unslop/CHANGELOG.md` is generated.

## Verification

Use Python 3.10 or newer and Node 24. CI repeats the test job on Python 3.10–3.14.

```bash
python3 -m pytest tests/unslop/
python3 -m pytest tests/
python3 -m mypy --config-file unslop/pyproject.toml unslop/scripts
python3 -m ruff check --config unslop/pyproject.toml unslop/scripts benchmarks
python3 benchmarks/run.py --strict
python3 benchmarks/run.py --all-intensities --strict
python3 benchmarks/detector_feedback_bench.py
python3 tests/verify_repo.py
```

`tests/verify_repo.py` runs `scripts/sync-mirrors.sh`. Inspect the generated diff, confirm a second sync is empty, then keep generated mirrors out of the PR. The post-merge `Sync SSOT Mirrors` workflow owns those copies.

Build the same sdist and wheel that the publication workflow will build:

```bash
python3 -m pip install build==1.5.0 twine==7.0.0
python3 -m build unslop
python3 -m twine check unslop/dist/*
python3 -m pip install --force-reinstall unslop/dist/*.whl
unslop --version
```

For a runtime smoke test:

```bash
docker build --build-arg PYTHON_VERSION=3.14 -t unslop:release-test .
docker run --rm unslop:release-test --version
```

## PR and merge

Push the branch, open the PR under the intended GitHub account, and wait for every required check. Address verified review findings before resolving their threads. Merge with a merge commit, matching this repository's history.

After merge, wait for both commits when sync has work:

1. the human merge commit;
2. the `github-actions[bot]` mirror-sync commit.

Do not tag until Tests, Sync SSOT Mirrors, and Pages are green on the final `main` SHA.

## Tag, PyPI, and GitHub release

Create the release tag on that final synced SHA:

```bash
git switch main
git pull --ff-only origin main
git tag -a unslop-vX.Y.Z -m "unslop X.Y.Z"
git push origin unslop-vX.Y.Z
```

The tag starts `Publish to PyPI`. That workflow checks the tag against `scripts.__version__`, builds with `build==1.5.0`, validates with `twine==7.0.0`, and publishes through the `pypi` Trusted Publisher environment.

When the workflow is green:

```bash
curl -fsSL https://pypi.org/pypi/unslop/json | python3 -c \
  'import json,sys; print(json.load(sys.stdin)["info"]["version"])'
python3 -m venv /tmp/unslop-release-check
/tmp/unslop-release-check/bin/pip install unslop==X.Y.Z
/tmp/unslop-release-check/bin/unslop --version
gh release create unslop-vX.Y.Z --verify-tag --title "unslop X.Y.Z" --generate-notes
```

Use a new temporary directory for each release check if `/tmp/unslop-release-check` already exists.

## Host distribution

- **Claude Code:** `.claude-plugin/marketplace.json` is served from the GitHub repository. Check that its version and source resolve at the final tag.
- **Cursor:** test the repository through `~/.cursor/plugins/local/unslop`. Public listing and updates require the signed-in publisher flow at <https://cursor.com/marketplace/publish>; Cursor manually reviews each submission and update.
- **OpenAI Codex / ChatGPT:** run the plugin-creator validator on `plugins/unslop/`, add the repository marketplace with `codex plugin marketplace add`, then install `unslop@unslop-agents-marketplace` in a disposable test source. Public listing requires the universal plugin submission flow at <https://developers.openai.com/plugins/deploy/submission>.
- **Gemini CLI:** `gemini-extension.json` is source-distributed. Clone the final tag and run `gemini extensions install ./` for a clean smoke test. Add the `gemini-cli-extension` GitHub topic so Gemini's crawler can discover tagged releases.
- **Agents, Windsurf, Cline, and Copilot:** these are repository manifests or generated instruction mirrors. Verify their paths on final `main`; there is no separate registry in this repo.
- **npm:** no npm package is published. `hooks/package.json` only fixes Node's CommonJS module mode.
- **Containers:** the Dockerfile is a build path, not a published image. No container registry action is configured.

Record any manual marketplace submission still awaiting review in the release handoff. Never describe a listing as live until its public page resolves.
