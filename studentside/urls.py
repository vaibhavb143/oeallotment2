from django.urls import path
from . import views

urlpatterns = [
    path('student-register/', views.student_register, name='student_register'),
    path('student-login/', views.student_login, name='student_login'),
    path('', views.student_dashboard, name='student_dashboard'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('select-preferences/', views.select_preferences, name='select_preferences'),
]

