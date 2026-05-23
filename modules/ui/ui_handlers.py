# ui_handlers.py
# Module to handle user interface interactions for the solar system simulation
# v.1.7 - Adjusted scaling logic for planet sizes based on current zoom level
# author: kuranez

# Importing necessary libraries
import panel as pn # For building the web interface
import constants # For simulation constants like scale and colors
from simulation.solarsystem_scale import calculate_scaled_sizes # For updating body sizes based on current scale
from .screen import pygame_surface_to_PNGbuf, draw_frame # For rendering the simulation and converting to PNG for Panel display


def advance_simulation(bodies):
    """Advances the simulation by one step for all bodies."""
    for body in bodies:
        body.update_position(bodies)

def update_body_radii(current_solarsystem, distance_scale):
    """Updates the radius of each body based on the current distance scale."""

    scaled_sizes = calculate_scaled_sizes(
        distance_scale
    )

    for body in current_solarsystem:

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
    advance_simulation(bodies)
    draw_frame(screen, bodies, state['distance_scale'], state['offset_x'], state['offset_y'], color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def periodic_update(screen, bodies, state, color_bg, img_pane):
    """Function called periodically when the simulation is playing."""
    advance_simulation(bodies)
    draw_frame(screen, bodies, state['distance_scale'], state['offset_x'], state['offset_y'], color_bg)
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
    state['distance_scale'] = min(state['distance_scale'], constants.DEFAULT_SCALE * 10)
    
    # Recalculate planet sizes and redraw the frame
    update_body_radii(current_solarsystem, state['distance_scale'])
    draw_frame(screen, current_solarsystem, state['distance_scale'], state['offset_x'], state['offset_y'], color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def zoom_out(event, state, current_solarsystem, screen, color_bg, img_pane):
    """Handles the 'Zoom Out' button click with full redraw logic."""
    # Decrease scale
    state['distance_scale'] /= 1.1
    # Ensure scale is within a reasonable range
    state['distance_scale'] = max(state['distance_scale'], constants.DEFAULT_SCALE * 0.05)

    # Recalculate planet sizes and redraw the frame
    update_body_radii(current_solarsystem, state['distance_scale'])
    draw_frame(screen, current_solarsystem, state['distance_scale'], state['offset_x'], state['offset_y'], color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)