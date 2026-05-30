""" simulation/solarsystem_scale.py

    # Module to handle scaling of planet sizes based on 
    # current zoom level in the solar system simulation

"""

# Importing necessary libraries and modules
import constants
import math

# Scale calculations
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

def scale_bodies_from_original_radius(bodies, scale, body_names=None):
    """Scale body radii from each body's `original_radius` baseline."""
    name_set = set(body_names) if body_names is not None else None
    for body in bodies:
        if name_set is not None and getattr(body, "name", None) not in name_set:
            continue
        if hasattr(body, "original_radius"):
            body.radius = max(1, int(body.original_radius * scale))

def calculate_hierarchical_scale(parent, target, scale, scene_cfg, mode="linear"):
    """Compute a visual distance_scale to anchor a child body to its parent."""
    parent_name = getattr(parent, "name", "").lower()
    target_name = getattr(target, "name", "").lower()
    delta_m = math.sqrt((target.x - parent.x)**2 + (target.y - parent.y)**2)

    if delta_m <= 0:
        return 1.0

    if mode == "logarithmic":
        # Logarithmic mapping: compress orbits so massive ranges (Sun vs Moon) fit.
        # 1 AU is mapped to sun_earth_base_px * scale.
        log_au = math.log10(constants.AU)
        log_dist = math.log10(delta_m)
        ref_px = scene_cfg.get("sun_earth_base_px", 350)
        desired_px = (ref_px * scale) * (log_dist / log_au)
    else:
        # Try absolute pixel value first (e.g., 'earth_moon_px')
        abs_px_key = f"{parent_name}_{target_name}_px"
        if abs_px_key in scene_cfg:
            desired_px = scene_cfg[abs_px_key] * scale
        else:
            # Fallback to ratio-based calculation
            base_px = scene_cfg.get("sun_earth_base_px", 350)
            ratio = scene_cfg.get(f"{parent_name}_{target_name}_ratio", 0.1)
            desired_px = base_px * ratio * scale

    min_px = scene_cfg.get(f"{target_name}_min_px", 12)
    desired_px = max(desired_px, min_px)

    return desired_px / delta_m
