"""
TECH LOGO GENERATOR
--------------------
Creates a creative, technology-themed logo using only 5 basic shapes:
    -> Line       (circuit traces)
    -> Circle     (core / connection nodes)
    -> Ellipse    (orbit ring)
    -> Rectangle  (chip body + pins)
    -> Triangle   (power / play emblem)

Run this file in VS Code (Run Python File) — it will pop up the logo
and also save it as 'tech_logo.png' next to this script.

Requirements:
    pip install matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, Polygon, FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np

# ----------------------------------------------------------------------
# 1. CANVAS SETUP
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor("#0b0f19")     # near-black background
ax.set_facecolor("#0b0f19")
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_aspect("equal")
ax.axis("off")

# Color palette
NEON_CYAN   = "#00e5ff"
NEON_BLUE   = "#2979ff"
NEON_PURPLE = "#b388ff"
WHITE_GLOW  = "#e8f9ff"
DARK_CHIP   = "#111827"

# ----------------------------------------------------------------------
# 2. SOFT GLOW BACKDROP (stacked translucent circles = glow effect)
# ----------------------------------------------------------------------
for r, a in [(6.6, 0.05), (5.6, 0.07), (4.6, 0.09)]:
    glow = Circle((0, 0), r, color=NEON_CYAN, alpha=a, zorder=1)
    ax.add_patch(glow)

# ----------------------------------------------------------------------
# 3. ORBIT ELLIPSES (tilted rings, like electron / data orbits)
# ----------------------------------------------------------------------
for angle, color, alpha in [(35, NEON_CYAN, 0.9), (-35, NEON_PURPLE, 0.6)]:
    orbit = Ellipse((0, 0), width=9.6, height=4.0, angle=angle,
                     facecolor="none", edgecolor=color,
                     linewidth=1.8, alpha=alpha, zorder=3)
    ax.add_patch(orbit)

    # a small "electron" node riding on each orbit
    rad = np.radians(angle)
    ex, ey = 4.8 * np.cos(rad), 2.0 * np.sin(rad)
    node = Circle((ex, ey), 0.28, color=color, zorder=6,
                   path_effects=None)
    ax.add_patch(node)

# ----------------------------------------------------------------------
# 4. CIRCUIT LINES + NODES (radiating outward like chip pins/traces)
# ----------------------------------------------------------------------
circuit_angles = [20, 70, 110, 160, 200, 250, 290, 340]
for ang in circuit_angles:
    rad = np.radians(ang)
    x1, y1 = 3.3 * np.cos(rad), 3.3 * np.sin(rad)
    x2, y2 = 6.6 * np.cos(rad), 6.6 * np.sin(rad)

    # elbowed circuit-board style trace (two segments, 90-degree feel)
    xm, ym = x1 + (x2 - x1) * 0.55, y1 + (y2 - y1) * 0.15
    line1 = Line2D([x1, xm], [y1, y1], color=NEON_CYAN, linewidth=2.0,
                    alpha=0.85, zorder=4, solid_capstyle="round")
    line2 = Line2D([xm, x2], [y1, y2], color=NEON_CYAN, linewidth=2.0,
                    alpha=0.85, zorder=4, solid_capstyle="round")
    ax.add_line(line1)
    ax.add_line(line2)

    # connector pad (small square) at the tip
    pad = Rectangle((x2 - 0.22, y2 - 0.22), 0.44, 0.44,
                     facecolor=NEON_CYAN, edgecolor=WHITE_GLOW,
                     linewidth=0.6, zorder=5)
    ax.add_patch(pad)

# ----------------------------------------------------------------------
# 5. CENTRAL CHIP BODY (rounded rectangle "die")
# ----------------------------------------------------------------------
chip = FancyBboxPatch((-3.0, -3.0), 6.0, 6.0,
                       boxstyle="round,pad=0.02,rounding_size=0.6",
                       facecolor=DARK_CHIP, edgecolor=NEON_CYAN,
                       linewidth=2.4, zorder=7)
ax.add_patch(chip)

# inner accent rectangle (thin frame)
inner = FancyBboxPatch((-2.4, -2.4), 4.8, 4.8,
                        boxstyle="round,pad=0.02,rounding_size=0.4",
                        facecolor="none", edgecolor=NEON_BLUE,
                        linewidth=1.0, alpha=0.7, zorder=8)
ax.add_patch(inner)

# ----------------------------------------------------------------------
# 6. CORE CIRCLE (glowing processor core)
# ----------------------------------------------------------------------
core_outer = Circle((0, 0), 1.65, facecolor="#0d1b2a",
                     edgecolor=NEON_CYAN, linewidth=2.2, zorder=9)
core_glow  = Circle((0, 0), 1.9, facecolor=NEON_CYAN, alpha=0.12, zorder=8.5)
ax.add_patch(core_glow)
ax.add_patch(core_outer)

# ----------------------------------------------------------------------
# 7. TRIANGLE (power / play emblem inside the core)
# ----------------------------------------------------------------------
tri_pts = [(-0.55, 0.95), (-0.55, -0.95), (1.05, 0.0)]
triangle = Polygon(tri_pts, closed=True, facecolor=WHITE_GLOW,
                    edgecolor=NEON_CYAN, linewidth=1.2, zorder=10)
ax.add_patch(triangle)

# ----------------------------------------------------------------------
# 8. WORDMARK
# ----------------------------------------------------------------------
ax.text(0, -8.6, "N E X U S", color=WHITE_GLOW, fontsize=26,
         ha="center", va="center", fontweight="bold",
         family="monospace", zorder=11)
ax.text(0, -9.4, "T E C H N O L O G I E S", color=NEON_CYAN, fontsize=10.5,
         ha="center", va="center", family="monospace",
         alpha=0.85, zorder=11)

# ----------------------------------------------------------------------
# 9. SAVE + SHOW
# ----------------------------------------------------------------------
plt.tight_layout()
plt.savefig("tech_logo.png", dpi=300, facecolor=fig.get_facecolor(),
            bbox_inches="tight", pad_inches=0.3)
print("Saved logo as tech_logo.png")
plt.show()
