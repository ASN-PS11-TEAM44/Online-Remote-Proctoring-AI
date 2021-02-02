import cv2
import numpy as np
from base64 import b64decode
from io import BytesIO
from PIL import Image
import re

# Load the frontal face cascade
face_cascade = cv2.CascadeClassifier(
    "saved_weights_and_models/haarcascade_frontalface_default.xml"
)
profile_cascade = cv2.CascadeClassifier('saved_weights_and_models/haarcascade_profileface.xml')


def load_image_file(file, mode="RGB"):
    im = Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)


def face_detector(image):
    image = re.sub("^data:image/.+;base64,", "", image)
    image_str = b64decode(image)
    byte_image = BytesIO(image_str)

    originalImage = load_image_file(byte_image)

    gray = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 1:
        return True, ""
    if len(faces) == 0:
        profile_faces = profile_cascade.detectMultiScale(gray, 1.3, 5)
        if len(profile_faces) == 1:
            return True, ""
        if len(profile_faces) == 0:
            return False, "No face is detected"
    return False, "Multiple faces are detected"