from django.contrib import admin
from .models import *

# admin.site.register(Project)
# admin.site.register(UrlDetail)
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'education_level', 'country', 'is_active')
    list_filter = ('education_level', 'is_active', 'country')
    search_fields = ('name', 'email', 'address')
    list_editable = ('is_active',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'passport_number', 'education_level', 'country', 'created_at')
    list_filter = ('education_level', 'gender', 'test_type', 'created_at')
    search_fields = ('full_name', 'passport_number', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'dob', 'gender', 'photo')
        }),
        ('Passport & Visa', {
            'fields': ('passport_number', 'passport_issue', 'passport_expiry', 'oldin_otkaz', 'country', 'bankshot')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address', 'zipcode')
        }),
        ('Academic Background', {
            'fields': ('test_type', 'score', 'test_date', 'expiry_date', 'education_level', 'prev_major', 'diplom_number', 'gpa', 'grad_date')
        }),
        ('University Interests', {
            'fields': ('uni_phone', 'uni_website', 'uni_email', 'uni_address')
        }),
        ('Family - Father', {
            'fields': ('father_name', 'father_passport', 'father_dob', 'father_phone', 'father_job')
        }),
        ('Family - Mother', {
            'fields': ('mother_name', 'mother_passport', 'mother_dob', 'mother_phone', 'mother_job')
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )