from django.contrib import admin
from .models import Module, Registration


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credit', 'category', 'availability', 'registered_students_count', 'available_spots', 'is_full']
    list_filter = ['category', 'availability', 'credit', 'created_at']
    search_fields = ['name', 'code', 'description']
    prepopulated_fields = {'code': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'registered_students_count', 'available_spots', 'is_full']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Module Details', {
            'fields': ('credit', 'category', 'availability', 'max_students')
        }),
        ('Statistics', {
            'fields': ('registered_students_count', 'available_spots', 'is_full'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def registered_students_count(self, obj):
        return obj.registered_students_count
    registered_students_count.short_description = 'Registered Students'

    def available_spots(self, obj):
        return obj.available_spots
    available_spots.short_description = 'Available Spots'

    def is_full(self, obj):
        return obj.is_full
    is_full.boolean = True
    is_full.short_description = 'Full'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'module', 'date_registered']
    list_filter = ['date_registered', 'module__category']
    search_fields = ['student__user__username', 'student__user__first_name', 'student__user__last_name', 'module__name', 'module__code']
    raw_id_fields = ['student', 'module']
    readonly_fields = ['date_registered']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student__user', 'module')
