from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'is_remote', 'salary', 'posted_date')
    list_filter = ('is_remote', 'location', 'posted_date')
    search_fields = ('title', 'company', 'location', 'description')
    ordering = ('-posted_date',)
    date_hierarchy = 'posted_date'