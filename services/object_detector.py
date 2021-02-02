# from app import pose_detection
# from imageai import Detection
# import numpy as np
# from base64 import b64decode
# from io import BytesIO
# from PIL import Image
# import re

# yolo = Detection.ObjectDetection()
# yolo.setModelTypeAsYOLOv3()
# yolo.setModelPath('saved_weights_and_models/yolo.h5')
# yolo.loadModel()

# SUSPICIOUS_OBJECTS = ['laptop', 'keyboard', 'remote', 'mouse', 'cell phone', 'book']

# def load_image_file(file, mode="RGB"):
#     im = Image.open(file)
#     if mode:
#         im = im.convert(mode)
#     return im

# def object_detection(image):
#     image = re.sub("^data:image/.+;base64,", "", image)
#     image_str = b64decode(image)
#     byte_image = BytesIO(image_str)

#     originalImage = load_image_file(byte_image)
#     ## predict yolo
#     img, preds = yolo.detectObjectsFromImage(input_image=originalImage, 
#                       custom_objects=None, input_type="array",
#                       output_type="array",
#                       minimum_percentage_probability=60,
#                       display_percentage_probability=False,
#                       display_object_name=True)
#     dangerous_detection = False
#     for pred in preds:
#         if pred['name'] in SUSPICIOUS_OBJECTS:
#             dangerous_detection = True
#             break
#     return dangerous_detection