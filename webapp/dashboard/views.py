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

    last_poo = last_walk_events.filter(
        event_type='poo').order_by('-id').first()
    last_poo_time = last_poo.walk.start_time if last_poo else None
    time_since_last_poo = timezone.now() - last_poo_time if last_poo else 0

    time_since = timezone.now() - last_walk.end_time if last_walk else 0

    context = {
        'last_walk': {
            'start_time': last_walk.start_time,
            'time_since': time_since.total_seconds() / 60,  # minutes
            'duration': last_walk.get_duration().total_seconds() / 60 if last_walk else 0,
        },
        'events': {
            'last_poo': last_poo_time,
            'time_since_last_poo': time_since_last_poo.total_seconds() / 60,  # minutes
        }
    }

    return render(request, 'dashboard/index.html', context=context)
