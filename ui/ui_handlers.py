""" ui/ui_handlers.py 

    # Method overview:

# advance_simulation: 
        Advances the simulation by one step for all bodies.
# update_simple_body_sizes: 
        Updates the sizes of Sun, Earth, and Moon based on a size factor.
# update_proportional_sun_earth_moon: 
        Updates the positions and sizes of the Sun, Earth, and Moon in the 
        simple system based on the current scale and view configuration.
#  update_body_radii: 
        Updates the radius of each body based on the current distance scale 
        using the calculate_scaled_sizes function.
# on_step: 
        Handles the 'Next Frame' button click to advance the simulation and 
        redraw the frame.
# periodic_update: 
        Function called periodically when the simulation is playing to 
        advance the simulation and redraw the frame.
# play_pause: 
        Handles the 'Play/Pause' button click to start or stop periodic 
        updates of the simulation.
# zoom_in: 
        Handles the 'Zoom In' button click to increase the distance scale, update body sizes, and redraw the frame.
# zoom_out: 
        Handles the 'Zoom Out' button click to decrease the distance scale, update body sizes, and redraw the frame.
"""

# Importing necessary libraries
import time

import panel as pn # For building the web interface
import constants # For simulation constants like scale and colors
from simulation.scale import calculate_scaled_sizes # For updating body sizes based on current scale
from .canvas import sync_canvas_frame # For browser-side canvas rendering


SPEED_STEP_MS = 10
MIN_FRAME_PERIOD = 10
MAX_FRAME_PERIOD = 500
SIMULATION_SPEED_PRESETS = [
    {"simulation_timestep": 1.0 * constants.TIMESTEP, "render_stride": 1.0},
    {"simulation_timestep": 1.5 * constants.TIMESTEP, "render_stride": 1.0},
    {"simulation_timestep": 2 * constants.TIMESTEP, "render_stride": 1.0},
    {"simulation_timestep": 3 * constants.TIMESTEP, "render_stride": 1.0},
    {"simulation_timestep": 7 * constants.TIMESTEP, "render_stride": 1.0},
    {"simulation_timestep": 7 * constants.TIMESTEP, "render_stride": 1.5},
    {"simulation_timestep": 7 * constants.TIMESTEP, "render_stride": 1.75},
    {"simulation_timestep": 7 * constants.TIMESTEP, "render_stride": 2.0},
]


def _restart_periodic_callback(bodies, state, color_bg, canvas_view, play_button):
    if state.get('callback'):
        state['callback'].stop()
        state['callback'] = None

    state['last_tick_time'] = time.monotonic()
    state['render_skip_counter'] = 0.0

    state['callback'] = pn.state.add_periodic_callback(
        lambda: periodic_update(bodies, state, color_bg, canvas_view),
        period=state.get('frame_period', 10)
    )


def _set_frame_period(state, period_ms):
    state['frame_period'] = max(MIN_FRAME_PERIOD, min(MAX_FRAME_PERIOD, int(period_ms)))

def _step_simulation_timestep(state, direction):
    current_timestep = float(state.get('simulation_timestep', constants.TIMESTEP))
    current_stride = float(state.get('render_stride', 1.0))
    current_index = 0
    for index, preset in enumerate(SIMULATION_SPEED_PRESETS):
        if preset["simulation_timestep"] == current_timestep and preset["render_stride"] == current_stride:
            current_index = index
            break
        if preset["simulation_timestep"] <= current_timestep:
            current_index = index

    new_index = max(0, min(len(SIMULATION_SPEED_PRESETS) - 1, current_index + direction))
    preset = SIMULATION_SPEED_PRESETS[new_index]
    state['simulation_timestep'] = preset["simulation_timestep"]
    state['render_stride'] = preset["render_stride"]
    state['render_skip_counter'] = 0.0
    return preset


def _sync_speed_status(state):
    # Removed as speed status is now only displayed in the HUD.
    pass





