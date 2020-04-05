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
        self.build_menu()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        self.category_selector = CategorySelector()
        main_layout.addWidget(self.category_selector)

        self.movie_browser = MovieBrowser()
        main_layout.addWidget(self.movie_browser)

        self.apply_style()

    def build_menu(self):
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

        movies_menu.addSeparator()

        delete_all_movie_action = QAction("Delete All Movie", movies_menu)
        delete_all_movie_action.triggered.connect(self.delete_all_movies_action)
        movies_menu.addAction(delete_all_movie_action)

    def apply_style(self):
        css_path = static_utils.css_path
        with open(css_path) as f:
            style = f.read()
            self.setStyleSheet(style)

    def add_movie_action(self):
        dialog = AddMovieDialog(self)

        if dialog.exec_() and dialog.selected_movies:
            selected_movies = dialog.selected_movies

            self.movie_browser.progressbar.setVisible(True)
            self.movie_browser.progressbar.setMaximum(len(selected_movies))

            for movie_data in selected_movies:
                movie_downloader = MovieDownloader(movie_data)

                movie_downloader.signals.finished.connect(
                    self.add_movie_to_library
                )

                self.downloader_pool.start(movie_downloader)

    def add_movie_to_library(self, movie_object):
        self.movie_browser.movie_list_view.add_movie(movie_object)
        self.movie_browser.progressbar.setValue(
            self.movie_browser.progressbar.value() + 1
        )

        if self.movie_browser.progressbar.value() == self.movie_browser.progressbar.maximum() - 1:
            self.movie_browser.progressbar.setVisible(False)
            self.movie_browser.progressbar.setValue(0)

            # refresh categories
            self.category_selector.refresh()

    def edit_movie_action(self):
        print("Edit selected movie")

    def delete_movie_action(self):
        print("Delete selected movies")

    def delete_all_movies_action(self):
        for movie in Movie.get_all():
            movie.delete()

        self.movie_browser.movie_list_view.clear()
        self.category_selector.refresh()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MovieLibrary()
    win.show()
    app.exec_()