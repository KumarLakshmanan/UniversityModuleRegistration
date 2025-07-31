from django.contrib import admin
from .models import Module

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits', 'category', 'is_active']
    list_filter = ['category', 'is_active', 'credits']
    search_fields = ['code', 'name', 'description']
    ordering = ['code']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Module Information', {
            'fields': ('code', 'name', 'description', 'image_url')
        }),
        ('Academic Details', {
            'fields': ('credits', 'max_students', 'category', 'prerequisites')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
