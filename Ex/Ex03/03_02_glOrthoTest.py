from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import *
import sys

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

class MyGLWindow(QOpenGLWidget):
    def __init__(self): # 생성자
        super().__init__()
        self.setWindowTitle('glortho 연습')

    def initializeGL(self) :
        pass

    def resizeGL(self, w:int, h:int):

        aspR = w/h
        range = 1
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        glOrtho(-range*aspR, range*aspR, 
                -range, range, -range, range)

    def paintGL(self):
        glBegin(GL_POLYGON)
        glVertex3f(1,0,0)
        glVertex3f(0,1,0)
        glVertex3f(-1,0,0)
        glVertex3f(0,-1,0)
        glEnd()
        drawAxes()

def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyGLWindow()
    window.show()

    app.exec()

if __name__ == '__main__':
    main(sys.argv)
