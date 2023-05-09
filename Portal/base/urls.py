from django.urls import path
from students import views as students_views
from lecturers import views as lecturers_views
from .import views

urlpatterns = [
    path('',views.index, name='home'),
    path('lecturer_page/<str:pk>/',lecturers_views.index, name='lecturer_index'),
    path('student_page/<str:pk>/',students_views.index, name='student_index'),

    path('login_page/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register_user/', views.registration_bridge, name='register'),
    path('register_student/<str:pk>/',students_views.register_student, name='register_student'),
    path('register_lecturer/<str:pk>/',lecturers_views.register_lecturer, name='register_lecturer'),

    path('create_module/', lecturers_views.create_module, name='create_module'),
    path('module/<str:pk>/', lecturers_views.module, name='module'),
    path('assessment_form/<str:pk>/', lecturers_views.create_assessment, name='add_assessment'),
    path('score_form/<str:pk>/', lecturers_views.create_score, name='score_assessment'),

    path('join-module/', students_views.join_module, name='join_module'),
    path('add-module/<str:pk>/', students_views.add_module, name='add_module'),
    path('students_module/<str:pk>/', students_views.module, name='students_module')
]