# Class Diagram (Mermaid)

```mermaid
classDiagram
    %% Inheritance
    Body <|-- Planet
    Body <|-- Moon
    Body <|-- Asteroid

    %% Body (base)
    class Body {
        +class AU, G, TIMESTEP
        +float x, y
        +float original_x, original_y
        +float radius, original_radius
        +float mass
        +str name
        +tuple color
        +bool is_sun
        +bool sun
        +float distance_to_sun
        +bool static_body
        +Body child_of
        +Body parent_body
        +list children
        +list orbit
        +int orbit_count
        +int orbit_start_index
        +list last_complete_orbit
        +bool orbit_detected
        +float orbit_last_angle
        +float orbit_angle_accumulator
        +int orbit_samples_since_completion
        +int orbit_completion_cooldown
        +int orbit_complete_flash
        +float prev_x, prev_y
        +float x_vel, y_vel
        +bool draw_line
        +float visual_distance_scale  "optional override"
        +update_distance_to_sun(sun)
        +attraction(other) --> (fx, fy)
        +update_position(current_solarsystem)
        +_check_orbit_completion(current_solarsystem=None)
        +_screen_position(distance_scale, screen_offset_x=0, screen_offset_y=0)
        +_orbit_points(distance_scale, screen_offset_x=0, screen_offset_y=0)
        +_complete_orbit_points(distance_scale, ...)
        +_draw_point_trail(surface, orbit_points, ...)
        +_draw_orbit_trail(surface, distance_scale, ...)
        +draw(surface, distance_scale, screen_offset_x=0, screen_offset_y=0)
    }

    class Planet {
        +bool is_inner_planet
        +int flash_timer
        +int flash_duration
        +update_position(current_solarsystem)  "overrides Body"
        +draw(surface, distance_scale, ...)  "overrides Body"
    }

    class Moon {
        +Body child_of
        +Body parent_body
        +float x_vel, y_vel
        +auto-register in parent's children (constructor)
    }

    class Asteroid {
        +draw_line = False
        +update_position(current_solarsystem)  "custom physics"
        +draw(surface, distance_scale, ...)  "custom draw bounds-check"
    }

    %% Associations / notes
    Body "1" o-- "*" Moon : "children / parent relationship"
    Body "1" o-- "*" Planet : "system membership"
    Body "1" o-- "*" Asteroid : "system membership"
    Body ..> "Sun-like flag" : "is_sun / sun attribute"

    %% Simulation helpers (module-level functions)
    class PhysicsModule {
        +circular_orbital_speed(central_mass, radius)
        +update_distance_to_sun(body, sun)
        +attraction(body, other)
        +find_sun(current_solarsystem)
        +advance_body(body, current_solarsystem, timestep=None)
    }

    %% UI note
    class HUD {
        +render_hud(screen, bodies, state)
    }

    PhysicsModule --> Body : "advance_body / attraction / distance updates"
    Body --> HUD : "orbit_count / orbit_complete_flash used for display"
```
```
