import matplotlib.pyplot as plt

radii = [20, 40, 60, 80, 100]

fig, ax = plt.subplots()

for r in radii:
    circle = plt.Circle((0, 0), r, fill=False, label=f"r={r}")
    ax.add_patch(circle)

ax.set_xlim(-110, 110)
ax.set_ylim(-110, 110)

ax.axhline(0, color='black')
ax.axvline(0, color='black')

ax.set_aspect('equal')
ax.grid()
ax.legend()
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Concentric Circles")

plt.show()