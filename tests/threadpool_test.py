from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, \
    QApplication, QProgressBar
from PySide2.QtCore import QRunnable, QThreadPool, QObject, Signal
import sys, time, random

from nodes.movie import Movie
from utilities.MovieDB import find_movie


class ThreadpoolTest(QWidget):
    def __init__(self):
        super(ThreadpoolTest, self).__init__()
        self.setWindowTitle("Trheading test")
        main_layout = QVBoxLayout(self)

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)

        button = QPushButton("Start")
        button.clicked.connect(self.start_progress)
        main_layout.addWidget(button)

        self.progressbar = QProgressBar()
        self.progressbar.setVisible(False)
        main_layout.addWidget(self.progressbar)

    def start_progress(self):
        self.movie_list = find_movie("Alien")
        self.progressbar.setMaximum(len(self.movie_list))
        self.progressbar.setVisible(True)

        self.start_time = time.time()

        for movie_data in self.movie_list:
            movie_worker = MovieWorker(movie_data)
            movie_worker.signals.finished.connect(self.download_finished)
            self.threadpool.start(movie_worker)

    def download_finished(self, movie_object):
        print(f"Download finished: {movie_object.original_title}")

        self.progressbar.setValue(self.progressbar.value() + 1)

        if self.progressbar.value() == len(self.movie_list) - 1:
            self.progressbar.setVisible(False)
            self.progressbar.setValue(0)
            print(f"Progress finished in: {time.time()-self.start_time}")


class WorkerSignals(QObject):
    finished = Signal(object)

    def __init__(self):
        super(WorkerSignals, self).__init__()


class MovieWorker(QRunnable):
    def __init__(self, movie_data):
        super(MovieWorker, self).__init__()
        self.movie_object = Movie(movie_data)
        self.signals = WorkerSignals()

    def run(self):
        self.movie_object.get_poster()
        self.movie_object.save()

        self.signals.finished.emit(self.movie_object)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ThreadpoolTest()
    win.show()
    app.exec_()