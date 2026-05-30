""" ui/screen.py

    # Handles off-screen rendering of the solar system simulation 
    # using Pygame and conversion to PNG for Panel display

"""

# Importing necessary libraries
import io
from PIL import Image
import numpy as np
import pygame
from .hud import render_hud
import constants


# Function to create the Pygame screen (off-screen)
def create_screen():
    """Initializes and returns the Pygame screen."""
    pygame.init()
    return pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

# Function to draw the current frame of the simulation
def draw_frame(screen, bodies, state, color_bg=constants.COLOR_BACKGROUND):
    # Clear screen
    screen.fill(color_bg)

    # Get values from state
    distance_scale = state['distance_scale']
    screen_offset_x = state['offset_x']
    screen_offset_y = state['offset_y']

    # Draw all objects
    for body in bodies:
        body.draw(screen, distance_scale, screen_offset_x, screen_offset_y)
    
    # Render the HUD
    render_hud(screen, bodies, state)

# Function to convert Pygame surface to PNG buffer for Panel display
def pygame_surface_to_PNGbuf(surface):
    """Converts a Pygame surface to a PNG buffer for Panel display."""
    raw_pixels = pygame.image.tostring(surface, "RGB", False)
    img = Image.frombytes("RGB", surface.get_size(), raw_pixels)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG", compress_level=1)
    return buffer.getvalue()


