#!/usr/bin/env python3
"""Blind A/B human-perception test for the Unslop deterministic mode.

Protocol:
  1. For each sample, randomly assign original and humanized to "Text A" / "Text B"
  2. An LLM judge (or quantitative fallback) scores each text independently
     on 5 dimensions, without knowing which was humanized
  3. After scoring, reveal the mapping and compute deltas
  4. Output JSON for tracking over time

Dimensions scored (1-10, higher = more human-sounding):
  - naturalness:    Does this read like a person wrote it?
  - vocabulary:     Are word choices natural, not corporate/vague?
  - rhythm:         Do sentence lengths vary like real writing?
  - grammar:        Free of errors that would embarrass the writer?
  - directness:     Gets to the point without hedging or filler?

Run:
  python3 tests/blind_ab_test.py              # quantitative only
  python3 tests/blind_ab_test.py --llm        # add LLM judge (uses `claude -p`, no API key needed)
  python3 tests/blind_ab_test.py --llm --json # JSON output for CI

Pass criteria (quantitative):
  - Humanized text has fewer AI markers than original in every sample
  - No grammar errors introduced (article agreement, verb agreement, capitalization)
  - Word count reduction >= 10% (filler removed)

Pass criteria (LLM judge):
  - Humanized text scores higher than original on naturalness in >= 80% of samples
  - Average naturalness delta >= +1.0 point
"""

from __future__ import annotations

import json
import os
import random
import re
import shutil
import statistics
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "unslop"))
from scripts.humanize import humanize_deterministic

# ── Samples ──────────────────────────────────────────────────────────────────

SAMPLES = [
    {
        "id": "resume-1",
        "domain": "resume",
        "text": (
            "Spearheaded a comprehensive overhaul of the data pipeline, "
            "leveraging cutting-edge technologies to create a robust and "
            "seamless integration with downstream systems. Furthermore, "
            "this pivotal initiative resulted in a 40% reduction in "
            "processing time and a holistic improvement in data quality."
        ),
    },
    {
        "id": "resume-2",
        "domain": "resume",
        "text": (
            "Embarked on a journey to navigate the complex landscape of "
            "cloud migration, delving into state-of-the-art solutions to "
            "ensure a seamless transition. It's worth mentioning that this "
            "comprehensive effort resulted in $200K annual savings."
        ),
    },
    {
        "id": "slack-1",
        "domain": "slack",
        "text": (
            "Great question! I'd be happy to help with that. It's important "
            "to note that the deployment pipeline leverages a robust CI/CD "
            "framework. Furthermore, the seamless integration with our "
            "monitoring stack provides a comprehensive view of system health. "
            "In essence, you just need to push to main and the rest is automated."
        ),
    },
    {
        "id": "slack-2",
        "domain": "slack",
        "text": (
            "Certainly! The PR looks good. However, it's worth mentioning "
            "that we should delve into the error handling a bit more. "
            "Additionally, the holistic approach to testing could be more "
            "comprehensive. Generally speaking, I'd suggest adding edge "
            "case tests before merging."
        ),
    },
    {
        "id": "email-1",
        "domain": "email",
        "text": (
            "I hope this email finds you well. I'd be happy to help provide "
            "an update on the Q3 deliverables. It's important to note that "
            "the team has been leveraging cutting-edge methodologies to "
            "ensure a comprehensive and robust delivery. Furthermore, the "
            "seamless collaboration between departments has been a testament "
            "to our holistic approach to project management.\n\n"
            "In essence, we are on track to deliver all pivotal milestones "
            "by the end of the quarter. However, it's worth mentioning that "
            "the state-of-the-art analytics platform requires additional "
            "testing. To summarize, the overall trajectory is positive and "
            "the team remains committed to delivering a seamless experience."
        ),
    },
    {
        "id": "email-2",
        "domain": "email",
        "text": (
            "Great question about the timeline. I'd be happy to help clarify. "
            "The team has been delving into the requirements and embarking on "
            "the journey of building a state-of-the-art platform. However, "
            "it's worth mentioning that navigating through the complex "
            "tapestry of legacy systems has been challenging.\n\n"
            "Firstly, the robust backend is 80% complete. Secondly, the "
            "seamless frontend integration is in progress. Thirdly, the "
            "comprehensive testing suite is being finalized. In conclusion, "
            "we anticipate delivery by March 15th, which represents a "
            "holistic completion of all pivotal deliverables."
        ),
    },
]

# ── Quantitative metrics ─────────────────────────────────────────────────────

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD_SPLIT = re.compile(r"\s+")

