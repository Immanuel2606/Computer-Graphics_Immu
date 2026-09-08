import matplotlib.pyplot as plt

r0 = 20
inc = 10

fig, ax = plt.subplots()

for n in range(5):
    r = r0 + inc * n
    circle = plt.Circle((0, 0), r, fill=False, label=f"r={r}")
    ax.add_patch(circle)

ax.axhline(0, color='black')
ax.axvline(0, color='black')

ax.set_xlim(-70, 70)
ax.set_ylim(-70, 70)

ax.set_aspect('equal')
ax.grid()
ax.legend()
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Increasing Size of Circles")

plt.show()