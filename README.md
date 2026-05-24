# Solar System Simulation Web
<p align="left">
    <a href="https://www.python.org/" target="_blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
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

- **Interactive Simulation Controls:** Play, pause, and advance the simulation frame-by-frame.
- **Multiple Simulation Views:** Easily switch between different scenarios, such as the full solar system or a simple Sun-Earth system.
- **Web App built using Panel:** The entire user interface is built with the powerful and flexible Panel library.
- **Off-Screen Pygame Rendering:** Utilizes Pygame for high-performance, off-screen rendering of the simulation, served through the Panel web interface.

---

## ⚙️ Project Architecture

```yaml
solar-system-simulation-web/
│
├── app.py                  # Main application entry point. Initializes Panel UI, state, and callbacks.
├── constants.py            # Central file for simulation constants (physics, colors, scaling).
├── modules/                # Simulation presets and helper generators
│   ├── simple_solar_system.py 
│   ├── simple_sun_and_earth.py 
│   ├── simple_sun_earth_moon.py 
│   └── simple_earth_moon.py 
├── objects/                # Runtime body definitions and presets
│   ├── base.py             
│   ├── planet.py           
│   ├── moon.py             
│   ├── asteroid.py         
│   └── presets/            
├── ui/                     # UI components and rendering helpers
│   ├── css.py
│   ├── hud.py
│   ├── screen.py
│   └── ui_handlers.py
├── simulation/             # Core simulation engine and scaling utilities
│   ├── solarsystem_sim.py
│   └── solarsystem_scale.py
├── requirements.txt
└── README.md
```

---

## 📦 Dependencies

- **`pygame`**: For off-screen rendering of the simulation.
- **`panel`**: For building the web interface and serving the application.
- **`numpy` & `math`**: For numerical operations, particularly in converting Pygame surfaces.
- **`Pillow`**: For image processing and handling the PNG conversion.

---

## 📕 Resources

[Planetary Data from NASA](https://nssdc.gsfc.nasa.gov/planetary/factsheet/)

---

## 📗 Contributing

Pull requests, bug reports, and feature requests are welcome!

---

## 📘 License

This project is open source and available under the MIT License. You may modify, distribute, and use it freely in your own projects.