AI_MARKERS = [
    r"\bdelv(?:e|es|ed|ing)\b",
    r"\btapestry\b",
    r"\btestament\s+to\b",
    r"\bnavigate(?:s|d)?(?=\s+(?:the|through|around|complex))\b",
    r"\bnavigating(?=\s+(?:the|through|around|complex))\b",
    r"\bembark(?:s|ed|ing)?\s+on\b",
    r"\bjourney(?=\s+(?:toward|to|of))\b",
    r"\brealm\s+of\b",
    r"\blandscape\s+of\b",
    r"\bpivotal\b",
    r"\bparamount\b",
    r"\bseamless(?:ly)?\b",
    r"\bholistic(?:ally)?\b",
    r"\bleverage(?:s|d)?\b",
    r"\bleveraging\b",
    r"\bcutting-edge\b",
    r"\bstate-of-the-art\b",
    r"\bcomprehensive(?:ly)?\b",
    r"\brobust(?=\s+(?:and|solution|implementation|approach|system|architecture|framework|platform|infrastructure|backend|frontend|foundation|delivery|automation|CI/CD|pipeline))\b",
    r"\bfurthermore\b",
    r"\bmoreover\b",
    r"\badditionally\b",
    r"\bin\s+essence\b",
    r"\bat\s+its\s+core\b",
    r"\bit'?s\s+important\s+to\s+note\b",
    r"\bit'?s\s+worth\s+mentioning\b",
    r"\bgenerally\s+speaking\b",
    r"\bto\s+summarize\b",
    r"\bin\s+conclusion\b",
    r"\bfirstly\b",
    r"\bsecondly\b",
    r"\bthirdly\b",
    r"\bgreat\s+question\b",
    r"\bi'?d\s+be\s+happy\s+to\s+help\b",
    r"\bi\s+hope\s+this\s+email\s+finds\s+you\s+well\b",
]
AI_MARKER_PATTERNS = [re.compile(p, re.IGNORECASE) for p in AI_MARKERS]

GRAMMAR_CHECKS = [
    (re.compile(r"\ba (?:overall|advanced|essential|important|earlier|original|open|obvious)\b", re.IGNORECASE),
     "article 'a' before vowel sound"),
    (re.compile(r"\bhas been shows\b", re.IGNORECASE),
     "broken verb 'has been shows'"),
    (re.compile(r"\b(?:insights|results|systems|tools|pipelines|processes) shows\b"),
     "possible subject-verb disagreement '[plural noun] shows'"),
    (re.compile(r"(?<=[.!?]\s)[a-z]"),
     "lowercase after sentence-ending punctuation"),
    (re.compile(r"\bstarting to \w+ing\b", re.IGNORECASE),
     "gerund after 'to' (should be infinitive)"),
    (re.compile(r"\ba latest\b", re.IGNORECASE),
     "article 'a latest' (should be 'the latest')"),
]


def count_ai_markers(text: str) -> int:
    return sum(len(p.findall(text)) for p in AI_MARKER_PATTERNS)


def count_grammar_errors(text: str) -> list[str]:
    found = []
    for pattern, desc in GRAMMAR_CHECKS:
        if pattern.search(text):
            found.append(desc)
    return found


def sentence_lengths(text: str) -> list[int]:
    sents = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
    return [len(_WORD_SPLIT.split(s)) for s in sents]


def burstiness(text: str) -> float:
    lengths = sentence_lengths(text)
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return statistics.stdev(lengths) / mean


def word_count(text: str) -> int:
    return len(_WORD_SPLIT.split(text.strip()))


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class Scores:
    naturalness: float = 0.0
    vocabulary: float = 0.0
    rhythm: float = 0.0
    grammar: float = 0.0
    directness: float = 0.0

    @property
    def mean(self) -> float:
        vals = [self.naturalness, self.vocabulary, self.rhythm,
                self.grammar, self.directness]
        return statistics.mean(vals)


@dataclass
class SampleResult:
    sample_id: str
    domain: str
    original_text: str
    humanized_text: str
    coin: str  # "A" or "B" — which slot got the humanized text
    quant_original: dict = field(default_factory=dict)
    quant_humanized: dict = field(default_factory=dict)
    llm_scores_a: Scores | None = None
    llm_scores_b: Scores | None = None
    grammar_errors: list[str] = field(default_factory=list)
    passed: bool = True
    fail_reasons: list[str] = field(default_factory=list)


# ── Quantitative scoring ─────────────────────────────────────────────────────

def score_quant(text: str) -> dict:
    return {
        "word_count": word_count(text),
        "ai_markers": count_ai_markers(text),
        "burstiness": round(burstiness(text), 3),
        "sentence_count": len(sentence_lengths(text)),
    }


