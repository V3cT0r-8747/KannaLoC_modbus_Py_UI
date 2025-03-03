import sys

from PyQt6 import QtWidgets
from LED_controller_UI import MainApp  # Importing the UI class

from pymodbus.client import AsyncModbusSerialClient
client = AsyncModbusSerialClient(port= "COM4", timeout=1, baudrate=115200, bytesize=8, stopbits=1, parity="N")
client.connect()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())

