from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pywavefront import *
from pywavefront import visualization
import numpy as np

from OpenGL.arrays import vbo
from OpenGL.GL import shaders


class Rocket:

    def __init__(self, body, isRotate):
        # Carrega o OBJ do foguete
        self.body = Wavefront(body, create_materials=True)
        # Estado de rotação do foguete
        self.isRotate = isRotate

        # EIXOS
        self.x = 0.0
        self.y = -15.0
        self.z = 0.0
        self.rotate = 0.0

        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0

        self.direction = np.array([0.0, 1.0, 0.0, 0.0])
        self.position = np.array([self.x, self.y, self.z, 0.0])

        # VELOCIDADE DE ROTAÇÃO
        self.rotationSpeed = 1.0

    def init(self):
        vertexShader = shaders.compileShader(
            open('objs/rocket.vert', 'r').read(), GL_VERTEX_SHADER)
        fragmentShader = shaders.compileShader(
            open('objs/rocket.frag', 'r').read(), GL_FRAGMENT_SHADER)

        self.rocket_shader = glCreateProgram()
        glAttachShader(self.rocket_shader, vertexShader)
        glAttachShader(self.rocket_shader, fragmentShader)
        glLinkProgram(self.rocket_shader)

        self.LIGTH_LOCATIONS = {
            'Global_ambient': glGetUniformLocation(self.rocket_shader, 'Global_ambient'),
            'Light_ambient': glGetUniformLocation(self.rocket_shader, 'Light_ambient'),
            'Light_diffuse': glGetUniformLocation(self.rocket_shader, 'Light_diffuse'),
            'Light_location': glGetUniformLocation(self.rocket_shader, 'Light_location'),
            'Light_specular': glGetUniformLocation(self.rocket_shader, 'Light_specular'),
            'Material_ambient': glGetUniformLocation(self.rocket_shader, 'Material_ambient'),
            'Material_diffuse': glGetUniformLocation(self.rocket_shader, 'Material_diffuse'),
            'Material_shininess': glGetUniformLocation(self.rocket_shader, 'Material_shininess'),
            'Material_specular': glGetUniformLocation(self.rocket_shader, 'Material_specular'),
        }

        self.ATTR_LOCATIONS = {
            'Vertex_position': glGetAttribLocation(self.rocket_shader, 'Vertex_position'),
            'Vertex_normal': glGetAttribLocation(self.rocket_shader, 'Vertex_normal')
        }

    def display(self):
        self._generateBodyAndMoveToOrigin()

    def renderShader(self, material):
        vertices = material.vertices
        vertices = np.array(vertices, dtype=np.float32).reshape(-1, 6)
        vbo_rocket = vbo.VBO(vertices)

        glPushMatrix()
        glTranslatef(self.position)
        glRotatef(80, 0.0, 1.0, 0.0)

        glUseProgram(self.rocket_shader)
        glUniform4f(
            self.LIGTH_LOCATIONS['Global_ambient'], 0.2, 0.2, 0.2, 1.0)
        glUniform3f(self.LIGTH_LOCATIONS['Light_location'], -5.0, 5.0, 0.0)
        glUniform4f(
            self.LIGTH_LOCATIONS['Light_ambient'], 0.2, 0.2, 0.2, 0.5)
        glUniform4f(
            self.LIGTH_LOCATIONS['Light_diffuse'], 0.9, 0.9, 0.9, 1.0)
        glUniform4f(
            self.LIGTH_LOCATIONS['Light_specular'], 0.9, 0.9, 0.9, 1.0)

        glUniform4f(
            self.LIGTH_LOCATIONS['Material_ambient'],
            material.ambient[0],
            material.ambient[1],
            material.ambient[2],
            material.ambient[3]
        )
        glUniform4f(
            self.LIGTH_LOCATIONS['Material_diffuse'],
            material.diffuse[0],
            material.diffuse[1],
            material.diffuse[2],
            material.diffuse[3])
        glUniform4f(
            self.LIGTH_LOCATIONS['Material_specular'],
            material.specular[0],
            material.specular[1],
            material.specular[2],
            material.specular[3])
        glUniform1f(
            self.LIGTH_LOCATIONS['Material_shininess'], material.shininess)

        vbo_rocket.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 24, vbo_rocket+12)
        glNormalPointer(GL_FLOAT, 24, vbo_rocket)
        glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])
        vbo_rocket.unbind()

        glUseProgram(0)

        glPopMatrix()

    # FUNÇÕES QUE DEFINEM TRANSFORMAÇÕES PARA O OBJETO

    def _generateBodyAndMoveToOrigin(self):
        # for mesh in self.body.mesh_list:
        #     for material in mesh.materials:
        #         self.renderShader(material)
        glPushMatrix()

        glTranslatef(self.position[0], self.position[1], self.position[2])

        glRotatef(80, 0.0, 1.0, 0.0)

        # glRotatef(self.rotate, 1.0, 0.0, 0.0)

        glMultMatrixf(self.handleToCreateRotationMatrix(
            [self.pitch, self.yaw, self.roll]))

        visualization.draw(self.body)

        glPopMatrix()

    # FUNÇÕES DE ANIMAÇÃO

    def animRotation(self, value):
        self.rotate += self.rotationSpeed
        glutPostRedisplay()
        glutTimerFunc(2000 // 60, self.animRotation, 0)

    def _objetcTouchInEdge(self):
        if (self.x == -32 or self.x == 32 or self.y == 15 or self.y == -18):
            return False
        return True

    def handleToCreateRotationMatrix(self, angles):
        pitch, yaw, roll = angles
        rotation_matrix = np.identity(4)
        cos_p, sin_p = np.cos(pitch), np.sin(pitch)
        cos_y, sin_y = np.cos(yaw), np.sin(yaw)
        cos_r, sin_r = np.cos(roll), np.sin(roll)

        rotation_matrix[0, 0] = cos_y * cos_r
        rotation_matrix[0, 1] = sin_p * sin_y * cos_r - cos_p * sin_r
        rotation_matrix[0, 2] = cos_p * sin_y * cos_r + sin_p * sin_r
        rotation_matrix[1, 0] = cos_y * sin_r
        rotation_matrix[1, 1] = sin_p * sin_y * sin_r + cos_p * cos_r
        rotation_matrix[1, 2] = cos_p * sin_y * sin_r - sin_p * cos_r
        rotation_matrix[2, 0] = -sin_y
        rotation_matrix[2, 1] = sin_p * cos_y
        rotation_matrix[2, 2] = cos_p * cos_y

        return rotation_matrix

    def keys(self, key, x, y):
        glutPostRedisplay()

        if key == GLUT_KEY_LEFT:
            self.pitch += np.radians(5)

            self.direction = np.dot(self.handleToCreateRotationMatrix(
                [0,  0, np.radians(5)]), self.direction)

        elif key == GLUT_KEY_RIGHT:
            self.pitch -= np.radians(5)

            self.direction = np.dot(self.handleToCreateRotationMatrix(
                [0,  0, -np.radians(5)]), self.direction)

        elif key == GLUT_KEY_UP:
            if self._objetcTouchInEdge():
                self.position += self.direction * 0.5
