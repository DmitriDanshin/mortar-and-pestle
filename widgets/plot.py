import matplotlib
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget

matplotlib.use('Qt5Agg')


class Plot(FigureCanvasQTAgg):
    def init(self, params):
        self.axes = self.fig.add_subplot()
        for p in params:
            self.axes.plot(*p)

    def __init__(self, params):
        self.axes = None
        self.fig = None
        self.fig = Figure(figsize=(4, 4), dpi=100)
        self.init(params)
        super(Plot, self).__init__(self.fig)

    def update_plot(self, params):
        self.fig.clf()
        self.init(params)
        self.draw()


class ToolBar(QWidget):
    def __init__(self, canvas, parent=None):
        super(ToolBar, self).__init__(parent)
        NavigationToolbar(canvas, self)
