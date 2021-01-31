# Online Remote Proctoring AI

### Features

1. Face Recognition
2. Face Detection
3. Brightness Detection
4. Object Detection
5. Head Pose Estimation

### Installation

1. `sh setup.sh`
2. Download [Haar Cascade File](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml), [Yolo Weight](https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5)and [Dlib face landmarks](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2) and add it to `saved_weights_and_models`

### Running

1. Create a `secret.ini` from `secret.example.ini`
2. `python3 app.py`
