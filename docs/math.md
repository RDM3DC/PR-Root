# PR-Root math notes

This document defines the conventions used by the code.

## Argument conventions

For \(z \neq 0\):
- magnitude \(r = |z|\)
- principal argument \(\mathrm{Arg}(z) \in (-\pi, \pi]\)

A *phase-resolved* argument is:
\[
\theta_k = \mathrm{Arg}(z) + 2\pi k, \quad k \in \mathbb{Z}
\]

## Multi-valued functions encoded with `k`

### Logarithm
\[
\log_k(z) = \ln|z| + i\,\theta_k
\]

### Power (real exponent)
\[
z^p\big|_k = |z|^p e^{i p \theta_k}
\]

### Square root
\[
\sqrt{z}\big|_k = |z|^{1/2} e^{i \theta_k/2}
\]

## Continuity along a path

If \(z(t)\) crosses the principal branch cut, \(\mathrm{Arg}(z(t))\) jumps by \(2\pi\).
To keep a continuous phase, update `k` or unwrap angle samples so that \(\theta_k(t)\) is continuous.

The helper `unwrap_angles` implements a standard unwrap rule:
- if a step \( \Delta \theta < -\pi\), add \(2\pi\)
- if a step \( \Delta \theta > \pi\), subtract \(2\pi\)

This produces a continuous representative of the same angle sequence.
