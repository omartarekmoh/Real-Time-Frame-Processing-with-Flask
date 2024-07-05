# Real-Time Frame Processing with Flask

This project captures frames from a webcam, processes them to detect fire, and sends the processed frames to a Flask server.

## Files

- `app.py`: Captures frames from the webcam and sends them to the Flask server.
- `process.py`: Contains the function to process the frames and detect fire.
- `send.py`: (Duplicate of app.py) Captures and sends frames to the Flask server.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/omartarekmoh/Real-Time-Frame-Processing-with-Flask.git
    cd Real-Time-Frame-Processing-with-Flask
    ```

2. Install the required libraries:
    ```bash
    pip install opencv-python requests numpy cvzone Flask ultralytics
    ```

## Usage

1. Ensure you have a Flask server running to receive the frames.

2. To start the server, run:
    ```bash
    python app.py
    ```

3. To start capturing and sending frames, run:
    ```bash
    python send.py
    ```

4. Make sure CUDA is available on your system to leverage GPU acceleration for the YOLO model.

5. If you want to change the camera used, edit `send.py` and change the number in the following line to the index of your desired camera:
    ```python
    cap = cv2.VideoCapture(0)
    ```

## Project Overview

### app.py / send.py

- These scripts capture frames from the default webcam.
- The captured frames are encoded as JPEG images.
- The encoded frames are sent to a specified Flask server URL.

### process.py

- This script contains a function to process the frames and detect fire.
- It uses `cvzone` and `cv2` for image processing.
- Detected fire areas are highlighted with a rectangle and labeled with a confidence score.

This project demonstrates real-time frame capture, processing, and transmission using OpenCV and Flask.
