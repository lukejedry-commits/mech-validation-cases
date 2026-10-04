#!/usr/bin/env python3
"""Live velocity-Verlet viewer. Runs until the window closes or Ctrl+C.

Does not touch the frozen asserts in run_all.py. Explicit Euler is not used.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Codespaces has no desktop. WebAgg serves the plot in the browser (port-forwarded).
if not os.environ.get("MPLBACKEND") and not (
    os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
):
    import matplotlib

    matplotlib.use("WebAgg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from src.case_a import DT as DT_A  # noqa: E402
from src.case_a import E_TARGET, K, M, X0, V0  # noqa: E402
from src.case_a import T_ANALYTIC as T_A  # noqa: E402
from src.case_a import accel as accel_a  # noqa: E402
from src.case_a import energy as energy_a  # noqa: E402
from src.case_b import DT as DT_B  # noqa: E402
from src.case_b import EPS_TARGET, H_TARGET, R0, V0 as V0_B  # noqa: E402
from src.case_b import T_ANALYTIC as T_B  # noqa: E402
from src.case_b import accel as accel_b  # noqa: E402
from src.case_b import specific_energy, specific_h  # noqa: E402
from src.integrators import velocity_verlet_step  # noqa: E402

# History shown on screen (physics itself is not windowed).
WINDOW_PERIODS = 8


def _parse() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Live velocity-Verlet viewer (Ctrl+C to stop).")
    p.add_argument("--case", required=True, choices=["A", "B", "a", "b"], help="A spring or B orbit")
    return p.parse_args()


def main() -> int:
    args = _parse()
    case = args.case.upper()
    if case == "A":
        return _run_a()
    return _run_b()


def _run_a() -> int:
    dt = DT_A
    steps_per_frame = 4  # 0.04 sim-seconds per frame; dt stays 0.01
    window = int(WINDOW_PERIODS * T_A / dt)
    x = np.array(X0, dtype=float)
    v = np.array(V0, dtype=float)
    a = accel_a(x)
    t = 0.0
    ts: deque[float] = deque(maxlen=window)
    xs: deque[float] = deque(maxlen=window)
    Es: deque[float] = deque(maxlen=window)
    ts.append(t)
    xs.append(float(x))
    Es.append(float(energy_a(x, v)))

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    (line_x,) = axes[0].plot([], [], lw=1.2)
    (line_e,) = axes[1].plot([], [], lw=1.2)
    axes[1].axhline(E_TARGET, color="k", ls="--", lw=0.8, label="E = 2")
    axes[0].set_ylabel("x(t)")
    axes[0].set_ylim(-1.3, 1.3)
    axes[0].set_title("Case A — velocity Verlet (Ctrl+C or close window to stop)")
    axes[1].set_ylabel("E(t)")
    axes[1].set_xlabel("t")
    axes[1].set_ylim(1.9, 2.1)
    axes[1].legend(loc="upper right")
    fig.tight_layout()

    def update(_frame: int):
        nonlocal x, v, a, t
        for _ in range(steps_per_frame):
            x, v, a = velocity_verlet_step(x, v, a, accel_a, dt)
            t += dt
            ts.append(t)
            xs.append(float(x))
            Es.append(float(0.5 * K * float(x) ** 2 + 0.5 * M * float(v) ** 2))
        line_x.set_data(ts, xs)
        line_e.set_data(ts, Es)
        axes[0].set_xlim(ts[0], max(ts[-1], ts[0] + dt))
        axes[1].set_xlim(ts[0], max(ts[-1], ts[0] + dt))
        return line_x, line_e

    _animate(fig, update)
    return 0


def _run_b() -> int:
    dt = DT_B
    steps_per_frame = 25  # 0.025 sim-seconds per frame; dt stays 0.001
    window = int(WINDOW_PERIODS * T_B / (dt * steps_per_frame))
    # One orbit of trail is enough to see closure; keep two periods of samples.
    trail = int(2 * T_B / (dt * steps_per_frame))
    r = np.array(R0, dtype=float)
    v = np.array(V0_B, dtype=float)
    a = accel_b(r)
    t = 0.0
    ts: deque[float] = deque(maxlen=window)
    eps: deque[float] = deque(maxlen=window)
    hs: deque[float] = deque(maxlen=window)
    rx: deque[float] = deque(maxlen=trail)
    ry: deque[float] = deque(maxlen=trail)

    def sample() -> None:
        rr = r.reshape(1, 2)
        vv = v.reshape(1, 2)
        ts.append(t)
        eps.append(float(specific_energy(rr, vv)[0]))
        hs.append(float(specific_h(rr, vv)[0]))
        rx.append(float(r[0]))
        ry.append(float(r[1]))

    sample()

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    (line_orb,) = axes[0].plot([], [], lw=0.8)
    axes[0].plot(0, 0, "y*", ms=12)
    (line_e,) = axes[1].plot([], [], lw=1.0)
    (line_h,) = axes[2].plot([], [], lw=1.0)
    axes[1].axhline(EPS_TARGET, color="k", ls="--", lw=0.8)
    axes[2].axhline(H_TARGET, color="k", ls="--", lw=0.8)
    axes[0].set_aspect("equal")
    axes[0].set_xlim(-2.0, 1.0)
    axes[0].set_ylim(-1.2, 1.2)
    axes[0].set_title("orbit")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[1].set_title("ε(t)")
    axes[1].set_ylabel("ε")
    axes[1].set_xlabel("t")
    axes[1].set_ylim(-0.55, -0.45)
    axes[2].set_title("h(t)")
    axes[2].set_ylabel("h")
    axes[2].set_xlabel("t")
    axes[2].set_ylim(0.8, 0.95)
    fig.suptitle("Case B — velocity Verlet (Ctrl+C or close window to stop)")
    fig.tight_layout()

    def update(_frame: int):
        nonlocal r, v, a, t
        for _ in range(steps_per_frame):
            r, v, a = velocity_verlet_step(r, v, a, accel_b, dt)
            t += dt
        sample()
        line_orb.set_data(rx, ry)
        line_e.set_data(ts, eps)
        line_h.set_data(ts, hs)
        axes[1].set_xlim(ts[0], max(ts[-1], ts[0] + dt))
        axes[2].set_xlim(ts[0], max(ts[-1], ts[0] + dt))
        return line_orb, line_e, line_h

    _animate(fig, update)
    return 0


def _animate(fig: plt.Figure, update) -> None:
    anim = FuncAnimation(fig, update, interval=30, cache_frame_data=False, blit=False)
    # Keep a reference so the animation is not garbage-collected.
    fig._live_anim = anim  # type: ignore[attr-defined]
    print("Running until you close the plot or press Ctrl+C.", flush=True)
    if plt.get_backend().lower() == "webagg":
        print("No desktop display — plot is in the browser (Codespaces will offer to forward the port).", flush=True)
    try:
        plt.show()
    except KeyboardInterrupt:
        print("\nStopped.", flush=True)
    finally:
        plt.close(fig)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nStopped.", flush=True)
        raise SystemExit(0)
