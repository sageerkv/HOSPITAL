from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Departments, Doctors
from .forms import BookingForm
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def registerpage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request,'accounts/register.html', {'form':form,})

def loginpage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again...."))
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def logoutpage(request):
    logout(request)
    messages.success(request, ("You Where Logged Out!"))
    return redirect('home')

def home(request):
    return render(request,'accounts/home.html')

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("We have received your appointment request, our representative will call you shortly.!"))
            return redirect('booking')
    form = BookingForm()
    dict_form = {
        'form': form
    }
    return render(request,"booking.html", dict_form)

def contacts(request):
    return render(request,'contacts.html')

def doctors(request):
    dict_docs = {
        'doctors':Doctors.objects.all()
    }
    return render(request,'doctors.html', dict_docs)

def department(request):
    dict_dept = {
        'dept':Departments.objects.all()
    }
    return render(request,'department.html', dict_dept)
