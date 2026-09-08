import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(10, 15))

ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis("off")


# Function to create boxes
def box(x, y, w, h, text):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.03",
            fill=False
        )
    )
    ax.text(
        x + w/2, y + h/2,
        text,
        ha="center",
        va="center",
        fontsize=10
    )


# Function to create arrows
def arrow(x1, y1, x2, y2):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->")
    )


# Flowchart boxes

box(3.5, 14.8, 3, 0.7, "START")

box(3, 13.2, 4, 0.9,
    "Initialize Python\nMatplotlib & NumPy")

box(3, 11.6, 4, 0.9,
    "Create 2D Coordinate\nSystem")

box(3, 10.0, 4, 0.9,
    "Set Initial\nVanishing Point")

box(3, 8.4, 4, 0.9,
    "Generate Perspective\n/ Converging Lines")

box(3, 6.8, 4, 0.9,
    "Draw Simple\nPerspective Scene")

box(3, 5.1, 4, 1.0,
    "User Changes\nVanishing Point\nUsing Slider")

box(3, 3.5, 4, 0.9,
    "Recalculate\nPerspective Lines")

box(3, 1.9, 4, 0.9,
    "Update Graphical\nOutput")

box(3, 0.3, 4, 0.9,
    "Continue Interaction?")


# END box
box(8, 0.3, 1.5, 0.9, "END")


# Main arrows

arrow(5, 14.8, 5, 14.1)
arrow(5, 13.2, 5, 12.5)
arrow(5, 11.6, 5, 10.9)
arrow(5, 10.0, 5, 9.3)
arrow(5, 8.4, 5, 7.7)
arrow(5, 6.8, 5, 6.1)
arrow(5, 5.1, 5, 4.4)
arrow(5, 3.5, 5, 2.8)
arrow(5, 1.9, 5, 1.2)


# NO → END
ax.annotate(
    "NO",
    xy=(8, 0.75),
    xytext=(7.3, 0.75),
    ha="center",
    va="center",
    arrowprops=dict(arrowstyle="->")
)


# YES → loop back to slider
ax.annotate(
    "YES",
    xy=(3, 0.75),
    xytext=(1.5, 0.75),
    ha="center",
    va="center",
    arrowprops=dict(arrowstyle="->")
)

# Loop line
ax.plot(
    [1.5, 1.5, 1.5, 3],
    [0.75, 5.6, 5.6, 5.6]
)

ax.annotate(
    "",
    xy=(3, 5.6),
    xytext=(1.5, 5.6),
    arrowprops=dict(arrowstyle="->")
)


# Title
plt.title(
    "Flowchart: Vanishing Point Detection and Perspective Visualization",
    fontsize=14,
    fontweight="bold"
)

plt.show()