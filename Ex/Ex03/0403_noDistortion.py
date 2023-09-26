from OpenGL.GL import *
from OpenGL.GLU import *

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import sys

def drawAxes():
    
    glLineWidth(5)

    glBegin(GL_LINES)
    # x축 (0,0,0) - (1,0,0)
    glColor(1, 0, 0) # 빨간색
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    # y축
    glColor(0, 1, 0) # 녹색
    glVertex3f(0,0,0)
    glVertex3f(0,1,0)
    # z축
    glColor(0, 0, 1) # 파란색
    glVertex3f(0,0,0)
    glVertex3f(0,0,1)
    glEnd()

#### MyWindow 클래스의 시작 ############################
class MyGLWindow(QOpenGLWidget) : # QOpenGLWidget 상속

    def __init__(self):  
        super().__init__()  # 슈퍼클래스 QMainWindow 생성자 실행

        self.setWindowTitle('glOrtho 연습')

    def initializeGL(self) :
        glClearColor(0.1, 0.7, 0.3, 1.0)
    
    def resizeGL(self, w: int, h: int) :

        aspRatio = w / h # 종횡비를 계산한다.
        range = 2
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-range*aspRatio, range*aspRatio, -range, range, -range, range)
        
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        glBegin(GL_POLYGON)
        glColor3f(1, 1, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(0, 1, 0)
        glVertex3f(-1, 0, 0)
        glVertex3f( 0, -1, 0)
        glEnd()

        drawAxes()

#### MyGLWindow 클래스의 끝 ############################

def main(argv = sys.argv) :
    ## 윈도우 생성하기
    app = QApplication(argv)
    window = MyGLWindow()
    window.show()

    app.exec()


if __name__ == '__main__' :
    main(sys.argv)