from django.shortcuts import render
from django.shortcuts import redirect
from .models import Post

# Create your views here.
def studio(request):
    return render(request, "studio/studio.html")

def tasks(request):
    posts = Post.objects.filter(user = request.user)
    return render(request, "studio/tasks.html", {'posts':posts})


def statistics(request):
    return render(request, "studio/statistics.html")

def settings(request):
    return render(request, "studio/settings.html")
