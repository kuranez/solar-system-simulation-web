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
        "position": 0.387098, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 46001200000,  # 46,001,200 km
        "aphelion": 69816900000,    # 69,816,900 km
        "radius": 2439.7e3,
        "mass": 0.33011e24,
        "orbital_velocity": 47.36e3,
        "is_inner": True,
        "color": COLOR_MERCURY,
    },
    "Venus": {
        "name": "Venus",
        "type": "planet",
        "position": 0.723332, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 107477000000, # 107,477,000 km
        "aphelion": 108939000000,   # 108,939,000 km
        "radius": 6051.8e3,
        "mass": 4.8675e24,
        "orbital_velocity": 35.02e3,
        "is_inner": True,
        "color": COLOR_VENUS,
    },
    "Earth": {
        "name": "Earth",
        "type": "planet",
        "position": 1.000000, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 147095000000, # 147,095,000 km
        "aphelion": 152100000000,   # 152,100,000 km
        "radius": 6378.1e3,
        "mass": 5.97237e24,
        "orbital_velocity": 29.78e3,
        "is_inner": True,
        "color": COLOR_EARTH,
    },
    "Mars": {
        "name": "Mars",
        "type": "planet",
        "position": 1.52368, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 206669000000, # 206,669,000 km
        "aphelion": 249209000000,   # 249,209,000 km
        "radius": 3396.2e3,
        "mass": 0.64171e24,
        "orbital_velocity": 24.07e3,
        "is_inner": True,
        "color": COLOR_MARS,
    },
    "Jupiter": {
        "name": "Jupiter",
        "type": "planet",
        "position": 5.2038, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 740520000000, # 740,520,000 km
        "aphelion": 816620000000,   # 816,620,000 km
        "radius": 71492e3,
        "mass": 1898.19e24,
        "orbital_velocity": 13.07e3,
        "is_inner": False,
        "color": COLOR_JUPITER,
    },
    "Saturn": {
        "name": "Saturn",
        "type": "planet",
        "position": 9.5826, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 1352550000000, # 1,352,550,000 km
        "aphelion": 1514500000000,   # 1,514,500,000 km
        "radius": 60268e3,
        "mass": 568.34e24,
        "orbital_velocity": 9.69e3,
        "is_inner": False,
        "color": COLOR_SATURN,
    },
    "Uranus": {
        "name": "Uranus",
        "type": "planet",
        "position": 19.2184, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 2741300000000, # 2,741,300,000 km
        "aphelion": 3003620000000,   # 3,003,620,000 km
        "radius": 25559e3,
        "mass": 86.813e24,
        "orbital_velocity": 6.81e3,
        "is_inner": False,
        "color": COLOR_URANUS,
    },
    "Neptune": {
        "name": "Neptune",
        "type": "planet",
        "position": 30.110, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 4444450000000, # 4,444,450,000 km
        "aphelion": 4545670000000,   # 4,545,670,000 km
        "radius": 24764e3,
        "mass": 102.413e24,
        "orbital_velocity": 5.43e3,
        "is_inner": False,
        "color": COLOR_NEPTUNE,
    },
    # Asteroids
    "Ceres": {
        "name": "Ceres",
        "type": "asteroid",
        "position": 2.767, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 380900000000, # 380,900,000 km
        "aphelion": 446400000000,   # 446,400,000 km
        "radius": 469.7e3,
        "mass": 9.393e20,
        "semi_major_axis": 2.77 * AU,
        "orbital_velocity": 17.9e3,
        "color": (180, 180, 180),
    },
    "Vesta": {
        "name": "Vesta",
        "type": "asteroid",
        "position": 2.361, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 315100000000, # 315,100,000 km
        "aphelion": 395400000000,   # 395,400,000 km (value seems correct)
        "radius": 262.7e3,
        "mass": 2.59e20,
        "semi_major_axis": 2.36 * AU,
        "orbital_velocity": 19.3e3,
        "color": (190, 185, 180),
    },
    "Pallas": {
        "name": "Pallas",
        "type": "asteroid",
        "position": 2.773, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 319900000000, # 319,900,000 km
        "aphelion": 510800000000,   # 510,800,000 km (value seems correct)
        "radius": 272e3,
        "mass": 2.11e20,
        "semi_major_axis": 2.77 * AU,
        "orbital_velocity": 17.6e3,
        "color": (185, 180, 175),
    },
    "Hygiea": {
        "name": "Hygiea",
        "type": "asteroid",
        "position": 3.141, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 420700000000, # 420,700,000 km
        "aphelion": 529300000000,   # 529,300,000 km (value seems correct)
        "radius": 215.5e3,
        "mass": 8.32e19,
        "semi_major_axis": 3.14 * AU,
        "orbital_velocity": 16.7e3,
        "color": (170, 165, 160),
    },
    "Eros": {
        "name": "Eros",
        "type": "asteroid",
        "position": 1.458, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 169200000000, # 169,200,000 km
        "aphelion": 266100000000,   # 266,100,000 km (value seems correct)
        "radius": 16.8e3, # Mean radius is 16.8km, not 8.4km
        "mass": 6.69e15,
        "semi_major_axis": 1.46 * AU,
        "orbital_velocity": 24.36e3,
        "color": (200, 190, 185),
    },
    # Moon (kept as a full spec/template)
    "Moon": {
        "name": "Moon",
        "type": "moon",
        "position": 0.00257, # Average distance from the Earth in AU (semi-major axis)
        "parent_body": "Earth",
        "perigee": 362600000,  # 362,600 km
        "apogee": 405400000,   # 405,400 km
        "perihelion": None,
        "apihelion": None,
        "radius": 1737.1e3,
        "mass": 7.342e22,
        "semi_major_axis": 384400e3,
        "average_distance": 384400e3,
        "orbital_velocity": 1.022e3,
        "color": (200, 200, 200),
    },
    # Saturn's Moons (example with Titan)
    "Titan": {
        "name": "Titan",
        "type": "moon",
        "position": 0.008168, # Average distance from Saturn in AU (semi-major axis)
        "parent_body": "Saturn",
        "perigee": 1221000000, # 1,221,000 km
        "apogee": 1222000000,  # 1,222,000 km
        "perihelion": None,
        "apihelion": None,
        "radius": 2575e3,
        "mass": 1.3452e23,
        "semi_major_axis": 1.22e9,
        "average_distance": 1.22e9,
        "orbital_velocity": 5.57e3,
        "color": (210, 180, 140),
    },
    # Jupiter's Moons (example with Europa)
    "Europa": {
        "name": "Europa",
        "type": "moon",
        "position": 0.00448, # Average distance from Jupiter in AU (semi-major axis)
        "parent_body": "Jupiter",
        "perigee": 670900000,  # 670,900 km
        "apogee": 671100000,   # 671,100 km
        "perihelion": None,
        "apihelion": None,
        "radius": 1560.8e3,
        "mass": 4.7998e22,
        "semi_major_axis": 670900e3,
        "average_distance": 670900e3,
        "orbital_velocity": 13.74e3,
        "color": (220, 220, 220),
    },
    "Io": {
        "name": "Io",
        "type": "moon",
        "position": 0.00282, # Average distance from Jupiter in AU (semi-major axis)
        "parent_body": "Jupiter",
        "perigee": 420000000,  # 420,000 km
        "apogee": 423400000,   # 423,400 km
        "perihelion": None,
        "apihelion": None,
        "radius": 1821.6e3,
        "mass": 8.9319e22,
        "semi_major_axis": 421700e3,
        "average_distance": 421700e3,
        "orbital_velocity": 17.33e3,
        "color": (255, 200, 150),
    },
    "Ganymede": {
        "name": "Ganymede",
        "type": "moon",
        "position": 0.007155, # Average distance from Jupiter in AU (semi-major axis)
        "parent_body": "Jupiter",
        "perigee": 1069000000, # 1,069,000 km
        "apogee": 1072000000,  # 1,072,000 km
        "perihelion": None,
        "apihelion": None,
        "radius": 2634.1e3,
        "mass": 1.4819e23,
        "semi_major_axis": 1070400e3,
        "average_distance": 1070400e3,
        "orbital_velocity": 10.88e3,
        "color": (200, 220, 255),
    },
    "Callisto": {
        "name": "Callisto",
        "type": "moon",
        "position": 0.012585, # Average distance from Jupiter in AU (semi-major axis)
        "parent_body": "Jupiter",
        "perigee": 1869000000, # 1,869,000 km
        "apogee": 1897000000,  # 1,897,000 km
        "perihelion": None,
        "apihelion": None,
        "radius": 2410.3e3,
        "mass": 1.0759e23,
        "semi_major_axis": 1882700e3,
        "average_distance": 1882700e3,
        "orbital_velocity": 8.204e3,
        "color": (180, 200, 255),
    },
    # Trans-Neptunian Objects (example with Pluto)
    "Pluto": {
        "name": "Pluto",
        "type": "tno",
        "position": 39.482, # Average distance from the Sun in AU (semi-major axis)
        "perihelion": 4436820000000, # 4,436,820,000 km
        "aphelion": 7375930000000,   # 7,375,930,000 km
        "radius": 1188.3e3,
        "mass": 1.303e22,
        "orbital_velocity": 4.74e3,
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