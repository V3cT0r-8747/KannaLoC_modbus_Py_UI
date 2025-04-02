import serial.tools.list_ports

def get_available_com_ports():
    # Scan and return the available ports on a Windows 10/11 system
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]