from django.urls import path
from . import views

urlpatterns =[
    path('medium/', views.medium)
]