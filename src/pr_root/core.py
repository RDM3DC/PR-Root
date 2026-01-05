from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import List, Optional, Sequence, Union

TAU = 2.0 * math.pi


ComplexLike = Union[complex, "PRComplex"]


def wrap_to_pi(theta: float) -> float:
    """
    Wrap an angle to (-pi, pi].

    This matches the usual principal argument range used by cmath.phase.
    """
    # Map to (-pi, pi]
    wrapped = (theta + math.pi) % TAU - math.pi
    if wrapped <= -math.pi:
        # move -pi to +pi to satisfy (-pi, pi]
        wrapped += TAU
    return wrapped


def unwrap_angles(angles: Sequence[float], *, discontinuity: float = math.pi) -> List[float]:
    """
    Unwrap a sequence of angles (radians) to remove jumps of ~2π.

    Parameters
    ----------
    angles:
        Sequence of angles (any real values).
    discontinuity:
        Threshold for detecting a jump; default π.

    Returns
    -------
    List[float]
        Unwrapped angles, same length as input.
    """
    if not angles:
        return []

    out = [float(angles[0])]
    offset = 0.0
    prev = float(angles[0])

    for a in angles[1:]:
        a = float(a)
        delta = a - prev
        if delta > discontinuity:
            offset -= TAU
        elif delta < -discontinuity:
            offset += TAU
        out.append(a + offset)
        prev = a

    return out


@dataclass(frozen=True)
class PRComplex:
    """
    Phase-resolved complex representation.

    Stores a magnitude r >= 0 and a lifted argument theta = Arg(z) + 2πk, where k ∈ ℤ.
    For z = 0, we store r=0 and theta=0 by convention; k is kept but not meaningful.
    """

    r: float
    theta: float
    k: int = 0

    def to_complex(self) -> complex:
        if self.r == 0.0:
            return 0.0 + 0.0j
        return self.r * complex(math.cos(self.theta), math.sin(self.theta))

    @property
    def principal_arg(self) -> float:
        return wrap_to_pi(self.theta)

    @property
    def branch(self) -> int:
        return self.k


def pr_from_complex(z: complex, *, k: int = 0) -> PRComplex:
    """
    Convert a complex number to PRComplex using branch integer k.

    theta_k = Arg(z) + 2πk
    """
    if z == 0:
        return PRComplex(r=0.0, theta=0.0, k=k)
    r = abs(z)
    arg = cmath.phase(z)  # (-pi, pi]
    theta = float(arg) + TAU * int(k)
    return PRComplex(r=float(r), theta=theta, k=int(k))


def _coerce(z: ComplexLike, *, k: Optional[int] = None) -> PRComplex:
    if isinstance(z, PRComplex):
        if k is None:
            return z
        # override branch by recomputing theta using principal Arg(z) + 2πk
        return pr_from_complex(z.to_complex(), k=k)
    return pr_from_complex(complex(z), k=0 if k is None else k)


def pr_log(z: ComplexLike, *, k: int = 0) -> complex:
    """
    Phase-resolved complex logarithm:
        log_k(z) = ln|z| + i(Arg(z) + 2πk)

    For z=0, raises ValueError (log undefined).
    """
    w = _coerce(z, k=k)
    if w.r == 0.0:
        raise ValueError("log is undefined for z=0")
    return math.log(w.r) + 1j * w.theta


def pr_pow(z: ComplexLike, p: float, *, k: int = 0) -> complex:
    """
    Phase-resolved power for real exponent p:
        z^p|_k = |z|^p * exp(i p theta_k)

    For z=0:
      - if p>0, returns 0
      - if p==0, returns 1 (convention)
      - if p<0, raises ValueError
    """
    w = _coerce(z, k=k)
    if w.r == 0.0:
        if p > 0:
            return 0.0 + 0.0j
        if p == 0:
            return 1.0 + 0.0j
        raise ValueError("0 cannot be raised to a negative power")
    mag = w.r**p
    ang = p * w.theta
    return mag * complex(math.cos(ang), math.sin(ang))


def pr_sqrt(z: ComplexLike, *, k: int = 0) -> complex:
    """
    Phase-resolved square root:
        sqrt(z)|_k = |z|^(1/2) * exp(i theta_k/2)

    For z=0, returns 0.
    """
    w = _coerce(z, k=k)
    if w.r == 0.0:
        return 0.0 + 0.0j
    mag = math.sqrt(w.r)
    ang = 0.5 * w.theta
    return mag * complex(math.cos(ang), math.sin(ang))
