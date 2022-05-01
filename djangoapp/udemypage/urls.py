from django.urls import path 
from . import views

urlpatterns = [
    path('udemy/', views.udemy)
]