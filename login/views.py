from django.shortcuts import render,redirect
from .models import Employee
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

def home(request):
    return render(request,"login/home.html")


def signin(request):
    return render(request,"login/signin.html")

def check_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            employee = Employee.objects.get(username=username)
            if employee.password == password: 
                return render(request, 'login/signin.html', {'user_authenticated': True, 'username': username})
            else:
                messages.error(request, "Incorrect password.")
                return redirect('login:signin')
        except Employee.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('login:signin')

    return render(request, 'login/signin.html', {'user_authenticated': False})

def logout(request):
    return redirect()

def signup(request):
    return render(request,"login/signup.html")


def  store_details(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if Employee.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect('login:signup')

        if Employee.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Try logging in.")
            return redirect('login:signup')
        employee = Employee(username=username, email=email, password=password)
        employee.save()
        return HttpResponseRedirect(reverse("login:home"))