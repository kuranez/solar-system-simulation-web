""" constants.py 

# Contains all constants used across the solar system simulation app, 
# including display settings, physical constants, and planetary data.

"""

# Importing necessary libraries and modules
import pygame # For rendering the simulation
import math # For mathematical calculations

# Initialize Pygame and Font
pygame.init()
pygame.font.init()

# Display Variables
WIDTH, HEIGHT = 1920, 1080
COLOR_TEXT = (255, 255, 255) # Pure white for text
COLOR_HUD_TEXT = (200, 200, 200)  # Slightly dimmer text for HUD
COLOR_BACKGROUND = (15, 22, 36) # Match the app's CSS background tone
FONT_1 = pygame.font.SysFont("monospace", 16)

# General
AU = 149.6e9  # Astronomical Unit in meters
G = 6.67428e-11  # Gravitational constant

# Scale Factors
DEFAULT_SCALE = 350 / AU  # 1 AU = 350 px
OUTER_PLANET_SCALE_FACTOR = 0.6  # Outer Planets are 40% smaller
BASE_SIZE = 50  # Base size for planets in px
earth_diameter = 12742e3  # Earth's diameter in meters
PLANET_ZOOM_EXPONENT = 0.5  # Exponent for zoom scaling (0.5 means square root scaling)

# Simulation Speed
# Reduce the global timestep to 12 hours to improve stability and make bodies
# move less per rendered frame (prevents fast detachment of moons).
TIMESTEP = 3600.0*24  # Seconds in 24 hours - Adjusted for better stability

# Solar System Colors
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (173, 168, 165)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (216, 202, 157)
COLOR_SATURN = (191, 189, 175)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)

