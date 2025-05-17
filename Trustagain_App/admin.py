from django.contrib import admin
from .models import User, InputData, ShiftNarrative, TimeSheet, IncidentReport
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django import forms
from .models import TimeSheet
from django.utils.timezone import localtime
from django.forms.widgets import TimeInput
from django.contrib import admin
from import_export.admin import ExportMixin
from django.contrib import admin
from .models import IncidentReport
from import_export import resources, fields
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME  # ✅ correct for Django 5.1
from django.http import HttpResponse
from import_export.formats.base_formats import CSV
#from .resources import IncidentReportResource
from import_export.formats.base_formats import XLSX







# Change the admin site header
admin.site.site_header = "TrustAgain Residential Services"
admin.site.site_title = "TrustAgain Residential Services Portal"
admin.site.index_title = "Welcome to TrustAgain Residential Services Admin"

# this is used to export my file
class IncidentReportResource(resources.ModelResource):
    username = fields.Field(attribute='user__username', column_name='User')
    Report_title = fields.Field(attribute='report_title', column_name='Report Title')
    client = fields.Field(attribute='client_name', column_name='Client Name')  # if it's a CharField or ForeignKey
    date = fields.Field(attribute='date', column_name='Date')
    time = fields.Field(attribute='time', column_name='Time')
    title = fields.Field(attribute='report_title', column_name='Report Title')
    notes = fields.Field(attribute='report_notes', column_name='Report Notes')
    severity = fields.Field(attribute='severity', column_name='Severity')

    class Meta:
        model = IncidentReport
        fields = (
            'id',
            'username',
            'title',
            'client',
            'severity',
            'notes',
            'date',
            'time',
            'Report_title',
            'Report_notes',
            'created_at',
        )
        export_order = (
            'id',
            'username',
            'title',
            'client',
            'severity',
            'notes',
            'date',
            'time',
            'Report_title',
            'Report_notes',
            'created_at',
            
        )
        

class TimeSheetResource(resources.ModelResource):
    username = fields.Field(attribute='user__username', column_name='User')
    #client = fields.Field(attribute='client_name', column_name='Client Name')  # if it's a CharField or ForeignKey
    date_in = fields.Field(attribute='date_in', column_name='Date In')
    time_in = fields.Field(attribute='time_in', column_name='Time In')
    date_out = fields.Field(attribute='date_out', column_name='Date Out')
    time_out = fields.Field(attribute='time_out', column_name='Time Out')
    report_notes = fields.Field(attribute='report_notes', column_name='Report Notes')
   
    class Meta:
        model = TimeSheet
        fields = (
            'id',
            'username',
            'date_in',
            'Time_in',
            'Time_out',
            'date_out',
            'report_notes',
        )
        export_order = (
            'id',
            'username',
            'date_in',
            'Time_in',
            'Time_out',
            'date_out',
            'report_notes',
        )
class ShiftNarrativeResource(resources.ModelResource):
    username = fields.Field(attribute='user__username', column_name='User')
    client_name = fields.Field(attribute='client_name', column_name='Client Name')  # if it's a CharField or ForeignKey
    date_in = fields.Field(attribute='date_in', column_name='Date In')
    time_in = fields.Field(attribute='time_in', column_name='Time In')
    date_out = fields.Field(attribute='date_out', column_name='Date Out')
    time_out = fields.Field(attribute='time_out', column_name='Time Out')
    report_notes = fields.Field(attribute='report_notes', column_name='Report Notes')
    bm_times = fields.Field(attribute='bm_times', column_name='BM Times')
    bm_size = fields.Field(attribute='bm_size', column_name='BM Size')
    symptoms = fields.Field(attribute='symptoms', column_name='Symptoms')
    behaviour_description = fields.Field(attribute='behaviour_description', column_name='Behaviour Description')
    created_at = fields.Field(attribute='created_at', column_name='Created At')
    class Meta:
        model = ShiftNarrative
        fields = (
            'id',
            'username',
            'Client_name',
            'date_in',
            'Time_in',
            'Time_out',
            'date_out',
            'report_notes',
            'bm_times',
            'bm_size',
            'symptoms',
            'behaviour_description',
            'created_at',
        )
        export_order = (
            'id',
            'username',
            'client_name',
            'date_in',
            'Time_in',
            'Time_out',
            'date_out',
            'report_notes',
            'bm_times',
            'bm_size',
            'symptoms',
            'behaviour_description',
            'created_at',
        )