def increase_simulation_speed(event, state, bodies, color_bg, canvas_view, play_button):
    """Increase simulation speed by raising the simulated time advanced per frame."""
    _step_simulation_timestep(state, +1)
    refresh_speed_display(canvas_view, state)

    sync_canvas_frame(
        canvas_view,
        bodies,
        state,
        color_bg,
        scene_token=state.get('scene_token', 1),
        reset=False,
    )


def decrease_simulation_speed(event, state, bodies, color_bg, canvas_view, play_button):
    """Decrease simulation speed by lowering the simulated time advanced per frame."""
    _step_simulation_timestep(state, -1)
    refresh_speed_display(canvas_view, state)

    sync_canvas_frame(
        canvas_view,
        bodies,
        state,
        color_bg,
        scene_token=state.get('scene_token', 1),
        reset=False,
    )

def advance_simulation(bodies, state, time_scale=1.0):
    """Advances the simulation by one logical frame.

    To keep close-orbit dynamics stable we integrate using the smallest
    per-body timestep (e.g., moon.TIMESTEP) and perform multiple substeps so
    that the total simulated time per frame is approximately `constants.TIMESTEP`.
    """
    # Determine the smallest integration timestep among dynamic bodies
    dynamic_ts = [getattr(b, 'TIMESTEP', constants.TIMESTEP) for b in bodies if not getattr(b, 'static_body', False)]
    if not dynamic_ts:
        return
    frame_timestep = float(state.get('simulation_timestep', constants.TIMESTEP))
    simulation_timestep = frame_timestep * max(0.0, float(time_scale))
    base_step_dt = min(dynamic_ts)
    substeps = max(1, int(round(simulation_timestep / base_step_dt)))
    step_dt = simulation_timestep / substeps

    for _ in range(substeps):
        for body in bodies:
            body.update_position(bodies, timestep=step_dt, frame_timestep=frame_timestep)
        # accumulate simulated time
        state['total_elapsed_time'] = state.get('total_elapsed_time', 0.0) + step_dt

def update_simple_body_sizes(bodies, size_factor):
    earth_radius_ratio = constants.BODIES_DATA["Earth"]["radius"] / constants.BODIES_DATA["Moon"]["radius"]

    for body in bodies:
        if body.name == "Sun":
            body.radius = 2
        elif body.name == "Earth":
            body.radius = max(1, int(constants.BASE_SIZE * size_factor))
        elif body.name == "Moon":
            body.radius = max(1, int((constants.BASE_SIZE * size_factor) / earth_radius_ratio))

def scale_bodies_from_original_radius(bodies, scale, body_names=None):
    """Scale body radii from each body's `original_radius` baseline.

    This keeps zoom logic consistent across simple views while leaving the
    physics-driven positions untouched.
    """
    body_names = set(body_names) if body_names is not None else None

    for body in bodies:
        if body_names is not None and body.name not in body_names:
            continue
        if hasattr(body, "original_radius"):
            body.radius = max(1, int(body.original_radius * scale))

