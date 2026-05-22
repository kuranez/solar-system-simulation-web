# constants.py 

# Display Variables
WIDTH, HEIGHT = 1920, 1080
COLOR_TEXT = (255, 255, 255)
COLOR_BACKGROUND = (36, 36, 36)

# General
AU = 149.6e9  # Astronomical Unit in meters
G = 6.67428e-11  # Gravitational constant

# Scale Factors
DEFAULT_SCALE = 350 / AU  # 1 AU = 350 px
OUTER_PLANET_SCALE_FACTOR = 0.6  # Outer Planets are 40% smaller
BASE_SIZE = 50  # Base size for planets in px
earth_diameter = 12742e3  # Earth's diameter in meters

# Simulation Speed
TIMESTEP = 3600 * 24.0 # Seconds in 1 day 

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
sun_radius = 1392700e3 / 2
sun_mass = 1.98892e30

# Planetary Data
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/

# Perihelion in meters
mercury_perihelion = 46.0e9
venus_perihelion = 107.5e9
earth_perihelion = 147.1e9
mars_perihelion = 206.7e9
jupiter_perihelion = 740.6e9
saturn_perihelion = 1357.6e9
uranus_perihelion = 2732.7e9
neptune_perihelion = 4471.1e9


# Radius in meters
mercury_radius = 4879e3 / 2
venus_radius = 12104e3 / 2
earth_radius = 12756e3 / 2
mars_radius = 6792e3 / 2
jupiter_radius = 142984e3 / 2
saturn_radius = 120536e3 / 2
uranus_radius = 51118e3 / 2
neptune_radius = 49528e3 / 2

# Mass in kilograms
mercury_mass = 0.33e24
venus_mass = 4.87e24
earth_mass = 5.97e24
mars_mass = 0.642e24
jupiter_mass = 1898e24
saturn_mass = 568e24
uranus_mass = 86.8e24
neptune_mass = 102e24

# Orbital velocity in meters per second
mercury_velocity = 47.40e3
venus_velocity = 35.02e3
earth_velocity = 29.78e3
mars_velocity = 24.06e3
jupiter_velocity = 13.06e3
saturn_velocity = 9.68e3
uranus_velocity = 6.80e3
neptune_velocity = 5.43e3

# Planets Data Structure
PLANETS_DATA = [
    {
        "name": "Mercury",
        "position": -0.387,  # AU from Sun
        "perihelion": 46.0e9,  # meters
        "radius": 4879e3 / 2,  # meters
        "mass": 0.33e24,  # kg
        "velocity": 47.40e3,  # m/s
        "is_inner": True
    },
    {
        "name": "Venus",
        "position": -0.723,
        "perihelion": 107.5e9,
        "radius": 12104e3 / 2,
        "mass": 4.87e24,
        "velocity": 35.02e3,
        "is_inner": True
    },
    {
        "name": "Earth",
        "position": -1.0,
        "perihelion": 147.1e9,
        "radius": 12756e3 / 2,
        "mass": 5.97e24,
        "velocity": 29.78e3,
        "is_inner": True
    },
    {
        "name": "Mars",
        "position": -1.524,
        "perihelion": 206.7e9,
        "radius": 6792e3 / 2,
        "mass": 0.642e24,
        "velocity": 24.06e3,
        "is_inner": True
    },
    {
        "name": "Jupiter",
        "position": -5.204,
        "perihelion": 740.6e9,
        "radius": 142984e3 / 2,
        "mass": 1898e24,
        "velocity": 13.06e3,
        "is_inner": False
    },
    {
        "name": "Saturn",
        "position": -9.573,
        "perihelion": 1357.6e9,
        "radius": 120536e3 / 2,
        "mass": 568e24,
        "velocity": 9.68e3,
        "is_inner": False
    },
    {
        "name": "Uranus",
        "position": -19.165,
        "perihelion": 2732.7e9,
        "radius": 51118e3 / 2,
        "mass": 86.8e24,
        "velocity": 6.80e3,
        "is_inner": False
    },
    {
        "name": "Neptune",
        "position": -30.178,
        "perihelion": 4471.1e9,
        "radius": 49528e3 / 2,
        "mass": 102e24,
        "velocity": 5.43e3,
        "is_inner": False
    }
]

# Major Asteroids
ASTEROID_CERES = {
    "name": "Ceres",
    "radius": 473e3,  # meters
    "mass": 9.393e20,  # kg
    "semi_major_axis": 2.77 * AU,
    "orbital_velocity": 17900,  # m/s
    "color": (180, 180, 180)
}

ASTEROID_VESTA = {
    "name": "Vesta",
    "radius": 262.7e3,
    "mass": 2.59e20,
    "semi_major_axis": 2.36 * AU,
    "orbital_velocity": 19300,
    "color": (190, 185, 180)
}