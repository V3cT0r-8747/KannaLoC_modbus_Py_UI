import sys

from PyQt6 import QtWidgets
from LED_controller_UI import MainApp  # Importing the UI class


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())