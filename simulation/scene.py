"""Scene presets and view registry for the solar system web app."""

from __future__ import annotations

import constants


SUN_EARTH_SCENE = {
	"sun_radius_px": 2,
	"earth_radius_px": 30,
	"earth_distance_m": constants.AU,
	"sun_earth_base_px": 600,
	"earth_velocity": constants.BODIES_DATA["Earth"]["orbital_velocity"],
	"simulation_timestep": constants.TIMESTEP/2,
}

EARTH_MOON_SCENE = {
	"earth_radius_px": 60,
	"moon_radius_px": 20,
	"moon_distance_m": constants.MOON_DATA["average_distance"],
	"moon_velocity": constants.MOON_DATA["orbital_velocity"],
	"earth_moon_px": 350,
	"simulation_timestep": 600,
}

SUN_EARTH_MOON_SCENE = {
	"sun_radius_px": 2,
	"earth_radius_px": 30,
	"moon_radius_px": 12,
	"sun_earth_distance_m": constants.AU,
	"sun_earth_base_px": constants.DEFAULT_SCALE * 2,
	"earth_moon_distance_m": constants.MOON_DATA["average_distance"],
	"earth_velocity": constants.BODIES_DATA["Earth"]["orbital_velocity"],
	"moon_velocity": constants.BODIES_DATA["Earth"]["orbital_velocity"] + constants.MOON_DATA["orbital_velocity"],
	"moon_min_px": 120,
	"simulation_timestep": 600,
}

TRAIL_RETENTION = {
	"max_completed_orbit_trails": 5,
	"min_orbits_before_prune": 1,
}


def build_simulation_views():
	"""Build the app's view registry from scene presets and generators."""
	from modules.simple_earth_moon import create_earth_moon_system
	from modules.simple_solar_system import create_solar_system
	from modules.simple_sun_earth import create_sun_earth_system
	from modules.simple_sun_earth_moon import create_sun_earth_moon_system
	from modules.solar_system import create_solar_system_skyfield
	return {
		"[Simple] Sun and Earth": {
			"title": "Simple Sun and Earth System",
			"description": "A simulation of the Sun and Earth system.",
			"generator": create_sun_earth_system,
			"base_scale": 600 / constants.AU,
			"scale_mode": "distance",
			"scaled_bodies": ["Sun", "Earth"],
			"scene": SUN_EARTH_SCENE,
			**TRAIL_RETENTION,
		},
		"[Simple] Earth and Moon": {
			"title": "Simple Earth and Moon System",
			"description": "A simulation of the Earth and Moon system.",
			"generator": create_earth_moon_system,
			"base_scale": constants.DEFAULT_SCALE,
			"scale_mode": "distance",
			"scaled_bodies": ["Earth", "Moon"],
			"visual_anchors": [("Earth", "Moon")],
			"scene": EARTH_MOON_SCENE,
			**TRAIL_RETENTION,
		},
		"[Simple] Sun, Earth, and Moon System": {
			"title": "Sun, Earth, and Moon System",
			"description": "A simulation of the Sun, Earth, and Moon system.",
			"generator": create_sun_earth_moon_system,
			"base_scale": 600 / constants.AU,
			"scale_mode": "logarithmic",
			"scaled_bodies": ["Sun", "Earth", "Moon"],
			"visual_anchors": [("Earth", "Moon")],
			"scene": SUN_EARTH_MOON_SCENE,
			**TRAIL_RETENTION,
		},
		"[Simple] Solar System": {
			"title": "Simple Solar System (Planets only, no asteroids)",
			"description": "A simulation of the simple solar system with planets only.",
			"generator": create_solar_system,
			"base_scale": constants.DEFAULT_SCALE,
			"scale_mode": "distance",
			"scene": {
				"simulation_timestep": constants.TIMESTEP * 2,
			},
			**TRAIL_RETENTION,
		},
		"[JPL] Solar System": {
			"title": "JPL Ephemeris Solar System",
			"description": "A simulation of the solar system using JPL ephemeris data.",
			"generator": create_solar_system_skyfield,
			"base_scale": constants.DEFAULT_SCALE,
			"scale_mode": "distance",
			"scene": {
				"simulation_timestep": constants.TIMESTEP * 2,
			},
			**TRAIL_RETENTION,
		},
	}
