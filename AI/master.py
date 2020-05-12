from CameraIO import OpenCamera
from robot_controller import RobotControl
from face_detector import FaceDetector
import cv2
import time
import threading

class Master:
    def __init__(self):
        super().__init__()
        self.left, self.right, self.face  = 60,60,False
        self.comloc = threading.Lock()
        self.__oc = None
        self.__robot = RobotControl()
        self.__robot.connect()
        self.__robot.activate_command_control()
        self.__robot.move()
        time.sleep(1)
        rt = threading.Thread(target=self.send_to_robot)
        rt.daemon = True
        rt.start()

        self.start_camera()
        self.__fd = FaceDetector()
        
        dm = threading.Thread(target=self.draw_images)
        dm.daemon=True
        dm.start()

        while True:
            time.sleep(0.1)
        
        
            # except:
                # pass

    def start_camera(self):
        if self.__oc is None:
            self.__oc = OpenCamera()
            self.__oc.daemon = True
            self.__oc.start()
        return True

    def draw_images(self):
        while True:
            img = self.__oc.getFrame(90)
            img = cv2.resize(img, (160, 120))
            l,e = self.__fd.get_loc_enc(img)
            img, left, right, face = self.__fd.get_face_loc(img, l, e)
            
            with self.comloc:
                self.left, self.right, self.face = left,right,face
            
            print("\t\t\t\tUpdate",left,right,face)
            time.sleep(0.1)
            img = cv2.resize(img, (320, 240))
            # try:

            cv2.imshow("win", img)
            cv2.waitKey(1)

    def send_to_robot(self):
        deg = 80
        while True:
            # with self.comloc:
            left, right, face = self.left, self.right, self.face
            print("\t\t\t\tconsume", left, right, face)
            if face:
                # mid = int((right-left)/2)
                # mid += int(0.3*mid)
                # val = abs(60-mid)
                deg = 130-left
                # if left > 60:
                #     deg = int(80-left)
                # else:
                #     deg = int(80+left)
                self.__robot.set_robot_deg(deg, 90)
                print("\t\t\t\t", left, right) 
            print(deg)
            self.__robot.move()
            time.sleep(0.05)
            print("\t\t\t\t\t",self.__robot.get_pot_values())


if __name__ == "__main__":
    m = Master()
