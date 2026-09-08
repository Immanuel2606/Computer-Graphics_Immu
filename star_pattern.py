import matplotlib.pyplot as plt

x = range(-10, 11)

plt.plot(x, x, label="y=x")
plt.plot(x, [-i for i in x], label="y=-x")
plt.axhline(0, color="black", label="y=0")
plt.axvline(0, color="black", label="x=0")

plt.xlim(-10, 10)
plt.ylim(-10, 10)

plt.grid()
plt.legend()
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Star Pattern")

plt.show()