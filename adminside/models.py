from django.db import models

class Year(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField(default=0)
    remaining_seats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.year.name})"
