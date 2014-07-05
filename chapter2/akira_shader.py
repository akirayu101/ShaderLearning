__author__ = 'akirayu101'

from PyQt5.QtGui import (QMatrix4x4, QOpenGLShader, QOpenGLShaderProgram, QVector4D)
from OpenGL import GL
from openglwindow import OpenGLWindow
from math import sin, cos


class AkiraRenderWindow(OpenGLWindow):

    def __init__(self):
        super(AkiraRenderWindow, self).__init__()

        self.m_program = 0
        self.m_frame = 0.0
        self.m_vertex = 0
        self.m_color = 0
        self.m_colors = []
        self.m_vertices = []
        self.m_vao = None
        self.m_matrixUniform = 0
        self.m_offset = []
        self.m_offset_vec = 0
        self.matrix = 0

    def initialize(self):

        self.create_shader()
        self.create_vao()

        self.matrix = QMatrix4x4()
        #self.matrix.perspective(60, 4.0/3.0, 0.01, 100)
        #self.matrix.translate(0, 0, -2)


    def create_shader(self):
        self.m_program = QOpenGLShaderProgram(self)

        self.m_program.addShaderFromSourceFile(QOpenGLShader.Vertex, "shaders/chapter2.vs.glsl")
        self.m_program.addShaderFromSourceFile(QOpenGLShader.Fragment, "shaders/chapter2.fs.glsl")

        self.m_program.link()

        self.m_vertex = self.m_program.attributeLocation("m_vertex")
        self.m_offset = self.m_program.attributeLocation("m_offset")
        self.m_color = self.m_program.attributeLocation("m_color")
        self.m_matrixUniform = self.m_program.uniformLocation('m_matrix')

        self.m_program.enableAttributeArray(self.m_vertex)
        self.m_program.enableAttributeArray(self.m_offset)
        self.m_program.enableAttributeArray(self.m_color)
        self.m_program.enableAttributeArray(self.m_matrixUniform)

        return self

    def create_vao(self):

        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)

        vertex_buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)

        #using PyQt shader program instead
        GL.glEnableVertexAttribArray(self.m_offset)
        GL.glEnableVertexAttribArray(self.m_vertex)
        GL.glEnableVertexAttribArray(self.m_color)
        self.m_vao = vertex_array_object
        return self

    def render(self):

        ratio = int(self.devicePixelRatio().real)
        GL.glViewport(0, 0, self.width()*ratio, self.height()*ratio)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.m_offset_vec = [(sin(self.m_frame/20)*0.5, cos(self.m_frame/20)*0.5, 0.0, 0.0),
                             (sin(self.m_frame/20)*0.5, cos(self.m_frame/20)*0.5, 0.0, 0.0),
                             (sin(self.m_frame/20)*0.5, cos(self.m_frame/20)*0.5, 0.0, 0.0)]

        self.m_vertices = [(0.25, -0.25, 0, 1.0),
                           (-0.25, -0.25, 0, 1.0),
                           (0.25,  0.25, 0, 1.0)]

        self.m_colors = [(0.0, 0.0, 1.0, 1.0),
                         (0.0, 1.0, 0.0, 1.0),
                         (1.0, 0.0, 0.0, 1.0)]

        self.m_program.setAttributeArray(self.m_offset, self.m_offset_vec)
        self.m_program.setAttributeArray(self.m_vertex, self.m_vertices)
        self.m_program.setAttributeArray(self.m_color, self.m_colors)

        self.m_program.bind()

        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        self.m_program.release()

        self.m_frame += 1