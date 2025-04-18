# First, install the necessary libraries
# pip install pytesseract Pillow

import base64
import json
import numpy as np
import cv2
from PIL import Image
import pytesseract

def ocr_detect(image_b64):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(image_b64)
        
        # Convert the decoded data to a NumPy array
        nparr = np.frombuffer(image_data, np.uint8)
        
        # Decode the NumPy array to an image
        image_rgb = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        return f"error: Failed to decode image data: {str(e)}"        

    try:
        # Perform OCR on the image
        text = pytesseract.image_to_string(image_rgb)
        return text
    except Exception as e:
        return f"error: Failed to perform OCR: {str(e)}"

