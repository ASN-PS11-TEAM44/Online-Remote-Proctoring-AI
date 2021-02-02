# -*- coding: utf-8 -*-
from flask import Flask
from flask_socketio import SocketIO
from services import facial_recognition, brightness_detector, face_detector, object_detector, pose_estimation
import configparser

config = configparser.ConfigParser()
config.read("secret.ini")

app = Flask(__name__)


PORT = config.get("APP", "PORT")
DEBUG = config.get("APP", "DEBUG") == "True"
app.config["SECRET_KEY"] = config.get("APP", "SECRET_KEY")
socketio = SocketIO(app)


@socketio.on("face verification")
def face_verification(image1, image2):
    try:
        response = facial_recognition.facial_verification_for_auth(
            image1=image1, image2=image2
        )
        return response
    except:
        return False


@socketio.on("brightness detector")
def brightness_validator(image):
    try:
        response = brightness_detector.detect_brightness(image)
        return response
    except:
        return False


@socketio.on("face detector")
def face_detection(image):
    try:
        response = face_detector.face_detector(image)
        return response
    except:
        return False, "No face is detected"

@socketio.on("object detector")
def object_detection(image):
    try:
        # response = object_detector.object_detection(image)
        return False
    except:
        return False

@socketio.on("pose detector")
def pose_detection(image):
    try:
        response = pose_estimation.pose_estimation(image)
        print(response)
        return response
    except:
        return True, ""


if __name__ == "__main__":
    socketio.run(app, debug=DEBUG, port=PORT)