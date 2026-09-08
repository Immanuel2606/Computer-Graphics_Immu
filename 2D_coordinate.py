import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Original square
P = np.array([
    [0, 0],
    [2, 0],
    [2, 2],
    [0, 2],
    [0, 0]
])

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.38)

# Original shape
ax.plot(P[:, 0], P[:, 1], '--', label="Original")

# Transformed shape
line, = ax.plot(P[:, 0], P[:, 1], 'o-', label="Transformed")

# Sliders
ax_tx = plt.axes([0.2, 0.28, 0.6, 0.03])
ax_ty = plt.axes([0.2, 0.23, 0.6, 0.03])
ax_r  = plt.axes([0.2, 0.18, 0.6, 0.03])
ax_s  = plt.axes([0.2, 0.13, 0.6, 0.03])
ax_sh = plt.axes([0.2, 0.08, 0.6, 0.03])

tx = Slider(ax_tx, "Move X", -5, 5, valinit=0)
ty = Slider(ax_ty, "Move Y", -5, 5, valinit=0)
r  = Slider(ax_r,  "Rotate", -180, 180, valinit=0)
s  = Slider(ax_s,  "Scale", 0.5, 3, valinit=1)
sh = Slider(ax_sh, "Shear", -2, 2, valinit=0)

# Transformation
def update(val):

    angle = np.radians(r.val)

    # Scaling matrix
    S = np.array([
        [s.val, 0],
        [0, s.val]
    ])

    # Rotation matrix
    R = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)]
    ])

    # Shearing matrix
    H = np.array([
        [1, sh.val],
        [0, 1]
    ])

    # Apply matrices
    Q = P @ S.T
    Q = Q @ R.T
    Q = Q @ H.T

    # Translation
    Q[:, 0] += tx.val
    Q[:, 1] += ty.val

    line.set_data(Q[:, 0], Q[:, 1])

    fig.canvas.draw_idle()

# Connect sliders
tx.on_changed(update)
ty.on_changed(update)
r.on_changed(update)
s.on_changed(update)
sh.on_changed(update)

# Graph
ax.axhline(0, color="black")
ax.axvline(0, color="black")
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
ax.set_aspect("equal")
ax.grid()

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Interactive 2D Coordinate Transformation")
ax.legend()

plt.show()