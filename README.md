# Solar System Simulation Web

This branch contains an early skeleton version of the web app with the full solar system and basic zoom controls.

## What it includes

- Full solar system view
- Play/Pause simulation
- Step one frame at a time
- Zoom in and zoom out controls
- Pygame rendering inside a Panel web UI

## Run it

Install the Python dependencies used by the app:

```bash
pip install panel pygame pillow numpy
```

Start the app:

```bash
python app.py
```

The app opens a local web UI on port `5000`.

## Notes

This is still a lightweight release branch, kept as an early stable skeleton before later HUD and modular UI work.