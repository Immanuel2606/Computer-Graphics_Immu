import numpy as np
import matplotlib.pyplot as plt

# Original polygon
P = np.array([
    [1, 1, 1],
    [4, 1, 1],
    [4, 3, 1],
    [2, 4, 1],
    [1, 3, 1]
]).T

# Reflection about X-axis
Rx = np.array([
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, 1]
])

# Reflection about Y-axis
Ry = np.array([
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

# Shearing along X direction
shx = 1
Sh = np.array([
    [1, shx, 0],
    [0, 1, 0],
    [0, 0, 1]
])

ref_x = Rx @ P
ref_y = Ry @ P
sheared = Sh @ P

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

def plot_polygon(ax, p, title):
    p = np.hstack((p, p[:, :1]))
    ax.plot(p[0], p[1], linewidth=2)
    ax.fill(p[0], p[1], alpha=0.15)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True)
    ax.set_aspect("equal")
    ax.set_title(title)

plot_polygon(axes[0, 0], P, "Original Polygon")
plot_polygon(axes[0, 1], ref_x, "Reflection about X-axis")
plot_polygon(axes[1, 0], ref_y, "Reflection about Y-axis")
plot_polygon(axes[1, 1], sheared, "X-Shearing")

plt.suptitle("Reflection and Shearing Transformations", fontsize=16)
plt.tight_layout()
plt.show()