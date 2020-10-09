from PySide2.QtWidgets import QWidget, QGroupBox, QPushButton, QVBoxLayout, QApplication
import sys

class LayoutColorTest(QWidget):
    def __init__(self):
        super(LayoutColorTest, self).__init__()
        main_layout = QVBoxLayout(self)

        box = QGroupBox()
        box.setObjectName("my_box")
        main_layout.addWidget(box)
        box_layout = QVBoxLayout(box)

        button = QPushButton("Click")
        box_layout.addWidget(button)

        box = QGroupBox()
        box.setObjectName("my_box2")
        main_layout.addWidget(box)
        box_layout = QVBoxLayout(box)

        button = QPushButton("Click")
        box_layout.addWidget(button)

        self.apply_style()

    def apply_style(self):
        style = "#my_box{background-color: red;} #my_box2{background-color: green;}"

        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LayoutColorTest()
    win.show()
    app.exec_()