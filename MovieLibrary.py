from PySide2.QtWidgets import QMainWindow, QApplication, QHBoxLayout, \
    QWidget, QAction
from PySide2.QtCore import QThreadPool
import sys

from modules.CategorySelector import CategorySelector
from modules.MovieBrowser import MovieBrowser
from modules.AddMovieDialog import AddMovieDialog

from nodes.movie import Movie
from utilities import static_utils

from modules.ThreadingModules import MovieDownloader


class MovieLibrary(QMainWindow):
    def __init__(self):
        super(MovieLibrary, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle("Movie Library")

        self.downloader_pool = QThreadPool()
        self.downloader_pool.setMaxThreadCount(8)

        # menu
        menu = self.menuBar()

        movies_menu = menu.addMenu("Movies")

        add_movie_action = QAction("Add Movie", movies_menu)
        add_movie_action.triggered.connect(self.add_movie_action)
        movies_menu.addAction(add_movie_action)

        edit_movie_action = QAction("Edit Movie", movies_menu)
        edit_movie_action.triggered.connect(self.edit_movie_action)
        movies_menu.addAction(edit_movie_action)

        delete_movie_action = QAction("Delete Movie", movies_menu)
        delete_movie_action.triggered.connect(self.delete_movie_action)
        movies_menu.addAction(delete_movie_action)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.category_selector = CategorySelector()
        main_layout.addWidget(self.category_selector)

        self.movie_browser = MovieBrowser()
        main_layout.addWidget(self.movie_browser)

        self.apply_style()

    def apply_style(self):
        css_path = static_utils.css_path
        with open(css_path) as f:
            style = f.read()
            self.setStyleSheet(style)

    def add_movie_action(self):
        dialog = AddMovieDialog(self)

        if dialog.exec_():
            for movie_data in dialog.selected_movies:
                movie_downloader = MovieDownloader(movie_data)

                movie_downloader.signals.finished.connect(
                    self.movie_browser.icon_view.add_movie
                )

                self.downloader_pool.start(movie_downloader)

    def edit_movie_action(self):
        print("Edit selected movie")

    def delete_movie_action(self):
        print("Delete selected movies")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MovieLibrary()
    win.show()
    app.exec_()