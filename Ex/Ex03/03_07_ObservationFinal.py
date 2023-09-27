import typing
from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtCore import *

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

def drawBox(l, r, b, t, n, f):
    # 앞면 그리기
    glBegin(GL_LINE_LOOP)
    glVertex3f(l,t, -n)
    glVertex3f(l,b, -n)
    glVertex3f(r,b, -n)
    glVertex3f(r,t, -n)
    glEnd()

    # 뒷면 그리기
    glBegin(GL_LINE_LOOP)
    glVertex3f(l,t, -f)
    glVertex3f(l,b, -f)
    glVertex3f(r,b, -f)
    glVertex3f(r,t, -f)
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
    
    left = bottom = near = -2.0
    right = top = far = 2.0

    def __init__(self, observation = False):
        super().__init__()
        self.observation = observation

    def initializeGL(self) :
        pass

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.observation == True:
            glOrtho(self.left*2, self.right*2, self.bottom*2, self.top*2, -100, 100)
        else:
            glOrtho(self.left, self.right, self.bottom, self.top, self.near, self.far)

    def paintGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.observation == True:
            glOrtho(-4, 4, -4, 4, -100, 100)
        else:
            glOrtho(self.left, self.right, self.bottom, self.top, self.near, self.far)


        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if self.observation == True:
            gluLookAt(1, 0.5, 0.5, 0, 0, 0, 0, 1, 0)
        drawAxes()
        drawHelix()
        drawBox(self.left, self.right, self.bottom, self.top, self.near, self.far)

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

    def keyPressEvent(self, e):
        # from PyQt6.QtCore import *
        if e.key() == Qt.Key.Key_A:
            MyGLWidget.left -= 0.1
        elif e.key() == Qt.Key.Key_S:
            MyGLWidget.left += 0.1
        elif e.key() == Qt.Key.Key_D:
            MyGLWidget.right -= 0.1
        elif e.key() == Qt.Key.Key_F:
            MyGLWidget.right += 0.1
        elif e.key() == Qt.Key.Key_Z:
            MyGLWidget.near -= 0.1
        elif e.key() == Qt.Key.Key_X:
            MyGLWidget.near += 0.1

        self.glWidget1.update()
        self.glWidget2.update()





def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('Two OpenGL Widgets')
    window.setFixedSize(1200,600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)








