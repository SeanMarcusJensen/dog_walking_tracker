import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands_model = mp_hands.Hands(
    static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)


def count_fingers_up(landmarks):
    finger_tips_ids = [8, 12, 16, 20]
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


cap = cv2.VideoCapture(0)  # Use webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

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

    cv2.imshow("Hand Gesture Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
