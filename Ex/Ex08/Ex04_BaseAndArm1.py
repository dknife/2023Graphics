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


def drawCube(color = [1, 1, 1]):
    v0 = [-0.5, 0.5, 0.5]
    v1 = [ 0.5, 0.5, 0.5]
    v2 = [ 0.5, 0.5,-0.5]
    v3 = [-0.5, 0.5,-0.5]
    v4 = [-0.5,-0.5, 0.5]
    v5 = [ 0.5,-0.5, 0.5]
    v6 = [ 0.5,-0.5,-0.5]
    v7 = [-0.5,-0.5,-0.5]
    glBegin(GL_LINES)
    glVertex3fv(v0); glVertex3fv(v1)
    glVertex3fv(v1); glVertex3fv(v2)
    glVertex3fv(v2); glVertex3fv(v3)
    glVertex3fv(v3); glVertex3fv(v0)
    glVertex3fv(v4); glVertex3fv(v5)
    glVertex3fv(v5); glVertex3fv(v6)
    glVertex3fv(v6); glVertex3fv(v7)
    glVertex3fv(v7); glVertex3fv(v4)
    glVertex3fv(v0); glVertex3fv(v4)
    glVertex3fv(v1); glVertex3fv(v5)
    glVertex3fv(v2); glVertex3fv(v6)
    glVertex3fv(v3); glVertex3fv(v7)
    glEnd()
    drawAxes()

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
                glVertex3f(startX, -0.05, startZ)
                glVertex3f(startX, -0.05, startZ+d)
                glVertex3f(startX+d, -0.05, startZ+d)
                glVertex3f(startX+d, -0.05, startZ)
    glEnd()


class MyGLWidget(QOpenGLWidget):
    def __init__(self) :
        super().__init__()
        self.basePosition = [0, 0, 0]
        self.arm1Y = 0.
        self.arm1X = 0.

    def initializeGL(self):
        glClearColor(0.0, 0.5, 0.5, 1.0)
        self.planeList = glGenLists(1)
        glNewList(self.planeList, GL_COMPILE)
        drawPlane()
        glEndList()

        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        gluPerspective(60, w/h, 0.1, 500)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 2, 6, 0, 0, -3, 0, 1, 0)

        glCallList(self.planeList)
        drawAxes()

        glTranslatef(self.basePosition[0], self.basePosition[1], self.basePosition[2])
        glTranslatef(0, 0.5, 0)
        glPushMatrix()
        glScalef(3, 1, 3)
        drawCube()
        glPopMatrix()

        # base의 두께 반을 빠져 나온다
        glTranslatef(0, 0.5, 0)
        # 중심이 관절 위치에 놓였음 - 회전 실시
        glRotatef(self.arm1Y, 0, 1, 0)
        glRotatef(self.arm1X, 1, 0, 0)
        # 팔의 아래 끝이 관절위치에 놓이도록 팔의 1/2 높이를 빠져나옴
        glTranslatef(0, 1, 0)
        glPushMatrix()
        glScalef(0.5, 2, 0.5)
        drawCube()
        glPopMatrix()

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
        


        self.glWidget.update()

def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('Robot Arm')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)


