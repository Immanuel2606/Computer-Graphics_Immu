import numpy as np
import matplotlib.pyplot as plt

# 3D cube vertices
cube = np.array([
    [-1, -1, 2],
    [ 1, -1, 2],
    [ 1,  1, 2],
    [-1,  1, 2],
    [-1, -1, 6],
    [ 1, -1, 6],
    [ 1,  1, 6],
    [-1,  1, 6]
])

# Perspective projection
f = 4

projected = []

for X, Y, Z in cube:
    x = f * X / Z
    y = f * Y / Z
    projected.append([x, y])

projected = np.array(projected)

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

fig = plt.figure(figsize=(12, 5))

# 3D view
ax1 = fig.add_subplot(121, projection='3d')

for a, b in edges:
    ax1.plot(
        [cube[a,0], cube[b,0]],
        [cube[a,1], cube[b,1]],
        [cube[a,2], cube[b,2]]
    )

ax1.set_title("Original 3D Object")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Depth (Z)")

# Perspective view
ax2 = fig.add_subplot(122)

for a, b in edges:
    ax2.plot(
        [projected[a,0], projected[b,0]],
        [projected[a,1], projected[b,1]]
    )

ax2.set_title("Perspective Projection")
ax2.set_xlabel("Projected X")
ax2.set_ylabel("Projected Y")
ax2.grid(True)
ax2.set_aspect("equal")

plt.tight_layout()
plt.show()