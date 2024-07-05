import cvzone
import cv2
import math

def _model(result, frame):
    """
    Process the results from the YOLO model to detect fire in the frame and annotate the frame.
    
    Args:
        result: The output from the YOLO model, containing detection results.
        frame: The frame in which detections need to be annotated.
    
    Returns:
        tuple: The annotated frame, fire detection status, coordinates of the detected fire, and width of the bounding box.
    """
    classnames = ["Fire"]  # List of class names (only "Fire" in this case)
    x1, y1, x2, y2 = 0, 0, 0, 0  # Initialize bounding box coordinates
    fire = False  # Flag to indicate if fire is detected

    for info in result:
        boxes = info.boxes  # Get the detected bounding boxes
        for box in boxes:
            fire = True  # Set fire detection flag to True
            confidence = box.conf[0]  # Get the confidence score of the detection
            confidence = math.ceil(confidence * 100)  # Convert confidence to percentage
            Class = int(box.cls[0])  # Get the class of the detected object (index 0)
            
            if confidence > 30:  # Only consider detections with confidence greater than 30%
                x1, y1, x2, y2 = box.xyxy[0]  # Get the coordinates of the bounding box
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert coordinates to integers
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)  # Draw rectangle on the frame
                cvzone.putTextRect(
                    frame,
                    f"{classnames[Class]}",  # Label with class name and confidence
                    [x1 + 8, y1 + 100],  # Position of the label
                    scale=1.5,  # Scale of the text
                    thickness=2,  # Thickness of the text
                )

    width = x2 - x1  # Calculate the width of the bounding box

    return frame, fire, (x1 + x2) / 2, (y1 + y2) / 2, width  # Return the annotated frame, fire status, center coordinates, and width
