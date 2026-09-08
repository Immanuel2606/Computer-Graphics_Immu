import matplotlib.pyplot as plt

hi = [-200, -100, 0, 100, 200]
r = 50

fig, ax = plt.subplots()

for h in hi:
    circle = plt.Circle((h, 0), r, fill=False, label=f"h={h}")
    ax.add_patch(circle)

ax.axhline(0, color='black')
ax.axvline(0, color='black')

ax.set_xlim(-260, 260)
ax.set_ylim(-70, 70)

ax.set_aspect('equal')
ax.grid()
ax.legend()
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Circles Along Horizontal Line")

plt.show()