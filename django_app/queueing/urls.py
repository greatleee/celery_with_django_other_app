from django.urls import path

from . import views

urlpatterns = [
    path('<str:task_id>/<int:seconds>/', views.push),
]