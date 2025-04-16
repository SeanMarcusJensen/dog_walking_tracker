import requests
import logging
import os
from .services.detect_dog_direction import detect_dog_direction
from .services.hand_gesture_detection import detect_hand_gesture
import time


def classify_video_task(video_id: str, video_url: str, callback_url: str):
    try:
        file_path = f"/tmp/video_{video_id}.mp4"
        print(f"Downloading video from {video_url} to {file_path}")

        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        inference_duration, direction, events = infere_video(file_path)

        """ We can calculate the weight of the events here.
        If the event has occurred more than 3 times, we can consider it as a significant event.
        If the event has occurred less than 3 times, we can consider it as a minor event or noise.
        """
        significant_events = []
        for event, count in events.items():
            print(f"Event: {event}, Count: {count}")
            significant_events.append(event)
            # if count > 3:
            # do not want duplicate events.

        print(
            f"Sending significant events: {significant_events} to {callback_url}")

        requests.patch(callback_url, json={
            "success": True,
            "video_id": video_id,
            "message": 'Video classification completed',
            "duration": inference_duration,
            "prediction": direction,
            "events": significant_events})

    except Exception as e:
        logging.error(f"Error in classify_video_task: {e}")
        requests.patch(callback_url, json={
            "success": False,
            "video_id": video_id,
            "message": str(e),
            "prediction": "unknown",
            "events": []})


def infere_video(tmp_file):
    # Mock example
    # Then load the file for your model
    logging.info("Running YOLOv11 model on video data")
    events = []

    start_time = time.time()

    # handle the video data with your model
    status, events = detect_dog_direction(tmp_file, debug=False)

    end_time = time.time()
    infer_time = end_time - start_time
    logging.info(f"YOLOv11 inference time: {infer_time:.2f} seconds")

    # delete temp
    os.remove(tmp_file)

    return infer_time, status, events
