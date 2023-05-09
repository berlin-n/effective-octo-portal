from django.shortcuts import render, redirect
from django.http import HttpResponse
from base.forms import NewUser_Form
from django.contrib.auth import authenticate, login
from .models import Student_Profile
from django.contrib import messages
from base.models import Module, Assessment
from django.db.models import Q
from django.contrib.auth.models import User

# Create your views here.

def index(request, pk):
    student = Student_Profile.objects.get(id=pk)

    modules = student.module_set.all()
    context = {'student': student,'modules': modules}
    return render(request, 'students/index.html', context)

def register_student(request, pk):
    form = NewUser_Form()

    if request.method == 'POST':
        form = NewUser_Form(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            login(request, user)
            student = Student_Profile.objects.create(
                first_name = request.user.first_name ,
                last_name = request.user.last_name ,
                User = request.user ,
                user_type = 'Student'
            )
            return redirect('student_index', pk=student.id)
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login.html', {'form': form})

def join_module(request):
    modules = Module.objects.all()
    student = Student_Profile.objects.get(User = request.user)
    context = {'modules': modules, 'student': student}
    return render(request, 'students/join_module.html', context)

def add_module(request, pk):
    student = Student_Profile.objects.get(User = request.user)
    module = Module.objects.get(id=pk)
    if request.method == 'POST':
        module.students.add(student)
        return redirect('student_index', pk=student.id)

    context = {'student': student}
    return render(request, 'students/add_module_form.html', context)

def module(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    student = Student_Profile.objects.get(User = request.user)
    module = Module.objects.get(id=pk)

    score = module.score_set.filter(
        Q(module__students__last_name__icontains=q)
    )
    module_assessments = module.assessment_set.all()
    context = {'student': student, 'module': module, 'module_assessments': module_assessments, 'score': score}
    return render(request, 'students/module.html', context)