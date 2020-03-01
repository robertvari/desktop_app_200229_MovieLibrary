from PySide2.QtWidgets import QWidget, QLineEdit, QListWidget, QListWidgetItem, QVBoxLayout

from utilities.dummy_data import create_dummy_data

movies_data = create_dummy_data(100)


class MovieBrowser(QWidget):
    def __init__(self):
        super(MovieBrowser, self).__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.search_field = QLineEdit()
        self.icon_view = IconView()

        main_layout.addWidget(self.search_field)
        main_layout.addWidget(self.icon_view)


class IconView(QListWidget):
    def __init__(self):
        super(IconView, self).__init__()
        self.refresh()

    def refresh(self):
        self.clear()

        for movie in movies_data:
            MovieItem(self, movie)


class MovieItem(QListWidgetItem):
    def __init__(self, parent, movie_data):
        super(MovieItem, self).__init__(parent)
        self.movie_data = movie_data

        self.setText(movie_data.get("title"))


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = MovieBrowser()
    win.show()
    app.exec_()