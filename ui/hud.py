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

    def _parent_of(body):
        return getattr(body, "parent_body", None) or getattr(body, "child_of", None)

    def _distance_between(body_a, body_b):
        return (((body_a.x - body_b.x) ** 2 + (body_a.y - body_b.y) ** 2) ** 0.5)

    def _distance_label(body, parent):
        if parent is None:
            return "stationary"

        distance = _distance_between(body, parent)
        if getattr(parent, "is_sun", False):
            return f"{distance / 1000:,.0f} km ({distance / constants.AU:.2f} AU)"

        return f"{distance / 1000:,.0f} km from {parent.name}"

    def _minmax_label(body, parent):
        if getattr(body, "static_body", False):
            return ""

        # Prefer instance attributes, fall back to constants lookup by name
        min_d = getattr(body, "perihelion", None) or getattr(body, "perigee", None) or getattr(body, "average_distance", None)
        max_d = getattr(body, "aphelion", None) or getattr(body, "apogee", None) or getattr(body, "average_distance", None)
        if min_d is None or max_d is None:
            const_entry = None
            try:
                const_entry = constants.BODIES_DATA.get(getattr(body, "name", ""), None) or (constants.MOON_DATA if getattr(body, "name", "") == "Moon" else None)
            except Exception:
                const_entry = None
            if const_entry:
                if min_d is None:
                    min_d = const_entry.get("perihelion") or const_entry.get("perigee") or const_entry.get("average_distance")
                if max_d is None:
                    max_d = const_entry.get("aphelion") or const_entry.get("apogee") or const_entry.get("average_distance")
        if min_d is None and max_d is None:
            return ""

        parts = []
        if min_d is not None:
            if getattr(parent, "is_sun", False):
                parts.append(f"min: {min_d/1000:,.0f} km ({min_d/constants.AU:.2f} AU)")
            else:
                parts.append(f"min: {min_d/1000:,.0f} km")
        if max_d is not None:
            if getattr(parent, "is_sun", False):
                parts.append(f"max: {max_d/1000:,.0f} km ({max_d/constants.AU:.2f} AU)")
            else:
                parts.append(f"max: {max_d/1000:,.0f} km")

        measured_mean = getattr(body, "orbit_delta_mean", None)
        if measured_mean is not None:
            reference = min_d if min_d is not None else max_d
            if reference:
                percent = (measured_mean / reference) * 100.0
                parts.append(f"Δmean: {percent:.2f}%")

        return " | " + " ".join(parts)

    def _render_row(body, parent, depth):
        if body in rendered:
            return
        rendered.add(body)

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

        # Render min/max as a subrow (indented) when available and body isn't stationary
        minmax = _minmax_label(body, parent)
        if minmax:
            # strip leading separator if present
            mm_text = minmax.lstrip(" | ")
            mm_surf = constants.FONT_1.render(mm_text, True, getattr(constants, "COLOR_HUD_TEXT", constants.COLOR_TEXT))
            screen.blit(mm_surf, (indent + 20, 10 + y_offset[0]))
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


    # Build mapping parent -> [children]. Prefer authoritative `parent.children`.
    children_map = defaultdict(list)
    rendered = set()
    for body in bodies:
        parent_children = getattr(body, "children", None)
        if parent_children:
            for child in parent_children:
                if child not in children_map[body]:
                    children_map[body].append(child)

    # Fallback for legacy parent_body links.
    for body in bodies:
        parent = _parent_of(body)
        if parent is not None and body not in children_map.get(parent, []):
            children_map[parent].append(body)

    # Render roots first, then their descendants.
    roots = [body for body in bodies if _parent_of(body) is None]
    for root in roots:
        if root in rendered:
            continue
        rendered.add(root)
        _render_row(root, None, 0)



