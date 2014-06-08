__author__ = 'akirayu101'

from PyQt5.QtGui import (QMatrix4x4, QOpenGLShader, QOpenGLShaderProgram)
from OpenGL import GL
import numpy
from openglwindow import OpenGLWindow


class AkiraRenderWindow(OpenGLWindow):

    def __init__(self):
        super(AkiraRenderWindow, self).__init__()

        self.m_program = 0
        self.m_frame = 0
        self.m_position = 0
        self.m_color = 0
        self.m_vertices = []
        self.m_vao = None
        self.m_matrixUniform = 0

    def initialize(self):

        self.m_vertices = [1,  1, 0.0, 1.0,
                           -1,  1, 0.0, 1.0,
                           0.0, -1, 0.0, 1.0]
        self.m_vertices = numpy.array(self.m_vertices, dtype=numpy.float32)

        self.create_shader()
        self.create_vao()

    def create_shader(self):
        self.m_program = QOpenGLShaderProgram(self)

        self.m_program.addShaderFromSourceFile(QOpenGLShader.Vertex, "shaders/chapter2.vs.glsl")
        self.m_program.addShaderFromSourceFile(QOpenGLShader.Fragment, "shaders/chapter2.fs.glsl")

        self.m_program.link()

        self.m_position = self.m_program.attributeLocation("position")
        self.m_color = self.m_program.attributeLocation("color")
        self.m_matrixUniform = self.m_program.uniformLocation('matrix')

        return self

    def create_vao(self):

        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)

        vertex_buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)

        GL.glEnableVertexAttribArray(self.m_position)
        GL.glVertexAttribPointer(self.m_position, 4, GL.GL_FLOAT, False, 0, self.m_vertices)

        self.m_vao = vertex_array_object
        return self

    def render(self):

        ratio = int(self.devicePixelRatio().real)
        GL.glViewport(0, 0, self.width()*ratio, self.height()*ratio)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.m_program.bind()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        self.m_program.release()