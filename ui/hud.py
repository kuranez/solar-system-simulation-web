""" ui/hud.py

    # Handles rendering of informational text overlays (HUD)
    # Displays elapsed simulation time, 
    # current scale, distances of bodies to the sun, 
    # orbits count, and other relevant info

"""

import pygame
import constants
from collections import defaultdict


def render_hud(screen, bodies, state):
    """Renders the Heads-Up Display (HUD) with information about the simulation."""

    y_offset = 0  # Initial vertical offset for text lines

    sun = next((body for body in bodies if getattr(body, "is_sun", False)), None)

    def _distance_between(body_a, body_b):
        return (((body_a.x - body_b.x) ** 2 + (body_a.y - body_b.y) ** 2) ** 0.5)

    # Display the total elapsed simulation time in years and days
    total_elapsed_time = state["total_elapsed_time"]

    # Format the elapsed time into years and days for better readability
    years = int(total_elapsed_time // (365.25 * 24 * 3600))
    remaining_time = total_elapsed_time % (365.25 * 24 * 3600)
    days = int(remaining_time // (24 * 3600))

    if years > 0:
        time_text = f"Time: {years}y {days}d"
    else:
        time_text = f"Time: {days}d"

    text_surface = constants.FONT_1.render(time_text, True, constants.COLOR_TEXT)
    screen.blit(text_surface, (10, 10 + y_offset))

    y_offset += 20  # Move down for the next line of text

    # Display the current scale of the simulation in meters per pixel
    meters_per_pixel = constants.AU / state["distance_scale"]

    scale_text = f"Scale: {meters_per_pixel:.2e} m/px"

    text_surface = constants.FONT_1.render(scale_text, True, constants.COLOR_TEXT)
    screen.blit(text_surface, (10, 10 + y_offset))

    y_offset += 20  # Move down for the next line of text

    # Transient notifications: show any bodies that just completed an orbit
    notifications = []
    for b in bodies:
        if getattr(b, "orbit_complete_flash", 0) > 0:
            notifications.append(f"{b.name} completed an orbit")

    if notifications:
        # Render notifications in the top-right corner, stacking downward
        nx = screen.get_width() - 10
        ny = 10
        for note in notifications:
            note_surf = constants.FONT_1.render(note, True, constants.COLOR_TEXT)
            screen.blit(note_surf, (nx - note_surf.get_width(), ny))
            ny += 20

    # Build mapping parent -> [children]. Prefer the authoritative `parent.children` lists
    children_map = defaultdict(list)
    for b in bodies:
        parent_children = getattr(b, "children", None)
        if parent_children:
            for child in parent_children:
                children_map[b].append(child)

    # Fallback: include any objects that still only have legacy `parent_body` set
    for b in bodies:
        parent = getattr(b, "parent_body", None)
        if parent is not None:
            # avoid duplicating entries already registered via parent.children
            if b not in children_map.get(parent, []):
                children_map[parent].append(b)

    # Display top-level bodies (skip sun), and render their children indented below
    for body in bodies:
        if getattr(body, "is_sun", False):
            continue

        # Skip child entries here; they'll be rendered under their parent
        if getattr(body, "parent_body", None) is not None:
            continue

        if sun is not None:
            distance_to_sun = _distance_between(body, sun)
        else:
            distance_to_sun = body.distance_to_sun

        distance_km = distance_to_sun / 1000
        distance_au = distance_to_sun / constants.AU

        text = f"{body.name}: {distance_km:,.0f} km ({distance_au:.2f} AU)"

        # Add orbit count if available (show the actual count, even if 0)
        if hasattr(body, "orbit_count"):
            text += f" | Orbits: {body.orbit_count}"

        text_surface = constants.FONT_1.render(text, True, body.color)
        screen.blit(text_surface, (10, 10 + y_offset))
        y_offset += 20

        # Render children (moons) as indented rows under the parent
        for child in children_map.get(body, []):
            if sun is not None:
                child_distance_to_sun = _distance_between(child, sun)
            else:
                child_distance_to_sun = child.distance_to_sun

            child_km = child_distance_to_sun / 1000
            child_au = child_distance_to_sun / constants.AU

            child_text = f"- {child.name}: {child_km:,.0f} km ({child_au:.2f} AU)"
            if hasattr(child, "orbit_count"):
                child_text += f" | Orbits: {child.orbit_count}"

            child_surface = constants.FONT_1.render(child_text, True, child.color)
            # Indent child entries slightly
            screen.blit(child_surface, (30, 10 + y_offset))
            y_offset += 20



