# hud.py 
# Handles rendering of informational text overlays (HUD)
# v.1.5 - Added total elapsed simulation time display in years and days, improved formatting of distance and scale information
# author: kuranez

# Importing necessary libraries
import pygame # For rendering text on the screen
import constants as constants # For HUD text color and other constants


def render_hud(screen, bodies, state):
    """Renders the Heads-Up Display (HUD) with information about the simulation."""
    
    y_offset = 0  # Initial vertical offset for text lines

    # Display the total elapsed simulation time in years and days
    total_elapsed_time = state['total_elapsed_time']

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

    y_offset += 20 # Move down for the next line of text

    # Display the current scale of the simulation in meters per pixel
    meters_per_pixel = constants.AU / state['distance_scale']

    scale_text = (
        f"Scale: {meters_per_pixel:.2e} m/px"
    )

    text_surface = constants.FONT_1.render(
        scale_text,
        True,
        constants.COLOR_TEXT
    )

    screen.blit(text_surface, (10, 10 + y_offset))

    y_offset += 20 # Move down for the next line of text

    # Display the name and distance of each celestial body from the Sun
    for body in bodies:
        # Ensure the body is a celestial body and not the sun before rendering
        if hasattr(body, 'is_sun') and body.is_sun:
            continue

        distance_km = body.distance_to_sun / 1000
        distance_au = body.distance_to_sun / constants.AU
            
        # Base text with name and distance
        text = f"{body.name}: {distance_km:,.0f} km ({distance_au:.2f} AU)"

            
        # Add orbit count if available
        if hasattr(body, 'orbit_count') and body.orbit_count > 0:
            text += f" | Orbits: {body.orbit_count}"
        else:
            text += " | Orbits: 0"
            
        text_surface = constants.FONT_1.render(text, True, body.color)
        screen.blit(text_surface, (10, 10 + y_offset))
        y_offset += 20



