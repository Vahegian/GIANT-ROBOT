from arduino_serial import ArduinoSerial

MIN_BODY_DEG = 50
MAX_BODY_DEG = 130
MIN_HEAD_DEG = 40
MAX_HEAD_DEG = 120

class RobotControl:
    def __init__(self):
        self.__control_type = 100
        self.__head_deg = 80
        self.__body_deg = 90
        self.__arduino_serial = None

    def connect(self):
        self.__arduino_serial = ArduinoSerial()

    def activate_pot_control(self):
        self.__control_type = 100
        
    def activate_command_control(self):
        self.__control_type = 101

    def get_pot_values(self): 
        self.__arduino_serial.clear_input()
        try:
            vals = []
            vals.append(int(self.__arduino_serial.read()))
            vals.append(int(self.__arduino_serial.read()))
        except Exception as e:
            print(str(e))
            return [0,0]
        return vals

    def set_robot_deg(self, head, body):
        self.__head_deg = head
        self.__body_deg = body
    
    def move(self):
        self.__arduino_serial.send([self.__control_type, self.__head_deg, self.__body_deg])


if __name__ == "__main__":
    import time
    sta = RobotControl()
    sta.connect()
    
    # sta.activate_pot_control()
    # sta.move()
    # time.sleep(0.1)
    # while True:
    #     print(sta.get_pot_values())
    #     time.sleep(0.01)


    print(sta.activate_command_control())
    time.sleep(0.1)
    while True:
        for i in reversed(range(30,130)):
            sta.set_robot_deg(i,i)
            sta.move()
            time.sleep(0.05)
            print(i, sta.get_pot_values())

        for i in range(30,130):
            sta.set_robot_deg(i,i)
            sta.move()
            time.sleep(0.05)
            print(i, sta.get_pot_values())
        
        sta.set_robot_deg(80,90)
        sta.move()