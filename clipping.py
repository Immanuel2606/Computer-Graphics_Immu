import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(14, 6))

# =================================================
# COHEN-SUTHERLAND
# =================================================
ax1 = plt.subplot(1, 2, 1)

xmin, ymin = 3, 2
xmax, ymax = 8, 6

# Clipping window
ax1.plot(
    [xmin, xmax, xmax, xmin, xmin],
    [ymin, ymin, ymax, ymax, ymin],
    'k-', linewidth=2
)

# Dashed extended boundaries
ax1.axhline(ymax, color='gray',
            linestyle='--', alpha=0.6)
ax1.axhline(ymin, color='gray',
            linestyle='--', alpha=0.6)
ax1.axvline(xmin, color='gray',
            linestyle='--', alpha=0.6)
ax1.axvline(xmax, color='gray',
            linestyle='--', alpha=0.6)

# Region codes
ax1.text(1.2, 6.8, '1001', fontsize=13,
         color='royalblue', fontweight='bold')
ax1.text(5, 6.8, '1000', fontsize=13,
         color='royalblue', fontweight='bold')
ax1.text(8.8, 6.8, '1010', fontsize=13,
         color='royalblue', fontweight='bold')

ax1.text(1.2, 4, '0001', fontsize=13,
         color='royalblue', fontweight='bold')
ax1.text(8.8, 4, '0010', fontsize=13,
         color='royalblue', fontweight='bold')

ax1.text(1.2, 1.2, '0101', fontsize=13,
         color='royalblue', fontweight='bold')
ax1.text(5, 1.2, '0100', fontsize=13,
         color='royalblue', fontweight='bold')
ax1.text(8.8, 1.2, '0110', fontsize=13,
         color='royalblue', fontweight='bold')

# Original line
p1 = np.array([2, 3])
p2 = np.array([9, 5.5])

ax1.plot([p1[0], p2[0]],
         [p1[1], p2[1]],
         color='black', linewidth=3)

# Calculate clipping
dx = p2[0] - p1[0]
dy = p2[1] - p1[1]

t1 = (xmin - p1[0]) / dx
t2 = (xmax - p1[0]) / dx

tc1 = (ymin - p1[1]) / dy
tc2 = (ymax - p1[1]) / dy

tmin = max(0, min(t1, t2, tc1, tc2))
tmax = min(1, max(t1, t2, tc1, tc2))

# Better Liang-style parameter intersection
ts = [0, 1]

if dx != 0:
    ts.extend([(xmin - p1[0]) / dx,
               (xmax - p1[0]) / dx])

if dy != 0:
    ts.extend([(ymin - p1[1]) / dy,
               (ymax - p1[1]) / dy])

valid = sorted([t for t in ts if 0 <= t <= 1])

points = []

for t in valid:
    x = p1[0] + t * dx
    y = p1[1] + t * dy

    if xmin <= x <= xmax and ymin <= y <= ymax:
        points.append((x, y))

if len(points) >= 2:
    x1, y1 = points[0]
    x2, y2 = points[-1]

    ax1.plot([x1, x2], [y1, y2],
             color='red', linewidth=4)

    ax1.plot([x1, x2], [y1, y2],
             'o', color='red', markersize=9)

# End points
ax1.plot(p1[0], p1[1], 'o',
         color='black', markersize=9)
ax1.plot(p2[0], p2[1], 'o',
         color='black', markersize=9)

ax1.set_title("Cohen-Sutherland Algorithm",
              fontsize=17,
              color='royalblue',
              fontweight='bold')

ax1.text(5.5, 0.2,
         "— Clipped Portion\n"
         "— Rejected Portion",
         fontsize=12, ha='center',
         fontweight='bold')

ax1.set_xlim(0, 10)
ax1.set_ylim(0, 8)
ax1.axis('off')


# =================================================
# LIANG-BARSKY
# =================================================
ax2 = plt.subplot(1, 2, 2)

ax2.plot(
    [xmin, xmax, xmax, xmin, xmin],
    [ymin, ymin, ymax, ymax, ymin],
    'k-', linewidth=2
)

# Lines
lines = [
    ([1, 6.5], [4, 9]),
    ([1.5, 5.2], [2, 4.2]),
    ([4.8, 8.8], [4.8, 1.3])
]

for start, end in lines:

    x1, y1 = start
    x2, y2 = end

    ax2.plot([x1, x2],
             [y1, y2],
             color='black',
             linewidth=2)

    dx = x2 - x1
    dy = y2 - y1

    ts = [0, 1]

    if dx != 0:
        ts.extend([
            (xmin - x1) / dx,
            (xmax - x1) / dx
        ])

    if dy != 0:
        ts.extend([
            (ymin - y1) / dy,
            (ymax - y1) / dy
        ])

    valid_points = []

    for t in ts:
        if 0 <= t <= 1:
            x = x1 + t * dx
            y = y1 + t * dy

            if xmin <= x <= xmax and ymin <= y <= ymax:
                valid_points.append((x, y))

    if len(valid_points) >= 2:
        valid_points.sort()

        a = valid_points[0]
        b = valid_points[-1]

        ax2.plot(
            [a[0], b[0]],
            [a[1], b[1]],
            color='green',
            linewidth=4
        )

        ax2.plot(
            [a[0], b[0]],
            [a[1], b[1]],
            'o',
            color='green',
            markersize=9
        )

    ax2.plot(x1, y1, 'o',
             color='black', markersize=8)
    ax2.plot(x2, y2, 'o',
             color='black', markersize=8)

ax2.set_title("Liang-Barsky Algorithm",
              fontsize=17,
              color='green',
              fontweight='bold')

ax2.text(5.5, 0.2,
         "— Clipped Portion\n"
         "— Rejected Portion",
         fontsize=12, ha='center',
         fontweight='bold')

ax2.set_xlim(0, 10)
ax2.set_ylim(0, 8)
ax2.axis('off')

plt.tight_layout()
plt.show()