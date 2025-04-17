"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'devices'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('export/', views.export, name='export'),
    path('import/', views.import_data, name='import'),
    path('details/<int:device_id>/', views.device_details, name='details'),
    path('register_frame/', views.register_frame, name='register_frame'),
]
