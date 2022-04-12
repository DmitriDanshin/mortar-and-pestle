import math
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

matplotlib.use('Qt5Agg')


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
        k = 2 * math.pi / (self.wavelength * nm)
        result = lp.Intensity(Fin=lp.Begin(self.size * mm, self.wavelength * nm, self.N))
        step = self.size / self.N

        for i in range(1, self.N):
            xray = i * step
            for j in range(1, self.N):
                yray = j * step
                x = (xray - self.size / 2)
                y = (yray - self.size / 2)
                radius = math.hypot(x, y)
                theta = radius / self.f
                delta = k * self.medium * self.distance * math.cos(theta) * mm
                intensity = 0.5 / (1 + (4.0 * self.reflection / (1.0 - self.reflection)) * math.pow(math.sin(delta), 2))
                result[i][j] = (intensity + 0.5 / (
                        1 + (4.0 * self.reflection / (1.0 - self.reflection)) * math.pow(math.sin(delta), 2)))
        return result


class Plot(FigureCanvasQTAgg):
    fig: Figure

    @staticmethod
    def get_figure(intensity: Intensity):
        fig, axes = plt.subplots(2, figsize=(15, 15))
        x = np.linspace(0, 1, intensity.N)
        axes[0].clear()
        axes[0].plot(x, intensity.value[int(intensity.N / 2), :], "r")  # for 2d mode
        axes[1].imshow(intensity.value, cmap="gist_heat")
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
            N=300,
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
