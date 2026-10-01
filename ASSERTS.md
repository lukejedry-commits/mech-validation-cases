# Validation assert table (frozen — do not soften)

## Case A (Verlet, dt=0.01, ≥10 periods)
- Period: |T − π| / π ≤ 1e−3
- Amplitude: max|x| within 1e−3 of 1
- Energy: |E(t) − 2| ≤ 1e−3 for all samples (bounded, no secular growth)

## Case A Euler control (same dt)
- Energy must grow: max E − min E > 0.1 over the run (pass only if conservation fails this way)

## Case B (Verlet, dt=0.001, ≥10 periods)
- Period: |T − 2π| / 2π ≤ 1e−3
- Orbit closure: |r(T) − r₀| ≤ 1e−2
- Specific energy: |ε(t) + 1/2| ≤ 1e−3 for all samples
- Specific angular momentum: |h(t) − √3/2| ≤ 1e−3 for all samples
