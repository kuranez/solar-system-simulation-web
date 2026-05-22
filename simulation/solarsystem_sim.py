# solarsystem_sim.py

from turtle import color

import constants
import pygame
import math
import itertools


# Solar system bodies
class Body:
    
    # Constants
    AU = constants.AU
    G = constants.G
    # DEFAULT_SCALE = constants.DEFAULT_SCALE
    TIMESTEP = constants.TIMESTEP

    def __init__(self, x, y, radius, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass

        self.color = (0, 0, 0)

        self.sun = False
        self.distance_to_sun = 0

        self.orbit = []

        self.x_vel = 0.0
        self.y_vel = 0.0

        self.draw_line = True


    def attraction(self, other):
        """Calculate the forces in x and y direction"""        
        # Coordinates
        dx, dy = other.x, other.y
        # Distances
        distance_x = dx - self.x
        distance_y = dy - self.y
        # Total Distance
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        if other.sun:
            self.distance_to_sun = distance
        # Force
        force = self.G * self.mass * other.mass / distance**2
        # Angle
        theta = math.atan2(distance_y, distance_x)
        # Forces
        fx = math.cos(theta) * force
        fy = math.sin(theta) * force

        return fx, fy

    def update_position(self, current_solarsystem):
        """Update Positions of objects"""
        # Total forces, conservation of mass
        total_fx = total_fy = 0

        # Calculate gravitational forces from other bodies
        for body in current_solarsystem:
            if self == body:
                continue

            fx, fy = self.attraction(body)
            total_fx += fx
            total_fy += fy

        # Update velocity based on acceleration a = F / m
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update position with velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # Append current position to the orbit
        self.orbit.append((self.x, self.y))

        # General limit for orbit length for all bodies
        general_trail_length = 20000  # Maximum points in the orbit for all bodies
        if len(self.orbit) > general_trail_length:
            self.orbit.pop(0)

    def draw(self, DISPLAYSURF, scale, screen_offset_x=0, screen_offset_y=0):
        """Draw the body and its faded orbit trail."""
        # Calculate position on screen
        x = self.x * scale + screen_offset_x
        y = self.y * scale + screen_offset_y

        # Draw the faded orbit trail
        if self.draw_line and len(self.orbit) >= 2:
            fade_scale = 1.5  # Adjust this value to control brightness
            orbit_points = [
                (
                    px * scale + screen_offset_x,
                    py * scale + screen_offset_y
                )
                for px, py in self.orbit
            ]
            for i in range(1, len(orbit_points)):
                distance = len(orbit_points) - i
                fade_factor = max(0, min(255, int(255 * (distance / len(orbit_points)) * fade_scale)))
                faded_color = (
                    int(self.color[0] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[0] * (fade_factor / 255)),
                    int(self.color[1] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[1] * (fade_factor / 255)),
                    int(self.color[2] * (1 - fade_factor / 255) + constants.COLOR_BACKGROUND[2] * (fade_factor / 255))
                )
                pygame.draw.line(DISPLAYSURF, faded_color, orbit_points[i - 1], orbit_points[i], 1)

        # Draw the body (planet or sun)
        pygame.draw.circle(DISPLAYSURF, self.color, (int(x), int(y)), int(self.radius))
    
# Sun
class Sun(Body):

    def __init__(self, x, y, radius, mass):
        super().__init__(x, y, radius, mass)
        self.sun = True
        self.name = "Sun"
        self.color = constants.COLOR_SUN
        self.orbit_count = 0  # Sun doesn't orbit but needs the attribute

    def draw(self, DISPLAYSURF, scale, screen_offset_x=0, screen_offset_y=0):
        super().draw(DISPLAYSURF, scale, screen_offset_x, screen_offset_y)


# Planets
class Planet(Body):
    cycle_colors = itertools.cycle([
        constants.COLOR_MERCURY,    # Mercury
        constants.COLOR_VENUS,      # Venus
        constants.COLOR_EARTH,      # Earths
        constants.COLOR_MARS,       # Mars
        constants.COLOR_JUPITER,    # Jupiter
        constants.COLOR_SATURN,     # Saturn
        constants.COLOR_URANUS,     # Uranus
        constants.COLOR_NEPTUNE     # Neptune
    ])

    def __init__(self, x, y, radius, mass, name, is_inner_planet=False, color=None):
        super().__init__(x, y, radius, mass)
        self.sun = False
        self.name = name
        if color:
            self.color = color
        else:
            self.color = next(Planet.cycle_colors)
        self.original_radius = radius  # Store the original size for later zooming

        # Orbit counting variables
        self.orbit = [] # Initialize orbit trail
        self.orbit_start_index = 0 # Start index for orbit trail
        self.last_complete_orbit = [] # Store the last complete orbit points

        self.orbit_count = 0
        self.prev_x = x
        self.prev_y = y
        self.orbit_detected = False
        self.has_crossed_reference = False  # Flag to track if the reference point has been crossed 

        # Visual indicator variables
        self.flash_timer = 0
        self.flash_duration = 10  # Duration in frames (1 second at 60 FPS)

    def update_position(self, current_solarsystem):
        """Update Positions of objects"""
        # Store previous position for orbit counting
        self.prev_x = self.x
        self.prev_y = self.y

        # Call the update_position method from Body to handle physics
        super().update_position(current_solarsystem)

        # Append current position to the orbit
        self.orbit.append((self.x, self.y))

        # Check if the planet has completed a full orbit
        self._check_orbit_completion()

        # Update the flash timer if it's active
        if self.flash_timer > 0:
            self.flash_timer -= 1

    def _check_orbit_completion(self):
        """Check if the planet has completed a full orbit by returning to start point."""
        # Only check for orbit completion if we have enough trail points
        if len(self.orbit) < 100:  # Need minimum points to have a meaningful orbit
            return
        
        # Get the starting point of the current orbit
        if self.orbit_start_index < len(self.orbit):
            start_point = self.orbit[self.orbit_start_index]
            current_point = (self.x, self.y)
            
            # Calculate distance from current position to start point
            distance_to_start = math.sqrt(
                (current_point[0] - start_point[0])**2 + 
                (current_point[1] - start_point[1])**2
            )
            
            # Define a threshold for "close enough" to starting point (relative to AU)
            threshold = 0.01 * self.AU  # 1% of AU distance
            
            # Check if we've returned close to the starting point
            if distance_to_start < threshold and not self.orbit_detected:
                # Make sure we've traveled far enough to be a real orbit
                if len(self.orbit) - self.orbit_start_index > 50:  # Minimum orbit length
                    self.orbit_count += 1
                    self.orbit_detected = True
                    
                    # Clear the old trail and start fresh for the new orbit
                    self.orbit = [(self.x, self.y)]  # Keep only current position
                    self.orbit_start_index = 0
                    
                    # Set the flash timer to create visual indicator
                    self.flash_timer = self.flash_duration
                    
                    # Print debug info
                    print(f"{self.name} completed orbit #{self.orbit_count}")
            
            # Reset detection flag when we're far enough from start point
            elif distance_to_start > threshold * 2:
                self.orbit_detected = False

    def draw(self, DISPLAYSURF, scale, screen_offset_x=0, screen_offset_y=0):
        """Draw the body with its orbit trail."""
        # Calculate position on screen
        x = self.x * scale + screen_offset_x
        y = self.y * scale + screen_offset_y
        
        # Draw orbit trail with fade effect
        if self.draw_line and len(self.orbit) >= 2:
            # Calculate the fade factor based on orbit count
            # Each completed orbit makes the trail 10% darker
            orbit_fade_multiplier = max(0.1, 1.0 - (self.orbit_count * 0.1))
            
            fade_scale = 1.0  # Adjust this value to control brightness
            orbit_points = [
                (
                    px * scale + screen_offset_x,
                    py * scale + screen_offset_y
                )
                for px, py in self.orbit
            ]
            
            # Draw the trail with both distance fade and orbit count fade
            for i in range(1, len(orbit_points)):
                # Distance-based fade (older parts of trail are more faded)
                distance = len(orbit_points) - i
                distance_fade_factor = max(0, min(255, int(255 * (distance / len(orbit_points)) * fade_scale)))
                
                # Combine orbit count fade with distance fade
                combined_fade = orbit_fade_multiplier * (1 - distance_fade_factor / 255)

                faded_color = (
                    int(self.color[0] * combined_fade + constants.COLOR_BACKGROUND[0] * (1 - combined_fade)),
                    int(self.color[1] * combined_fade + constants.COLOR_BACKGROUND[1] * (1 - combined_fade)),
                    int(self.color[2] * combined_fade + constants.COLOR_BACKGROUND[2] * (1 - combined_fade))
                )
                
                pygame.draw.line(DISPLAYSURF, faded_color, orbit_points[i - 1], orbit_points[i], 1)
        
        # Draw the planet itself
        pygame.draw.circle(DISPLAYSURF, self.color, (int(x), int(y)), int(self.radius))
        
        # If flash timer is active, add a visual indicator (bright ring)
        if self.flash_timer > 0:
            # Calculate flash intensity (fade out effect)
            flash_intensity = self.flash_timer / self.flash_duration
            
            # Draw a larger circle around the planet
            flash_radius = int(self.radius * (1.5 + flash_intensity))
            flash_color = (255, 255, 200)  # Bright yellow/white flash
            
            # Draw as a ring (not filled)
            pygame.draw.circle(DISPLAYSURF, flash_color, (int(x), int(y)), flash_radius, 2)

class Asteroid(Body):
    def __init__(self, x, y, radius, mass, color=(192, 192, 192)):
        super().__init__(x, y, radius, mass)
        self.sun = False
        self.name = "Asteroid"
        self.color = color  # Set asteroid color
        self.draw_line = False # Asteroids don't need orbit trails
    
    def draw(self, DISPLAYSURF, scale, screen_offset_x=0, screen_offset_y=0):
        """Optimized draw for asteroids"""
        x = self.x * scale + screen_offset_x
        y = self.y * scale + screen_offset_y
        
        # Only draw if on screen (culling)
        if 0 <= x <= constants.WIDTH and 0 <= y <= constants.HEIGHT:
            # Draw as simple circle (no fade trails)
            pygame.draw.circle(DISPLAYSURF, self.color, (int(x), int(y)), max(1, int(self.radius)))

    def update_position(self, current_solarsystem):
        """Only calculate attraction to the Sun for performance"""
        # The Sun is the first object in the solar system list
        sun = current_solarsystem[0]
        fx, fy = self.attraction(sun)
        self.x_vel += fx / self.mass * self.TIMESTEP
        self.y_vel += fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        # No orbit trail needed