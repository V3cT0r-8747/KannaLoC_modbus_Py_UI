from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QPushButton
from modbus_controller import ModbusController
from serial_functions import get_available_com_ports


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
        self.modbus_controller = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 200)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title Label
        self.titleLabel = QLabel("Kanna_LOC LED Controller", parent=self.centralwidget)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 14pt; font-weight: bold;")
        self.mainLayout.addWidget(self.titleLabel)

        # COM Port Selection Layout
        self.comPortLayout = QHBoxLayout()
        self.comPortDropdown = QComboBox(parent=self.centralwidget)
        self.comPortDropdown.setFixedSize(150, 25)
        self.refresh_com_ports()
        self.comPortLayout.addWidget(self.comPortDropdown)

        self.refreshButton = QPushButton("Refresh", parent=self.centralwidget)
        self.refreshButton.setFixedSize(70, 25)
        self.refreshButton.clicked.connect(self.refresh_com_ports)
        self.comPortLayout.addWidget(self.refreshButton)

        self.mainLayout.addLayout(self.comPortLayout)

        # Connection buttons layout
        self.connectionLayout = QHBoxLayout()
        self.connectButton = QPushButton("Connect", parent=self.centralwidget)
        self.connectButton.setFixedSize(70, 25)
        self.connectButton.clicked.connect(self.init_modbus)
        self.connectionLayout.addWidget(self.connectButton)

        self.disconnectButton = QPushButton("Disconnect", parent=self.centralwidget)
        self.disconnectButton.setFixedSize(70, 25)
        self.disconnectButton.clicked.connect(self.disconnect_modbus)
        self.connectionLayout.addWidget(self.disconnectButton)

        self.mainLayout.addLayout(self.connectionLayout)

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

    # Refresh list of valid COM ports
    def refresh_com_ports(self):
        self.comPortDropdown.clear()
        available_ports = get_available_com_ports()
        if available_ports:
            self.comPortDropdown.addItems(available_ports)
        else:
            self.comPortDropdown.addItem("No serial ports found")

    # Initialise UART connection with selected COM port
    def init_modbus(self):
        selected_port = self.comPortDropdown.currentText()
        if "COM" in selected_port:
            self.modbus_controller = ModbusController(selected_port)
            self.statusbar.showMessage(f"Connected to {selected_port}")
        else:
            self.statusbar.showMessage("Select a valid COM port")

    # Disconnect from Serial Port
    def disconnect_modbus(self):
        if self.modbus_controller:
            self.modbus_controller = None
            self.statusbar.showMessage("Disconnected from Kanna_LOC")
        else:
            self.statusbar.showMessage("No active connection")



    def toggle_all(self):
        if self.modbus_controller:
            all_checked = all(checkbox.isChecked() for checkbox in self.checkboxes)
            for checkbox in self.checkboxes:
                checkbox.setChecked(not all_checked)
        else:
            self.statusbar.showMessage("Error: Connect to Kanna_LOC first")


    def checkbox_toggled(self, index, checkbox):
        if self.modbus_controller:
            status = checkbox.isChecked()
            self.modbus_controller.write_coil("1", status)
            print(f"LED {index} was toggled {status}")

            if status:
                self.indicators[index].setStyleSheet(
                    "background-color: green; border: 1px solid black; border-radius: 10px;")
            else:
                self.indicators[index].setStyleSheet(
                    "background-color: grey; border: 1px solid black; border-radius: 10px;")
        else:
            self.statusbar.showMessage("Error: Connect to Kanna_LOC first")


class MainApp(QMainWindow, UiMainwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
