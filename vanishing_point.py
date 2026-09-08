import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# Sliders
ax_x = plt.axes([0.2, 0.12, 0.6, 0.03])
ax_y = plt.axes([0.2, 0.07, 0.6, 0.03])

sx = Slider(ax_x, "Vanishing X", -10, 10, valinit=0)
sy = Slider(ax_y, "Vanishing Y", 2, 8, valinit=5)

def draw(val=None):
    ax.clear()

    vx = sx.val
    vy = sy.val

    # Vanishing point
    ax.plot(vx, vy, 'ro', markersize=8, label="Vanishing Point")

    # Ground perspective lines
    bottom_x = np.linspace(-10, 10, 9)

    for x in bottom_x:
        ax.plot([vx, x], [vy, -10], 'b-')

    # Horizontal road lines
    for y in [-8, -6, -4, -2, 0]:
        ax.plot([-10, 10], [y, y], 'k-')

    # Road boundaries
    ax.plot([vx, -8], [vy, -10], 'r-', linewidth=2)
    ax.plot([vx, 8], [vy, -10], 'r-', linewidth=2)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    ax.axhline(0, color='gray')
    ax.axvline(0, color='gray')

    ax.grid()
    ax.set_aspect('equal')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Interactive Vanishing Point & Perspective")
    ax.legend()

    fig.canvas.draw_idle()

sx.on_changed(draw)
sy.on_changed(draw)

draw()
plt.show()