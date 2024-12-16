from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth

# Create your views here.
def register(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            User.objects.create_user(
                first_name = request.POST['first_name'].title(),
                last_name = request.POST['last_name'].title(),
                email = request.POST['email'].lower(),
                username = request.POST['email'].lower(),
                password = request.POST['password1']
            ).save()
            return render(request, 'user/login.html', {'passError': False, 'created': True})
        else:
            return render(request, 'user/register.html', {'passError' : True})
    return render(request, 'user/register.html', {'passError': False})

def login(request):
    if request.method == 'POST':
        username = request.POST['email'].lower()
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
        else:
            return render(request, 'user/login.html', {'error': True,  'created': False})
        return redirect('/')
    return render(request, 'user/login.html', {'error': False,  'create': False})

def logout(request):
    auth.logout(request)
    return render(request, 'user/login.html')