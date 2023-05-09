from django.contrib import admin
from .models import Assessment, Grade, Module, Score


# Register your models here.

admin.site.register(Assessment)
admin.site.register(Grade)
admin.site.register(Module)
admin.site.register(Score)
