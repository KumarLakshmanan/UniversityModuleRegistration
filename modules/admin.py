from django.contrib import admin
from .models import Course, Module, Registration


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_credits', 'total_modules', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'total_credits', 'total_modules']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Statistics', {
            'fields': ('total_credits', 'total_modules'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def total_credits(self, obj):
        return obj.total_credits
    total_credits.short_description = 'Total Credits'

    def total_modules(self, obj):
        return obj.total_modules
    total_modules.short_description = 'Total Modules'


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credit', 'course', 'availability', 'current_enrollment', 'available_spots']
    list_filter = ['credit', 'availability', 'created_at', 'course', 'category']
    search_fields = ['name', 'code', 'description', 'course__name']
    prepopulated_fields = {'code': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'current_enrollment', 'available_spots', 'is_full']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Module Details', {
            'fields': ('course', 'credit', 'category', 'availability', 'max_students')
        }),
        ('Statistics', {
            'fields': ('current_enrollment', 'available_spots', 'is_full'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def current_enrollment(self, obj):
        return obj.current_enrollment
    current_enrollment.short_description = 'Current Enrollment'

    def available_spots(self, obj):
        return obj.available_spots
    available_spots.short_description = 'Available Spots'

    def is_full(self, obj):
        return obj.is_full
    is_full.boolean = True
    is_full.short_description = 'Full'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'module', 'module_course', 'date_registered']
    list_filter = ['date_registered']
    search_fields = ['student__user__username', 'student__user__first_name', 'student__user__last_name', 'module__name', 'module__code']
    raw_id_fields = ['student', 'module']
    readonly_fields = ['date_registered']
    
    def module_course(self, obj):
        return obj.module.course.name if obj.module and obj.module.course else '-'
    module_course.short_description = 'Module Course'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student__user', 'module__course')
