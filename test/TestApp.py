import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import os
import time
import base64
import logging

# Add the path of folder1 to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../main')))
from ocr_detect import ocr_detect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def TestApp():
    """
    Display the results of object detection.
    
    Args:
        output_json: JSON object containing detected objects and class labels.
    """
    cap = cv2.VideoCapture(0)  # Initialize the camera
    if not cap.isOpened():
        logging.error("Failed to open camera.")
        return

    while True:    
        try:
            ret, frame = cap.read()
            if not ret:
                logging.error("Failed to capture image from camera.")
                continue
            
            # Convert the frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Encode the frame as base64
            _, buffer = cv2.imencode('.jpg', frame_rgb)
            image_b64 = base64.b64encode(buffer).decode('utf-8')
            
            # Perform OCR on the image
            output_json = ocr_detect(image_b64)
            
            logging.info(output_json)
            
            # if output_json["status"] == "SUCCESS":
                # logging.info(f"Transcription: {output_json['transcription']}")
            # else:
                # logging.error(f"Failed to perform OCR: {output_json['error']}")
                
            # Display the captured image
            cv2.imshow("Captured Image", frame_rgb)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(5)   # Sleep for 5 seconds
        
        except Exception as e:
            logging.error(f"Failed to display results: {str(e)}")

    cap.release()  # Release the camera
# Example usage:
TestApp()
