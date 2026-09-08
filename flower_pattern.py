import matplotlib.pyplot as plt
import numpy as np

hc, kc = 0, 0
R = 50
r = 20
n = 8

fig, ax = plt.subplots()

for i in range(n):
    hi = hc + R * np.cos(2 * np.pi * i / n)
    ki = kc + R * np.sin(2 * np.pi * i / n)

    circle = plt.Circle((hi, ki), r, fill=False)
    ax.add_patch(circle)

ax.set_xlim(-80, 80)
ax.set_ylim(-80, 80)

ax.axhline(0, color='black')
ax.axvline(0, color='black')

ax.set_aspect('equal')
ax.grid()
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Flower Pattern")

plt.show()