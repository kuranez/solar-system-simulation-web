# Solar System Simulation Web - Panel UI with Pygame Rendering

# This is a Panel-based web application that simulates the solar system.
# It uses Pygame for off-screen rendering and Panel for the web interface. The simulation includes
# the Sun, planets, and an asteroid belt. Users can play the simulation live or advance it frame by frame.

# version: 1.7 - Live Simulation with Play/Pause and Zoom
# author: kuranez

# Importing system libraries
import io # For in-memory byte streams
import sys # For modifying the Python path to include the simulation package
import os # For handling file paths and directories

# Add directories to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'simulation')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

# Importing necessary libraries
import numpy as np # For numerical operations and array handling
from PIL import Image # For image processing and conversion between Pygame surfaces and PNG format
import pygame # For off-screen rendering of the solar system simulation

import panel as pn # For building the web interface
from panel.template import MaterialTemplate
from panel.theme import DarkTheme

# Importing from the simulation package
import constants # For simulation constants like scale and colors
from simulation.solarsystem_sim import Planet, Sun
from modules.solar_system import create_solar_system
from modules.sun_and_earth import create_sun_and_earth
from modules.ui.screen import pygame_surface_to_PNGbuf, draw_frame 
from modules.ui.ui_handlers import advance_simulation, on_step, periodic_update, play_pause, zoom_in, zoom_out


# Initialize Panel extension
pn.extension()

# Pygame initialization (off-screen)
pygame.display.init()
width, height = 1600, 740  # Default dimensions, can be adjusted as needed
screen = pygame.Surface((width, height))
screen.fill(constants.COLOR_BACKGROUND)  # Fill with background color

# Solar system initialization
solarsystem = create_solar_system()
# major_asteroids = create_major_asteroids()
# asteroids = create_asteroid_belt(num_asteroids=200)
# current_solarsystem = solarsystem + major_asteroids + asteroids

# Assign individual planet variables
sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune = solarsystem

current_solarsystem = solarsystem

# current_solarsystem = create_sun_and_earth()

# State variables for app
# ---------------------------------------------
# Screen variables for centering and scaling
state = {
    'is_playing': False,
    'callback': None,
    # 'scale': constants.DEFAULT_SCALE,
    
    # orbital zoom
    'distance_scale': constants.DEFAULT_SCALE,

    # visual planet scaling
    'planet_scale': 1.0,

    'offset_x': width // 2,
    'offset_y': height // 2,
}

# Controls for Panel UI
# ---------------------------------------------
# Buttons for controling the simulation
step_button = pn.widgets.Button(name="Next Frame", button_type="primary")
play_button = pn.widgets.Button(name="Play", button_type="success")
zoom_in_button = pn.widgets.Button(name="Zoom In", button_type="primary")
zoom_out_button = pn.widgets.Button(name="Zoom Out", button_type="primary")

# Initial render of the simulation frame
img_pane = pn.pane.PNG(pygame_surface_to_PNGbuf(screen), width=width, height=height, align="center")

# Attach event handlers to buttons
step_button.on_click(lambda event: on_step(event, screen, current_solarsystem, state, constants.COLOR_BACKGROUND, img_pane))
play_button.on_click(lambda event: play_pause(event, state, screen, current_solarsystem, constants.COLOR_BACKGROUND, img_pane, play_button))
zoom_in_button.on_click(lambda event: zoom_in(event, state, current_solarsystem, screen, constants.COLOR_BACKGROUND, img_pane))
zoom_out_button.on_click(lambda event: zoom_out(event, state, current_solarsystem, screen, constants.COLOR_BACKGROUND, img_pane))

# Layout for Panel UI
# ---------------------------------------------
controls = pn.Row (play_button, step_button, zoom_in_button, zoom_out_button, align="center")
app = pn.Column(controls, img_pane, align="center")

# Use HSpacer to center the content
centered_layout = pn.Row(pn.layout.HSpacer(), app, pn.layout.HSpacer())

template = MaterialTemplate(
    site="Earth and Sun",
    title="Solar System Simulation",
    theme=DarkTheme,
    header_background="#422C71",
    sidebar_width=0,
    # favicon="path/to/your/icon.png"  # Replace with the actual path to your icon
)
template.main.append(centered_layout)


if __name__ == "__main__":
    # Make the template servable and launch it in a browser
    template.servable()
    pn.serve(template, port=5000, show=True)