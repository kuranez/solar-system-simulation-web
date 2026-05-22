# sun_and_earth.py
# Module to create Sun and Earth system
# v.1.0 - Initial creation

from simulation import constants
from simulation.solarsystem_sim import Planet, Sun
from simulation.solarsystem_scale import calculate_scaled_sizes

def create_sun_and_earth():
    """Creates the Sun and Earth."""
    # Calculate scaled sizes for Sun and Earth based on current scale
    scaled_sizes = calculate_scaled_sizes(constants.DEFAULT_SCALE)
    
    # Create Sun at the center
    sun = Sun(0, 0, 1, constants.sun_mass)
    
    # Find Earth's data in constants
    earth_data = next((p for p in constants.PLANETS_DATA if p['name'] == 'Earth'), None)
    
    if earth_data:
        earth_radius = scaled_sizes.get("Earth", earth_data["radius"])
        earth = Planet(
            earth_data["position"] * constants.AU, # x position
            0, # y position
            earth_radius, # scaled radius
            earth_data["mass"],
            earth_data["name"],
            color=constants.COLOR_EARTH
        )
        earth.y_vel = earth_data["velocity"]
        return [sun, earth]
    return [sun] # Return only sun if Earth data is not found