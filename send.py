import cv2
import requests
import json
from twilio.rest import Client
import requests
from message import send_location_sms

# Flask server URL
flask_server_url = "http://127.0.0.1:8000/receive_frames/device1"  # Replace with your Flask server's IP address
cap = cv2.VideoCapture(0)  # Initialize video capture object for the default camera

sentMessage = False

def send_frames_to_flask():
    """
    Capture frames from the webcam and send them to the Flask server.
    """
    global sentMessage

    while True:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:
            print("Failed to capture frame from webcam")
            break

        # Encode frame as JPEG
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        # Send frame to Flask server
        try:
            response = requests.post(
                flask_server_url,
                data=frame_bytes,
                headers={"Content-Type": "image/jpeg"},
            )
            if response.status_code != 200:
                print("Failed to send frame to Flask server:", response.status_code)
            else:
                # Parse the JSON response
                try:
                    response_data = response.json()
                    x = response_data.get('x', None)
                    y = response_data.get('y', None)
                    w = response_data.get('w', None)  # Detected object width
                    fire = response_data.get('fire', None)

                    if fire == 0:
                        print(f"x: {x}, y: {y}, w: {w}, fire: {fire}")

                    if fire == 1:
                        if not sentMessage:
                            # send_location_sms('+201069472545')
                            print("message Sent.")
                            sentMessage = True

                        if x is not None and w is not None:
                            # Define boundaries based on the detected object width
                            margin = 0.2 * w  # 20% of the object's width
                            middle_x = 320

                            left_launch_boundary = middle_x - margin
                            right_launch_boundary = middle_x + margin

                            if x < left_launch_boundary:
                                print(f"x: {x}, y: {y}, w: {w}, fire: {fire}")
                                print("left")
                            elif left_launch_boundary <= x <= right_launch_boundary:
                                print(f"x: {x}, y: {y}, w: {w}, fire: {fire}")
                                print("launch")
                            elif x > right_launch_boundary:
                                print(f"x: {x}, y: {y}, w: {w}, fire: {fire}")
                                print("right")
                except json.JSONDecodeError:
                    print("Failed to decode JSON response")
        except Exception as e:
            print("Error sending frame to Flask server:", str(e))

if __name__ == "__main__":
    send_frames_to_flask()  # Start capturing and sending frames to the Flask server
