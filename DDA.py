import matplotlib.pyplot as plt

def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    pixels = []

    for _ in range(steps + 1):
        pixels.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    return pixels


# End points
x1, y1 = 2, 3
x2, y2 = 18, 11

pixels = dda(x1, y1, x2, y2)

x = [p[0] for p in pixels]
y = [p[1] for p in pixels]

plt.figure(figsize=(9, 5))

# Grid-like pixel display
plt.scatter(x, y, s=100)
plt.plot(x, y, linestyle="--", alpha=0.5)

for px, py in pixels:
    plt.text(px, py + 0.25, f"({px},{py})",
             fontsize=8, ha="center")

plt.title("DDA Line Drawing Algorithm")
plt.xlabel("X Pixels")
plt.ylabel("Y Pixels")
plt.xticks(range(0, 21))
plt.yticks(range(0, 15))
plt.grid(True)
plt.axis("equal")
plt.show()