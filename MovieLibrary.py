from PySide2.QtWidgets import QMainWindow, QApplication, QHBoxLayout, \
    QWidget
import sys

from modules.CategorySelector import CategorySelector
from modules.MovieBrowser import MovieBrowser


class MovieLibrary(QMainWindow):
    def __init__(self):
        super(MovieLibrary, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle("Movie Library")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.category_selector = CategorySelector()
        main_layout.addWidget(self.category_selector)

        self.movie_browser = MovieBrowser()
        main_layout.addWidget(self.movie_browser)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MovieLibrary()
    win.show()
    app.exec_()