# Sun Data
# Compact bodies data structure
BODIES_DATA = {
    "Sun": {
        "name": "Sun",
        "type": "star",
        "position": 0.0, # Sun is at the center
        "radius": 1392700e3 / 2,
        "mass": 1.98892e30,
        "color": COLOR_SUN,
    },
    "Mercury": {
        "name": "Mercury",
        "type": "planet",
        "position": 0.387, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 46.0e9,
        "aphelion": 69.8e9,
        "radius": 4879e3 / 2,
        "mass": 0.33e24,
        "orbital_velocity": 47.40e3,
        "is_inner": True,
        "color": COLOR_MERCURY,
    },
    "Venus": {
        "name": "Venus",
        "type": "planet",
        "position": 0.723, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 107.5e9,
        "aphelion": 108.9e9,
        "radius": 12104e3 / 2,
        "mass": 4.87e24,
        "orbital_velocity": 35.02e3,
        "is_inner": True,
        "color": COLOR_VENUS,
    },
    "Earth": {
        "name": "Earth",
        "type": "planet",
        "position": 1.0, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 147.1e9,
        "aphelion": 152.1e9,
        "radius": 12756e3 / 2,
        "mass": 5.97e24,
        "orbital_velocity": 29.78e3,
        "is_inner": True,
        "color": COLOR_EARTH,
    },
    "Mars": {
        "name": "Mars",
        "type": "planet",
        "position": 1.524, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 206.7e9,
        "aphelion": 249.2e9,
        "radius": 6792e3 / 2,
        "mass": 0.642e24,
        "orbital_velocity": 24.06e3,
        "is_inner": True,
        "color": COLOR_MARS,
    },
    "Jupiter": {
        "name": "Jupiter",
        "type": "planet",
        "position": 5.204, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 740.6e9,
        "aphelion": 816.6e9,
        "radius": 142984e3 / 2,
        "mass": 1898e24,
        "orbital_velocity": 13.06e3,
        "is_inner": False,
        "color": COLOR_JUPITER,
    },
    "Saturn": {
        "name": "Saturn",
        "type": "planet",
        "position": 9.573, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 1357.6e9,
        "aphelion": 1514.5e9,
        "radius": 120536e3 / 2,
        "mass": 568e24,
        "orbital_velocity": 9.68e3,
        "is_inner": False,
        "color": COLOR_SATURN,
    },
    "Uranus": {
        "name": "Uranus",
        "type": "planet",
        "position": 19.165, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 2732.7e9,
        "aphelion": 3000.0e9,
        "radius": 51118e3 / 2,
        "mass": 86.8e24,
        "orbital_velocity": 6.80e3,
        "is_inner": False,
        "color": COLOR_URANUS,
    },
    "Neptune": {
        "name": "Neptune",
        "type": "planet",
        "position": 30.178, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 4471.1e9,
        "aphelion": 4558.0e9,
        "radius": 49528e3 / 2,
        "mass": 102e24,
        "orbital_velocity": 5.43e3,
        "is_inner": False,
        "color": COLOR_NEPTUNE,
    },
    # Asteroids
    "Ceres": {
        "name": "Ceres",
        "type": "asteroid",
        "position": None, # Ceres has a more complex orbit, so we can set this to None or calculate it dynamically
        "perihelion": 413.7e9,
        "aphelion": 469.8e9,
        "radius": 473e3,
        "mass": 9.393e20,
        "semi_major_axis": 2.77 * AU,
        "orbital_velocity": 17900,
        "color": (180, 180, 180),
    },
    "Vesta": {
        "name": "Vesta",
        "type": "asteroid",
        "position": None, # Vesta has a more complex orbit, so we can set this to None or calculate it dynamically
        "perihelion": 355.0e9,
        "aphelion": 420.0e9,
        "radius": 262.7e3,
        "mass": 2.59e20,
        "semi_major_axis": 2.36 * AU,
        "orbital_velocity": 19300,
        "color": (190, 185, 180),
    },
    "Pallas": {
        "name": "Pallas",
        "type": "asteroid",
        "position": None, # Pallas has a more complex orbit, so we can set this to None or calculate it dynamically
        "perihelion": 414.0e9,
        "aphelion": 510.0e9,
        "radius": 256e3,
        "mass": 2.11e20,
        "semi_major_axis": 2.77 * AU,
        "orbital_velocity": 17000,
        "color": (185, 180, 175),
    },
    "Hygiea": {
        "name": "Hygiea",
        "type": "asteroid",
        "position": None, # Hygiea has a more complex orbit, so we can set this to None or calculate it dynamically
        "perihelion": 470.0e9,
        "aphelion": 540.0e9,
        "radius": 215e3,
        "mass": 8.32e19,
        "semi_major_axis": 3.14 * AU,
        "orbital_velocity": 15000,
        "color": (170, 165, 160),
    },
    "Eros": {
        "name": "Eros",
        "type": "asteroid",
        "position": None, # Eros has a more complex orbit, so we can set this to None or calculate it dynamically
        "perihelion": 218.0e9,
        "aphelion": 250.0e9,
        "radius": 8.4e3,
        "mass": 6.69e15,
        "semi_major_axis": 1.46 * AU,
        "orbital_velocity": 24000,
        "color": (200, 190, 185),
    },
    # Moon (kept as a full spec/template)
    "Moon": {
        "name": "Moon",
        "type": "moon",
        "position": None, # Moon's position is relative to Earth, so we can set this to None or calculate it dynamically
        "parent_body": "Earth",
        "perigee": 363300e3,
        "apogee": 405500e3,
        "perihelion": None,
        "apihelion": None,
        "radius": 1737.1e3,
        "mass": 7.342e22,
        "semi_major_axis": 384400e3,
        "average_distance": 384400e3,
        "orbital_velocity": 1022,
        "color": (200, 200, 200),
    },
    # Saturn's Moons (example with Titan)
    "Titan": {
        "name": "Titan",
        "type": "moon",
        "position": None, # Titan's position is relative to Saturn, so we can set this to None or calculate it dynamically
        "parent_body": "Saturn",
        "perigee": 1.2e9,
        "apogee": 1.5e9,
        "perihelion": None,
        "apihelion": None,
        "radius": 2575e3,
        "mass": 1.3452e23,
        "semi_major_axis": 1.22e9,
        "average_distance": 1.22e9,
        "orbital_velocity": 5500,
        "color": (210, 180, 140),
    },
    # Jupiter's Moons (example with Europa)
    "Europa": {
        "name": "Europa",
        "type": "moon",
        "position": None, # Europa's position is relative to Jupiter, so we can set this to None or calculate it dynamically
        "parent_body": "Jupiter",
        "perigee": 670900e3,
        "apogee": 671100e3,
        "perihelion": None,
        "apihelion": None,
        "radius": 1560.8e3,
        "mass": 4.7998e22,
        "semi_major_axis": 670900e3,
        "average_distance": 670900e3,
        "orbital_velocity": 13500,
        "color": (220, 220, 220),
    },
    "Io": {
        "name": "Io",
        "type": "moon",
        "position": None, # Io's position is relative to Jupiter, so we can set this to None or calculate it dynamically
        "parent_body": "Jupiter",
        "perigee": 421700e3,
        "apogee": 422000e3,
        "perihelion": None,
        "apihelion": None,
        "radius": 1821.6e3,
        "mass": 8.9319e22,
        "semi_major_axis": 421700e3,
        "average_distance": 421700e3,
        "orbital_velocity": 17300,
        "color": (255, 200, 150),
    },
    "Ganymede": {
        "name": "Ganymede",
        "type": "moon",
        "position": None, # Ganymede's position is relative to Jupiter, so we can set this to None or calculate it dynamically
        "parent_body": "Jupiter",
        "perigee": 1070400e3,
        "apogee": 1071000e3,
        "perihelion": None,
        "apihelion": None,
        "radius": 2634.1e3,
        "mass": 1.4819e23,
        "semi_major_axis": 1070400e3,
        "average_distance": 1070400e3,
        "orbital_velocity": 10800,
        "color": (200, 220, 255),
    },
    "Callisto": {
        "name": "Callisto",
        "type": "moon",
        "position": None, # Callisto's position is relative to Jupiter, so we can set this to None or calculate it dynamically
        "parent_body": "Jupiter",
        "perigee": 1882700e3,
        "apogee": 1883000e3,
        "perihelion": None,
        "apihelion": None,
        "radius": 2410.3e3,
        "mass": 1.0759e23,
        "semi_major_axis": 1882700e3,
        "average_distance": 1882700e3,
        "orbital_velocity": 8200,
        "color": (180, 200, 255),
    },
    # Trans-Neptunian Objects (example with Pluto)
    "Pluto": {
        "name": "Pluto",
        "type": "tno",
        "position": 39.48, # Average distance from the Sun in AU (negative for left side)
        "perihelion": 4436e9,
        "aphelion": 7375e9,
        "radius": 1188.3e3,
        "mass": 1.303e22,
        "orbital_velocity": 4700,
        "is_inner": False,
        "color": (200, 150, 150),
    },
}

