from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

angle = 0

def display():
    global angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0, 0, -6)
    glRotatef(angle, 1, 1, 0)

    faces = [
        ((1,0,0), [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]),
        ((0,1,0), [(-1,-1,-1),(-1,1,-1),(1,1,-1),(1,-1,-1)]),
        ((0,0,1), [(-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)]),
        ((1,1,0), [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1)]),
        ((1,0,1), [(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)]),
        ((0,1,1), [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1)])
    ]

    glBegin(GL_QUADS)
    for color, vertices in faces:
        glColor3f(*color)
        for v in vertices:
            glVertex3f(*v)
    glEnd()

    glutSwapBuffers()


def update():
    global angle
    angle += 5          # Faster rotation
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(600, 500)
glutCreateWindow(b"Fast GPU Rendering")

glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, 600/500, 1, 100)
glMatrixMode(GL_MODELVIEW)

glutDisplayFunc(display)
glutIdleFunc(update)

glutMainLoop()