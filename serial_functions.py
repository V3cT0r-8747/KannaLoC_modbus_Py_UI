import serial.tools.list_ports

def get_available_com_ports():
    # scan and return available ports
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]