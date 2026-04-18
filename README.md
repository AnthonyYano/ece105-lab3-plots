<!-- Sections: Overview, Installation, Usage, Output files, Files of interest, AI tools used and disclosure -->

# Lab 3 — Synthetic Sensor Plots

## Overview

This repository generates reproducible synthetic temperature readings for two sensors and creates publication-quality plots: a scatter plot (readings vs time), an overlaid histogram, and a box plot. The main script is `generate_plots.py` which exposes `generate_data(seed)` and a `main()` entry point.

## Installation

1. Activate the course environment:

   ```bash
   conda activate ece105
   ```

2. Install required packages (choose one):

   - Using conda:
     ```bash
     conda install -c conda-forge numpy matplotlib
     ```

   - Using mamba (recommended for speed):
     ```bash
     mamba install -c conda-forge numpy matplotlib
     ```

## Usage

To generate the plots and save the combined figure, run:

```bash
python generate_plots.py
```

This runs `main()` with the default seed (2143) and writes `sensor_analysis.png` in the current directory. The module functions `generate_data`, `plot_scatter`, and `main` can also be imported for programmatic use.

## Output files

- `sensor_analysis.png` — Combined 1x3 figure (scatter, histogram, box plot) saved at 150 DPI by default.

Backups of the notebook file (e.g., `lab3_sensor_plots.ipynb.bak*`) may also be present.

## Files of interest

- `generate_plots.py` — Contains `generate_data(seed)`, `plot_scatter(ax, ...)`, and `main()` to create and save figures.
- `lab3_sensor_plots.ipynb` — Original notebook used for development and exploration.

## AI tools used and disclosure

(Placeholder) Describe which AI tools were used, what assistance they provided, and what review/verification steps you performed.

---

If you want the script to support CLI arguments (output path, seed, DPI) or additional formats (PDF/SVG), I can add an argparse interface.
