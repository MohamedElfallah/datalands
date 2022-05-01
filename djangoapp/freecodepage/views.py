from django.shortcuts import render
from .models import Freecodecamp

# Create your views here.
def freecodecamp(request):
    articles = Freecodecamp.objects.all()
    data ={
        'articles':articles
    }
    return render(request, 'freecodepage/freecodecamp.html', data)
