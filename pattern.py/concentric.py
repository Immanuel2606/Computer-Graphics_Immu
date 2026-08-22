import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
import math

def draw_circle(cx, cy, radius, color, segments=100):
    glColor3f(*color)
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2 * math.pi * i / segments
        x = cx + radius * math.cos(theta)
        y = cy + radius * math.sin(theta)
        glVertex2f(x, y)
    glEnd()

def draw_concentric_circles(cx, cy):
    radii = [20, 40, 60, 80, 100]
    colors = [
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
    ]
    for r, color in zip(radii, colors):
        draw_circle(cx, cy, r, color)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Concentric Circles")

    glClearColor(1, 1, 1, 1)  # white background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glLineWidth(2)

    center_x, center_y = 400, 300  # center of the window

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)

        draw_concentric_circles(center_x, center_y)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()