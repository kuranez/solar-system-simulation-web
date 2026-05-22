# solar_system.py
# Main module for the solar system simulation web app
# v.1.0 - Initial version with basic structure and imports

import constants
from simulation.solarsystem_sim import Planet, Sun
from simulation.solarsystem_scale import calculate_scaled_sizes

def create_solar_system():
    """Creates the solar system with the Sun, planets"""
    # Calculate scaled sizes for all planets based on current scale
    scaled_sizes = calculate_scaled_sizes(constants.DEFAULT_SCALE)
    
    # Create Sun at the center
    sun = Sun(0, 0, 1, constants.sun_mass)
    
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
        planets.append(planet)
    
    return [sun] + planets