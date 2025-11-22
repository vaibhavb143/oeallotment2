from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Preference, Year, Student
from adminside.models import Subject

# --- Student Registration ---
def student_register(request):
    years = Year.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        name = request.POST["name"]
        roll_no = request.POST["roll_no"]
        year_id = request.POST["year"]

        if User.objects.filter(username=username).exists():
            return render(request, "student_register.html", {
                "years": years,
                "error": "Username already exists!"
            })

        year = Year.objects.get(id=year_id)
        user = User.objects.create_user(username=username, password=password, first_name=name)
        Student.objects.create(user=user, roll_no=roll_no, year=year)
        return redirect("student_login")

    return render(request, "student_register.html", {"years": years})


# --- Student Login ---
def student_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_superuser:
            login(request, user)
            return redirect("student_dashboard")
        else:
            return render(request, "student_login.html", {"error": "Invalid credentials"})
    return render(request, "student_login.html")


# --- Student Dashboard ---
@login_required(login_url='student_login')
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    return render(request, "student_dashboard.html", {"student": student})


# --- Student Logout ---
def student_logout(request):
    logout(request)
    return redirect("student_login")



from django.shortcuts import render
from .models import Year, Subject, Student, Preference
from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required
def select_preferences(request):
    student = Student.objects.get(user=request.user)

    # If already allotted, stop them
    if student.allotted_subject:
        return render(request, "preference_message.html", {
            "message": f"You have already been allotted: {student.allotted_subject.name}"
        })

    # Get all subjects of the student's year
    subjects = Subject.objects.filter(year=student.year)

    existing_prefs = Preference.objects.filter(student=student).order_by('priority')

    if request.method == "POST":
        # ---- Collect subject IDs and priorities from dropdown selections ----
        subject_data = request.POST.getlist('subject_order')

        # Format: "subjectID-priority"
        Preference.objects.filter(student=student).delete()
        preference_map = {}

        for item in subject_data:
            if "-" in item:
                subj_id, priority = item.split('-')
                subj_id, priority = int(subj_id), int(priority)
                preference_map[priority] = subj_id

        # ---- Save preferences in order ----
        for priority in sorted(preference_map.keys()):
            subject = Subject.objects.get(id=preference_map[priority])
            Preference.objects.create(student=student, subject=subject, priority=priority)

        # ---- FCFS ALLOTMENT LOGIC ----
        with transaction.atomic():
            preferences = Preference.objects.filter(student=student).order_by('priority')
            allotted = None
            for pref in preferences:
                subj = pref.subject
                if subj.remaining_seats > 0:
                    subj.remaining_seats -= 1
                    subj.save()
                    student.allotted_subject = subj
                    student.save()
                    allotted = subj
                    break

        # ---- Allotment result message ----
        if allotted:
            msg = f"🎉 Congratulations! You have been allotted '{allotted.name}'."
        else:
            msg = "❌ Sorry, all preferred subjects are full. You could not be allotted any subject."

        return render(request, "preference_message.html", {"message": msg})

    # ---- GET request (show preference form) ----
    return render(request, "select_preferences.html", {
        "subjects": subjects,
        "existing_prefs": existing_prefs
    })



