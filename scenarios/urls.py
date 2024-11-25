from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_from_request),
]