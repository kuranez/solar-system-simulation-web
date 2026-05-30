# Changelog

## Summary

### Recent changes since main (v2-modular-sim)

Summary of major jumps in architecture, simulation logic and UI _(timeline, oldest → newest)_:

| Event | Details |
|---:|---|
| **[v1.4](https://github.com/kuranez/solar-system-simulation-web/commits/v.1.4)** | **Initial minimal web app** — single-file Sun+Earth demo with basic Play/Pause and step controls (baseline). |
| **[a3322f7](https://github.com/kuranez/solar-system-simulation-web/commit/a3322f7)** | **HUD introduced** — elapsed time and per-body telemetry added to the overlay for runtime insight. |
| **[4aa1718](https://github.com/kuranez/solar-system-simulation-web/commit/4aa1718)** | **Full solar system added** — expanded simulation generator to include all major planets and related data. |
| **[a1d0d8b](https://github.com/kuranez/solar-system-simulation-web/commit/a1d0d8b)** | **Zoom support added** — orbital distance scaling controls for exploring the system visually. |
| **[095535d](https://github.com/kuranez/solar-system-simulation-web/commit/095535d)** / **[bc17f10](https://github.com/kuranez/solar-system-simulation-web/commit/bc17f10)** / **[bb341c8](https://github.com/kuranez/solar-system-simulation-web/commit/bb341c82)** | **Zoom bugfixes and polish** — multiple fixes to make zoom reliable across views. |
| **[74ada85](https://github.com/kuranez/solar-system-simulation-web/commit/74ada85)** | **UI modularization** — created `modules/ui` and restructured UI code for clearer responsibilities. |
| **[ca91ce6](https://github.com/kuranez/solar-system-simulation-web/commit/ca91ce6)** | **Rendering and handlers outsourced** — moved screen creation and UI handlers out of `app.py`, centralizing surface-to-PNG and callbacks. |
| **[ed2ad19](https://github.com/kuranez/solar-system-simulation-web/commit/ed2ad19)** / **[6817c7f](https://github.com/kuranez/solar-system-simulation-web/commit/6817c7f)** | **Architecture refactor for modularity** — larger project restructuring to support multiple views and future extensions. |
| **[91f9c45](https://github.com/kuranez/solar-system-simulation-web/commit/91f9c45)** | **Docs, cleanup and repo hygiene** — README/badges, removed Docker artifacts and cleaned pycache; prepared the v2.0 notes. |
| **[c4be4e4](https://github.com/kuranez/solar-system-simulation-web/commit/c4be4e4)** | **Modular restructure** — reworked classes, system views, and simulation logic to establish the v2 modular foundation. |
| **[34ea9f4](https://github.com/kuranez/solar-system-simulation-web/commit/34ea9f4)** | **Updated docs** — refreshed documentation after the modular restructuring. |
| **[c7fa19a](https://github.com/kuranez/solar-system-simulation-web/commit/c7fa19a)** | **Refactor - New module structure, base class for bodies, physics module** — introduced the base body model and shared physics layer. |
| **[6b82f5b](https://github.com/kuranez/solar-system-simulation-web/commit/6b82f5b)** | **Improved orbit trails** — refined trail rendering and orbit visualization. |
| **[6dd8d03](https://github.com/kuranez/solar-system-simulation-web/commit/6dd8d03)** | **Sun, Earth, Moon system - Fixed moon orbit trails** — attached moon trails correctly in the hierarchical view. |
| **[d928ec6](https://github.com/kuranez/solar-system-simulation-web/commit/d928ec6)** | **Fixed and updated Zoom & scaling for all modules** — aligned zoom and scaling behavior across views. |
| **[b26277d](https://github.com/kuranez/solar-system-simulation-web/commit/b26277d)** | **Removed duplicate code** — cleaned repeated logic from the modular refactor. |
| **[5d82f55](https://github.com/kuranez/solar-system-simulation-web/commit/5d82f55)** | **HUD customized for earth and moon system** — tailored overlay output for the Earth-Moon view. |
| **[41c4895](https://github.com/kuranez/solar-system-simulation-web/commit/41c4895)** | **HUD tree view for systems** — added hierarchical HUD display for bodies and their children. |
| **[7a897a3](https://github.com/kuranez/solar-system-simulation-web/commit/7a897a3)** | **Updated custom scene simplifying system creation with preset** — streamlined scene creation using presets. |
| **[cf5d717](https://github.com/kuranez/solar-system-simulation-web/commit/cf5d717)** | **Changing scene resets timer.** — reset elapsed time when switching views. |
| **[a64e0ee](https://github.com/kuranez/solar-system-simulation-web/commit/a64e0ee)** | **Removed comment.** — cleanup commit removing stale text. |
| **[a87e5af](https://github.com/kuranez/solar-system-simulation-web/commit/a87e5af)** | **Sun and earth system also simplified using presets** — applied the preset-based scene simplification to Sun-Earth. |
| **[69763ea](https://github.com/kuranez/solar-system-simulation-web/commit/69763ea)** | **Added asteroids and moons.** — expanded the object set with additional small bodies. |
| **[3ac6dc2](https://github.com/kuranez/solar-system-simulation-web/commit/3ac6dc2)** | **Reworked Layout** — reorganized the app layout for the new modular UI. |
| **[f14a95d](https://github.com/kuranez/solar-system-simulation-web/commit/f14a95d)** | **Update class diagram** — refreshed architecture documentation. |
| **[4ae2a39](https://github.com/kuranez/solar-system-simulation-web/commit/4ae2a39)** | **Implemented canvas rendering using templates** — introduced template-based browser canvas rendering. |
| **[086c8e8](https://github.com/kuranez/solar-system-simulation-web/commit/086c8e8)** | **Updated constants with aphelion data and added Pluto** — expanded orbital data and object coverage. |
| **[2b1fbaf](https://github.com/kuranez/solar-system-simulation-web/commit/2b1fbaf)** | **Changed HUD font to monospaced, removed and renamed legacy modules** — cleaned up old module naming and improved HUD readability. |
| **[6cd141c](https://github.com/kuranez/solar-system-simulation-web/commit/6cd141c)** | **Updated README** — refreshed project documentation and usage guidance. |
| **[2910ea8](https://github.com/kuranez/solar-system-simulation-web/commit/2910ea8)** | **Added simulation speed controls** — introduced speed adjustment controls for playback. |
| **[c391d2b](https://github.com/kuranez/solar-system-simulation-web/commit/c391d2b)** | **Update requirements** — refreshed dependency pins and environment requirements. |

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