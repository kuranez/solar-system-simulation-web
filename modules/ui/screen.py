# screen.py
#  Handles off-screen rendering of the solar system simulation using Pygame and conversion to PNG for Panel display
# v.1.3 - Refactored from non-web version of the app, added HUD rendering and Scaling

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
def draw_frame(screen, bodies, scale, screen_offset_x, screen_offset_y, color_bg):
    # Clear screen
    screen.fill(color_bg)
    # Draw all objects
    for body in bodies:
        body.draw(screen, scale, screen_offset_x, screen_offset_y)
    # Render the HUD
    render_hud(screen, bodies)

# Function to convert Pygame surface to PNG buffer for Panel display
def pygame_surface_to_PNGbuf(surface):
    """Converts a Pygame surface to a PNG buffer for Panel display."""
    arr = pygame.surfarray.array3d(surface)
    arr = np.transpose(arr, (1, 0, 2))  # Pygame (w,h,3) -> (h,w,3)
    img = Image.fromarray(arr)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


