from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.utils.timezone import now



# Custom User Model
class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)

    class Meta:
        swappable = "AUTH_USER_MODEL"  # Allows Django to swap the model correctly


# Model to store screen input data
class InputData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=255)  # Name of the screen
    data = models.JSONField()  # Store input data as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.screen_name}"


# Shift Narrative Model
class ShiftNarrative(models.Model):
    staff_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    Time_in = models.TimeField()
    Time_out = models.TimeField()
    date_in = models.DateField(default=now)
    date_out = models.DateField(default=now)
    # severity = models.CharField(max_length=50, choices=[
    #     ('Low', 'Low'),
    #     ('Medium', 'Medium'),
    #     ('High Risk', 'High Risk'),
    #     ('Critical', 'Critical')
    # ])
    report_notes = models.TextField()

    def __str__(self):
        return f"{self.staff_name} - {self.client_name} ({self.date_in})"


# TimeSheet Model
class TimeSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_in = models.DateField()
    time_in = models.TimeField()
    date_clock_out = models.DateField(null=True, blank=True)
    time_clock_out = models.TimeField(null=True, blank=True)
    report_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date_in}"
    

User = get_user_model()

class IncidentReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to a user
    report_title = models.CharField(max_length=255)
    staff_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    severity = models.CharField(max_length=50, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High Risk', 'High Risk'),
        ('Critical', 'Critical')
    ])
    report_notes = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_title} - {self.client_name} ({self.date})"
