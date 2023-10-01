from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

def drawPlane():
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

    def paintGL(self):
        drawPlane()
        glFlush()

class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()
        self.setWindowTitle(title)
        ## OpenGL Widget 달기
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)
        
def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('FPS 스타일 카메라 제어')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__' :
    main(sys.argv)