import math
import matplotlib
import numpy as np
from LightPipes import nm, mm, Begin, Intensity
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget

matplotlib.use('Qt5Agg')


class Plot(FigureCanvasQTAgg):

    def TheExample(self, wavelength, reflection, distance, n):
        wavelength = wavelength * nm  # Длина волны
        size = 5 * mm  # Масштаб
        N = 300  # Количество шагов интегрирования
        f = 100 * mm
        d = distance * mm
        Dlabda = 0.0
        nmedium = n
        k = 2 * math.pi / wavelength

        fig, ax1 = plt.subplots(2, figsize=(15, 15))

        k2 = 2 * math.pi / (wavelength + Dlabda)

        F = Begin(size, wavelength, N)
        I = Intensity(1, F)
        step = size / N / mm
        for i in range(1, N):
            xray = i * step
            for j in range(1, N):
                yray = j * step
                X = xray * mm - size / 2
                Y = yray * mm - size / 2
                radius = math.hypot(X, Y)
                theta = radius / f
                delta2 = k * nmedium * d * math.cos(theta)
                Inten = 0.5 / (1 + (4.0 * reflection / (1.0 - reflection)) * math.pow(math.sin(delta2), 2))
                delta2 = k2 * nmedium * d * math.cos(theta)
                I[i][j] = (Inten + 0.5 / (1 + (4.0 * reflection / (1.0 - reflection)) * math.pow(math.sin(delta2), 2)))
        ax1[0].clear()
        x1 = np.linspace(0, 1, N)
        ax1[0].plot(x1, I[int(N / 2), :], "r")  # for 2d mode

        ax1[1].imshow(I, cmap="gist_heat")
        ax1[1].axis('off')
        ax1[1].axis('equal')
        str = 'Распределение интенсивности'
        ax1[0].set_title(str)
        plt.close(fig)
        return fig

    def __init__(self, wavelength, reflection, distance, n):
        self.fig = None
        self.axes = None
        self.init(wavelength, reflection, distance, n)
        super(Plot, self).__init__(self.fig)

    def init(self, wavelength, reflection, distance, n):
        self.axes = None
        self.fig = self.TheExample(wavelength, reflection, distance, n)

    def update_parameters(self, wavelength, reflection, distance, n):
        self.fig.clf()
        self.init(wavelength, reflection, distance, n)
        self.draw()


class ToolBar(QWidget):
    def __init__(self, canvas, parent=None):
        super(ToolBar, self).__init__(parent)
        NavigationToolbar(canvas, self)
