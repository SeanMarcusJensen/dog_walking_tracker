from django.db import models
from django.core.files.storage import default_storage
from django.utils import timezone
import uuid
from devices.models import Device
# Create your models here.


class Video(models.Model):
    """
    Model representing a video.
    """
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(
        Device, related_name='videos', on_delete=models.CASCADE)
    file = models.FileField(
        upload_to='uploads/', storage=default_storage)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    video_size = models.BigIntegerField()
    extension = models.CharField(max_length=10, default='mp4')
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_from_file(device_id, video_file):
        """
        Create a Video instance from a file.
        """
        if not video_file:
            raise ValueError("File is required.")
        
        if not device_id:
            raise ValueError("Device ID is required.")
            
        device = Device.objects.get(id=device_id)
        if not device:
            raise ValueError("Device not found.")

        extension = video_file.name.split('.')[-1]
        video_file.name = uuid.uuid4().hex + '.' + extension

        video = Video.objects.create(
            device=device,
            file=video_file,
            video_size=video_file.size,
            extension=extension,
            status='pending',
        )

        video.save()
        return video

    def __str__(self):
        return f'{self.file.name} ({self.id})'
