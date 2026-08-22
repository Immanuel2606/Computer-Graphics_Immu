import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))

cx, cy = 300, 200
offsets = [-200, -100, 0, 100, 200]
radius = 30

def draw_circle_outline(surface, center_x, center_y, r, color):
    for x in range(center_x - r, center_x + r + 1):
        for y in range(center_y - r, center_y + r + 1):
            dist_sq = (x - center_x) ** 2 + (y - center_y) ** 2
            if (r - 1) ** 2 <= dist_sq <= r ** 2:
                if 0 <= x < 600 and 0 <= y < 400:
                    surface.set_at((x, y), color)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for offset in offsets:
        draw_circle_outline(screen, cx + offset, cy, radius, (0, 0, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()