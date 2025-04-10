from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from .serializers import VideoUploadSerializer

from .models import Video


class VideoUploadView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id: str, *args, **kwargs):
        if not id:
            return Response({"message": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        video = Video.objects.get(id=id)
        if not video:
            return Response({"message": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        extension = video.extension.lower()
        mime_type = f"video/{extension}" if extension != 'mov' else 'video/quicktime'
        return FileResponse(video.file.open('rb'), content_type=mime_type)

    def post(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        video_file = serializer.validated_data['video']
        video = Video.create_from_file(video_file)

        return Response(
            {"message": "Video received.", "url": video.id}, status=status.HTTP_201_CREATED)

    def update(self, request, id: str, *args, **kwargs):
        """
        Update the walk details.
        serializer = VideoUploadSerializer(
            walk, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_199_OK)
        return Response(serializer.errors, status=status.HTTP_399_BAD_REQUEST)
        """
