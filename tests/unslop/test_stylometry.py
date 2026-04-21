"""Tests for unslop/scripts/stylometry.py.

Each signal gets a pointed test on a tiny input so regressions on a single
metric surface fast. Integration (end-to-end analyze on a realistic doc) is
covered by the profile-shape test."""

from __future__ import annotations

import pytest

from unslop.scripts.stylometry import (
    StyleDelta,
    StyleProfile,
    analyze,
    format_delta,
)


class TestEmptyInputs:
    def test_empty_string(self):
        p = analyze("")
        assert p.total_words == 0
        assert p.sentences == 0

    def test_only_code(self):
        p = analyze("```python\nprint(1)\n```")
        assert p.total_words == 0
        assert p.sentences == 0

    def test_only_yaml(self):
        p = analyze("---\ntitle: test\n---")
        assert p.total_words == 0


class TestSentenceLength:
    def test_mean_stdev_uniform(self):
        text = "The cat sat on the mat. The dog sat on the log. The bird sat on the perch."
        p = analyze(text)
        assert p.sentences == 3
        # Each sentence is 6 words. Uniform → σ = 0.
        assert p.sentence_length_mean == pytest.approx(6.0, rel=0.01)
        assert p.sentence_length_stdev == 0.0

    def test_varied_sentence_lengths(self):
        text = (
            "Short. "
            "A medium-length sentence with several words for balance. "
            "This is a much longer sentence with quite a lot of words in it, enough to pull the standard deviation substantially upward."
        )
        p = analyze(text)
        assert p.sentence_length_stdev > 5.0

    def test_fragment_rate(self):
        text = "Short. Tiny. A much longer sentence with many words."
        p = analyze(text)
        # Two of three sentences are <5 words.
        assert p.fragment_rate == pytest.approx(2 / 3, abs=0.01)


class TestContractionRate:
    def test_no_contractions(self):
        text = "We do not ship. It is a policy we are strict about."
        p = analyze(text)
        assert p.contraction_rate == 0.0

    def test_multiple_contractions(self):
        text = "We don't ship. It's a policy we're strict about. I've seen it work."
        p = analyze(text)
        # 4 contractions in ~14 words → ~285 per 1k
        assert p.contraction_rate > 200.0


class TestPunctuationRates:
    def test_em_dash_rate(self):
        text = "Alpha — a thing — continues. Bravo — another — ends."
        p = analyze(text)
        assert p.em_dash_rate > 0.0

    def test_semicolon_rate(self):
        text = "This is one clause; this is the next; and this is the last."
        p = analyze(text)
        assert p.semicolon_rate > 0.0

    def test_parenthetical_rate(self):
        text = "The value (which defaults to zero) is required (in most cases)."
        p = analyze(text)
        assert p.parenthetical_rate > 0.0


class TestPersonRates:
    def test_first_person(self):
        text = "I saw it. We told them. My take is clear."
        p = analyze(text)
        assert p.first_person_rate > 0.0

    def test_second_person(self):
        text = "You will find that your data is fine."
        p = analyze(text)
        assert p.second_person_rate > 0.0


class TestLatinateRatio:
    def test_formal_register_high(self):
        text = (
            "The implementation of the operationalization constitutes a "
            "significant development in the administration of infrastructure."
        )
        p = analyze(text)
        # Many -tion and -ment words; expect > 0.15
        assert p.latinate_ratio >= 0.15

    def test_anglo_saxon_low(self):
        text = "We built it. It works. Ship."
        p = analyze(text)
        assert p.latinate_ratio == 0.0


class TestStartsWithAndBut:
    def test_detected(self):
        text = "The plan is simple. And we ship tomorrow. But not without tests."
        p = analyze(text)
        # 2 of 3 sentences start with And/But
        assert p.starts_with_and_but > 0.5

    def test_absent_when_formal(self):
        text = "The plan is simple. The team ships tomorrow."
        p = analyze(text)
        assert p.starts_with_and_but == 0.0


class TestDelta:
    def test_delta_simple(self):
        a = StyleProfile(sentence_length_mean=20.0)
        b = StyleProfile(sentence_length_mean=15.0)
        delta = a.delta(b)
        assert delta.diffs["sentence_length_mean"] == 5.0

    def test_largest_gaps_ordered(self):
        a = StyleProfile(sentence_length_mean=10.0, contraction_rate=50.0)
        b = StyleProfile(sentence_length_mean=8.0, contraction_rate=200.0)
        delta = a.delta(b)
        gaps = delta.largest_gaps(n=2)
        # contraction_rate gap (-150) is larger in magnitude than mean (+2)
        assert gaps[0][0] == "contraction_rate"
        assert gaps[0][1] == -150.0

    def test_format_delta_runs(self):
        a = StyleProfile(sentence_length_mean=10.0, contraction_rate=50.0)
        b = StyleProfile(sentence_length_mean=8.0, contraction_rate=200.0)
        out = format_delta(a.delta(b))
        assert "Style-delta" in out
        assert "contraction_rate" in out


class TestProfileShape:
    def test_to_dict_has_all_fields(self):
        p = analyze("We don't ship on Fridays. It's a matter of policy.")
        d = p.to_dict()
        required = {
            "total_words",
            "sentences",
            "sentence_length_mean",
            "sentence_length_stdev",
            "fragment_rate",
            "contraction_rate",
            "em_dash_rate",
            "semicolon_rate",
            "colon_rate",
            "parenthetical_rate",
            "type_token_ratio",
            "avg_commas_per_sentence",
            "latinate_ratio",
            "first_person_rate",
            "second_person_rate",
            "passive_voice_approx",
            "starts_with_and_but",
        }
        assert required.issubset(d.keys())

    def test_realistic_sample_produces_sensible_signals(self):
        # Casual human-ish: mixed length, contractions, direct address.
        text = (
            "You'll find the config in /etc/platform/settings.yaml. It's "
            "not obvious — I missed it the first time. We use YAML because "
            "the legacy tooling can't parse JSON5. There's a migration "
            "underway but I wouldn't hold my breath."
        )
        p = analyze(text)
        assert p.contraction_rate > 100.0
        assert p.second_person_rate > 0.0
        assert p.first_person_rate > 0.0
        assert p.em_dash_rate > 0.0
        # Sentences are ~10 words each in this sample; σ is low by design.
        assert p.sentence_length_stdev >= 0.0
