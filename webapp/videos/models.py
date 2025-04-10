from django.db import models
from django.core.files.storage import default_storage
from django.utils import timezone
import uuid
# Create your models here.


class Video(models.Model):
    """
    Model representing a video.
    """
    id = models.AutoField(primary_key=True)
    file = models.FileField(
        upload_to='uploads/', storage=default_storage)
    # video_file = models.FilePathField()
    video_size = models.BigIntegerField()
    extension = models.CharField(max_length=10, default='mp4')
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_from_file(video_file):
        """
        Create a Video instance from a file.
        """
        if not video_file:
            raise ValueError("File is required.")

        extension = video_file.name.split('.')[-1]
        video_file.name = uuid.uuid4().hex + '.' + extension

        video = Video.objects.create(
            file=video_file,
            video_size=video_file.size,
            extension=extension,
        )

        video.save()
        return video

    def __str__(self):
        return f'{self.file.name} ({self.id})'
