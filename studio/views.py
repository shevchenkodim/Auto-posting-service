from django.shortcuts import render

# Create your views here.
def studio(request):
    return render(request, "studio/studio.html")

def tasks(request):
    return render(request, "studio/tasks.html")

def statistics(request):
    return render(request, "studio/statistics.html")

def settings(request):
    return render(request, "studio/settings.html")
