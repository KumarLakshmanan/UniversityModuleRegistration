from django.contrib import admin
from .models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin interface for Module model."""
    list_display = [
        'code', 'name', 'credits', 'category', 
        'status', 'is_available_for_registration', 'enrolled_count'
    ]
    list_filter = ['category', 'status', 'is_available_for_registration', 'credits']
    search_fields = ['code', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'code': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description', 'category')
        }),
        ('Academic Details', {
            'fields': ('credits', 'prerequisites')
        }),
        ('Availability', {
            'fields': ('status', 'is_available_for_registration', 'max_students')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def enrolled_count(self, obj):
        """Display number of enrolled students."""
        return obj.enrolled_students_count
    enrolled_count.short_description = 'Enrolled Students'
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch."""
        return super().get_queryset(request).prefetch_related('registrations')
