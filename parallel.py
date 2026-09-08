import matplotlib.pyplot as plt

x = range(-10, 11)

for c in [-2, -1, 0, 1, 2]:
    y = [2*i + c for i in x]
    plt.plot(x, y, label=f"c={c}")

plt.axhline(0, color='black')
plt.axvline(0, color='black')

plt.grid()
plt.legend()
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Family of Parallel Lines: y = 2x + c")

plt.show()