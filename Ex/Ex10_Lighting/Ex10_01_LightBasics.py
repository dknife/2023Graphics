from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import *

import math
import numpy as np

mat_spec = [1, 1, 1, 1]
mat_diff = [0, 1, 1, 1]
mat_ambi = [1, 1, 1, 1]
mat_shin = [120]

lit_spec = [1, 1, 1, 1]
lit_diff = [1, 1, 1, 1]
lit_ambi = [0, 0, 0, 1]

light_pos = [1, 1, 1, 0]

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



class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
       
        self.angle = 0
   
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)

        glEnable(GL_DEPTH_TEST)
        LightSet()


    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.01, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        LightPositioning()
        gluLookAt(0,7,10, 0,2,0, 0,1,0)

        P0 = np.array([0,5,0])
        P1 = np.array([-3,1,3])
        P2 = np.array([ 3,1,3])
        P3 = np.array([ 0,1,-3])
        
        glRotatef(self.angle, 0.1, 1, 0.3)
        self.angle += 1

        N = np.array([0, 1, 0])
        glBegin(GL_TRIANGLES)
        glNormal3fv(N)
        glVertex3fv(P0)
        glVertex3fv(P1)  
        glVertex3fv(P2)

        glVertex3fv(P0)
        glVertex3fv(P2) 
        glVertex3fv(P3)

        glVertex3fv(P0)
        glVertex3fv(P3) 
        glVertex3fv(P1)
        glEnd()
       


class MyWindow(QMainWindow):
    def __init__(self, title=''):
        QMainWindow.__init__(self)
        self.setWindowTitle(title)
        self.glWidget = MyGLWidget()
        self.setCentralWidget(self.glWidget)

    def keyPressEvent(self, e):        
        self.glWidget.update()

def main(argv = []):
    app = QApplication(argv)
    window = MyWindow('조명의 이해 - 단순 컬러')
    window.setFixedSize(1200, 600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)