from OpenGL.GL import *
from OpenGL.GLU import *

import sys
import numpy as np

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

class MeshLoader :
    def __init__(self):
        self.nV = 0 # 정점의 개수
        self.nF = 0 # 면의 개수
        self.vBuffer = None # 정점 버퍼
        self.iBuffer = None # 면을 표현하는 인덱스 버퍼

    def loadMesh(self, filename) :
        with open(filename, 'rt') as inputfile:
            # with 구문의 내부 블럭 시작
            self.nV = int(next(inputfile))
            self.vBuffer = np.zeros((self.nV*3, ), dtype=float)
            for i in range(self.nV):
                verts = next(inputfile).split()
                self.vBuffer[i*3: i*3+3] = verts
                print(verts)
                print(self.vBuffer[i*3: i*3+3])
            # with 구문의 내부 블럭 끝

    def draw(self):
        pass


class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
       

    def initializeGL(self):
        # OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화
        glClearColor(0.0, 1.0, 0.0, 1.0)  

        self.myLoader = MeshLoader()
        self.myLoader.loadMesh("./Ex06_Meshes/mesh.txt")

       
       
       
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

        


class MyWindow(QMainWindow):

    def __init__(self, title=''):
        QMainWindow.__init__(self)  # QMainWindow 슈퍼 클래스의 초기화
        self.setWindowTitle(title)

        self.glWidget = MyGLWidget()  # OpenGL Widget
        self.setCentralWidget(self.glWidget)
   
def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('Mesh Visualization')
    window.setFixedSize(600, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)