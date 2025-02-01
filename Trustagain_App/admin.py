from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User) # now if we go to our model we will see user in it
