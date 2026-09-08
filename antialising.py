import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(14, 6))

# =================================================
# LEFT: SUTHERLAND-HODGMAN
# =================================================
ax1 = plt.subplot(1, 2, 1)

# Original polygon
polygon = np.array([
    [1, 6],
    [3, 7.5],
    [3.5, 5.5],
    [7, 4],
    [5, 2],
    [2.5, 1.2],
    [2.5, 3.2]
])

# Clipping window
xmin, ymin = 2.5, 2.0
xmax, ymax = 7, 6

# Original polygon
ax1.fill(
    polygon[:, 0],
    polygon[:, 1],
    color='salmon',
    alpha=0.75
)

ax1.plot(
    np.r_[polygon[:, 0], polygon[0, 0]],
    np.r_[polygon[:, 1], polygon[0, 1]],
    color='black',
    linewidth=2
)

# Vertices
ax1.plot(
    polygon[:, 0],
    polygon[:, 1],
    'o',
    color='black',
    markersize=8
)

# Clipping rectangle
ax1.plot(
    [xmin, xmax, xmax, xmin, xmin],
    [ymin, ymin, ymax, ymax, ymin],
    color='royalblue',
    linestyle='--',
    linewidth=2
)

# Approximate clipped polygon
clipped = np.array([
    [3, 6],
    [3.5, 5.5],
    [7, 4],
    [5, 2],
    [2.5, 2],
    [2.5, 3.2]
])

ax1.set_title("Sutherland-Hodgman Polygon Clipping",
              fontsize=16,
              color='royalblue',
              fontweight='bold')

ax1.text(3.8, 0.8,
         "Original Polygon",
         fontsize=13,
         fontweight='bold',
         ha='center')

# Arrow
ax1.annotate(
    '',
    xy=(8.5, 4.5),
    xytext=(7.5, 4.5),
    arrowprops=dict(
        arrowstyle='->',
        linewidth=3
    )
)

# =================================================
# Right side of left panel: clipped polygon
# =================================================

# Use inset-like coordinates by plotting shifted version
clipped_shifted = clipped.copy()
clipped_shifted[:, 0] = (
    clipped_shifted[:, 0] - 2.5
) * 0.55 + 8.5

clipped_shifted[:, 1] = (
    clipped_shifted[:, 1] - 1.5
) * 0.75 + 2

ax1.fill(
    clipped_shifted[:, 0],
    clipped_shifted[:, 1],
    color='lightgreen',
    alpha=0.8
)

ax1.plot(
    np.r_[clipped_shifted[:, 0],
          clipped_shifted[0, 0]],
    np.r_[clipped_shifted[:, 1],
          clipped_shifted[0, 1]],
    color='black',
    linewidth=2
)

ax1.plot(
    clipped_shifted[:, 0],
    clipped_shifted[:, 1],
    'o',
    color='green',
    markersize=8
)

# Small clipping window
cx1, cy1 = 8.2, 2.0
cx2, cy2 = 10.3, 6

ax1.plot(
    [cx1, cx2, cx2, cx1, cx1],
    [cy1, cy1, cy2, cy2, cy1],
    color='royalblue',
    linestyle='--',
    linewidth=2
)

ax1.text(9.2, 0.8,
         "Clipped Polygon",
         fontsize=13,
         fontweight='bold',
         ha='center')

ax1.set_xlim(0, 11)
ax1.set_ylim(0, 8.5)
ax1.axis('off')


# =================================================
# RIGHT: ANTIALIASING
# =================================================
ax2 = plt.subplot(1, 2, 2)

# Pixel grid
n = 14

# Without antialiasing
for i in range(n):
    for j in range(n):

        if abs(i - j) <= 1:
            ax2.add_patch(
                plt.Rectangle(
                    (i, j),
                    1, 1,
                    facecolor='black'
                )
            )

        ax2.add_patch(
            plt.Rectangle(
                (i, j),
                1, 1,
                fill=False,
                edgecolor='gray',
                linewidth=0.7
            )
        )

ax2.text(
    7, -1,
    "Without Antialiasing",
    ha='center',
    fontsize=13,
    fontweight='bold'
)

# Second image
for i in range(n):
    for j in range(n):

        # Distance from diagonal
        distance = abs(i - j)

        if distance == 0:
            intensity = 1.0
        elif distance == 1:
            intensity = 0.45
        else:
            intensity = 0

        if intensity > 0:
            ax2.add_patch(
                plt.Rectangle(
                    (i + 16, j),
                    1, 1,
                    facecolor=str(1 - intensity),
                    edgecolor='gray'
                )
            )

        else:
            ax2.add_patch(
                plt.Rectangle(
                    (i + 16, j),
                    1, 1,
                    fill=False,
                    edgecolor='gray',
                    linewidth=0.7
                )
            )

ax2.text(
    23, -1,
    "With Antialiasing",
    ha='center',
    fontsize=13,
    fontweight='bold'
)

ax2.set_xlim(0, 30)
ax2.set_ylim(-2, 15)
ax2.set_aspect('equal')
ax2.axis('off')

ax2.set_title(
    "Antialiasing (Boundary Smoothing)",
    fontsize=16,
    color='green',
    fontweight='bold'
)

plt.tight_layout()
plt.show()