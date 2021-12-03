import numpy as np
from PyQt5.QtWidgets import QMainWindow
from assets.MainWindow import Ui_MainWindow
from widgets.plot import Plot, ToolBar


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_plots()

    def init_plots(self):
        x1 = np.linspace(0, 100, 100)
        y1 = np.log(x1)

        plot1 = Plot([(x1, y1, 'b--'), (x1, y1 - 2, 'g.')])
        tb1 = ToolBar(plot1)

        plot2 = Plot([(x1, y1, 'r--'), (x1, y1 - 2, 'r.')])
        tb2 = ToolBar(plot2)

        self.plot1Grid.addWidget(tb1)
        self.plot1Grid.addWidget(plot1)

        self.plot2Grid.addWidget(tb2)
        self.plot2Grid.addWidget(plot2)
