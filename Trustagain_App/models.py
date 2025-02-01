from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# Custom User Model
class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)

# Model to store screen input data
class InputData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=255)  # Name of the screen
    data = models.JSONField()  # Store input data as JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.screen_name}"

