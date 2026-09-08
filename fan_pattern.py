import matplotlib.pyplot as plt

x = range(-10, 11)

for m in [-3, -2, -1, 0, 1, 2, 3]:
    y = [m*i for i in x]
    plt.plot(x, y, label=f"m={m}")

plt.axhline(0, color='black')
plt.axvline(0, color='black')

plt.xlim(-10, 10)
plt.ylim(-10, 10)

plt.grid()
plt.legend()
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Fan Pattern: y = mx")

plt.show()