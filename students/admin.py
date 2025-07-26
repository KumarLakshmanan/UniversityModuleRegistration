from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Student, EmailVerification, PasswordResetOTP


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'country', 'is_email_verified', 'registered_modules_count', 'created_at']
    list_filter = ['is_email_verified', 'country', 'city', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'registered_modules_count']
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp', 'is_used', 'created_at', 'expires_at', 'is_expired']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'expires_at']

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp', 'is_used', 'created_at', 'expires_at', 'is_expired']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'expires_at']

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True


# Re-register User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
