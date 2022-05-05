import math
from math import sin, cos
from dataclasses import dataclass
import LightPipes as lp
import matplotlib
import numpy as np
from LightPipes import mm, nm
from PyQt5.QtWidgets import QWidget
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from numba import njit

matplotlib.use('Qt5Agg')


@njit(fastmath=True)
def get_intensity(
        N: int, wavelength: float,
        size: int, f: float,
        medium: float, distance: float,
        reflection: float):
    k = 2 * math.pi / (wavelength * nm)

    step = size / N
    result = [[1.0 for _ in range(N)] for _ in range(N)]

    for i in range(1, N):
        xray = i * step
        for j in range(1, N):
            yray = j * step
            x = (xray - size / 2)
            y = (yray - size / 2)
            radius = math.hypot(x, y)

            theta = radius / f

            delta = k * 2 * medium * distance * cos(theta) * mm

            intensity = 1 / (1 + (4.0 * reflection / (1.0 - reflection) ** 2) * sin(delta / 2) ** 2)
            intensity = intensity * (1 / (1 + np.exp(radius / 2 - math.e / math.pi)))
            result[i][j] = intensity
    return result


@dataclass
class Intensity:
    wavelength: float
    reflection: float
    distance: float
    medium: int
    size: int
    N: int
    f: float

    @property
    def value(self) -> lp.Intensity:
        return self.__get_value()

    def __get_value(self) -> lp.Intensity:
        result = get_intensity(
            self.N, self.wavelength,
            self.size, self.f,
            self.medium, self.distance,
            self.reflection
        )
        return result


class Plot(FigureCanvasQTAgg):
    fig: Figure

    @staticmethod
    def get_figure(intensity: Intensity):
        fig, axes = plt.subplots(2, figsize=(15, 15))
        x = np.linspace(0, intensity.N, intensity.N)
        axes[0].clear()
        value = np.asarray(intensity.value)
        axes[0].plot(x, value[intensity.N // 2, :], "r")  # for 2d mode
        axes[1].imshow(value, cmap="gist_heat")
        axes[1].axis('off')
        axes[1].axis('equal')
        axes[0].set_title('Распределение интенсивности')
        plt.close(fig)
        return fig

    def calculate(self, wavelength, reflection, distance, medium):
        intensity = Intensity(
            wavelength=wavelength,
            reflection=reflection,
            distance=distance,
            medium=medium,
            N=500,
            f=100,
            size=5,
        )
        return self.get_figure(intensity)

    def __init__(self, wavelength, reflection, distance, n):
        self.init(wavelength, reflection, distance, n)
        super(Plot, self).__init__(self.fig)

    def init(self, wavelength, reflection, distance, n):
        self.fig = self.calculate(wavelength, reflection, distance, n)

    def update_parameters(self, wavelength, reflection, distance, n):
        self.fig.clf()
        self.init(wavelength, reflection, distance, n)
        self.draw()


class ToolBar(QWidget):
    def __init__(self, canvas, parent=None):
        super(ToolBar, self).__init__(parent)
        NavigationToolbar(canvas, self)
