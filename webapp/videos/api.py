from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from .serializers import VideoUploadSerializer
from django.conf import settings
import requests

from .models import Video


def notify(video_id, video_url, callback):
    data = {
        "video_id": str(video_id),
        "video_url": video_url,
        "callback_url": callback
    }
    print(f"Nofitying Data: {data}")

    response = requests.post(settings.NOTIFY_URL, json=data)
    if response.raise_for_status():
        raise Exception("Failed to notify callback URL")
    return response.json()


class VideoUploadView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        video_file = serializer.validated_data['video']
        video = Video.create_from_file(video_file)

        try:
            task = notify(
                video.id,
                video_url=f"{settings.VIDEO_BASE_URL}{request.path}{video.id}",
                callback=f"{settings.CALLBACK_BASE_URL}{request.path}{video.id}")
        except requests.RequestException as e:
            print("Error notifying callback URL:", e)
            return Response({"message": "Failed to notify callback URL."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"message": "Video received.", "url": video.id, "task": task}, status=status.HTTP_201_CREATED)

    def get(self, request, id: str, *args, **kwargs):
        if not id:
            return Response({"message": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        video = Video.objects.get(id=id)
        if not video:
            return Response({"message": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        extension = video.extension.lower()
        mime_type = f"video/{extension}" if extension != 'mov' else 'video/quicktime'
        return FileResponse(video.file.open('rb'), content_type=mime_type)

    def patch(self, request, id: str, *args, **kwargs):
        return Response({"message": "PATCH method not allowed yet."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, id: str, *args, **kwargs):
        return Response({"message": "PUT method not allowed yet."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, id: str, *args, **kwargs):
        if not id:
            return Response({"message": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        video = Video.objects.filter(id=id).first()
        if not video:
            return Response({"message": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        video.delete()
        return Response({"message": "Video deleted."}, status=status.HTTP_204_NO_CONTENT)
