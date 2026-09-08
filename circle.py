import numpy as np
import matplotlib.pyplot as plt

# Circle parameters
h = 5
k = 5
r = 3

# Draw circle
theta = np.linspace(0, 2 * np.pi, 500)

xc = h + r * np.cos(theta)
yc = k + r * np.sin(theta)

plt.plot(xc, yc, color="black", linewidth=2.5)

# Slope of both parallel lines
m = 0.2


# Function to draw only the part of line inside circle
def draw_line(c, color):

    # Circle:
    # (x-h)^2 + (y-k)^2 = r^2
    #
    # Line:
    # y = mx + c

    A = 1 + m**2
    B = 2 * (m * (c - k) - h)
    C = h**2 + (c - k)**2 - r**2

    # Find intersection points
    roots = np.roots([A, B, C])

    x1, x2 = sorted(roots)

    y1 = m * x1 + c
    y2 = m * x2 + c

    # Draw only between the two intersection points
    plt.plot(
        [x1, x2],
        [y1, y2],
        color=color,
        linewidth=8,
        solid_capstyle="butt"
    )


# RED line - upper
draw_line(4.5, "red")

# GREEN line - lower
draw_line(2.9, "green")


# X-axis
plt.axhline(0, color="black", linewidth=2)

# Y-axis
plt.axvline(0, color="black", linewidth=2)


# Axis limits - circle remains in 1st quadrant
plt.xlim(0, 10)
plt.ylim(0, 10)

# Labels
plt.xlabel("X", fontsize=14)
plt.ylabel("Y", fontsize=14)

plt.title("Parallel Lines Inside a Circle")

# Grid
plt.grid(True, linestyle="--", alpha=0.3)

# Equal scale
plt.gca().set_aspect("equal")

plt.show()