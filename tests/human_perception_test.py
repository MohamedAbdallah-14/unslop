"""Human-perception naturalness test for the Unslop deterministic mode.

Tests across three real-world domains: resume bullets, Slack messages,
and professional emails. Measures quantitative metrics (burstiness,
vocabulary diversity, sentence length variance) and outputs before/after
pairs for LLM-as-judge evaluation.
"""

import json
import math
import re
import statistics
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "unslop"))
from scripts.humanize import humanize_deterministic

# --------------- Test Samples ---------------

SAMPLES = {
    "resume": {
        "label": "Resume / LinkedIn Bullets",
        "texts": [
            (
                "Spearheaded a comprehensive overhaul of the data pipeline, "
                "leveraging cutting-edge technologies to create a robust and "
                "seamless integration with downstream systems. Furthermore, "
                "this pivotal initiative resulted in a 40% reduction in "
                "processing time and a holistic improvement in data quality."
            ),
            (
                "Embarked on a journey to navigate the complex landscape of "
                "cloud migration, delving into state-of-the-art solutions to "
                "ensure a seamless transition. It's worth mentioning that this "
                "comprehensive effort resulted in $200K annual savings."
            ),
            (
                "Led a pivotal project to leverage machine learning for fraud "
                "detection. The robust system seamlessly processes 10M+ "
                "transactions daily. Additionally, the cutting-edge approach "
                "reduced false positives by 60%, a testament to the team's "
                "holistic understanding of the problem domain."
            ),
            (
                "Navigated the complex landscape of regulatory compliance, "
                "comprehensively auditing existing processes. At its core, "
                "this initiative leveraged automation to create a robust "
                "framework. The seamless integration with existing workflows "
                "resulted in paramount improvements to audit readiness."
            ),
        ],
    },
    "slack": {
        "label": "Slack / Team Chat Messages",
        "texts": [
            (
                "Great question! I'd be happy to help with that. It's important "
                "to note that the deployment pipeline leverages a robust CI/CD "
                "framework. Furthermore, the seamless integration with our "
                "monitoring stack provides a comprehensive view of system health. "
                "In essence, you just need to push to main and the rest is automated."
            ),
            (
                "Certainly! The PR looks good. However, it's worth mentioning "
                "that we should delve into the error handling a bit more. "
                "Additionally, the holistic approach to testing could be more "
                "comprehensive. Generally speaking, I'd suggest adding edge "
                "case tests before merging."
            ),
            (
                "Absolutely! I've been navigating through the codebase and the "
                "state-of-the-art authentication module is a testament to great "
                "engineering. However, the seamless integration with the legacy "
                "system is paramount. To summarize, I think we need another "
                "sprint to get this across the finish line."
            ),
            (
                "Wonderful question! At its core, the issue is that our "
                "cutting-edge microservices architecture creates a complex "
                "tapestry of dependencies. It's important to note that "
                "leveraging service mesh would provide a holistic solution. "
                "Furthermore, this comprehensive approach would seamlessly "
                "address the latency concerns."
            ),
        ],
    },
    "email": {
        "label": "Professional Emails",
        "texts": [
            (
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
            (
                "Thank you for the comprehensive feedback on the proposal. "
                "Certainly, your insights are a testament to your deep "
                "understanding of the landscape. At its core, our approach "
                "leverages robust automation to navigate the complex regulatory "
                "environment.\n\n"
                "Additionally, it's important to note that the cutting-edge "
                "compliance framework provides a holistic view of risk. "
                "Furthermore, the seamless integration with existing systems "
                "is paramount. Generally speaking, we believe this comprehensive "
                "solution addresses all the pivotal concerns you raised."
            ),
            (
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
        ],
    },
}


# --------------- Quantitative Metrics ---------------

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD_SPLIT = re.compile(r"\s+")
_CONTRACTION = re.compile(r"\b\w+'\w+\b")


def sentence_lengths(text):
    sents = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
    return [len(_WORD_SPLIT.split(s)) for s in sents]


def burstiness_index(lengths):
    """Coefficient of variation of sentence lengths. Higher = more human."""
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return statistics.stdev(lengths) / mean


def vocab_diversity(text):
    """Type-token ratio. Higher = richer vocabulary."""
    words = [w.lower() for w in _WORD_SPLIT.split(text) if w.strip()]
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def contraction_rate(text):
    """Contractions per 100 words. Humans use more contractions."""
    words = _WORD_SPLIT.split(text)
    contractions = _CONTRACTION.findall(text)
    if not words:
        return 0.0
    return len(contractions) / len(words) * 100


def avg_sentence_length(text):
    lengths = sentence_lengths(text)
    return statistics.mean(lengths) if lengths else 0


def max_min_spread(text):
    """Difference between longest and shortest sentence (in words)."""
    lengths = sentence_lengths(text)
    if len(lengths) < 2:
        return 0
    return max(lengths) - min(lengths)


# --------------- AI-ism residual scan ---------------

AI_MARKERS = [
    "delve", "tapestry", "testament", "navigate", "embark", "journey",
    "realm", "landscape", "pivotal", "paramount", "seamless", "seamlessly",
    "holistic", "holistically", "leverage", "leverages", "leveraged",
    "leveraging", "cutting-edge", "state-of-the-art", "comprehensive",
    "comprehensively", "robust", "furthermore", "moreover", "additionally",
    "in essence", "at its core", "it's important to note",
    "it's worth mentioning", "generally speaking", "to summarize",
    "in conclusion", "firstly", "secondly", "thirdly",
    "great question", "certainly!", "absolutely!", "i'd be happy to help",
    "i hope this email finds you well",
]


def residual_ai_markers(text):
    """Count remaining AI markers in humanized text."""
    low = text.lower()
    found = []
    for marker in AI_MARKERS:
        if marker in low:
            found.append(marker)
    return found


# --------------- Main ---------------

def analyze_pair(label, original, humanized):
    """Compute metrics for an original/humanized pair."""
    orig_lens = sentence_lengths(original)
    hum_lens = sentence_lengths(humanized)

    return {
        "original": {
            "text": original,
            "word_count": len(_WORD_SPLIT.split(original)),
            "sentence_count": len(orig_lens),
            "avg_sentence_len": round(avg_sentence_length(original), 1),
            "burstiness": round(burstiness_index(orig_lens), 3),
            "vocab_diversity": round(vocab_diversity(original), 3),
            "contraction_rate": round(contraction_rate(original), 2),
            "max_min_spread": max_min_spread(original),
        },
        "humanized": {
            "text": humanized,
            "word_count": len(_WORD_SPLIT.split(humanized)),
            "sentence_count": len(hum_lens),
            "avg_sentence_len": round(avg_sentence_length(humanized), 1),
            "burstiness": round(burstiness_index(hum_lens), 3),
            "vocab_diversity": round(vocab_diversity(humanized), 3),
            "contraction_rate": round(contraction_rate(humanized), 2),
            "max_min_spread": max_min_spread(humanized),
            "residual_markers": residual_ai_markers(humanized),
        },
    }


def main():
    all_results = {}
    all_orig_burstiness = []
    all_hum_burstiness = []
    all_residuals = []

    for domain, data in SAMPLES.items():
        print("=" * 70)
        print("DOMAIN: {}".format(data["label"]))
        print("=" * 70)
        print()

        domain_results = []
        for i, text in enumerate(data["texts"]):
            humanized = humanize_deterministic(text)
            result = analyze_pair(
                "{} #{}".format(data["label"], i + 1),
                text, humanized,
            )
            domain_results.append(result)

            all_orig_burstiness.append(result["original"]["burstiness"])
            all_hum_burstiness.append(result["humanized"]["burstiness"])
            all_residuals.extend(result["humanized"]["residual_markers"])

            print("--- Sample {} ---".format(i + 1))
            print()
            print("BEFORE:")
            print(text)
            print()
            print("AFTER:")
            print(humanized)
            print()

            row = "{:<22} {:>10} {:>10} {:>10}"
            print(row.format("Metric", "Before", "After", "Change"))
            print("-" * 55)
            o = result["original"]
            h = result["humanized"]
            print(row.format("Words", str(o["word_count"]), str(h["word_count"]),
                             "{:+d}".format(h["word_count"] - o["word_count"])))
            print(row.format("Sentences", str(o["sentence_count"]), str(h["sentence_count"]),
                             "{:+d}".format(h["sentence_count"] - o["sentence_count"])))
            print(row.format("Avg sent length", str(o["avg_sentence_len"]), str(h["avg_sentence_len"]),
                             "{:+.1f}".format(h["avg_sentence_len"] - o["avg_sentence_len"])))
            print(row.format("Burstiness", str(o["burstiness"]), str(h["burstiness"]),
                             "{:+.3f}".format(h["burstiness"] - o["burstiness"])))
            print(row.format("Vocab diversity", str(o["vocab_diversity"]), str(h["vocab_diversity"]),
                             "{:+.3f}".format(h["vocab_diversity"] - o["vocab_diversity"])))
            print(row.format("Contractions/100w", str(o["contraction_rate"]), str(h["contraction_rate"]),
                             "{:+.2f}".format(h["contraction_rate"] - o["contraction_rate"])))
            print(row.format("Sent length spread", str(o["max_min_spread"]), str(h["max_min_spread"]),
                             "{:+d}".format(h["max_min_spread"] - o["max_min_spread"])))

            residuals = result["humanized"]["residual_markers"]
            if residuals:
                print()
                print("  RESIDUAL AI MARKERS: {}".format(", ".join(residuals)))
            else:
                print()
                print("  RESIDUAL AI MARKERS: none")
            print()

        all_results[domain] = domain_results

    # --------------- Summary ---------------
    print()
    print("=" * 70)
    print("AGGREGATE SUMMARY")
    print("=" * 70)
    print()

    total_samples = sum(len(d) for d in all_results.values())
    avg_orig_burst = statistics.mean(all_orig_burstiness) if all_orig_burstiness else 0
    avg_hum_burst = statistics.mean(all_hum_burstiness) if all_hum_burstiness else 0

    print("Total samples tested: {}".format(total_samples))
    print("Avg burstiness  BEFORE: {:.3f}".format(avg_orig_burst))
    print("Avg burstiness  AFTER:  {:.3f}".format(avg_hum_burst))
    burst_change = avg_hum_burst - avg_orig_burst
    print("Burstiness change:      {:+.3f} ({})".format(
        burst_change,
        "more varied" if burst_change > 0 else "less varied" if burst_change < 0 else "unchanged"
    ))
    print()

    if all_residuals:
        from collections import Counter
        counts = Counter(all_residuals)
        print("Residual AI markers still present ({} total):".format(len(all_residuals)))
        for marker, count in counts.most_common():
            print("  {:30s} x{}".format(marker, count))
    else:
        print("No residual AI markers detected in any sample.")

    print()

    # Write JSON for sub-agent consumption
    output_path = os.path.join(os.path.dirname(__file__), "human_perception_results.json")
    json_output = {}
    for domain, results in all_results.items():
        domain_pairs = []
        for r in results:
            domain_pairs.append({
                "original": r["original"]["text"],
                "humanized": r["humanized"]["text"],
                "metrics": {
                    "burstiness_before": r["original"]["burstiness"],
                    "burstiness_after": r["humanized"]["burstiness"],
                    "vocab_div_before": r["original"]["vocab_diversity"],
                    "vocab_div_after": r["humanized"]["vocab_diversity"],
                    "residual_markers": r["humanized"]["residual_markers"],
                },
            })
        json_output[domain] = {
            "label": SAMPLES[domain]["label"],
            "pairs": domain_pairs,
        }

    with open(output_path, "w") as f:
        json.dump(json_output, f, indent=2)
    print("Results written to {}".format(output_path))


if __name__ == "__main__":
    main()
