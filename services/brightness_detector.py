import cv2
import numpy as np
from base64 import b64decode
from io import BytesIO
from PIL import Image
import re

BRIGHTNESS_THRESHOLD = 30

def load_image_file(file, mode="RGB"):
    im = Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)


def detect_brightness(image):
    image = re.sub("^data:image/.+;base64,", "", image)
    image_str = b64decode(image)
    byte_image = BytesIO(image_str)

    originalImage = load_image_file(byte_image)
    hsvImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2HSV)
    val = hsvImage[:, :, 2]
    brightness = np.mean(val)
    adjustedScaleBrightness = round((brightness / 255) * 100, 2)
    if adjustedScaleBrightness > BRIGHTNESS_THRESHOLD:
        return True
    return False