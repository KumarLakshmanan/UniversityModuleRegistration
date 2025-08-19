from django.contrib import admin
from .models import Course, Module


class ModuleInline(admin.TabularInline):
    """Inline admin for modules within a course."""
    model = Module
    extra = 1
    fields = ['code', 'name', 'credits', 'category', 'status']
    readonly_fields = []


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""
    list_display = [
        'course_code', 'title', 'status', 
        'is_available_for_registration', 'module_count', 'total_credits', 'enrolled_count'
    ]
    list_filter = ['status', 'is_available_for_registration']
    search_fields = ['course_code', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'course_code': ('title',)}
    inlines = [ModuleInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course_code', 'title', 'description')
        }),
        ('Availability', {
            'fields': ('status', 'is_available_for_registration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def module_count(self, obj):
        """Display number of modules in the course."""
        return obj.module_count
    module_count.short_description = 'Modules'
    
    def total_credits(self, obj):
        """Display total credits for the course."""
        return obj.total_credits
    total_credits.short_description = 'Total Credits'
    
    def enrolled_count(self, obj):
        """Display number of enrolled students."""
        return obj.enrolled_students_count
    enrolled_count.short_description = 'Enrolled Students'


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin interface for Module model."""
    list_display = [
        'full_code', 'name', 'course', 'credits', 'category', 
        'status', 'is_available_for_registration'
    ]
    list_filter = ['course', 'category', 'status', 'is_available_for_registration', 'credits']
    search_fields = ['code', 'name', 'description', 'course__title', 'course__course_code']
    readonly_fields = ['created_at', 'updated_at', 'full_code']
    prepopulated_fields = {'code': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'code', 'name', 'description', 'category', 'image_url')
        }),
        ('Academic Details', {
            'fields': ('credits', 'prerequisites')
        }),
        ('Availability', {
            'fields': ('status', 'is_available_for_registration', 'max_students')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'full_code'),
            'classes': ('collapse',)
        }),
    )
    
    def full_code(self, obj):
        """Display full module code."""
        return obj.full_code
    full_code.short_description = 'Full Code'
