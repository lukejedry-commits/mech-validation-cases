# One-page verdict
Plots: `/workspace/mech-validation-cases/plots/`

- **PASS** — A Verlet period: |T-π|/π=1.667e-05 (≤1e-3)
- **PASS** — A Verlet amplitude: |max|x|-1|=0.000e+00 (≤1e-3)
- **PASS** — A Verlet energy bound: max|E-2|=2.000e-04 (≤1e-3)
- **PASS** — A Euler energy growth (known-bad): maxE-minE=5.027e+00 (>0.1 required)
- **PASS** — B Verlet period: |T-2π|/2π=4.118e-06 (≤1e-3)
- **PASS** — B orbit closure: |r(T)-r0|=3.658e-04 (≤1e-2)
- **PASS** — B energy flat: max|ε+1/2|=1.359e-06 (≤1e-3)
- **PASS** — B h flat: max|h-√3/2|=1.898e-14 (≤1e-3)

DONE — Verlet A/B pass; Euler-A fails conservation as required.
