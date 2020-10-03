from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request,'chapters/home.html')

def view_chapter(request):
    receive_req = request.GET.get("chapter")
    if receive_req.lower() == "trignometry":
        return render(request,'chapters/trigs.html')
    else:
        return HttpResponse("Topic Not Found")
