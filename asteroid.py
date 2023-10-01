from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pywavefront import *
from pywavefront import visualization


class Asteroid:

    def __init__(self, body):
        # Carrega o OBJ
        self.body = Wavefront(body)

        # EIXOS
        self.x = 0.0
        self.y = 10.0
        self.z = 0.0
        self.translate = 0.0
        # VELOCIDADE DE ROTAÇÃO
        self.translateSpeed = 1.0

    def display(self):
        # self._rotation()
        self._generateBodyAndMoveToOrigin()

    # FUNÇÕES QUE DEFINEM TRANSFORMAÇÕES PARA O OBJETO
    def _generateBodyAndMoveToOrigin(self):
        glPushMatrix()
        glTranslatef(self.translate, self.y, self.z)
        glRotatef(80 - self.translate, 1.0, 0.0, 0.0)

        visualization.draw(self.body)

        glPopMatrix()

    # FUNÇÕES DE ANIMAÇÃO
    def animRotation(self, value):
        if (self.translate <= -30):
            self.translateSpeed = 1
        elif (self.translate >= 30):
            self.translateSpeed = -1

        self.translate += self.translateSpeed
        glutPostRedisplay()
        glutTimerFunc(2000 // 60, self.animRotation, 0)
