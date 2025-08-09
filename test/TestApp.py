import base64
import os
import sys

# Add the path to the 'main' directory so we can import handler.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main')))

from handler import handle

IMAGE_FILE = "ocr-1.png"  # Make sure this file is in the same directory as TestApp.py

# Load image and convert to base64
with open(IMAGE_FILE, "rb") as image_file:
    image_data = image_file.read()
    image_b64 = base64.b64encode(image_data).decode("utf-8")

# Optional: set env vars for logging
os.environ["DIAGNOSTICS"] = "true"
os.environ["LOG_DIR"] = "/tmp/ocr_logs"

# Call the OCR function directly
result = handle(image_b64)

# Print the result
print("Function returned:")
print(result)
