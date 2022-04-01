import math
import matplotlib
from LightPipes import nm, mm, Begin, Intensity
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget

matplotlib.use('Qt5Agg')


class Plot(FigureCanvasQTAgg):

    def TheExample(self, wavelength, reflection):
        wavelength = wavelength * nm  # Длина волны
        size = 5 * mm  # Масштаб
        N = 300  # Количество шагов интегрирования
        f = 100 * mm
        d = 6 * mm
        Dlabda = 0.0
        nmedium = 1.0
        k = 2 * math.pi / wavelength

        fig = plt.figure(figsize=(6, 4))
        ax1 = fig.add_subplot(111)

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
        ax1.clear()
        ax1.imshow(I, cmap='gist_heat')
        ax1.axis('off')
        ax1.axis('equal')
        str = 'Распределение интенсивности'
        ax1.set_title(str)
        return fig

    def __init__(self, wavelength, reflection):
        self.init(wavelength, reflection)
        super(Plot, self).__init__(self.fig)

    def init(self, wavelength, reflection):
        self.axes = None
        self.fig = self.TheExample(wavelength, reflection)

    def update_parameters(self, wavelength, reflection):
        self.fig.clf()
        self.init(wavelength, reflection)
        self.draw()


class ToolBar(QWidget):
    def __init__(self, canvas, parent=None):
        super(ToolBar, self).__init__(parent)
        NavigationToolbar(canvas, self)
