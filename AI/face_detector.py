import dlib
if dlib.cuda.get_num_devices()>=1:
    print("Enabeling CUDA")
    dlib.DLIB_USE_CUDA = True
    dlib.USE_AVX_INSTRUCTIONS = True
    dlib.DLIB_USE_BLAS, dlib.DLIB_USE_LAPACK, dlib.USE_NEON_INSTRUCTIONS = True, True, True
print(dlib.DLIB_USE_CUDA, dlib.USE_AVX_INSTRUCTIONS, dlib.DLIB_USE_BLAS, dlib.DLIB_USE_LAPACK, dlib.USE_NEON_INSTRUCTIONS)
import face_recognition
import os
import cv2


KNOWN_FACES_DIR = 'private'
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model


class FaceDetector():
    def __init__(self):
        super().__init__()
        self.known_faces, self.known_names = self.explore_known_faces()
        print(len(self.known_faces), len(self.known_names))

    def explore_known_faces(self):
        print('Loading known faces...')
        known_faces = []
        known_names = []

        # We oranize known faces as subfolders of KNOWN_FACES_DIR
        # Each subfolder's name becomes our label (name)
        for name in os.listdir(KNOWN_FACES_DIR):

            # Next we load every file of faces of known person
            for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):

                # Load an image
                image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')

                # Get 128-dimension face encoding
                # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
                try:
                    encoding = face_recognition.face_encodings(image)[0]

                    # Append encodings and name
                    known_faces.append(encoding)
                    known_names.append(name)
                except Exception as e:
                    os.remove(f'{KNOWN_FACES_DIR}/{name}/{filename}')
                    print(str(e), f"\nremoved {KNOWN_FACES_DIR}/{name}/{filename}")

        return known_faces, known_names

    def get_face(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(image, model=MODEL)
        encodings = face_recognition.face_encodings(image, locations)

        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(self.known_faces, face_encoding, TOLERANCE)
            match = None
            if True in results:  # If at least one is true, get a name of first of found labels
                match = self.known_names[results.index(True)]
                # print(f' - {match} from {results}')
                # Each location contains positions in order: top, right, bottom, left
                top_left = [face_location[0], face_location[3]]
                bottom_right = [face_location[2], face_location[1]]
                return top_left, bottom_right, match
        return [0,0],[0,0], "Unknown"