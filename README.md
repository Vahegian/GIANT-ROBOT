# GIANT-ROBOT

Python "face_recognition" library is used for detecting and recognizing faces. The library uses the "siamese" network for recognition and returns locations of the detected faces. The location data is used to derive degrees of rotations for the robot's body and head. These are then transmitted over a serial port to the Arduino board which rotates the correct servos and returns the new position of the robot.
 
The robot's positional data can be used for coding a PID controller to make the robot's motions smoother, or it can be used for creating a reinforcement learning agent to teach the robot how to move. Both will be implemented in the future.
 
There is no kinematic or inverse kinematic model for the robot since the motion space is very simple, but as it gets more complex I will create one.
 
The UI is done with HTML and JS. Flask is used for serving static files and SocketIO is used for streaming the camera footage.
 
There is a Dockerfile you can use to create the environment with correct dependencies (must have docker-nvidia installed) and 3d models to print the robot parts (use 9g servos and 10K potentiometers for "encoders")
 
For face recognition to work use this folder structure:

    AI
    |_ private
            |_ name1
                |_ picture_of_face_1.jpg
                        …
            |_ name2
                |_ ....

To start the system type "python3.7 start.py" inside docker container under folder "AI" and on host locate "localhost:10000"