import numpy as np
import matplotlib.pyplot as plt

# Original triangle
P = np.array([
    [1, 1, 1],
    [4, 1, 1],
    [2.5, 4, 1]
]).T

# Transformation values
tx, ty = 3, 2
sx, sy = 1.5, 1.5
angle = 30

# Translation matrix
T = np.array([
    [1, 0, tx],
    [0, 1, ty],
    [0, 0, 1]
])

# Scaling matrix
S = np.array([
    [sx, 0, 0],
    [0, sy, 0],
    [0, 0, 1]
])

# Rotation matrix
theta = np.radians(angle)
R = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
    [0, 0, 1]
])

# Apply transformations
translated = T @ P
scaled = S @ P
rotated = R @ P

def draw(ax, points, title, style='-'):
    points = np.hstack((points, points[:, :1]))
    ax.plot(points[0], points[1], style, linewidth=2)
    ax.fill(points[0], points[1], alpha=0.15)
    ax.set_title(title)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True)
    ax.set_aspect('equal')

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

draw(axes[0, 0], P, "Original Triangle")
draw(axes[0, 1], translated, "Translation")
draw(axes[1, 0], scaled, "Scaling")
draw(axes[1, 1], rotated, "Rotation")

plt.suptitle("2D Geometric Transformations", fontsize=16)
plt.tight_layout()
plt.show()