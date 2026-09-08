from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Points
    glColor3f(1, 0, 0)
    glPointSize(8)
    glBegin(GL_POINTS)
    glVertex2f(-70, 70)
    glVertex2f(-50, 70)
    glVertex2f(-30, 70)
    glEnd()

    # Line
    glColor3f(0, 0, 1)
    glLineWidth(4)
    glBegin(GL_LINES)
    glVertex2f(-80, 40)
    glVertex2f(80, 40)
    glEnd()

    # Triangle
    glColor3f(0, 1, 0)
    glBegin(GL_TRIANGLES)
    glVertex2f(-70, -10)
    glVertex2f(-20, 30)
    glVertex2f(20, -10)
    glEnd()

    # Rectangle
    glColor3f(1, 0.5, 0)
    glBegin(GL_QUADS)
    glVertex2f(30, -10)
    glVertex2f(75, -10)
    glVertex2f(75, 30)
    glVertex2f(30, 30)
    glEnd()

    # Polygon
    glColor3f(0.7, 0, 0.8)
    glBegin(GL_POLYGON)
    glVertex2f(-40, -80)
    glVertex2f(-10, -50)
    glVertex2f(30, -60)
    glVertex2f(20, -90)
    glVertex2f(-20, -95)
    glEnd()

    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(600, 500)
    glutCreateWindow(b"Graphics Primitives and Framebuffer")

    glClearColor(1, 1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-100, 100, -100, 100)

    glutDisplayFunc(display)
    glutMainLoop()

main()