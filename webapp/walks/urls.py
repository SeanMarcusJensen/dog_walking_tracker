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
from .views import get_walks, get_walk, stop_walk, delete_walk, add_event, delete_event

app_name = 'walks'

urlpatterns = [
    path('', get_walks, name='index'),
    path('<int:id>/', get_walk, name='details'),
    path('<int:id>/delete', delete_walk, name='delete'),
    path('<int:id>/stop', stop_walk, name='stop'),
    path('<int:id>/events/', add_event, name='add_event'),
    path('<int:id>/events/<int:eid>/delete',
         delete_event, name='delete_event'),
]
