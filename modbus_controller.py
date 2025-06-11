from pymodbus.client import ModbusSerialClient

LED_REGISTER_ADDRESS = 0x0001  # LED address on Microblaze system side

class ModbusController:
    def __init__(self, port , baudrate=115200):
        self.client = ModbusSerialClient(port = port, timeout=1, baudrate=baudrate, bytesize=8, stopbits=1, parity="N")
        self.client.connect()

    def write_register(self, value):
        try:
            self.client.write_register(LED_REGISTER_ADDRESS,value,slave=1, no_response_expected= True)
            print(f"Write to holding register: Address={LED_REGISTER_ADDRESS}, Data = {value}")
        except Exception as e:
            print(f"Error sending modbus packet:{e}")

