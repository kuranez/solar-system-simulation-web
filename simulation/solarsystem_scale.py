# solarsystem_scale.py
# Module to handle scaling of planet sizes based on current zoom level in the solar system simulation
# v.1.1 - Adjusted for scaled sizes based on current scale
# author: kuranez

import constants
import math

# Scale calculations

# def scale_planet_size(planet_radius, distance_scale, is_outer_planet=False):
#     """Scale the planet size based on Earth diameter and current scale (zoom)."""
#     diameter = planet_radius * 2
#     scale_factor = constants.OUTER_PLANET_SCALE_FACTOR if is_outer_planet else 1
#     # Multiply by scale so planet size grows/shrinks with zoom
#     return (diameter / constants.earth_diameter) * constants.BASE_SIZE * scale_factor * distance_scale / constants.DEFAULT_SCALE

def scale_planet_size(planet_radius, distance_scale, is_outer_planet=False):
    diameter = planet_radius * 2

    scale_factor = (
        constants.OUTER_PLANET_SCALE_FACTOR
        if is_outer_planet
        else 1
    )

    base_size = (
        diameter / constants.earth_diameter
    ) * constants.BASE_SIZE * scale_factor

    zoom_factor = (
        distance_scale / constants.DEFAULT_SCALE
    ) * constants.PLANET_ZOOM_EXPONENT

    return base_size * zoom_factor

def calculate_scaled_sizes(distance_scale):
    """Calculate scaled sizes for all planets using radius and current distance scale."""
    scaled_sizes = {}
    
    # Add planets from PLANETS_DATA
    for planet_data in constants.PLANETS_DATA:
        planet_name = planet_data["name"]
        planet_radius = planet_data["radius"]
        is_outer = not planet_data["is_inner"]
        scaled_sizes[planet_name] = scale_planet_size(planet_radius, distance_scale, is_outer_planet=is_outer)
    
    return scaled_sizes

# # Get Sizes
# scaled_sizes = calculate_scaled_sizes()

# def main():
#     """Main function to execute calculations and display results."""
#     for planet, size in scaled_sizes.items():
#         print(f"{planet}: {size:.2f} pixels")

# if __name__ == "__main__":
#     main()