# -*- coding: utf-8 -*-
from flask import Flask
from flask_socketio import SocketIO
from services import facial_recognition
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


if __name__ == "__main__":
    socketio.run(app, debug=DEBUG, port=PORT)