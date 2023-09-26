from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *
import math

def drawAxes():
    glBegin(GL_LINES)
    glColor3f(1,0,0) # red x axis
    glVertex3f(0,0,0); glVertex3f(1,0,0)
    glColor3f(0,1,0) # green y axis
    glVertex3f(0,0,0); glVertex3f(0,1,0)
    glColor3f(0,0,1) # blue z axis
    glVertex3f(0,0,0); glVertex3f(0,0,1)
    glEnd()


def drawHelix():
    glColor3f(1,1,1)
    glBegin(GL_LINE_STRIP)
    for i in range(1000):
        angle = i/10
        x, y = math.cos(angle), math.sin(angle)
        glVertex3f(x, y, -angle/10)
    glEnd()

def drawFrustum(l, r, b, t, n, f):
    # 뒷면의 좌우하상 좌표를 구하자
    L = l * (f/n)
    R = r * (f/n)
    B = b * (f/n)
    T = t * (f/n)
    # 절두체의 앞면을 그리기
    glColor3f(1,1,1)
    glBegin(GL_LINE_LOOP)
    glVertex3f(l,t,-n)    
    glVertex3f(l,b,-n)
    glVertex3f(r,b,-n)
    glVertex3f(r,t,-n)    
    glEnd()
    # 절두체 뒷면 그리기
    glBegin(GL_LINE_LOOP)
    glVertex(L,T,-f)
    glVertex(L,B,-f)
    glVertex(R,B,-f)
    glVertex(R,T,-f)
    glEnd()
    # 앞뒷면 연결
    glBegin(GL_LINES)
    glVertex3f(l,t,-n) 
    glVertex3f(L,T,-f)   
    glVertex3f(l,b,-n)
    glVertex3f(L,B,-f)
    glVertex3f(r,b,-n)
    glVertex3f(R,B,-f)
    glVertex3f(r,t,-n)
    glVertex3f(R,T,-f)    
    glEnd()


class MyGLWidget(QOpenGLWidget):
    left = bottom = -2
    near = 0.5  ### 원근 투영에서는 반드시 near가 양수
    right = top = far = 2

    def __init__(self, parent=None, observation = False):
        super().__init__(parent)
        self.observation = observation

    def initializeGL(self):
        pass

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.observation:
            glOrtho(-4, 4, -4, 4, -100, 100)
        else:
            glFrustum(self.left, self.right, self.bottom, self.top, self.near, self.far)

    def paintGL(self):
        
        self.projection_update()

        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.observation:
            gluLookAt(
                1.5, 1.0, 0.2, # 눈의 위치
                0, 0, 0, # 쳐다보는 목표 지점 위치
                0, 1, 0  # 카메라의 상향 벡터
            )

        drawAxes()
        drawHelix()
        drawFrustum(self.left, self.right, self.bottom, self.top, self.near, self.far)

    def projection_update(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.observation:
            glOrtho(-4, 4, -4, 4, -100, 100)
        else:
            glFrustum(self.left, self.right, self.bottom, self.top, self.near, self.far)
        

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()
        self.setWindowTitle(title)

        ## GUI 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        gui_layout = QHBoxLayout()

        central_widget.setLayout(gui_layout)

        self.glWidget1 = MyGLWidget()
        self.glWidget2 = MyGLWidget(observation = True) # 관측용 OpenGL 위짓

        gui_layout.addWidget(self.glWidget1)     
        gui_layout.addWidget(self.glWidget2)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key.Key_A:
            MyGLWidget.left -= 0.1
        elif e.key() == Qt.Key.Key_S:
            MyGLWidget.left += 0.1
        elif e.key() == Qt.Key.Key_D:
            MyGLWidget.right -= 0.1
        elif e.key() == Qt.Key.Key_F:
            MyGLWidget.right += 0.1
        elif e.key() == Qt.Key.Key_Q:
            MyGLWidget.top += 0.1
        elif e.key() == Qt.Key.Key_W:
            MyGLWidget.top -= 0.1
        elif e.key() == Qt.Key.Key_Z:
            MyGLWidget.near += 0.1
        elif e.key() == Qt.Key.Key_X:
            MyGLWidget.near -= 0.1
        elif e.key() == Qt.Key.Key_V:
            MyGLWidget.far += 0.1
        elif e.key() == Qt.Key.Key_C:
            MyGLWidget.far -= 0.1
            
        self.glWidget1.update()
        self.glWidget2.update()


def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('glOrtho 관측')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)