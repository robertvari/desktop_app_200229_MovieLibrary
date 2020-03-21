from PySide2.QtWidgets import QWidget, QLineEdit, QListWidget, QListWidgetItem, \
    QVBoxLayout, QItemDelegate
from PySide2.QtGui import QColor, QPen, QBrush, QPixmap, QFont
from PySide2.QtCore import QSize, Qt, QRect

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

        self.poster_rect = QRect()
        self.content_box = QRect()
        self.date_rect = QRect()
        self.user_score_rect = QRect()
        self.description_rect = QRect()
        self.writer_rect = QRect()

        self.outline = QPen(QColor(0, 0, 0, 30))
        self.font_pen = QPen(QColor(0, 0, 0, 150))
        self.poster_background = QBrush(QColor("black"))

        self.font = QFont()

        self.title_font = QFont()
        self.title_font.setPixelSize(20)
        self.title_font.setBold(True)

    def paint(self, painter, option, index):
        rect = option.rect

        painter.setPen(self.outline)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect)

        item_data = index.data(Qt.UserRole)
        poster = index.data(Qt.UserRole + 1)

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
        painter.drawText(self.content_box, item_data.get('title'))

        # draw release date
        painter.setFont(self.font)
        self.date_rect.setRect(self.content_box.x(), self.content_box.y() + 25, self.content_box.width(), 15)
        painter.drawText(self.date_rect, item_data["release_date"])

        # director/writer
        self.writer_rect.setRect(self.content_box.x(), self.date_rect.bottom() + 2, self.content_box.width(), 15)
        painter.drawText(self.writer_rect, f"Director: {item_data['director']}, Writer: {item_data['writer']}")

        # description
        self.description_rect.setRect(self.content_box.x(), self.writer_rect.bottom() + 20, self.content_box.width(), rect.height())
        painter.drawText(self.description_rect, item_data["description"])


class MovieItem(QListWidgetItem):
    def __init__(self, parent, movie_data):
        super(MovieItem, self).__init__(parent)
        self.movie_data = movie_data
        self.setSizeHint(QSize(480, 270))

        self.setData(Qt.UserRole, movie_data)

        poster = QPixmap(movie_data["poster"])
        poster = poster.scaled(QSize(200, 270), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setData(Qt.UserRole + 1, poster)


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = MovieBrowser()
    win.show()
    app.exec_()