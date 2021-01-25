from base64 import b64decode
from io import BytesIO
from face_recognition import face_encodings, compare_faces
import numpy as np
import PIL
import re


def load_image_file(file, mode="RGB"):
    im = PIL.Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)


def facial_verification_for_auth(image1, image2):
    image1 = re.sub("^data:image/.+;base64,", "", image1)
    image2 = re.sub("^data:image/.+;base64,", "", image2)
    image_1_str = b64decode(image1)
    image_2_str = b64decode(image2)

    byte_1_image = BytesIO(image_1_str)
    byte_2_image = BytesIO(image_2_str)

    got_image_facialfeatures = face_encodings(load_image_file(byte_1_image))[0]
    existing_image_facialfeatures = face_encodings(load_image_file(byte_2_image))[0]
    results = compare_faces([existing_image_facialfeatures], got_image_facialfeatures)
    if results[0]:
        return True
    else:
        return False