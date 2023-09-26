from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
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
        glVertex3f(x, y, angle/10)
    glEnd()

def drawBox(l, r, b, t, n, f): # glOrtho가 만드는 공간(육면체)을 가시화
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    # 앞면
    glVertex3f(l,t,n)
    glVertex3f(l,b,n)
    glVertex3f(r,b,n)
    glVertex3f(r,t,n)
    glEnd()
    
    glBegin(GL_LINE_LOOP)
    # 뒷면
    glVertex3f(l,t,f)
    glVertex3f(l,b,f)
    glVertex3f(r,b,f)
    glVertex3f(r,t,f)
    glEnd()

class MyGLWidget(QOpenGLWidget):
    def __init__(self, observation = False):
        super().__init__()
        self.observation = observation

        self.left = self.bottom = self.near = -2
        self.right = self.top = self.far = 2

    def initializeGL(self):
        pass

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.observation:
            glOrtho(-4, 4, -4, 4, -100, 100)
        else:
            glOrtho(self.left, self.right, self.bottom, self.top, self.near, self.far)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if self.observation:
            gluLookAt(1, 0.7, 0.5, 0, 0, 0, 0, 1, 0)
        drawAxes()
        drawHelix()
        drawBox(self.left, self.right, self.bottom, self.top, self.near, self.far)
        

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




def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('glOrtho 관측')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)