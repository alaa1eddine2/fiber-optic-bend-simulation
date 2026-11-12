# fiber_bend_simulation.py
# Interactive simulation of bend-induced loss in optical fiber
# Based on empirical model: L_R = 70 * exp(-0.5 * R) [dB/turn] at λ=1550 nm
# Material scaling uses numerical aperture (NA) from paper's equation (4)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from matplotlib.animation import FuncAnimation

# ----------------------------
# Constants from the paper
# ----------------------------
ETA_R1 = 70.0  # dB/turn coefficient
ETA_R2 = 0.5   # 1/mm (for reference fiber)

# Material presets (n1, n2)
MATERIAL_PRESETS = {
    "Standard SMF": (1.48, 1.46),
    "High NA Fiber": (1.50, 1.46),
    "Plastic Fiber": (1.49, 1.40),
}

def compute_NA(n1, n2):
    return np.sqrt(n1**2 - n2**2)

REF_NA = compute_NA(*MATERIAL_PRESETS["Standard SMF"])  # ~0.242

# Visual scaling (not physical)
VIS_CORE_RADIUS = 6.0
VIS_CLAD_RADIUS = 18.0

# ----------------------------
# Helper functions
# ----------------------------
def loss_to_escape_probability(loss_db):
    if loss_db <= 0:
        return 0.0
    transmitted = 10 ** (-loss_db / 10.0)
    return max(0.0, min(1.0, 1.0 - transmitted))

def calculate_data_transfer(loss_db):
    return 100.0 * (1.0 - loss_to_escape_probability(loss_db))

def calculate_loss(radius_mm, n1, n2):
    na = compute_NA(n1, n2)
    scaling = (REF_NA / na) ** 2
    exponent = -ETA_R2 * scaling * radius_mm
    return ETA_R1 * np.exp(exponent)

