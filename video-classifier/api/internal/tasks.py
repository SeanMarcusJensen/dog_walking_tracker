import requests
import logging


def classify_video_task(video_id: int, video_url: str, callback_url: str):
    # Download video from webapp
    video_data = requests.get(video_url).content

    # Run your YOLOv11 model here
    label = run_yolov11(video_data)  # Assume this is implemented

    # Send back result to webapp
    requests.patch(callback_url, json={"label": label})


def run_yolov11(video_data):
    # Mock example
    logging.info("Running YOLOv11 model on video data")
    return "dog entering door"
