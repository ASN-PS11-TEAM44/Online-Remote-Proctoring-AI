""" Credits
https://medium.com/analytics-vidhya/real-time-head-pose-estimation-with-opencv-and-dlib-e8dc10d62078
https://github.com/by-sabbir/HeadPoseEstimation
"""

import os
import cv2
import dlib
import numpy as np
from base64 import b64decode
from io import BytesIO
from PIL import Image
import re
import face_recognition

PREDICTOR_PATH = os.path.join("saved_weights_and_models", "shape_predictor_68_face_landmarks.dat")
FOCAL_LENGTH_OF_CAMERA = 1

def ref3DModel():
    modelPoints = [[0.0, 0.0, 0.0],
                   [0.0, -330.0, -65.0],
                   [-225.0, 170.0, -135.0],
                   [225.0, 170.0, -135.0],
                   [-150.0, -150.0, -125.0],
                   [150.0, -150.0, -125.0]]
    return np.array(modelPoints, dtype=np.float64)


def ref2dImagePoints(shape):
    imagePoints = [[shape.part(30).x, shape.part(30).y],
                   [shape.part(8).x, shape.part(8).y],
                   [shape.part(36).x, shape.part(36).y],
                   [shape.part(45).x, shape.part(45).y],
                   [shape.part(48).x, shape.part(48).y],
                   [shape.part(54).x, shape.part(54).y]]
    return np.array(imagePoints, dtype=np.float64)


def refCameraMatrix(fl, center):
    mat = [[fl, 1, center[0]],
                    [0, fl, center[1]],
                    [0, 0, 1]]
    return np.array(mat, dtype=np.float)

def load_image_file(file, mode="RGB"):
    im = Image.open(file)
    if mode:
        im = im.convert(mode)
    return np.array(im)

def pose_estimation(image):
    image = re.sub("^data:image/.+;base64,", "", image)
    image_str = b64decode(image)
    byte_image = BytesIO(image_str)
    img = load_image_file(byte_image)
    predictor = dlib.shape_predictor(PREDICTOR_PATH)
    GAZE = "No face is detected"
    faces = face_recognition.face_locations(img, number_of_times_to_upsample=1, model="cnn")

    face3Dmodel = ref3DModel()

    for face in faces:

        #Extracting the co cordinates to convert them into dlib rectangle object
        x = int(face[3])
        y = int(face[0])
        w = int(abs(face[1]-x))
        h = int(abs(face[2]-y))
        u=int(face[1])
        v=int(face[2])
        newrect = dlib.rectangle(x,y,u,v)
        shape = predictor(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), newrect)
        refImgPts = ref2dImagePoints(shape)

        height, width, channels = img.shape
        focalLength = FOCAL_LENGTH_OF_CAMERA * width
        cameraMatrix = refCameraMatrix(focalLength, (height / 2, width / 2))
        mdists = np.zeros((4, 1), dtype=np.float64)
        # Calculate rotation and translation vector using solvePnP
        success, rotationVector, translationVector = cv2.solvePnP(face3Dmodel, refImgPts, cameraMatrix, mdists)

        noseEndPoints3D = np.array([[0, 0, 1000.0]], dtype=np.float64)
        noseEndPoint2D, jacobian = cv2.projectPoints(noseEndPoints3D, rotationVector, translationVector, cameraMatrix, mdists)
        # calculating euler angles
        rmat, jac = cv2.Rodrigues(rotationVector)
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
        x = np.arctan2(Qx[2][1], Qx[2][2])
        y = np.arctan2(-Qy[2][0], np.sqrt((Qy[2][1] * Qy[2][1] ) + (Qy[2][2] * Qy[2][2])))
        z = np.arctan2(Qz[0][0], Qz[1][0])
        print(angles[1])
        if angles[1] < -15:
            GAZE = "User is looking left"
            return False, GAZE
        elif angles[1] > 15:
            GAZE = "User is looking right"
            return False, GAZE
        else:
            GAZE = ""
            return True, GAZE
    return False, GAZE