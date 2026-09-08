import matplotlib.pyplot as plt

def bresenham(x1, y1, x2, y2):

    pixels = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:
        pixels.append((x1, y1))

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy

    return pixels


x1, y1 = 2, 3
x2, y2 = 18, 11

pixels = bresenham(x1, y1, x2, y2)

x = [p[0] for p in pixels]
y = [p[1] for p in pixels]

plt.figure(figsize=(9, 5))

plt.scatter(x, y, s=120)
plt.plot(x, y, linestyle="--", alpha=0.5)

for px, py in pixels:
    plt.text(px, py + 0.3, f"{px},{py}",
             fontsize=8, ha="center")

plt.title("Bresenham's Line Drawing Algorithm")
plt.xlabel("X Pixels")
plt.ylabel("Y Pixels")
plt.xticks(range(0, 21))
plt.yticks(range(0, 15))
plt.grid(True)
plt.axis("equal")
plt.show()