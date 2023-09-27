from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import *

import math

def drawHelix(): ## 나선을 그리는 함수
    glColor3f(1, 1, 1)

    glBegin(GL_LINE_STRIP)
    for i in range(1000):
        angle = i/10
        x, y = math.cos(angle), math.sin(angle)
        z = angle/10
        glVertex3f(x,y,z)
    glEnd()


def drawAxes():  ## 축을 그리는 함수
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

class MyGLWidget(QOpenGLWidget) :
    
    def __init__(self, observation = False):
        super().__init__()
        self.observation = observation

    def initializeGL(self) :
        pass

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.observation == True:
            glOrtho(-2, 2, -2, 2, -2, 2)
        else:
            glOrtho(-1, 1, -1, 1, -1, 1)

    def paintGL(self):
        drawAxes()
        drawHelix()

class MyWindow(QMainWindow):
    def __init__(self, title='OpenGL'):
        super().__init__()
        self.setWindowTitle(title)

        ### GUI 정의
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        ## 중심 위짓이 가질 레이아웃 지정
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # 두 개의 GL 위짓을 생성하고,
        # 이 두 위짓 객체를 각각 이 클래스의 멤버로 저장
        self.glWidget1 = MyGLWidget()
        self.glWidget2 = MyGLWidget(observation = True)

        layout.addWidget(self.glWidget1)
        layout.addWidget(self.glWidget2)


def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('Two OpenGL Widgets')
    window.setFixedSize(1200,600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)