#===================================================  
# Export as CSV for Incident Report
@admin.action(description="Export selected reports as CSV")
def export_selected_incidents_csv(modeladmin, request, queryset):
    resource = IncidentReportResource()
    dataset = resource.export(queryset)
    export_format = CSV()
    export_data = export_format.export_data(dataset)

    response = HttpResponse(export_data, content_type=export_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename="selected_incident_reports.csv"'
    return response

# Export as Excel for Incident Report
@admin.action(description="Export selected reports as Excel")
def export_selected_incidents_excel(modeladmin, request, queryset):
    resource = IncidentReportResource()
    dataset = resource.export(queryset)
    export_format = XLSX()
    export_data = export_format.export_data(dataset)

    response = HttpResponse(export_data, content_type=export_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename="selected_incident_reports.xlsx"'
    return response

# Export as CSV for Shift Narrative
@admin.action(description="Export selected reports as CSV")
def export_selected_shift_narrative_csv(modeladmin, request, queryset):
    resource = ShiftNarrativeResource()
    dataset = resource.export(queryset)
    export_format = CSV()
    export_data = export_format.export_data(dataset)

    response = HttpResponse(export_data, content_type=export_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename="selected_shift_narrative_reports.csv"'
    return response

# Export as Excel for shift narrative
@admin.action(description="Export selected reports as Excel")
def export_selected_shift_narrative_excel(modeladmin, request, queryset):
    resource = ShiftNarrativeResource()
    dataset = resource.export(queryset)
    export_format = XLSX()
    export_data = export_format.export_data(dataset)

    response = HttpResponse(export_data, content_type=export_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename="selected_shift_narrative_reports.xlsx"'
    return response


# Export as CSV for time sheet
@admin.action(description="Export selected reports as CSV")
def export_selected_time_sheet_csv(modeladmin, request, queryset):
    resource = TimeSheetResource()
    dataset = resource.export(queryset)
    export_format = CSV()
    export_data = export_format.export_data(dataset)

    response = HttpResponse(export_data, content_type=export_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename="selected_time_sheet_reports.csv"'
    return response

# Export as Excel for time sheet
@admin.action(description="Export selected reports as Excel")
def export_selected_time_sheet_excel(modeladmin, request, queryset):
    resource = TimeSheetResource()
    dataset = resource.export(queryset)
    export_format = XLSX()
    export_data = export_format.export_data(dataset)

    response = HttpResponse(export_data, content_type=export_format.get_content_type())
    response['Content-Disposition'] = 'attachment; filename="selected_time_sheet_reports.xlsx"'
    return response










class TimeSheetAdminForm(forms.ModelForm):
    class Meta:
        model = TimeSheet
        fields = '__all__'
        widgets = {
            'time_in': forms.TimeInput(format='%H:%M:%S', attrs={'type': 'time'}),
            'time_out': forms.TimeInput(format='%H:%M:%S', attrs={'type': 'time'}),
        }



@admin.register(ShiftNarrative)
class ShiftNarrativeAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = ShiftNarrativeResource
    list_display = (
        'user', 'client_name', 'date_in', 'Time_in', 'Time_out', 'date_out',
        'report_notes', 'bm_times', 'bm_size', 'symptoms', 'behaviour_description'
    )
    search_fields = ('user__username', 'client_name', 'report_notes', 'date_in')
    list_filter = ('client_name', 'date_in')
    actions = [export_selected_shift_narrative_csv, export_selected_shift_narrative_excel] # this is used to export as cvs or excel


#using time widjet
class TimeSheetForm(forms.ModelForm):
    class Meta:
        model = TimeSheet
        fields = '__all__'
        widgets = {
            'time_in': TimeInput(
                format='%H:%M', attrs={'type': 'time'}  # uses 24-hour HTML5 picker
            ),
            'time_out': TimeInput(
                format='%H:%M', attrs={'type': 'time'}
            ),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_in'].input_formats = ['%H:%M', '%I:%M %p']
        self.fields['time_out'].input_formats = ['%H:%M', '%I:%M %p']


@admin.register(TimeSheet)
class TimeSheetAdmin(ExportMixin, admin.ModelAdmin):
    form = TimeSheetForm
    resource_class = TimeSheetResource
    list_display = ('user', 'date_in', 'formatted_time_in', 'date_out', 'formatted_time_out', 'report_notes', 'duration')
    search_fields = ('user__username', 'date_in', 'report_notes')
    list_filter = ('date_in',)
    actions = [export_selected_time_sheet_csv, export_selected_time_sheet_excel] # this is used to export as cvs or excel


    def formatted_time_in(self, obj):
        if obj.time_in:
            return obj.time_in.strftime('%I:%M %p')
        return "-"
    formatted_time_in.short_description = 'Time In'

    def formatted_time_out(self, obj):
        if obj.time_out:
            return obj.time_out.strftime('%I:%M %p')
        return "-"
    formatted_time_out.short_description = 'Time Out'

    def duration(self, obj):
        return obj.duration_hours()
    duration.short_description = 'Hours Worked'
    ## change_list_template = 'admin/timesheet_changelist.html'  ## this will be redirected to html file in templates folder

    def changelist_view(self, request, extra_context=None):
        queryset = self.get_queryset(request)
        user_hours = {}

        for obj in queryset:
            user = obj.user
            hours = obj.duration_hours() or 0
            user_hours[user] = user_hours.get(user, 0) + hours

        extra_context = extra_context or {}
        extra_context['user_hours'] = user_hours
        return super().changelist_view(request, extra_context=extra_context)




@admin.register(IncidentReport)
class IncidentReportAdmin(ExportMixin,admin.ModelAdmin):
    resource_class = IncidentReportResource
    list_display = ('user', 'report_title', 'client_name', 'severity', 'date', 'time', 'report_notes')
    search_fields = ('user__username', 'report_title', 'client_name', 'report_notes')
    list_filter = ('severity', 'date')
    actions = [export_selected_incidents_csv, export_selected_incidents_excel] # this is used to export as cvs or excel



# === Custom User Admin ===
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone", "is_staff", "is_active")
    
    fieldsets = (
        (None, {"fields": ("username",)}),
        (_("Personal Info"), {"fields": ("email", "phone")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    exclude = ("password",)  # Hide password field in admin

#admin.site.register(User, CustomUserAdmin)

