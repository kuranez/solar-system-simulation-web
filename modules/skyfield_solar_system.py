from skyfield.api import load
from skyfield.timelib import Time

import constants # For simulation constants like scale and colors
from objects import Planet, create_sun
from simulation.ephemeris import EphemerisManager
from simulation.scale import calculate_scaled_sizes # For calculating scaled sizes of planets based on current scale
from simulation.ephemeris import EphemerisManager # For loading Skyfield ephemeris data

def create_solar_system_skyfield():
    """Create objects in the solar system using Skyfield for real positions."""
    # Use the default simulation scale for initial planet rendering sizes.
    scaled_sizes = calculate_scaled_sizes(constants.DEFAULT_SCALE)

    # Load Skyfield data
    # Use most recent DE440s ephemeris for accurate planetary positions
    eph = EphemerisManager.get()
    # Load timescale and get current time
    ts = load.timescale()
    # Set time to now for current positions, or you can set it to a specific date/time
    t = ts.now()

    # Get the Sun object from Skyfield
    sun_obj = eph['SUN']
    # Create Sun at center with mass from constants
    sun = create_sun()
    # List to hold planet objects
    planets = []

    # Map planet names to the names Skyfield expects for the de440s kernel
    skyfield_names = {
        "MERCURY": "MERCURY",
        "VENUS": "VENUS",
        "EARTH": "EARTH", # Special handling for Earth to get the planet
        "MARS": "MARS BARYCENTER",
        "JUPITER": "JUPITER BARYCENTER",
        "SATURN": "SATURN BARYCENTER",
        "URANUS": "URANUS BARYCENTER",
        "NEPTUNE": "NEPTUNE BARYCENTER",
    }

    # Loop through our planet data and create Planet objects with positions and velocities from Skyfield
    for data in constants.PLANETS_DATA:
        planet_name_upper = data["name"].upper()
        
        # Get the correct skyfield object name from our map
        skyfield_name = skyfield_names.get(planet_name_upper)
        
        if skyfield_name is None:
            continue # Skip if we don't have a mapping for this planet

        # For Earth, we need to get the planet itself, not the barycenter with the Moon
        if planet_name_upper == "EARTH":
            sky_planet = eph['earth']
        else:
            sky_planet = eph[skyfield_name]

        # Get position and velocity from Skyfield
        astrometric = (sky_planet - sun_obj).at(t)
        position = astrometric.position
        velocity = astrometric.velocity

        # Convert from AU and AU/day to meters and m/s
        x = position.au[0] * constants.AU
        y = position.au[1] * constants.AU  # Use x and y for 2D projection
        
        vx = velocity.au_per_d[0] * constants.AU / (24 * 3600)
        vy = velocity.au_per_d[1] * constants.AU / (24 * 3600)

        # Create Planet object with scaled size and mass from constants
        planet = Planet(
            x,
            y,
            scaled_sizes[data["name"]],
            data["mass"],
            name=data["name"],
            is_inner_planet=data.get("is_inner", False)
        )
        # Set velocity from Skyfield data
        planet.x_vel = vx
        planet.y_vel = vy
        # Draw orbit lines for planets (except the Sun)
        planet.draw_line = True
        # Add planet to the list
        planets.append(planet)

    sun.draw_line = False
    return [sun] + planets