# PR-Root (Phase-Resolved Root)

**PR-Root** is a small, explicit way to handle **complex roots, powers, and logarithms** without losing track of the **branch**. It does **not** change complex analysis; it makes the branch choice **first-class** via an integer `k`.

## Why
Functions like `sqrt(z)` and `log(z)` are multi-valued in the complex plane. Most libraries return the **principal value** (a specific branch). PR-Root lets you specify the branch explicitly:

- pick an integer branch `k ∈ ℤ`
- use the lifted argument `θ = Arg(z) + 2πk`
- compute roots/powers/logs using that `θ`

This is useful for simulations, continuity across cuts, and “phase-unwrapped” workflows.

---

## Core math (single source of truth)

Let \( z \in \mathbb{C}\setminus\{0\} \). Write
\[
z = r e^{i\theta}, \quad r = |z| > 0
\]
where the **principal argument** is
\[
\mathrm{Arg}(z) \in (-\pi, \pi]
\]
PR-Root uses an explicit branch integer \(k \in \mathbb{Z}\) and defines the **phase-resolved argument**
\[
\theta_k = \mathrm{Arg}(z) + 2\pi k
\]

Then:

### Phase-resolved logarithm
\[
\log_k(z) = \ln r + i\,\theta_k
\]

### Phase-resolved power
For real \(p\),
\[
z^{\,p}\big|_k = r^{p} e^{i p \theta_k}
\]

### Phase-resolved square root
\[
\sqrt{z}\big|_k = r^{1/2} e^{i \theta_k/2}
\]

Notes:
- `k = 0` matches the principal branch for `log`/`sqrt`/`pow`.
- Different `k` values produce different (valid) branches.
- For continuity along a path, adjust `k` (or unwrap angles) to avoid jumps of \(2\pi\).

---

## Visualizations

These animations demonstrate phase-resolved behaviors and branch structures in complex analysis. They illustrate how phase evolves continuously across branch cuts and how different branch choices affect the behavior of multi-valued functions.

### Phase Drag
<video src="PhaseDrag.mp4" controls title="Phase Drag">Your browser does not support the video tag.</video>

### Phase Spine
<video src="PhaseSpine.mp4" controls title="Phase Spine">Your browser does not support the video tag.</video>

### Phase Split (4-way)
<video src="PhaseSplit4.mp4" controls title="Phase Split 4">Your browser does not support the video tag.</video>

### Phase Winding Without Force
<video src="PhaseWindingWithoutForce.mp4" controls title="Phase Winding Without Force">Your browser does not support the video tag.</video>

### Spinor Rotation: Why 360° Isn't Enough
<video src="SpinorRotationWhy360IsntEnough.mp4" controls title="Spinor Rotation Why 360 Isn't Enough">Your browser does not support the video tag.</video>

### Josephson Junction Phase Gate
<video src="JosephsonJunctionPhaseGate.mp4" controls title="Josephson Junction Phase Gate">Your browser does not support the video tag.</video>

### SQUID Geometry: Controlled Phase Closure
<video src="SQUIDGeometryControlledPhaseClosure.mp4" controls title="SQUID Geometry Controlled Phase Closure">Your browser does not support the video tag.</video>

---

## Install

From source:
```bash
python -m pip install -e .[dev]
```

---

## Usage

```python
from pr_root import pr_log, pr_sqrt, pr_pow, PRComplex, pr_from_complex

z = -1 + 0j

# principal sqrt (k=0): i
print(pr_sqrt(z, k=0))  # 1j

# next branch (k=1): -i (since theta = pi + 2pi)
print(pr_sqrt(z, k=1))  # -1j

# phase-resolved log differs by 2πi per branch
print(pr_log(z, k=0))   # 0 + i*pi
print(pr_log(z, k=1))   # 0 + i*(pi + 2*pi)

# represent as an explicit (r, theta, k)
w = pr_from_complex(z, k=1)
print(w.r, w.theta, w.k)  # 1.0, pi+2pi, 1
print(w.to_complex())     # (-1+0j)
```

Unwrapping example (angle sequence):
```python
from pr_root import unwrap_angles

angles = [3.10, -3.12, -3.11]  # near the -π/π cut
print(unwrap_angles(angles))    # continuous angles (adds 2π where needed)
```

---

## Development

```bash
python -m pip install -e .[dev]
pytest -q
ruff check .
```

---

## License
MIT. See `LICENSE`.
