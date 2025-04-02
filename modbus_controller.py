from pymodbus.client import ModbusSerialClient

class ModbusController:
    def __init__(self, port , baudrate=115200):
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


def get_available_com_ports():
    """Scans the system for available COM ports and returns a list."""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]
