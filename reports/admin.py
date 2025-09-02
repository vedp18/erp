from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("name", "report_type", "generated_on")
    list_filter = ("report_type", "generated_on")
