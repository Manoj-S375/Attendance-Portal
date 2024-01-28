from django.shortcuts import render
from requests import request
from .forms import userRegister

# Create your views here.

def register(request):
    if request.method == "POST":
        form = userRegister(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = userRegister()

    return render(request,"user/register.html",{'form':form})
