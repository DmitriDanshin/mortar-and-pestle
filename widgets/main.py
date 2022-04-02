from PyQt5.QtWidgets import QMainWindow
import matplotlib
from widgets.plot import Plot, ToolBar
from assets.MainWindow import Ui_MainWindow

matplotlib.use('Qt5Agg')


class Main(QMainWindow, Ui_MainWindow):
    wavelength = 500
    reflection = 0.7
    distance = 3  # 0 .. 10
    n = 1.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.plot2d = None
        self.tb = None
        self.plot = None
        self.setupUi(self)
        self.init_plots()

    def update_plots(self):
        self.plot.update_parameters(self.wavelength, self.reflection, self.distance, self.n)
        self.plot1Grid.removeWidget(self.plot)
        self.plot = Plot(self.wavelength, self.reflection, self.distance, self.n)
        self.plot1Grid.addWidget(self.plot)
        self.tb = ToolBar(self.plot)

    def change_distance(self, x):
        self.distance = x / 10
        self.distance_label.setText(f"{self.distance : .2f}")
        self.update_plots()

    def change_n(self, x):
        self.n = x
        self.n_label.setText(str(x))
        self.update_plots()

    def change_reflection(self, x):
        self.reflection = x / 100
        self.reflection_label.setText(str(self.reflection))
        self.update_plots()

    def change_wavelength(self, x):
        self.wavelength = 300 + x * 15
        self.wavelength_label.setText(str(self.wavelength))
        self.update_plots()

    def init_plots(self):
        self.plot = Plot(
            wavelength=self.wavelength,
            reflection=self.reflection,
            distance=self.distance,
            n=self.n
        )

        self.plot1Grid.addWidget(self.plot)

        self.horizontalSlider.valueChanged.connect(self.change_wavelength)
        self.horizontalSlider_2.valueChanged.connect(self.change_reflection)
        self.horizontalSlider_3.valueChanged.connect(self.change_distance)
        self.doubleSpinBox.valueChanged.connect(self.change_n)
