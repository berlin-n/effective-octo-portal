from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from students.models import Student_Profile
from lecturers.models import Lecturer_Profile
from django.db.models import Q

# Create your views here.

def login_user(request):
    students = Student_Profile.objects.all()
    lecturers = Lecturer_Profile.objects.all()
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Sorry, User not found")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            for i in lecturers:
                if request.user.username == i.User.username:
                    return redirect('lecturer_index', pk= i.id)
            for i in students:
                if request.user.username == i.User.username:
                    return redirect('student_index', pk=i.id)
        else:
            messages.error(request,'Incorrect Password')
    context = {'page': page}
    return render(request, 'base/login.html', context)

def registration_bridge(request):
    return render(request, 'base/registration_bridge.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def index(request):
    context = {}
    return render(request, 'base/index.html', context)


