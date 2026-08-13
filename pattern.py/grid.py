import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for x in [100, 200, 300, 400, 500]:
        for y in range(0, 400):
            screen.set_at((x, y), (0, 0, 0))

    for y in [60, 130, 200, 270, 340]:
        for x in range(0, 600):
            screen.set_at((x, y), (0, 0, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()