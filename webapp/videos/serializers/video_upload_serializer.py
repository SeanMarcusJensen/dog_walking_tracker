# serializers.py
from rest_framework import serializers


class VideoUploadSerializer(serializers.Serializer):
    video = serializers.FileField()

    def validate_video(self, value):
        if not hasattr(value, 'content_type'):
            raise serializers.ValidationError("Invalid file upload.")
        if not value.content_type.startswith('video/'):
            raise serializers.ValidationError("Uploaded file must be a video.")
        return value
