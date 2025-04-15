from django.shortcuts import render, redirect

# Create your views here.
from django.http import JsonResponse
from .models import Walk, WalkEvent
from django.utils.timezone import now


def get_walks(request):
    walks = Walk.objects.all()

    context = {
        "walks": [{
            "id": walk.id,
            "start_time": walk.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": walk.end_time.strftime("%Y-%m-%d %H:%M:%S") if walk.end_time else None,
            "status": walk.status,
            "duration": walk.get_duration().total_seconds() if walk.end_time else None,
            "events": [{
                "id": event.id,
                "event_type": event.event_type,
            } for event in walk.events.all()]
        }for walk in walks],
    }

    return render(request, "walks/index.html", context)


def get_walk(request, id):
    walk = Walk.objects.get(id=id)
    if not walk:
        return JsonResponse({"message": "Walk not found."}, status=404)
    events = walk.events.all()

    context = {
        "id": walk.id,
        "start_time": walk.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": walk.end_time.strftime("%Y-%m-%d %H:%M:%S") if walk.end_time else None,
        "status": walk.status,
        "duration": walk.get_duration().total_seconds() if walk.end_time else None,
        "events": [{
            "id": event.id,
            "event_type": event.event_type,
        } for event in events]
    }
    return render(request, "walks/details.html", context)


def stop_walk(request, id):
    walk = Walk.objects.get(id=id)
    if not walk:
        return JsonResponse({"message": "Walk not found."}, status=404)
    if walk.status == "completed":
        return redirect("walks:index")
    if walk.status == "cancelled":
        return redirect("walks:index")
    walk.status = "completed"
    walk.end_time = now()
    walk.save()
    return redirect("walks:index")


def delete_walk(request, id):
    walk = Walk.objects.get(id=id)
    if not walk:
        return JsonResponse({"message": "Walk not found."}, status=404)
    walk.delete()
    return redirect("walks:index")


def add_event(request, id):
    walk = Walk.objects.get(id=id)
    if not walk:
        return JsonResponse({"message": "Walk not found."}, status=404)
    event_type = request.POST.get("event_type")
    event = WalkEvent.objects.create(walk=walk, event_type=event_type)
    return redirect("walks:details", id=walk.id)


def delete_event(request, id, eid):
    walk = Walk.objects.get(id=id)
    if not walk:
        return JsonResponse({"message": "Walk not found."}, status=404)
    event = walk.events.get(id=eid)
    if not event:
        return JsonResponse({"message": "Event not found."}, status=404)

    walk_id = walk.id
    event.delete()
    return redirect("walks:details", id=walk_id)
