import cv2
from ultralytics import YOLO
from .hand_gesture_detection import detect_hand_gesture

# Load YOLO model
model = YOLO("yolo11n.pt")


def detect_dog_direction(video_path, frame_data, debug=False):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    door_frame_x = frame_data.get('x')
    door_frame_y = frame_data.get('y')
    door_frame_width = frame_data.get('width')
    door_frame_height = frame_data.get('height')
    door_frame = (door_frame_x, door_frame_y,
                  door_frame_width, door_frame_height)
    print(f"Door frame: {door_frame}")

    # Define door threshold (center line)
    door_line_lower_y = door_frame_y + door_frame_height
    door_line_y = frame_height // 2 + 100
    previous_positions = []
    events = {}  # [event, count]

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
            elif label == "person":
                event = detect_hand_gesture(frame)
                if event is None:
                    continue
                if event in events:
                    events[event] += 1
                else:
                    events[event] = 1
                print(f"Detected event: {event}")

        if dog_boxes:
            # Track centroid of the first dog box
            x1, y1, x2, y2 = dog_boxes[0]
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            previous_positions.append(cy)

        # Finalize for debug(optional)
        if debug:
            cv2.line(frame, (0, door_line_lower_y),
                     (frame_width, door_line_lower_y), (255, 0, 0), 2)
            cv2.imshow("Tracking", frame)
            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()
    if debug:
        cv2.destroyAllWindows()

    # Decide movement direction
    if len(previous_positions) < 2:
        return "unknown", {}

    start = previous_positions[0]
    end = previous_positions[-1]

    if start < door_line_lower_y and end > door_line_lower_y:
        return "in", events
    elif start > door_line_lower_y and end < door_line_lower_y:
        return "out", {}
    else:
        return "unknown", {}
