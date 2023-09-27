from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt6.QtWidgets import *
from PyQt6.QtOpenGLWidgets import *

class MyGLWidget(QOpenGLWidget) :
    def __init__(self):
        super().__init__()

    def initializeGL(self) :
        pass

    def resizeGL(self, w, h):
        pass

    def paintGL(self):
        pass

class MyWindow(QMainWindow):
    def __init__(self, title='OpenGL'):
        super().__init__()
        self.setWindowTitle(title)

        ### GUI 정의
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        ## 중심 위짓이 가질 레이아웃 지정
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # 두 개의 GL 위짓을 생성하고,
        # 이 두 위짓 객체를 각각 이 클래스의 멤버로 저장
        self.glWidget1 = MyGLWidget()
        self.glWidget2 = MyGLWidget()

        layout.addWidget(self.glWidget1)
        layout.addWidget(self.glWidget2)


def main(argv = sys.argv):
    app = QApplication(argv)
    window = MyWindow('Two OpenGL Widgets')
    window.setFixedSize(1200,600)
    window.show()
    app.exec()

if __name__ == '__main__':
    main(sys.argv)







