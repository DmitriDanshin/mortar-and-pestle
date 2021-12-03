import matplotlib
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget
from numpy import ndarray

matplotlib.use('Qt5Agg')


class Plot(FigureCanvasQTAgg):
    def __init__(self, params: list[tuple[ndarray, ndarray, str]]):
        fig = Figure(figsize=(4, 4), dpi=100)
        self.axes = fig.add_subplot()
        for p in params:
            self.axes.plot(*p)
        super(Plot, self).__init__(fig)


class ToolBar(QWidget):
    def __init__(self, canvas, parent=None):
        super(ToolBar, self).__init__(parent)
        NavigationToolbar(canvas, self)
