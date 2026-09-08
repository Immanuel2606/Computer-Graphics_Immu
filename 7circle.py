import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Center and radius
hc, kc = 0, 0
r = 2
R = 2
n = 6

# 8 colors
colors = [
    "red", "orange", "yellow", "green",
    "cyan", "blue", "purple", "pink"
]

fig, ax = plt.subplots()

# Center circle
ax.add_patch(Circle(
    (hc, kc), r,
    facecolor=colors[0],
    alpha=0.45
))

# Six surrounding circles
for i in range(n):

    theta = 2 * np.pi * i / n

    # Center of each circle
    hi = hc + R * np.cos(theta)
    ki = kc + R * np.sin(theta)

    ax.add_patch(Circle(
        (hi, ki), r,
        facecolor=colors[i + 1],
        alpha=0.45
    ))

# Draw all circle outlines
theta = np.linspace(0, 2*np.pi, 500)

for i in range(7):

    if i == 0:
        hi, ki = hc, kc
    else:
        angle = 2 * np.pi * (i - 1) / n
        hi = hc + R * np.cos(angle)
        ki = kc + R * np.sin(angle)

    x = hi + r * np.cos(theta)
    y = ki + r * np.sin(theta)

    ax.plot(x, y, "black", linewidth=2)

# Settings
ax.set_aspect("equal")
ax.axis("off")

plt.title("7-Circle Flower Pattern with 8 Colors")
plt.show()