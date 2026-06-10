"""
test_project.py
===============

pytest suite for the Penrose Aperiodicity Barrier proof project.

Run with:
    source ~/heartlib/.venv/bin/activate
    python -m pytest tests/ -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import torch

sys.path.insert(0, str(Path(__file__).parent.parent / "empirical"))
from verify import (
    PHI,
    generate_fibonacci_word,
    all_windows,
    is_periodic,
    build_periodic_approximant,
    check_theorem_1,
    check_theorem_2,
    check_theorem_3,
    get_device,
    manual_seed,
)


@pytest.fixture(scope="module")
def device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


@pytest.fixture(scope="module", autouse=True)
def seed():
    manual_seed(1729)


class TestFibonacciWord:
    """Unit tests for Fibonacci word generation."""

    def test_fibonacci_word_lengths(self):
        """Fibonacci word lengths follow the Fibonacci sequence."""
        lengths = [len(generate_fibonacci_word(k)) for k in range(10)]
        # F_0=1, F_1=2, F_2=3, F_3=5, F_4=8, F_5=13, F_6=21, F_7=34, F_8=55, F_9=89
        expected = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        assert lengths == expected

    def test_fibonacci_word_substitution(self):
        """The word follows the substitution rule 0→01, 1→0."""
        w0 = generate_fibonacci_word(0)
        assert w0 == "0"
        
        w1 = generate_fibonacci_word(1)
        assert w1 == "01"
        
        w2 = generate_fibonacci_word(2)
        assert w2 == "010"
        
        w3 = generate_fibonacci_word(3)
        assert w3 == "01001"

    def test_fibonacci_no_consecutive_ones(self):
        """The Fibonacci word never contains "11"."""
        for levels in range(5, 12):
            word = generate_fibonacci_word(levels)
            assert "11" not in word


class TestAllWindows:
    """Tests for window extraction."""

    def test_window_count(self):
        """Correct number of windows."""
        word = "abcdef"
        windows_size_2 = all_windows(word, 2)
        assert len(windows_size_2) == 5  # ab, bc, cd, de, ef

    def test_window_content(self):
        """Windows contain the correct substrings."""
        word = "00101"
        windows = all_windows(word, 3)
        assert windows == {"001", "010", "101"}

    def test_fibonacci_window_growth(self):
        """Window count grows with word length but saturates for Sturmian words."""
        for levels in range(5, 12):
            word = generate_fibonacci_word(levels)
            windows_3 = all_windows(word, 3)
            # For Sturmian words, number of distinct n-windows is n+1
            assert len(windows_3) == 4  # 3+1


class TestIsPeriodic:
    """Tests for periodicity detection."""

    def test_periodic_simple(self):
        """Detect simple periodic words."""
        is_per, period = is_periodic("ababab", 10)
        assert is_per and period == 2

    def test_not_periodic(self):
        """Fibonacci word is not periodic."""
        word = generate_fibonacci_word(8)
        is_per, period = is_periodic(word, len(word) // 2)
        assert not is_per

    def test_periodic_with_period_gt_1(self):
        """Detect period > 1."""
        is_per, period = is_periodic("abcabcabc", 10)
        assert is_per and period == 3


class TestPeriodicApproximant:
    """Tests for periodic approximant construction."""

    def test_approximant_contains_all_windows(self):
        """Periodic approximant contains all Fibonacci R-windows."""
        for R in [4, 6, 8]:
            fib = generate_fibonacci_word(12)
            periodic = build_periodic_approximant(fib, R)
            fib_windows = all_windows(fib, R)
            per_windows = all_windows(periodic, R)
            assert fib_windows.issubset(per_windows), f"R={R}: missing windows"

    def test_approximant_is_periodic(self):
        """The approximant is actually periodic."""
        fib = generate_fibonacci_word(12)
        periodic = build_periodic_approximant(fib, 8)
        is_per, period = is_periodic(periodic, len(periodic) // 2)
        assert is_per, "Approximant not periodic"
        assert period > 8, f"Period {period} not > 8"

    def test_approximant_globally_different(self):
        """Approximant differs from Fibonacci word globally."""
        fib = generate_fibonacci_word(12)
        periodic = build_periodic_approximant(fib, 8)
        # Take first min(len) chars and compare
        n = min(len(fib), len(periodic))
        assert fib[:n] != periodic[:n], "Should be globally different"


class TestTheorem1:
    """Theorem 1: Local Indistinguishability."""

    def test_pass_default(self):
        r = check_theorem_1(R=8, fib_levels=12)
        assert r.passed, f"Theorem 1 failed: {r.detail}"

    def test_different_window_sizes(self):
        for R in [4, 6, 8]:
            r = check_theorem_1(R=R, fib_levels=12)
            assert r.passed, f"R={R} failed: {r.detail}"


class TestTheorem2:
    """Theorem 2: Substitution Depth."""

    def test_pass_default(self):
        r = check_theorem_2(max_n=500, max_depth=15)
        assert r.passed, f"Theorem 2 failed: {r.detail}"

    def test_small_depth(self):
        r = check_theorem_2(max_n=100, max_depth=10)
        assert r.passed, f"Small depth failed: {r.detail}"


class TestTheorem3:
    """Theorem 3: Global Consistency."""

    def test_pass_default(self):
        r = check_theorem_3(R=8, fib_levels=12)
        assert r.passed, f"Theorem 3 failed: {r.detail}"

    def test_different_window_sizes(self):
        for R in [4, 6, 8]:
            r = check_theorem_3(R=R, fib_levels=12)
            assert r.passed, f"R={R} failed: {r.detail}"


class TestGoldenRatio:
    """Sanity checks on φ."""

    def test_phi_value(self):
        assert abs(PHI - 1.6180339887) < 1e-9

    def test_phi_reciprocal(self):
        assert abs(PHI - 1 - 1/PHI) < 1e-9
