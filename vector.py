from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Raster representation - pixels
    glColor3f(1, 0, 0)
    glPointSize(8)

    glBegin(GL_POINTS)
    for x in range(-80, 81, 20):
        glVertex2f(x, 50)
    glEnd()

    # Vector representation - line
    glColor3f(0, 0, 1)
    glLineWidth(3)

    glBegin(GL_LINES)
    glVertex2f(-80, -20)
    glVertex2f(80, -20)
    glEnd()

    # Vector representation - triangle
    glColor3f(0, 0.7, 0)

    glBegin(GL_TRIANGLES)
    glVertex2f(-50, -80)
    glVertex2f(0, -20)
    glVertex2f(50, -80)
    glEnd()

    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(600, 500)
    glutCreateWindow(b"Raster and Vector Graphics")

    glClearColor(1, 1, 1, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-100, 100, -100, 100)

    glutDisplayFunc(display)
    glutMainLoop()

main()