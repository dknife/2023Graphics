
from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *
import math
import numpy as np

class MeshLoader:
    def __init__(self):
        self.nV = 0
        self.nF = 0
        self.vertexBuffer = None
        self.idxBuffer = None

    def loadData(self, filename):
        with open(filename, 'rt') as inputfile:
            self.nV = int(next(inputfile))
            self.vertexBuffer = np.zeros(shape=(self.nV*3, ), dtype = float)

            for i in range(self.nV):
                self.vertexBuffer[i*3: i*3+3] = next(inputfile).split()

            coordMin = self.vertexBuffer.min()
            coordMax = self.vertexBuffer.max()
            scale = max([coordMin, coordMax], key=abs)
            if scale < 0: scale*=-1.0
            self.vertexBuffer /= scale # 가장 큰 좌표값이 1을 넘지 않도록 조정

    def draw(self):
        glBegin(GL_POINTS)
        for i in range(self.nV):            
            glVertex3fv(self.vertexBuffer[i*3:i*3+3])
        glEnd()

class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.myLoader = MeshLoader()
        
    def initializeGL(self):
        glColor3f(0,1,1)
        glPointSize(5)
        self.myLoader.loadData('./Lab06_Meshes/simpleMesh.txt')

        

    def resizeGL(self, w: int, h: int):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, w/h, 0.2, 100)

    def paintGL(self):      

        glClear(GL_COLOR_BUFFER_BIT)        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt( 0, 2, 2, 0, 0, 0, 0, 1, 0)

        self.myLoader.draw()

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()
        self.setWindowTitle(title)
        ## OpenGL Widget 달기
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)
        
def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('Mesh Loader')
    window.show()
    app.exec()

if __name__ == '__main__' :
    main(sys.argv)