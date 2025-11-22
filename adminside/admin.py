from django.contrib import admin
from .models import Year, Subject

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'total_seats', 'remaining_seats')
    list_filter = ('year',)