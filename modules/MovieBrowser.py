from PySide2.QtWidgets import QWidget, QLineEdit, QListWidget, QListWidgetItem, \
    QVBoxLayout, QItemDelegate, QPushButton, QHBoxLayout
from PySide2.QtGui import QColor, QPen, QBrush, QPixmap, QFont, QImage
from PySide2.QtCore import QSize, Qt, QRect, Signal, QThread, QThreadPool, QRunnable, QObject

import tempfile

from nodes.movie import Movie
from utilities.image_utils import download_image

class MovieBrowser(QWidget):
    def __init__(self):
        super(MovieBrowser, self).__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.search_field = QLineEdit()
        self.movie_list_view = MovieListView()

        main_layout.addWidget(self.search_field)
        main_layout.addWidget(self.movie_list_view)


class MovieListView(QListWidget):
    def __init__(self):
        super(MovieListView, self).__init__()

        self.setItemDelegate(MovieListDelegate())
        self.setSpacing(10)

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        # self.setMovement(QListWidget.Static)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setAcceptDrops(True)

        self.refresh()

    def check_drag_data(self, event):

        if event.mimeData().urls():
                current_path = event.mimeData().urls()[0].toLocalFile()
                if not current_path:
                    current_path = event.mimeData().urls()[0].toString()

                if current_path.lower().endswith(".jpg"):
                    return True
        return False

    def dragEnterEvent(self, event):

        if self.check_drag_data(event):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self.itemAt(event.pos()):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        current_item = self.itemAt(event.pos())

        # set poster for movie object
        current_url = event.mimeData().urls()[0]

        if "http" in current_url.toString():
            poster_path = download_image(tempfile.gettempdir(), current_url.toString())
        else:
            poster_path = event.mimeData().urls()[0].toLocalFile()

        current_item.movie.set_poster(poster_path)

        # refresh movie item in view
        current_item.set_item_poster(poster_path)

    def set_favorited_action(self, movie):
        value = not movie.favorited
        movie.set_favorited(value)

        self.repaint()

    def delete_movie(self, movie):
        movie.delete()
        self.refresh()

    def refresh(self):
        self.clear()

        self.movie_worker = MovieWorker()
        self.movie_worker.movie_finished.connect(self.movie_ready)
        self.movie_worker.start()

    def movie_ready(self, data_dict):
        movie_item = MovieItem(self, data_dict["movie"], data_dict["image"])
        movie_item.widget.delete_clicked.connect(self.delete_movie)

    def add_movie(self, movie):
        movie_item = MovieItem(self, movie, QImage(movie.get_poster()))
        movie_item.widget.delete_clicked.connect(self.delete_movie)


class MovieListDelegate(QItemDelegate):
    def __init__(self):
        super(MovieListDelegate, self).__init__()

        self.poster_rect = QRect()
        self.content_box = QRect()
        self.date_rect = QRect()
        self.user_score_rect = QRect()
        self.description_rect = QRect()
        self.vote_average = QRect()

        self.outline = QPen(QColor(0, 0, 0, 30))
        self.font_pen = QPen(QColor(0, 0, 0, 150))
        self.poster_background = QBrush(QColor("black"))
        self.favorited_background = QBrush(QColor("lightBlue"))

        self.font = QFont()

        self.title_font = QFont()
        self.title_font.setPixelSize(20)
        self.title_font.setBold(True)

    def paint(self, painter, option, index):
        rect = option.rect
        movie = index.data(Qt.UserRole)
        poster = index.data(Qt.UserRole + 1)

        painter.setPen(self.outline)

        if movie.favorited:
            painter.setBrush(self.favorited_background)
        else:
            painter.setBrush(Qt.NoBrush)

        painter.drawRect(rect)

        # draw poster
        self.poster_rect.setRect(rect.x()+2, rect.y() + 2, poster.width(), poster.height() -4)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.poster_background)
        painter.drawPixmap(self.poster_rect, poster)

        # content box
        content_box_width = (rect.width() - self.poster_rect.width()) - 14
        self.content_box.setRect(self.poster_rect.right()+10, rect.y() + 2, content_box_width, poster.height() -4)

        # draw title
        painter.setPen(self.font_pen)
        painter.setFont(self.title_font)
        painter.drawText(self.content_box, movie.original_title)

        # draw release date
        painter.setFont(self.font)
        self.date_rect.setRect(self.content_box.x(), self.content_box.y() + 25, self.content_box.width(), 15)
        painter.drawText(self.date_rect, movie.release_date)

        # director/writer
        self.vote_average.setRect(self.content_box.x(), self.date_rect.bottom() + 2, self.content_box.width(), 15)
        painter.drawText(self.vote_average, f"Vote average: {movie.vote_average}")

        # description
        self.description_rect.setRect(self.content_box.x(), self.vote_average.bottom() + 20, self.content_box.width(), rect.height())
        painter.drawText(self.description_rect, movie.overview)


class MovieItem(QListWidgetItem):
    def __init__(self, parent, movie, image):
        super(MovieItem, self).__init__(parent)
        self.movie = movie
        self.setSizeHint(QSize(480, 270))

        self.setText(movie.original_title)

        self.setData(Qt.UserRole, movie)

        self.set_item_poster(image)

        self.widget = MovieItemWidget(movie)
        parent.setItemWidget(self, self.widget)

    def set_item_poster(self, image):
        poster = QPixmap(image)
        poster = poster.scaled(QSize(200, 270), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setData(Qt.UserRole + 1, poster)


class MovieItemWidget(QWidget):
    favorite_clicked = Signal(object)
    delete_clicked = Signal(object)

    def __init__(self, movie):
        super(MovieItemWidget, self).__init__()
        self.movie = movie

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignBottom)
        main_layout.setContentsMargins(190, 5, 5, 5)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        favorite_bttn = QPushButton("Favorite")
        button_layout.addWidget(favorite_bttn)

        edit_bttn = QPushButton("Edit")
        button_layout.addWidget(edit_bttn)

        delete_bttn = QPushButton("Delete")
        button_layout.addWidget(delete_bttn)

        favorite_bttn.clicked.connect(self.favorite_clicked_action)
        delete_bttn.clicked.connect(self.delete_action)

    def delete_action(self):
        self.delete_clicked.emit(self.movie)

    def favorite_clicked_action(self):
        self.favorite_clicked.emit(self.movie)


class MovieWorker(QThread):
    movie_finished = Signal(dict)

    def __init__(self):
        super(MovieWorker, self).__init__()

    def run(self):
        for movie in Movie.get_all():
            movie_dict = {
                "movie": movie,
                "image": QImage(movie.get_poster())
            }

            self.movie_finished.emit(movie_dict)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = MovieBrowser()
    win.show()
    app.exec_()