# solar_system.py
# Main module for the solar system simulation web app
# v.1.1 - Tweaked comments and structure for better readability
# author: kuranez

# Importing necessary libraries and modules
import constants # For simulation constants like scale and colors
from simulation.solarsystem_sim import Planet, Sun # For defining celestial bodies
from simulation.solarsystem_scale import calculate_scaled_sizes # For calculating scaled sizes of planets based on current scale

# Function to create the solar system with the Sun, planets
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