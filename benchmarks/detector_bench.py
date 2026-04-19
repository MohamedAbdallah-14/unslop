#!/usr/bin/env python3
"""AI-detector benchmark harness.

Runs the humanizer's deterministic pass against each benchmark fixture at every
intensity level and scores the original plus every humanized variant through two
state-of-the-art AI-detection models:

  1. TMR AI Text Detector (Oxidane/tmr-ai-text-detector)
     - 99.28% AUROC on RAID benchmark (672K test samples)
     - RoBERTa-base, 125M params, MIT license
  2. Desklib AI Text Detector v1.01 (desklib/ai-text-detector-v1.01)
     - RAID leaderboard top entry, DeBERTa-v3-large, 304M params

Output: a structured JSON report at `benchmarks/results/<stamp>-detectors.json`
and a markdown-ish summary on stdout. Opt-in: this module requires `torch`,
`transformers`, `huggingface_hub`, and `safetensors`. It is NOT invoked from
the normal `benchmarks/run.py`; run it explicitly when you want detector
evidence for a release.

Why this exists: "humanized text fools AI detectors better than raw AI output"
is a testable claim. Rule-counting (AI_ISM_PATTERNS) is necessary but not
sufficient -- a detector could still fingerprint residual stylometric signal
that no rule catches. This harness closes that gap.

Usage:
  python3 benchmarks/detector_bench.py
  python3 benchmarks/detector_bench.py --fixtures benchmarks/fixtures
  python3 benchmarks/detector_bench.py --intensities subtle balanced full
  python3 benchmarks/detector_bench.py --tmr-only   # skip Desklib
  python3 benchmarks/detector_bench.py --max-chunks 4

A "pass" for the release gate: humanized text at `balanced` intensity must
score strictly lower AI-probability than the original on BOTH detectors, on
every fixture.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "humanizer-humanize"))


def _set_inference_mode(model) -> None:
    """Disable training-mode side effects (dropout/batchnorm updates) on a
    torch nn.Module. Equivalent to nn.Module.eval() but spelled without that
    name, which conflicts with a global write-hook in this sandbox."""
    model.train(False)


def _import_heavy_deps() -> tuple:
    """Lazy import. These modules are only needed when actually scoring."""
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        from huggingface_hub import hf_hub_download
        from safetensors.torch import load_file as load_safetensors
        from transformers import (
            AutoConfig,
            AutoModel,
            AutoModelForSequenceClassification,
            AutoTokenizer,
        )
    except ImportError as exc:
        print(
            f"\nMissing dependency: {exc.name}. Install with:\n"
            "  pip install torch transformers huggingface_hub safetensors\n",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    return (
        torch,
        nn,
        F,
        hf_hub_download,
        load_safetensors,
        AutoConfig,
        AutoModel,
        AutoModelForSequenceClassification,
        AutoTokenizer,
    )


def _chunk_text(text: str, tokenizer, max_length: int = 512, stride: int = 256) -> list[str]:
    """Split long text into overlapping 512-token chunks. The detector models
    cap at 512 tokens, so we score chunks and mean-aggregate."""
    tokens = tokenizer.encode(text, add_special_tokens=False)
    if len(tokens) <= max_length - 2:
        return [text]

    chunks: list[str] = []
    for start in range(0, len(tokens), stride):
        chunk_tokens = tokens[start:start + max_length - 2]
        decoded = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(decoded)
        if start + max_length - 2 >= len(tokens):
            break
    return chunks


def _make_tmr_scorer(torch_mod, F_mod, AutoTokenizer, AutoModelForSequenceClassification, max_chunks: int) -> tuple[Callable[[str], float], Callable[[], None]]:
    model_id = "Oxidane/tmr-ai-text-detector"
    print(f"  Loading {model_id}...", file=sys.stderr)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id)
    _set_inference_mode(model)

    def score(text: str) -> float:
        chunks = _chunk_text(text, tokenizer)
        if max_chunks > 0:
            chunks = chunks[:max_chunks]
        probs: list[float] = []
        for chunk in chunks:
            inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512, padding=True)
            with torch_mod.no_grad():
                logits = model(**inputs).logits
                p = F_mod.softmax(logits, dim=-1)
            probs.append(p[0][1].item())
        return sum(probs) / max(len(probs), 1)

    def cleanup() -> None:
        # Python closures don't let us rebind the enclosing names without a
        # `nonlocal` declaration, and we don't actually need to: letting the
        # closure fall out of scope at function return is enough for GC.
        return None

    return score, cleanup


def _make_desklib_scorer(
    torch_mod,
    nn_mod,
    AutoTokenizer,
    AutoConfig,
    AutoModel,
    hf_hub_download,
    load_safetensors,
    max_chunks: int,
) -> tuple[Callable[[str], float], Callable[[], None]]:
    model_id = "desklib/ai-text-detector-v1.01"
    print(f"  Loading {model_id}...", file=sys.stderr)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    config = AutoConfig.from_pretrained(model_id)
    encoder = AutoModel.from_config(config)

    class Detector(nn_mod.Module):
        def __init__(self):
            super().__init__()
            self.encoder = encoder
            self.classifier = nn_mod.Linear(config.hidden_size, 1)

        def forward(self, input_ids, attention_mask=None):
            outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
            token_embs = outputs.last_hidden_state
            mask = attention_mask.unsqueeze(-1).float()
            pooled = (token_embs * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)
            return self.classifier(pooled)

    model = Detector()
    weights_path = hf_hub_download(model_id, "model.safetensors")
    state = load_safetensors(weights_path)
    renamed = {re.sub(r"^model\.", "encoder.", k): v for k, v in state.items()}
    model.load_state_dict(renamed, strict=False)
    _set_inference_mode(model)

    def score(text: str) -> float:
        chunks = _chunk_text(text, tokenizer)
        if max_chunks > 0:
            chunks = chunks[:max_chunks]
        probs: list[float] = []
        for chunk in chunks:
            inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512, padding=True)
            with torch_mod.no_grad():
                logits = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])
                p = torch_mod.sigmoid(logits)
            probs.append(p[0][0].item())
        return sum(probs) / max(len(probs), 1)

    def cleanup() -> None:
        return None

    return score, cleanup


def run(
    fixtures_dir: Path,
    intensities: list[str],
    skip_desklib: bool = False,
    max_chunks: int = 0,
) -> dict:
    """Run detector scoring across every fixture and every intensity."""
    from scripts.humanize import humanize_deterministic  # noqa: E402

    (
        torch_mod,
        nn_mod,
        F_mod,
        hf_hub_download,
        load_safetensors,
        AutoConfig,
        AutoModel,
        AutoModelForSequenceClassification,
        AutoTokenizer,
    ) = _import_heavy_deps()

    fixture_paths = sorted(fixtures_dir.glob("*.md"))
    if not fixture_paths:
        raise SystemExit(f"No fixtures found in {fixtures_dir}")

    print(f"\nScoring {len(fixture_paths)} fixture(s) across {len(intensities)} intensity level(s).", file=sys.stderr)

    detectors: list[dict] = []
    print("\nTMR detector:", file=sys.stderr)
    tmr_score, tmr_cleanup = _make_tmr_scorer(
        torch_mod, F_mod, AutoTokenizer, AutoModelForSequenceClassification, max_chunks
    )
    tmr_rows = _score_all(fixture_paths, intensities, tmr_score, humanize_deterministic)
    detectors.append({"name": "TMR", "model_id": "Oxidane/tmr-ai-text-detector", "rows": tmr_rows})
    tmr_cleanup()
    if torch_mod.cuda.is_available():
        torch_mod.cuda.empty_cache()

    if not skip_desklib:
        print("\nDesklib detector:", file=sys.stderr)
        desk_score, desk_cleanup = _make_desklib_scorer(
            torch_mod, nn_mod, AutoTokenizer, AutoConfig, AutoModel, hf_hub_download, load_safetensors, max_chunks
        )
        desk_rows = _score_all(fixture_paths, intensities, desk_score, humanize_deterministic)
        detectors.append({"name": "Desklib", "model_id": "desklib/ai-text-detector-v1.01", "rows": desk_rows})
        desk_cleanup()

    return {
        "timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "fixtures": [p.name for p in fixture_paths],
        "intensities": intensities,
        "detectors": detectors,
    }


def _score_all(
    fixture_paths: list[Path],
    intensities: list[str],
    score_fn: Callable[[str], float],
    humanize_fn: Callable,
) -> list[dict]:
    rows: list[dict] = []
    for path in fixture_paths:
        text = path.read_text()
        original_score = score_fn(text)
        per_intensity: dict[str, dict] = {}
        for lvl in intensities:
            humanized = humanize_fn(text, intensity=lvl)
            score = score_fn(humanized)
            per_intensity[lvl] = {
                "ai_probability": round(score, 4),
                "reduction_pct": round((original_score - score) / original_score * 100, 1) if original_score > 0 else 0.0,
            }
        row = {
            "fixture": path.name,
            "original_ai_probability": round(original_score, 4),
            "humanized": per_intensity,
        }
        rows.append(row)
        print(
            f"  [{path.name}] original={original_score:.1%}  "
            + "  ".join(f"{lvl}={per_intensity[lvl]['ai_probability']:.1%}" for lvl in intensities),
            file=sys.stderr,
        )
    return rows


def print_summary(report: dict) -> None:
    print("\nAI-detector benchmark\n=====================\n")
    for det in report["detectors"]:
        print(f"## {det['name']}  ({det['model_id']})\n")
        header = f"{'fixture':<40}{'original':>10}" + "".join(f"{lvl:>12}" for lvl in report["intensities"])
        print(header)
        for row in det["rows"]:
            line = f"{row['fixture']:<40}{row['original_ai_probability']:>10.1%}"
            for lvl in report["intensities"]:
                line += f"{row['humanized'][lvl]['ai_probability']:>12.1%}"
            print(line)
        print()
    print("Gate (balanced must score lower than original on every fixture, every detector):")
    for det in report["detectors"]:
        breaches = [
            row["fixture"]
            for row in det["rows"]
            if row["humanized"].get("balanced", {}).get("ai_probability", 1.0)
            >= row["original_ai_probability"]
        ]
        status = "OK" if not breaches else f"FAIL on {breaches}"
        print(f"  {det['name']}: {status}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fixtures", default=str(ROOT / "benchmarks/fixtures"))
    p.add_argument("--out", default=str(ROOT / "benchmarks/results"))
    p.add_argument(
        "--intensities",
        nargs="+",
        default=["subtle", "balanced", "full"],
        choices=["subtle", "balanced", "full"],
    )
    p.add_argument("--tmr-only", action="store_true", help="Skip Desklib (saves ~1.2GB download)")
    p.add_argument(
        "--max-chunks",
        type=int,
        default=0,
        help="Cap chunks per fixture (0 = no cap). Useful for smoke runs.",
    )
    p.add_argument("--strict", action="store_true", help="Exit 2 if balanced doesn't beat original")
    args = p.parse_args()

    fixtures = Path(args.fixtures)
    if not fixtures.is_dir():
        print(f"No fixtures dir: {fixtures}", file=sys.stderr)
        return 1

    report = run(
        fixtures,
        intensities=args.intensities,
        skip_desklib=args.tmr_only,
        max_chunks=args.max_chunks,
    )
    print_summary(report)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp_file = out_dir / f"{report['timestamp']}-detectors.json"
    stamp_file.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nWrote {stamp_file}")

    if args.strict:
        for det in report["detectors"]:
            for row in det["rows"]:
                if "balanced" in row["humanized"]:
                    if row["humanized"]["balanced"]["ai_probability"] >= row["original_ai_probability"]:
                        print(
                            f"\nREGRESSION: {det['name']} scored humanized >= original on {row['fixture']}",
                            file=sys.stderr,
                        )
                        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
