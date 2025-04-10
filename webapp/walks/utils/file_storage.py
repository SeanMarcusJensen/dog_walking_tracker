import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage


def store_video(video):
    # Ensure the directory exists
    video_dir = os.path.join(settings.MEDIA_ROOT, "videos")
    os.makedirs(video_dir, exist_ok=True)

    # Generate a unique filename
    unique_id = str(uuid.uuid4())
    filename = default_storage.get_available_name(
        unique_id + os.path.splitext(video.name)[1])
    relative_path = default_storage.save(
        os.path.join('videos', filename), video)

    print(f"Store Video Out: {relative_path}")
    return relative_path
