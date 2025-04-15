from django.urls import path
from . import views

app_name = 'tasks'  # Defina o namespace aqui

urlpatterns = [
    path('', views.task_list, name='task_list'),
]

