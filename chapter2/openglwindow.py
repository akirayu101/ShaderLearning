__author__ = 'akirayu101'

from PyQt5.QtGui import (QGuiApplication, QOpenGLContext,
                         QSurfaceFormat, QWindow)
from PyQt5.QtCore import QEvent

class OpenGLWindow(QWindow):
    def __init__(self, parent=None):
        super(OpenGLWindow, self).__init__(parent)
        self.m_update_pending = False
        self.m_animating = False
        self.m_context = None
        self.setSurfaceType(QWindow.OpenGLSurface)

    def initialize(self):
        pass

    def setAnimating(self, animating):
        self.m_animating = animating
        if animating:
            self.renderLater()

    def renderLater(self):
        if not self.m_update_pending:
            self.m_update_pending = True
            QGuiApplication.postEvent(self, QEvent(QEvent.UpdateRequest))

    def renderNow(self):
        if not self.isExposed():
            return

        self.m_update_pending = False

        needsInitialize = False

        if self.m_context is None:
            self.m_context = QOpenGLContext(self)
            self.surface_format = QSurfaceFormat()
            self.surface_format.setVersion(4, 1)
            self.surface_format.setProfile(QSurfaceFormat.CoreProfile)
            self.m_context.setFormat(self.surface_format)
            self.m_context.create()
            needsInitialize = True

        self.m_context.makeCurrent(self)

        if needsInitialize:
            self.initialize()

        self.render()

        self.m_context.swapBuffers(self)

        if self.m_animating:
            self.renderLater()

    def event(self, event):
        if event.type() == QEvent.UpdateRequest:
            self.renderNow()
            return True
        return super(OpenGLWindow, self).event(event)

    def exposeEvent(self, event):
        self.renderNow()

    def resizeEvent(self, event):
        self.renderNow()
