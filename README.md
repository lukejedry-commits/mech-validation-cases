# mech-validation-cases

Case A (undamped spring) and Case B (Kepler orbit, fixed sun) — velocity Verlet primary, explicit Euler on A as known-bad control.

## Codespaces

Open this repo in GitHub Codespaces, then:

```bash
pip install -r requirements.txt   # already run by postCreateCommand
python run_all.py
```

Plots land in `plots/`. Exit code 0 means Verlet A/B pass and Euler-A fails conservation as required.

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
