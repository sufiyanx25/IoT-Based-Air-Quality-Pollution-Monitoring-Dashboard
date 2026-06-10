Repository folder explanations

Root layout (GitHub-ready):

- `arduino_code/` — Place Arduino/ESP32 sketches intended for microcontroller deployment. Organize by board (esp32/, arduino_uno/) and include `README` per sketch explaining wiring and dependencies.

- `python_simulation/` — Python scripts and notebooks to simulate sensor data, run AQI calculations, preprocess data, and prototype dashboard backends (Flask, FastAPI). Include `requirements.txt` snippets and example Jupyter notebooks here.

- `dashboard/` — Frontend and backend dashboard code. Example subfolders: `react/`, `flask/`, `node/`. Store dashboard source, dashboard assets, and small demo projects that visualize `data/` outputs.

- `data/` — Collected or simulated CSV/JSON datasets. Use dated filenames and keep raw vs processed data separate (e.g., `raw/` and `processed/`). Do NOT commit large raw datasets to GitHub; include small sample files for demos.

- `outputs/` — Generated artifacts such as exported charts, generated PDFs, and CSV export results used in reports or presentations.

- `images/` — Diagrams, screenshots, and photos used in documentation and the README. Store circuit photos, dashboard screenshots, and sensor images.

- `circuit_diagram/` — Source files for schematics and breadboard layouts (Fritzing, KiCad, or SVG exports). Include `export/` subfolder for PNG/SVG/PDF exports used in reports.

- `reports/` — Final writeups, lab reports, and presentation slides. Store PDF deliverables and grading-friendly documents.

- `docs/` — Project documentation, explanations, and guides. This file (`FOLDER_STRUCTURE.md`) lives here. Use `docs/` for step-by-step tutorials and assembly instructions.

- `README.md` — High-level project description and quick start.

- `requirements.txt` — Python dependencies for simulation and dashboard prototypes.

- `.gitignore` — Ignore common build artifacts, virtualenvs, PlatformIO cache, and large data folders.

- `main.py` — Small runner to start local simulations or launch a minimal dashboard demo.

Usage tips
- Keep hardware-specific code in `arduino_code/` and keep a clear `README` for wiring and sensor calibration.
- Keep `data/` small in the repo; provide scripts in `python_simulation/` to regenerate sample data.
- Export final diagrams into `images/` and `circuit_diagram/export/` for use in reports.
