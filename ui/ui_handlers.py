"""" ui/ui_handlers.py 

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
    """Advances the simulation by one step for all bodies."""
    if not all(getattr(body, "static_body", False) for body in bodies):
        state['total_elapsed_time'] += constants.TIMESTEP
    for body in bodies:
        body.update_position(bodies)

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
    sun = bodies[0]
    earth = bodies[1]
    moon = bodies[2]

    sun_earth_px = view_cfg["sun_earth_base_px"] * scale
    earth_moon_px = sun_earth_px * view_cfg["earth_moon_ratio"]

    earth_radius = max(1, int(constants.BASE_SIZE * scale))
    moon_radius = max(1, int(earth_radius / earth_radius_ratio))

    earth.x = sun_earth_px
    earth.radius = earth_radius

    moon.x = earth.x + earth_moon_px
    moon.radius = moon_radius

    state["distance_scale"] = 1.0

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
    draw_frame(screen, current_solarsystem, state['distance_scale'], state['offset_x'], state['offset_y'], color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def zoom_out(event, state, current_solarsystem, screen, color_bg, img_pane):
    """Handles the 'Zoom Out' button click with full redraw logic."""
    # Decrease scale
    state['distance_scale'] /= 1.1
    # Ensure scale is within a reasonable range
    state['distance_scale'] = max(state['distance_scale'], constants.DEFAULT_SCALE * 10)

    # Recalculate planet sizes and redraw the frame
    update_body_radii(current_solarsystem, state['distance_scale'])
    draw_frame(screen, current_solarsystem, state['distance_scale'], state['offset_x'], state['offset_y'], color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)