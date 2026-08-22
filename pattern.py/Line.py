import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))

cx, cy = 300, 200
m = -1
c = cy - m * cx

line_start_x = cx - 150
line_end_x = cx + 150

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for x in range(0, 600):
        screen.set_at((x, cy), (150, 150, 150))

    for y in range(0, 400):
        screen.set_at((cx, y), (150, 150, 150))

    for x in range(line_start_x, line_end_x + 1):
        y = round(m * x + c)
        if 0 <= y < 400:
            screen.set_at((x, y), (0, 0, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()