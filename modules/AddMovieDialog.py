from PySide2.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout

from utilities.MovieDB import find_movie
from nodes.database import Client

class AddMovieDialog(QDialog):
    client = Client()

    def __init__(self, parent):
        super(AddMovieDialog, self).__init__(parent)
        self.setWindowTitle("Add Movie")
        main_layout = QVBoxLayout(self)

        self.selected_movies = None

        self.search_field = QLineEdit()
        self.search_field.returnPressed.connect(self.find_action)
        self.search_field.setPlaceholderText("Search movies...")
        main_layout.addWidget(self.search_field)

        self.result_list = QListWidget()
        self.result_list.setSelectionMode(QListWidget.ExtendedSelection)
        main_layout.addWidget(self.result_list)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        add_bttn = QPushButton("Add Movie")
        add_bttn.clicked.connect(self.accept)

        add_all_bttn = QPushButton("Add All Movies")
        add_all_bttn.clicked.connect(self.add_all_action)

        cancel_bttn = QPushButton("Cancel")
        cancel_bttn.clicked.connect(self.reject)

        button_layout.addWidget(add_bttn)
        button_layout.addWidget(add_all_bttn)
        button_layout.addWidget(cancel_bttn)

    def keyPressEvent(self, event):
        event.ignore()

    def add_all_action(self):
        for i in range(self.result_list.count()):
            self.result_list.setItemSelected(self.result_list.item(i), True)

        self.accept()

    def accept(self):
        selected_items = self.result_list.selectedItems()
        if not selected_items:
            return

        self.selected_movies = [i.movie_data for i in selected_items if not self.client.find_movie(i.movie_data["id"])]
        super(AddMovieDialog, self).accept()

    def find_action(self):
        movie_title = self.search_field.text()
        if len(movie_title):
            self.result_list.clear()

            for item in find_movie(movie_title):
                MovieItem(self.result_list, item)


class MovieItem(QListWidgetItem):
    def __init__(self, parent, movie_data):
        super(MovieItem, self).__init__(parent)
        self.movie_data = movie_data
        self.setText(f"{movie_data['original_title']} ({movie_data['release_date']})")


if __name__ == '__main__':
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = AddMovieDialog(None)
    win.show()
    app.exec_()