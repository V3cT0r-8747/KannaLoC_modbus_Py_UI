import pymodbus
from pymodbus.client import ModbusSerialClient


class ModbusController:
    def __init__(self, port = "COM6", baudrate=115200):
        self.client = ModbusSerialClient(port = port, timeout=1, baudrate=baudrate, bytesize=8, stopbits=1, parity="N")
        self.client.connect()

    def write_coil(self, address, value):
        # turn LED ON/OFF by writing to a Modbus coil
        try:
            self.client.write_coil(address, value, slave = 1)
            print(f"Written to coil: Address={address}, Data = {value}")
        except Exception as e:
            print(f"Error sending modbus packet:{e}")

    def close(self):
        self.client.close()

