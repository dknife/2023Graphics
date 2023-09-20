from OpenGL.GL import *
from OpenGL.GLU import *

import math

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import sys

### 나의 첫번째 오픈지엘 윈도우
class MyGLWindow(QOpenGLWidget) :
    def __init__(self):
        super().__init__()

    #### 다음 세 기본 콜백은 이름을 바꿀 수 없다.
    def initializeGL(self):
        glClearColor(0.0, 1.0, 1.0, 1.0)

    def resizeGL(self, w, h):
        pass

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_POLYGON)
        # 원 그리기!

        for i in range(0, 360, 15):
            angle = 2*3.141592*i/360.0
            print(angle)
            glVertex2f(math.cos(angle)+0.2, math.sin(angle)+0.2)
        glEnd()



def main(argv = []):
    app = QApplication(argv)
    window = MyGLWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)

