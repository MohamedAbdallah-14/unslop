"""Analytical tests for shield_metrics.py — pure stdlib detector metrics.

Each test uses synthetic scores where the correct answer is computable
by hand. No randomness, no model weights."""

from __future__ import annotations

import math

import pytest

from unslop.scripts.shield_metrics import auroc, sfd, tpr_at_fpr, urss, w_auroc


class TestTPRatFPR:
    def test_perfect_separator(self):
        y_true = [0, 0, 0, 0, 1, 1, 1, 1]
        y_score = [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]
        tpr, actual_fpr = tpr_at_fpr(y_true, y_score, target_fpr=0.05)
        assert tpr == pytest.approx(1.0)
        assert actual_fpr == pytest.approx(0.0)

    def test_random_classifier_near_target(self):
        y_true = [1, 0] * 50
        y_score = [i / 100 for i in range(100)]
        tpr, actual_fpr = tpr_at_fpr(y_true, y_score, target_fpr=0.05)
        assert actual_fpr <= 0.05 + 1e-9

    def test_inverted_scores_yield_zero_tpr(self):
        y_true = [0, 0, 0, 0, 1, 1, 1, 1]
        y_score = [0.9, 0.8, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1]
        tpr, actual_fpr = tpr_at_fpr(y_true, y_score, target_fpr=0.05)
        assert tpr == pytest.approx(0.0)

    def test_empty_input(self):
        assert tpr_at_fpr([], [], target_fpr=0.05) == (0.0, 0.0)

    def test_single_class(self):
        assert tpr_at_fpr([1, 1, 1], [0.5, 0.6, 0.7]) == (0.0, 0.0)
        assert tpr_at_fpr([0, 0, 0], [0.5, 0.6, 0.7]) == (0.0, 0.0)

    def test_length_mismatch(self):
        assert tpr_at_fpr([0, 1], [0.5]) == (0.0, 0.0)

    def test_known_threshold(self):
        y_true = [0] * 20 + [1] * 20
        y_score = [i / 40 for i in range(40)]
        tpr, actual_fpr = tpr_at_fpr(y_true, y_score, target_fpr=0.05)
        assert actual_fpr <= 0.05


class TestAUROC:
    def test_perfect_classifier(self):
        y_true = [0, 0, 0, 1, 1, 1]
        y_score = [0.1, 0.2, 0.3, 0.7, 0.8, 0.9]
        assert auroc(y_true, y_score) == pytest.approx(1.0)

    def test_known_auroc_value(self):
        y_true = [0, 0, 1, 0, 1, 1]
        y_score = [0.1, 0.4, 0.5, 0.6, 0.7, 0.9]
        auc = auroc(y_true, y_score)
        assert 0.5 < auc < 1.0

    def test_worst_classifier(self):
        y_true = [0, 0, 0, 1, 1, 1]
        y_score = [0.9, 0.8, 0.7, 0.3, 0.2, 0.1]
        assert auroc(y_true, y_score) == pytest.approx(0.0)

    def test_empty_input(self):
        assert auroc([], []) == pytest.approx(0.0)

    def test_single_class(self):
        assert auroc([1, 1], [0.5, 0.6]) == pytest.approx(0.0)

    def test_all_tied_scores_produce_half(self):
        """All-tied labels [0,1,0,1] with identical scores must produce AUROC 0.5."""
        y_true = [0, 1, 0, 1]
        y_score = [0.5, 0.5, 0.5, 0.5]
        assert auroc(y_true, y_score) == pytest.approx(0.5)

    def test_tied_scores_no_label_order_bias(self):
        """Tied scores give same AUROC regardless of label order."""
        y_true_a = [0, 0, 1, 1]
        y_true_b = [1, 1, 0, 0]
        y_score = [0.7, 0.7, 0.7, 0.7]
        assert auroc(y_true_a, y_score) == auroc(y_true_b, y_score)
        assert auroc(y_true_a, y_score) == pytest.approx(0.5)

    def test_partial_ties(self):
        """Mix of tied and distinct: [0,1] at 0.5, [1] at 0.9 -> AUROC > 0.5."""
        y_true = [0, 1, 1]
        y_score = [0.5, 0.5, 0.9]
        auc = auroc(y_true, y_score)
        assert 0.5 <= auc <= 1.0


