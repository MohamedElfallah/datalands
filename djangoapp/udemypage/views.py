from django.shortcuts import render
from .models import Udemy

# Create your views here.
def udemy(request):
    articles = Udemy.objects.all().order_by('-id')
    data = {'articles': articles}
    return render(request, 'udemypage/udemy.html', data )