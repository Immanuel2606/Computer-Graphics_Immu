import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("7 Circle Flower Pattern")

cx, cy = WIDTH // 2, HEIGHT // 2
R = 120

# 6 Outer circle centers (starting at top: -90 deg, then clockwise by 60 deg)
outer_centers = []
for i in range(6):
    angle = math.radians(i * 60 - 90)
    ox = cx + R * math.cos(angle)
    oy = cy + R * math.sin(angle)
    outer_centers.append((ox, oy))

# Outer circle colors (6 unique colors, 2 shaded regions each)
OUTER_COLORS = [
    (30, 144, 255),   # 0: Blue (Top)
    (76, 175, 80),    # 1: Green (Top-Right)
    (255, 215, 0),    # 2: Gold/Yellow (Bottom-Right)
    (255, 140, 0),    # 3: Orange (Bottom)
    (156, 39, 176),   # 4: Purple (Bottom-Left)
    (233, 30, 99)     # 5: Pink (Top-Left)
]

# Inner circle colors
COLOR_INNER_BASE = (72, 209, 204)  # Cyan background inside central circle
COLOR_PETAL = (255, 69, 58)        # Coral Red for the 6 inner petals

def get_pixel_color(px, py):
    d_center_sq = (px - cx) ** 2 + (py - cy) ** 2
    in_center = d_center_sq <= R ** 2

    # Check which outer circles contain this pixel
    inside_indices = []
    for i, (ox, oy) in enumerate(outer_centers):
        if (px - ox) ** 2 + (py - oy) ** 2 <= R ** 2:
            inside_indices.append(i)

    # Inner central circle area
    if in_center:
        # The 6 intersecting petal lenses inside the inner circle
        if len(inside_indices) >= 2:
            return COLOR_PETAL
        return COLOR_INNER_BASE

    # Outer regions (each outer circle receives 2 shaded segments)
    if len(inside_indices) == 1:
        return OUTER_COLORS[inside_indices[0]]
    elif len(inside_indices) == 2:
        i, j = inside_indices
        if (i + 1) % 6 == j:
            return OUTER_COLORS[i]
        elif (j + 1) % 6 == i:
            return OUTER_COLORS[j]
        return OUTER_COLORS[i]

    return None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Fill regions pixel-by-pixel
    for x in range(cx - 2 * R, cx + 2 * R + 1):
        for y in range(cy - 2 * R, cy + 2 * R + 1):
            color = get_pixel_color(x, y)
            if color:
                screen.set_at((x, y), color)

    # Draw black circle outlines
    pygame.draw.circle(screen, (0, 0, 0), (cx, cy), R, 2)
    for ox, oy in outer_centers:
        pygame.draw.circle(screen, (0, 0, 0), (round(ox), round(oy)), R, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()