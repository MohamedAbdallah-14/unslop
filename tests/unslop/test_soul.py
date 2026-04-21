"""Tests for the Phase 5 soul-injection module."""

from __future__ import annotations

from unslop.scripts.soul import (
    SoulReport,
    contract_copula,
    contract_negations,
    humanize_soul,
)


class TestNegationContractions:
    def test_do_not_contracts(self):
        out = contract_negations("We do not ship on Fridays.")
        assert out == "We don't ship on Fridays."

    def test_does_not_contracts(self):
        out = contract_negations("The system does not retry.")
        assert out == "The system doesn't retry."

    def test_cannot_contracts(self):
        out = contract_negations("You cannot override that.")
        assert out == "You can't override that."

    def test_will_not_contracts(self):
        out = contract_negations("The worker will not ack.")
        assert out == "The worker won't ack."

    def test_case_preserved(self):
        out = contract_negations("Do not pass GO.")
        assert out == "Don't pass GO."

    def test_all_auxiliaries(self):
        inputs = [
            ("I did not know.", "I didn't know."),
            ("It is not ready.", "It isn't ready."),
            ("They are not listening.", "They aren't listening."),
            ("She was not around.", "She wasn't around."),
            ("We were not told.", "We weren't told."),
            ("He has not seen it.", "He hasn't seen it."),
            ("They have not replied.", "They haven't replied."),
            ("I had not noticed.", "I hadn't noticed."),
            ("We should not push.", "We shouldn't push."),
            ("It would not work.", "It wouldn't work."),
            ("You could not tell.", "You couldn't tell."),
            ("We must not skip that.", "We mustn't skip that."),
        ]
        for inp, expected in inputs:
            assert contract_negations(inp) == expected, inp

    def test_report_counts(self):
        r = SoulReport()
        text = "We do not ship. The system does not retry. Tests cannot fail."
        contract_negations(text, report=r)
        # 3 contractions on this line.
        assert r.negations_contracted == 3


class TestCopulaContractions:
    def test_it_is_plus_determiner_contracts(self):
        out = contract_copula("It is a bug.")
        assert "it's a bug" in out.lower()

    def test_it_is_plus_not_contracts(self):
        out = contract_copula("It is not ready.")
        assert "it's not ready" in out.lower()

    def test_it_is_before_noun_preserved(self):
        # "It is Martin" — proper noun, skip (not in the allow-list).
        out = contract_copula("It is Martin who pushed the change.")
        assert out == "It is Martin who pushed the change."

    def test_that_is_why_contracts(self):
        out = contract_copula("That is why we pinned it.")
        assert "that's why" in out.lower()

    def test_there_is_a_contracts(self):
        out = contract_copula("There is a race in the mutex.")
        assert "there's a race" in out.lower()

    def test_we_are_always_contracts(self):
        out = contract_copula("We are ready to ship.")
        assert out == "We're ready to ship."

    def test_you_are_always_contracts(self):
        out = contract_copula("You are probably right.")
        assert out == "You're probably right."

    def test_i_am_contracts(self):
        out = contract_copula("I am watching the logs.")
        assert out == "I'm watching the logs."

    def test_i_have_plus_participle_contracts(self):
        out = contract_copula("I have seen that happen.")
        assert out == "I've seen that happen."

    def test_i_have_plus_noun_preserved(self):
        # "I have a theory" — not in participle allow-list, stays full.
        out = contract_copula("I have a theory.")
        assert out == "I have a theory."

    def test_i_will_contracts(self):
        out = contract_copula("I will check the logs.")
        assert out == "I'll check the logs."

    def test_we_will_contracts(self):
        out = contract_copula("We will ship by Friday.")
        assert out == "We'll ship by Friday."


class TestPreservation:
    def test_placeholder_not_broken(self):
        # Placeholder tokens used by _protect() in humanize.py
        text = "We do not touch \x00FENCE#0\x00 in this pass."
        out = contract_negations(text)
        assert "\x00FENCE#0\x00" in out
        assert "don't" in out

    def test_no_change_on_already_contracted(self):
        text = "We don't ship. It's a trap."
        out = humanize_soul(text)
        assert out == text

    def test_code_style_tokens_untouched_in_protected_context(self):
        # `is not` inside a code path shouldn't appear here because the
        # real pipeline wraps code in placeholders. We simulate by using a
        # placeholder: the regex skips.
        text = "See \x00INLINE#0\x00 for `is not` semantics. We do not override it."
        out = humanize_soul(text)
        assert "\x00INLINE#0\x00" in out
        assert "don't" in out


class TestHumanizeSoulIntegration:
    def test_both_passes_run(self):
        text = (
            "We do not ship on Fridays. It is a policy we are strict about. "
            "They are not flexible on that."
        )
        r = SoulReport()
        out = humanize_soul(text, report=r)
        assert "don't" in out
        assert "we're" in out.lower()
        assert "aren't" in out
        assert r.negations_contracted >= 2
        assert r.copulas_contracted >= 1
