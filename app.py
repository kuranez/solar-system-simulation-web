"""Solar System Simulation Web - Panel UI with Pygame Rendering

# This is a Panel-based web application that simulates the solar system.
# It uses Pygame for off-screen rendering and Panel for the web interface. The simulation includes
# the Sun, planets, and an asteroid belt. Users can play the simulation live or advance it frame by frame.

# version: 2.3 - Live Simulation with Play/Pause and Zoom, Multiple Views (Sun & Earth, Full Solar System)
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
from simulation.scene import build_simulation_views

# Importing UI handlers and CSS
from ui.css import GLOBAL_THEME_CSS, CUSTOM_SELECT_CSS, CUSTOM_SLIDER_CSS, APP_LAYOUT_CSS, BUTTON_CSS
from ui.canvas import SimulationCanvas, sync_canvas_frame
from ui.ui_handlers import apply_zoom_for_view, decrease_simulation_speed, increase_simulation_speed, play_pause, stop_and_reset, refresh_speed_display

# Importing the EphemerisManager to load Skyfield ephemeris data
from simulation.ephemeris import EphemerisManager

# Load the ephemeris data at startup to avoid delays during simulation
EphemerisManager.load()
EphemerisManager.get()  # Ensure the ephemeris is loaded and ready for use

# Initialize Panel extension
pn.extension(raw_css=[GLOBAL_THEME_CSS, APP_LAYOUT_CSS])

# Canvas dimensions are still driven by the simulation constants.
width, height = constants.WIDTH, constants.HEIGHT

SIMULATION_VIEWS = build_simulation_views()
initial_view_name = "[JPL] Solar System"

def choose_serve_port(preferred_port=5000):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", preferred_port))
            return preferred_port
    except OSError:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

# State variables for app
# ---------------------------------------------
state = {
    'is_playing': False,
    'callback': None,
    'base_distance_scale': SIMULATION_VIEWS[initial_view_name]['base_scale'],
    'distance_scale': SIMULATION_VIEWS[initial_view_name]['base_scale'],
    'simulation_timestep': SIMULATION_VIEWS[initial_view_name].get('scene', {}).get('simulation_timestep', constants.TIMESTEP),
    'planet_scale': 1.0,
    'offset_x': width // 2,
    'offset_y': height // 2,
    'total_elapsed_time': 0.0,
    'frame_period': 33,
    'scene_token': 1,
    'render_stride': 1.0,
    'render_skip_counter': 0.0,
    'max_completed_orbit_trails': SIMULATION_VIEWS[initial_view_name].get('max_completed_orbit_trails', 5),
    'min_orbits_before_prune': SIMULATION_VIEWS[initial_view_name].get('min_orbits_before_prune', 1),
}

current_solarsystem = SIMULATION_VIEWS[initial_view_name]["generator"]()

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
play_button = pn.widgets.Button(name="Play", icon="player-play", button_type="success", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)
reset_button = pn.widgets.Button(name="Reset", icon="player-stop", button_type="warning", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)
slower_button = pn.widgets.Button(name="Slower", icon="minus", button_type="default", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)
faster_button = pn.widgets.Button(name="Faster", icon="plus", button_type="default", width=84, height=42, margin=0, css_classes=["big-button"], stylesheets=button_stylesheets)

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
    state['render_skip_counter'] = 0.0

    # Load the new set of celestial bodies
    current_solarsystem = SIMULATION_VIEWS[view_name]["generator"]()

    # Apply per-view base scale so each simulation can define its own distance mapping.
    state['base_distance_scale'] = SIMULATION_VIEWS[view_name]['base_scale']
    state['simulation_timestep'] = SIMULATION_VIEWS[view_name].get('scene', {}).get('simulation_timestep', constants.TIMESTEP)
    state['render_stride'] = 1.0
    state['max_completed_orbit_trails'] = SIMULATION_VIEWS[view_name]['max_completed_orbit_trails']
    state['min_orbits_before_prune'] = SIMULATION_VIEWS[view_name]['min_orbits_before_prune']
    apply_zoom_for_view(current_solarsystem, state, 1.0, SIMULATION_VIEWS[view_name])
    refresh_speed_display(canvas_view, state)
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
play_button.on_click(lambda event: play_pause(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view, play_button))
reset_button.on_click(lambda event: stop_and_reset(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view, play_button))
slower_button.on_click(lambda event: decrease_simulation_speed(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view, play_button))
faster_button.on_click(lambda event: increase_simulation_speed(event, state, current_solarsystem, constants.COLOR_BACKGROUND, canvas_view, play_button))

# Layout for Panel UI
# ---------------------------------------------
controls = pn.Row(play_button, reset_button, slower_button, faster_button, pn.layout.HSpacer(), view_select, align="center", sizing_mode="fixed", width=1120, height=60, margin=0, css_classes=["app-controls"])
app = pn.Column(controls, canvas_view, sizing_mode="stretch_both", margin=0, css_classes=["app-shell"])


if __name__ == "__main__":
    serve_port = choose_serve_port(int(os.environ.get("PORT", "5000")))
    if serve_port != int(os.environ.get("PORT", "5000")):
        print(f"Port {os.environ.get('PORT', '5000')} is busy; starting Panel on port {serve_port} instead.")

    pn.serve(
        app,
        port=serve_port,
        show=True,
        allow_websocket_origin=[f"localhost:{serve_port}", f"127.0.0.1:{serve_port}"],
    )