# ui_handlers.py
# Module to handle user interface interactions for the solar system simulation
# v.1.1 - Refactored from app.py

# Importing necessary libraries
import panel as pn

from simulation import constants # For building the web interface
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