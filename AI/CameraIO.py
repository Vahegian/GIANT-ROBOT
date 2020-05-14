import threading
import cv2
# import tkinter as tk
import numpy as np

'''
30 Dec. 2018 : Vahe Grigoryan

The class constructor asks user to chose a camera option and
with a new thread it captures frames from the selected camera.
The captured frames can be obtained with a call to "getFrame" method
'''


WIDTH = 480
HEIGHT = 640


class OpenCamera(threading.Thread):
    def __init__(self, select_cam: bool = False):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.img = None
        self.video_capture = None
        if select_cam:
            self.createDialogBox()
        else:
            self.selectCam(0)

    def selectCam(self, id):
        self.video_capture = cv2.VideoCapture(id)
        print("Camera {} selected".format(id))

    def createDialogBox(self):
        tk.Button(text='Internal', command=self.selectMainCam, height=3, width=21).pack()
        tk.Button(text='External', command=self.selectSecondaryCam, height=3, width=21).pack()
        tk._default_root.title("Select Camera")
        tk.mainloop()

    def selectMainCam(self):
        self.video_capture = cv2.VideoCapture(0)
        tk._default_root.destroy()
        print("Internal Camera selected")

    def selectSecondaryCam(self):
        self.video_capture = cv2.VideoCapture(1)
        tk._default_root.destroy()
        print("External Camera selected")

    def __rotate_img(self, mat, angle):
        height, width = mat.shape[:2] # image shape has 3 dimensions
        image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0,0]) 
        abs_sin = abs(rotation_mat[0,1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w/2 - image_center[0]
        rotation_mat[1, 2] += bound_h/2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        return cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

    def getFrame(self, rotation_degree: int = None):
        self.lock.acquire()
        picture = self.img
        self.lock.release()

        if rotation_degree != None and picture is not None:
            picture = self.__rotate_img(picture, rotation_degree)
        elif picture is None:
            return np.ones((HEIGHT,WIDTH))

        return picture

    def run(self):
        while True:
            ret, frame = self.video_capture.read()
            # self.img = cv2.resize(frame, (100, 100), interpolation=cv2.INTER_AREA)
            # print(frame.shape)
            self.img = cv2.resize(frame, (HEIGHT, WIDTH))
            self.lock.acquire()
            self.img = frame
            self.lock.release()

if __name__ == "__main__":
    cio = OpenCamera()
    # cio.daemon = True
    cio.start()