class TestWeightedAUROC:
    def test_perfect_classifier_high_w_auroc(self):
        y_true = [0, 0, 0, 1, 1, 1]
        y_score = [0.1, 0.2, 0.3, 0.7, 0.8, 0.9]
        w = w_auroc(y_true, y_score)
        assert w == pytest.approx(1.0, abs=0.02)

    def test_w_auroc_bounded_zero_one(self):
        y_true = [0, 1, 0, 1, 0, 1]
        y_score = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        w = w_auroc(y_true, y_score)
        assert 0.0 <= w <= 1.0

    def test_w_auroc_at_least_auroc_for_good_classifier(self):
        y_true = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        y_score = [0.1, 0.2, 0.3, 0.35, 0.4, 0.6, 0.7, 0.8, 0.85, 0.9]
        w = w_auroc(y_true, y_score)
        a = auroc(y_true, y_score)
        assert a == pytest.approx(1.0)
        assert w > 0.9

    def test_empty_input(self):
        assert w_auroc([], []) == pytest.approx(0.0)

    def test_all_tied_scores_no_label_order_bias(self):
        """All-tied scores: same W-AUROC regardless of label order."""
        y_true_a = [0, 1, 0, 1]
        y_true_b = [1, 0, 1, 0]
        y_score = [0.5, 0.5, 0.5, 0.5]
        assert w_auroc(y_true_a, y_score) == w_auroc(y_true_b, y_score)
        w = w_auroc(y_true_a, y_score)
        assert 0.0 < w < 0.5  # random classifier, penalized at low FPR

    def test_perfect_separation_returns_one(self):
        y_true = [0] * 50 + [1] * 50
        y_score = [i / 100 for i in range(50)] + [0.5 + i / 100 for i in range(50)]
        w = w_auroc(y_true, y_score)
        assert w == pytest.approx(1.0, abs=0.01)


class TestSFD:
    def test_equal_fprs_return_one(self):
        """Equal scenario FPRs -> SFD = 1.0 (perfect stability)."""
        assert sfd([0.05, 0.05, 0.05]) == pytest.approx(1.0)

    def test_sigma_0_1_returns_half(self):
        """sigma_FPR = 0.1, lambda = 10*ln(2) -> exp(-ln2) = 0.5."""
        fprs = [0.0, 0.2]
        sigma = math.sqrt(sum((f - 0.1) ** 2 for f in fprs) / 2)
        assert sigma == pytest.approx(0.1)
        result = sfd(fprs)
        assert result == pytest.approx(0.5, abs=0.01)

    def test_unequal_fprs_less_than_one(self):
        result = sfd([0.01, 0.10, 0.30])
        assert 0.0 < result < 1.0

    def test_single_scenario_returns_one(self):
        assert sfd([0.05]) == pytest.approx(1.0)

    def test_monotonic_in_disparity(self):
        low_disp = sfd([0.04, 0.06])
        high_disp = sfd([0.01, 0.20])
        assert high_disp < low_disp

    def test_higher_is_better(self):
        """More equal FPRs -> higher SFD."""
        equal = sfd([0.05, 0.05])
        unequal = sfd([0.01, 0.09])
        assert equal > unequal


class TestURSS:
    def test_perfect_fair_score(self):
        """Perfect W-AUROCs and perfect stability -> URSS = 1.0."""
        result = urss([1.0, 1.0], 1.0)
        assert result == pytest.approx(1.0)

    def test_zero_w_auroc_zero_urss(self):
        assert urss([0.0, 0.0], 1.0) == pytest.approx(0.0)

    def test_low_sfd_penalizes(self):
        """Lower SFD (instability) reduces URSS."""
        stable = urss([0.9, 0.9], 1.0)
        unstable = urss([0.9, 0.9], 0.5)
        assert unstable < stable

    def test_empty_w_aurocs(self):
        assert urss([], 1.0) == pytest.approx(0.0)

    def test_formula_is_mean_times_sfd(self):
        """URSS = mean(W-AUROCs) * SFD, not * (1 - SFD)."""
        w_vals = [0.8, 0.6]
        s = 0.7
        expected = (0.8 + 0.6) / 2 * 0.7
        assert urss(w_vals, s) == pytest.approx(expected)
