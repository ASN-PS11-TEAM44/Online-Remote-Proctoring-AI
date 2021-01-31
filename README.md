# Online Remote Proctoring AI

### Features

1. Face Recognition
2. Face Detection
3. Brightness Detection
4. Object Detection

### Installation

1. `sh setup.sh`
2. Download [Haar Cascade File](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml) amd [Yolo Weight](https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5) and add it to `saved_weights_and_models`

### Running

1. Create a `secret.ini` from `secret.example.ini`
2. `python3 app.py`
