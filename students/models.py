from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import random
import string
from django.utils import timezone
from datetime import timedelta


class Student(models.Model):
    """Student profile model extending Django User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.username})"

    def get_absolute_url(self):
        return reverse('students:profile', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def registered_modules_count(self):
        return self.registrations.count()

    @property 
    def registered_courses_count(self):
        return self.course_registrations.count()


class EmailVerification(models.Model):
    """Model to handle email verification via OTP"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_otp()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))

    def is_expired(self):
        """Check if OTP is expired"""
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp}"

    class Meta:
        ordering = ['-created_at']


class PasswordResetOTP(models.Model):
    """Model to handle password reset via OTP"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.generate_otp()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))

    def is_expired(self):
        """Check if OTP is expired"""
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Password Reset OTP for {self.user.email} - {self.otp}"

    class Meta:
        ordering = ['-created_at']
