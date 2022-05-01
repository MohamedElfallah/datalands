from django.shortcuts import render
from .models import Medium

# Create your views here.
def medium(request):
    articles=Medium.objects.all().order_by('-id')
    data={
        'articles':articles
        }
    return render(request, 'mediumpage/medium.html', data)