import math
import numpy as np
from LightPipes import nm, mm, Begin, Intensity
from PyQt5.QtWidgets import QMainWindow
from matplotlib import pyplot as plt
import matplotlib
from widgets.plot import Plot, ToolBar
from assets.MainWindow import Ui_MainWindow

matplotlib.use('Qt5Agg')


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tb = None
        self.plot = None
        self.setupUi(self)
        self.init_plots()

    def TheExample(self):
        fig = plt.figure(figsize=(6, 4))
        ax1 = fig.add_subplot(111)
        labda = 550 * nm
        size = 5 * mm
        N = 300
        f = 100 * mm
        Dlabda = 0.0
        nmedium = 1.0
        k = 2 * math.pi / labda
        d = 10 * mm
        r = 5
        k2 = 2 * math.pi / (labda + Dlabda)
        Fin = 4.0 * r / (1.0 - r)
        F = Begin(size, labda, N)
        I = Intensity(1, F)
        step = size / N / mm
        for i in range(1, N):
            xray = i * step
            for j in range(1, N):
                yray = j * step
                X = xray * mm - size / 2
                Y = yray * mm - size / 2
                radius = math.sqrt(X * X + Y * Y)
                theta = radius / f
                delta2 = k * nmedium * d * math.cos(theta)
                Inten = 0.5 / (1 + Fin * math.pow(math.sin(delta2), 2))
                delta2 = k2 * nmedium * d * math.cos(theta)
                I[i][j] = (Inten + 0.5 / (1 + Fin * math.pow(math.sin(delta2), 2)))
        ax1.clear()
        ax1.imshow(I, cmap='hot')
        ax1.axis('off')
        ax1.axis('equal')
        str = 'Распределение интенсивности'
        ax1.set_title(str)
        return I

    def changeLabel(self, x, label, plot):
        label.setText(str(x))
        plot.update_plot([(np.linspace(0, 100) ** x, np.linspace(0, 100))])

    def init_plots(self):
        x = np.linspace(0, 100)
        self.plot = Plot([(x, x, 'b--'), (x, x, 'g--')])
        self.plot1Grid.addWidget(self.plot)
        self.tb = ToolBar(self.plot)
        self.plot1Grid.addWidget(self.tb)
        self.horizontalSlider.valueChanged.connect(lambda y: self.changeLabel(y, self.label, self.plot))
        self.horizontalSlider_2.valueChanged.connect(lambda y: self.changeLabel(y, self.label_2, self.plot))
