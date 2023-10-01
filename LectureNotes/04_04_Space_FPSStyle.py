from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

import math # 삼각함수를 사용하기 위해 임포트
import numpy as np # 벡터 연산을 위한 넘파이 임포트

def drawPlane():
    glColor3f(0,0,1)
    glBegin(GL_LINES)
    for i in range(100):
        glVertex3f(i-50, 0,  -50)
        glVertex3f(i-50, 0,   50)
        glVertex3f( -50, 0, i-50)
        glVertex3f(  50, 0, i-50)
    glEnd()


class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #  카메라의 위치 p와 방향 d
        self.p = np.array([0.0, 0.0, 0.0])
        self.d = np.array([0.0, 0.0, 1.0])
        self.angle = 0.0

    def initializeGL(self): 
        glClearColor(0.5, 1.0, 1.0, 1.0)

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 10)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        target = self.p + self.d # 넘파이 배열은 벡터 덧셈 가능
        gluLookAt(
            self.p[0], self.p[1] + 0.3, self.p[2],  # 카메라 위치
            target[0], target[1], target[2],  # 카메라 시선 목표지점
            0, 1, 0                           # 카메라 상향벡터 (y축)    
        )

        drawPlane()
        glFlush()

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()
        self.setWindowTitle(title)
        ## OpenGL Widget 달기
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

    def keyPressEvent(self, e):
        small_step = np.array([0.1])
        angle_step = 0.05
        if e.key() == Qt.Key.Key_W:
            self.glWidget.p += small_step * self.glWidget.d
        if e.key() == Qt.Key.Key_S:
            self.glWidget.p -= small_step * self.glWidget.d
        if e.key() == Qt.Key.Key_A:
            self.glWidget.angle += angle_step
            dir = [math.sin(self.glWidget.angle), 
                   0, 
                   math.cos(self.glWidget.angle)]
            self.glWidget.d = np.array( dir )
        if e.key() == Qt.Key.Key_D:
            self.glWidget.angle -= angle_step
            dir = [math.sin(self.glWidget.angle), 
                   0, 
                   math.cos(self.glWidget.angle)]
            self.glWidget.d = np.array( dir )

        self.glWidget.update()

        
def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('FPS 스타일 카메라 제어')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__' :
    main(sys.argv)