from django.shortcuts import render
from .models import Device

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
        
        # Here you would typically save the device information to the database
        print(device.__dict__)  # For debugging purposes
        return render(request, 'devices/details.html', context=device.__dict__)

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
        'stop_url': device.get_stream_url() + '/stop',
        'start_url': device.get_stream_url() + '/start',
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