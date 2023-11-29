from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

import math
import numpy as np

class MeshLoader :
    def __init__(self):
        self.nV = 0 # 정점의 개수
        self.nF = 0 # 면의 개수
        self.vBuffer = None # 정점 버퍼
        self.iBuffer = None # 면을 표현하는 인덱스 버퍼
    def make_display_list(self):  
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        self.draw()
        glEndList()

    def draw_display_list(self):
        glCallList(self.list)

    def loadMesh(self, filename, reverseNormal = False) :
        with open(filename, 'rt') as inputfile:
            # with 구문의 내부 블럭 시작
            self.nV = int(next(inputfile))
            self.vBuffer = np.zeros((self.nV*3, ), dtype=float)
            for i in range(self.nV):
                verts = next(inputfile).split()
                self.vBuffer[i*3: i*3+3] = verts[0:3]

            coordMin = self.vBuffer.min()
            coordMax = self.vBuffer.max()
            scale = max([coordMin, coordMax], key=abs)
            self.vBuffer /= scale

            self.nF = int(next(inputfile))
            self.iBuffer = np.zeros((self.nF*3, ), dtype=int)
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            self.nBuffer = np.zeros((self.nV*3, ), dtype=float)
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            for i in range(self.nF):
                idx = next(inputfile).split() # idx[0]: 면을 구성하는 점의 개수
                # 필요한 정보는 idx[1], idx[2], idx[3] = idx[1:4]
                self.iBuffer[i*3: i*3+3] = idx[1:4]
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                index = self.iBuffer[i*3: i*3+3]
                p0 = self.vBuffer[index[0]*3: index[0]*3+3]
                p1 = self.vBuffer[index[1]*3: index[1]*3+3]
                p2 = self.vBuffer[index[2]*3: index[2]*3+3]
                u = p1 - p0
                v = p2 - p0
                if reverseNormal:
                    N = -np.cross(u, v)
                else :
                    N = np.cross(u,v)

                self.nBuffer[index[0]*3:index[0]*3+3] += N
                self.nBuffer[index[1]*3:index[1]*3+3] += N
                self.nBuffer[index[2]*3:index[2]*3+3] += N

            for i in range(self.nV) :
                N = self.nBuffer[i*3: i*3+3]
                N = N / np.linalg.norm(N)
                self.nBuffer[i*3: i*3+3] = N
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # with 구문의 내부 블럭 끝

        self.make_display_list() ####################################################

    def draw(self):
        
        glBegin(GL_TRIANGLES)
        for i in range(self.nF):            
            # 각 면을 그린다.
            # 각 면을 구성하는 정점의 번호는 
            v = self.iBuffer[i*3: i*3+3]

## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            N = self.nBuffer[i*3: i*3+3]

            glNormal3fv(self.nBuffer[v[0]*3: v[0]*3+3])
            glVertex3fv(self.vBuffer[v[0]*3: v[0]*3+3])
            glNormal3fv(self.nBuffer[v[1]*3: v[1]*3+3])
            glVertex3fv(self.vBuffer[v[1]*3: v[1]*3+3])
            glNormal3fv(self.nBuffer[v[2]*3: v[2]*3+3])
            glVertex3fv(self.vBuffer[v[2]*3: v[2]*3+3])        
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        glEnd()

## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
mat_spec = [1, 0, 0, 1]
mat_diff = [0.5, 0.5, 0, 1]
mat_ambi = [0, 0, 0, 1]
mat_shin = [120]

lit_spec = [1, 1, 1, 1]
lit_diff = [1, 1, 1, 1]
lit_ambi = [0, 0, 0, 1]

light_pos = [1, 2, 1, 0]

def LightSet():
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_spec)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diff)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambi)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shin)

    glLightfv(GL_LIGHT0, GL_SPECULAR, lit_spec)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lit_diff)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lit_ambi)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

def LightPositioning() :
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
       

    def initializeGL(self):
        # OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화
        glClearColor(0.0, 0.0, 0.0, 1.0)  
        glEnable(GL_DEPTH_TEST)

        self.myLoader = MeshLoader()
        self.myLoader.loadMesh("./Lab11_Lights/sphere.txt", reverseNormal=True)
        self.angle = 0
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        LightSet()
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#        
    def resizeGL(self, width, height):
        # 카메라의 투영 특성을 여기서 설정
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 100)

    def paintGL(self):
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()       

        gluLookAt(0,15,50, 0,0,0, 0,1,0)
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        LightPositioning()
## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        for x in range(-50, 50, 2):
            for z in range(-50, 50, 2):
                glPushMatrix()
                glTranslatef(x, 0, z)
                self.myLoader.draw_display_list()
                glPopMatrix()
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
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)
