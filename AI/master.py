from CameraIO import OpenCamera, WIDTH
from robot_controller import RobotControl
from face_detector import FaceDetector
import cv2
import time
import threading

class Master:
    def __init__(self, camera):
        super().__init__()
        self.left, self.right, self.face  = 60,60,False
        self.comloc = threading.Lock()
        self.__oc = camera

        self.__robot = RobotControl()
        self.__robot.connect()
        self.__robot.activate_command_control()
        self.__robot.move()
        time.sleep(1)
        # rt = threading.Thread(target=self.send_to_robot)
        # rt.daemon = True
        # rt.start()
        self.__fd = FaceDetector()
        
        # dm = threading.Thread(target=self.draw_images)
        # dm.daemon=True
        # dm.start()
        
            # except:
                # pass

    def get_face(self):
        while True:
            beg = time.time()
            img = self.__oc.getFrame(90)
            tl, br, name = self.__fd.get_face(img)
            cur = time.time()
            yield tl, br, name, 1/(cur-beg)  
            

    def map_val(self, x, in_min=0, in_max=1000, out_min=0, out_max=100): 
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



    def send_to_robot(self, tl, br, name):
        if name =="Vahe":
            area = abs((tl[0]-br[0])*(br[1]-tl[1]))
            body_deg = int(self.map_val(area, 0, 100000, 80, 130))

            img_center = WIDTH/2
            mid_point = ((br[1]-tl[1])/2)+tl[1]
            
            head_deg = 80
            if mid_point > img_center+50:
                head_deg = int(self.map_val(mid_point, 0, WIDTH, 30,80))
            elif mid_point < img_center-50:
                head_deg = int(self.map_val(mid_point, 0, WIDTH, 80,130))

            self.__robot.set_robot_deg(head_deg, body_deg)

        self.__robot.move()
        time.sleep(0.05)
        print("\t\t\t\t\t",self.__robot.get_pot_values())
            


if __name__ == "__main__":
    m = Master()
