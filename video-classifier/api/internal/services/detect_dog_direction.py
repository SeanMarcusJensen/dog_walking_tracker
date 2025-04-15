from multiprocessing.util import Finalize
import cv2
import numpy as np
from ultralytics import YOLO
from .hand_gesture_detection import detect_hand_gesture

# Load YOLO model
model = YOLO("yolo11n.pt")


def detect_dog_direction(video_path, debug=False):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define door threshold (center line)
    door_line_y = frame_height // 2 + 100
    previous_positions = []
    events = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        dog_boxes = []
        door_boxes = []
        events = []

        for r in results.boxes:
            cls = int(r.cls[0])
            label = model.names[cls]
            x1, y1, x2, y2 = map(int, r.xyxy[0])

            if label == "dog":
                dog_boxes.append((x1, y1, x2, y2))
            elif label == "door":  # Custom class — may not exist in default model
                door_boxes.append((x1, y1, x2, y2))
            elif label == "person":
                cropped = frame[y1:y2, x1:x2]
                event = detect_hand_gesture(cropped)
                if event == "B":
                    events.append("poo")
                elif event == "T":
                    events.append("pee")

        if dog_boxes:
            # Track centroid of the first dog box
            x1, y1, x2, y2 = dog_boxes[0]
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            previous_positions.append(cy)

        # Finalize for debug(optional)
        if debug:
            cv2.line(frame, (0, door_line_y),
                     (frame_width, door_line_y), (255, 0, 0), 2)
            cv2.imshow("Tracking", frame)
            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()
    if debug:
        cv2.destroyAllWindows()

    # Decide movement direction
    if len(previous_positions) < 2:
        return "unknown", []

    start = previous_positions[0]
    end = previous_positions[-1]

    if start < door_line_y and end > door_line_y:
        return "in", events
    elif start > door_line_y and end < door_line_y:
        return "out", []
    else:
        return "unknown", []
