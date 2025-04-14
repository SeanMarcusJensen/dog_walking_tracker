import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")


def detect_dog_direction(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    door_line_x = frame_width // 2  # Define door threshold (center line)
    previous_positions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        dog_boxes = []
        door_boxes = []

        for r in results.boxes:
            cls = int(r.cls[0])
            label = model.names[cls]
            x1, y1, x2, y2 = map(int, r.xyxy[0])

            if label == "dog":
                dog_boxes.append((x1, y1, x2, y2))
            elif label == "door":  # Custom class — may not exist in default model
                door_boxes.append((x1, y1, x2, y2))

        if dog_boxes:
            # Track centroid of the first dog box
            x1, y1, x2, y2 = dog_boxes[0]
            cx = (x1 + x2) // 2
            previous_positions.append(cx)

        # Visualize for debug (optional)
        # cv2.line(frame, (door_line_x, 0), (door_line_x, frame_height), (255, 0, 0), 2)
        # cv2.imshow("Tracking", frame)
        # if cv2.waitKey(1) == ord('q'):
        #     break

    cap.release()
    # cv2.destroyAllWindows()

    # Decide movement direction
    if len(previous_positions) < 2:
        return "unknown"

    start = previous_positions[0]
    end = previous_positions[-1]

    if start < door_line_x and end > door_line_x:
        return "in"
    elif start > door_line_x and end < door_line_x:
        return "out"
    else:
        return "unknown"
