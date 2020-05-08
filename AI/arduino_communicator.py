import time

import serial as port
import threading
import os

'''
03.Jan.2019 : Vahe Grigoryan

This class takes a object that has an array 'handPos'
and transmits the array via serial port to connected
devices.
'''
# set access privileges of serial ports
# ls /dev/serial/by-path
# sudo chmod 666 /dev/serial/by-path/****

class SerialToArduino:
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.message_to_sendLock = threading.Lock()
        # os.chdir(os.path.expanduser("~"))
        self.port = '/dev/serial/by-path/pci-0000:0b:00.3-usb-0:1.4.3:1.0'
        # os.chmod('/dev/serial/by-path/pci-0000:00:14.0-usb-0:2:1.0',666)
        try:
            self.arduinoPort = port.Serial(self.port, 9600)
            while self.read() != "1000":
                time.sleep(0.1)
            print(f"serial connected on {self.port}")
        except Exception as e:
            print(f"Nothing is Connected to Serial Port > {self.port} \n {e}")

    def send(self, msg):
        return self.arduinoPort.write(msg)
        

    def read(self):
        received_message = self.arduinoPort.readline()
        received_message = received_message.decode()
        received_message = received_message.strip()
        return received_message

    def __change_control_type(self, code: int):
        self.arduinoPort.flushInput()
        if self.send(str.encode(f"{code}\n")) > 0:
            if self.read() == f"{code}":
                return True
            return False
        return False

    def activate_pot_control(self):
        return self.__change_control_type(100)
        
    def activate_command_control(self):
        return self.__change_control_type(101)

    def get_pot_values(self):
        time.sleep(0.1)
        if self.send(str.encode(f"{102}\n")) > 0:
            time.sleep(1)
            vals = self.read().split(":")
            try:
                vals[0] = int(vals[0])
                vals[1] = int(vals[1])
            except:
                return [0,0]
            return vals

sta = SerialToArduino()
print(sta.activate_pot_control())
time.sleep(1)
# print(sta.activate_command_control())
# time.sleep(1)
for i in range(1000):
    print(i, sta.get_pot_values())

print(sta.activate_pot_control())
