### OpenGL ###################
from OpenGL.GL import *
from OpenGL.GLU import *
##############################

#### 추가로 필요한 패키지
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
##############################

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtWidgets import QGroupBox, QPushButton
from PyQt6.QtCore import *
from PyQt6.QtGui import QPainter, QPen
import sys


# 정점 데이터 (2차원 정점을 리스트로 표현하고, 이들의 리스트로 복수의 정점 관리)
POINTS = [[0, 0], [10, 10], [100, 50]]

############ 프리미터 선택을 위한 데이터
PRIMITIVES = ['GL_POINTS', 'GL_LINES', 'GL_LINE_STRIP', 'GL_LINE_LOOP',
              'GL_TRIANGLES', 'GL_TRIANGLE_STRIP', 'GL_TRIANGLE_FAN',
              'GL_QUADS', 'GL_QUAD_STRIP', 'GL_POLYGON']

PRIMITIVE_VALUES = [GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP,
                    GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN,
                    GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]
selected = 0
######################################################################

############## 정점 정보 그리기
class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    def initializeGL(self):
        # OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화
        glClearColor(0.8, 0.8, 0.6, 1.0)
        glPointSize(4)
        glLineWidth(2)

    def resizeGL(self, width, height):
        # 카메라의 투영 특성을 여기서 설정
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 240, 380, 0, -1, 1)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 프리미티브를 이용한 객체 그리기
        glBegin(PRIMITIVE_VALUES[selected])
        nPoints = len(POINTS)
        for i in range(nPoints):
            glVertex2fv(POINTS[i])
        glEnd()

        # 그려진 프레임버퍼를 화면으로 송출
        glFlush()
###########################################

class MyWindow(QMainWindow):

    def __init__(self, title=''):
        QMainWindow.__init__(self)  # QMainWindow 슈퍼 클래스의 초기화
        self.setWindowTitle(title)

        ### GUI 설정

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        gui_layout = QHBoxLayout()  # CentralWidget의 수평 나열 레이아웃


        # 배치될 것들 - 정점 입력을 받기 위한 위짓
        central_widget.setLayout(gui_layout)

        ############ OpenGL Widget 추가
        self.glWidget = MyGLWidget()  # OpenGL Widget
        gui_layout.addWidget(self.glWidget)
        ############################################################

        self.controlGroup = QGroupBox('정점 입력')
        gui_layout.addWidget(self.controlGroup)

        control_layout = QVBoxLayout()
        self.controlGroup.setLayout(control_layout)
     
        #################### 프리미티브 선택 기능 추가
        primitive_selection = QComboBox()
        for i in range(len(PRIMITIVES)):
            primitive_selection.addItem(PRIMITIVES[i])

        # ComboBox에 기능 연결
        primitive_selection.currentIndexChanged.connect(
                                      self.selectPrimitive)

        reset_button = QPushButton('정점 초기화', self)
        reset_button.clicked.connect(self.resetPoints)

        control_layout.addWidget(primitive_selection)
        control_layout.addWidget(reset_button)
        #################################################

        ## 정점을 입력받기 위한 위짓을 만들고, pointInput이라는 멤버로 관리하자.
        self.pointInput = Drawer(parent=self)
        gui_layout.addWidget(self.pointInput)

    ########## Primitive 선택 ###################
    def selectPrimitive(self, text):
        global selected
        selected = int(text)
        self.glWidget.update()
    ###########################################

    # 정점 초기화 버튼을 눌렀을 때 호출되는 메소드
    def resetPoints(self, btn):
        global POINTS
        POINTS = []
        self.pointInput.update()


#### 정점 입력을 위해 사용되는 위짓으로 QPainter를 활용한다.
class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        # QPainter 멤버 준비
        self.painter = QPainter()

    # QPainter를 이용하여 입력된 정점을 출력한다.
    def paintEvent(self, event):
        global POINTS

        self.painter.begin(self)
        self.painter.setPen(QPen(Qt.GlobalColor.red, 6))

        for i in range(len(POINTS)):
            self.painter.drawPoint(QPointF(POINTS[i][0], POINTS[i][1]))

        self.painter.setPen(QPen(Qt.GlobalColor.blue, 2))
        for i in range(len(POINTS) - 1):
            self.painter.drawLine(QLineF(POINTS[i][0], POINTS[i][1],POINTS[i + 1][0], POINTS[i + 1][1]))
        self.painter.end()

    # 정점을 입력하는 방법은 마우스 이벤트 발생시에 좌표를 읽어
    # 이 정점을 표현하는 2차원 정보를 리스트로 만들어 정점 리스트 POINTS에 추가
    def mousePressEvent(self, event):
        POINTS.append([event.position().x(), event.position().y()])
        ############################################
        self.parent.glWidget.update()
        ############################################
        self.update()


def main(argv=[]):
    app = QApplication(argv)
    window = MyWindow('데이터 입력')
    window.setFixedSize(800, 400)
    window.show()
    app.exec()


if __name__ == '__main__':
    main(sys.argv)