from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import json
import numpy as np
import cv2
import base64
from CameraIO import OpenCamera
import time
from master import Master, CAM_ROTATION_DEG



oc = OpenCamera()
oc.daemon = True
oc.start()
m = Master(oc)


app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def root():
    return app.send_static_file('index.html')


@socketio.on('face')
def send_face_data(msg):
    for tl, br, name, fps in m.get_face():
        emit("face", {"tl":tl, "br":br, "name":name, "fps":fps})
        m.send_to_robot(tl,br,name)

@socketio.on('image')
def send_data(msg):
    while True:
        is_success, im_buf_arr = cv2.imencode(".jpg", oc.getFrame(CAM_ROTATION_DEG))
        emit("image", im_buf_arr.tobytes())
        # time.sleep(0.01)



if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=False)
