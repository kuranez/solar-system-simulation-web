# Changelog

## Summary

The project has evolved from a basic demo into a high-performance web application:

- **Better Organization**: Moved from one big file to a modular system, separating the simulation logic from the user interface (74ada85, ca91ce6).
- **Shared Physics**: Created a standard "Body" model so planets and moons interact using the same reliable physics math (c7fa19a).
- **Live Browser Rendering**: Switched from sending static images to using a live "Canvas" via a template in the browser, which allows for smooth zooming and panning (4ae2a39).
- **Resource Efficiency**: Added "smart" data handling to prevent long-running simulations from slowing down or crashing the browser due to high RAM usage.

## Previous Releases

### v2.0 - Modular extendable basis for more complex simulations
- Refined the web app into a more complete solar system simulator with multiple views.
- Added the full solar system view alongside the simpler Sun-Earth scene.
- Kept live Play/Pause, step controls, zoom, and a clearer modular UI structure.
- Introduced the HUD and other early UI refinements while keeping the app lightweight.

### v1.7 - Simple Solar System

- Upgraded the app from the simple Sun-Earth layout to the full solar system.
- Added zoom controls alongside live play/pause and step controls.

### v.1.4 - Earth & Sun Simulation

- Initial minimal web version.
- Sun and Earth only.
- Basic Play/Pause and step controls.