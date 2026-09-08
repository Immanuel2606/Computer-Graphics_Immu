import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(14, 6))

# -------------------------------------------------
# LEFT: FLOOD FILL
# -------------------------------------------------
ax1 = plt.subplot(1, 2, 1)

polygon = np.array([
    [2, 1],
    [1, 5],
    [4, 8],
    [8, 5],
    [7, 2]
])

# Polygon boundary
ax1.fill(polygon[:, 0], polygon[:, 1],
         color='lightskyblue', alpha=0.35)

ax1.plot(
    np.r_[polygon[:, 0], polygon[0, 0]],
    np.r_[polygon[:, 1], polygon[0, 1]],
    'k-', linewidth=3
)

# Dotted pixel grid
for x in range(0, 10):
    for y in range(0, 9):
        ax1.plot(x, y, 'o', markersize=6,
                 markerfacecolor='none',
                 markeredgecolor='gray',
                 alpha=0.7)

# Seed point
seed_x, seed_y = 4, 4
ax1.plot(seed_x, seed_y, 'o',
         color='royalblue', markersize=12)

# Four-direction arrows
ax1.arrow(seed_x, seed_y, 0, 1.4,
          head_width=0.25, color='royalblue',
          length_includes_head=True)

ax1.arrow(seed_x, seed_y, 0, -1.4,
          head_width=0.25, color='royalblue',
          length_includes_head=True)

ax1.arrow(seed_x, seed_y, 1.4, 0,
          head_width=0.25, color='royalblue',
          length_includes_head=True)

ax1.arrow(seed_x, seed_y, -1.4, 0,
          head_width=0.25, color='royalblue',
          length_includes_head=True)

ax1.set_title("Flood Fill (Seed Fill)",
              fontsize=18, color='royalblue',
              fontweight='bold')

ax1.text(4, -0.3,
         "Fills connected region from a seed point\n"
         "until the boundary is reached.",
         ha='center', fontsize=12, fontweight='bold')

ax1.set_xlim(-0.5, 9.5)
ax1.set_ylim(-1.5, 9)
ax1.axis('off')


# -------------------------------------------------
# RIGHT: SCAN-LINE FILL
# -------------------------------------------------
ax2 = plt.subplot(1, 2, 2)

ax2.fill(polygon[:, 0], polygon[:, 1],
         color='lightgreen', alpha=0.25)

ax2.plot(
    np.r_[polygon[:, 0], polygon[0, 0]],
    np.r_[polygon[:, 1], polygon[0, 1]],
    'k-', linewidth=3
)

# Scan lines
for y in np.arange(2.0, 7.1, 0.8):

    intersections = []

    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]

        if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
            x = p1[0] + (y - p1[1]) * \
                (p2[0] - p1[0]) / (p2[1] - p1[1])
            intersections.append(x)

    intersections.sort()

    if len(intersections) >= 2:
        x1, x2 = intersections[0], intersections[-1]

        ax2.plot([x1, x2], [y, y],
                 color='green', linewidth=3)

        ax2.plot([x1, x2], [y, y],
                 'o', color='green', markersize=8)

        ax2.arrow(x2, y, 1.3, 0,
                  head_width=0.22,
                  head_length=0.3,
                  color='green',
                  length_includes_head=True)

ax2.set_title("Scan-Line Fill",
              fontsize=18, color='green',
              fontweight='bold')

ax2.text(4.5, -0.3,
         "Fills span between intersection points\n"
         "for each scan line.",
         ha='center', fontsize=12, fontweight='bold')

ax2.set_xlim(-0.5, 10)
ax2.set_ylim(-1.5, 9)
ax2.axis('off')

plt.tight_layout()
plt.show()