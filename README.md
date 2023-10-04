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

#### 실습 3

[실습 3-01 glOrtho 연습](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex03/03_02_glOrthoTest.py)

[실습 3-02 왜곡없는 좌표계](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex03/03_02_glOrthoTest.py)

[실습 3-03 두 개의 OpenGL 위짓](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex03/03_03_TwoGLWindow.py)

[실습 3-04 두 창에 나선 그리기기](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex03/03_04_DrawHelixInTwoViews.py)

[실습 3-05 서로 다른 동작을 하는 GL 위짓](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex03/03_05_DifferentActionsInTwoViews.py)

[실습 3-06 카메라를 옮겨 관측공간 확인하기](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex03/03_06_Observation.py)

[실습 3-07 glOrtho 관측공간 관찰 최종](https://github.com/dknife/2023Graphics/blob/main/Ex/Ex03/03_07_ObservationFinal.py)

### 실습 4

#### Frustum 그리기
``` python
def drawFrustum(l, r, b, t, n, f):
    # 뒷면의 좌우하상 좌표를 구하자
    L = l * (f/n)
    R = r * (f/n)
    B = b * (f/n)
    T = t * (f/n)
    # 절두체의 앞면을 그리기
    glColor3f(1,1,1)
    glBegin(GL_LINE_LOOP)
    glVertex3f(l,t,-n)    
    glVertex3f(l,b,-n)
    glVertex3f(r,b,-n)
    glVertex3f(r,t,-n)    
    glEnd()
    # 절두체 뒷면 그리기
    glBegin(GL_LINE_LOOP)
    glVertex(L,T,-f)
    glVertex(L,B,-f)
    glVertex(R,B,-f)
    glVertex(R,T,-f)
    glEnd()
    # 앞뒷면 연결
    glBegin(GL_LINES)
    glVertex3f(l,t,-n) 
    glVertex3f(L,T,-f)   
    glVertex3f(l,b,-n)
    glVertex3f(L,B,-f)
    glVertex3f(r,b,-n)
    glVertex3f(R,B,-f)
    glVertex3f(r,t,-n)
    glVertex3f(R,T,-f)    
    glEnd()
```
