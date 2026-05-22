# screen.py - Handles off-screen rendering of the solar system simulation using Pygame and conversion to PNG for Panel display
# v.1.1 - Refactored from app.py

# Importing necessary libraries
import io
from PIL import Image
import numpy as np
import pygame

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

# Function to draw the current frame of the simulation
def draw_frame(screen, bodies, scale, screen_offset_x, screen_offset_y, color_bg):
    # Clear screen
    screen.fill(color_bg)
    # Draw all objects
    for body in bodies:
        body.draw(screen, scale, screen_offset_x, screen_offset_y)