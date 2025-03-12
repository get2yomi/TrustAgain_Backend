from django.contrib import admin
from .models import User, InputData
from .models import ShiftNarrative
from .models import TimeSheet
from .models import IncidentReport
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _  # Import gettext_lazy for translation






# # Register your models here.
# admin.site.register(User) # now if we go to our model we will see user in it
# class UserAdmin(User):
#     list_display = ("username", "email", "phone", "is_staff", "is_active")
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#     )
#     readonly_fields = ("password",)  # This prevents editing the hashed password

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if "password" in form.base_fields:
#             form.base_fields["password"].widget.attrs["type"] = "password"
#         return form

@admin.register(ShiftNarrative)
class ShiftNarrativeAdmin(admin.ModelAdmin):
    list_display = ('user', 'client_name', 'date_in', 'Time_in', 'Time_out', 'date_out', 'report_notes', 'bm_times', 'bm_size', 'symptoms', 'behaviour_description')
    search_fields = ('user', 'client_name', 'report_notes', 'date_in')
    list_filter = ('client_name', 'date_in')


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_in', 'time_in', 'date_out', 'time_out', 'report_notes')  # Fields to display in list view
    search_fields = ('user__username', 'date_in', 'report_note')
    list_filter = ('date_in',)


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_title', 'client_name', 'severity', 'date', 'time', 'report_notes')
    search_fields = ('user__username', 'report_title', 'client_name', 'report_notes')
    list_filter = ('severity', 'date')



class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone", "is_staff", "is_active")
    
    fieldsets = (
        (None, {"fields": ("username",)}),  # Removed password field
        (_("Personal Info"), {"fields": ("email", "phone")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    exclude = ("password",)  # This completely hides the password field

admin.site.register(User, CustomUserAdmin)