from PySide2.QtWidgets import QWidget, QLineEdit, QListWidget, QVBoxLayout


class MovieBrowser(QWidget):
    def __init__(self):
        super(MovieBrowser, self).__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.search_field = QLineEdit()
        self.icon_view = QListWidget()

        main_layout.addWidget(self.search_field)
        main_layout.addWidget(self.icon_view)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = MovieBrowser()
    win.show()
    app.exec_()