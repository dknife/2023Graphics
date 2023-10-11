from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *
import numpy as np
import math

def drawPlane() :
    n = 500 # 체스 판을 구성하는 한 면에 놓일 정점의 수
    w = 100 # 체스 판의 한쪽 면 길이
    d = w/(n-1) # 인접한 두 정점 사이의 거리
    # 체스판을 그린다
    glBegin(GL_QUADS)
    for i in range(n):
        for j in range(n):
            startX = -w/2 + i*d
            startZ = -w/2 + j*d
            # 행과 열의 번호 합이 짝수일 때만 그린다 (체스판)
            if (i+j)%2 == 0:
                glVertex3f(startX, 0, startZ)
                glVertex3f(startX, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ+d)
                glVertex3f(startX+d, 0, startZ)
    glEnd()

def drawPlane_vertexBuffer():
    n = 500 # 체스 판을 구성하는 한 면에 놓일 정점의 수
    w = 100 # 체스 판의 한쪽 면 길이
    d = w/(n-1) # 인접한 두 정점 사이의 거리
    
    # 버퍼를 준비한다.
    vertexBuffer = []

    for i in range(n):
        for j in range(n):
            startX = -w/2 + i*d
            startZ = -w/2 + j*d
            # 행과 열의 번호 합이 짝수일 때만 그린다 (체스판)
            if (i+j)%2 == 0:
                vertexBuffer.append([startX, 0.3, startZ])
                vertexBuffer.append([startX, 0.3, startZ+d])
                vertexBuffer.append([startX+d, 0.3, startZ+d])
                vertexBuffer.append([startX+d, 0.3, startZ])

    return vertexBuffer

class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 멤버 변수를 선언한다
        # 카메라의 위치
        self.cam = np.array([0, 0, 0], dtype = float)
        self.camDir = np.array([0, 0, 1], dtype = float)  
        self.target = self.cam + self.camDir  
        self.angle = 0.0

    def initializeGL(self):

        ### Display List 정의 ---        
        self.myDisplayList = glGenLists(1)
        glNewList(self.myDisplayList, GL_COMPILE)
        # 리스트에 들어갈 그리기 내용
        drawPlane()
        glEndList()

        #### DrawArrays를 위한 버퍼 준비
        self.myBuffer = drawPlane_vertexBuffer()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.myBuffer)

    def paintGL(self):  
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 2, 0.2, 100)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt( self.cam[0], self.cam[1] + 0.6, self.cam[2], # 카메라 위치
                   self.target[0], self.target[1], self.target[2], # 카메라가 쳐다보는 지점
                   0, 1, 0  # 카메라 위쪽 방향
        )

        #drawPlane()
        glColor3f(0, 0, 1)
        glCallList(self.myDisplayList)

        glColor3f(0, 1, 1)
        glDrawArrays(GL_QUADS, 0, len(self.myBuffer))


class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()
        self.setWindowTitle(title)
        ## OpenGL Widget 달기
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

    def keyPressEvent(self, e):
        step = np.array([0.05])
        angleStep = 0.05

        if e.key() == Qt.Key.Key_W:
            self.glWidget.cam += step * self.glWidget.camDir
            self.glWidget.target = self.glWidget.cam + self.glWidget.camDir
            self.glWidget.update()
        elif e.key() == Qt.Key.Key_S:
            self.glWidget.cam -= step * self.glWidget.camDir
            self.glWidget.target = self.glWidget.cam + self.glWidget.camDir
            self.glWidget.update()
        elif e.key() == Qt.Key.Key_A:
            self.glWidget.angle -= angleStep
            A = self.glWidget.angle
            self.glWidget.camDir = np.array([ math.sin(A), 0.0, -math.cos(A)])
            self.glWidget.target = self.glWidget.cam + self.glWidget.camDir
            self.glWidget.update()
        elif e.key() == Qt.Key.Key_D:
            self.glWidget.angle += angleStep
            A = self.glWidget.angle
            self.glWidget.camDir = np.array([ math.sin(A), 0.0, -math.cos(A)])
            self.glWidget.target = self.glWidget.cam + self.glWidget.camDir
            self.glWidget.update()




        
def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('FPS 스타일 카메라 제어')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__' :
    main(sys.argv)