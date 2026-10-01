"""Case A — undamped harmonic oscillator (Hooke spring)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.integrators import explicit_euler, velocity_verlet

M = 1.0
K = 4.0
X0 = 1.0
V0 = 0.0
OMEGA = np.sqrt(K / M)  # 2
T_ANALYTIC = 2.0 * np.pi / OMEGA  # π
E_TARGET = 0.5 * K * X0**2 + 0.5 * M * V0**2  # 2
DT = 0.01
N_PERIODS = 10


def accel(x: np.ndarray) -> np.ndarray:
    return -(K / M) * x


def energy(x: np.ndarray, v: np.ndarray) -> np.ndarray:
    return 0.5 * K * x**2 + 0.5 * M * v**2


def estimate_period(t: np.ndarray, x: np.ndarray) -> float:
    """Mean period from successive positive zero-crossings of x(t)."""
    crossings = []
    for i in range(len(x) - 1):
        if x[i] <= 0.0 < x[i + 1]:
            # linear interpolate
            frac = -x[i] / (x[i + 1] - x[i])
            crossings.append(t[i] + frac * (t[i + 1] - t[i]))
    if len(crossings) < 2:
        return float("nan")
    periods = np.diff(crossings)
    return float(np.mean(periods))


def run_verlet(plot_dir: Path) -> dict:
    n_steps = int(np.ceil(N_PERIODS * T_ANALYTIC / DT))
    t, x, v = velocity_verlet(
        np.array(X0), np.array(V0), accel, DT, n_steps
    )
    x = x.ravel()
    v = v.ravel()
    E = energy(x, v)
    T_est = estimate_period(t, x)
    amp = float(np.max(np.abs(x)))

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(t, x, lw=1.0)
    axes[0].set_ylabel("x(t)")
    axes[0].set_title("Case A — velocity Verlet")
    axes[1].plot(t, E, lw=1.0)
    axes[1].axhline(E_TARGET, color="k", ls="--", lw=0.8)
    axes[1].set_ylabel("E(t)")
    axes[1].set_xlabel("t")
    fig.tight_layout()
    fig.savefig(plot_dir / "case_a_verlet.png", dpi=120)
    plt.close(fig)

    return {
        "t": t,
        "x": x,
        "v": v,
        "E": E,
        "T_est": T_est,
        "amp": amp,
        "E_max_abs_err": float(np.max(np.abs(E - E_TARGET))),
        "E_range": float(np.max(E) - np.min(E)),
    }


def run_euler(plot_dir: Path) -> dict:
    n_steps = int(np.ceil(N_PERIODS * T_ANALYTIC / DT))
    t, x, v = explicit_euler(
        np.array(X0), np.array(V0), accel, DT, n_steps
    )
    x = x.ravel()
    v = v.ravel()
    E = energy(x, v)

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(t, x, lw=1.0, color="C1")
    axes[0].set_ylabel("x(t)")
    axes[0].set_title("Case A — explicit Euler (known-bad control)")
    axes[1].plot(t, E, lw=1.0, color="C1")
    axes[1].axhline(E_TARGET, color="k", ls="--", lw=0.8)
    axes[1].set_ylabel("E(t)")
    axes[1].set_xlabel("t")
    fig.tight_layout()
    fig.savefig(plot_dir / "case_a_euler.png", dpi=120)
    plt.close(fig)

    return {
        "t": t,
        "x": x,
        "E": E,
        "E_range": float(np.max(E) - np.min(E)),
        "E_max_abs_err": float(np.max(np.abs(E - E_TARGET))),
    }


def assert_verlet(res: dict) -> list[tuple[str, bool, str]]:
    checks = []
    rel_T = abs(res["T_est"] - T_ANALYTIC) / T_ANALYTIC
    ok = rel_T <= 1e-3
    checks.append(("A Verlet period", ok, f"|T-π|/π={rel_T:.3e} (≤1e-3)"))

    amp_err = abs(res["amp"] - 1.0)
    ok = amp_err <= 1e-3
    checks.append(("A Verlet amplitude", ok, f"|max|x|-1|={amp_err:.3e} (≤1e-3)"))

    ok = res["E_max_abs_err"] <= 1e-3
    checks.append(
        ("A Verlet energy bound", ok, f"max|E-2|={res['E_max_abs_err']:.3e} (≤1e-3)")
    )
    return checks


def assert_euler(res: dict) -> list[tuple[str, bool, str]]:
    ok = res["E_range"] > 0.1
    return [
        (
            "A Euler energy growth (known-bad)",
            ok,
            f"maxE-minE={res['E_range']:.3e} (>0.1 required)",
        )
    ]
