from django.contrib import admin
from .models import Module

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits', 'semester', 'is_active']
    list_filter = ['semester', 'is_active', 'credits']
    search_fields = ['code', 'name', 'description']
    ordering = ['code']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Module Information', {
            'fields': ('code', 'name', 'description')
        }),
        ('Academic Details', {
            'fields': ('credits', 'semester', 'prerequisites')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
