# objects/

Purpose
- Defines the `Body` model and related objects used by the simulation. Encapsulates physical state (mass, position, velocity), visual properties (color, radius), and helper methods for screen projection and drawing.

Key files
- `base.py` — `Body` class and core helpers (screen projection, orbit tracking, trail storage).
- `planet.py`, `moon.py`, `asteroid.py` — convenience subclasses or builders and helpers.
- `presets/` — pre-configured `Body` parameters for common bodies (e.g., `presets/sun.py`, `presets/earth.py`).

How it connects
- Module generators instantiate `Body` objects (or objects with the same expected API) and set physical/visual parameters.
- Server rendering code in `ui/screen.py` and `ui/canvas.py` expects each object to expose screen coordinates (via `_screen_position()` or similar) and drawing-related attributes.
- Trails (orbit history) are collected on the server side and serialized into the frame payload for the client to draw.

Developer notes
- If you extend `Body`, preserve the `_screen_position(distance_scale, screen_offset_x, screen_offset_y)` API so existing UI code continues to work.
- Prefer storing physical units (meters) internally; only convert to pixels at render time.
- To tune visuals, adjust the `visual_distance_scale` attribute on a per-body basis rather than changing global physics values.