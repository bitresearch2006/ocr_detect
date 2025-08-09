import base64
import numpy as np
import cv2
import pytesseract
import logging
import os

def setup_logger(log_dir, diagnostics=False):
    logger = logging.getLogger("ocr_logger")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not diagnostics or logger.handlers:
        return logger

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "ocr_detect.log")

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def log(logger, level, msg, diagnostics=False):
    if diagnostics and logger:
        logger.log(level, msg)

def handle(image_b64):
    # Read env vars
    diagnostics = os.getenv("DIAGNOSTICS", "false").lower() == "true"
    log_dir = os.getenv("LOG_DIR", "/tmp")
    logger = setup_logger(log_dir, diagnostics)

    try:
        log(logger, logging.INFO, "Decoding base64 image", diagnostics)
        image_data = base64.b64decode(image_b64)
        nparr = np.frombuffer(image_data, np.uint8)
        image_rgb = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        log(logger, logging.INFO, "Image decoded successfully", diagnostics)
    except Exception as e:
        log(logger, logging.ERROR, f"Failed to decode image data: {e}", diagnostics)
        return f"error: Failed to decode image data: {str(e)}"

    try:
        log(logger, logging.INFO, "Running OCR", diagnostics)
        text = pytesseract.image_to_string(image_rgb)
        log(logger, logging.INFO, f"OCR result: {text.strip()}", diagnostics)
        return text
    except Exception as e:
        log(logger, logging.ERROR, f"Failed to perform OCR: {e}", diagnostics)
        return f"error: Failed to perform OCR: {str(e)}"
