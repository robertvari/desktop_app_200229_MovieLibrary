from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PySide2.QtCore import QRunnable, QThreadPool, QObject, Signal
import sys, time, random


class ThreadpoolTest(QWidget):
    def __init__(self):
        super(ThreadpoolTest, self).__init__()
        self.setWindowTitle("Trheading test")
        self.resize(500, 500)
        main_layout = QVBoxLayout(self)

        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(8)

        button = QPushButton("Start")
        button.clicked.connect(self.start_progress)
        main_layout.addWidget(button)

    def start_progress(self):
        for index in range(100):
            movie_worker = MovieWorker(index)
            movie_worker.signals.finished.connect(self.download_finished)
            self.threadpool.start(movie_worker)

    def download_finished(self, index):
        print(f"Download finished: {index}")


class WorkerSignals(QObject):
    finished = Signal(int)

    def __init__(self):
        super(WorkerSignals, self).__init__()


class MovieWorker(QRunnable):
    def __init__(self, index):
        super(MovieWorker, self).__init__()
        self.index = index
        self.signals = WorkerSignals()

    def run(self):
        time.sleep(random.randint(1, 6))
        self.signals.finished.emit(self.index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ThreadpoolTest()
    win.show()
    app.exec_()