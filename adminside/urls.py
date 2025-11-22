from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin/allotment-summary/', views.admin_allotment_summary, name='admin_allotment_summary'),
]
