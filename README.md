# Solar System Simulation Web

Web implementation of my previous [Solar System Simulation](https://github.com/kuranez/solar-system-simulation) with simplified functionality for web rendering.

---

## 🌐 WebApp

> [![Live Demo](https://img.shields.io/badge/🟢%20Live%20App-Solar%20System%20Sim-422C71?style=for-the-badge)](https://apps.kuracodez.space/solar-system-sim/main)
>
> **Try the app - explore the solar system directly in your browser.**
>

---

## 💡 Features

- - **Interactive Simulation Controls:** Play, pause, and advance the simulation frame-by-frame.
- **Multiple Simulation Views:** Easily switch between different scenarios, such as the full solar system or a simple Sun-Earth system.
- **Web App built using Panel:** The entire user interface is built with the powerful and flexible Panel library.
- **Off-Screen Pygame Rendering:** Utilizes Pygame for high-performance, off-screen rendering of the simulation, served through the Panel web interface.

---

## ⚙️ Project Architecture

```
solar-system-simulation-web/
│
├── app.py                  # Main application entry point. Initializes Panel UI, state, and callbacks.
│
├── constants.py            # Central file for all simulation constants (physics, colors, scaling).
│
├── modules/
│   ├── simple_solar_system.py # Logic for creating the full solar system view.
│   ├── simple_sun_and_earth.py # Logic for creating the Sun-Earth view.
│   │
│   └── ui/
│       ├── css.py          # Contains all custom CSS for theming and styling widgets.
│       ├── hud.py          # Renders the Heads-Up Display (e.g., elapsed time).
│       ├── screen.py       # Handles the main Pygame drawing loop and surface-to-PNG conversion.
│       └── ui_handlers.py  # Contains all callback functions for UI events (e.g., play, pause, zoom).
│
└── simulation/
    ├── solarsystem_sim.py  # Core classes for celestial bodies (Body, Planet, Sun) and their physics.
    └── solarsystem_scale.py # Logic for calculating the dynamic scaling of planet sizes.
```

---

## 📦 Dependencies

- **`pygame`**: For off-screen rendering of the simulation.
- **`panel`**: For building the web interface and serving the application.
- **`numpy` & `math`**: For numerical operations, particularly in converting Pygame surfaces.
- **`Pillow`**: For image processing and handling the PNG conversion.

---

## 📗 Contributing

Pull requests, bug reports, and feature requests are welcome!

---

## 📘 License

This project is open source and available under the MIT License. You may modify, distribute, and use it freely in your own projects.