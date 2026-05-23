# Solar System Simulation Web - Panel UI with Pygame Rendering

# This is a Panel-based web application that simulates the solar system.
# It uses Pygame for off-screen rendering and Panel for the web interface. The simulation includes
# the Sun, planets, and an asteroid belt. Users can play the simulation live or advance it frame by frame.

# version: 2.0 - Live Simulation with Play/Pause and Zoom, Multiple Views (Sun & Earth, Full Solar System)
# Update Log: Tweaked architecture for better modularity

# Importing system libraries
import io # For in-memory byte streams
import sys # For modifying the Python path to include the simulation package
import os # For handling file paths and directories

# Add directories to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'simulation')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui')))

# Importing necessary libraries
import numpy as np # For numerical operations and array handling
from PIL import Image # For image processing and conversion between Pygame surfaces and PNG format
import pygame # For off-screen rendering of the solar system simulation

import panel as pn # For building the web interface
from panel.template import FastListTemplate
from panel.theme import DarkTheme

# Importing from the simulation package
import constants # For simulation constants like scale and colors
from simulation.solarsystem_sim import Planet, Sun
from modules.simple_solar_system import create_solar_system
from modules.simple_sun_and_earth import create_sun_and_earth

# Importing UI handlers and CSS
from ui.css import GLOBAL_THEME_CSS, CUSTOM_SELECT_CSS, CUSTOM_SLIDER_CSS
from ui.screen import pygame_surface_to_PNGbuf, draw_frame 
from ui.ui_handlers import advance_simulation, on_step, periodic_update, play_pause, update_body_radii, zoom_in, zoom_out


# Initialize Panel extension
pn.extension(raw_css=[GLOBAL_THEME_CSS])
# pn.extension() 

# Pygame initialization (off-screen)
pygame.display.init()
width, height = 1600, 740  # Default dimensions, can be adjusted as needed
screen = pygame.Surface((width, height))
screen.fill(constants.COLOR_BACKGROUND)  # Fill with background color

# Simulation setup
SIMULATION_VIEWS = {
    "Simple Sun and Earth System": {
        "title": "Simple Sun and Earth System (No moon)",
        "generator": create_sun_and_earth
    },
    "Simple Solar System": {
        "title": "Simple Solar System (Planets only, no asteroids)",
        "generator": create_solar_system
    }
}

initial_view_name = "Simple Solar System"
current_solarsystem = SIMULATION_VIEWS[initial_view_name]["generator"]()


# State variables for app
# ---------------------------------------------
# Screen variables for centering and scaling
state = {
    'is_playing': False,
    'callback': None,
    'distance_scale': constants.DEFAULT_SCALE, # orbital distance scaling
    'planet_scale': 1.0, # planet size scaling (can be adjusted separately if needed)
    'offset_x': width // 2,
    'offset_y': height // 2,
    'total_elapsed_time': 0.0, # Total elapsed simulation time in seconds
}

# Controls for Panel UI
# ---------------------------------------------

# Selection of predefined views (e.g., Sun & Earth, Full Solar System)
view_select = pn.widgets.Select(
    label="Select Simulation", 
    options=list(SIMULATION_VIEWS.keys()),
    value=initial_view_name, # Set the default value
    width=450,
    stylesheets=[CUSTOM_SELECT_CSS]
)

# Buttons for controling the simulation
step_button = pn.widgets.Button(name="Next Frame", button_type="primary", width=150, css_classes=["big-button"])
play_button = pn.widgets.Button(name="Play", button_type="success", width=150, css_classes=["big-button"])
# zoom_in_button = pn.widgets.Button(name="Zoom In", button_type="primary")
# zoom_out_button = pn.widgets.Button(name="Zoom Out", button_type="primary")

# New slider for zoom control
zoom_slider = pn.widgets.FloatSlider(
    label='Zoom', 
    start=0.05,  # Minimum zoom factor
    end=2.5,    # Maximum zoom factor
    step=0.05, 
    value=0.5,   # Start at 50% zoom
    format="0.0%",  # Display as percentage
    stylesheets=[CUSTOM_SLIDER_CSS],
)

# Initial render of the simulation frame
img_pane = pn.pane.PNG(pygame_surface_to_PNGbuf(screen), width=width, height=height, align="center")

# Callback functions
def update_view(event):
    """
    Handles changes in the view_select dropdown.
    Switches the simulation, updates the title, and redraws.
    """
    global current_solarsystem
    view_name = event.new  # The new value from the dropdown
    
    # Stop the current simulation if it's playing
    if state['is_playing']:
        play_pause(None, state, screen, current_solarsystem, constants.COLOR_BACKGROUND, img_pane, play_button)

    # Load the new set of celestial bodies
    current_solarsystem = SIMULATION_VIEWS[view_name]["generator"]()
    
    # Redraw the scene with the new system
    draw_frame(screen, current_solarsystem, state, constants.COLOR_BACKGROUND)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

# Attach the callback to the view selector
view_select.param.watch(update_view, 'value')

def on_zoom_change(event):
    """Handles changes in the zoom slider."""
    # The slider's value is a multiplier for the default scale
    state['distance_scale'] = constants.DEFAULT_SCALE * event.new
    
    # Recalculate planet sizes and redraw the frame
    update_body_radii(current_solarsystem, state['distance_scale'])
    
    # Redraw the scene with the new scale
    draw_frame(screen, current_solarsystem, state, constants.COLOR_BACKGROUND)
    img_pane.object = pygame_surface_to_PNGbuf(screen)

# Attach the callback to the slider
zoom_slider.param.watch(on_zoom_change, 'value')

# Attach event handlers to buttons
step_button.on_click(lambda event: on_step(event, screen, current_solarsystem, state, constants.COLOR_BACKGROUND, img_pane))
play_button.on_click(lambda event: play_pause(event, state, screen, current_solarsystem, constants.COLOR_BACKGROUND, img_pane, play_button))
# zoom_in_button.on_click(lambda event: zoom_in(event, state, current_solarsystem, screen, constants.COLOR_BACKGROUND, img_pane))
# zoom_out_button.on_click(lambda event: zoom_out(event, state, current_solarsystem, screen, constants.COLOR_BACKGROUND, img_pane))

# Layout for Panel UI
# ---------------------------------------------
controls = pn.Row (play_button, step_button, zoom_slider, view_select, align="center")
app = pn.Column(controls, img_pane, align="center")

# Use HSpacer to center the content
centered_layout = pn.Row(pn.layout.HSpacer(), app, pn.layout.HSpacer())

template = FastListTemplate(
    title= "Solar System Simulation",
    theme=DarkTheme,
    header_background="#422C71",
    sidebar_width=0,
    theme_toggle=False,
    # favicon="path/to/your/icon.png"  # Replace with the actual path to your icon
)
template.main.append(centered_layout)


if __name__ == "__main__":
    # Make the template servable and launch it in a browser
    template.servable()
    pn.serve(template, port=5000, show=True)