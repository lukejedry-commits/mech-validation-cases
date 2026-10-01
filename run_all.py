#!/usr/bin/env python3
"""Run Case A (Verlet + Euler control) and Case B (Verlet); write plots; assert."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src import case_a, case_b  # noqa: E402

PLOT_DIR = ROOT / "plots"


def main() -> int:
    PLOT_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Case A — velocity Verlet ===")
    a_v = case_a.run_verlet(PLOT_DIR)
    print(f"  T_est={a_v['T_est']:.6f} (π={case_a.T_ANALYTIC:.6f})")
    print(f"  amp={a_v['amp']:.6f}  max|E-2|={a_v['E_max_abs_err']:.3e}")

    print("=== Case A — explicit Euler (control) ===")
    a_e = case_a.run_euler(PLOT_DIR)
    print(f"  maxE-minE={a_e['E_range']:.3e}")

    print("=== Case B — velocity Verlet ===")
    b_v = case_b.run_verlet(PLOT_DIR)
    print(f"  T_est={b_v['T_est']:.6f} (2π={case_b.T_ANALYTIC:.6f})")
    print(f"  closure={b_v['closure']:.3e}")
    print(f"  max|ε+1/2|={b_v['eps_max_abs_err']:.3e}  max|h-√3/2|={b_v['h_max_abs_err']:.3e}")

    checks = []
    checks.extend(case_a.assert_verlet(a_v))
    checks.extend(case_a.assert_euler(a_e))
    checks.extend(case_b.assert_verlet(b_v))

    print("\n=== Assert table ===")
    all_ok = True
    lines = ["# One-page verdict\n", f"Plots: `{PLOT_DIR}/`\n\n"]
    for name, ok, detail in checks:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}: {detail}")
        lines.append(f"- **{mark}** — {name}: {detail}\n")
        all_ok = all_ok and ok

    verdict = "DONE — Verlet A/B pass; Euler-A fails conservation as required.\n" if all_ok else "NOT DONE — one or more asserts failed.\n"
    lines.append("\n" + verdict)
    (ROOT / "VERDICT.md").write_text("".join(lines))
    print("\n" + verdict.strip())
    print(f"Wrote {ROOT / 'VERDICT.md'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
