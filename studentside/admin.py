from django.http import HttpResponse
import csv
from django.contrib import admin
from studentside.models import *
# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_no', 'year', 'allotted_subject_display']
    list_filter = ['year']
    actions = ['export_allotment_csv']

    # Column to show allotted subject name
    def allotted_subject_display(self, obj):
        return obj.allotted_subject.name if obj.allotted_subject else "Not allotted"
    allotted_subject_display.short_description = "Allotted Subject"

    # ----------------------------
    # Action: Export Allotment CSV
    # ----------------------------
    def export_allotment_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="elective_allotment.csv"'
        writer = csv.writer(response)
        writer.writerow(['Roll No', 'Student Name', 'Year', 'Allotted Subject'])

        for student in queryset:
            writer.writerow([
                student.roll_no,
                student.user.get_full_name(),
                student.year.name,
                student.allotted_subject.name if student.allotted_subject else 'Not Allotted'
            ])

        return response

    export_allotment_csv.short_description = "Export selected students as CSV"


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'priority']
    list_filter = ['subject']