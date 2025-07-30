from django.contrib import admin
from .models import Contact

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False  # Prevent adding contacts through admin
        
    def has_change_permission(self, request, obj=None):
        return False  # Make contacts read-only
