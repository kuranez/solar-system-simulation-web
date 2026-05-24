# Changelog

## Summary

### Recent changes since main (v2-modular-sim)

- **[c4be4e4](https://github.com/kuranez/solar-system-simulation-web/commit/c4be4e4)** — Modular restructure: reworking classes, system views, and simulation logic to establish the v2 modular foundation.

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