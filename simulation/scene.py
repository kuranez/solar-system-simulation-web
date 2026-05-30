"""Scene presets and view registry for the solar system web app."""

from __future__ import annotations

import constants


SUN_EARTH_SCENE = {
	"sun_radius_px": 2,
	"earth_radius_px": 18,
	"earth_distance_m": constants.AU,
	"earth_velocity": constants.BODIES_DATA["Earth"]["orbital_velocity"],
	"simulation_timestep": constants.TIMESTEP,
}

EARTH_MOON_SCENE = {
	"earth_radius_px": 18,
	"moon_radius_px": 5,
	"moon_distance_m": constants.MOON_DATA["average_distance"],
	"moon_velocity": constants.MOON_DATA["orbital_velocity"],
	"distance_anchor_px": 350,
	"simulation_timestep": constants.TIMESTEP,
}

SUN_EARTH_MOON_SCENE = {
	"sun_radius_px": 4,
	"earth_radius_px": 20,
	"moon_radius_px": 6,
	"sun_earth_distance_m": constants.AU,
	"sun_earth_base_px": 420,
	"earth_moon_ratio": 0.257,
	"moon_min_px": 42,
	"simulation_timestep": constants.TIMESTEP,
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
	from ui.ui_handlers import update_proportional_sun_earth_moon, update_simple_earth_moon, update_simple_sun_earth

	return {
		"[Simple] Sun and Earth": {
			"title": "Simple Sun and Earth System",
			"description": "A simulation of the Sun and Earth system.",
			"generator": create_sun_earth_system,
			"base_scale": constants.DEFAULT_SCALE,
			"zoom_updater": update_simple_sun_earth,
			"scale_mode": "distance",
			"scene": SUN_EARTH_SCENE,
			**TRAIL_RETENTION,
		},
		"[Simple] Earth and Moon": {
			"title": "Simple Earth and Moon System",
			"description": "A simulation of the Earth and Moon system.",
			"generator": create_earth_moon_system,
			"base_scale": 350 / constants.MOON_DATA["average_distance"],
			"scale_mode": "distance",
			"zoom_updater": update_simple_earth_moon,
			"scene": EARTH_MOON_SCENE,
			**TRAIL_RETENTION,
		},
		"[Simple] Sun, Earth, and Moon System": {
			"title": "Sun, Earth, and Moon System",
			"description": "A simulation of the Sun, Earth, and Moon system.",
			"generator": create_sun_earth_moon_system,
			"base_scale": 1.0,
			"zoom_updater": update_proportional_sun_earth_moon,
			"scale_mode": "proportional",
			"scene": SUN_EARTH_MOON_SCENE,
			**TRAIL_RETENTION,
		},
		"[Simple] Solar System": {
			"title": "Simple Solar System (Planets only, no asteroids)",
			"description": "A simulation of the simple solar system with planets only.",
			"generator": create_solar_system,
			"base_scale": constants.DEFAULT_SCALE,
			"scale_mode": "distance",
			"zoom_updater": None,
			"scene": {
				"simulation_timestep": constants.TIMESTEP * 2,
			},
			**TRAIL_RETENTION,
		},
	}
