from CameraIO import OpenCamera, WIDTH
from robot_controller import RobotControl
from face_detector import FaceDetector
import time

CAM_ROTATION_DEG = 90

class Master:
    def __init__(self, camera):
        super().__init__()
        self.__oc = camera

        self.__robot = RobotControl()
        self.__robot.connect()
        self.__robot.activate_command_control()
        self.__robot.move()
        time.sleep(1)
        self.head_deg, self.body_deg = 80, 90
        self.__fd = FaceDetector()
        

    def get_face(self):
        while True:
            beg = time.time()
            img = self.__oc.getFrame(CAM_ROTATION_DEG)
            tl, br, name = self.__fd.get_face(img)
            cur = time.time()
            yield tl, br, name, 1/(cur-beg)  
            

    def map_val(self, x, in_min=0, in_max=1000, out_min=0, out_max=100): 
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



    def send_to_robot(self, tl, br, name):
        if name !="Unknown":
            area = abs((tl[0]-br[0])*(br[1]-tl[1]))
            self.body_deg = abs(int(self.map_val(area, 1000, 300000, 80, 130)))

            img_center = WIDTH/2
            percent_diff_from_middle = ((br[1]-tl[1])/img_center)*100
            
            if tl[1] > img_center+50 and br[1] > img_center:
                self.head_deg = int(self.map_val(percent_diff_from_middle, 0, 100, 30,70))
                print(1, percent_diff_from_middle, self.head_deg)
            elif br[1] < img_center-50 and tl[1] < img_center:
                self.head_deg = int(self.map_val(percent_diff_from_middle, 0, 100, 90,130))
                print(2, percent_diff_from_middle, self.head_deg)

            self.__robot.set_robot_deg(self.head_deg, self.body_deg)

        self.__robot.move()
        time.sleep(0.05)
        print("\t\t\t\t\t",self.__robot.get_pot_values())          


if __name__ == "__main__":
    m = Master()
