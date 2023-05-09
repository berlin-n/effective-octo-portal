from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Module, Assessment, Score

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = ['module_code', 'module_name', 'description', 'lecturer']

class NewUser_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','password1', 'password2']

class AssessmentForm(ModelForm):
    class Meta:
        model = Assessment
        fields = '__all__'
        exclude = ['module']

class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = '__all__'
        exclude = ['module']