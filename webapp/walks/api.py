from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from .serializers import VideoUploadSerializer

from .utils.file_storage import store_video, get_video_location
from .models import Walk, WalkEvent, Video


class VideoUploadView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id: str, *args, **kwargs):
        if not id:
            return Response({"message": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        video = get_video_location(id)
        if not video:
            return Response({"message": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(video, content_type="video/mp4")

    def post(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # TODO: You can save it or pass it to your AI logic here
        video_file = serializer.validated_data['video']
        video_file_path = store_video(video_file)

        video = Video.objects.create(
            video_file=video_file_path
        )
        video.save()

        return Response(
            {"message": "Video received.", "url": video.video_file}, status=status.HTTP_200_OK)

    def update(self, request, id: str, *args, **kwargs):
        """
        Update the walk details.
        """
        try:
            walk = Walk.objects.get(id=id)
        except Walk.DoesNotExist:
            return Response({"message": "Walk not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoUploadSerializer(
            walk, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
