from PySide2.QtWidgets import QMainWindow, QApplication, QHBoxLayout, \
    QWidget, QAction
import sys

from modules.CategorySelector import CategorySelector
from modules.MovieBrowser import MovieBrowser
from modules.AddMovieDialog import AddMovieDialog

from nodes.movie import Movie


class MovieLibrary(QMainWindow):
    def __init__(self):
        super(MovieLibrary, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle("Movie Library")

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

    def add_movie_action(self):
        dialog = AddMovieDialog(self)

        if dialog.exec_():
            movie = Movie(dialog.selected_movie)
            movie.save()
            self.movie_browser.icon_view.add_movie(movie)

    def edit_movie_action(self):
        print("Edit selected movie")

    def delete_movie_action(self):
        print("Delete selected movies")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MovieLibrary()
    win.show()
    app.exec_()