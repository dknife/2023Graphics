from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *
import math
import numpy as np

TEXSIZE = 64
def createTexture() :
    return np.random.rand( TEXSIZE, TEXSIZE, 3 )

def SetupTexture(texImage):
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, TEXSIZE, TEXSIZE, 0, GL_RGB, GL_FLOAT, texImage)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glEnable(GL_TEXTURE_2D)



def drawPlane() :   
    
    glColor3f(1,1,0)
    glBegin(GL_QUADS)
    glTexCoord2f(0,0)
    glVertex3f(-1, 0, -1)
    glTexCoord2f(0,1)
    glVertex3f(-1, 0,  1)
    glTexCoord2f(1,1)
    glVertex3f( 1, 0,  1)
    glTexCoord2f(1,0)
    glVertex3f( 1, 0, -1)
    glEnd()



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
        myTexture = createTexture()
        SetupTexture(myTexture)

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

        drawPlane()


class MyWindow(QMainWindow):
    def __init__(self, title=''):
        super().__init__()
        self.setWindowTitle(title)
        ## OpenGL Widget 달기
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

    def keyPressEvent(self, e):
        step = np.array([0.01])

        if e.key() == Qt.Key.Key_W:
            self.glWidget.cam += step * self.glWidget.camDir
            self.glWidget.target = self.glWidget.cam + self.glWidget.camDir
            self.glWidget.update()
        elif e.key() == Qt.Key.Key_S:
            self.glWidget.cam -= step * self.glWidget.camDir
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