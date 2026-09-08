import numpy as np
import matplotlib.pyplot as plt

# Object
P = np.array([
    [1, 1, 1],
    [3, 1, 1],
    [3, 3, 1],
    [1, 3, 1]
]).T

# Matrices
T = np.array([
    [1, 0, 4],
    [0, 1, 2],
    [0, 0, 1]
])

S = np.array([
    [1.5, 0, 0],
    [0, 1.5, 0],
    [0, 0, 1]
])

angle = np.radians(45)

R = np.array([
    [np.cos(angle), -np.sin(angle), 0],
    [np.sin(angle),  np.cos(angle), 0],
    [0, 0, 1]
])

# Order 1: Scale -> Rotate -> Translate
M1 = T @ R @ S
result1 = M1 @ P

# Order 2: Translate -> Rotate -> Scale
M2 = S @ R @ T
result2 = M2 @ P

def plot(ax, points, title):
    points = np.hstack((points, points[:, :1]))
    ax.plot(points[0], points[1], linewidth=2)
    ax.fill(points[0], points[1], alpha=0.15)
    ax.grid(True)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.set_aspect("equal")
    ax.set_title(title)

fig, ax = plt.subplots(1, 3, figsize=(14, 5))

plot(ax[0], P, "Original")
plot(ax[1], result1, "Scale → Rotate → Translate")
plot(ax[2], result2, "Translate → Rotate → Scale")

plt.suptitle("Composite Transformation and Order Effect")
plt.tight_layout()
plt.show()