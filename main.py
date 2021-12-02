import matplotlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget
import sys
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from assets.MainWindow import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Plot(QWidget):
    def __init__(self, parent=None, params=()):
        super(Plot, self).__init__(parent)
        sc = MplCanvas(width=5, height=4, dpi=100)

        sc.axes.plot(*params)

        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(layout)
        self.show()


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.plot1Grid.addWidget(Plot(self, params=([0, 1, 2, 3, 4], [10, 1, 20, 3, 40], 'b--')).widget)
        self.plot2Grid.addWidget(Plot(self, params=([0, 1, 2, 3, 4], [10, 1, 20, 3, 40], 'g--')).widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())
