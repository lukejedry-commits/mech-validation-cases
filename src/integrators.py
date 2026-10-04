"""Fixed-timestep integrators."""

from __future__ import annotations

from typing import Callable

import numpy as np


def velocity_verlet_step(
    x: np.ndarray,
    v: np.ndarray,
    a: np.ndarray,
    accel: Callable[[np.ndarray], np.ndarray],
    dt: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """One velocity-Verlet step. Returns x, v, a at the new time."""
    x_new = x + v * dt + 0.5 * a * dt * dt
    a_new = accel(x_new)
    v_new = v + 0.5 * (a + a_new) * dt
    return x_new, v_new, a_new


def velocity_verlet(
    x0: np.ndarray,
    v0: np.ndarray,
    accel: Callable[[np.ndarray], np.ndarray],
    dt: float,
    n_steps: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Velocity Verlet. Returns t, x[n_steps+1], v[n_steps+1]."""
    x = np.empty((n_steps + 1,) + np.shape(x0), dtype=float)
    v = np.empty((n_steps + 1,) + np.shape(v0), dtype=float)
    t = np.arange(n_steps + 1, dtype=float) * dt
    x[0] = x0
    v[0] = v0
    a = accel(x[0])
    for i in range(n_steps):
        x[i + 1], v[i + 1], a = velocity_verlet_step(x[i], v[i], a, accel, dt)
    return t, x, v


def explicit_euler(
    x0: np.ndarray,
    v0: np.ndarray,
    accel: Callable[[np.ndarray], np.ndarray],
    dt: float,
    n_steps: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Explicit (forward) Euler — known-bad for energy conservation."""
    x = np.empty((n_steps + 1,) + np.shape(x0), dtype=float)
    v = np.empty((n_steps + 1,) + np.shape(v0), dtype=float)
    t = np.arange(n_steps + 1, dtype=float) * dt
    x[0] = x0
    v[0] = v0
    for i in range(n_steps):
        a = accel(x[i])
        x[i + 1] = x[i] + v[i] * dt
        v[i + 1] = v[i] + a * dt
    return t, x, v
