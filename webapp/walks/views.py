from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import Walk, WalkEvent


def get_walks(request):
    walks = Walk.objects.all()

    return JsonResponse(
        {"walks": [{"id": walk.id, "start_time": walk.start_time,
                    "end_time": walk.end_time} for walk in walks]}
    )
