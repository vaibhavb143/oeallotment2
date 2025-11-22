from django.db import models
from django.contrib.auth.models import User
from adminside.models import Year, Subject


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20, unique=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    allotted_subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.year.name})"


class Preference(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField()

    class Meta:
        unique_together = ('student', 'priority')
        ordering = ['priority']

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} (Priority {self.priority})"
