# ui_handlers.py
# Module to handle user interface interactions for the solar system simulation
# v.1.3 - Buttons for Play/Pause, Zoom In/Out, and periodic updates for live simulation

# Importing necessary libraries
import panel as pn

from simulation import constants # For building the web interface
from simulation.solarsystem_scale import calculate_scaled_sizes # For updating body sizes based on current scale
from .screen import pygame_surface_to_PNGbuf, draw_frame # For rendering the simulation and converting to PNG for Panel display


def advance_simulation(bodies):
    """Advances the simulation by one step for all bodies."""
    for body in bodies:
        body.update_position(bodies)

def on_step(event, screen, bodies, scale, offset_x, offset_y, color_bg, img_pane):
    """Handles the 'Next Frame' button click."""
    advance_simulation(bodies)
    draw_frame(screen, bodies, scale, offset_x, offset_y, color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def periodic_update(screen, bodies, scale, offset_x, offset_y, color_bg, img_pane):
    """Function called periodically when the simulation is playing."""
    advance_simulation(bodies)
    draw_frame(screen, bodies, scale, offset_x, offset_y, color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def play_pause(event, state, screen, bodies, scale, offset_x, offset_y, color_bg, img_pane, play_button):
    """Handles the 'Play/Pause' button click."""
    if not state['is_playing']:
        state['is_playing'] = True
        play_button.name = "Pause"
        play_button.button_type = "danger"
        # Start periodic updates (e.g., 20 FPS)
        state['callback'] = pn.state.add_periodic_callback(
            lambda: periodic_update(screen, bodies, scale, offset_x, offset_y, color_bg, img_pane),
            period=50
        )
    else:
        state['is_playing'] = False
        play_button.name = "Play"
        play_button.button_type = "success"
        if state['callback']:
            state['callback'].stop()
            state['callback'] = None

def update_body_radii(bodies, scale):
    """Updates the radius of each body based on the current scale."""
    scaled_sizes = calculate_scaled_sizes(scale)
    for body in bodies:
        if hasattr(body, "name") and body.name in scaled_sizes:
            body.radius = scaled_sizes[body.name]


def zoom_in(event, state, bodies, screen, img_pane):
    """Handles the 'Zoom In' button click with full redraw logic."""
    # Increase scale
    state['scale'] *= 1.1
    # Ensure scale is within a reasonable range
    state['scale'] = min(state['scale'], constants.DEFAULT_SCALE * 0.05)
    
    # Recalculate planet sizes and redraw the frame
    update_body_radii(bodies, state['scale'])

    # obtain background color from state (fallback to black)
    color_bg = state.get('color_bg')
    draw_frame(screen, bodies, state['scale'], state['offset_x'], state['offset_y'], color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

def zoom_out(event, state, bodies, screen, img_pane):
    """Handles the 'Zoom Out' button click with full redraw logic."""
    # Decrease scale
    state['scale'] /= 1.1
    # Ensure scale is within a reasonable range
    state['scale'] = max(state['scale'], constants.DEFAULT_SCALE * 10)

    # Recalculate planet sizes and redraw the frame
    update_body_radii(bodies, state['scale'])
    # obtain background color from state (fallback to black)
    color_bg = state.get('color_bg')
    draw_frame(screen, bodies, state['scale'], state['offset_x'], state['offset_y'], color_bg)
    img_pane.object = pygame_surface_to_PNGbuf(screen)