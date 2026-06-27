# Solar System Simulation Web
<p align="left">
    <a href="https://www.python.org/" target="_blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
    </a>
    <a href="https://rhodesmill.org/skyfield/" target="_blank">
        <img src="https://img.shields.io/badge/Skyfield-00008B?style=for-the-badge" alt="Pygame"/>
    </a>
    <a href="https://www.pygame.org" target="_blank">
        <img src="https://img.shields.io/badge/Pygame-62B66B?style=for-the-badge&logo=pygame&logoColor=white" alt="Pygame"/>
    </a>
    <a href="https://panel.holoviz.org/" target="_blank">
        <img src="https://img.shields.io/badge/Holoviz%20Panel-0094A9?style=for-the-badge" alt="Holoviz Panel"/>
    </a>
    <a href="https://docs.docker.com/" target="_blank">
        <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
    </a>
</p>

Web implementation of my previous [Solar System Simulation](https://github.com/kuranez/solar-system-simulation) with simplified functionality for web rendering.

---

## 🌐 WebApp

> [![Live Demo](https://img.shields.io/badge/🟢%20Live%20App-Solar%20System%20Sim-422C71?style=for-the-badge)](https://apps.kuracodez.space/solar-system-sim/app)
>
> **Try the app - explore the solar system directly in your browser.**
>

---

## 💡 Features
- **High-Precision Physics:** Utilizes JPL ephemeris data via Skyfield for accurate initial planet positions and velocities. All planetary data (mass, radius, orbital parameters) is based on NASA's fact sheets.
- **Live Interactive Rendering:** A client-side HTML5 Canvas provides smooth, responsive panning and zooming without waiting for the server.
- **Advanced Orbit Trails:** Completed orbits are shown with a distinct, solid color, while the active trail has a smooth gradient fade for visual clarity.
- **Dynamic HUD:** The Heads-Up Display provides real-time data on simulation time, speed, scale, and detailed orbital information for each celestial body.
- **Multiple Simulation Views:** Easily switch between different scenarios, from a simple Sun-Earth system to the full JPL-powered solar system.
- **Flexible Controls:** Adjust simulation speed, play/pause, and reset the view.

---

## ⚙️ Project Architecture

```yaml
solar-system-simulation-web/
│
├── app.py              # Main application entry point. Initializes Panel UI, state, and callbacks.
├── constants.py        # Central file for physical constants, colors, and celestial body data.
├── modules/            # Simulation view generators (e.g., simple systems, JPL solar system).
├── objects/            # `Body` class definition and subclasses for planets, moons, etc.
├── simulation/         # Core physics engine, ephemeris integration, and scaling utilities.
├── ui/                 # UI components: client-side canvas, HUD logic, and control handlers.
├── requirements.txt    # Project dependencies.
└── README.md           # This file.
```

---

## 📦 Dependencies

- **`skyfield`**: For real planet positions.
- **`pygame`**: For off-screen rendering of the simulation.
- **`panel`**: For building the web interface and serving the application.
- **`numpy` & `math`**: For numerical operations, particularly in converting Pygame surfaces.

---

## 📕 Resources

[Planetary Data from NASA](https://nssdc.gsfc.nasa.gov/planetary/factsheet/)

---

## 📗 Contributing

Pull requests, bug reports, and feature requests are welcome!

---

## 📘 License

This project is open source and available under the MIT License. You may modify, distribute, and use it freely in your own projects.