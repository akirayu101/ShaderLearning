__author__ = 'akirayu101'


from PyQt5.QtGui import (QGuiApplication, QSurfaceFormat)
from akira_shader import AkiraRenderWindow


if __name__ == '__main__':

    import sys

    app = QGuiApplication(sys.argv)

    surface_format = QSurfaceFormat()
    surface_format.setSamples(4)

    window = AkiraRenderWindow()
    window.setFormat(surface_format)
    window.resize(800, 600)
    window.show()

    window.setAnimating(True)

    sys.exit(app.exec_())
