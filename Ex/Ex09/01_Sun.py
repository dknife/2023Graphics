import typing
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

import math
import numpy as np

def drawAxes():
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)
    glEnd()

class MeshLoader :
    def __init__(self):
        self.nV = 0 # 정점의 개수
        self.nF = 0 # 면의 개수
        self.vBuffer = None # 정점 버퍼
        self.iBuffer = None # 면을 표현하는 인덱스 버퍼
##################################################################################
    def make_display_list(self):  
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        self.draw()
        glEndList()

    def draw_display_list(self):
        glCallList(self.list)
##################################################################################

    def loadMesh(self, filename) :
        with open(filename, 'rt') as inputfile:
            # with 구문의 내부 블럭 시작
            self.nV = int(next(inputfile))
            self.vBuffer = np.zeros((self.nV*3, ), dtype=float)
            for i in range(self.nV):
                verts = next(inputfile).split()
                self.vBuffer[i*3: i*3+3] = verts[0:3]

            coordMin = self.vBuffer.min()
            coordMax = self.vBuffer.max()
            scale = max([coordMin, coordMax], key=abs)
            self.vBuffer /= scale

            self.nF = int(next(inputfile))
            self.iBuffer = np.zeros((self.nF*3, ), dtype=int)
            for i in range(self.nF):
                idx = next(inputfile).split() # idx[0]: 면을 구성하는 점의 개수
                # 필요한 정보는 idx[1], idx[2], idx[3] = idx[1:4]
                self.iBuffer[i*3: i*3+3] = idx[1:4]
            # with 구문의 내부 블럭 끝

        self.make_display_list() ####################################################

    def draw(self):
        
        glBegin(GL_TRIANGLES)
        for i in range(self.nF):            
            # 각 면을 그린다.
            # 각 면을 구성하는 정점의 번호는 
            v = self.iBuffer[i*3: i*3+3]
            # 각 정점은 v[0], v[1], v[2]
            # 첫 점은 v[0]의 번호를 가진 정점을 vBuffer에서 찾는다
            glColor3fv( (self.vBuffer[v[0]*3: v[0]*3+3] + np.array([1])) / 2.0)
            glVertex3fv(self.vBuffer[v[0]*3: v[0]*3+3])
            # 두번째 점은 v[1]의 번호를 가진 정점을 vBuffer에서 찾는다
            glColor3fv( (self.vBuffer[v[1]*3: v[1]*3+3] + np.array([1])) / 2.0)            
            glVertex3fv(self.vBuffer[v[1]*3: v[1]*3+3])
            # 세번째 점은 v[2]의 번호를 가진 정점을 vBuffer에서 찾는다
            glColor3fv( (self.vBuffer[v[2]*3: v[2]*3+3] + np.array([1])) / 2.0)  
            glVertex3fv(self.vBuffer[v[2]*3: v[2]*3+3])        
        glEnd()

        glColor3f(0,0,1)
        for i in range(self.nF):
            glBegin(GL_LINE_LOOP)
            # 각 면을 그린다.
            # 각 면을 구성하는 정점의 번호는 
            v = self.iBuffer[i*3: i*3+3]
            # 각 정점은 v[0], v[1], v[2]
            # 첫 점은 v[0]의 번호를 가진 정점을 vBuffer에서 찾는다
            glVertex3fv(self.vBuffer[v[0]*3: v[0]*3+3])
            # 두번째 점은 v[1]의 번호를 가진 정점을 vBuffer에서 찾는다
            glVertex3fv(self.vBuffer[v[1]*3: v[1]*3+3])
            # 세번째 점은 v[2]의 번호를 가진 정점을 vBuffer에서 찾는다
            glVertex3fv(self.vBuffer[v[2]*3: v[2]*3+3])
            glEnd()


class MyGLWidget(QOpenGLWidget):
    def __init__(self) :
        super().__init__()

    def initializeGL(self):
        glClearColor(0.0, 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)
        self.sphereMesh = MeshLoader()
        self.sphereMesh.loadMesh("./Ex09_SolarSystem/sphere.txt")

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        gluPerspective(60, w/h, 0.1, 500)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 2, 6, 0, 0, -3, 0, 1, 0)

        self.sphereMesh.draw_display_list()
        



class MyWindow(QMainWindow):
    def __init__(self, titleString):
        QMainWindow.__init__(self)
        self.setWindowTitle(titleString)
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

    def keyPressEvent(self, e):
        step = 0.1
        angleStep = 5

        if e.key() == Qt.Key.Key_W:
            self.glWidget.basePosition[2] -= step
        if e.key() == Qt.Key.Key_S:
            self.glWidget.basePosition[2] += step
        if e.key() == Qt.Key.Key_A:
            self.glWidget.basePosition[0] -= step
        if e.key() == Qt.Key.Key_D:
            self.glWidget.basePosition[0] += step

        if e.key() == Qt.Key.Key_Q:
            self.glWidget.arm1Y += angleStep
        if e.key() == Qt.Key.Key_E:
            self.glWidget.arm1Y -= angleStep
        if e.key() == Qt.Key.Key_R:
            self.glWidget.arm1X += angleStep
        if e.key() == Qt.Key.Key_F:
            self.glWidget.arm1X -= angleStep

        if e.key() == Qt.Key.Key_T:
            self.glWidget.arm2X += angleStep
        if e.key() == Qt.Key.Key_G:
            self.glWidget.arm2X -= angleStep
        
        if e.key() == Qt.Key.Key_Z:
            self.glWidget.handX += angleStep
        if e.key() == Qt.Key.Key_C:
            self.glWidget.handX -= angleStep


        self.glWidget.update()

def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('Robot Arm')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)


