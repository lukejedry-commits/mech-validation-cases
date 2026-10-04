# mech-validation-cases

Case A (undamped spring) and Case B (Kepler orbit, fixed sun) — velocity Verlet primary, explicit Euler on A as known-bad control.

## Codespaces

Open this repo in GitHub Codespaces, then:

```bash
pip install -r requirements.txt   # already run by postCreateCommand
python run_all.py
```

Plots land in `plots/`. Exit code 0 means Verlet A/B pass and Euler-A fails conservation as required.

## Live viewer (runs until you stop it)

One file, `live.html`. Open it in a browser. Nothing to install, and no port to forward. In Codespaces, download `live.html` and open that download in Chrome.

Case A starts on its own. Use the buttons for Case A, Case B, or Stop. Closing the tab also stops it.

Same velocity Verlet step as `src/integrators.py`, same `dt` (0.01 for A, 0.001 for B) and the same initial conditions. The frame gap is not the timestep. Explicit Euler is not on this page. The frozen checks stay on `python run_all.py`.

The time axis shows the last 8 periods so the plot stays readable. The integration itself does not stop. A slow phase drift with flat energy is expected.

## Spec (frozen)

| | Case A | Case B | Euler-A control |
|---|---|---|---|
| Integrator | velocity Verlet | velocity Verlet | explicit Euler |
| `dt` | 0.01 | 0.001 | 0.01 |
| Duration | ≥10 periods | ≥10 periods | same as A |

See `ASSERTS.md` for the Validation Engineer freeze table.

## Local (non-Codespaces)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_all.py
```
