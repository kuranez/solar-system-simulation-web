"""ui/hud.py

Handles rendering of informational text overlays (HUD).
"""

from collections import defaultdict

import pygame

import constants


def render_hud(screen, bodies, state):
    """Render the simulation HUD using a generic parent/child hierarchy."""

    y_offset = [0]
    sun = next((body for body in bodies if getattr(body, "is_sun", False)), None)

    def _distance_between(body_a, body_b):
        return (((body_a.x - body_b.x) ** 2 + (body_a.y - body_b.y) ** 2) ** 0.5)

    def _distance_label(body, parent):
        if parent is None:
            return "stationary"

        distance = _distance_between(body, parent)
        if getattr(parent, "is_sun", False):
            return f"{distance / 1000:,.0f} km ({distance / constants.AU:.2f} AU)"

        return f"{distance / 1000:,.0f} km from {parent.name}"

    def _render_row(body, parent, depth):
        indent = 10 + (depth * 20)
        prefix = "- " if depth > 0 else ""

        if getattr(body, "static_body", False):
            text = f"{prefix}{body.name}: stationary"
        elif parent is None:
            if getattr(body, "is_sun", False):
                text = f"{body.name}: stationary"
            else:
                distance = _distance_between(body, sun) if sun is not None else getattr(body, "distance_to_sun", 0.0)
                text = f"{body.name}: {distance / 1000:,.0f} km ({distance / constants.AU:.2f} AU)"
                if hasattr(body, "orbit_count"):
                    text += f" | Orbits: {body.orbit_count}"
        else:
            text = f"{prefix}{body.name}: {_distance_label(body, parent)}"
            if hasattr(body, "orbit_count"):
                text += f" | Orbits: {body.orbit_count}"

        text_surface = constants.FONT_1.render(text, True, body.color)
        screen.blit(text_surface, (indent, 10 + y_offset[0]))
        y_offset[0] += 20

        for child in children_map.get(body, []):
            _render_row(child, body, depth + 1)

    # Display elapsed simulation time in years and days.
    total_elapsed_time = state["total_elapsed_time"]
    years = int(total_elapsed_time // (365.25 * 24 * 3600))
    remaining_time = total_elapsed_time % (365.25 * 24 * 3600)
    days = int(remaining_time // (24 * 3600))
    time_text = f"Time: {years}y {days}d" if years > 0 else f"Time: {days}d"

    text_surface = constants.FONT_1.render(time_text, True, constants.COLOR_TEXT)
    screen.blit(text_surface, (10, 10 + y_offset[0]))
    y_offset[0] += 20

    meters_per_pixel = constants.AU / state["distance_scale"]
    scale_text = f"Scale: {meters_per_pixel:.2e} m/px"
    text_surface = constants.FONT_1.render(scale_text, True, constants.COLOR_TEXT)
    screen.blit(text_surface, (10, 10 + y_offset[0]))
    y_offset[0] += 20

    # Transient notifications: show any bodies that just completed an orbit.
    notifications = [f"{b.name} completed an orbit" for b in bodies if getattr(b, "orbit_complete_flash", 0) > 0]
    if notifications:
        nx = screen.get_width() - 10
        ny = 10
        for note in notifications:
            note_surf = constants.FONT_1.render(note, True, constants.COLOR_TEXT)
            screen.blit(note_surf, (nx - note_surf.get_width(), ny))
            ny += 20

    # Build mapping parent -> [children]. Prefer authoritative `parent.children`.
    children_map = defaultdict(list)
    for body in bodies:
        parent_children = getattr(body, "children", None)
        if parent_children:
            for child in parent_children:
                children_map[body].append(child)

    # Fallback for legacy parent_body links.
    for body in bodies:
        parent = getattr(body, "parent_body", None)
        if parent is not None and body not in children_map.get(parent, []):
            children_map[parent].append(body)

    # Render roots first, then their descendants.
    roots = [body for body in bodies if getattr(body, "parent_body", None) is None]
    rendered = set()
    for root in roots:
        if root in rendered:
            continue
        rendered.add(root)
        _render_row(root, None, 0)



