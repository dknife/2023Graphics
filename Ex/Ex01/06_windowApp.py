# 필요한 클래스를 임포트 한다
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget

import sys

class MyWindow(QMainWindow) :

    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)
win = MyWindow()
win.show()

app.exec()

