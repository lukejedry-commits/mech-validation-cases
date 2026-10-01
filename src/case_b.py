"""Case B — one planet, fixed sun (Kepler)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.integrators import velocity_verlet

GM = 1.0
A = 1.0
E_ORB = 0.5
T_ANALYTIC = 2.0 * np.pi * np.sqrt(A**3 / GM)  # 2π
RP = A * (1.0 - E_ORB)  # 0.5
VP = np.sqrt(GM * (2.0 / RP - 1.0 / A))  # √3
R0 = np.array([RP, 0.0])
V0 = np.array([0.0, VP])
EPS_TARGET = -GM / (2.0 * A)  # -0.5
H_TARGET = np.sqrt(GM * A * (1.0 - E_ORB**2))  # √3/2
DT = 0.001
N_PERIODS = 10


def accel(r: np.ndarray) -> np.ndarray:
    r2 = float(np.dot(r, r))
    r3 = r2 * np.sqrt(r2)
    return -GM * r / r3


def specific_energy(r: np.ndarray, v: np.ndarray) -> np.ndarray:
    # r, v shape (N, 2)
    speed2 = np.sum(v * v, axis=1)
    radius = np.sqrt(np.sum(r * r, axis=1))
    return 0.5 * speed2 - GM / radius


def specific_h(r: np.ndarray, v: np.ndarray) -> np.ndarray:
    # 2D: h = x vy - y vx
    return r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]


def estimate_period(t: np.ndarray, r: np.ndarray) -> float:
    """Mean orbital period from successive +x periapsis-like crossings (y: -→+, x>0)."""
    y = r[:, 1]
    x = r[:, 0]
    crossings = []
    for i in range(len(y) - 1):
        if y[i] <= 0.0 < y[i + 1] and x[i] > 0.0:
            frac = -y[i] / (y[i + 1] - y[i])
            crossings.append(t[i] + frac * (t[i + 1] - t[i]))
    if len(crossings) < 2:
        return float("nan")
    return float(np.mean(np.diff(crossings)))


def run_verlet(plot_dir: Path) -> dict:
    n_steps = int(np.ceil(N_PERIODS * T_ANALYTIC / DT))
    t, r, v = velocity_verlet(R0, V0, accel, DT, n_steps)
    eps = specific_energy(r, v)
    h = specific_h(r, v)
    T_est = estimate_period(t, r)

    # Closure after one analytic period
    idx_T = int(round(T_ANALYTIC / DT))
    idx_T = min(idx_T, len(r) - 1)
    closure = float(np.linalg.norm(r[idx_T] - R0))

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    axes[0].plot(r[:, 0], r[:, 1], lw=0.6)
    axes[0].plot(0, 0, "y*", ms=12)
    axes[0].set_aspect("equal")
    axes[0].set_title("Case B — orbit (Verlet)")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")

    axes[1].plot(t, eps, lw=0.8)
    axes[1].axhline(EPS_TARGET, color="k", ls="--", lw=0.8)
    axes[1].set_title("ε(t)")
    axes[1].set_xlabel("t")
    axes[1].set_ylabel("ε")

    axes[2].plot(t, h, lw=0.8)
    axes[2].axhline(H_TARGET, color="k", ls="--", lw=0.8)
    axes[2].set_title("h(t)")
    axes[2].set_xlabel("t")
    axes[2].set_ylabel("h")

    fig.tight_layout()
    fig.savefig(plot_dir / "case_b_verlet.png", dpi=120)
    plt.close(fig)

    # Also save E(t) alias plot name for NM gate (ε is specific energy)
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    ax2.plot(t, eps, lw=0.8)
    ax2.axhline(EPS_TARGET, color="k", ls="--", lw=0.8)
    ax2.set_xlabel("t")
    ax2.set_ylabel("ε(t)  [E(t)]")
    ax2.set_title("Case B — specific energy vs time")
    fig2.tight_layout()
    fig2.savefig(plot_dir / "case_b_E_t.png", dpi=120)
    plt.close(fig2)

    return {
        "t": t,
        "r": r,
        "v": v,
        "eps": eps,
        "h": h,
        "T_est": T_est,
        "closure": closure,
        "eps_max_abs_err": float(np.max(np.abs(eps - EPS_TARGET))),
        "h_max_abs_err": float(np.max(np.abs(h - H_TARGET))),
    }


def assert_verlet(res: dict) -> list[tuple[str, bool, str]]:
    checks = []
    rel_T = abs(res["T_est"] - T_ANALYTIC) / T_ANALYTIC
    ok = rel_T <= 1e-3
    checks.append(("B Verlet period", ok, f"|T-2π|/2π={rel_T:.3e} (≤1e-3)"))

    ok = res["closure"] <= 1e-2
    checks.append(("B orbit closure", ok, f"|r(T)-r0|={res['closure']:.3e} (≤1e-2)"))

    ok = res["eps_max_abs_err"] <= 1e-3
    checks.append(
        ("B energy flat", ok, f"max|ε+1/2|={res['eps_max_abs_err']:.3e} (≤1e-3)")
    )

    ok = res["h_max_abs_err"] <= 1e-3
    checks.append(
        ("B h flat", ok, f"max|h-√3/2|={res['h_max_abs_err']:.3e} (≤1e-3)")
    )
    return checks
