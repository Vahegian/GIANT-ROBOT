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
TOLERANCE = 0.8
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


    # Returns (R, G, B) from name
    def name_to_color(self, name):
        # Take 3 first letters, tolower()
        # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
        color = [(ord(c.lower())-97)*8 for c in name[:3]]
        return color



    def get_loc_enc(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # This time we first grab face locations - we'll need them to draw boxes
        locations = face_recognition.face_locations(image, model=MODEL)

        # Now since we know loctions, we can pass them to face_encodings as second argument
        # Without that it will search for faces once again slowing down whole process
        encodings = face_recognition.face_encodings(image, locations)

        return locations, encodings


    def get_face_loc(self, image, locations ,encodings):
        # But this time we assume that there might be more faces in an image - we can find faces of dirrerent people
        print(f', found {len(encodings)} face(s)')
        for face_encoding, face_location in zip(encodings, locations):

            # We use compare_faces (but might use face_distance as well)
            # Returns array of True/False values in order of passed known_faces
            results = face_recognition.compare_faces(self.known_faces, face_encoding, TOLERANCE)

            # Since order is being preserved, we check if any face was found then grab index
            # then label (name) of first matching known face withing a tolerance

            match = None
            if True in results:  # If at least one is true, get a name of first of found labels
                match = self.known_names[results.index(True)]
                print(f' - {match} from {results}')

                # Each location contains positions in order: top, right, bottom, left
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])

                # Get color by name using our fancy function
                color = self.name_to_color(match)

                # Paint frame
                image = cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

                # Now we need smaller, filled grame below for a name
                # This time we use bottom in both corners - to start from bottom and move 50 pixels down
                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2] + 22)

                # Paint frame
                image = cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

                # Wite a name
                image = cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

                return image, face_location[3], face_location[1], True
        return image, 60, 60, False