def update_proportional_sun_earth_moon(bodies, state, scale, view_cfg):
    # Proportional view: compute a distance_scale that maps 1 AU -> desired pixel distance
    # without mutating physical `body.x` values (which are in meters). This preserves
    # SI-based physics while allowing a proportional visual scaling.
    # Desired Sun-Earth pixel distance at this slider scale
    sun_earth_px = view_cfg.get("sun_earth_base_px", 350) * scale

    # Map 1 AU (meters) to the desired pixel distance
    # distance_scale is pixels per meter
    state["distance_scale"] = sun_earth_px / constants.AU

    # Update visual radii from the shared pixel baseline.
    scale_bodies_from_original_radius(bodies, scale, body_names=("Earth", "Moon"))
    # Compute a moon-specific visual distance_scale so the Earth-Moon separation
    # matches the desired pixel ratio in this proportional view. This anchors the
    # Moon to Earth visually while keeping physics in meters.
    try:
        earth = next(b for b in bodies if getattr(b, 'name', None) == 'Earth')
        moon = next(b for b in bodies if getattr(b, 'name', None) == 'Moon')
        desired_moon_px = view_cfg.get('sun_earth_base_px', 350) * view_cfg.get('earth_moon_ratio', 0.257) * scale
        # enforce a sensible minimum pixel separation so the Moon never visually collapses
        desired_moon_px = max(desired_moon_px, view_cfg.get('moon_min_px', 8))
        delta_m = abs(moon.x - earth.x)
        if delta_m > 0:
            moon_visual_scale = desired_moon_px / delta_m
            moon.visual_distance_scale = moon_visual_scale
    except StopIteration:
        # no earth/moon pair in this view
        pass
    # Remove any leftover overrides on non-moon bodies
    for b in bodies:
        if getattr(b, 'name', None) != 'Moon' and hasattr(b, 'visual_distance_scale'):
            delattr(b, 'visual_distance_scale')


def update_static_scene_scaling(bodies, state, scale, scaled_body_names, fixed_body_names=()):
    """Scale preset scenes from their original positions and radii."""
    fixed_body_names = set(fixed_body_names)
    scaled_body_names = set(scaled_body_names)

    for body in bodies:
        if hasattr(body, "original_x") and body.name not in fixed_body_names:
            body.x = body.original_x * scale
            body.y = body.original_y * scale

        if hasattr(body, "original_radius") and body.name in scaled_body_names:
            body.radius = max(1, int(body.original_radius * scale))

    state["distance_scale"] = 1.0


def update_simple_sun_earth(bodies, state, scale, view_cfg):
    state["distance_scale"] = state["base_distance_scale"] * scale
    scale_bodies_from_original_radius(bodies, scale, body_names=("Earth",))


def update_simple_earth_moon(bodies, state, scale, view_cfg):
    state["distance_scale"] = state["base_distance_scale"] * scale
    scale_bodies_from_original_radius(bodies, scale, body_names=("Earth", "Moon"))

def update_body_radii(current_solarsystem, distance_scale):
    """Updates the radius of each body based on the current distance scale."""

    scaled_sizes = calculate_scaled_sizes(
        distance_scale
    )

    for body in current_solarsystem:

        if getattr(body, "static_body", False):
            continue

        if (
            hasattr(body, "name")
            and body.name in scaled_sizes
        ):

            body.radius = max(
                1,
                int(scaled_sizes[body.name])
            )


def apply_zoom_for_view(current_solarsystem, state, scale, view_cfg):
    """Apply the active view's zoom behavior and redraw state."""
    updater = view_cfg.get("zoom_updater")
    mode = view_cfg.get("scale_mode", "distance")

    if updater is not None:
        updater(current_solarsystem, state, scale, view_cfg)
    elif mode == "distance":
        state["distance_scale"] = state["base_distance_scale"] * scale
        update_body_radii(current_solarsystem, state["distance_scale"])

# Event handlers for UI buttons
def on_step(event, bodies, state, color_bg, canvas_view):
    """Handles the 'Next Frame' button click."""
    advance_simulation(bodies, state)
    sync_canvas_frame(
        canvas_view,
        bodies,
        state,
        color_bg,
        scene_token=state.get('scene_token', 1),
        reset=False,
    )

def periodic_update(bodies, state, color_bg, canvas_view):
    """Function called periodically when the simulation is playing."""
    now = time.monotonic()
    last_tick_time = state.get('last_tick_time', now)
    state['last_tick_time'] = now
    nominal_period = max(1, int(state.get('frame_period', 10))) / 1000.0
    elapsed = max(0.0, now - last_tick_time)
    time_scale = elapsed / nominal_period if nominal_period > 0 else 1.0
    advance_simulation(bodies, state, time_scale=time_scale)
    render_stride = max(1.0, float(state.get('render_stride', 1.0)))
    render_skip_counter = float(state.get('render_skip_counter', 0.0)) + 1.0
    if render_skip_counter < render_stride:
        state['render_skip_counter'] = render_skip_counter
        return

    state['render_skip_counter'] = render_skip_counter - render_stride
    sync_canvas_frame(
        canvas_view,
        bodies,
        state,
        color_bg,
        scene_token=state.get('scene_token', 1),
        reset=False,
    )

