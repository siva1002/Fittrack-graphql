from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm
from django.http import HttpResponse
import requests
# Create your views here.
def baseview(request):
    form=LoginForm()
    if request.method == 'POST':
        username,password=request.POST.get('username'),request.POST.get('password')
        user=authenticate(request=request,username=username,password=password)
        print(user)
        if user:
            login(request,user)
    if request.user.is_authenticated:
        return HttpResponse("<h1 style='text-align:center'>Logged in successfully</h1>")
    return render(request, 'login.html', {'form':form })

def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("base")

def homeview(request):
    return render(request, 'home.html')
