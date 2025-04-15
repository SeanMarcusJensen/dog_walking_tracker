from multiprocessing.util import Finalize
import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLO model
model = YOLO("hand_gesture.pt")


def detect_hand_gesture(frame):
    event = None
    results = model(frame)[0]
    for r in results.boxes:
        cls = int(r.cls[0])
        label = model.names[cls]

        if label == "B":
            event = "poo"
        elif label == "T":
            event = 'pee'

    return event
