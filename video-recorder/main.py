import cv2
import threading
import time
import requests
from collections import deque
from datetime import datetime

VIDEO_DURATION_AFTER_DETECTION = 5  # seconds
VIDEO_DURATION_BEFORE_DETECTION = 5  # seconds
FPS = 20
FRAME_WIDTH, FRAME_HEIGHT = 640, 480
MAX_CLIP_LENGTH = 60  # seconds

SERVER_URL = "http://localhost:8000/api/v1/video/upload"
DEVICE_ID = 'device_id_123'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')


class VideoRecorder:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        pass

    def monitor(self):
        pass

    def _record_loop(self):
        pass

    def stop_and_save(self):
        pass

    def cleanup(self):
        self.cap.release()
        # GPIO.cleanup()  # Uncomment if using GPIO pins


class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.session.headers.update({'Device-ID': DEVICE_ID})
