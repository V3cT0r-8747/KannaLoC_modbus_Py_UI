from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from modbus_controller import ModbusController

class UiMainwindow(object):
    def __init__(self):
        self.toggleAllButton = None
        self.mainLayout = None
        self.centralwidget = None
        self.widget = None
        self.horizontalLayout = None
        self.indicators = None
        self.checkboxes = None
        self.statusbar = None
        self.modbus_controller = ModbusController()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 150)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.checkboxes = []
        self.indicators = []

        for i in range(8):
            container = QWidget(parent=self.widget)
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)

            indicator = QLabel(parent=container)
            indicator.setFixedSize(20, 20)
            indicator.setStyleSheet("background-color: grey; border: 1px solid black; border-radius: 10px;")
            layout.addWidget(indicator, alignment=Qt.AlignmentFlag.AlignCenter)

            label = QLabel(f"LED {i}", parent=container)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

            checkbox = QtWidgets.QCheckBox(parent=container)
            checkbox.setChecked(False)
            checkbox.setObjectName(f"checkBox_{i}")
            checkbox.setText(f"D{i}")
            checkbox.stateChanged.connect(lambda state, x=i, cb=checkbox: self.checkbox_toggled(x, cb))
            layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

            self.horizontalLayout.addWidget(container)
            self.checkboxes.append(checkbox)
            self.indicators.append(indicator)

        self.mainLayout.addWidget(self.widget)

        self.toggleAllButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.toggleAllButton.setObjectName("toggleAllButton")
        self.toggleAllButton.setText("Toggle All On/Off")
        self.toggleAllButton.clicked.connect(self.toggle_all)
        self.mainLayout.addWidget(self.toggleAllButton, alignment=Qt.AlignmentFlag.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    def toggle_all(self):
        all_checked = all(checkbox.isChecked() for checkbox in self.checkboxes)
        for checkbox in self.checkboxes:
            checkbox.setChecked(not all_checked)

    def checkbox_toggled(self, index, checkbox):
        status = checkbox.isChecked()
        self.modbus_controller.write_coil("1",status)
        print(f"LED {index} was toggled {status}")


        if checkbox.isChecked():
            self.indicators[index].setStyleSheet(
                "background-color: green; border: 1px solid black; border-radius: 10px;")
        else:
            self.indicators[index].setStyleSheet(
                "background-color: grey; border: 1px solid black; border-radius: 10px;")


class MainApp(QMainWindow, UiMainwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
