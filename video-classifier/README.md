# Automatic Dog Walking Tracker

## Components

This project relies on a couple of different components:

1. AI component to detect and classify video.
2. Django App to handle entries and authentication.
3. Raspberry Pi for capturing the video clip.

Read more about them in the respected component folder.

## FLOW Diagram

[Pi] --> [webapp: POST /videos/] --> stores video
               |
               +--> [POST /notify] --> [video-classifier]
                                           |
                                           v
                                 [queue classification]
                                           |
                                           v
                              [GET video file from webapp]
                                           |
                                           v
                             [POST result to webapp / PATCH]

## Notes

Could have used one api. But I wanted to have the inverse, because inference on the video is blocking for the video length. Thus Queue system.

FineTuning of YOLO -> Had to use two models.

Using two yolo models was hard to do. It took a long time to train for it to become any good - it must be other models that can do this better and faster.

That is where MediaPipe Hands comes into the picture. It is efficient at key-pointing hands - we can thus use this to determine hand shape and fingers shown. The only problem now is that it detects hands, even when we're not explicitly showing the hand to the camera for signaling.we need functionality to fix this. (https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)

