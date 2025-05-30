from django.shortcuts import render, redirect
from .models import Device
from django.utils import timezone
import requests
import json

# Create your views here.

def index(request):
    devices = Device.objects.all()
    return render(request, 'devices/index.html', context={'devices': devices})

def register(request):
    if request.method == 'POST':
        # Handle the form submission
        device_name = request.POST.get('device_name')
        device_type = request.POST.get('device_type')
        device_location = request.POST.get('device_location')
        device_ip = request.POST.get('device_ip')
        device_port = request.POST.get('device_port')

        device = Device.objects.create(
            name=device_name,
            type=device_type,
            location=device_location,
            ip=device_ip,
            server_port=device_port,
        )

        # Save the device to the database
        device.save()

        register_url = device.get_registration_url()
        response = requests.post(
            register_url,
            data=json.dumps({
                'device_id': device.id,
                'device_name': device.name,
            }),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
        )
        
        if response.status_code == 201:
            # Handle successful registration
            print("Device registered successfully.")
            device.status = True
            device.last_seen = timezone.now()
            device.save()
        else:
            # Handle registration failure
            print("Device registration failed.")
            Device.objects.get(id=device.id).delete()
            return redirect('devices:index')
        
        # Here you would typically save the device information to the database
        return redirect('devices:details', device_id=device.id)

    return render(request, 'devices/register.html')

def device_details(request, device_id):
    # Logic to fetch device details from the database using device_id
    # For example, you might query the database for a device with the given ID
    device = Device.objects.get(id=device_id)
    device_details = {
        'id': device.id,
        'name': device.name,
        'ip': device.ip,
        'server_port': device.server_port,
        'type': device.type,
        'location': device.location,
        'status': device.status,
        'created_at': device.created_at,
        'updated_at': device.updated_at,
        'stream_url': device.get_stream_url(),
        'websocket_url': device.get_websocket_url(),
        'door_frame': device.get_door_frame()
    }
    return render(request, 'devices/details.html', context={'device': device_details})

def export(request):
    # Logic to export device data
    # This could involve querying the database and formatting the data for export
    # For example, exporting to CSV or JSON format
    pass

def import_data(request):
    # Logic to import device data
    # This could involve reading a file (e.g., CSV or JSON) and saving the data to the database
    pass

def register_frame(request):
    import json
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('device_id')
        print(f"DATA: {data}")

        device = Device.objects.get(id=id)

        device.update_door_frame(
            x=data.get('x'),
            y=data.get('y'),
            width=data.get('width'),
            height=data.get('height'),
        )

        device.save()
        
        print(f"Device ID: {id}")
        return redirect('devices:details', device_id=id)
    return render(request, 'devices/index.html')