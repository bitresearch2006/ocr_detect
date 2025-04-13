import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import os
import time
import base64
import logging
import requests

# Add the path of folder1 to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../main')))
from ocr_detect import ocr_detect

SERVER_URL = "http://34.93.156.134:5000/web_server"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_request(service, req_type, params):
    """Send request to the server and handle FUTURE_CALL polling."""
    payload = {
        "service_name": service,
        "sub_json": params,
        "request_type": req_type
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

def TestApp(image_path):
    """
    Display the results of ocr detection.
    
    Args:
        image_path: Image path.
    """   
    try:
        # Read original image
        original_image = cv2.imread(image_path)
        
        # Convert the image from BGR to RGB
        rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        # Encode the image to base64
        _, buffer = cv2.imencode('.jpg', rgb_image)
        image_b64 = base64.b64encode(buffer).decode('utf-8')
        # Create the sub_json object with image data
        image_json = {"image_b64": image_b64}
      
        # Perform OCR on the image
        #output_json = ocr_detect(image_b64)
        output_json = send_request("ocr_detect","INLINE",image_json)
        
        if output_json["status"] == "SUCCESS":
            logging.info(f"Transcription: {output_json['data']}")
        else:
            logging.error(f"Failed to perform OCR: {output_json['error']}")
            
        # Display the captured image
        # Display the image
        plt.imshow(rgb_image)
        plt.axis('off')
        plt.show()
    
    except Exception as e:
        logging.error(f"Failed to display results: {str(e)}")

# Example usage:
TestApp('ocr-1.png')
