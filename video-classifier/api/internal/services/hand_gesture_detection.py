import mediapipe as mp
import cv2
import numpy as np

mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(
    static_image_mode=True, max_num_hands=1, min_detection_confidence=0.7)
hand_connections = mp_hands.HAND_CONNECTIONS


def count_fingers_up(landmarks):
    finger_tips_ids = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
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


def detect_hand_gesture(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_model.process(frame_rgb)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark
        fingers_up = count_fingers_up(landmarks)

        # Map gesture to event
        if fingers_up == 1:
            return "pee"
        elif fingers_up == 2:
            return "poo"
        elif fingers_up == 3:
            return "both"
        elif fingers_up == 5:
            return "play"

    return None
