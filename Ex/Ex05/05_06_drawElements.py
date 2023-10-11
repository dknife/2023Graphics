from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *



class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
       
       

    def initializeGL(self):
        # OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화
        glClearColor(0.0, 0.0, 0.0, 1.0)  

        self.vertexBuffer = [ [0.0, 1.0, 0.0], 
                             [-0.5, 0.0, 0.0], 
                             [0.5, 0.0, 0.0] ,
                             [-1.0, -1.0, 0.0], 
                             [0.0, -1.0, 0.0], 
                             [1.0, -1.0, 0.0] ]
        
        self.indexBuffer = [ 0, 1, 2, 1, 3, 4, 2, 4, 5]

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertexBuffer)
       
       
       
    def resizeGL(self, width, height):
        # 카메라의 투영 특성을 여기서 설정
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 100)

    def paintGL(self):
 
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
       
        gluLookAt(0,0,-3, 0,0,0, 0,1,0)

        glColor3f(0, 0, 1)
        glPointSize(10)
        glBegin(GL_POINTS)
        for i in range(len(self.vertexBuffer)) :
            glVertex3fv(self.vertexBuffer[i])            
        glEnd()

        glColor3f(1, 0, 1)
        glDrawElements(GL_TRIANGLES, 9, GL_UNSIGNED_INT, self.indexBuffer)


class MyWindow(QMainWindow):

    def __init__(self, title=''):
        QMainWindow.__init__(self)  # QMainWindow 슈퍼 클래스의 초기화
        self.setWindowTitle(title)

        self.glWidget = MyGLWidget()  # OpenGL Widget
        self.setCentralWidget(self.glWidget)
   
def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('glDrawElements')
    window.setFixedSize(600, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)
