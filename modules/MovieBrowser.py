from PySide2.QtWidgets import QWidget, QLineEdit, QListWidget, QListWidgetItem, \
    QVBoxLayout, QItemDelegate
from PySide2.QtCore import QSize
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
        self.setItemDelegate(IconViewDelegate())
        self.setSpacing(10)

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSelectionMode(QListWidget.ExtendedSelection)

        self.refresh()

    def refresh(self):
        self.clear()

        for movie in movies_data:
            MovieItem(self, movie)


class IconViewDelegate(QItemDelegate):
    def __init__(self):
        super(IconViewDelegate, self).__init__()

    def paint(self, painter, option, index):
        rect = option.rect
        painter.drawRect(rect)


class MovieItem(QListWidgetItem):
    def __init__(self, parent, movie_data):
        super(MovieItem, self).__init__(parent)
        self.movie_data = movie_data
        self.setSizeHint(QSize(480, 270))

        self.setText(movie_data.get("title"))


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = MovieBrowser()
    win.show()
    app.exec_()