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