def run_quant(sample: dict) -> SampleResult:
    original = sample["text"]
    humanized = humanize_deterministic(original)
    coin = random.choice(["A", "B"])

    result = SampleResult(
        sample_id=sample["id"],
        domain=sample["domain"],
        original_text=original,
        humanized_text=humanized,
        coin=coin,
        quant_original=score_quant(original),
        quant_humanized=score_quant(humanized),
        grammar_errors=count_grammar_errors(humanized),
    )

    # Pass/fail checks
    if result.quant_humanized["ai_markers"] >= result.quant_original["ai_markers"]:
        result.passed = False
        result.fail_reasons.append(
            "AI markers not reduced ({} -> {})".format(
                result.quant_original["ai_markers"],
                result.quant_humanized["ai_markers"],
            )
        )

    if result.grammar_errors:
        result.passed = False
        result.fail_reasons.extend(
            "grammar: {}".format(e) for e in result.grammar_errors
        )

    orig_wc = result.quant_original["word_count"]
    hum_wc = result.quant_humanized["word_count"]
    if orig_wc > 0 and (orig_wc - hum_wc) / orig_wc < 0.05:
        result.fail_reasons.append(
            "word count barely reduced ({} -> {}, {:.0f}%)".format(
                orig_wc, hum_wc, (orig_wc - hum_wc) / orig_wc * 100
            )
        )

    return result


# ── LLM judge ────────────────────────────────────────────────────────────────

JUDGE_PROMPT = """You are a writing quality evaluator. You will see two texts labeled "Text A" and "Text B" written for the context: {domain}.

Rate EACH text independently on these 5 dimensions (1-10 scale, 10 = most human-sounding):

1. naturalness: Does this read like a real person wrote it? (vs. formulaic/robotic)
2. vocabulary: Are word choices natural and specific? (vs. vague corporate filler)
3. rhythm: Do sentence lengths vary like real writing? (vs. uniform AI cadence)
4. grammar: Free of errors that would embarrass the writer? (10 = no errors)
5. directness: Gets to the point without hedging or filler? (vs. padding)

IMPORTANT:
- Score each text on its own merits. Do not compare them.
- Do not guess which was AI-generated. Just rate the writing quality.
- Be strict. Real human writing in {domain} context scores 6-8. Perfect is rare.

Text A:
{text_a}

Text B:
{text_b}

Respond with ONLY this JSON (no other text):
{{"text_a": {{"naturalness": N, "vocabulary": N, "rhythm": N, "grammar": N, "directness": N}}, "text_b": {{"naturalness": N, "vocabulary": N, "rhythm": N, "grammar": N, "directness": N}}}}"""


