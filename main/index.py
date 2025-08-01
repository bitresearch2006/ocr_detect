import json
from function import ocr_detect  # assuming your ocr_detect is in ocr_detect.py

def handle(event):
    try:
        body = json.loads(event.body)
        image_b64 = body.get("image_b64", "")
        if not image_b64:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing image_b64"})
            }

        result = ocr_detect.main(image_b64)

        return {
            "statusCode": 200,
            "body": json.dumps({"text": result})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
