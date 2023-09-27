[홈](https://github.com/dknife/dknife.github.io/wiki)

# 2023 3D 그래픽스 프로그래밍

## 2023년 2학기 동명대학교 게임공학과 


### 강의실: 제1정 518

### 담당교수 연락처: ymkang @ tu.ac.kr

### 강의노트

강의 00 - 강의소개

* [강의노트](https://github.com/dknife/2023Graphics/raw/main/LectureNotes/Lec00_Orientation.pdf)

강의 01 - 그래픽스 소개

* [강의노트](https://github.com/dknife/2023Graphics/raw/main/LectureNotes/Lec01_Introduction2Graphics.pdf)

강의 02 - 그래픽스 프로그래밍 환경 구축

* [강의노트](https://github.com/dknife/2023Graphics/raw/main/LectureNotes/Lec02_BasicGraphicsProgramming.pdf)

* [발표자료](https://github.com/dknife/2023Graphics/raw/main/LectureNotes/Lec02_BasicGraphicsProgramming_Pres.pdf)

강의 03 - OpenGL 프리미티브

* [강의노트](https://github.com/dknife/2023Graphics/raw/main/LectureNotes/Lec03_Primitives.pdf)

* [발표자료](https://github.com/dknife/2023Graphics/raw/main/LectureNotes/Lec03_Primitives_Pres.pdf)

강의 04 - 카메라와 투영

* [강의노트](https://github.com/dknife/2023Graphics/raw/main/LectureNotes/Lec04_CameraProjection.pdf)

* [발표자료](https://github.com/dknife/2023Graphics/raw/main/LectureNotes/Lec04_CameraProjection_pres.pdf)

### 실습기록

#### 실습 1

[실습 1-01 변수](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex01/01_variables.py)

[실습 1-02 조건문과 반복문](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex01/02_control.py)

[실습 1-03 리스트](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex01/03_list.py)

[실습 1-04 함수](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex01/04_function.py)

[실습 1-05 pyQt 시작](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex01/05_pyqt.py)

[실습 1-06 pyQt Widgets](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex01/06_windowApp.py)

#### 실습 2

[실습 2-01 첫 오픈지엘 윈도우](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex02/02_01_firstOpenGLWidget.py)

[실습 2-02 프리미티브 연습](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex02/02_02_primitives.py)

[실습 2-02 프리미티브 연습 2 - 원 그리기](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex02/02_02_primitives_circle.py)

[실습 2-Project 프리미티브 조작](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex02/02_03_primitiveControl.py)

##### 교재 코드 수정(API 변화)

self.painter.drawPoint(POINTS[i][0], POINTS[i][1]) $\rightarrow$ self.painter.drawPoint(**QPointF**(POINTS[i][0], POINTS[i][1]))

self.painter.drawLine(POINTS[i][0], POINTS[i][1],POINTS[i + 1][0], POINTS[i + 1][1]) $\rightarrow$ self.painter.drawLine(**QLineF**(POINTS[i][0], POINTS[i][1],POINTS[i + 1][0], POINTS[i + 1][1]))

<pre>
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
</pre>


#### 실습 4

[실습 4-01 glOrtho 연습](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex03/03_01_glOrthoTest.py)
