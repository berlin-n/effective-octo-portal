from django.shortcuts import render, redirect
from django.http import HttpResponse
from base.forms import NewUser_Form
from django.contrib.auth import authenticate, login
from .models import Lecturer_Profile
from django.contrib import messages
from base.forms import ModuleForm, AssessmentForm, ScoreForm
from base.models import Module
from django.db.models import Q

# Create your views here.

def index(request, pk):
    lecturers = Lecturer_Profile.objects.all()
    lecturer = Lecturer_Profile.objects.get(id=pk)
    lecturerModules = lecturer.module_set.all()
    context = {'lecturers': lecturers,'lecturer': lecturer,
                'lecturerModules': lecturerModules,}
    return render(request, 'lecturers/index.html', context)

def register_lecturer(request, pk):
    form = NewUser_Form()

    if request.method == 'POST':
        form = NewUser_Form(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            login(request, user)
            lecturer = Lecturer_Profile.objects.create(
                first_name = request.user.first_name ,
                last_name = request.user.last_name ,
                User = request.user ,
                user_type = 'Lecturer'
            )
            return redirect('lecturer_index', pk=lecturer.id) 
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login.html', {'form': form})

def create_module(request):
    form = ModuleForm()
    lecturers = Lecturer_Profile.objects.all()

    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            for i in lecturers:
                if request.user.username == i.User.username:
                    return redirect('lecturer_index', pk=i.id)
    lecturer = Lecturer_Profile.objects.get(User = request.user)
    context = {'form': form, 'lecturer': lecturer}
    return render(request, 'lecturers/module_form.html', context)
        
def module(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    module = Module.objects.get(id=pk)
    allStudents = module.students.all()
    score = module.score_set.filter(
        Q(module__students__last_name__icontains=q)
    )
    lecturer = Lecturer_Profile.objects.get(User = request.user)
    context = {'module': module, 'allStudents': allStudents, 'score': score, 'lecturer': lecturer}
    return render(request, 'lecturers/module.html', context)

def create_assessment(request, pk):
    module = Module.objects.get(id=pk)
    form = AssessmentForm

    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.module = module
            assessment.save()
            return redirect('module',pk=module.id )
    lecturer = Lecturer_Profile.objects.get(User = request.user)
    context = {'form': form, 'lecturer': lecturer}
    return render(request, 'lecturers/assessment_form.html', context)

def create_score(request, pk):
    module = Module.objects.get(id=pk)
    form = ScoreForm
    assessment = module.assessment_set.all()

    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.save(commit=False)
            score.module = module
            for i in assessment:
                score.assessment = i
            score.save()
            return redirect('module', pk=module.id)
    lecturer = Lecturer_Profile.objects.get(User = request.user)
    context = {'form': form, 'lecturer': lecturer}
    return render(request, 'lecturers/score_form.html', context)