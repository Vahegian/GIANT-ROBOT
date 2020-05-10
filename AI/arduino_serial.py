import time

import serial as port
import threading
import os

'''
This class takes a object that has an array 'handPos'
and transmits the array via serial port to connected
devices.
'''
# set access privileges of serial ports
# ls /dev/serial/by-path
# sudo chmod 666 /dev/serial/by-path/****

class ArduinoSerial:
    def __init__(self, serial_port:str='/dev/serial/by-path/pci-0000:0b:00.3-usb-0:1.4.3:1.0'):
        # os.chdir(os.path.expanduser("~"))
        self.port = serial_port
        # os.chmod('/dev/serial/by-path/pci-0000:00:14.0-usb-0:2:1.0',666)
        try:
            self.arduinoPort = port.Serial(self.port, 9600, timeout=1)
            while self.read() != "1000":
                time.sleep(0.1)
            time.sleep(0.1)
            print(f"serial connected on {self.port}")
        except Exception as e:
            print(f"Nothing is Connected to Serial Port > {self.port} \n {e}")

    def send(self, msg:list):
        return self.arduinoPort.write(msg)
        

    def read(self):
        received_message = self.arduinoPort.readline()
        received_message = received_message.decode()
        received_message = received_message.strip()
        return received_message

    def clear_input(self):
        self.arduinoPort.flushInput()