# ----------------------------
# Main App Class
# ----------------------------
class FiberBendSimulator:
    def __init__(self):
        self.radius_mm = 8.0
        self.speed_factor = 1.0
        self.material_key = "Standard SMF"
        self.is_paused = True
        self.time_phase = 0.0
        self.pulses = []          # (creation_time, escaped, distance)
        self.historical_data = []
        self.bend_center = (0, 0)

        # Setup figure
        self.fig = plt.figure(figsize=(12, 6.5))
        self.fig.suptitle("Fiber-Optic Bend Simulation", fontsize=16, fontweight='bold')

        # Left panel: graph
        self.ax_graph = plt.axes([0.05, 0.35, 0.35, 0.55])
        self.ax_graph.set_title("Data Transfer vs. Bend Radius", fontsize=12)
        self.ax_graph.set_xlim(4, 15)
        self.ax_graph.set_ylim(0, 100)
        self.ax_graph.set_xlabel("Bend Radius (mm)")
        self.ax_graph.set_ylabel("Data Transfer (%)")
        self.ax_graph.grid(True, linestyle='--', alpha=0.3)
        self.ax_graph.plot([4, 15], [100, 100], 'k--', alpha=0.3)
        self.ax_graph.plot([4, 15], [0, 0], 'k--', alpha=0.3)

        self.historical_line, = self.ax_graph.plot([], [], 'b-', linewidth=2)
        self.data_points, = self.ax_graph.plot([], [], 'bo', markersize=8)

        # Right panel: animation
        self.ax_animation = plt.axes([0.45, 0.35, 0.5, 0.55])
        self.ax_animation.set_title("Light Propagation & Loss", fontsize=12)
        self.ax_animation.set_xlim(-150, 150)
        self.ax_animation.set_ylim(-50, 150)
        self.ax_animation.set_aspect('equal')
        self.ax_animation.axis('off')
        self.ax_animation.patch.set_facecolor('none')

        # Controls
        self.ax_radius = plt.axes([0.2, 0.25, 0.3, 0.03])
        self.ax_speed = plt.axes([0.2, 0.20, 0.3, 0.03])
        self.ax_material = plt.axes([0.6, 0.20, 0.25, 0.12])
        self.ax_start_stop = plt.axes([0.88, 0.25, 0.1, 0.04])

        self.slider_radius = Slider(self.ax_radius, 'Bend Radius (mm)', 4.0, 15.0, valinit=self.radius_mm, valstep=0.1)
        self.slider_speed = Slider(self.ax_speed, 'Speed', 0.2, 3.0, valinit=self.speed_factor, valstep=0.1)
        self.radio_material = RadioButtons(self.ax_material, list(MATERIAL_PRESETS.keys()), active=0)
        self.button_toggle = Button(self.ax_start_stop, 'Start')

        self.slider_radius.on_changed(self.update_radius)
        self.slider_speed.on_changed(self.update_speed)
        self.radio_material.on_clicked(self.update_material)
        self.button_toggle.on_clicked(self.toggle_animation)

        self.draw_cable()
        self.update_data_graph()

        self.animation = FuncAnimation(self.fig, self.animate, interval=50, blit=False, cache_frame_data=False)

    def update_radius(self, val):
        self.radius_mm = float(val)
        self.update_data_graph()
        self.draw_cable()

    def update_speed(self, val):
        self.speed_factor = float(val)

    def update_material(self, label):
        self.material_key = label
        self.historical_data.clear()
        self.update_data_graph()
        self.draw_cable()

    def toggle_animation(self, _):
        self.is_paused = not self.is_paused
        self.button_toggle.label.set_text('Pause' if not self.is_paused else 'Start')
        plt.draw()

    def update_data_graph(self):
        n1, n2 = MATERIAL_PRESETS[self.material_key]
        loss_db = calculate_loss(self.radius_mm, n1, n2)
        data_transfer = calculate_data_transfer(loss_db)

        exists = any(abs(r - self.radius_mm) < 0.2 and abs(t - data_transfer) < 0.5
                     for r, t in self.historical_data)
        if not exists:
            self.historical_data.append((self.radius_mm, data_transfer))
            self.historical_data.sort(key=lambda x: x[0])

        radii, transfers = zip(*self.historical_data) if self.historical_data else ([], [])
        self.data_points.set_data(radii, transfers)
        self.historical_line.set_data(radii, transfers)

        self.ax_graph.set_title(
            f"Data Transfer vs. Bend Radius | R = {self.radius_mm:.1f} mm | Transfer: {data_transfer:.1f}%",
            fontsize=12
        )

    def draw_cable(self):
        self.ax_animation.clear()
        self.ax_animation.set_title("Light Propagation & Loss", fontsize=12)
        self.ax_animation.set_xlim(-150, 150)
        self.ax_animation.set_ylim(-50, 150)
        self.ax_animation.set_aspect('equal')
        self.ax_animation.axis('off')
        self.ax_animation.patch.set_facecolor('none')

        vis_radius = self.radius_mm * 5.0
        center_x = -vis_radius
        center_y = 50 + vis_radius
        self.bend_center = (center_x, center_y)
        self.horizontal_end_x = -vis_radius
        self.vertical_start_y = 50 + vis_radius

        # Straight segments
        self.ax_animation.plot([-120, self.horizontal_end_x], [50, 50], 'k-', linewidth=2.5, zorder=1)
        self.ax_animation.plot([0, 0], [self.vertical_start_y, 130], 'k-', linewidth=2.5, zorder=1)

        # Quarter circle
        theta = np.linspace(-np.pi/2, 0, 100)
        x_arc = center_x + vis_radius * np.cos(theta)
        y_arc = center_y + vis_radius * np.sin(theta)
        self.ax_animation.plot(x_arc, y_arc, 'k-', linewidth=2.5, zorder=1)

        # Core/cladding visuals (thick)
        # Horizontal
        self.ax_animation.plot([-120, self.horizontal_end_x], [50, 50], 'b-', linewidth=8, alpha=0.6, zorder=1)
        self.ax_animation.plot([-120, self.horizontal_end_x], [50, 50], 'c-', linewidth=5, alpha=0.9, zorder=2)

        # Curved
        inner_radius = vis_radius - VIS_CORE_RADIUS
        x_core = center_x + inner_radius * np.cos(theta)
        y_core = center_y + inner_radius * np.sin(theta)
        inner_clad = vis_radius - VIS_CLAD_RADIUS
        x_clad = center_x + inner_clad * np.cos(theta)
        y_clad = center_y + inner_clad * np.sin(theta)
        self.ax_animation.plot(x_clad, y_clad, 'b-', linewidth=8, alpha=0.6, zorder=1)
        self.ax_animation.plot(x_core, y_core, 'c-', linewidth=5, alpha=0.9, zorder=2)

        # Vertical
        self.ax_animation.plot([0, 0], [self.vertical_start_y, 130], 'b-', linewidth=8, alpha=0.6, zorder=1)
        self.ax_animation.plot([0, 0], [self.vertical_start_y, 130], 'c-', linewidth=5, alpha=0.9, zorder=2)

        # Radius label
        self.ax_animation.plot([center_x, 0], [center_y, 50], 'k-', linewidth=1, alpha=0.7)
        self.ax_animation.plot([-2, 2], [50, 50], 'k-', linewidth=1)
        self.ax_animation.text(0, 50 + 8, f"R = {self.radius_mm:.1f} mm",
                               fontsize=10, ha='center',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        self.ax_animation.plot(center_x, center_y, 'ko', markersize=5, zorder=2)
        self.ax_animation.text(center_x + 8, center_y - 5, "Bend Center", fontsize=9, style='italic')

    def animate(self, _):
        if self.is_paused:
            return

        for collection in self.ax_animation.collections[:]:
            collection.remove()

        n1, n2 = MATERIAL_PRESETS[self.material_key]
        loss_db = calculate_loss(self.radius_mm, n1, n2)
        escape_prob = loss_to_escape_probability(loss_db)

        vis_radius = self.radius_mm * 5.0
        center_x = -vis_radius
        center_y = 50 + vis_radius

        # Path lengths
        horiz_len = self.horizontal_end_x - (-120)   # = 120 - vis_radius
        arc_len = 0.5 * np.pi * vis_radius
        vert_len = 130 - self.vertical_start_y
        total_len = horiz_len + arc_len + vert_len

        linear_speed = 2.5 * self.speed_factor   # per frame

        # Add new pulse
        if not self.pulses or (self.time_phase - self.pulses[-1][0]) > 0.45:
            if len(self.pulses) < 25:
                escaped = np.random.rand() < escape_prob
                self.pulses.append((self.time_phase, escaped, 0.0))   # distance starts at 0

        new_pulses = []
        for t0, escaped, dist in self.pulses:
            dist += linear_speed
            if dist > total_len:
                continue   # pulse exits

            # Determine position
            if dist < horiz_len:
                x = -120 + dist
                y = 50
                segment = 'horizontal'
            elif dist < horiz_len + arc_len:
                arc_dist = dist - horiz_len
                angle = -np.pi/2 + (arc_dist / vis_radius)
                x = center_x + vis_radius * np.cos(angle)
                y = center_y + vis_radius * np.sin(angle)
                segment = 'bend'
            else:
                vert_dist = dist - (horiz_len + arc_len)
                x = 0
                y = self.vertical_start_y + vert_dist
                segment = 'vertical'

            new_pulses.append((t0, escaped, dist))

            # Draw
            if escaped:
                if segment == 'bend':
                    dx = x - center_x
                    dy = y - center_y
                    norm = np.hypot(dx, dy) + 1e-5
                    drift_x = x + (dx / norm) * np.random.uniform(8, 15)
                    drift_y = y + (dy / norm) * np.random.uniform(8, 15)
                elif segment == 'horizontal':
                    drift_x = x + np.random.uniform(-3, 8)
                    drift_y = y + np.random.uniform(5, 12)
                else:  # vertical
                    drift_x = x + np.random.uniform(5, 12)
                    drift_y = y + np.random.uniform(-3, 8)
                self.ax_animation.scatter([drift_x], [drift_y], c='#FF0000', s=40,
                                          edgecolor='#8B0000', zorder=5, alpha=0.85, marker='o')
            else:
                self.ax_animation.scatter([x], [y], c='#00FFFF', s=30,
                                          edgecolor='white', zorder=4, alpha=0.95)

        self.pulses = new_pulses
        self.time_phase += 0.05

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    sim = FiberBendSimulator()
    plt.show()