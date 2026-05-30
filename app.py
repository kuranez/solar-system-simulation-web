"""Solar System Simulation Web - Panel UI with Pygame Rendering

# This is a Panel-based web application that simulates the solar system.
# It uses Pygame for off-screen rendering and Panel for the web interface. The simulation includes
# the Sun, planets, and an asteroid belt. Users can play the simulation live or advance it frame by frame.

# version: 2.2 - Live Simulation with Play/Pause and Zoom, Multiple Views (Sun & Earth, Full Solar System)
# Update Log: Tweaked architecture for better modularity

"""

import sys # For modifying the Python path to include the simulation package
import os
import socket

# Add directories to the Python path
repo_root = os.path.abspath(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import panel as pn # For building the web interface

# Importing from the simulation package
import constants # For simulation constants like scale and colors
from modules.simple_solar_system import create_solar_system
from modules.simple_sun_earth import create_sun_earth_system
from modules.simple_earth_moon import create_earth_moon_system
from modules.simple_sun_earth_moon import create_sun_earth_moon_system

# Importing UI handlers and CSS
from ui.css import GLOBAL_THEME_CSS, CUSTOM_SELECT_CSS, CUSTOM_SLIDER_CSS, APP_LAYOUT_CSS, BUTTON_CSS
from ui.canvas import SimulationCanvas, sync_canvas_frame
from ui.ui_handlers import apply_zoom_for_view, decrease_simulation_speed, increase_simulation_speed, periodic_update, play_pause, stop_and_reset, update_proportional_sun_earth_moon, update_simple_earth_moon, update_body_radii


# Initialize Panel extension
pn.extension(raw_css=[GLOBAL_THEME_CSS, APP_LAYOUT_CSS])
# pn.extension() 

# Canvas dimensions are still driven by the simulation constants.
width, height = constants.WIDTH, constants.HEIGHT

# Simulation setup
SIMULATION_VIEWS = {
        "[Simple] Sun and Earth": {
        "title": "Simple Sun and Earth System",
        "description": "A simulation of the Sun and Earth system.",
        "generator": create_sun_earth_system,
        "base_scale": constants.DEFAULT_SCALE,
        "zoom_updater": None,
        "scale_mode": "distance",
    },
    "[Simple] Earth and Moon": {
        "title": "Simple Earth and Moon System",
        "description": "A simulation of the Earth and Moon system.",
        "generator": create_earth_moon_system,
        "base_scale": 350 / constants.MOON_DATA["average_distance"],
        "scale_mode": "distance",
        "zoom_updater": update_simple_earth_moon,
    },
    "[Simple] Sun, Earth, and Moon System": {
        "title": "Sun, Earth, and Moon System",
        "description": "A simulation of the Sun, Earth, and Moon system.",
        "generator": create_sun_earth_moon_system,
        "base_scale": 1.0,
        "zoom_updater": update_proportional_sun_earth_moon, # Custom updater for proportional scaling of the Sun-Earth-Moon system
        "scale_mode": "proportional", # This view will use proportional scaling for both distance and size based on the slider
        "sun_earth_base_px": 420, # Base pixel distance for Sun-Earth at default scale
        "earth_moon_ratio": 0.257, # Ratio of Earth-Moon
    },
    "[Simple] Solar System": {
        "title": "Simple Solar System (Planets only, no asteroids)",
        "description": "A simulation of the simple solar system with planets only.",
        "generator": create_solar_system,
        "base_scale": constants.DEFAULT_SCALE, 
        "scale_mode": "distance", # This view will use distance scaling for the zoom slider 
        "zoom_updater": None, # No custom updater, will use the default distance scaling logic in on_zoom_change
    },
}

initial_view_name = "[Simple] Solar System"
current_solarsystem = SIMULATION_VIEWS[initial_view_name]["generator"]()


def choose_serve_port(preferred_port=5000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", preferred_port))
    except OSError:
        return 0

    return preferred_port


# State variables for app
# ---------------------------------------------
# Screen variables for centering and scaling
state = {
    'is_playing': False,
    'callback': None,
    'base_distance_scale': SIMULATION_VIEWS[initial_view_name]['base_scale'],
    'distance_scale': SIMULATION_VIEWS[initial_view_name]['base_scale'], # orbital distance scaling
    'planet_scale': 1.0, # planet size scaling (can be adjusted separately if needed)
    'offset_x': width // 2,
    'offset_y': height // 2,
    'total_elapsed_time': 0.0, # Total elapsed simulation time in seconds
    'frame_period': 50,
    'scene_token': 1,
}

# Controls for Panel UI
# ---------------------------------------------

# Selection of predefined views (e.g., Sun & Earth, Full Solar System)
view_select = pn.widgets.Select(
    label="Select Simulation", 
    options=list(SIMULATION_VIEWS.keys()),
    value=initial_view_name, # Set the default value
    width=270,
    margin=0,
    stylesheets=[CUSTOM_SELECT_CSS]
)

# Buttons for controling the simulation
button_stylesheets = [BUTTON_CSS]
# step_button = pn.widgets.Button(name="Next Frame", icon="player-step-forward", button_type="primary", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)
play_button = pn.widgets.Button(name="Play", icon="player-play", button_type="success", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)
reset_button = pn.widgets.Button(name="Reset", icon="player-stop", button_type="warning", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)
slower_button = pn.widgets.Button(name="Slower", icon="minus", button_type="default", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)
faster_button = pn.widgets.Button(name="Faster", icon="plus", button_type="default", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)
# zoom_in_button = pn.widgets.Button(name="Zoom In", button_type="primary")
# zoom_out_button = pn.widgets.Button(name="Zoom Out", button_type="primary")

# Browser-side canvas view.
canvas_view = SimulationCanvas(sizing_mode="stretch_both", margin=0, align="center", css_classes=["app-viewer"])
sync_canvas_frame(
    canvas_view,
    current_solarsystem,
    state,
    constants.COLOR_BACKGROUND,
    scene_token=state['scene_token'],
    reset=True,
)

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
        play_pause(None, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view, play_button)

    # Reset elapsed simulation time whenever the user changes views
    state['total_elapsed_time'] = 0.0

    # Load the new set of celestial bodies
    current_solarsystem = SIMULATION_VIEWS[view_name]["generator"]()

    # Apply per-view base scale so each simulation can define its own distance mapping.
    state['base_distance_scale'] = SIMULATION_VIEWS[view_name]['base_scale']
    apply_zoom_for_view(current_solarsystem, state, 1.0, SIMULATION_VIEWS[view_name])
    state['scene_token'] += 1
    
    # Push a reset frame to clear the browser-side trail state.
    sync_canvas_frame(
        canvas_view,
        current_solarsystem,
        state,
        constants.COLOR_BACKGROUND,
        scene_token=state['scene_token'],
        reset=True,
    )

# Attach the callback to the view selector
view_select.param.watch(update_view, 'value')

# Attach event handlers to buttons
# step_button.on_click(lambda event: on_step(event, current_solarsystem, state, constants.COLOR_BACKGROUND, canvas_view))
play_button.on_click(lambda event: play_pause(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view, play_button))
slower_button.on_click(lambda event: decrease_simulation_speed(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view, play_button))
faster_button.on_click(lambda event: increase_simulation_speed(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view, play_button))
# reset_button.on_click(lambda event: stop_and_reset(event, state, screen, current_solarsystem, constants.COLOR_BACKGROUND, img_pane, play_button))
# zoom_in_button.on_click(lambda event: zoom_in(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view))
# zoom_out_button.on_click(lambda event: zoom_out(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view))

# Layout for Panel UI
# ---------------------------------------------
controls = pn.Row(play_button, slower_button, faster_button, pn.layout.HSpacer(), view_select, align="center", sizing_mode="fixed", width=1120, height=60, margin=0, css_classes=["app-controls"])
app = pn.Column(controls, canvas_view, sizing_mode="stretch_both", margin=0, css_classes=["app-shell"])


if __name__ == "__main__":
    serve_port = choose_serve_port(int(os.environ.get("PORT", "5000")))
    if serve_port == 0:
        print("Port 5000 is busy; starting Panel on a free port instead.")

    pn.serve(app, port=serve_port, show=True)