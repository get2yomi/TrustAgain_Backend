from django.contrib import admin
from .models import User, InputData
from .models import ShiftNarrative
from .models import TimeSheet
from .models import IncidentReport






# Register your models here.
admin.site.register(User) # now if we go to our model we will see user in it
admin.site.register(InputData)
@admin.register(ShiftNarrative)
class ShiftNarrativeAdmin(admin.ModelAdmin):
    list_display = ('staff_name', 'client_name', 'date_in', 'Time_in', 'Time_out', 'date_out', 'report_notes')
    search_fields = ('staff_name', 'client_name', 'report_notes', 'date_in')
    list_filter = ('client_name', 'date_in')


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_in', 'time_in', 'date_clock_out', 'time_clock_out', 'report_note')  # Fields to display in list view
    search_fields = ('user__username', 'date_in', 'report_note')
    list_filter = ('date_in',)


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'report_title', 'client_name', 'severity', 'date', 'time', 'report_notes')
    search_fields = ('user__username', 'report_title', 'client_name', 'report_notes')
    list_filter = ('severity', 'date')
