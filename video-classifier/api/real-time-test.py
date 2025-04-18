import cv2
import mediapipe as mp
from ultralytics import YOLO

video_path = '/Users/jensen/Exams/dog_walking_tracker/demo_videos/dog_walk_in.mp4'

yolo_model = YOLO('yolo11n.pt')

frame_data = {
    'x': 120,
    'y': 0,
    'width': 500,
    'height': 750
}

frame_x1 = frame_data['x']
frame_y1 = frame_data['y']
frame_x2 = frame_x1 + frame_data['width']
frame_y2 = frame_y1 + frame_data['height']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands_model = mp_hands.Hands(
    static_image_mode=False, max_num_hands=1, min_detection_confidence=0.75)


def detect_gesture_shown_to_camera(frame):
    """ Determines is the fingers are above the palm. If so, returns the gesture.
    Args:
        frame: The frame from the camera.
    Returns:
        str: The gesture shown by the hand.
    """

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_model.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers_up(hand_landmarks.landmark)
            gesture_text = gesture_from_fingers(fingers_up)
            return gesture_text

    return "No hand"


def count_fingers_up(landmarks):
    finger_tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip_id in finger_tips_ids:
        if landmarks[tip_id].y < landmarks[tip_id - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)


def gesture_from_fingers(fingers_up):
    if fingers_up == 0:
        return "poo"
    elif fingers_up == 2:
        return "pee"
    elif fingers_up == 5:
        return "play"
    else:
        return f"{fingers_up} fingers"


cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break


     # === YOLO ===
    results = yolo_model(frame, verbose=False)[0]

    for result in results.boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        conf = result.conf[0]
        cls_id = int(result.cls[0])
        label = yolo_model.names[cls_id]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 100, 0), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 0), 2)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_model.process(frame_rgb)

    gesture_text = "No hand"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers_up(hand_landmarks.landmark)
            gesture_text = gesture_from_fingers(fingers_up)

    # Display gesture on frame
    cv2.putText(frame, f"Gesture: {gesture_text}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    overlay = frame.copy()
    cv2.rectangle(frame, (frame_x1, frame_y1), (frame_x2, frame_y2), (42, 42, 165), 5)
    cv2.rectangle(frame, (frame_x1, frame_y1), (frame_x2, frame_y2), (42, 42, 165), -1)
    cv2.addWeighted(overlay, .6, frame, 1 - .6, 0, frame)

    cv2.imshow("Hand Gesture Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
