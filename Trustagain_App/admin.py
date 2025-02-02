from django.contrib import admin
from .models import User, InputData

# Register your models here.
admin.site.register(User) # now if we go to our model we will see user in it
admin.site.register(InputData)
