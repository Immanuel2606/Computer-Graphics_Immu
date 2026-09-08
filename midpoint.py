import matplotlib.pyplot as plt

def circle_points(xc, yc, r):
    x = 0
    y = r
    p = 1 - r
    points = []

    while x <= y:

        points += [
            (xc+x, yc+y), (xc-x, yc+y),
            (xc+x, yc-y), (xc-x, yc-y),
            (xc+y, yc+x), (xc-y, yc+x),
            (xc+y, yc-x), (xc-y, yc-x)
        ]

        x += 1

        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x-y) + 1

    return points


def ellipse_points(xc, yc, rx, ry):

    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    p1 = ry2 - rx2 * ry + 0.25 * rx2

    points = []

    while dx < dy:

        points += [
            (xc+x, yc+y),
            (xc-x, yc+y),
            (xc+x, yc-y),
            (xc-x, yc-y)
        ]

        if p1 < 0:
            x += 1
            dx = 2 * ry2 * x
            p1 += dx + ry2
        else:
            x += 1
            y -= 1
            dx = 2 * ry2 * x
            dy = 2 * rx2 * y
            p1 += dx - dy + ry2

    p2 = (
        ry2 * (x + 0.5)**2
        + rx2 * (y - 1)**2
        - rx2 * ry2
    )

    while y >= 0:

        points += [
            (xc+x, yc+y),
            (xc-x, yc+y),
            (xc+x, yc-y),
            (xc-x, yc-y)
        ]

        if p2 > 0:
            y -= 1
            dy = 2 * rx2 * y
            p2 += rx2 - dy
        else:
            y -= 1
            x += 1
            dx = 2 * ry2 * x
            dy = 2 * rx2 * y
            p2 += dx - dy + rx2

    return points


circle = circle_points(0, 0, 10)
ellipse = ellipse_points(0, 0, 14, 8)

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

cx, cy = zip(*circle)
ex, ey = zip(*ellipse)

ax[0].scatter(cx, cy, s=20)
ax[0].set_title("Midpoint Circle")
ax[0].grid(True)
ax[0].axis("equal")

ax[1].scatter(ex, ey, s=20)
ax[1].set_title("Midpoint Ellipse")
ax[1].grid(True)
ax[1].axis("equal")

plt.suptitle("Circle and Ellipse Rasterization")
plt.tight_layout()
plt.show()