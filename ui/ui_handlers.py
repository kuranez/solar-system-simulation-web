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
import panel as pn # For building the web interface
import constants # For simulation constants like scale and colors
from simulation.solarsystem_scale import calculate_scaled_sizes # For updating body sizes based on current scale
from .screen import pygame_surface_to_PNGbuf, draw_frame # For rendering the simulation and converting to PNG for Panel display
from modules.simple_sun_earth_moon import earth_radius_ratio # For maintaining correct size ratio between Earth and Moon in the simple system

def advance_simulation(bodies, state):
    """Advances the simulation by one logical frame.

    To keep close-orbit dynamics stable we integrate using the smallest
    per-body timestep (e.g., moon.TIMESTEP) and perform multiple substeps so
    that the total simulated time per frame is approximately `constants.TIMESTEP`.
    """
    # Determine the smallest integration timestep among dynamic bodies
    dynamic_ts = [getattr(b, 'TIMESTEP', constants.TIMESTEP) for b in bodies if not getattr(b, 'static_body', False)]
    if not dynamic_ts:
        return
    step_dt = min(dynamic_ts)
    # Number of substeps to reach roughly one 'frame' worth of simulated time
    substeps = max(1, int(round(constants.TIMESTEP / step_dt)))

    for _ in range(substeps):
        for body in bodies:
            body.update_position(bodies)
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

def update_proportional_sun_earth_moon(bodies, state, scale, view_cfg):
    # Proportional view: compute a distance_scale that maps 1 AU -> desired pixel distance
    # without mutating physical `body.x` values (which are in meters). This preserves
    # SI-based physics while allowing a proportional visual scaling.
    sun = bodies[0]
    earth = bodies[1]
    moon = bodies[2]

    # Desired Sun-Earth pixel distance at this slider scale
    sun_earth_px = view_cfg.get("sun_earth_base_px", 350) * scale

    # Map 1 AU (meters) to the desired pixel distance
    # distance_scale is pixels per meter
    state["distance_scale"] = sun_earth_px / constants.AU

    # Update visual radii based on the computed distance_scale
    update_body_radii(bodies, state["distance_scale"])
    # Ensure Moon radius scales relative to Earth's visual radius (calculate_scaled_sizes
    # doesn't include the Moon). Keep a minimum pixel size.
    try:
        earth_radius = next(b.radius for b in bodies if getattr(b, 'name', None) == 'Earth')
        for b in bodies:
            if getattr(b, 'name', None) == 'Moon':
                # Physical radius ratio: Moon_radius_m / Earth_radius_m
                phys_ratio = constants.BODIES_DATA.get('Moon', {}).get('radius', constants.BODIES_DATA['Earth']['radius']) / constants.BODIES_DATA['Earth']['radius'] if False else (constants.MOON_DATA['radius'] / constants.BODIES_DATA['Earth']['radius'])
                # Fallback: use known constants if structure differs
                try:
                    phys_ratio = constants.MOON_DATA['radius'] / constants.BODIES_DATA['Earth']['radius']
                except Exception:
                    phys_ratio = 0.27
                b.radius = max(1, int(earth_radius * phys_ratio))
    except StopIteration:
        pass
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
    update_static_scene_scaling(
        bodies,
        state,
        scale,
        scaled_body_names=("Earth",),
        fixed_body_names=("Sun",),
    )


def update_simple_earth_moon(bodies, state, scale, view_cfg):
    update_static_scene_scaling(
        bodies,
        state,
        scale,
        scaled_body_names=("Earth", "Moon"),
    )

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
def on_step(event, screen, bodies, state, color_bg, img_pane):
    """Handles the 'Next Frame' button click."""
    advance_simulation(bodies, state)
    draw_frame(screen, bodies, state, color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def periodic_update(screen, bodies, state, color_bg, img_pane):
    """Function called periodically when the simulation is playing."""
    advance_simulation(bodies,state)
    draw_frame(screen, bodies, state, color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def play_pause(event, state, screen, bodies,color_bg, img_pane, play_button):
    """Handles the 'Play/Pause' button click."""
    if not state['is_playing']:
        state['is_playing'] = True
        play_button.name = "Pause"
        play_button.button_type = "danger"
        # Start periodic updates (e.g., 20 FPS)
        state['callback'] = pn.state.add_periodic_callback(
            lambda: periodic_update(screen, bodies, state, color_bg, img_pane),
            period=50
        )
    else:
        state['is_playing'] = False
        play_button.name = "Play"
        play_button.button_type = "success"
        if state['callback']:
            state['callback'].stop()
            state['callback'] = None

def zoom_in(event, state, current_solarsystem, screen, color_bg, img_pane):
    """Handles the 'Zoom In' button click with full redraw logic."""
    # Increase scale
    state['distance_scale'] *= 1.1 
    # Ensure scale is within a reasonable range
    state['distance_scale'] = min(state['distance_scale'], constants.DEFAULT_SCALE * 0.05)
    
    # Recalculate planet sizes and redraw the frame
    update_body_radii(current_solarsystem, state['distance_scale'])
    draw_frame(screen, current_solarsystem, state, color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def zoom_out(event, state, current_solarsystem, screen, color_bg, img_pane):
    """Handles the 'Zoom Out' button click with full redraw logic."""
    # Decrease scale
    state['distance_scale'] /= 1.1
    # Ensure scale is within a reasonable range
    state['distance_scale'] = max(state['distance_scale'], constants.DEFAULT_SCALE * 10)

    # Recalculate planet sizes and redraw the frame
    update_body_radii(current_solarsystem, state['distance_scale'])
    draw_frame(screen, current_solarsystem, state, color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)