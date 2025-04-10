from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from .serializers import VideoUploadSerializer

from .utils.file_storage import store_video


class VideoUploadView(APIView):
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        video_file = serializer.validated_data['video']
        video_file_path = store_video(video_file)
        # TODO: You can save it or pass it to your AI logic here

        return Response(
            {"message": "Video received.", "url": video_file_path}, status=status.HTTP_200_OK)
