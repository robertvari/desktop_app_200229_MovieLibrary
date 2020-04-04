from PySide2.QtCore import QRunnable, QObject, Signal
from nodes.movie import Movie


class WorkerSignals(QObject):
    finished = Signal(object)

    def __init__(self):
        super(WorkerSignals, self).__init__()


class MovieDownloader(QRunnable):
    def __init__(self, movie_data):
        super(MovieDownloader, self).__init__()
        self.movie_object = Movie(movie_data)
        self.signals = WorkerSignals()

    def run(self):
        self.movie_object.get_poster()
        self.movie_object.save()
        print(f"Movie data saved: {self.movie_object.original_title}")
        self.signals.finished.emit(self.movie_object)
