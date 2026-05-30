""" Full solar system with all planets (no asteroids) """

# Importing necessary libraries and modules
import constants # For simulation constants like scale and colors
from objects import Planet, create_sun
from simulation.scale import calculate_scaled_sizes # For calculating scaled sizes of planets based on current scale

# Function to create the solar system with the Sun, planets
def create_solar_system():
    """Creates the solar system with the Sun, planets"""
    sun = create_sun()

    scaled_sizes = calculate_scaled_sizes(constants.DEFAULT_SCALE)
    
    # Create planets based on constants data
    planets = []
    for planet_data in constants.PLANETS_DATA:
        radius = scaled_sizes.get(planet_data["name"], planet_data["radius"])
        planet = Planet(
            planet_data["position"] * constants.AU, # x position
            0, # y position
            radius, # scaled radius
            planet_data["mass"],
            planet_data["name"],
            planet_data["is_inner"]
        )
        planet.y_vel = planet_data["velocity"]
        planet.parent_body = sun
        planet.child_of = sun
        sun.children.append(planet)
        planets.append(planet)
    
    return [sun] + planets