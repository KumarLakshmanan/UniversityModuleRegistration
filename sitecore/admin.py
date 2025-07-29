from django.contrib import admin
from .models import ContactMessage, SystemStats


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for ContactMessage model."""
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        """Mark selected messages as read."""
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        """Mark selected messages as replied."""
        queryset.update(is_replied=True)
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    actions = [mark_as_read, mark_as_replied]


@admin.register(SystemStats)
class SystemStatsAdmin(admin.ModelAdmin):
    """Admin interface for SystemStats model."""
    list_display = [
        'last_updated', 'total_students', 'total_modules', 
        'total_registrations', 'active_modules'
    ]
    list_filter = ['last_updated']
    readonly_fields = [
        'total_students', 'total_modules', 'total_registrations',
        'active_modules', 'last_updated'
    ]
    
    def has_add_permission(self, request):
        """Prevent manual creation of stats."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent modification of stats."""
        return False
