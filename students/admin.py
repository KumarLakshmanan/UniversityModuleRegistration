from django.contrib import admin
from .models import Student, OTP


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student model."""
    list_display = [
        'user', 'is_verified', 'phone', 'created_at'
    ]
    list_filter = ['is_verified', 'created_at']
    search_fields = [
        'user__username', 'user__email', 
        'user__first_name', 'user__last_name', 'phone'
    ]
    readonly_fields = ['created_at']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'is_verified')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'phone', 'address', 'city', 'country')
        }),
        ('Profile', {
            'fields': ('photo',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Customize queryset to include related user data."""
        return super().get_queryset(request).select_related('user')


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """Admin interface for OTP model."""
    list_display = [
        'user', 'purpose', 'otp_code', 'is_used', 'expires_at', 'created_at'
    ]
    list_filter = ['purpose', 'is_used', 'created_at']
    search_fields = ['user__username', 'user__email', 'otp_code']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        """Customize queryset to include related user data."""
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        """Prevent manual creation of OTPs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent modification of OTPs."""
        return False