def play_pause(event, state, bodies, color_bg, canvas_view, play_button):
    """Handles the 'Play/Pause' button click."""
    if not state['is_playing']:
        state['is_playing'] = True
        play_button.name = "Pause"
        play_button.icon = "player-pause"
        play_button.button_type = "danger"
        # Start periodic updates. Use a configurable period to lower CPU/network
        # pressure in slower browsers (Firefox). Default to 80ms (~12.5 FPS).
        _restart_periodic_callback(bodies, state, color_bg, canvas_view, play_button)
    else:
        state['is_playing'] = False
        play_button.name = "Play"
        play_button.icon = "player-play"
        play_button.button_type = "success"
        if state['callback']:
            state['callback'].stop()
            state['callback'] = None
        state['last_tick_time'] = None

def stop_and_reset(event, state, bodies, color_bg, canvas_view, play_button):
    """Stop playback and reset the elapsed simulation time."""
    if state.get('is_playing'):
        state['is_playing'] = False
        play_button.name = "Play"
        play_button.button_type = "success"
        if state.get('callback'):
            state['callback'].stop()
            state['callback'] = None

    state['total_elapsed_time'] = 0.0
    state['scene_token'] = state.get('scene_token', 1) + 1
    state['render_skip_counter'] = 0.0
    state['last_tick_time'] = None
    sync_canvas_frame(
        canvas_view,
        bodies,
        state,
        color_bg,
        scene_token=state['scene_token'],
        reset=True,
    )

def zoom_in(event, state, current_solarsystem, color_bg, canvas_view):
    """Handles the 'Zoom In' button click with full redraw logic."""
    # Increase scale
    state['distance_scale'] *= 1.1 
    # Ensure scale is within a reasonable range
    state['distance_scale'] = min(state['distance_scale'], constants.DEFAULT_SCALE * 0.05)
    
    # Recalculate planet sizes and redraw the frame
    update_body_radii(current_solarsystem, state['distance_scale'])
    state['scene_token'] = state.get('scene_token', 1) + 1
    sync_canvas_frame(
        canvas_view,
        current_solarsystem,
        state,
        color_bg,
        scene_token=state['scene_token'],
        reset=True,
    )

def zoom_out(event, state, current_solarsystem, color_bg, canvas_view):
    """Handles the 'Zoom Out' button click with full redraw logic."""
    # Decrease scale
    state['distance_scale'] /= 1.1
    # Ensure scale is within a reasonable range
    state['distance_scale'] = max(state['distance_scale'], constants.DEFAULT_SCALE * 10)

    # Recalculate planet sizes and redraw the frame
    update_body_radii(current_solarsystem, state['distance_scale'])
    state['scene_token'] = state.get('scene_token', 1) + 1
    sync_canvas_frame(
        canvas_view,
        current_solarsystem,
        state,
        color_bg,
        scene_token=state['scene_token'],
        reset=True,
    )

def refresh_speed_display(canvas_view, state):
    frame_data = dict(canvas_view.frame_data or {})
    frame_data["simulation_timestep"] = state["simulation_timestep"]

    stride = state.get("render_stride", 1.0)

    if stride > 1:
        frame_data["speed_text"] = (
            f"Step: {state['simulation_timestep']/86400:.1f} d/frame "
            f"| Render x{stride:g}"
        )
    else:
        frame_data["speed_text"] = (
            f"Step: {state['simulation_timestep']/86400:.1f} d/frame"
        )

    canvas_view.frame_data = frame_data