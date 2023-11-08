from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

import math
import numpy as np


def drawPlane():
    n, w = 100, 500
    d = w / (n-1)

    # Chess 판 그리기
    glColor3f(0.3, 0.5, 0.0)
    glBegin(GL_QUADS)
    for i in range(n):
        for j in range(n): 
            if (i+j)%2 ==0:
                startX = -w/2 + i*d
                startZ = -w/2 + j*d
                glVertex3f(startX, 0, startZ)
                glVertex3f(startX, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ)
    glEnd()

class MyGLWidget(QOpenGLWidget):
    def __init__(self) :
        super().__init__()

    def initializeGL(self):
        pass

    def resizeGL(self, w, h):
        pass

    def paintGL(self):
        pass

class MyWindow(QMainWindow):
    def __init__(self, titleString):
        QMainWindow.__init__(self)
        self.setWindowTitle(titleString)
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('Robot Arm')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)


