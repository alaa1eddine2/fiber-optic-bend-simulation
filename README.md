# Fiber Optic Macro-Bending Loss Simulation

This repository contains an interactive Python simulation and its accompanying research paper, "Fiber_Optics_bend_effect_on_data.pdf". The project demonstrates and quantifies macro-bending power loss in single-mode step-index optical fibers at a 1550nm wavelength.

This project translates an empirical model into a dynamic visual tool for engineers, technicians, and optics students.

## Features
* **Interactive Visualization:** Real-time Matplotlib animation showing light pulses propagating through a fiber bend.
* **Empirical Modeling:** Directly utilizes the curve-fitted formula $LR = 70 \exp(-0.5 R)$ to calculate decibel loss per turn based on the bend radius.
* **Material Scaling:** Allows users to switch between fiber types (Standard SMF, High NA Fiber, Plastic Fiber) to observe how varying the Numerical Aperture (NA) impacts bend sensitivity.
* **Live Data Tracking:** Automatically generates a "Data Transfer vs. Bend Radius" graph as the simulation runs.

## The Physics
The simulation is driven by the relationship between the bend radius ($R$) and the resulting power loss. As the fiber bends, the evanescent field on the outer edge of the curve couples to radiating modes in the cladding, causing light to leak out. Total loss increases linearly with the number of wrapping turns.

## Screenshot from the Script
<img width="1200" height="709" alt="image" src="https://github.com/user-attachments/assets/1cbc4f25-0ce1-4933-89d2-b051277c8aef" />


## Requirements
* Python 3.x
* NumPy
* Matplotlib
* Linux may need python3-tk for the Matplotlib backend.

## Installation & Usage
1. Clone this repository:
   ```bash
   git clone https://github.com/alaa1eddine2/fiber-optic-bend-simulation.git
   ```

2. Install the required dependencies:
   ```
   pip install numpy matplotlib 
   ```
   You may need to use a virtual environment, so please follow https://docs.python.org/3/library/venv.html
   Or simply
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   There is activate for bash/zsh, activate.fish for fish and activate.ps1 for powershell
   
4. Run the simulation:
    ```
    python3 Fiber-Optics-Simulation.py
    ```

## Caution
This repo is meant for education and serve as an example to understand the physics behind fiber-optics data-loss on bend without delving into complex physics and theoretical models like Marcuse's integral equations.
DO NOT use this as a source for production as it may be unreliable.
Wrapping turns aren’t implemented in the python script.
The script has heuristics for implementation purposes.

## Author
TOUATI Alaa Eddine NHSAT-Algiers, Math. & CS (2025/2026)

## LICENCE
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>
