import math

import pytest

from pr_root import pr_log, pr_pow, pr_sqrt, pr_from_complex, unwrap_angles, wrap_to_pi

TAU = 2 * math.pi


def almost_equal(a: complex, b: complex, eps: float = 1e-12) -> bool:
    return abs(a - b) <= eps


def test_wrap_to_pi_range():
    for x in [0.0, math.pi, -math.pi, 10.0, -10.0, 123.456]:
        y = wrap_to_pi(x)
        assert -math.pi < y <= math.pi


def test_pr_from_complex_roundtrip():
    z = -1.0 + 0.0j
    w0 = pr_from_complex(z, k=0)
    w1 = pr_from_complex(z, k=1)
    assert almost_equal(w0.to_complex(), z)
    assert almost_equal(w1.to_complex(), z)
    assert abs((w1.theta - w0.theta) - TAU) < 1e-12


def test_pr_sqrt_branches_for_minus_one():
    z = -1.0 + 0.0j
    s0 = pr_sqrt(z, k=0)
    s1 = pr_sqrt(z, k=1)
    assert almost_equal(s0, 0.0 + 1.0j)
    assert almost_equal(s1, 0.0 - 1.0j)
    assert almost_equal(s0 * s0, z)
    assert almost_equal(s1 * s1, z)


def test_pr_log_branch_difference():
    z = -1.0 + 0.0j
    l0 = pr_log(z, k=0)
    l1 = pr_log(z, k=1)
    assert abs((l1 - l0) - 1j * TAU) < 1e-12


def test_pr_pow_matches_pr_sqrt_when_p_half():
    z = 2.0 + 3.0j
    a = pr_pow(z, 0.5, k=0)
    b = pr_sqrt(z, k=0)
    assert almost_equal(a, b, eps=1e-10)


def test_zero_behavior():
    assert pr_sqrt(0.0 + 0.0j, k=0) == 0.0 + 0.0j
    assert pr_pow(0.0 + 0.0j, 2.0, k=0) == 0.0 + 0.0j
    assert pr_pow(0.0 + 0.0j, 0.0, k=0) == 1.0 + 0.0j
    with pytest.raises(ValueError):
        pr_pow(0.0 + 0.0j, -1.0, k=0)
    with pytest.raises(ValueError):
        pr_log(0.0 + 0.0j, k=0)


def test_unwrap_angles_removes_cut_jump():
    angles = [3.10, -3.12, -3.11]  # jump across -pi/pi cut
    unwrapped = unwrap_angles(angles)
    assert len(unwrapped) == 3
    # After unwrapping, differences should be small
    assert abs(unwrapped[1] - unwrapped[0]) < 0.5
    assert abs(unwrapped[2] - unwrapped[1]) < 0.5
