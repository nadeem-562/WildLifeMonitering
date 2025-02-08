from ultralytics import YOLO
import cv2
import numpy as np

def detect_and_mark(image, model):
    # Perform inference
    results = model(image)

    # Access the detections
    detections = results[0].boxes  # Get boxes from the first image result

    # Convert to numpy for easier handling
    boxes = detections.xyxy.cpu().numpy()  # Bounding box coordinates
    confidences = detections.conf.cpu().numpy()  # Confidence scores
    classes = detections.cls.cpu().numpy()  # Class predictions

    # Draw detections on the image
    for box, conf, cls in zip(boxes, confidences, classes):
        x1, y1, x2, y2 = map(int, box)
        label = f"Species {int(cls)}: {conf:.2f}"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image, boxes
