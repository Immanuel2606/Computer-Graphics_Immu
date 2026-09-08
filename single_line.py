import matplotlib.pyplot as plt

x = range(-10, 11)
y = [2*i + 1 for i in x]

plt.axhline(0, color='black')
plt.axvline(0, color='black')

plt.plot(x, y)

plt.grid()
plt.xlabel("X")
plt.ylabel("Y")
plt.title("y = 2x + 1")

plt.show()