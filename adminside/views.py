from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from studentside.models import Student
from .models import Year, Subject
from django.contrib.auth import authenticate, login, logout

def is_admin(user):
    return user.is_superuser

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin_login.html')

@user_passes_test(is_admin)
def admin_dashboard(request):
    years = Year.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'admin_dashboard.html', {'years': years, 'subjects': subjects})


@user_passes_test(is_admin)
def add_subject(request):
    years = Year.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        year_id = request.POST.get('year')
        total_seats = int(request.POST.get('total_seats') or 0)
        year = Year.objects.get(id=year_id)
        Subject.objects.create(
            name=name,
            year=year,
            total_seats=total_seats,
            remaining_seats=total_seats
        )
        messages.success(request, f"Subject '{name}' added for {year.name} with {total_seats} seats.")
        return redirect('admin_dashboard')
    return render(request, 'add_subject.html', {'years': years})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')



from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import csv

@staff_member_required
def admin_allotment_summary(request):
    students = Student.objects.select_related('user', 'year', 'allotted_subject').order_by('year', 'roll_no')

    # CSV Export Option
    if 'export' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="allotment_summary.csv"'
        writer = csv.writer(response)
        writer.writerow(['Roll No', 'Student Name', 'Year', 'Allotted Subject'])
        for s in students:
            writer.writerow([
                s.roll_no,
                s.user.get_full_name(),
                s.year.name,
                s.allotted_subject.name if s.allotted_subject else 'Not Allotted'
            ])
        return response

    return render(request, 'admin_allotment_summary.html', {'students': students})
