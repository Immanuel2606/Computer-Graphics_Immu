import matplotlib.pyplot as plt
import numpy as np

hc, kc = 0, 0
a = 5
r0 = 2
b = 1
delta_theta = 0.5

fig, ax = plt.subplots()

for i in range(30):
    theta = i * delta_theta

    hi = hc + a * i * np.cos(theta)
    ki = kc + a * i * np.sin(theta)
    ri = r0 + b * i

    circle = plt.Circle((hi, ki), ri, fill=False)
    ax.add_patch(circle)

ax.set_xlim(-170, 170)
ax.set_ylim(-170, 170)

ax.axhline(0, color='black')
ax.axvline(0, color='black')

ax.set_aspect('equal')
ax.grid()
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Spiral of Increasing Circles")

plt.show()