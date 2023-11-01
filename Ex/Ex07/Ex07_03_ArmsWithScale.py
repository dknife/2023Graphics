from OpenGL.GL import *
from OpenGL.GLU import *

import sys
import numpy as np

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

def drawCube(color = [1, 1, 1]):
    v0 = [-0.5, 0.5, 0.5]
    v1 = [ 0.5, 0.5, 0.5]
    v2 = [ 0.5, 0.5,-0.5]
    v3 = [-0.5, 0.5,-0.5]
    v4 = [-0.5,-0.5, 0.5]
    v5 = [ 0.5,-0.5, 0.5]
    v6 = [ 0.5,-0.5,-0.5]
    v7 = [-0.5,-0.5,-0.5]
    glColor3fv(color)
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

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def initializeGL(self):
        # OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화
        glClearColor(0.0, 0.0, 0.0, 1.0)  

       
    def resizeGL(self, width, height):
        # 카메라의 투영 특성을 여기서 설정
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 100)

    def paintGL(self):
 
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()       
        gluLookAt(1,1.5, 7, 0,1.0,0, 0,1,0)

        glLineWidth(5)
        drawAxes()
        glLineWidth(1)
        
        glTranslatef(0.0, 1.0, 0.0)   
        glPushMatrix()    
        glScalef(1.0, 2.0, 1.0)        
        drawCube(color=[1, 1, 0])
        glPopMatrix()

        glTranslatef(0, 1, 0)
        glRotatef(45, 0, 0, 1)
        glTranslatef(0, 1, 0)
        glPushMatrix()      
        glScalef(1.0, 2.0, 1.0) 
        drawCube(color=[0, 1, 1])
        glPopMatrix()
        
        

class MyWindow(QMainWindow):

    def __init__(self, title=''):
        QMainWindow.__init__(self)  # QMainWindow 슈퍼 클래스의 초기화
        self.setWindowTitle(title)

        self.glWidget = MyGLWidget()  # OpenGL Widget
        self.setCentralWidget(self.glWidget)


def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('transform')
    window.setFixedSize(600, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)