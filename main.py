import sys
from PyQt5.QtWidgets import QApplication
from widgets.main import Main

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())
