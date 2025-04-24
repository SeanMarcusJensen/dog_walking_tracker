from django.shortcuts import render
from django.utils import timezone

from walks.models import Walk, WalkEvent
# Create your views here.


def index(request):
    walks = Walk.objects.all()
    last_walk = walks.order_by('-start_time').first()

    if not last_walk:
        return render(request, 'dashboard/index.html', context={})

    if last_walk:
        last_walk_events = WalkEvent.objects.filter(walk=last_walk)
    else:
        last_walk_events = []

    time_since = timezone.now() - last_walk.end_time if last_walk else 0

    context = {
        'last_walk': {
            'start_time': last_walk.start_time,
            'time_since': time_since,
            'duration': last_walk.get_duration() if last_walk else 0,
        },
    }

    return render(request, 'dashboard/index.html', context=context)
