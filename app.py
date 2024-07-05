from flask import Flask, Response, render_template, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
from process import _model
import sqlite3
from database import create_frames_table  # Import the function to create the table

app = Flask(__name__)

# Load the YOLO model (initialize outside of routes)
model = YOLO("yolo/best.pt")

# Create the frames table using the function from create_db.py
create_frames_table()

# SQLite connection setup (per thread)
def get_db_connection():
    conn = sqlite3.connect('yolo_data.db')
    conn.row_factory = sqlite3.Row  # Optional: Enable accessing columns by name
    return conn

# Function to get a database cursor
def get_db_cursor(conn):
    return conn.cursor()

# Dictionary to store frames from different devices in memory
camera_frames = {}

@app.route("/")
def index():
    """
    Route to render the main HTML page.
    """
    return render_template("new.html")

def generate_frames():
    """
    Generator function to yield frames in byte format for streaming.
    Iterates through the stored frames in `camera_frames` and encodes them as JPEG.
    """
    while True:
        for device_id, frame in camera_frames.items():
            # Resize frame to a smaller resolution (e.g., 640x480)
            # frame, fire, x, y, w = model2(model, frame)  # Process frame with model (commented out)

            # Encode frame as JPEG with compression quality (0-100)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # Adjust quality as needed
            _, buffer = cv2.imencode(".jpg", frame, encode_param)
            frame_bytes = buffer.tobytes()

            # Yield the frame in byte format
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"

@app.route("/video_feed")
def video_feed():
    """
    Route to stream video feed.
    """
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/receive_frames/<device_id>", methods=["POST"])
def receive_frames(device_id):
    """
    Route to receive frames from devices, detect fire using YOLO, and save only frames with detected fire.
    
    Args:
        device_id (str): Identifier for the device sending frames.
    
    Returns:
        JSON response with fire detection results and coordinates.
    """
    frame_data = request.data

    # Convert received data to numpy array
    nparr = np.frombuffer(frame_data, np.uint8)

    # Decode numpy array as image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (640, 480))
    
    # Process the image with YOLO model
    result = model(img)
    frame, fire, x, y, w = _model(result, img)
    camera_frames[device_id] = frame

    # Only save frames where fire is detected
    if fire:
        # Get SQLite connection and cursor for the current thread
        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            # Store the processed frame in SQLite database
            insert_frame_sql = """
                              INSERT INTO frames (device_id, frame_data, fire, x, y, w)
                              VALUES (?, ?, ?, ?, ?, ?)
                              """
            frame_data_blob = cv2.imencode(".jpg", frame)[1].tobytes()
            values = (device_id, sqlite3.Binary(frame_data_blob), fire, x, y, w)
            cursor.execute(insert_frame_sql, values)
            conn.commit()

            # Store the processed frame in memory (optional)

        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()

    return jsonify({"fire": fire, "x": x, "y": y, "w": w})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000, use_reloader=False)
