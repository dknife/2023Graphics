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

            self.nF = int(next(inputfile))
            self.iBuffer = np.zeros((self.nF*3, ), dtype=int)
            for i in range(self.nF):
                idx = next(inputfile).split() # idx[0]: 면을 구성하는 점의 개수
                # 필요한 정보는 idx[1], idx[2], idx[3] = idx[1:4]
                self.iBuffer[i*3: i*3+3] = idx[1:4]

            # with 구문의 내부 블럭 끝

    def draw(self):
        glPointSize(5)
        
        
        glBegin(GL_TRIANGLES)
        for i in range(self.nF):            
            # 각 면을 그린다.
            # 각 면을 구성하는 정점의 번호는 
            v = self.iBuffer[i*3: i*3+3]
            # 각 정점은 v[0], v[1], v[2]
            # 첫 점은 v[0]의 번호를 가진 정점을 vBuffer에서 찾는다
            glColor3fv( (self.vBuffer[v[0]*3: v[0]*3+3] + np.array([1])) / 2.0)
            glVertex3fv(self.vBuffer[v[0]*3: v[0]*3+3])
            # 두번째 점은 v[1]의 번호를 가진 정점을 vBuffer에서 찾는다
            glColor3fv( (self.vBuffer[v[1]*3: v[1]*3+3] + np.array([1])) / 2.0)            
            glVertex3fv(self.vBuffer[v[1]*3: v[1]*3+3])
            # 세번째 점은 v[2]의 번호를 가진 정점을 vBuffer에서 찾는다
            glColor3fv( (self.vBuffer[v[2]*3: v[2]*3+3] + np.array([1])) / 2.0)  
            glVertex3fv(self.vBuffer[v[2]*3: v[2]*3+3])        
        glEnd()

        glColor3f(0,0,1)
        for i in range(self.nF):
            glBegin(GL_LINE_LOOP)
            # 각 면을 그린다.
            # 각 면을 구성하는 정점의 번호는 
            v = self.iBuffer[i*3: i*3+3]
            # 각 정점은 v[0], v[1], v[2]
            # 첫 점은 v[0]의 번호를 가진 정점을 vBuffer에서 찾는다
            glVertex3fv(self.vBuffer[v[0]*3: v[0]*3+3])
            # 두번째 점은 v[1]의 번호를 가진 정점을 vBuffer에서 찾는다
            glVertex3fv(self.vBuffer[v[1]*3: v[1]*3+3])
            # 세번째 점은 v[2]의 번호를 가진 정점을 vBuffer에서 찾는다
            glVertex3fv(self.vBuffer[v[2]*3: v[2]*3+3])
            glEnd()


class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
       

    def initializeGL(self):
        # OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화
        glClearColor(0.0, 0.0, 0.0, 1.0)  

        self.myLoader = MeshLoader()
        self.myLoader.loadMesh("D:\\ymkang\\2023Graphics\\Ex\\Ex06_Meshes\\cow.txt")
        self.angle = 0
       
    def resizeGL(self, width, height):
        # 카메라의 투영 특성을 여기서 설정
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 100)

    def paintGL(self):
 
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()       
        gluLookAt(0,2,6, 0,1,0, 0,1,0)

        glRotatef(self.angle, 0, 1, 0)
        self.myLoader.draw()
        self.angle += 1.0

        


class MyWindow(QMainWindow):

    def __init__(self, title=''):
        QMainWindow.__init__(self)  # QMainWindow 슈퍼 클래스의 초기화
        self.setWindowTitle(title)

        self.glWidget = MyGLWidget()  # OpenGL Widget
        self.setCentralWidget(self.glWidget)

        self.timer = QTimer(self)
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

    def timeout(self):
        self.glWidget.update()
   
def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('Mesh Visualization')
    window.setFixedSize(600, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)