# modules/

Purpose
- Contains high-level simulation generators. Each module produces a list of `Body` objects and any view-specific configuration used by the web UI.

Key files
- `simple_sun_earth.py`, `simple_earth_moon.py`, `simple_sun_earth_moon.py`, `simple_solar_system.py`

What each module does
- Export a factory function (e.g. `create_sun_earth_system()`) that returns a list of `Body`-like objects configured with physical positions (meters), visual radii (px), colors, and optional orbit traces.
- Set any view-specific constants (for example, `sun_earth_base_px`, `earth_moon_ratio`) that the app may use to initialize `state['base_distance_scale']` or to drive `zoom_updater` callbacks.

How modules are used
- `app.py` selects a generator from `SIMULATION_VIEWS` and calls the generator to build the `current_solarsystem` list.
- The app passes that list to `sync_canvas_frame()` (via `SimulationCanvas`) to render frames.
- Modules provide the authoritative physical arrangement; conversions to screen pixels are handled by `Body._screen_position()` and the UI rendering code.

Developer notes
- To add a new scenario, create a new generator function that returns `Body` instances and add an entry to `SIMULATION_VIEWS` in `app.py` with appropriate `base_scale` and `scale_mode`.
- Keep physical distances in SI (meters) and let `constants` + `scale` convert to pixels where appropriate.