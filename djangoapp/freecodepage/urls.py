from django.urls import path
from . import views

urlpatterns = [
    path('freecodecamp/', views.freecodecamp)
]