from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """Admin interface for Registration model."""
    list_display = [
        'student', 'module', 'status', 'date_registered', 
        'completion_date', 'grade', 'is_active'
    ]
    list_filter = ['status', 'is_active', 'date_registered', 'grade']
    search_fields = [
        'student__user__username', 
        'student__user__email', 'module__code', 'module__name'
    ]
    readonly_fields = ['date_registered']
    
    fieldsets = (
        ('Registration Details', {
            'fields': ('student', 'module', 'status', 'is_active')
        }),
        ('Academic Information', {
            'fields': ('grade', 'completion_date')
        }),
        ('Timestamps', {
            'fields': ('date_registered',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'student__user', 'module'
        )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Customize foreign key fields."""
        if db_field.name == "student":
            kwargs["queryset"] = db_field.related_model.objects.select_related('user')
        elif db_field.name == "module":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
