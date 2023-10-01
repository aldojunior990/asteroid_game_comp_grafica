from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pywavefront import *
from pywavefront import visualization
from rocket import *
from asteroid import *

from OpenGL.arrays import vbo
from OpenGL.GL import shaders


class Game:

    def __init__(self, enemie, hero):
        self.enemie = enemie
        self.hero = hero

        self.light_position = [0.0, 0.0, 30.0, 1.0]
        self.amb_light = [0.2, 0.2, 0.2, 0.5]
        self.diffuse = [0.9, 0.9, 0.9, 1.0]
        self.specular = [1.0, 1.0, 1.0, 1.0]
        self.attenuation_quad = 0.00
        self.attenuation_linear = 0.005

    def ilumination(self):
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.amb_light)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular)
        glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, self.attenuation_quad)
        glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, self.attenuation_linear)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.enemie.display()
        self.ilumination()
        self.hero.display()
        glutSwapBuffers()

    def init(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)
        # glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        self.hero.init()

    def gameCamera(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, w / h, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 30.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(1280, 720)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(b"GAME")

        self.init()
        # self.ilumination()

        # Configuração do modelo de shading

        # Chama a função callback de display dos inimigos
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.gameCamera)
        glutTimerFunc(0, self.enemie.animRotation, 0)

        glutSpecialFunc(self.hero.keys)

        # Loop principal do OpenGL
        glutMainLoop()


if __name__ == "__main__":
    rocket = Rocket("./objs/rocket.obj", True)
    asteroid = Asteroid("./objs/asteroid.obj")
    game = Game(asteroid, rocket)
    game.run()
