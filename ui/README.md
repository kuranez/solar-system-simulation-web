# ui/

Purpose
- Houses all UI-specific code: canvas rendering, HUD drawing, CSS, and the server-side handlers that bridge simulation state to the browser.

Key files
- `canvas.py` — `SimulationCanvas` (a `pn.reactive.ReactiveHTML` widget) and client-side JS template that draws the trail layer and HUD layer. This file contains the client wheel-zoom and pointer-drag logic and the `sync_canvas_frame()` helper used by `app.py` to push frames.
- `screen.py` — server-side routines to render the simulation into images (Pygame) when used, and helpers to compute frame payloads.
- `hud.py` — utilities and layout for drawing on-screen HUD elements (scale text, time, legend) used by the client and server.
- `ui_handlers.py` — server-side control handlers (play/pause, speed adjustments, `apply_zoom_for_view()` and per-view `zoom_updater` hooks).
- `css.py` — theme and layout CSS injected into the Panel app.
- `templates/` — HTML/CSS snippets used by the ReactiveHTML widget.

Data flow (high level)
1. `app.py` maintains authoritative `state` (distance_scale, offsets, play state, frame token).
2. On each frame or on view changes, `sync_canvas_frame()` packages a compact payload (bodies + distance/offsets + scene token + optional `scale_text`) and sends it to the browser-side `SimulationCanvas`.
3. The browser JS unpacks the payload and draws two canvas layers: one for trails (persistent between frames until a reset) and one for HUD/bodies. Client-side transforms (zoom/pan) are applied to the drawing context so the server can remain the authoritative source of body coordinates while the user can pan/zoom locally.

Developer notes
- Client-side zoom/pan: the wheel and pointer handlers implemented in `canvas.py` update a local transform (`viewZoom`/`viewOffset`) so immediate interactions feel responsive. If you need persistent zoom synced back to the server, update `state['distance_scale']` and re-send a frame.
- To add HUD elements, modify the `frame_data` JS template in `SimulationCanvas` and add values to the Python `build_frame_data()` payload.
- When debugging rendering issues, inspect the `scene_token` payload — changing it forces the client to clear persistent trail canvas and redraw from scratch.