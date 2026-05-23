"""Sun preset factory."""

import constants

from ..base import Body


def create_sun():
	sun = Body(0, 0, 1, constants.sun_mass, name="Sun", color=constants.COLOR_SUN, is_sun=True)
	sun.orbit_count = 0
	return sun