# Convenience single-value aliases for backwards compatibility
sun_radius = BODIES_DATA["Sun"]["radius"]
sun_mass = BODIES_DATA["Sun"]["mass"]

# Rebuild PLANETS_DATA in the previous shape expected by the simulation
PLANETS_DATA = []
for _name, entry in BODIES_DATA.items():
    if entry.get("type") == "planet":
        PLANETS_DATA.append({
            "name": entry.get("name"),
            "position": entry.get("position"),
            "perihelion": entry.get("perihelion"),
            "radius": entry.get("radius"),
            "mass": entry.get("mass"),
            "velocity": entry.get("orbital_velocity"),
            "is_inner": entry.get("is_inner", False),
        })

# Asteroid compatibility variables
ASTEROID_CERES = BODIES_DATA["Ceres"]
ASTEROID_VESTA = BODIES_DATA["Vesta"]
ASTEROID_PALLAS = BODIES_DATA["Pallas"]
ASTEROID_HYGIEA = BODIES_DATA["Hygiea"]
ASTEROID_EROS = BODIES_DATA["Eros"]

# MOON_DATA kept for compatibility
MOON_DATA = BODIES_DATA["Moon"]

# Other moons
MOON_TITAN = BODIES_DATA["Titan"]
MOON_EUROPA = BODIES_DATA["Europa"]
MOON_IO = BODIES_DATA["Io"]
MOON_GANYMEDE = BODIES_DATA["Ganymede"]
MOON_CALLISTO = BODIES_DATA["Callisto"]