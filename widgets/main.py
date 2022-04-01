from PyQt5.QtWidgets import QMainWindow
import matplotlib
from widgets.plot import Plot, ToolBar
from assets.MainWindow import Ui_MainWindow

matplotlib.use('Qt5Agg')


class Main(QMainWindow, Ui_MainWindow):
    wavelength = 500
    reflection = 0.7

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tb = None
        self.plot = None
        self.setupUi(self)
        self.init_plots()

    def update_plots(self):
        self.plot.update_parameters(self.wavelength, self.reflection)
        self.plot1Grid.removeWidget(self.plot)
        self.plot = Plot(self.wavelength, self.reflection)
        self.plot1Grid.addWidget(self.plot)
        self.plot1Grid.removeWidget(self.tb)
        self.tb = ToolBar(self.plot)
        self.plot1Grid.addWidget(self.tb)

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
            reflection=self.reflection
        )
        self.plot1Grid.addWidget(self.plot)


        self.horizontalSlider.valueChanged.connect(lambda y: self.change_wavelength(y))
        self.horizontalSlider_2.valueChanged.connect(lambda y: self.change_reflection(y))
