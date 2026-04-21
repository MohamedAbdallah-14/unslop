"""Tests for the surprisal-variance reader.

These tests avoid downloading weights: they either (a) verify the skip-
flag path, (b) verify the empty-input fast path, or (c) patch the LM
loader to return a tiny fake model.

A real end-to-end test with distilgpt2 exists but is guarded behind the
UNSLOP_RUN_REAL_SURPRISAL=1 env var so CI without HF cache doesn't fail."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from unslop.scripts import surprisal
from unslop.scripts.surprisal import (
    SurprisalReading,
    SurprisalUnavailable,
    compute_surprisal_variance,
    is_available,
)


class TestReadingShape:
    def test_to_dict_shape(self):
        r = SurprisalReading(
            mean_log_prob=-2.5,
            surprisal_stdev=1.2,
            surprisal_cv=0.48,
            token_count=100,
            model="distilgpt2",
        )
        d = r.to_dict()
        assert d["token_count"] == 100
        assert d["model"] == "distilgpt2"
        assert d["surprisal_stdev"] == 1.2
        assert d["surprisal_cv"] == 0.48

    def test_empty_reading_zeros(self):
        # compute_surprisal_variance on empty input returns a zero reading
        # *without* loading the model, so it's safe even with no deps.
        r = compute_surprisal_variance("")
        assert r.token_count == 0
        assert r.surprisal_stdev == 0.0
        assert r.surprisal_cv == 0.0

    def test_whitespace_only_reading_zeros(self):
        r = compute_surprisal_variance("   \n\t  \n")
        assert r.token_count == 0


class TestSkipFlag:
    def test_env_flag_raises_unavailable(self, monkeypatch):
        monkeypatch.setenv("UNSLOP_SKIP_SURPRISAL", "1")
        with pytest.raises(SurprisalUnavailable):
            compute_surprisal_variance("anything")

    def test_env_flag_is_available_returns_false(self, monkeypatch):
        monkeypatch.setenv("UNSLOP_SKIP_SURPRISAL", "1")
        assert is_available() is False


class TestMockedLM:
    """Patch `_load_scorer` to return a toy fake that exercises the full pipe."""

    def setup_method(self):
        # Flush the cache so each test starts clean.
        surprisal._LM_CACHE.clear()

    def test_full_pass_with_fake_lm(self, monkeypatch):
        try:
            import torch
        except ImportError:
            pytest.skip("torch not installed")

        class FakeTokenizer:
            def encode(self, text, return_tensors=None):
                # Deterministic: each word becomes one token id equal to
                # its length mod 50. Enough variety to produce nonzero
                # stdev.
                toks = [len(w) % 50 + 1 for w in text.split() if w]
                if not toks:
                    return torch.zeros((1, 0), dtype=torch.long)
                return torch.tensor([toks], dtype=torch.long)

        class FakeLM:
            def __init__(self, vocab=60, dim=8):
                self.vocab = vocab
                # Random-ish but deterministic logits.
                torch.manual_seed(0)
                self.emb = torch.randn(vocab, dim)
                self.proj = torch.randn(dim, vocab)

            def __call__(self, ids):
                x = self.emb[ids]
                logits = x @ self.proj
                return type("O", (), {"logits": logits})

            def train(self, mode):
                return self

        fake_tok = FakeTokenizer()
        fake_lm = FakeLM()
        monkeypatch.setattr(surprisal, "_load_scorer", lambda _m: (fake_tok, fake_lm))

        text = "one two three four five six seven eight nine ten"
        r = compute_surprisal_variance(text, model="fake")

        # Nonzero readings on nonempty text.
        assert r.token_count > 0
        assert r.surprisal_stdev >= 0.0
        assert r.model == "fake"

    def test_short_input_returns_zero_without_crashing(self, monkeypatch):
        try:
            import torch
        except ImportError:
            pytest.skip("torch not installed")

        class FakeTokenizer:
            def encode(self, text, return_tensors=None):
                # Only one token -> can't compute variance.
                return torch.tensor([[42]], dtype=torch.long)

        class FakeLM:
            def __call__(self, ids):
                vocab = 50
                return type("O", (), {"logits": torch.zeros(1, ids.shape[1], vocab)})

            def train(self, mode):
                return self

        monkeypatch.setattr(
            surprisal, "_load_scorer", lambda _m: (FakeTokenizer(), FakeLM())
        )
        r = compute_surprisal_variance("hi", model="fake")
        assert r.token_count == 1
        assert r.surprisal_stdev == 0.0


@pytest.mark.skipif(
    os.environ.get("UNSLOP_RUN_REAL_SURPRISAL") != "1",
    reason="Set UNSLOP_RUN_REAL_SURPRISAL=1 to exercise the real distilgpt2 path",
)
class TestRealDistilGPT2:
    """End-to-end test against distilgpt2. Skipped by default; set the env
    var to enable locally when the HF cache is populated."""

    def test_real_reading_is_reasonable(self):
        text = (
            "The quick brown fox jumps over the lazy dog. "
            "The cat sat on the mat. Shakespeare wrote Hamlet."
        )
        r = compute_surprisal_variance(text)
        assert r.token_count > 5
        # distilgpt2 on short English prose: stdev should be clearly >0.
        assert r.surprisal_stdev > 0.1
        # Mean log-prob for coherent English is well above -20.
        assert -20 < r.mean_log_prob < 0

    def test_bursty_beats_repetitive(self):
        # A repetitive, low-surprisal input should have a SMALLER stdev
        # than a varied, high-content input. This is the core DivEye
        # claim, boiled down to two strings.
        flat = " ".join(["the cat sat on the mat."] * 10)
        varied = (
            "Diffeomorphism preserves orientation. "
            "Shakespeare's iambic pentameter stumbles around the caesura. "
            "Kafka's bureaucracies metastasize into infinite recursion. "
            "The quick brown fox thought about dinner."
        )
        r_flat = compute_surprisal_variance(flat)
        r_varied = compute_surprisal_variance(varied)
        assert r_varied.surprisal_stdev > r_flat.surprisal_stdev
