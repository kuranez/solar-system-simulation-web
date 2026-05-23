# Solar System Simulation Web (step-by-step)

# This is a Panel-based web application that simulates the solar system step-by-step.
# It uses Pygame for off-screen rendering and Panel for the web interface. The simulation includes
# the Sun, planets, and an asteroid belt. Users can advance the simulation one frame at a time by clicking a button.

# version: 1.1 - Initial creation (Step by Step, Sun and Earth only)
# author: kuranez

# Importing system libraries
import io # For in-memory byte streams
import sys # For modifying the Python path to include the simulation package
import os # For handling file paths

# Add directories to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'simulation')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

# Importing necessary libraries
import numpy as np # For numerical operations and array handling
import panel as pn # For building the web interface
from PIL import Image # For image processing and conversion between Pygame surfaces and PNG format
import pygame # For off-screen rendering of the solar system simulation

# Importing from the simulation package
import constants
from solarsystem_sim import Planet, Sun
from modules.simple_sun_and_earth import create_sun_and_earth


# Initialize Panel extension
pn.extension()

# Pygame initialization (off-screen)
pygame.display.init()
width, height = 1600, 740  # Default dimensions, can be adjusted as needed
screen = pygame.Surface((width, height))
screen.fill(constants.COLOR_BACKGROUND)  # Fill with background color

# Solar system initialization, FULL (later)
# solarsystem = create_solarsystem()
# major_asteroids = create_major_asteroids()
# asteroids = create_asteroid_belt(num_asteroids=200)
# current_solarsystem = solarsystem + major_asteroids + asteroids

# Solar system initialization, Sun and Earth (only for now)
current_solarsystem = create_sun_and_earth()

# State variables for app
scale = constants.DEFAULT_SCALE
screen_offset_x = width // 2
screen_offset_y = height // 2

def pygame_surface_to_pngbuf(surface):
    arr = pygame.surfarray.array3d(surface)
    arr = np.transpose(arr, (1, 0, 2))  # Pygame (w,h,3) -> (h,w,3)
    img = Image.fromarray(arr)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def advance_simulation():
    # Advance the simulation one step
    for body in current_solarsystem:
        body.update_position(current_solarsystem)

def draw_frame():
    # Clear screen
    screen.fill(constants.COLOR_BACKGROUND)
    # Draw all objects
    for body in current_solarsystem:
        body.draw(screen, scale, screen_offset_x, screen_offset_y)
    return pn.pane.PNG(pygame_surface_to_pngbuf(screen), width=width, height=height, align="center")

# Controls for Panel UI
step_button = pn.widgets.Button(name="Next Frame", button_type="primary")
img_pane = pn.pane.PNG(pygame_surface_to_pngbuf(screen), width=width, height=height, align="center")

def on_step(event):
    advance_simulation()
    # Redraw after simulation step to generate the new frame
    screen.fill(constants.COLOR_BACKGROUND)
    for body in current_solarsystem:
        body.draw(screen, scale, screen_offset_x, screen_offset_y)
    img_pane.object = pygame_surface_to_pngbuf(screen)

step_button.on_click(on_step)

def pygame_to_panel_image(screen_surface):
    # Convert Pygame surface to RGB array
    pygame_array = pygame.surfarray.array3d(screen_surface)  # shape: (w, h, 3)
    pygame_array = np.transpose(pygame_array, (1, 0, 2))     # shape: (h, w, 3)
    img = Image.fromarray(pygame_array)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def render_test_screen():
    screen.fill(constants.COLOR_BACKGROUND)  # Dark gray background
    return pn.pane.PNG(pygame_to_panel_image(screen), width=width, height=height)



# Layout for Panel
app = pn.Column(
    img_pane,
    step_button,
    sizing_mode="stretch_width"
)

# Placeholder for the simulation screen
panel_layout = pn.Column(
    # render_test_screen,
    app,
    sizing_mode="stretch_both"
)

# Use HSpacer to center the content
centered_layout = pn.Row(pn.layout.HSpacer(), panel_layout, pn.layout.HSpacer())

template = pn.template.VanillaTemplate(
    title="Solar System Simulation Web",
    sidebar_width=0,
)
template.main.append(centered_layout)


if __name__ == "__main__":
    # Make the template servable and launch it in a browser
    template.servable()
    pn.serve(template, port=5000, show=True)