"""Create a simple stationary Sun-Earth-Moon system."""

from objects.base import Body

import constants

earth_radius_ratio = (
    constants.BODIES_DATA["Earth"]["radius"] / constants.BODIES_DATA["Moon"]["radius"]
)

def create_sun_earth_moon_system(
    earth_radius_px=max(1, int(constants.BASE_SIZE * 0.8)),
    sun_radius_px=2,
):
    """Create a dynamic Sun-Earth-Moon system using SI units for positions.

    Positions are specified in meters so the physics engine advances bodies
    correctly. Radii remain in pixels for rendering.
    """
    moon_radius_px = max(1, int(earth_radius_px / earth_radius_ratio))

    # Visual baseline for proportional view (pixels)
    sun_earth_base_px = 420
    earth_moon_ratio = 0.257

    # Place Sun at origin (meters)
    sun = Body(0.0, 0.0, sun_radius_px, constants.sun_mass, name="Sun", color=constants.COLOR_SUN, is_sun=True)
    sun.static_body = True
    sun.draw_line = False

    # Store original pixel positions/radii used by proportional view updaters
    sun.original_x = 0
    sun.original_y = 0
    sun.original_radius = sun_radius_px

    # Earth at 1 AU from Sun (meters)
    earth_x_m = -constants.AU
    earth = Body(earth_x_m, 0.0, earth_radius_px, constants.BODIES_DATA["Earth"]["mass"], name="Earth", color=constants.COLOR_EARTH)
    earth.static_body = False
    earth.draw_line = True
    earth.child_of = sun
    earth.parent_body = sun
    sun.children.append(earth)

    # original pixel placement for proportional view
    earth.original_x = sun_earth_base_px
    earth.original_y = 0
    earth.original_radius = earth_radius_px

    # Give Earth the approximate orbital velocity around the Sun
    earth.y_vel = constants.BODIES_DATA["Earth"]["orbital_velocity"]
    # Use a smaller integration timestep for Earth and Moon to keep close-orbit
    # dynamics stable (seconds). Default TIMESTEP is 86400 (1 day); use 3600s (1 hour).
    earth.TIMESTEP = 600.0

    # Moon positioned relative to Earth using average distance (meters)
    moon_x_m = earth_x_m - constants.MOON_DATA["average_distance"]
    moon = Body(moon_x_m, 0.0, moon_radius_px, constants.MOON_DATA["mass"], name="Moon", color=constants.MOON_DATA["color"])
    moon.static_body = False
    moon.draw_line = True
    moon.child_of = earth
    moon.parent_body = earth
    earth.children.append(moon)

    # original pixel placement for proportional view (relative to Earth's original)
    moon.original_x = earth.original_x + sun_earth_base_px * earth_moon_ratio
    moon.original_y = 0
    moon.original_radius = moon_radius_px

    # Moon's velocity should be Earth velocity plus the Moon's orbital velocity around Earth
    moon.y_vel = earth.y_vel + constants.MOON_DATA["orbital_velocity"]
    moon.TIMESTEP = 600.0

    return [sun, earth, moon]
