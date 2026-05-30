# simulation/

Purpose
- Contains the physics and scaling logic used by the simulation engine. This folder is responsible for numerical updates to body positions, unit conversions, and any utility functions for simulating orbits.

Key files
- `physics.py` — integration and force calculations (e.g. gravitational acceleration, time-stepping).
- `scale.py` — helpers to map SI distances (meters) to pixels and to compute default scales used by views.

How it connects
- The generator modules set initial physical states (positions, velocities) for `Body` instances.
- The simulation timestep and physics integrator update those `Body` objects over time.
- `scale.py` is consulted by `app.py` and `ui` code to determine `state['base_distance_scale']` and to produce stable pixel mappings for rendering.

Developer notes
- Keep physics code separate from rendering. Physics should operate purely on physical units (meters, seconds) and not touch pixel values.
- When changing integrators or timestep behavior, check `ui/ui_handlers.py` and `app.py` for places that assume a fixed `frame_period` or time scaling.