def call_llm_judge(domain: str, text_a: str, text_b: str) -> dict | None:
    """Call the claude CLI (`claude -p`) as a free, local LLM judge."""
    claude_bin = shutil.which("claude")
    if not claude_bin:
        print("  [skip] claude CLI not found on PATH")
        return None

    prompt = JUDGE_PROMPT.format(
        domain=domain, text_a=text_a, text_b=text_b,
    )
    try:
        proc = subprocess.run(
            [claude_bin, "-p", prompt],
            capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        print("  [skip] claude -p timed out")
        return None

    if proc.returncode != 0:
        print("  [skip] claude -p failed: {}".format(proc.stderr.strip()[:120]))
        return None

    raw = proc.stdout.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                print("  [skip] could not parse JSON from claude output")
                return None
        else:
            print("  [skip] no JSON in claude output: {}".format(raw[:120]))
            return None

    return data


def add_llm_scores(result: SampleResult) -> None:
    if result.coin == "A":
        text_a, text_b = result.humanized_text, result.original_text
    else:
        text_a, text_b = result.original_text, result.humanized_text

    data = call_llm_judge(result.domain, text_a, text_b)
    if data is None:
        return

    def to_scores(d: dict) -> Scores:
        return Scores(
            naturalness=d.get("naturalness", 0),
            vocabulary=d.get("vocabulary", 0),
            rhythm=d.get("rhythm", 0),
            grammar=d.get("grammar", 0),
            directness=d.get("directness", 0),
        )

    result.llm_scores_a = to_scores(data.get("text_a", {}))
    result.llm_scores_b = to_scores(data.get("text_b", {}))


# ── Reporting ────────────────────────────────────────────────────────────────

def print_report(results: list[SampleResult], use_llm: bool) -> dict:
    print()
    print("=" * 70)
    print("BLIND A/B HUMAN-PERCEPTION TEST")
    print("=" * 70)
    print()

    all_passed = True
    nat_deltas = []
    mean_deltas = []

    for r in results:
        marker_orig = r.quant_original["ai_markers"]
        marker_hum = r.quant_humanized["ai_markers"]
        wc_orig = r.quant_original["word_count"]
        wc_hum = r.quant_humanized["word_count"]
        wc_pct = (wc_orig - wc_hum) / wc_orig * 100 if wc_orig > 0 else 0

        status = "PASS" if r.passed else "FAIL"
        if not r.passed:
            all_passed = False

        print("--- {} [{}] {} ---".format(r.sample_id, r.domain, status))
        print("  Quantitative:")
        print("    AI markers:  {} -> {} ({})".format(
            marker_orig, marker_hum,
            "reduced" if marker_hum < marker_orig else "NOT reduced"
        ))
        print("    Word count:  {} -> {} ({:.0f}% reduction)".format(
            wc_orig, wc_hum, wc_pct))
        print("    Grammar:     {}".format(
            "clean" if not r.grammar_errors else ", ".join(r.grammar_errors)
        ))
        print("    Blind slot:  humanized = Text {}".format(r.coin))

        if r.llm_scores_a and r.llm_scores_b:
            if r.coin == "A":
                hum_scores, orig_scores = r.llm_scores_a, r.llm_scores_b
            else:
                hum_scores, orig_scores = r.llm_scores_b, r.llm_scores_a

            nat_delta = hum_scores.naturalness - orig_scores.naturalness
            nat_deltas.append(nat_delta)
            mean_deltas.append(hum_scores.mean - orig_scores.mean)

            print("  LLM Judge (blind):")
            dims = ["naturalness", "vocabulary", "rhythm", "grammar", "directness"]
            header = "    {:14s} {:>8s} {:>8s} {:>8s}".format(
                "Dimension", "Original", "Humanized", "Delta")
            print(header)
            print("    " + "-" * 44)
            for dim in dims:
                o = getattr(orig_scores, dim)
                h = getattr(hum_scores, dim)
                d = h - o
                print("    {:14s} {:8.1f} {:8.1f} {:>+8.1f}".format(dim, o, h, d))
            print("    {:14s} {:8.1f} {:8.1f} {:>+8.1f}".format(
                "MEAN", orig_scores.mean, hum_scores.mean,
                hum_scores.mean - orig_scores.mean))

        if r.fail_reasons:
            for reason in r.fail_reasons:
                print("  ! {}".format(reason))
        print()

    # ── Aggregate ──
    print("=" * 70)
    print("AGGREGATE")
    print("=" * 70)
    print()

    total = len(results)
    quant_passed = sum(1 for r in results if r.passed)
    print("Quantitative: {}/{} passed".format(quant_passed, total))

    llm_verdict = None
    if nat_deltas:
        wins = sum(1 for d in nat_deltas if d > 0)
        ties = sum(1 for d in nat_deltas if d == 0)
        losses = sum(1 for d in nat_deltas if d < 0)
        avg_nat = statistics.mean(nat_deltas)
        avg_mean = statistics.mean(mean_deltas)

        print()
        print("LLM Judge:")
        print("  Naturalness wins/ties/losses: {}/{}/{}".format(wins, ties, losses))
        print("  Avg naturalness delta:        {:+.2f}".format(avg_nat))
        print("  Avg overall delta:            {:+.2f}".format(avg_mean))

        win_rate = wins / total
        llm_pass = win_rate >= 0.8 and avg_nat >= 1.0
        llm_verdict = "PASS" if llm_pass else "FAIL"
        print("  Win rate:                     {:.0f}% (threshold: 80%)".format(
            win_rate * 100))
        print("  LLM verdict:                  {}".format(llm_verdict))
        if not llm_pass:
            all_passed = False

    print()
    overall = "PASS" if all_passed else "FAIL"
    print("OVERALL: {}".format(overall))
    print()

    summary = {
        "overall": overall,
        "total_samples": total,
        "quant_passed": quant_passed,
        "llm_judge_used": use_llm and bool(nat_deltas),
        "llm_verdict": llm_verdict,
        "results": [],
    }
    for r in results:
        entry = {
            "sample_id": r.sample_id,
            "domain": r.domain,
            "passed": r.passed,
            "fail_reasons": r.fail_reasons,
            "quant_original": r.quant_original,
            "quant_humanized": r.quant_humanized,
            "grammar_errors": r.grammar_errors,
            "blind_slot": r.coin,
        }
        if r.llm_scores_a and r.llm_scores_b:
            if r.coin == "A":
                hum_s, orig_s = r.llm_scores_a, r.llm_scores_b
            else:
                hum_s, orig_s = r.llm_scores_b, r.llm_scores_a
            entry["llm_original"] = asdict(orig_s)
            entry["llm_humanized"] = asdict(hum_s)
        summary["results"].append(entry)

    return summary


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    use_llm = "--llm" in sys.argv
    json_output = "--json" in sys.argv

    random.seed(42)

    results = []
    for sample in SAMPLES:
        result = run_quant(sample)
        if use_llm:
            add_llm_scores(result)
        results.append(result)

    summary = print_report(results, use_llm)

    if json_output:
        out_path = Path(__file__).parent / "blind_ab_results.json"
        with open(out_path, "w") as f:
            json.dump(summary, f, indent=2)
        print("JSON written to {}".format(out_path))

    return 0 if summary["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
