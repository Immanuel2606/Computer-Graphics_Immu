import matplotlib.pyplot as plt

k = range(-5, 6)

for i in k:
    plt.axvline(i)
    plt.axhline(i)

plt.xlim(-6, 6)
plt.ylim(-6, 6)

plt.grid()
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Grid Pattern: x=k, y=k")

plt.show()