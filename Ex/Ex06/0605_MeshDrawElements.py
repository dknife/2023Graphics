
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
        self.colorBuffer = None

    def loadData(self, filename):
        with open(filename, 'rt') as inputfile:
            self.nV = int(next(inputfile))
            self.vertexBuffer = np.zeros(shape=(self.nV*3, ), dtype = float)
            self.colorBuffer =  np.zeros(shape = (self.nV*3, ), dtype=float)


            tenpercent = self.nV//10
            print('vertice loading... 0%')

            for i in range(self.nV):
                if i % tenpercent == 0:
                    print(f' {i*10//tenpercent} %')

                verts = next(inputfile).split()
                self.vertexBuffer[i*3: i*3+3] = verts[0:3]
                self.colorBuffer[i*3: i*3+3] = verts[0:3]

            coordMin = self.vertexBuffer.min()
            coordMax = self.vertexBuffer.max()
            scale = max([coordMin, coordMax], key=abs)
            if scale < 0: scale*=-1.0
            self.vertexBuffer /= scale # 가장 큰 좌표값이 1을 넘지 않도록 조정
            self.colorBuffer /= scale
            self.colorBuffer = (self.colorBuffer + np.array([1])) / 2.0

            self.nF = int(next(inputfile))
            self.idxBuffer = np.zeros(shape=(self.nF*3, ), dtype=int)

            tenpercent = self.nF//10
            print('faces loading... 0%')
            for i in range(self.nF):
                if i % tenpercent == 0:
                    print(f' {i*10//tenpercent} %')
                idx = next(inputfile).split()
                self.idxBuffer[i*3: i*3+3] = idx[1:4]
            print(' done')

    def draw(self):
        glColor3f(0, 1, 0.5)
        for i in range(self.nF):
            vIdx = self.idxBuffer[i*3: i*3+3]
            v0, v1, v2 = vIdx[0], vIdx[1], vIdx[2]

            glBegin(GL_TRIANGLES)            
            glColor3fv((self.vertexBuffer[v0*3: v0*3+3]+np.array([1]))/2)
            glVertex3fv(self.vertexBuffer[v0*3: v0*3+3])
            glColor3fv((self.vertexBuffer[v1*3: v1*3+3]+np.array([1]))/2)
            glVertex3fv(self.vertexBuffer[v1*3: v1*3+3])
            glColor3fv((self.vertexBuffer[v2*3: v2*3+3]+np.array([1]))/2)
            glVertex3fv(self.vertexBuffer[v2*3: v2*3+3])
            glEnd()

            glColor3f(1,1,0)
            glBegin(GL_LINE_LOOP)
            glVertex3fv(self.vertexBuffer[v0*3: v0*3+3])
            glVertex3fv(self.vertexBuffer[v1*3: v1*3+3])
            glVertex3fv(self.vertexBuffer[v2*3: v2*3+3])
            glEnd()

    def draw_elements(self):
        glEnableClientState(GL_COLOR_ARRAY)
        glDrawElements(GL_TRIANGLES, self.nF * 3, GL_UNSIGNED_INT, self.idxBuffer)
        glDisableClientState(GL_COLOR_ARRAY)
        glDrawArrays(GL_POINTS, 0, self.nV)

    

class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.myLoader = MeshLoader()
        
    def initializeGL(self):
        glColor3f(0,1,1)
        glPointSize(5)
        self.myLoader.loadData('./Lab06_Meshes/skull.txt')
        
        self.drawList = glGenLists(1)
        glNewList(self.drawList, GL_COMPILE)
        self.myLoader.draw()
        glEndList()

        self.angle = 0

        glEnable(GL_DEPTH_TEST)
        glEnableClientState(GL_VERTEX_ARRAY)
        
        glVertexPointer(3, GL_FLOAT, 0, self.myLoader.vertexBuffer)
        glColorPointer(3, GL_FLOAT, 0, self.myLoader.colorBuffer)
        glPointSize(1)
        

    def resizeGL(self, w: int, h: int):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, w/h, 0.2, 100)
        self.myLoader.draw()

    def paintGL(self):      
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt( 2, 1, 5, 0, 0, 0, 0, 1, 0)
        
        glRotatef(self.angle, 0, 1, 0)
        #self.myLoader.draw()
        #glCallList(self.drawList)
        self.myLoader.draw_elements()
        self.angle += 1

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()
        self.setWindowTitle(title)
        ## OpenGL Widget 달기
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def timeout(self):
        self.glWidget.update()
        
def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('Mesh Loader')
    window.show()
    app.exec()

if __name__ == '__main__' :
    main(sys.argv)